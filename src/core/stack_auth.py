import requests
from typing import Optional, Dict, Any
from pydantic import BaseModel
import structlog
from src.core.config import settings

logger = structlog.get_logger(__name__)

class StackAuthUser(BaseModel):
    """Official Stack Auth user data structure based on API documentation"""
    id: str
    display_name: Optional[str] = None
    primary_email: str
    primary_email_verified: bool
    profile_image_url: Optional[str] = None
    signed_up_at_millis: int
    last_active_at_millis: int
    oauth_providers: list
    has_password: bool
    auth_with_email: bool
    client_metadata: Optional[Dict[str, Any]] = None
    client_read_only_metadata: Optional[Dict[str, Any]] = None

class StackAuthClient:
    """Stack Auth client using official API headers and structure"""
    
    def __init__(self):
        self.settings = settings
        self.api_base_url = self.settings.stack_api_base_url
        
        # Initialize JWKS client for JWT verification
        # self.jwks_client = PyJWKClient(
        #     f"{self.api_base_url}/api/v1/projects/{self.settings.stack_project_id}/.well-known/jwks.json"
        # )
        
        logger.info("Stack Auth client initialized", project_id=self.settings.stack_project_id)
    
    def _make_stack_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request to Stack Auth API using official headers from docs"""
        headers = {
            'X-Stack-Access-Type': 'server',  # Official header name from docs
            'X-Stack-Project-Id': self.settings.stack_project_id,
            'X-Stack-Publishable-Client-Key': self.settings.stack_publishable_client_key,
            'X-Stack-Secret-Server-Key': self.settings.stack_secret_server_key,
            **kwargs.pop('headers', {})
        }
        
        url = f"{self.api_base_url}/{endpoint}"
        
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Stack Auth API request failed", 
                        method=method, endpoint=endpoint, error=str(e))
            raise Exception(f"Stack Auth API request failed: {str(e)}")
    
    async def verify_token_via_api(self, access_token: str) -> StackAuthUser:
        """Verify access token via REST API (comprehensive user data)"""
        try:
            user_data = self._make_stack_request(
                'GET', 
                'api/v1/users/me',
                headers={'X-Stack-Access-Token': access_token}  # Official header name
            )
            
            logger.info("User authenticated via API", user_id=user_data.get('id'))
            return StackAuthUser(**user_data)
            
        except Exception as e:
            logger.error("Token verification via API failed", error=str(e))
            raise
    
    # async def verify_token_via_jwt(self, access_token: str) -> Dict[str, Any]:
    #     """Verify access token locally via JWT (faster, basic user data)"""
    #     try:
    #         signing_key = self.jwks_client.get_signing_key_from_jwt(access_token)
    #         payload = jwt.decode(
    #             access_token,
    #             signing_key.key,
    #             algorithms=["ES256"],
    #             audience=self.settings.stack_project_id
    #         )
            
    #         logger.info("User authenticated via JWT", user_id=payload.get('sub'))
    #         return payload
            
    #     except Exception as e:
    #         logger.error("JWT verification failed", error=str(e))
    #         raise Exception("Invalid access token")

# Global instance
stack_auth_client = StackAuthClient()