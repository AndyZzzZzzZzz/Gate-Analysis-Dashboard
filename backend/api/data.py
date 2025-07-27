from fastapi import APIRouter
from services.excel_service import get_char_data

router = APIRouter()

@router.get("/data")
async def get_data():
    data = get_chart_data()
    return data



