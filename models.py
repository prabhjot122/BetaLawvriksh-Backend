from datetime import datetime
from typing import Optional, Dict, Any
import pymysql
from database import get_db_connection
import logging

logger = logging.getLogger(__name__)


class UserRegistration:
    def __init__(self, id: Optional[int] = None, name: str = "", email: str = "",
                 phone: str = "", gender: Optional[str] = None, profession: Optional[str] = None,
                 user_type: str = "", submitted_at: Optional[datetime] = None,
                 ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.gender = gender
        self.profession = profession
        self.user_type = user_type
        self.submitted_at = submitted_at
        self.ip_address = ip_address
        self.user_agent = user_agent

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'gender': self.gender,
            'profession': self.profession,
            'user_type': self.user_type,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent
        }

    @classmethod
    def create(cls, name: str, email: str, phone: str, user_type: str,
               gender: Optional[str] = None, profession: Optional[str] = None,
               ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> 'UserRegistration':
        """Create a new user registration"""
        try:
            with get_db_connection() as connection:
                cursor = connection.cursor()

                query = """
                    INSERT INTO user_registrations
                    (name, email, phone, gender, profession, user_type, ip_address, user_agent)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (name, email, phone, gender, profession, user_type, ip_address, user_agent)

                cursor.execute(query, values)
                connection.commit()

                # Get the created record
                user_id = cursor.lastrowid
                cursor.execute("SELECT * FROM user_registrations WHERE id = %s", (user_id,))
                row = cursor.fetchone()

                if row:
                    return cls._from_row(row)
                else:
                    raise Exception("Failed to retrieve created user registration")

        except Exception as e:
            logger.error(f"Error creating user registration: {e}")
            raise

    @classmethod
    def get_all(cls, page: int = 1, per_page: int = 50) -> tuple[list['UserRegistration'], int]:
        """Get all user registrations with pagination"""
        try:
            with get_db_connection() as connection:
                cursor = connection.cursor()

                # Get total count
                cursor.execute("SELECT COUNT(*) FROM user_registrations")
                total = cursor.fetchone()[0]

                # Get paginated results
                offset = (page - 1) * per_page
                query = """
                    SELECT * FROM user_registrations
                    ORDER BY submitted_at DESC
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (per_page, offset))
                rows = cursor.fetchall()

                registrations = [cls._from_row(row) for row in rows]
                return registrations, total

        except Exception as e:
            logger.error(f"Error getting user registrations: {e}")
            raise

    @classmethod
    def _from_row(cls, row: tuple) -> 'UserRegistration':
        """Create UserRegistration instance from database row"""
        return cls(
            id=row[0],
            name=row[1],
            email=row[2],
            phone=row[3],
            gender=row[4],
            profession=row[5],
            user_type=row[6],
            submitted_at=row[7],
            ip_address=row[8],
            user_agent=row[9]
        )



