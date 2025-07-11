from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserTypeEnum(str, Enum):
    USER = "USER"
    CREATOR = "Creator"


class ContactWillingEnum(str, Enum):
    YES = "yes"
    NO = "no"


# User Registration Schemas
class UserRegistrationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=20)
    gender: Optional[str] = Field(None, max_length=50)
    profession: Optional[str] = Field(None, max_length=255)
    user_type: UserTypeEnum = Field(..., alias="userType")

    class Config:
        populate_by_name = True


class UserRegistrationResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    gender: Optional[str]
    profession: Optional[str]
    user_type: str
    submitted_at: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]

    class Config:
        from_attributes = True


# Feedback Schemas
class FeedbackCreate(BaseModel):
    # Rating questions (1-5 scale)
    visual_design: Optional[int] = Field(None, ge=1, le=5, alias="visualDesign")
    ease_of_navigation: Optional[int] = Field(None, ge=1, le=5, alias="easeOfNavigation")
    mobile_responsiveness: Optional[int] = Field(None, ge=1, le=5, alias="mobileResponsiveness")
    overall_satisfaction: Optional[int] = Field(None, ge=1, le=5, alias="overallSatisfaction")
    ease_of_tasks: Optional[int] = Field(None, ge=1, le=5, alias="easeOfTasks")
    quality_of_services: Optional[int] = Field(None, ge=1, le=5, alias="qualityOfServices")
    
    # Conditional fields for low ratings
    visual_design_issue: Optional[str] = Field(None, alias="visualDesignIssue")
    ease_of_navigation_issue: Optional[str] = Field(None, alias="easeOfNavigationIssue")
    mobile_responsiveness_issue: Optional[str] = Field(None, alias="mobileResponsivenessIssue")
    overall_satisfaction_issue: Optional[str] = Field(None, alias="overallSatisfactionIssue")
    ease_of_tasks_issue: Optional[str] = Field(None, alias="easeOfTasksIssue")
    quality_of_services_issue: Optional[str] = Field(None, alias="qualityOfServicesIssue")
    
    # Text area questions
    like_most: Optional[str] = Field(None, alias="likeMost")
    improvements: Optional[str] = None
    features: Optional[str] = None
    legal_challenges: Optional[str] = Field(None, alias="legalChallenges")
    additional_comments: Optional[str] = Field(None, alias="additionalComments")
    
    # Follow-up questions
    contact_willing: Optional[ContactWillingEnum] = Field(None, alias="contactWilling")
    contact_email: Optional[EmailStr] = Field(None, alias="contactEmail")

    class Config:
        populate_by_name = True

    @model_validator(mode='after')
    def validate_feedback_data(self):
        # Validate contact email
        if self.contact_willing == ContactWillingEnum.YES and not self.contact_email:
            raise ValueError('Email is required when willing to be contacted')

        # Validate issue fields for low ratings
        rating_issue_pairs = [
            (self.visual_design, self.visual_design_issue, 'visual design'),
            (self.ease_of_navigation, self.ease_of_navigation_issue, 'ease of navigation'),
            (self.mobile_responsiveness, self.mobile_responsiveness_issue, 'mobile responsiveness'),
            (self.overall_satisfaction, self.overall_satisfaction_issue, 'overall satisfaction'),
            (self.ease_of_tasks, self.ease_of_tasks_issue, 'ease of tasks'),
            (self.quality_of_services, self.quality_of_services_issue, 'quality of services')
        ]

        for rating, issue, field_name in rating_issue_pairs:
            if rating and rating < 3 and not issue:
                raise ValueError(f'Please explain what you didn\'t like for {field_name} (rating below 3)')

        return self


class FeedbackResponse(BaseModel):
    id: int
    visual_design: Optional[int]
    ease_of_navigation: Optional[int]
    mobile_responsiveness: Optional[int]
    overall_satisfaction: Optional[int]
    ease_of_tasks: Optional[int]
    quality_of_services: Optional[int]
    visual_design_issue: Optional[str]
    ease_of_navigation_issue: Optional[str]
    mobile_responsiveness_issue: Optional[str]
    overall_satisfaction_issue: Optional[str]
    ease_of_tasks_issue: Optional[str]
    quality_of_services_issue: Optional[str]
    like_most: Optional[str]
    improvements: Optional[str]
    features: Optional[str]
    legal_challenges: Optional[str]
    additional_comments: Optional[str]
    contact_willing: Optional[str]
    contact_email: Optional[str]
    submitted_at: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]

    class Config:
        from_attributes = True


# Generic Response Schemas
class SuccessResponse(BaseModel):
    message: str
    id: int
    submitted_at: datetime


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


class PaginatedResponse(BaseModel):
    total: int
    pages: int
    current_page: int
    per_page: int


class UserRegistrationListResponse(PaginatedResponse):
    registrations: List[UserRegistrationResponse]


class FeedbackListResponse(PaginatedResponse):
    feedback: List[FeedbackResponse]


class ErrorResponse(BaseModel):
    error: str
    details: Optional[List[str]] = None


class HomeResponse(BaseModel):
    message: str
    version: str
    endpoints: dict
