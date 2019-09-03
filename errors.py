class AuthorizationError(Exception):
    """
Raise when there is an issue with the user's config file
"""
class ICD11CodeError(ValueError):
    """Raise when an ICD11 code is correctly formatted but leads to an error when used with the api"""
