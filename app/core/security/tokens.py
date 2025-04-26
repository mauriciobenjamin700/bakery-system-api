from jose import JWTError, jwt

from app.core.constants.messages import (
    ERROR_TOKEN_CLAIMS_INVALID,
    ERROR_TOKEN_EXPIRED,
)
from app.core.errors import UnauthorizedError
from app.core.generate.dates import (
    get_expiration_timestamp,
    get_now,
    get_now_timestamp,
)
from app.core.generate.ids import id_generator
from app.core.settings import config


class TokenManager:
    """
    A class to manage JWT tokens.

    - Methods:
        - create_access_token: Create an access token with the given data.
        - create_refresh_token: Create a refresh token with the given data.
        - verify_token: Verify the token and return the payload if valid.
    """

    ALGORITHM = config.TOKEN_ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = config.TOKEN_EXPIRES_IN_MINUTES
    SECRET_KEY = config.TOKEN_SECRET_KEY

    @classmethod
    def create_access_token(cls, data: dict, infinity: bool = True) -> str:
        """
        Create an access token with the given data and expiration time.

        - Args:
          - data: dict: The data to include in the token.
            - infinity: bool: If True, the token will not expire.

        - Returns:
          - str: The encoded token.
        """
        # Implementation for creating an access token
        to_encode = data.copy()
        now = get_now_timestamp()

        to_encode.update(
            {
                "iat": now,  #  # Quando o token foi criado
                "nbf": now,  # # Quando o token começa a ser válido,
                "jti": id_generator(),  # ID do token
            }
        )

        if not infinity:
            to_encode.update(
                {
                    "exp": get_expiration_timestamp(
                        get_now(), cls.ACCESS_TOKEN_EXPIRE_MINUTES
                    ),  # Quando o token expira
                }
            )

        return jwt.encode(data, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def create_refresh_token(
        cls, data: dict, expires_delta: int = None
    ) -> str:
        """
        Cria um refresh token com os dados fornecidos e tempo de expiração.

        - Args:
            - data: dict: Os dados a serem incluídos no token.
            - expires_delta: int: Tempo de expiração em minutos (opcional).

        - Returns:
            - str: O token codificado.
        """
        to_encode = data.copy()
        now = get_now_timestamp()

        # Adiciona os campos padrão ao payload
        to_encode.update(
            {
                "iat": now,  # Quando o token foi criado
                "jti": id_generator(),  # ID único do token
            }
        )

        # Define o tempo de expiração
        if expires_delta:
            expire = get_expiration_timestamp(get_now(), expires_delta)
        else:
            expire = get_expiration_timestamp(
                get_now(), cls.ACCESS_TOKEN_EXPIRE_MINUTES * 24 * 7
            )  # 7 dias por padrão
        to_encode.update({"exp": expire})

        # Gera o token JWT
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def verify_token(cls, token: str) -> dict:
        """
        Verifica o token fornecido e retorna o payload se for válido.

        - Args:
            - token: str: O token JWT a ser verificado.

        - Returns:
            - dict: O payload decodificado do token.

        - Raises:
            - UnauthorizedError: Se o token for inválido ou expirado.
        """
        try:
            # Decodifica e valida o token
            payload = jwt.decode(
                token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM]
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise UnauthorizedError(ERROR_TOKEN_EXPIRED)

        except jwt.JWTClaimsError:
            raise UnauthorizedError(ERROR_TOKEN_CLAIMS_INVALID)

        except JWTError as e:
            raise UnauthorizedError(f"Token inválido: {e}")
