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
    # print(tasks)
    if tasks:
        return jsonify({'tasks': tasks}), 200
    return jsonify({'message': 'No tasks found'}), 404

@cross_origin
@auth_bp.route('/getalltasksbyfunctions', methods=['GET'])
def get_all_tasks_by_functions():
    tasks = ProjectManagementService.get_all_tasks_by_functions()
    if tasks:
        return jsonify(tasks), 200
    return jsonify({'message': 'No tasks found'}), 404

@cross_origin
@auth_bp.route('/getfunctions', methods=['POST'])
def get_functions():
    data=request.get_json()
    template_id= data.get('templateId')
    functions = ProjectManagementService.get_functions(template_id)
    if functions:
        return jsonify(functions), 200
    return jsonify({'message': 'No Functions found'}), 404

@cross_origin
@auth_bp.route('/getallemployees', methods=['GET'])
def get_all_employees():
    employees = ProjectManagementService.get_all_employees()
    # print(employees)
    if employees:
        return jsonify({'employees': employees}), 200
    return jsonify({'message': 'No Employees found'}), 404

@cross_origin
@auth_bp.route('/getalltemplates', methods=['GET'])
def get_all_templates():
    templates = ProjectManagementService.get_all_templates()
    # print(templates)
    if templates:
        return jsonify({'templates': templates}), 200
    return jsonify({'message': 'No Functions found'}), 404

@cross_origin
@auth_bp.route('/saveproject', methods=['POST'])
def create_project():
    data = request.get_json()
    project_name = data.get('projectName')
    template_id = data.get('projectTemplateId')
    created_by = data.get('createdByEmail')
    created_on = datetime.datetime.now()
    functionalLeads = data.get('projectFunctionLeads')
    completion = False
    project_id = ProjectManagementService.save_project(project_name,template_id, created_by, created_on,completion,functionalLeads)
    if project_id:
        return jsonify({'message': 'Project Created Successfully',"project_id":project_id}), 201
    return jsonify({'message': 'Project already exists'}), 400

@cross_origin
@auth_bp.route('/createtaskinmaster', methods=['POST'])
def create_task_in_master():
    data = request.get_json()
    task_name = data.get('taskName')
    function_id = data.get('functionId')
    weightage = data.get('weightage')
    email_id = data.get("emailId")
    tasks = ProjectManagementService.create_task_in_master(task_name, function_id, weightage, email_id)
    if tasks:
        return jsonify({'message': 'Tasks Created Successfully'}), 201
    return jsonify({'message': 'Tasks already exists'}), 400

@cross_origin
@auth_bp.route('/modifytaskinmaster', methods=['POST'])
def modify_task_in_master():
    data = request.get_json()
    task_name = data.get("taskName", None)
    task_id = data.get("taskId")
    function_id = data.get("functionId", None)
    weightage = data.get("weightage", None)
    is_obsolete = data.get("isObsolete", None)
    email_id = data.get("emailId")
    try:
        task_id =ProjectManagementService.modify_task_in_master(taskid=task_id, taskname=task_name, functionid=function_id, weightage=weightage, is_obsolete=is_obsolete, email_id=email_id)
        return jsonify({"message": "Task Modified Successfully"}), 200
    except Exception as e:
        return jsonify({"message":e}), 400

@cross_origin
@auth_bp.route('/getallfunctions', methods=['GET'])
def get_all_functions():
    functions = ProjectManagementService.get_all_functions()
    if functions:
        return jsonify(functions), 200
    return jsonify({'message': 'No Functions found'}), 404


@cross_origin
@auth_bp.route("/getmodifyprojectinfo", methods=["GET"])
def get_modify_project_info():
    try:

        project_id = request.args.get("projectid")
        print(project_id)
        project_info = ProjectManagementService.get_modify_project_info(projectid=project_id)
        print(project_info)
        return jsonify(project_info),200
    except Exception as e:
        return jsonify({"message": "Unable to get the project data", "data":e}),400
    
@cross_origin
@auth_bp.route("/getfunctionsnotinproject", methods=["GET"])
def get_functions_not_in_projec():
    project_id = request.args.get("projectid")
    functions = ProjectManagementService.get_functions_not_in_project(project_id)
    return jsonify(functions), 200


@cross_origin
@auth_bp.route("/modifyfunctionalleads", methods=["POST"])
def modifyprojectLeads():
    data = request.get_json()
    data=ProjectManagementService.modify_leads(data.get('projectId'), data.get('projectFunctionLeads'))
    return jsonify(data), 200

@cross_origin
@auth_bp.route('/getallprojects', methods=['GET'])
def get_all_projects():
    projects = ProjectManagementService.get_all_projects()
    if projects:
        return jsonify(projects), 200
    return jsonify({'message': 'No projects found'}), 404

@cross_origin
@auth_bp.route('/saveportfolio', methods=['POST'])
def save_portfolio():
    data = request.get_json()
    portfolio_name = data.get('portfolioName')
    projects = data.get('projects')
    portfolio_id = ProjectManagementService.save_portfolio(portfolio_name, projects)
    if portfolio_id:
        return jsonify({'message': 'portfolio created successfully',"portfolio_id":portfolio_id}), 201
    return jsonify({'message': 'portfolio already exists'}), 400

@cross_origin
@auth_bp.route('/getallportfolios', methods=['GET'])
def get_all_portfolios():
    portfolios = ProjectManagementService.get_all_portfolios()
    if portfolios:
        return jsonify(portfolios), 200
    return jsonify({'message': 'No portfolios found'}), 404

@cross_origin
@auth_bp.route('/getallprojecttasksandnonprojecttasks', methods=['GET'])
def get_all_project_tasks_and_non_project_tasks():
    project_id = request.args.get('projectId')
    print(project_id)
    tasks_in_project,tasks_not_in_project = ProjectManagementService.get_project_and_non_project_tasks(project_id)
    if tasks_in_project or tasks_not_in_project:
        print(tasks_in_project)
        print(tasks_not_in_project)
        return jsonify({'tasks_in_project': tasks_in_project,'tasks_not_in_project':tasks_not_in_project}), 200
    return jsonify({'message': 'No tasks found'}), 404

@cross_origin
@auth_bp.route('/modifyprojecttasks', methods=['PUT'])
def modify_project():
    data = request.get_json()
    print(data)
    project_id = data.get('projectId')
    added_tasks = data.get('addedTasks')
    removed_tasks = data.get('removedTasks')
    email = data.get('email')
    print(project_id,added_tasks,removed_tasks,email)
    project_id = ProjectManagementService.modify_project(project_id, added_tasks, removed_tasks,email)
    if project_id:
        return jsonify({'message': 'Project Modified Successfully',"project_id":project_id}), 201
    return jsonify({'message': 'Project already exists'}), 400
