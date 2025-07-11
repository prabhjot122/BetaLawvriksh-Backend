import os
from fastapi import HTTPException, Header
from typing import Optional


def verify_admin_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify admin API key"""
    expected_key = os.environ.get('ADMIN_API_KEY', 'admin-key-123')
    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
