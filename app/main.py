"""Vehicle Service API.

A Python (FastAPI) implementation of the Vehicle Service API, generated from the
Postman "Vehicle Service Collection".

Endpoints:
    POST   /vehicles       -> create a vehicle           (201 / 400 / 409 / 500)
    GET    /vehicles/{id}  -> retrieve a vehicle          (200 / 404 / 500)
    PATCH  /vehicles/{id}  -> update a vehicle            (200 / 400 / 500)
    DELETE /vehicles/{id}  -> delete a vehicle            (204 / 500)
"""

from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

app = FastAPI(
    title="Vehicle Service API",
    description="Implements the Vehicle Service Collection endpoints.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class VehicleBase(BaseModel):
    nickName: Optional[str] = None
    vin: str
    make: str
    model: str
    year: str
    miles: int


class VehicleUpdate(BaseModel):
    nickName: Optional[str] = None
    vin: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    miles: Optional[int] = None


class Vehicle(VehicleBase):
    id: int


# ---------------------------------------------------------------------------
# In-memory data store (stand-in for a real database)
# ---------------------------------------------------------------------------
_vehicles: dict[int, dict] = {}
_next_id: int = 1

# Required attributes for creating a vehicle.
REQUIRED_ATTRS = ["vin", "make", "model", "year", "miles"]


def _error(message: str) -> dict:
    """Return the standard error body used across the API."""
    return {"message": message}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.post("/vehicles", status_code=status.HTTP_201_CREATED)
def create_vehicle(payload: dict):
    """Create a new vehicle. Returns 201 with the created resource."""
    global _next_id

    # 400 - validate required attributes.
    for attr in REQUIRED_ATTRS:
        if attr not in payload or payload[attr] in (None, ""):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=_error(f"Request body missing required attribute: {attr}"),
            )

    # 409 - reject duplicate VIN.
    vin = payload["vin"]
    for existing in _vehicles.values():
        if existing["vin"] == vin:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=_error(
                    f"Vehicle with VIN {vin} already exists. "
                    f"Existing vehicle ID: {existing['id']}"
                ),
            )

    vehicle = {
        "id": _next_id,
        "nickName": payload.get("nickName"),
        "vin": payload["vin"],
        "make": payload["make"],
        "model": payload["model"],
        "year": payload["year"],
        "miles": payload["miles"],
    }
    _vehicles[_next_id] = vehicle
    _next_id += 1

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=vehicle)


@app.get("/vehicles/{vehicle_id}")
def retrieve_vehicle(vehicle_id: int):
    """Retrieve a vehicle by id. Returns 200, or 404 when not found."""
    vehicle = _vehicles.get(vehicle_id)
    if vehicle is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=_error(f"Vehicle with id: {vehicle_id} not found."),
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=vehicle)


@app.patch("/vehicles/{vehicle_id}")
def update_vehicle(vehicle_id: int, payload: dict):
    """Partially update a vehicle. Returns 200 with the updated resource."""
    vehicle = _vehicles.get(vehicle_id)
    if vehicle is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=_error(f"Vehicle with id: {vehicle_id} not found."),
        )

    # 400 - reject unknown attributes in the body.
    allowed = set(VehicleUpdate.model_fields.keys())
    for key in payload:
        if key not in allowed:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=_error(f"Request body contains invalid attribute: {key}"),
            )

    for key, value in payload.items():
        vehicle[key] = value

    return JSONResponse(status_code=status.HTTP_200_OK, content=vehicle)


@app.delete("/vehicles/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int):
    """Delete a vehicle. Returns 204 No Content."""
    _vehicles.pop(vehicle_id, None)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/")
def root():
    return {"service": "Vehicle Service API", "status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=4500, reload=True)
