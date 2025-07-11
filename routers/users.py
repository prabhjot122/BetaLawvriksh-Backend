import os
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
import pymysql
from database import get_db
from models import UserRegistration
from schemas import UserRegistrationCreate, SuccessResponse
from utils.excel import generate_excel_report

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=SuccessResponse, status_code=201)
async def register_user(
    user_data: UserRegistrationCreate,
    request: Request,
    db: pymysql.Connection = Depends(get_db)
):
    """Register a new user (USER or Creator)"""
    try:
        # Get client IP and user agent
        ip_address = request.headers.get("x-forwarded-for") or request.client.host
        user_agent = request.headers.get("user-agent")

        # Create user registration record
        registration = UserRegistration.create(
            name=user_data.name.strip(),
            email=user_data.email,
            phone=user_data.phone.strip(),
            gender=user_data.gender.strip() if user_data.gender else None,
            profession=user_data.profession.strip() if user_data.profession else None,
            user_type=user_data.user_type.value,
            ip_address=ip_address,
            user_agent=user_agent
        )

        # Generate updated Excel file (only save locally in development)
        if os.environ.get('FLASK_ENV') == 'development':
            excel_buffer = generate_excel_report()
            if excel_buffer:
                # Save Excel file to disk with error handling (development only)
                try:
                    with open('lawvriksh_data.xlsx', 'wb') as f:
                        f.write(excel_buffer.getvalue())
                except PermissionError:
                    logger.warning('Could not update Excel file - file may be open in another program')
                except Exception as e:
                    logger.error(f'Error saving Excel file: {str(e)}')

        logger.info(f'User registration submitted successfully with ID: {registration.id}')

        return SuccessResponse(
            message="Registration submitted successfully",
            id=registration.id,
            submitted_at=registration.submitted_at
        )

    except Exception as e:
        logger.error(f'Error submitting registration: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal server error")
