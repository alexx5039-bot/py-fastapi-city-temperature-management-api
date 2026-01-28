from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cities.models import City
from app.cities.schemas import CityCreate, CityUpdate


async def get_all_cities(db: AsyncSession) -> list[City]:
    stmt = select(City)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> City | None:
    return await db.get(City, city_id)


async def get_city_by_name(db: AsyncSession, name: str) -> City | None:
    stmt = select(City).where(City.name == name)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_city(db: AsyncSession, city_data: CityCreate) -> City:
    city = City(
        name=city_data.name,
        latitude=city_data.latitude,
        longitude=city_data.longitude,
    )
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


async def update_city(
    db: AsyncSession,
    city: City,
    city_data: CityUpdate
) -> City:
    if city_data.name is not None:
        city.name = city_data.name
    if city_data.latitude is not None:
        city.latitude = city_data.latitude
    if city_data.longitude is not None:
        city.longitude = city_data.longitude

    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city: City) -> None:
    await db.delete(city)
    await db.commit()
