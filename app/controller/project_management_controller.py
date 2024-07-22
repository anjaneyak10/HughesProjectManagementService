from xmlrpc.client import DateTime
import datetime

from flask import Blueprint, request, jsonify
from app.service.project_management_service import ProjectManagementService
from flask_cors import cross_origin

auth_bp = Blueprint('auth_bp', __name__)


@cross_origin
@auth_bp.route('/addTemplate', methods=['POST'])
def add_template():
    data = request.get_json()
    template_name = data.get('templateName')
    created_by = data.get('createdBy')
    created_on = datetime.datetime.now()
    template_id = ProjectManagementService.save_template(template_name, created_by, created_on)
    if template_id:
        return jsonify({'message': 'template created successfully',"template_id":template_id}), 201
    return jsonify({'message': 'template already exists'}), 400

@cross_origin
@auth_bp.route('/addtasktotemplate', methods=['POST'])
def add_task_to_template():
    data = request.get_json()
    template_id = data.get('templateId')
    task_ids = data.get('taskId')
    if ProjectManagementService.save_task_template(template_id,task_ids):
        return jsonify({'message': 'task added to template successfully'}), 201
    return jsonify({'message': 'error in saving tasks'}), 400

@cross_origin
@auth_bp.route('/gettasktemplate', methods=['POST'])
def get_task_template():
    data = request.get_json()
    template_id = data.get('templateId')
    tasks = ProjectManagementService.get_task_template(template_id)
    if tasks:
        return jsonify({'tasks': tasks}), 200
    return jsonify({'message': 'No tasks found'}), 404

@cross_origin
@auth_bp.route('/getalltasks', methods=['GET'])
def get_all_tasks():
    tasks = ProjectManagementService.get_all_tasks()
    print(tasks)
    if tasks:
        return jsonify({'tasks': tasks}), 200
    return jsonify({'message': 'No tasks found'}), 404
