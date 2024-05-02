class LightMetricsError(Exception):
    """Base class for exceptions in this module."""

    class UnauthorizedRequestError(Exception):
        """Exception raised when LightMetrics denies a request."""

    class UnexpectedStatusCodeError(Exception):
        """Exception raised when response is unexpected."""

    class CredentialsNotFoundError(Exception):
        """Exception raised when LightMetrics credentials are not found."""

    errors = {
        1: "Invalid API key",
    }
