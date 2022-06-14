from uuid import UUID

from fastapi import APIRouter, Depends

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from charity.schemas import (
    AddManagerSchema,
    CharityFullOutputSchema,
    CharityInputSchema,
    CharityUpdateSchema,
    ManagerResponseSchema,
)
from charity.services import CharityService
from common.schemas.responses import ResponseBaseSchema

charities_router = APIRouter(prefix='/charities', tags=['Charities'])


@charities_router.get("/{org_id}", response_model=ResponseBaseSchema, status_code=HTTP_200_OK)
async def show_charity_organisation(org_id: UUID, charity_service: CharityService = Depends()):
    """
    Retrieves full info about definite organisation.

    Args:
        org_id: id of organisation.
        charity_service: dependency as business logic instance

    Returns:
        ResponseBaseSchema object with CharityOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=HTTP_200_OK,
        data=CharityFullOutputSchema.from_orm(await charity_service.get_exact_organisation(org_id)),
        errors=[],
    )


@charities_router.get("/", response_model=ResponseBaseSchema, status_code=HTTP_200_OK)
async def show_charities_list(charity_service: CharityService = Depends()):
    """
    Retrieves info about active organisations.

    Args:
        charity_service: dependency as business logic instance

    Returns:
        ResponseBaseSchema object with CharityOutputSchema object as response data.
    """
    return ResponseBaseSchema(status_code=HTTP_200_OK,
                              data=[
                                  CharityFullOutputSchema.from_orm(charity)
                                  for charity in await charity_service.get_organisations_list()],
                              errors=[])


@charities_router.post("/", response_model=ResponseBaseSchema, status_code=HTTP_201_CREATED)
async def create_charity(organisation_data: CharityInputSchema, charity_service: CharityService = Depends()):
    """
    Creates new organisation.

    Args:
        organisation_data: Serialized CharityInputSchema object.
        charity_service: dependency as business logic instance.

    Returns:
        ResponseBaseSchema object with CharityOutputSchema object as response data.
    """
    return ResponseBaseSchema(status_code=HTTP_201_CREATED,
                              data=CharityFullOutputSchema.from_orm(
                                      await charity_service.add_organisation(organisation_data)
                                  ),
                              errors=[])


@charities_router.patch("/{org_id}", response_model=ResponseBaseSchema, response_model_exclude_unset=True)
async def edit_charity(org_id: UUID,
                       organisation_data: CharityUpdateSchema,
                       charity_service: CharityService = Depends()):
    """
    Edits organisation.

    Args:
        org_id: id of organisation.
        organisation_data: Serialized CharityInputSchema object.
        charity_service: dependency as business logic instance.

    Returns:
        ResponseBaseSchema object with CharityOutputSchema object as response data.
    """
    return ResponseBaseSchema(status_code=HTTP_200_OK,
                              data=[
                                  CharityFullOutputSchema.from_orm(
                                      await charity_service.edit_organisation(org_id, organisation_data)
                                  )],
                              errors=[])


@charities_router.delete("/{org_id}", response_model=ResponseBaseSchema)
async def delete_charity(org_id: UUID, charity_service: CharityService = Depends()):
    """
     Deletes organisation.

    Args:
        org_id: id of organisation.
        charity_service: dependency as business logic instance.

    Returns:
        ResponseBaseSchema object with CharityOutputSchema object as response data.
    """
    await charity_service.delete_organisation(org_id)
    return ResponseBaseSchema(status_code=HTTP_200_OK,
                              data={"detail": "Organisation has been deleted successfully."},
                              errors=[])


@charities_router.post("/{organisation_id}/managers", response_model=ResponseBaseSchema)
async def add_manager(organisation_id: UUID, manager_data: AddManagerSchema,
                      charity_service: CharityService = Depends()):
    """
     Adds new manager to current organisation.

    Args:
        organisation_id: id of organisation.
        manager_data: AddManagerData object.
        charity_service: dependency as business logic instance.

    Returns:
        ResponseBaseSchema object with CharityOutputSchema object as response data.
    """
    association = await charity_service.add_manager(organisation_id, manager_data)
    message = f"Manager {association.user.username} has been successfully added. "
    if association.is_supermanager:
        message = message + "He is supermanager."
    else:
        message = message + "He is not supermanager."
    return ResponseBaseSchema(status_code=HTTP_200_OK,
                              data=[{"detail": message}],
                              errors=[])


@charities_router.get("/{organisation_id}/managers", response_model=ResponseBaseSchema)
async def show_managers_of_this_organisation(organisation_id: UUID, charity_service: CharityService = Depends()):
    return ResponseBaseSchema(status_code=HTTP_200_OK,
                              data=[ManagerResponseSchema.from_orm(manager)
                                    for manager in await charity_service.show_charity_managers(organisation_id)],
                              errors=[])


@charities_router.delete("/{organisation_id}/managers/{user_id}", response_model=ResponseBaseSchema)
async def delete_manager_from_organisation(
        organisation_id: UUID,
        user_id: UUID,
        charity_service: CharityService = Depends()
):
    await charity_service.delete_manager_from_organisation(organisation_id, user_id)
    return ResponseBaseSchema(status_code=HTTP_200_OK,
                              data={"detail": "Manager has been deleted successfully"},
                              errors=[])
