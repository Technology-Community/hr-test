from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.database import get_database
from app.internal.services.employee import get_employee_service, EmployeeService
from app.internal.dtos.employee import EmployeeSearchRequest, EmployeeSearchResponse
from app.utils.response import APIResponse
from app.constants import EmployeeStatus

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=EmployeeSearchResponse)
async def get_employees(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[EmployeeStatus] = Query(None, description="Filter by status"),
    locations: Optional[list[str]] = Query(None, description="Filter by locations"),
    organization_ids: Optional[list[str]] = Query(None, description="Filter by organizations"),
    departments: Optional[list[str]] = Query(None, description="Filter by departments"),
    positions: Optional[list[str]] = Query(None, description="Filter by positions"),
    db: AsyncSession = Depends(get_database),
    employee_service: EmployeeService = Depends(get_employee_service),
):
    search_request = EmployeeSearchRequest(
        page=page,
        page_size=page_size,
        status=status,
        locations=locations,
        organization_ids=organization_ids,
        departments=departments,
        positions=positions,
    )

    result = await employee_service.get_employees(db, search_request)
    response = result.model_dump(mode="json")
    return APIResponse.success_response(
        data=response,
        message="Employees retrieved successfully"
    )
