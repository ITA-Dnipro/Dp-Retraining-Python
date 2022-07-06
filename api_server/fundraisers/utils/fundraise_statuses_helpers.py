from fastapi import status

from common.exceptions.fundraisers import FundraiseStatusExceptionMsgs
from fundraisers.utils.exceptions import FundraiseStatusNotSupportedError


def get_allowed_statuses_for_fundraise_status(status_name: str, allowed_statuses: dict) -> tuple:
    """Gets allowed statuses for provided fundraise status.

    Args:
        status_name: name of FundraiseStatus.
        allowed_statuses: dict with status name as a key and tuple of allowed statuses as value.

    Returns:
    tuple with allowed fundraise statuses.
    """
    try:
        status_allowed_statuses = allowed_statuses[status_name]
    except KeyError:
        raise FundraiseStatusNotSupportedError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FundraiseStatusExceptionMsgs.FUNDRAISE_STATUS_NOT_SUPPORTED.value.format(
                field_name='name',
                field_value=status_name,
            )
        )
    return status_allowed_statuses


def fundraise_status_validator(fundraise_status_name: str, allowed_statuses: tuple) -> bool:
    """Checks if fundraise status name present in tuple of allowed_statuses.

    Args:
        fundraise_status_name: name of FundraiseStatus object.
        allowed_statuses: tuple with allowed fundraise statuses.

    Returns:
    bool of presence fundraise_status_name in allowed_statuses.
    """
    return fundraise_status_name in allowed_statuses
