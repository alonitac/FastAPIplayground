from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn

app = FastAPI()
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == "fjohnsmith") or not (credentials.password == "swordfish"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@app.get("/profile")
async def main(username: str = Depends(get_current_username)):
    return {"username": username}


if __name__ == "__main__":
    uvicorn.run("basic_auth2:app", host="127.0.0.1", port=8000, log_level="info")