class Feedback:
    def __init__(self, id: Optional[int] = None, visual_design: Optional[int] = None,
                 ease_of_navigation: Optional[int] = None, mobile_responsiveness: Optional[int] = None,
                 overall_satisfaction: Optional[int] = None, ease_of_tasks: Optional[int] = None,
                 quality_of_services: Optional[int] = None, visual_design_issue: Optional[str] = None,
                 ease_of_navigation_issue: Optional[str] = None, mobile_responsiveness_issue: Optional[str] = None,
                 overall_satisfaction_issue: Optional[str] = None, ease_of_tasks_issue: Optional[str] = None,
                 quality_of_services_issue: Optional[str] = None, like_most: Optional[str] = None,
                 improvements: Optional[str] = None, features: Optional[str] = None,
                 legal_challenges: Optional[str] = None, additional_comments: Optional[str] = None,
                 contact_willing: Optional[str] = None, contact_email: Optional[str] = None,
                 submitted_at: Optional[datetime] = None, ip_address: Optional[str] = None,
                 user_agent: Optional[str] = None):
        self.id = id
        self.visual_design = visual_design
        self.ease_of_navigation = ease_of_navigation
        self.mobile_responsiveness = mobile_responsiveness
        self.overall_satisfaction = overall_satisfaction
        self.ease_of_tasks = ease_of_tasks
        self.quality_of_services = quality_of_services
        self.visual_design_issue = visual_design_issue
        self.ease_of_navigation_issue = ease_of_navigation_issue
        self.mobile_responsiveness_issue = mobile_responsiveness_issue
        self.overall_satisfaction_issue = overall_satisfaction_issue
        self.ease_of_tasks_issue = ease_of_tasks_issue
        self.quality_of_services_issue = quality_of_services_issue
        self.like_most = like_most
        self.improvements = improvements
        self.features = features
        self.legal_challenges = legal_challenges
        self.additional_comments = additional_comments
        self.contact_willing = contact_willing
        self.contact_email = contact_email
        self.submitted_at = submitted_at
        self.ip_address = ip_address
        self.user_agent = user_agent

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'visual_design': self.visual_design,
            'ease_of_navigation': self.ease_of_navigation,
            'mobile_responsiveness': self.mobile_responsiveness,
            'overall_satisfaction': self.overall_satisfaction,
            'ease_of_tasks': self.ease_of_tasks,
            'quality_of_services': self.quality_of_services,
            'visual_design_issue': self.visual_design_issue,
            'ease_of_navigation_issue': self.ease_of_navigation_issue,
            'mobile_responsiveness_issue': self.mobile_responsiveness_issue,
            'overall_satisfaction_issue': self.overall_satisfaction_issue,
            'ease_of_tasks_issue': self.ease_of_tasks_issue,
            'quality_of_services_issue': self.quality_of_services_issue,
            'like_most': self.like_most,
            'improvements': self.improvements,
            'features': self.features,
            'legal_challenges': self.legal_challenges,
            'additional_comments': self.additional_comments,
            'contact_willing': self.contact_willing,
            'contact_email': self.contact_email,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent
        }

    @classmethod
    def create(cls, visual_design: Optional[int] = None, ease_of_navigation: Optional[int] = None,
               mobile_responsiveness: Optional[int] = None, overall_satisfaction: Optional[int] = None,
               ease_of_tasks: Optional[int] = None, quality_of_services: Optional[int] = None,
               visual_design_issue: Optional[str] = None, ease_of_navigation_issue: Optional[str] = None,
               mobile_responsiveness_issue: Optional[str] = None, overall_satisfaction_issue: Optional[str] = None,
               ease_of_tasks_issue: Optional[str] = None, quality_of_services_issue: Optional[str] = None,
               like_most: Optional[str] = None, improvements: Optional[str] = None,
               features: Optional[str] = None, legal_challenges: Optional[str] = None,
               additional_comments: Optional[str] = None, contact_willing: Optional[str] = None,
               contact_email: Optional[str] = None, ip_address: Optional[str] = None,
               user_agent: Optional[str] = None) -> 'Feedback':
        """Create a new feedback"""
        try:
            with get_db_connection() as connection:
                cursor = connection.cursor()

                query = """
                    INSERT INTO feedback
                    (visual_design, ease_of_navigation, mobile_responsiveness, overall_satisfaction,
                     ease_of_tasks, quality_of_services, visual_design_issue, ease_of_navigation_issue,
                     mobile_responsiveness_issue, overall_satisfaction_issue, ease_of_tasks_issue,
                     quality_of_services_issue, like_most, improvements, features, legal_challenges,
                     additional_comments, contact_willing, contact_email, ip_address, user_agent)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    visual_design, ease_of_navigation, mobile_responsiveness, overall_satisfaction,
                    ease_of_tasks, quality_of_services, visual_design_issue, ease_of_navigation_issue,
                    mobile_responsiveness_issue, overall_satisfaction_issue, ease_of_tasks_issue,
                    quality_of_services_issue, like_most, improvements, features, legal_challenges,
                    additional_comments, contact_willing, contact_email, ip_address, user_agent
                )

                cursor.execute(query, values)
                connection.commit()

                # Get the created record
                feedback_id = cursor.lastrowid
                cursor.execute("SELECT * FROM feedback WHERE id = %s", (feedback_id,))
                row = cursor.fetchone()

                if row:
                    return cls._from_row(row)
                else:
                    raise Exception("Failed to retrieve created feedback")

        except pymysql.Error as e:
            logger.error(f"Error creating feedback: {e}")
            raise

    @classmethod
    def get_all(cls, page: int = 1, per_page: int = 50) -> tuple[list['Feedback'], int]:
        """Get all feedback with pagination"""
        try:
            with get_db_connection() as connection:
                cursor = connection.cursor()

                # Get total count
                cursor.execute("SELECT COUNT(*) FROM feedback")
                total = cursor.fetchone()[0]

                # Get paginated results
                offset = (page - 1) * per_page
                query = """
                    SELECT * FROM feedback
                    ORDER BY submitted_at DESC
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query, (per_page, offset))
                rows = cursor.fetchall()

                feedback_list = [cls._from_row(row) for row in rows]
                return feedback_list, total

        except Exception as e:
            logger.error(f"Error getting feedback: {e}")
            raise

    @classmethod
    def _from_row(cls, row: tuple) -> 'Feedback':
        """Create Feedback instance from database row"""
        return cls(
            id=row[0],
            visual_design=row[1],
            ease_of_navigation=row[2],
            mobile_responsiveness=row[3],
            overall_satisfaction=row[4],
            ease_of_tasks=row[5],
            quality_of_services=row[6],
            visual_design_issue=row[7],
            ease_of_navigation_issue=row[8],
            mobile_responsiveness_issue=row[9],
            overall_satisfaction_issue=row[10],
            ease_of_tasks_issue=row[11],
            quality_of_services_issue=row[12],
            like_most=row[13],
            improvements=row[14],
            features=row[15],
            legal_challenges=row[16],
            additional_comments=row[17],
            contact_willing=row[18],
            contact_email=row[19],
            submitted_at=row[20],
            ip_address=row[21],
            user_agent=row[22]
        )
