import base64
import json

from fastapi import Depends, FastAPI, HTTPException, status
import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# reference https://fastapi.tiangolo.com/tutorial/security/first-steps/#the-password-flow


# Why token? API should be independent of the server that authenticates the user.
# Endpoint should be the same as `tokenUrl="token"`
@app.post("/token")
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # verify username and password
    # where to store passwords? how?
    if form_data.username != 'israel' and form_data.password != 'israeli':
        raise HTTPException(status_code=400, detail="Bad username or password")

    # A "token" is just a string with some content that we can use later to verify this user.
    user_token = base64.b64encode(bytes(json.dumps({
        'username': 'israel',
        'scope': ['reader', 'commenter'],
        'expires_in': '30m'  # Normally, a token is set to expire after some time (why?)
    }), 'utf-8'))

    # The frontend stores that token temporarily somewhere (where?)
    return {"token": user_token}


@app.get("/items")
async def read_items(token: str = Depends(oauth2_scheme)):
    if not token:  # verify token integrity end expiry (how?)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # extract the username and permissions scope from the token
    user = json.loads(base64.b64decode(token).decode('utf-8'))

    # access protected data ...
    return {"data": f"sensitive data of {user['username']}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
