import os
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
import pymysql
from database import get_db
from models import Feedback
from schemas import FeedbackCreate, SuccessResponse
from utils.excel import generate_excel_report

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/feedback", response_model=SuccessResponse, status_code=201)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    request: Request,
    db: pymysql.Connection = Depends(get_db)
):
    """Submit feedback form"""
    try:
        # Get client IP and user agent
        ip_address = request.headers.get("x-forwarded-for") or request.client.host
        user_agent = request.headers.get("user-agent")

        # Create feedback record
        feedback = Feedback.create(
            visual_design=feedback_data.visual_design,
            ease_of_navigation=feedback_data.ease_of_navigation,
            mobile_responsiveness=feedback_data.mobile_responsiveness,
            overall_satisfaction=feedback_data.overall_satisfaction,
            ease_of_tasks=feedback_data.ease_of_tasks,
            quality_of_services=feedback_data.quality_of_services,

            visual_design_issue=feedback_data.visual_design_issue.strip() if feedback_data.visual_design_issue else None,
            ease_of_navigation_issue=feedback_data.ease_of_navigation_issue.strip() if feedback_data.ease_of_navigation_issue else None,
            mobile_responsiveness_issue=feedback_data.mobile_responsiveness_issue.strip() if feedback_data.mobile_responsiveness_issue else None,
            overall_satisfaction_issue=feedback_data.overall_satisfaction_issue.strip() if feedback_data.overall_satisfaction_issue else None,
            ease_of_tasks_issue=feedback_data.ease_of_tasks_issue.strip() if feedback_data.ease_of_tasks_issue else None,
            quality_of_services_issue=feedback_data.quality_of_services_issue.strip() if feedback_data.quality_of_services_issue else None,

            like_most=feedback_data.like_most.strip() if feedback_data.like_most else None,
            improvements=feedback_data.improvements.strip() if feedback_data.improvements else None,
            features=feedback_data.features.strip() if feedback_data.features else None,
            legal_challenges=feedback_data.legal_challenges.strip() if feedback_data.legal_challenges else None,
            additional_comments=feedback_data.additional_comments.strip() if feedback_data.additional_comments else None,

            contact_willing=feedback_data.contact_willing.value if feedback_data.contact_willing else None,
            contact_email=feedback_data.contact_email if feedback_data.contact_email else None,

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

        logger.info(f'Feedback submitted successfully with ID: {feedback.id}')

        return SuccessResponse(
            message="Feedback submitted successfully",
            id=feedback.id,
            submitted_at=feedback.submitted_at
        )

    except Exception as e:
        logger.error(f'Error submitting feedback: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal server error")
