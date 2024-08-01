from app.repository.project_management_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app
from collections import defaultdict

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

    @staticmethod
    def get_all_tasks():
        tasks = UserRepository.get_all_tasks()
        return tasks

    @staticmethod
    def get_all_employees():
        employees = UserRepository.get_all_employees()
        return employees

    @staticmethod
    def get_functions(template_id):
        functions = UserRepository.get_functions(template_id)
        return functions

    @staticmethod
    def get_all_templates():
        templates = UserRepository.get_all_templates()
        return templates
    
    @staticmethod
    def save_project(project_name,template_id, created_by, created_on,completion,functionalLeads):
        project_id = UserRepository.save_project(project_name,template_id, created_by, created_on,completion,functionalLeads)
        return project_id

    @staticmethod
    def get_all_tasks_by_functions():
        tasks = UserRepository.get_all_tasks()
        tasks_by_functions = defaultdict(list)
        for task in tasks:
            tasks_by_functions[task['function_name']].append(task['taskName'])
        return tasks_by_functions

    @staticmethod
    def create_task_in_master(task_name, function_id, weightage, email_id):
        return UserRepository.create_task_in_master(task_name, function_id, weightage, email_id)
    
    @staticmethod
    def modify_task_in_master(taskid,email_id, taskname=None, functionid=None, weightage=None, is_obsolete=None,  ):
        return UserRepository.modify_task_in_master(taskid=taskid, taskname=taskname, functionid=functionid, weightage=weightage, is_obsolete=is_obsolete, email_id=email_id)
    
    @staticmethod
    def get_all_functions():
        functions = UserRepository.get_all_functions()
        return functions
    
    @staticmethod
    def get_modify_project_info(projectid:str):
        return UserRepository.get_modify_project_info(projectid=projectid)
    
    @staticmethod
    def get_functions_not_in_project(projectid:str):
        return UserRepository.get_functions_not_in_project(projectid=projectid)

    @staticmethod
    def modify_leads(projectId,functionalLeads):
        return UserRepository.modify_leads(projectId,functionalLeads)

