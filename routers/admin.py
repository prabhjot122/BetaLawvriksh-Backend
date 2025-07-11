import io
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
import pymysql
from database import get_db
from models import UserRegistration, Feedback
from schemas import FeedbackListResponse, UserRegistrationListResponse
from utils.excel import generate_excel_report
from routers.auth import verify_admin_api_key

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/feedback", response_model=FeedbackListResponse)
async def get_feedback(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: pymysql.Connection = Depends(get_db),
    _: bool = Depends(verify_admin_api_key)
):
    """Get all feedback (admin only)"""
    try:
        # Get feedback with pagination
        feedback_list, total = Feedback.get_all(page=page, per_page=per_page)

        # Calculate total pages
        pages = (total + per_page - 1) // per_page

        return FeedbackListResponse(
            feedback=[f.to_dict() for f in feedback_list],
            total=total,
            pages=pages,
            current_page=page,
            per_page=per_page
        )

    except Exception as e:
        logger.error(f'Error retrieving feedback: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/registrations", response_model=UserRegistrationListResponse)
async def get_registrations(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: pymysql.Connection = Depends(get_db),
    _: bool = Depends(verify_admin_api_key)
):
    """Get all user registrations (admin only)"""
    try:
        # Get registrations with pagination
        registrations, total = UserRegistration.get_all(page=page, per_page=per_page)

        # Calculate total pages
        pages = (total + per_page - 1) // per_page

        return UserRegistrationListResponse(
            registrations=[r.to_dict() for r in registrations],
            total=total,
            pages=pages,
            current_page=page,
            per_page=per_page
        )

    except Exception as e:
        logger.error(f'Error retrieving registrations: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/download-excel")
async def download_excel(
    db: pymysql.Connection = Depends(get_db),
    _: bool = Depends(verify_admin_api_key)
):
    """Download Excel file with all data (admin only)"""
    try:
        # Generate Excel file
        excel_buffer = generate_excel_report()
        if not excel_buffer:
            raise HTTPException(status_code=500, detail="Failed to generate Excel file")

        # Create filename with timestamp
        filename = f'lawvriksh_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        # Return file as streaming response
        return StreamingResponse(
            io.BytesIO(excel_buffer.getvalue()),
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        logger.error(f'Error downloading Excel file: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal server error")
