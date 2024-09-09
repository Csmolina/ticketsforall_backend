from fastapi import APIRouter, Depends
from core.src.use_cases import CreateUser, CreateUserRequest
from factories.use_cases import get_or_create_user_use_case
from ..dtos import CreateUserResponseDto, CreateUserRequestDto

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", response_model=CreateUserResponseDto)
async def create_or_get_user(
    request: CreateUserRequestDto,
    use_case: CreateUser = Depends(get_or_create_user_use_case),
) -> CreateUserResponseDto:
    response = use_case(
        CreateUserRequest(
            id=request.id,
            name=request.name,
            email=request.email,
            user_type=request.user_type,
        )
    )
    response_dto: CreateUserResponseDto = CreateUserResponseDto(
        **response.user._asdict()
    )
    return response_dto
