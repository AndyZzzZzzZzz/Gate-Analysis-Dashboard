import typing

from fastapi import APIRouter, Query
from services.excel_services import (
    get_faculties,
    get_courses,
    get_course_data,
    get_faculty_grade_heatmap,
    get_faculty_data,
    get_population_data,
    get_subjects,
    get_top_dfw_courses,
    get_worst_subjects_data,
)

router = APIRouter()

# curl "http://localhost:8000/api/data/get_worst_subjects_data?subject=STAT"

@router.get("/data/get_worst_subjects_data")
async def get_worst_subjects(subject: str = Query(..., examples="STAT")):
    return get_worst_subjects_data(subject)


@router.get("/data/get_faculty_data")
async def faculty_data(faculty: str = Query(..., examples="SCI")):
    return get_faculty_data(faculty)


@router.get("/data/get_course_data")
async def course_data(course: str = Query(..., examples="ACMA 101")):
    return get_course_data(course)


@router.get("/data/get_population_data")
async def population_data():
    return get_population_data()


@router.get("/data/get_subjects")
async def subjects_data(faculty: typing.Optional[str] = Query(default=None, examples="SCI")):
    return get_subjects(faculty)


@router.get("/data/get_faculties")
async def faculties_data():
    return get_faculties()


@router.get("/data/get_courses")
async def courses_data(subject: typing.Optional[str] = Query(default=None, examples="STAT")):
    return get_courses(subject)


@router.get("/data/get_faculty_grade_heatmap")
async def faculty_grade_heatmap_data():
    return get_faculty_grade_heatmap()


@router.get("/data/get_top_dfw_courses")
async def top_dfw_courses_data(
    subject: typing.Optional[str] = Query(default=None, examples="STAT"),
    faculty: typing.Optional[str] = Query(default=None, examples="SCI"),
    level: typing.Optional[str] = Query(default=None, examples="100"),
    metric: str = Query(default="ALL", examples="ALL"),
    min_students: typing.Optional[int] = Query(default=None, ge=0),
    limit: int = Query(default=10, ge=1, le=50),
):
    return get_top_dfw_courses(
        subject=subject,
        faculty=faculty,
        level=level,
        metric=metric,
        min_students=min_students,
        limit=limit,
    )
