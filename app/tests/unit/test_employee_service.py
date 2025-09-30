import math
from datetime import datetime, timezone
from typing import List
from unittest.mock import AsyncMock, MagicMock, Mock, patch
from uuid import UUID, uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import EmployeeStatus
from app.internal.dtos.employee import (
    EmployeeSearchRequest,
    EmployeeSearchResponse,
)
from app.internal.models import Employee, OrganizationConfig
from app.internal.services.employee import EmployeeService, get_employee_service


class TestEmployeeService:
    """Test suite for EmployeeService"""

    @pytest.fixture
    def mock_db(self) -> AsyncMock:
        """Create a mock database session"""
        return AsyncMock(spec=AsyncSession)

    @pytest.fixture
    def employee_service(self) -> EmployeeService:
        """Create an EmployeeService instance"""
        # Reset singleton for testing
        EmployeeService._instance = None
        EmployeeService._initialized = False
        return EmployeeService()

    @pytest.fixture
    def sample_employee(self) -> Employee:
        """Create a sample employee for testing"""
        org_id = uuid4()
        employee = Employee(
            id=uuid4(),
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
            department="Engineering",
            position="Software Engineer",
            location="New York",
            status=EmployeeStatus.ACTIVE,
            organization_id=org_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        return employee

    @pytest.fixture
    def sample_employees(self) -> List[Employee]:
        """Create a list of sample employees"""
        org_id = uuid4()
        employees = [
            Employee(
                id=uuid4(),
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone_number="+1234567890",
                department="Engineering",
                position="Software Engineer",
                location="New York",
                status=EmployeeStatus.ACTIVE,
                organization_id=org_id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            Employee(
                id=uuid4(),
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                phone_number="+1234567891",
                department="Marketing",
                position="Marketing Manager",
                location="San Francisco",
                status=EmployeeStatus.ACTIVE,
                organization_id=org_id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            Employee(
                id=uuid4(),
                first_name="Bob",
                last_name="Johnson",
                email="bob.johnson@example.com",
                phone_number="+1234567892",
                department="Engineering",
                position="Senior Engineer",
                location="New York",
                status=EmployeeStatus.INACTIVE,
                organization_id=org_id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
        ]
        return employees

    @pytest.fixture
    def sample_org_config(self, sample_employees: List[Employee]) -> OrganizationConfig:
        """Create a sample organization config"""
        return OrganizationConfig(
            id=uuid4(),
            organization_id=sample_employees[0].organization_id,
            visible_columns=["first_name", "last_name", "email", "department"],
            column_order=["first_name", "last_name", "email", "department"],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    def test_singleton_pattern(self, employee_service: EmployeeService):
        """Test that EmployeeService follows singleton pattern"""
        service1 = EmployeeService()
        service2 = EmployeeService()
        assert service1 is service2
        assert service1._initialized is True

    def test_get_employee_service(self):
        """Test get_employee_service dependency function"""
        # Reset singleton
        EmployeeService._instance = None
        EmployeeService._initialized = False

        service1 = get_employee_service()
        service2 = get_employee_service()
        assert service1 is service2
        assert isinstance(service1, EmployeeService)

    @pytest.mark.asyncio
    async def test_get_employees_success_no_filters(
        self, employee_service: EmployeeService, mock_db: AsyncMock, sample_employees: List[Employee]
    ):
        """Test getting employees without filters"""
        search_request = EmployeeSearchRequest(page=1, page_size=20)

        # Mock repository
        with patch("app.internal.services.employee.EmployeeRepository") as mock_repo_class:
            mock_repo = mock_repo_class.return_value
            mock_repo.search_employees = AsyncMock(return_value=(sample_employees, len(sample_employees)))

            # Mock organization config query (no configs)
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = []
            mock_db.execute = AsyncMock(return_value=mock_result)

            # Execute
            response = await employee_service.get_employees(mock_db, search_request)

            # Verify
            assert isinstance(response, EmployeeSearchResponse)
            assert len(response.employees) == 3
            assert response.total == 3
            assert response.page == 1
            assert response.page_size == 20
            assert response.total_pages == 1

            # Verify repository was called correctly
            mock_repo.search_employees.assert_called_once_with(
                page=1,
                page_size=20,
                status=None,
                locations=None,
                organization_ids=None,
                departments=None,
                positions=None,
            )

    @pytest.mark.asyncio
    async def test_get_employees_with_status_filter(
        self, employee_service: EmployeeService, mock_db: AsyncMock, sample_employees: List[Employee]
    ):
        """Test getting employees with status filter"""
        search_request = EmployeeSearchRequest(
            page=1, page_size=20, status=EmployeeStatus.ACTIVE
        )

        active_employees = [emp for emp in sample_employees if emp.status == EmployeeStatus.ACTIVE]

        with patch("app.internal.services.employee.EmployeeRepository") as mock_repo_class:
            mock_repo = mock_repo_class.return_value
            mock_repo.search_employees = AsyncMock(return_value=(active_employees, len(active_employees)))

            # Mock organization config query
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = []
            mock_db.execute = AsyncMock(return_value=mock_result)

            response = await employee_service.get_employees(mock_db, search_request)

            assert len(response.employees) == 2
            assert response.total == 2
            mock_repo.search_employees.assert_called_once_with(
                page=1,
                page_size=20,
                status=EmployeeStatus.ACTIVE,
                locations=None,
                organization_ids=None,
                departments=None,
                positions=None,
            )

    @pytest.mark.asyncio
    async def test_get_employees_with_multiple_filters(
        self, employee_service: EmployeeService, mock_db: AsyncMock, sample_employees: List[Employee]
    ):
        """Test getting employees with multiple filters"""
        org_ids = [sample_employees[0].organization_id]
        search_request = EmployeeSearchRequest(
            page=1,
            page_size=20,
            status=EmployeeStatus.ACTIVE,
            locations=["New York"],
            organization_ids=org_ids,
            departments=["Engineering"],
            positions=["Software Engineer"],
        )

        filtered_employees = [sample_employees[0]]  # Only John Doe matches all filters

        with patch("app.internal.services.employee.EmployeeRepository") as mock_repo_class:
            mock_repo = mock_repo_class.return_value
            mock_repo.search_employees = AsyncMock(return_value=(filtered_employees, len(filtered_employees)))

            # Mock organization config query
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = []
            mock_db.execute = AsyncMock(return_value=mock_result)

            response = await employee_service.get_employees(mock_db, search_request)

            assert len(response.employees) == 1
            assert response.total == 1
            assert response.employees[0]["email"] == "john.doe@example.com"
            mock_repo.search_employees.assert_called_once_with(
                page=1,
                page_size=20,
                status=EmployeeStatus.ACTIVE,
                locations=["New York"],
                organization_ids=org_ids,
                departments=["Engineering"],
                positions=["Software Engineer"],
            )

    @pytest.mark.asyncio
    async def test_get_employees_with_pagination(
        self, employee_service: EmployeeService, mock_db: AsyncMock, sample_employees: List[Employee]
    ):
        """Test pagination works correctly"""
        search_request = EmployeeSearchRequest(page=2, page_size=1)

        # Simulate paginated results
        with patch("app.internal.services.employee.EmployeeRepository") as mock_repo_class:
            mock_repo = mock_repo_class.return_value
            mock_repo.search_employees = AsyncMock(return_value=([sample_employees[1]], 3))

            # Mock organization config query
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = []
            mock_db.execute = AsyncMock(return_value=mock_result)

            response = await employee_service.get_employees(mock_db, search_request)

            assert len(response.employees) == 1
            assert response.total == 3
            assert response.page == 2
            assert response.page_size == 1
            assert response.total_pages == 3

    @pytest.mark.asyncio
    async def test_get_employees_empty_result(
        self, employee_service: EmployeeService, mock_db: AsyncMock
    ):
        """Test getting employees with no results"""
        search_request = EmployeeSearchRequest(page=1, page_size=20)

        with patch("app.internal.services.employee.EmployeeRepository") as mock_repo_class:
            mock_repo = mock_repo_class.return_value
            mock_repo.search_employees = AsyncMock(return_value=([], 0))

            # Mock organization config query
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = []
            mock_db.execute = AsyncMock(return_value=mock_result)

            response = await employee_service.get_employees(mock_db, search_request)

            assert len(response.employees) == 0
            assert response.total == 0
            assert response.page == 1
            assert response.total_pages == 0

    @pytest.mark.asyncio
    async def test_get_employees_with_organization_config(
        self,
        employee_service: EmployeeService,
        mock_db: AsyncMock,
        sample_employees: List[Employee],
        sample_org_config: OrganizationConfig,
    ):
        """Test that organization config filters visible columns"""
        search_request = EmployeeSearchRequest(page=1, page_size=20)

        with patch("app.internal.services.employee.EmployeeRepository") as mock_repo_class:
            mock_repo = mock_repo_class.return_value
            mock_repo.search_employees = AsyncMock(return_value=(sample_employees, len(sample_employees)))

            # Mock organization config query with config
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = [sample_org_config]
            mock_db.execute = AsyncMock(return_value=mock_result)

            response = await employee_service.get_employees(mock_db, search_request)

            # Verify that only visible columns are returned
            for employee in response.employees:
                assert "first_name" in employee
                assert "last_name" in employee
                assert "email" in employee
                assert "department" in employee
                # These should be filtered out
                assert "phone_number" not in employee
                assert "position" not in employee
                assert "location" not in employee

    @pytest.mark.asyncio
    async def test_get_organization_configs(
        self,
        employee_service: EmployeeService,
        mock_db: AsyncMock,
        sample_org_config: OrganizationConfig,
    ):
        """Test _get_organization_configs private method"""
        org_ids = [sample_org_config.organization_id]

        # Mock database query
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [sample_org_config]
        mock_db.execute = AsyncMock(return_value=mock_result)

        configs = await employee_service._get_organization_configs(mock_db, org_ids)

        assert len(configs) == 1
        assert sample_org_config.organization_id in configs
        assert configs[sample_org_config.organization_id] == sample_org_config

    def test_apply_organization_config_with_config(
        self, employee_service: EmployeeService, sample_org_config: OrganizationConfig
    ):
        """Test _apply_organization_config filters and orders columns correctly"""
        employee_data = {
            "id": uuid4(),
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "+1234567890",
            "department": "Engineering",
            "position": "Software Engineer",
            "location": "New York",
            "status": "active",
        }

        filtered_data = employee_service._apply_organization_config(employee_data, sample_org_config)

        # Should only contain visible columns
        assert "first_name" in filtered_data
        assert "last_name" in filtered_data
        assert "email" in filtered_data
        assert "department" in filtered_data
        # These should be filtered out
        assert "phone_number" not in filtered_data
        assert "position" not in filtered_data
        assert "location" not in filtered_data
        assert "status" not in filtered_data

    def test_apply_organization_config_without_config(
        self, employee_service: EmployeeService
    ):
        """Test _apply_organization_config returns original data when no config"""
        employee_data = {
            "id": uuid4(),
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
        }

        filtered_data = employee_service._apply_organization_config(employee_data, None)

        # Should return original data
        assert filtered_data == employee_data

    @pytest.mark.asyncio
    async def test_get_employees_total_pages_calculation(
        self, employee_service: EmployeeService, mock_db: AsyncMock
    ):
        """Test total_pages calculation with different scenarios"""
        test_cases = [
            (100, 20, 5),  # Exact division
            (101, 20, 6),  # With remainder
            (19, 20, 1),   # Less than page size
            (0, 20, 0),    # No results
        ]

        for total, page_size, expected_pages in test_cases:
            search_request = EmployeeSearchRequest(page=1, page_size=page_size)

            with patch("app.internal.services.employee.EmployeeRepository") as mock_repo_class:
                mock_repo = mock_repo_class.return_value
                mock_repo.search_employees = AsyncMock(return_value=([], total))

                # Mock organization config query
                mock_result = MagicMock()
                mock_result.scalars.return_value.all.return_value = []
                mock_db.execute = AsyncMock(return_value=mock_result)

                response = await employee_service.get_employees(mock_db, search_request)

                assert response.total_pages == expected_pages, (
                    f"Failed for total={total}, page_size={page_size}: "
                    f"expected {expected_pages}, got {response.total_pages}"
                )