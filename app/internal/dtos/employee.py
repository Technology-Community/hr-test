from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from app.constants import EmployeeStatus


class EmployeeResponse(BaseModel):
    id: UUID = Field(description="Employee ID")
    first_name: str = Field(description="Employee first name")
    last_name: str = Field(description="Employee last name")
    email: str = Field(description="Employee email address")
    phone_number: str = Field(description="Employee phone number")
    department: str = Field(description="Department name")
    position: str = Field(description="Job position/title")
    location: str = Field(description="Work location")
    status: EmployeeStatus = Field(description="Employee status")
    organization_id: UUID = Field(description="Organization ID")
    created_at: str = Field(description="Creation timestamp")
    updated_at: str = Field(description="Last update timestamp")

    class Config:
        from_attributes = True


class EmployeeSearchRequest(BaseModel):
    page: int = Field(1, ge=1, description="Page number (1-based)")
    page_size: int = Field(20, ge=1, le=100, description="Number of items per page")
    status: Optional[EmployeeStatus] = Field(None, description="Filter by employee status")
    locations: Optional[List[str]] = Field(None, description="Filter by work locations (WHERE IN)")
    organization_ids: Optional[List[UUID]] = Field(None, description="Filter by organization IDs (WHERE IN)")
    departments: Optional[List[str]] = Field(None, description="Filter by departments (WHERE IN)")
    positions: Optional[List[str]] = Field(None, description="Filter by positions (WHERE IN)")


class EmployeeSearchResponse(BaseModel):
    employees: List[dict] = Field(description="List of employees with dynamic columns")
    total: int = Field(description="Total number of employees matching filters")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Number of items per page")
    total_pages: int = Field(description="Total number of pages")