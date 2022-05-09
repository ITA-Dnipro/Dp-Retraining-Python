from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from balances.schemas import BalanceInputSchema, BalanceOutputSchema, BalanceUpdateSchema
from balances.services import BalanceService
from common.schemas.responses import ResponseBaseSchema

balances_router = APIRouter(prefix='/balances', tags=['Balances'])


@balances_router.get('/', response_model=ResponseBaseSchema)
async def get_balances(balance_service: BalanceService = Depends()) -> ResponseBaseSchema:
    """GET '/balances' endpoint view function.

    Args:
        balance_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with list of BalanceOutputSchema objects as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=[BalanceOutputSchema.from_orm(balance) for balance in await balance_service.get_balances()],
        errors=[],
    )


@balances_router.get('/{id}', response_model=ResponseBaseSchema)
async def get_balance(id: UUID, balance_service: BalanceService = Depends()) -> ResponseBaseSchema:
    """GET '/balances/{id}' endpoint view function.

    Args:
        id: UUID of balance.
        balance_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with BalanceOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=BalanceOutputSchema.from_orm(await balance_service.get_balance_by_id(id_=id)),
        errors=[],
    )


@balances_router.put('/{id}', response_model=ResponseBaseSchema)
async def put_balance(id: UUID, balance: BalanceUpdateSchema,
                      balance_service: BalanceService = Depends()) -> ResponseBaseSchema:
    """PUT '/balances/{id}' endpoint view function.

    Args:
        id: UUID of balance.
        balance: Serialized BalanceUpdateSchema object.
        balance_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with BalanceOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=BalanceOutputSchema.from_orm(await balance_service.update_balance(id_=id, balance=balance)),
        errors=[],
    )
