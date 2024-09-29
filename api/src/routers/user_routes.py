from fastapi import APIRouter, Depends
from core.src.use_cases import CreateUser, CreateUserRequest
from adapters.src.jwt.jwt_token import verify_jwt_token
from factories.use_cases import get_or_create_user_use_case
from ..dtos import CreateUserResponseDto, CreateUserRequestDto

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
