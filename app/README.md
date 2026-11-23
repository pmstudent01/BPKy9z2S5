# Vehicle Service API (Python / FastAPI)

A Python implementation of the **Vehicle Service Collection** from Postman.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --port 4500
```

The API will be available at `http://localhost:4500`.
Interactive docs: `http://localhost:4500/docs`.

## Endpoints

| Method   | Path             | Success | Other responses |
|----------|------------------|---------|-----------------|
| `POST`   | `/vehicles`      | `201`   | `400`, `409`    |
| `GET`    | `/vehicles/{id}` | `200`   | `404`           |
| `PATCH`  | `/vehicles/{id}` | `200`   | `400`, `404`    |
| `DELETE` | `/vehicles/{id}` | `204`   | —               |

### Vehicle shape

```json
{
  "id": 1,
  "nickName": "The Lisa Marie",
  "vin": "4M2DV11W4RDJ53329",
  "make": "Mercury",
  "model": "Villager",
  "year": "1994",
  "miles": 159864
}
```

> **Note:** Data is stored in-memory and resets on restart. Swap the
> `_vehicles` dict in `app/main.py` for a real database for persistence.
