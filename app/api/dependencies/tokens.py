from fastapi.security import OAuth2PasswordBearer

oauth_access = OAuth2PasswordBearer(tokenUrl="/user/token")
