import logging
import math
from typing import Optional, Dict
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.internal.repositories.employee import EmployeeRepository
from app.internal.models import OrganizationConfig
from app.internal.dtos.employee import (
    EmployeeSearchRequest, EmployeeSearchResponse, EmployeeResponse
)
from app.constants import EmployeeStatus

logger = logging.getLogger(__name__)


class EmployeeService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            logger.info("Initializing EmployeeService")
            self._initialized = True

    async def _get_organization_configs(self, db: AsyncSession, organization_ids: list[UUID]) -> Dict[UUID, OrganizationConfig]:
        """Get organization configs for given organization IDs"""
        result = await db.execute(
            select(OrganizationConfig).where(OrganizationConfig.organization_id.in_(organization_ids))
        )
        configs = result.scalars().all()
        return {config.organization_id: config for config in configs}

    def _apply_organization_config(self, employee_data: dict, config: OrganizationConfig) -> dict:
        """Apply organization config to filter and order employee data"""
        if not config:
            return employee_data

        # Filter to only visible columns
        filtered_data = {
            col: employee_data.get(col)
            for col in config.visible_columns
            if col in employee_data
        }

        # Order according to config
        ordered_data = {}
        for col in config.column_order:
            if col in filtered_data:
                ordered_data[col] = filtered_data[col]

        return ordered_data

    async def get_employees(
        self,
        db: AsyncSession,
        search_request: EmployeeSearchRequest,
    ) -> EmployeeSearchResponse:
        logger.info(
            f"Getting employees with filters: page={search_request.page}, "
            f"page_size={search_request.page_size}, status={search_request.status}, "
            f"locations={search_request.locations}, organization_ids={search_request.organization_ids}, "
            f"departments={search_request.departments}, positions={search_request.positions}"
        )

        repository = EmployeeRepository(db)

        employees, total = await repository.search_employees(
            page=search_request.page,
            page_size=search_request.page_size,
            status=search_request.status,
            locations=search_request.locations,
            organization_ids=search_request.organization_ids,
            departments=search_request.departments,
            positions=search_request.positions,
        )

        # Get organization configs for filtering/ordering
        unique_org_ids = list(set(emp.organization_id for emp in employees))
        org_configs = await self._get_organization_configs(db, unique_org_ids)

        # Convert to DTOs with organization config applied
        employee_responses = []
        for emp in employees:
            # Convert employee to dict
            employee_data = {
                "id": emp.id,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "email": emp.email,
                "phone_number": emp.phone_number,
                "department": emp.department,
                "position": emp.position,
                "location": emp.location,
                "status": emp.status,
                "organization_id": emp.organization_id,
                "created_at": emp.created_at.isoformat(),
                "updated_at": emp.updated_at.isoformat(),
            }

            # Apply organization config to filter visible fields only
            config = org_configs.get(emp.organization_id)
            if config:
                # Filter to only visible columns (don't care about order)
                filtered_data = {
                    col: employee_data[col]
                    for col in employee_data
                    if col in config.visible_columns
                }

                # Return as dict instead of EmployeeResponse to allow dynamic fields
                employee_responses.append(filtered_data)
            else:
                # Fallback to full data if no config
                employee_responses.append(employee_data)

        total_pages = math.ceil(total / search_request.page_size) if total > 0 else 0
        return EmployeeSearchResponse(
            employees=employee_responses,
            total=total,
            page=search_request.page,
            page_size=search_request.page_size,
            total_pages=total_pages,
        )


def get_employee_service() -> EmployeeService:
    return EmployeeService()
