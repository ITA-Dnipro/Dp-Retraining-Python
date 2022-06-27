import enum


class CharityEmployeeAllowedRolesConstants(enum.Enum):
    """EmployeeRole table population data."""
    SUPERVISOR = 'supervisor'
    MANAGER = 'manager'

    ADD_EMPLOYEE_ROLES_MAPPING = {
        SUPERVISOR: (SUPERVISOR,),
        MANAGER: (SUPERVISOR, MANAGER),
    }

    DELETE_EMPLOYEE_ROLES_MAPPING = {
        SUPERVISOR: (SUPERVISOR,),
        MANAGER: (SUPERVISOR, MANAGER),
    }


class CharityEmployeeServiceConstants(enum.Enum):
    """CharityEmployee Service constants."""
    SUCCESSSFUL_EMPLOYEE_REMOVAL_MSG = {
        'message': "Employee with id: '{employee_id}' successfully removed from Charity with id: '{charity_id}'."
    }
