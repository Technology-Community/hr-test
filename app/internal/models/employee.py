from typing import TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, Relationship
from app.constants import EmployeeStatus
from .base import BaseModel

if TYPE_CHECKING:
    from .organization import Organization


class Employee(BaseModel, table=True):
    __tablename__ = "employees"  # type: ignore

    first_name: str = Field(
        description="Employee first name"
    )
    last_name: str = Field(
        description="Employee last name"
    )
    email: str = Field(
        description="Employee email address",
        index=True,
        unique=True
    )
    phone_number: str = Field(
        description="Employee phone number"
    )
    department: str = Field(
        description="Department name",
        index=True
    )
    position: str = Field(
        description="Job position/title",
        index=True
    )
    location: str = Field(
        description="Work location",
        index=True
    )
    status: EmployeeStatus = Field(
        description="Employee status",
        index=True
    )
    organization_id: UUID = Field(
        foreign_key="organizations.id",
        description="Organization ID",
        index=True
    )

    organization: "Organization" = Relationship(back_populates="employees")
