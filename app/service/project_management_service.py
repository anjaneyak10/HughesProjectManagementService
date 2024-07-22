from app.repository.project_management_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app

class ProjectManagementService:


    @staticmethod
    def save_template(template_name,created_by,created_on ):
        template_id = UserRepository.save_template(template_name,created_by,created_on)
        return template_id

    @staticmethod
    def save_task_template(template_id,task_ids):
        return UserRepository.save_task_template(template_id,task_ids)

    @staticmethod
    def get_task_template(template_id):
        return UserRepository.get_task_template(template_id)
