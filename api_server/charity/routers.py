from uuid import UUID

from common.schemas.responses import ResponseBaseSchema
from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from .schemas import CharityInputSchema, CharityOutputSchema, CharityUpdateSchema
from .services import CharityService

charities_router = APIRouter(prefix='/charities', tags=['Charities'])


@charities_router.post("/")
async def create_charity(organisation_data: CharityInputSchema, charity_service: CharityService = Depends()):
    """Creates new organisation.

        Args:
            organisation_data: Serialized CharityInputSchema object.
            charity_service: dependency as business logic instance.

        Returns:
        ResponseBaseSchema object with CharityOutputSchema object as response data.
        """
    return ResponseBaseSchema(status_code=HTTP_201_CREATED,
                              data=[
                                  CharityOutputSchema.from_orm(
                                      await charity_service.add_organisation(organisation_data)
                                    )],
                              errors=[])


@charities_router.put("/{org_id}", response_model_exclude_unset=True)
async def edit_charity(org_id: UUID,
                       organisation_data: CharityUpdateSchema,
                       charity_service: CharityService = Depends()):
    return ResponseBaseSchema(status_code=HTTP_200_OK,
                              data=[
                                  CharityOutputSchema.from_orm(
                                      await charity_service.edit_organisation(org_id, organisation_data)
                                  )],
                              errors=[])
