import os
from typing import Dict

import pandas as pd


RAW_SHEET_NAME = "Raw Grade Data"
EXCEL_FILE_NAME = "gatekeeper_d_cutoff_202223.xlsx"

GRADE_COUNT_COLUMNS = [
    "# A+",
    "# A",
    "# A-",
    "# B+",
    "# B",
    "# B-",
    "# C+",
    "# C",
    "# C-",
    "# D",
    "# F",
    "# FD",
    "# N",
    "# W",
    "# P",
    "# P*",
    "# CR",
    "# NC",
]

GPA_GRADE_COLUMNS = {
    "# A+": 4.33,
    "# A": 4.00,
    "# A-": 3.67,
    "# B+": 3.33,
    "# B": 3.00,
    "# B-": 2.67,
    "# C+": 2.33,
    "# C": 2.00,
    "# C-": 1.67,
    "# D": 1.00,
    "# F": 0.00,
}


def _resolve_excel_path() -> str:
    """
    Resolve the Excel file path from env override or common local locations.
    """
    env_path = os.getenv("GATE_EXCEL_PATH")
    if env_path and os.path.exists(env_path):
        return os.path.abspath(env_path)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(base_dir, "..", "data", EXCEL_FILE_NAME)),
    return path


def _extract_course_level(catalog_number: str) -> str:
    catalog = "".join(ch for ch in str(catalog_number) if ch.isdigit())
    if not catalog:
        return "Unknown"
    return f"{catalog[0]}00-level"


def _safe_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator.div(denominator.where(denominator > 0, pd.NA)).fillna(0.0)


def _prepare_raw_grade_data() -> pd.DataFrame:
    excel_path = _resolve_excel_path()
    data = pd.read_excel(excel_path, sheet_name=RAW_SHEET_NAME).copy()

    data["Course Faculty"] = data["Course Faculty"].astype(str).str.strip().str.upper()
    data["Course Subject"] = data["Course Subject"].astype(str).str.strip().str.upper()
    data["Catalog Number"] = data["Catalog Number"].astype(str).str.strip()
    data["Course"] = data["Course"].astype(str).str.strip()

    if "W Status" in data.columns:
        data["W Status"] = data["W Status"].astype(str).str.strip()
    else:
        data["W Status"] = ""

    numeric_columns = list(dict.fromkeys(GRADE_COUNT_COLUMNS + ["Total #", "Total # (incl # W)"]))
    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)
        else:
            data[col] = 0

    data["course_code"] = data["Course Subject"] + " " + data["Catalog Number"]
    data["course_level"] = data["Catalog Number"].map(_extract_course_level)
    data["total_students"] = data["Total # (incl # W)"]
    data["dfw_count"] = data["# D"] + data["# F"] + data["# W"]
    data["withdraw_count"] = data["# W"]
    data["dfw_rate"] = _safe_ratio(data["dfw_count"], data["total_students"])
    data["withdraw_rate"] = _safe_ratio(data["withdraw_count"], data["total_students"])

    gpa_numerator = sum(data[col] * weight for col, weight in GPA_GRADE_COLUMNS.items())
    gpa_denominator = sum(data[col] for col in GPA_GRADE_COLUMNS.keys())
    data["avg_gpa"] = _safe_ratio(gpa_numerator, gpa_denominator)

    w_status_norm = data["W Status"].str.upper()
    data["is_w_course"] = (~w_status_norm.isin(["", "NAN", "NONE", "NO", "N", "0"])).astype(int)
    return data


raw_data = _prepare_raw_grade_data()


def get_worst_subjects_data(subject: str) -> Dict[str, int]:
    """
    Fetch the top 10 worst-performing courses in a subject by D/F counts.
    Returns a dict used directly by the donut chart.
    """
    subject_key = str(subject).strip().upper()
    subject_data = raw_data[raw_data["Course Subject"] == subject_key]
    if subject_data.empty:
        return {"Others": 0}

    grouped = (
        subject_data.groupby("course_code", as_index=False)[["# D", "# F"]]
        .sum()
        .assign(total_failed=lambda df: df["# D"] + df["# F"])
        .sort_values("total_failed", ascending=False)
    )

    top10 = grouped.head(10)
    top_courses = set(top10["course_code"])
    others_total = int(grouped[~grouped["course_code"].isin(top_courses)]["total_failed"].sum())

    result = {row["course_code"]: int(row["total_failed"]) for _, row in top10.iterrows()}
    result["Others"] = others_total
    return result


