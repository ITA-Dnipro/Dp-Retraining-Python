import enum


class EmployeeRolePopulateData(enum.Enum):
    """EmployeeRole table population data."""
    SUPERVISOR = 'supervisor'
    MANAGER = 'manager'

    ALL_ROLES = [
        SUPERVISOR,
        MANAGER,
    ]
