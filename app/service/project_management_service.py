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
    def add_template(template_id,templateName, taskid):
        template_id = UserRepository.save_template(template_id,templateName, taskid)
        return template_id
    @staticmethod
    def add_task(task_id,task_name, function):
        task_id = UserRepository.save_task(task_id,task_name, function)
        return task_id
    @staticmethod
    def get_all_tasks():
        tasks = UserRepository.get_all_tasks()
        return tasks
    @staticmethod
    def create_project(project_name, project_description, project_start_date, project_end_date, project_manager):
        project_id = UserRepository.save_project(project_name, project_description, project_start_date, project_end_date, project_manager)
        return project_id
