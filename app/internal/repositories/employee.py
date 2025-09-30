from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_
from sqlalchemy.orm import selectinload
from app.internal.models import Employee
from app.constants import EmployeeStatus


class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_employees(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[EmployeeStatus] = None,
        locations: Optional[List[str]] = None,
        organization_ids: Optional[List[UUID]] = None,
        departments: Optional[List[str]] = None,
        positions: Optional[List[str]] = None,
    ) -> Tuple[List[Employee], int]:
        # Build filter conditions
        conditions = [Employee.deleted_at.is_(None)]  # Only active records

        if status:
            conditions.append(Employee.status == status)
        if locations:
            conditions.append(Employee.location.in_(locations))
        if organization_ids:
            conditions.append(Employee.organization_id.in_(organization_ids))
        if departments:
            conditions.append(Employee.department.in_(departments))
        if positions:
            conditions.append(Employee.position.in_(positions))

        # Count query
        count_query = select(func.count(Employee.id)).where(and_(*conditions))
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()

        # Data query with pagination
        offset = (page - 1) * page_size
        data_query = (
            select(Employee)
            .options(selectinload(Employee.organization))
            .where(and_(*conditions))
            .order_by(Employee.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )

        result = await self.db.execute(data_query)
        employees = result.scalars().all()

        return list(employees), total