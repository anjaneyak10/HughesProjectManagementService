from xmlrpc.client import DateTime

from flask import Blueprint, request, jsonify
from app.service.project_management_service import ProjectManagementService
from flask_cors import cross_origin

auth_bp = Blueprint('auth_bp', __name__)
@cross_origin
@auth_bp.route('/getalltemplates', methods=['GET'])
def get_all_templates():
    templates = ProjectManagementService.get_all_templates()
    if templates:
        return jsonify({'templates': templates}), 200
    return jsonify({'message': 'No templates found'}), 404

@cross_origin
@auth_bp.route('/addTemplates', methods=['POST'])
def add_templates():
    data = request.get_json()
    template_id = data.get('templateid')
    template_name = data.get('templateName')
    task_id = data.get('taskid')
    user = ProjectManagementService.add_template(template_id,template_name, task_id)
    if user:
        return jsonify({'message': 'template created successfully'}), 201
    return jsonify({'message': 'User already exists'}), 400
@cross_origin
@auth_bp.route('/addTasks', methods=['POST'])
def add_tasks():
    data = request.get_json()
    task_id = data.get('taskid')
    task_name = data.get('taskName')
    function = data.get('function')
    user = ProjectManagementService.add_task(task_id,task_name, function)
    if user:
        return jsonify({'message': 'task created successfully'}), 201
    return jsonify({'message': 'User already exists'}), 400
@cross_origin
@auth_bp.route('/getalltasks', methods=['GET'])
def get_all_tasks():
    tasks = ProjectManagementService.get_all_tasks()
    print(tasks)
    if tasks:
        return jsonify({'tasks': tasks}), 200
    return jsonify({'message': 'No tasks found'}), 404

@cross_origin
@auth_bp.route('/getallfunctions', methods=['GET'])
def get_all_functions():
    functions = ProjectManagementService.get_all_functions()
    if functions:
        return jsonify(functions), 200
    return jsonify({'message': 'No functions found'}), 404


@cross_origin
@auth_bp.route('/addproject', methods=['POST'])
def add_project():
    data = request.get_json()
    project_name = data.get('projectName')
    project_template_id = data.get('projectTemplateId')
    project_created_by = data.get('projectCreatedBy')
    project_portfolio = data.get('portfolio')
    project_created_time= DateTime.now()
    project_id = ProjectManagementService.save_project(project_name, project_template_id, project_created_by, project_portfolio,project_created_time)
    if project_id:
        return jsonify({'message': 'project created successfully'}), 201
    return jsonify({'message': 'project already exists'}), 400
