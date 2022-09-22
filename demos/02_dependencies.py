from typing import Union
from fastapi import Depends, FastAPI
import uvicorn
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


async def common_parameters(
        q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

if __name__ == "__main__":
    uvicorn.run("dependencies:app", host="127.0.0.1", port=8000, log_level="info")
