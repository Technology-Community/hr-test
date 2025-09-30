# Base exceptions
from .base import ApplicationException, DomainException, InfrastructureException

# Handlers
from .handlers import (
    BaseExceptionHandler,
    BusinessRuleViolationHandler,
    DomainExceptionHandler,
    HttpExceptionConverter,
    ValidationErrorHandler,
    register_exception_handlers,
)

# Infrastructure exceptions
from .infrastructure import (
    DatabaseConnectionError,
    DatabaseException,
    DatabaseTimeoutError,
    ExternalServiceException,
    ExternalServiceTimeout,
    ExternalServiceUnavailable,
    FileNotFoundError,
    FilePermissionError,
    FileSystemException,
)


# Validation exceptions
from .validation import (
    BusinessRuleViolation,
    ConcurrencyError,
    DataIntegrityError,
    InvalidOperationError,
    ValidationError,
    ValidationException,
)

__all__ = [
    # Base
    "DomainException",
    "ApplicationException",
    "InfrastructureException",
    # Handlers
    "BaseExceptionHandler",
    "DomainExceptionHandler",
    "ValidationErrorHandler",
    "BusinessRuleViolationHandler",
    "HttpExceptionConverter",
    "register_exception_handlers",
    # Infrastructure
    "DatabaseException",
    "DatabaseConnectionError",
    "DatabaseTimeoutError",
    "ExternalServiceException",
    "ExternalServiceUnavailable",
    "ExternalServiceTimeout",
    "FileSystemException",
    "FileNotFoundError",
    "FilePermissionError",
    # Validation
    "ValidationException",
    "ValidationError",
    "BusinessRuleViolation",
    "InvalidOperationError",
    "DataIntegrityError",
    "ConcurrencyError",
]
