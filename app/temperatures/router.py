from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.cities.models import City
from sqlalchemy import select
from app.temperatures.schemas import TemperatureRead
from app.temperatures import crud
from app.temperatures.services.weather import fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])

@router.get("/", response_model=list[TemperatureRead])
async def read_temperatures(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(db, city_id)

@router.post("/update")
async def update_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        result = await db.scalars(select(City))
        cities = result.all()

        created = 0

        for city in cities:
            temperature = await fetch_current_temperature(
                city.latitude,
                city.longitude,
            )

            await crud.create_temperature(
                db=db,
                city_id=city.id,
                temperature=temperature,
            )

            created += 1

        return {
            "status": "ok",
            "records_created": created,
        }

    except Exception as e:
        await db.rollback()
        raise e
