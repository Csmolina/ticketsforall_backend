from fastapi import APIRouter, Depends
from core.src.use_cases import CreateUser, CreateUserRequest
from adapters.src.jwt import verify_jwt_token, verify_admin_user
from core.src.use_cases.user.get_all.use_case import GetAllUsers
from factories.use_cases import get_or_create_user_use_case, get_all_users_use_case
from ..dtos import CreateUserResponseDto, CreateUserRequestDto, ListUsersResponseDto

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post(
    "/", response_model=CreateUserResponseDto, dependencies=[Depends(verify_jwt_token)]
)
async def create_or_get_user(
    request: CreateUserRequestDto,
    use_case: CreateUser = Depends(get_or_create_user_use_case),
) -> CreateUserResponseDto:
    response = use_case(
        CreateUserRequest(
            name=request.name,
            email=request.email,
        )
    )
    response_dto: CreateUserResponseDto = CreateUserResponseDto(
        user=response.user.model_dump()
    )
    return response_dto


@user_router.get(
    "/", response_model=ListUsersResponseDto, dependencies=[Depends(verify_admin_user)]
)
async def list_users(
    use_case: GetAllUsers = Depends(get_all_users_use_case),
) -> ListUsersResponseDto:
    response = use_case()
    response_dto: ListUsersResponseDto = ListUsersResponseDto(
        users=[user.model_dump() for user in response.users]
    )
    return response_dto
