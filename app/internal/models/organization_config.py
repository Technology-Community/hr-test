from typing import List, TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, Relationship, JSON, Column
from sqlalchemy import JSON as SA_JSON
from .base import BaseModel

if TYPE_CHECKING:
    from .organization import Organization


class OrganizationConfig(BaseModel, table=True):
    __tablename__ = "organization_configs"  # type: ignore

    organization_id: UUID = Field(
        foreign_key="organizations.id",
        description="Organization ID",
        index=True,
        unique=True
    )
    visible_columns: List[str] = Field(
        sa_column=Column(SA_JSON),
        description="List of visible employee columns for this organization",
        default=[
            "first_name", "last_name", "email", "phone_number",
            "department", "position", "location", "status"
        ]
    )
    column_order: List[str] = Field(
        sa_column=Column(SA_JSON),
        description="Order of columns display for this organization",
        default=[
            "first_name", "last_name", "email", "phone_number",
            "department", "position", "location", "status"
        ]
    )

    organization: "Organization" = Relationship(back_populates="config") 
