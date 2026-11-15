from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Transport Service API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# DTO (модель данных на основе Pydantic)
class RouteModel(BaseModel):
    id: int
    name: str
    start_point: str
    end_point: str
    distance: float

class RouteCreateDTO(BaseModel):
    name: str
    start_point: str
    end_point: str
    distance: float

# In-Memory хранилище (заглушка)
fake_routes_db = [
    RouteModel(id=1, name="Маршрут 1", start_point="Москва", end_point="Санкт-Петербург", distance=700.5),
    RouteModel(id=2, name="Маршрут 2", start_point="Казань", end_point="Екатеринбург", distance=950.0)
]

@app.get("/api/v1/routes/", response_model=List[RouteModel], status_code=status.HTTP_200_OK)
def get_routes():
    """Получение списка всех объектов маршрутов."""
    return fake_routes_db

@app.get("/api/v1/routes/{id}", response_model=RouteModel, status_code=status.HTTP_200_OK)
def get_route_by_id(id: int):
    """Получение детальной информации об объекте по его ID."""
    for route in fake_routes_db:
        if route.id == id:
            return route
    raise HTTPException(status_code=404, detail="Маршрут не найден")

@app.post("/api/v1/routes/", response_model=RouteModel, status_code=status.HTTP_201_CREATED)
def create_route(route_data: RouteCreateDTO):
    """Создание нового объекта маршрута."""
    new_id = max([r.id for r in fake_routes_db], default=0) + 1
    new_route = RouteModel(id=new_id, **route_data.dict())
    fake_routes_db.append(new_route)
    return new_route

@app.delete("/api/v1/routes/{id}", status_code=status.HTTP_200_OK)
def delete_route(id: int):
    """Удаление объекта по ID."""
    for index, route in enumerate(fake_routes_db):
        if route.id == id:
            del fake_routes_db[index]
            return {"detail": f"Маршрут с id={id} успешно удален"}
    raise HTTPException(status_code=404, detail="Маршрут не найден")