def get_faculty_data(faculty: str) -> Dict[str, object]:
    """
    Aggregate department-level performance summary for one faculty.
    """
    faculty_key = str(faculty).strip().upper()
    faculty_data = raw_data[raw_data["Course Faculty"] == faculty_key]
    if faculty_data.empty:
        return {"faculty": faculty_key, "subjects": []}

    grouped = (
        faculty_data.groupby("Course Subject", as_index=False)
        .agg(
            total_students=("total_students", "sum"),
            withdraw_count=("withdraw_count", "sum"),
            dfw_count=("dfw_count", "sum"),
            avg_gpa=("avg_gpa", "mean"),
            active_courses=(
                "Offered in the Last 3 Terms",
                lambda s: int(s.astype(str).str.strip().str.upper().eq("YES").sum()),
            ),
            total_courses=("course_code", "nunique"),
        )
        .sort_values("total_students", ascending=False)
    )
    grouped["withdraw_rate"] = _safe_ratio(grouped["withdraw_count"], grouped["total_students"])
    grouped["dfw_rate"] = _safe_ratio(grouped["dfw_count"], grouped["total_students"])

    return {"faculty": faculty_key, "subjects": grouped.to_dict(orient="records")}


def get_course_data(course: str) -> Dict[str, object]:
    """
    Return grade distribution and key metrics for a specific course code.
    Accepts forms like 'ACMA 101' or 'ACMA101'.
    """
    normalized = str(course).strip().upper().replace(" ", "")
    course_rows = raw_data[raw_data["course_code"].str.replace(" ", "", regex=False) == normalized]
    if course_rows.empty:
        return {"course": str(course).strip().upper(), "records": 0, "grades": {}, "percentages": {}}

    grade_totals = course_rows[GRADE_COUNT_COLUMNS].sum()
    total_students = float(course_rows["total_students"].sum())
    total_gpa_base = float(course_rows[list(GPA_GRADE_COLUMNS.keys())].sum().sum())
    gpa_numerator = float(
        sum(course_rows[col].sum() * weight for col, weight in GPA_GRADE_COLUMNS.items())
    )
    avg_gpa = (gpa_numerator / total_gpa_base) if total_gpa_base > 0 else 0.0

    percentages = (
        (grade_totals / total_students).fillna(0).replace([pd.NA], 0).to_dict()
        if total_students > 0
        else {k: 0.0 for k in GRADE_COUNT_COLUMNS}
    )

    return {
        "course": course_rows["course_code"].iloc[0],
        "records": int(len(course_rows)),
        "course_faculties": sorted(course_rows["Course Faculty"].dropna().unique().tolist()),
        "w_status_values": sorted(course_rows["W Status"].dropna().unique().tolist()),
        "course_level": course_rows["course_level"].iloc[0],
        "total_students": int(total_students),
        "withdraw_count": int(grade_totals.get("# W", 0)),
        "dfw_count": int(grade_totals.get("# D", 0) + grade_totals.get("# F", 0) + grade_totals.get("# W", 0)),
        "withdraw_rate": float((grade_totals.get("# W", 0) / total_students) if total_students > 0 else 0.0),
        "dfw_rate": float(
            ((grade_totals.get("# D", 0) + grade_totals.get("# F", 0) + grade_totals.get("# W", 0)) / total_students)
            if total_students > 0
            else 0.0
        ),
        "avg_gpa": float(avg_gpa),
        "grades": {k: int(v) for k, v in grade_totals.to_dict().items()},
        "percentages": {k: float(v) for k, v in percentages.items()},
    }


def get_population_data() -> Dict[str, object]:
    """
    Return broad university-level aggregates used by multiple dashboards.
    """
    total_students = float(raw_data["total_students"].sum())
    total_withdraw = float(raw_data["withdraw_count"].sum())
    total_dfw = float(raw_data["dfw_count"].sum())

    top_dfw_courses = (
        raw_data.groupby("course_code", as_index=False)
        .agg(dfw_count=("dfw_count", "sum"), total_students=("total_students", "sum"))
        .sort_values("dfw_count", ascending=False)
        .head(10)
    )
    top_dfw_courses["dfw_rate"] = _safe_ratio(top_dfw_courses["dfw_count"], top_dfw_courses["total_students"])

    by_course_level = (
        raw_data.groupby("course_level", as_index=False)
        .agg(avg_gpa=("avg_gpa", "mean"), withdraw_rate=("withdraw_rate", "mean"), courses=("course_code", "nunique"))
        .sort_values("course_level")
    )

    by_w_status = (
        raw_data.groupby("is_w_course", as_index=False)
        .agg(
            rows=("course_code", "count"),
            total_students=("total_students", "sum"),
            avg_gpa=("avg_gpa", "mean"),
            withdraw_rate=("withdraw_rate", "mean"),
            dfw_rate=("dfw_rate", "mean"),
        )
        .assign(group=lambda df: df["is_w_course"].map({1: "W", 0: "Non-W"}))
        .drop(columns=["is_w_course"])
    )

    return {
        "total_records": int(len(raw_data)),
        "total_students": int(total_students),
        "withdraw_rate": float((total_withdraw / total_students) if total_students > 0 else 0.0),
        "dfw_rate": float((total_dfw / total_students) if total_students > 0 else 0.0),
        "top_dfw_courses": top_dfw_courses.to_dict(orient="records"),
        "course_level_difficulty": by_course_level.to_dict(orient="records"),
        "w_vs_non_w_summary": by_w_status.to_dict(orient="records"),
    }