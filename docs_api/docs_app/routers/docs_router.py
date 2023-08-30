from fastapi import APIRouter, Depends, HTTPException, status
#from docs_app.controllers.city_weather_controller import CityWeatherController
from docs_app.models.document import Document
from passlib.context import CryptContext
from docs_app.models.user import User, UserInDB, fake_decode_token, fake_users_db, fake_hash_password
from docs_app.core.config import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated

router = APIRouter()

base_url = f'http://{settings.PRJ_HOST}/docs'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/")
async def usage():
    return [
        {
            'Endpoints': {
                'Get document: ': base_url,
                'Post new document: ': base_url + '/new',
                'Update existing document: ': base_url + '/put/<id>',
                'Delete existing document: ': base_url + '/delete/<id>',
            },
        }
    ]

# @router.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    #if current_user.disabled:
    #    raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user