from fastapi import APIRouter
from services.excel_service import get_char_data

router = APIRouter()

@router.get("/data")
async df et_data():
    data = get_chart_)data()
    return data