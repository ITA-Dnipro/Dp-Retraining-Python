import enum


class JWTTokenExceptionsMsgs(enum.Enum):
    """Constants for generic JWT exception messages."""
    INVALID_JWT_TOKEN = 'Invalid JWT token provided.'
    JWT_TOKEN_EXPIRED = 'Provided JWT token already expired.'
