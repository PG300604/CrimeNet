"""
Helpers for authorization
"""
import jwt
from datetime import datetime, timedelta
from falcon import HTTP_401, HTTP_400
from ..config import config
from ..exceptions import AuthenticationError


class InvalidTokenError(AuthenticationError):
    """ Error in token structure """
    code = "InvalidTokenError"
    response_code = HTTP_400


class TokenExpiredError(AuthenticationError):
    """ Token is expired """
    code = "TokenExpiredError"
    response_code = HTTP_401


ALGORITHM = "HS256"


def create_token(claims: dict):
    """
    Create token with claims. Adds iat and exp claims to token.

    :param claims: claims to be stored in the token
    :returns: str token
    """
    token_payload = {
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=config["JWT_ACCESS_TOKEN_EXPIRES"])
    }
    token_payload.update(claims)
    return jwt.encode(
        token_payload,
        config["JWT_SECRET_KEY"],
        algorithm=ALGORITHM
    ).decode()


def read_token(token, required_claims=None):
    """
    Decode token and get claims

    :param token: token to be decoded and validated
    :param required_claims: claims, that must be present in the token
    :returns: dict of claims from token
    :raises TokenExpiredError: error when token is expired
    :raises InvalidTokenError: error when token could not be decoded, or doesn't have proper claims
    """
    try:
        claims = jwt.decode(token, config["JWT_SECRET_KEY"], algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as err:
        raise TokenExpiredError(str(err), "token claims")
    except jwt.InvalidTokenError as err:
        raise InvalidTokenError(str(err), "token")
    if required_claims:
        for claim_name in required_claims:
            if claim_name not in claims:
                raise InvalidTokenError(f"Malformed token, claim {claim_name} not found!", "token claims")
    return claims
