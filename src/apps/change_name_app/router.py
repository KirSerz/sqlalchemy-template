from fastapi import APIRouter


router = APIRouter(prefix='/data', tags=['Get all data'])


@router.get("/", summary="Get all data")
async def get_all_data():
    return []