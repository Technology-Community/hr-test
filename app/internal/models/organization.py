from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship
from .base import BaseModel

if TYPE_CHECKING:
    from .employee import Employee
    from .organization_config import OrganizationConfig


class Organization(BaseModel, table=True):
    __tablename__ = "organizations"  # type: ignore

    name: str = Field(description="Organization name", index=True)

    config: Optional["OrganizationConfig"] = Relationship(back_populates="organization")
    employees: List["Employee"] = Relationship(back_populates="organization")
