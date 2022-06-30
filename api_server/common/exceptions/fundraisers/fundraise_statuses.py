import enum


class FundraiseStatusExceptionMsgs(enum.Enum):
    """Constants for FundraiseStatus exception messages."""
    FUNDRAISE_STATUS_NOT_FOUND_IN_FUNDRAISE = (
        "FundraiseStatus with {field_name}: '{field_value}' not found in Fundraise with id: '{fundraise_id}'."
    )
