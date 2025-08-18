import json
from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, status, Request, Header
from src.core.stack_auth import stack_auth_client, StackAuthUser
import structlog

logger = structlog.get_logger(__name__)

def get_stack_auth_client():
    """Get Stack Auth client instance."""
    if not stack_auth_client.settings.stack_secret_server_key:
        logger.error("Stack Auth secret server key not configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stack Auth secret server key not configured"
        )
    return stack_auth_client

async def get_access_token(
    x_stack_auth: Optional[str] = Header(None, alias="x-stack-auth")
) -> str:
    """Extract access token from request headers using official Stack Auth header name."""
    if not x_stack_auth:
        logger.warning("Missing x-stack-auth header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    
    try:
        auth_data = json.loads(x_stack_auth)
        access_token = auth_data.get("accessToken")
        if not access_token:
            logger.warning("'accessToken' not found in x-stack-auth header")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed"
            )
        return access_token
    except json.JSONDecodeError:
        logger.warning("Invalid JSON in x-stack-auth header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )

async def get_current_user(
    request: Request,
    access_token: str = Depends(get_access_token),
    stack_client = Depends(get_stack_auth_client)
) -> Dict[str, Any]:
    """
    Verify Stack Auth token and return authenticated user data.
    
    This dependency:
    1. Extracts the access token from the x-stack-auth header
    2. Verifies the token using Stack Auth's official API
    3. Returns the authenticated user data with official Stack Auth structure
    """
    try:
        # Verify the token using Stack Auth's official API
        user = await stack_client.verify_token_via_api(access_token)
        
        # Return user data in the same format as your Clerk implementation
        user_data = {
            "user_id": user.id,
            "display_name": user.display_name,
            "primary_email": user.primary_email,
            "email_verified": user.primary_email_verified,
            "profile_image_url": user.profile_image_url,
            "signed_up_at": user.signed_up_at_millis,
            "last_active_at": user.last_active_at_millis,
            "oauth_providers": user.oauth_providers,
            "has_password": user.has_password,
            "auth_with_email": user.auth_with_email,
            "client_metadata": user.client_metadata,
            "client_read_only_metadata": user.client_read_only_metadata,
            # Additional fields for compatibility with your Clerk pattern
            "session_id": None,  # Stack Auth doesn't have session IDs like Clerk
            "actor": None,       # Stack Auth doesn't have actor concept like Clerk
            "session_claims": {
                "sub": user.id,
                "email": user.primary_email,
                "email_verified": user.primary_email_verified
            }
        }

        logger.info("User authenticated successfully", user_id=user_data["user_id"])
        logger.info(f"user_data: {user_data}")
        return user_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Authentication failed", error=str(e), error_type=type(e).__name__)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )

async def get_optional_user(
    request: Request,
    stack_client = Depends(get_stack_auth_client)
) -> Optional[Dict[str, Any]]:
    """Optional authentication - returns user data if authenticated, None otherwise."""
    try:
        x_stack_auth = request.headers.get("x-stack-auth")
        if not x_stack_auth:
            return None

        auth_data = json.loads(x_stack_auth)
        access_token = auth_data.get("accessToken")
        if not access_token:
            return None

        # Verify the token
        user = await stack_client.verify_token_via_api(access_token)
        
        user_data = {
            "user_id": user.id,
            "display_name": user.display_name,
            "primary_email": user.primary_email,
            "email_verified": user.primary_email_verified,
            "profile_image_url": user.profile_image_url,
            "signed_up_at": user.signed_up_at_millis,
            "last_active_at": user.last_active_at_millis,
            "oauth_providers": user.oauth_providers,
            "has_password": user.has_password,
            "auth_with_email": user.auth_with_email,
            "client_metadata": user.client_metadata,
            "client_read_only_metadata": user.client_read_only_metadata
        }
        
        logger.info("Optional user authenticated successfully", user_id=user_data["user_id"])
        logger.info(f"user_data: {user_data}")
        return user_data
        
    except Exception as e:
        logger.debug("Optional authentication failed", error=str(e))
        return None

# Convenience functions for common data extraction
async def get_current_user_id(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> str:
    """Extract user ID from authenticated user data."""
    return current_user["user_id"]

async def get_current_user_email(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> str:
    """Extract user email from authenticated user data."""
    return current_user["primary_email"]

# Convenience function for checking if user has specific permission
async def require_email_verification(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Require email verification for protected endpoints."""
    if not current_user.get("email_verified"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required"
        )
    return current_user