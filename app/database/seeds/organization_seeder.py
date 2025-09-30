from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.internal.models import Organization, OrganizationConfig


class OrganizationSeeder:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def seed_organizations(self):
        """Seed organizations and their configurations."""

        # Organization 1: Full contact info display
        org1_id = uuid4()
        organization1 = Organization(
            id=org1_id,
            name="Tech Solutions Inc",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        org1_config = OrganizationConfig(
            id=uuid4(),
            organization_id=org1_id,
            visible_columns=[
                "first_name", "last_name", "email", "phone_number",
                "department", "position", "location", "status"
            ],
            column_order=[
                "first_name", "last_name", "email", "phone_number",
                "department", "position", "location", "status"
            ],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Organization 2: Basic info only
        org2_id = uuid4()
        organization2 = Organization(
            id=org2_id,
            name="StartupCorp",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        org2_config = OrganizationConfig(
            id=uuid4(),
            organization_id=org2_id,
            visible_columns=["department", "position", "location"],
            column_order=["department", "position", "location"],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Organization 3: Custom order
        org3_id = uuid4()
        organization3 = Organization(
            id=org3_id,
            name="Global Enterprise",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        org3_config = OrganizationConfig(
            id=uuid4(),
            organization_id=org3_id,
            visible_columns=[
                "status", "location", "department", "position",
                "first_name", "last_name"
            ],
            column_order=[
                "status", "location", "department", "position",
                "first_name", "last_name"
            ],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Add to database
        self.db.add(organization1)
        self.db.add(org1_config)
        self.db.add(organization2)
        self.db.add(org2_config)
        self.db.add(organization3)
        self.db.add(org3_config)

        await self.db.commit()

        print(f"✅ Seeded 3 organizations with their configs")
        print(f"   - Tech Solutions Inc: Full display")
        print(f"   - StartupCorp: Department, position, location only")
        print(f"   - Global Enterprise: Custom order with status first")

        return {
            "tech_solutions": org1_id,
            "startup_corp": org2_id,
            "global_enterprise": org3_id
        }