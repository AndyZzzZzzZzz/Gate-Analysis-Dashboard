from fastapi import APIRouter
from fastapi import Query
from services.excel_services import *

router = APIRouter()

@router.get("/data/get_worst_subjects_data")
async def get_worst_subjects(subject: str = Query(..., example="STAT")):
    data = get_worst_subjects_data(subject)
    return data



