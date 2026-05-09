from fastapi import APIRouter, Query
from services.excel_services import (
    get_course_data,
    get_faculty_data,
    get_population_data,
    get_subjects,
    get_worst_subjects_data,
)

router = APIRouter()

# curl "http://localhost:8000/api/data/get_worst_subjects_data?subject=STAT"

@router.get("/data/get_worst_subjects_data")
async def get_worst_subjects(subject: str = Query(..., example="STAT")):
    return get_worst_subjects_data(subject)


@router.get("/data/get_faculty_data")
async def faculty_data(faculty: str = Query(..., example="SCI")):
    return get_faculty_data(faculty)


@router.get("/data/get_course_data")
async def course_data(course: str = Query(..., example="ACMA 101")):
    return get_course_data(course)


@router.get("/data/get_population_data")
async def population_data():
    return get_population_data()


@router.get("/data/get_subjects")
async def subjects_data(faculty: str | None = Query(default=None, example="SCI")):
    return get_subjects(faculty)
