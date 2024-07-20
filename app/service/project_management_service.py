from app.repository.project_management_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app

class ProjectManagementService:

    @staticmethod
    def get_all_templates():
        templates = UserRepository.get_all_templates()
        return templates
    @staticmethod
    def add_task(task_id,task_name, function):
        task_id = UserRepository.save_task(task_id,task_name, function)
        return task_id
    @staticmethod
    def get_all_tasks():
        tasks = UserRepository.get_all_tasks()
        return tasks
    @staticmethod
    def save_project(project_name, project_template_id, project_created_by, project_portfolio,project_created_time):
        project_id = UserRepository.save_project(project_name, project_template_id, project_created_by, project_portfolio,project_created_time)
        return project_id
    @staticmethod
    def get_all_functions():
        functions = UserRepository.get_all_functions()
        return functions

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
