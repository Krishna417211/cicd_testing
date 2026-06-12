from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="FastAPI Demo",
    description="A production-ready FastAPI app with Docker + CI/CD",
    version="1.0.0",
)

items_db: dict = {}
counter = {"id": 1}


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class Item(ItemCreate):
    id: int
    created_at: datetime


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "FastAPI app is running 🚀"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow()}


@app.get("/items", response_model=List[Item], tags=["Items"])
def list_items():
    return list(items_db.values())


@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.post("/items", response_model=Item, status_code=201, tags=["Items"])
def create_item(item: ItemCreate):
    item_id = counter["id"]
    new_item = Item(id=item_id, created_at=datetime.utcnow(), **item.dict())
    items_db[item_id] = new_item
    counter["id"] += 1
    return new_item


@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
def update_item(item_id: int, item: ItemCreate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = Item(id=item_id, created_at=items_db[item_id].created_at, **item.dict())
    items_db[item_id] = updated
    return updated


@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted"}