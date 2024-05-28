from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import json

app = FastAPI()

class Spot(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    location: Optional[str] = None
    time: Optional[str] = None
    tags: Optional[list[str]] = None
    description: Optional[str] = None
    category: Optional[str] = None
    isVideo: Optional[bool] = None
    likes: Optional[int] = None
    like_ratio: Optional[float] = None
    img_url: Optional[str] = None

#여기 부터 복붙

db = []

def load_data_from_json(file_path: str):
    global db
    max_id = max((spot.id for spot in db), default=0) if db else 0

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            max_id += 1
            # 필드 기본값 설정
            default_values = {
                "id": max_id,
                "name": None,
                "location": None,
                "time": None,
                "tags": None,
                "description": None,
                "category": None,
                "like": None,
                "isVideo": None,
                "img_url": None
            }

            # 필드 매칭 및 기본값 적용
            item = {key: item.get(key, default) if item.get(key) is not None else default for key, default in default_values.items()}
            spot = Spot(**item)
            db.append(spot)

@app.get("/")
async def message():
    return '어디가유 데이터 서버입니다. 확인용3'

@app.post("/load-data/")
def load_data(file_path: str):
    try:
        load_data_from_json(file_path)
        return {"message": "Data loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/spots/")
def create_spot(spot: Spot):
    # 새로운 id 자동 할당
    if db:
        max_id = max(spot.id for spot in db if spot.id is not None)
        spot.id = max_id + 1
    else:
        spot.id = 1

    db.append(spot)
    return spot

@app.get("/spots/")
def read_spots():
    return db

@app.get("/spots/{spot_id}")
def read_spot(spot_id: int):
    for spot in db:
        if spot_id == spot.id:
            return spot
    raise HTTPException(status_code=404, detail="Spot not found")