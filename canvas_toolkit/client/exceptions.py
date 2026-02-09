"""Custom exceptions for Canvas API interactions."""


class CanvasAPIError(Exception):
    """Base exception for Canvas API errors."""
    pass


class AuthenticationError(CanvasAPIError):
    """Raised when Canvas API authentication fails."""
    pass


class CourseNotFoundError(CanvasAPIError):
    """Raised when a course is not found."""
    pass


class RateLimitError(CanvasAPIError):
    """Raised when Canvas API rate limit is exceeded."""
    pass
