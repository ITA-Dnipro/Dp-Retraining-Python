import enum


class SchemaExceptionMsgs(enum.Enum):
    """Constants for schema exception messages."""
    INVALID_ASSOCIATION_LIST_TYPE = "Invalid field type, '_AssociationList' required."
    AT_LEAST_ONE_FIELD_PRESENT = 'At least one field must be present in the schema.'
