import asyncio
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.configs.database import db_manager
from app.internal.models.employee import Employee
from app.constants import EmployeeStatus


class EmployeeSeeder:
    """Seeder class for Employee data"""

    @staticmethod
    def get_sample_data(organization_ids):
        """Return sample employee data with organization assignments"""
        return [
            Employee(
                id=str(uuid.uuid4()),
                first_name="John",
                last_name="Doe",
                email="john.doe@company.com",
                phone_number="+1-555-0101",
                department="Engineering",
                position="Senior Software Engineer",
                location="New York, NY",
                status=EmployeeStatus.ACTIVE,
                organization_id=organization_ids["tech_solutions"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            Employee(
                id=str(uuid.uuid4()),
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@company.com",
                phone_number="+1-555-0102",
                department="Engineering",
                position="Frontend Developer",
                location="San Francisco, CA",
                status=EmployeeStatus.ACTIVE,
                organization_id=organization_ids["tech_solutions"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            Employee(
                id=str(uuid.uuid4()),
                first_name="Michael",
                last_name="Johnson",
                email="michael.johnson@company.com",
                phone_number="+1-555-0103",
                department="Product",
                position="Product Manager",
                location="Austin, TX",
                status=EmployeeStatus.ACTIVE,
                organization_id=organization_ids["startup_corp"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            Employee(
                first_name="Sarah",
                last_name="Williams",
                email="sarah.williams@company.com",
                phone_number="+1-555-0104",
                department="Design",
                position="UX Designer",
                location="Seattle, WA",
                status="Active"
            ),
            Employee(
                first_name="David",
                last_name="Brown",
                email="david.brown@company.com",
                phone_number="+1-555-0105",
                department="Engineering",
                position="DevOps Engineer",
                location="Denver, CO",
                status="Active"
            ),
            Employee(
                first_name="Emily",
                last_name="Davis",
                email="emily.davis@company.com",
                phone_number="+1-555-0106",
                department="Marketing",
                position="Marketing Manager",
                location="Los Angeles, CA",
                status="Active"
            ),
            Employee(
                first_name="James",
                last_name="Miller",
                email="james.miller@company.com",
                phone_number="+1-555-0107",
                department="Sales",
                position="Sales Representative",
                location="Chicago, IL",
                status="Active"
            ),
            Employee(
                first_name="Lisa",
                last_name="Wilson",
                email="lisa.wilson@company.com",
                phone_number="+1-555-0108",
                department="HR",
                position="HR Manager",
                location="Boston, MA",
                status="Active"
            ),
            Employee(
                first_name="Robert",
                last_name="Garcia",
                email="robert.garcia@company.com",
                phone_number="+1-555-0109",
                department="Finance",
                position="Financial Analyst",
                location="Miami, FL",
                status="Active"
            ),
            Employee(
                first_name="Jennifer",
                last_name="Martinez",
                email="jennifer.martinez@company.com",
                phone_number="+1-555-0110",
                department="Engineering",
                position="QA Engineer",
                location="Portland, OR",
                status="Inactive"
            )
        ]

    @staticmethod
    async def seed_employees(session: AsyncSession, organization_ids):
        """Seed employee data"""
        print("🌱 Seeding Employee data...")

        # Check if employees already exist
        result = await session.execute(select(Employee))
        existing_employees = result.scalars().all()

        if existing_employees:
            print(f"   ⚠️  Found {len(existing_employees)} existing employees. Skipping seed.")
            return

        # Create sample employees with organization assignments
        sample_employees = [
            Employee(
                id=uuid4(),
                first_name="John", last_name="Doe", email="john.doe@company.com",
                phone_number="+1-555-0101", department="Engineering", position="Senior Software Engineer",
                location="New York", status=EmployeeStatus.ACTIVE, organization_id=organization_ids["tech_solutions"],
                created_at=datetime.now(), updated_at=datetime.now()
            ),
            Employee(
                id=uuid4(),
                first_name="Jane", last_name="Smith", email="jane.smith@company.com",
                phone_number="+1-555-0102", department="Engineering", position="Frontend Developer",
                location="San Francisco", status=EmployeeStatus.ACTIVE, organization_id=organization_ids["startup_corp"],
                created_at=datetime.now(), updated_at=datetime.now()
            ),
            Employee(
                id=uuid4(),
                first_name="Michael", last_name="Johnson", email="michael.johnson@company.com",
                phone_number="+1-555-0103", department="Product", position="Product Manager",
                location="Austin", status=EmployeeStatus.ACTIVE, organization_id=organization_ids["startup_corp"],
                created_at=datetime.now(), updated_at=datetime.now()
            ),
            Employee(
                id=uuid4(),
                first_name="Sarah", last_name="Williams", email="sarah.williams@company.com",
                phone_number="+1-555-0104", department="Design", position="UX Designer",
                location="Seattle", status=EmployeeStatus.ACTIVE, organization_id=organization_ids["global_enterprise"],
                created_at=datetime.now(), updated_at=datetime.now()
            ),
            Employee(
                id=uuid4(),
                first_name="David", last_name="Brown", email="david.brown@company.com",
                phone_number="+1-555-0105", department="Engineering", position="DevOps Engineer",
                location="Denver", status=EmployeeStatus.ACTIVE, organization_id=organization_ids["global_enterprise"],
                created_at=datetime.now(), updated_at=datetime.now()
            )
        ]

        # Add employees to session
        for employee in sample_employees:
            session.add(employee)

        # Commit changes
        await session.commit()

        print(f"   ✅ Successfully seeded {len(sample_employees)} employees")

    @staticmethod
    async def clear_employees(session: AsyncSession):
        """Clear all employee data"""
        print("🧹 Clearing Employee data...")

        # Delete all employees
        result = await session.execute(select(Employee))
        employees = result.scalars().all()

        for employee in employees:
            await session.delete(employee)

        await session.commit()
        print(f"   ✅ Cleared {len(employees)} employees")


async def main():
    """Main seeder function"""
    await db_manager.connect()

    async with db_manager.session_maker() as session:
        await EmployeeSeeder.seed_employees(session)

    await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())