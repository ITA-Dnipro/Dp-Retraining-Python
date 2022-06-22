import enum


class CharityEmployeeAllowedRolesConstants(enum.Enum):
    """EmployeeRole table population data."""
    SUPERVISOR = 'supervisor'
    MANAGER = 'manager'

    ROLES_MAPPING = {
        SUPERVISOR: (SUPERVISOR,),
        MANAGER: (SUPERVISOR, MANAGER),
    }

