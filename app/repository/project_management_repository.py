from app.extensions import get_db
from datetime import datetime, timezone

class UserRepository:
    @staticmethod
    def save_template(template_name,created_by,created_on):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO templatemaster (templateName, createdBy, createdOn)
            VALUES (%s,%s,%s) RETURNING templateId
        """, (template_name,created_by,created_on))
        template_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return template_id

    @staticmethod
    def save_task_template(template_id, task_ids):
        conn = None
        try:
            conn = get_db()
            cur = conn.cursor()
            for task_id in task_ids:
                cur.execute("""
                    INSERT INTO templatetasklist (templateId, taskId)
                    VALUES (%s, %s)
                """, (template_id, task_id))
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False
        finally:
            conn.close()
        return True

    @staticmethod
    def get_task_template(template_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT taskid
            FROM templateTaskList
            JOIN taskmaster tm ON tm.taskid =taskid
            WHERE templateid = %s AND tm.is_obsolete =FALSE;
        """, (template_id,))
        tasks = cur.fetchall()
        cur.close()
        return [task[0] for task in tasks]

    @staticmethod
    def get_all_tasks():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                task.taskid,
                task.taskName,
                task.functionid AS function_id,
                func.functionName AS function_name,
                task.weightage,
                task.createdon,
                task.createdby,
                um1.name AS createdbyName,
                task.lastmodifiedby,
                um2.name AS lastmodifiedbyName,
                task.lastmodifiedon
                
            FROM 
                taskmaster AS task
            JOIN 
                functionmaster AS func
            ON 
                task.functionid = func.functionid
            LEFT JOIN
                usermaster AS um1
            ON
                task.createdby = um1.email
            LEFT JOIN 
                usermaster as um2
            ON
                task.lastmodifiedby=um2.email
            WHERE
                task.is_obsolete IS FALSE;
                    
        """)
        tasks = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        result = [dict(zip(column_names, row)) for row in tasks]
        return result
        # print(tasks)
        # return [{
        #     'taskid': task[0],
        #     'taskName': task[1],
        #     'function_id': task[2],
        #     "function_name": task[3],
        #     'weightage': task[4],

        # } for task in tasks]

    @staticmethod
    def get_all_employees():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT email
            FROM userMaster
        """)
        employees = cur.fetchall()
        cur.close()
        print(employees)
        return [{
            'email': employee[0],
        } for employee in employees]

    @staticmethod
    def get_functions(template_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT Distinct f.*
            FROM functionMaster f inner join taskMaster t on (f.functionId = t.functionid) 
            inner join templateTaskList t2 on (t2.taskID = t.taskId)
            where t2.templateId = %s
        """, (template_id,))
        functions = cur.fetchall()
        cur.close()
        print(functions)
        return [{
            'functionId': function[0],
            'functionName': function[1],
        } for function in functions]

    @staticmethod
    def get_all_templates():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM templateMaster
        """)
        templates = cur.fetchall()
        cur.close()
        print(templates)
        return [{
            'templateId': template[0],
            'templateName': template[1],
        } for template in templates]

    @staticmethod
    def save_project(project_name,template_id, created_by, created_on,completion,functionalLeads):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO projectMaster (projectName, projectTemplateId, createdByEmail, createdOn, completion)
            VALUES (%s,%s,%s,%s,%s) RETURNING projectId
        """, (project_name,template_id, created_by, created_on, completion))
        project_id = cur.fetchone()[0]
        project_function_data = [
            (project_id, functionId, leadEmail, 0)
            for functionId, leadEmail in functionalLeads.items()
        ]
        cur.executemany("""
            INSERT INTO projectFunctionMaster (projectId, functionId, functionLeadEmail, completion)
            VALUES (%s, %s, %s, %s)
        """, project_function_data)
        cur.execute("""
            insert into projecttaskmaster (projectid,taskid,assigneeemail,functionid,completion,exception,specialinstruction,weightage,priority,duedate,createdby,createdon,lastupdatedby,lastupdatedon,dependencyoverride,active)
            select distinct p.projectid,t2.taskid,pf.functionleademail ,t2.functionid,false,null,null,t2.weightage,null, null,p.createdbyemail ,now(),null,null,False,True 
            from projectmaster p inner join templatemaster t on (p.projecttemplateid = t.templateid)
            inner join templatetasklist t3 on (t.templateid=t3.templateid)
            inner join taskmaster t2 on (t2.taskid=t3.taskid)
            inner join projectfunctionmaster pf on (pf.projectid = p.projectid and t2.functionid = pf.functionid)
            where p.projectid = %s
        """,(project_id,))
        cur.execute("""
            insert into dependenttaskmaster (projectid, taskid, depdendenttaskid, createdby, createdon)
            select p.projectId,t.taskid, t.depdendenttaskid, p.createdbyemail, now() from templatedependenttasklist t inner join templatemaster t2 on t.templateid = t2.templateid 
            inner join projectmaster p on p.projecttemplateid = t.templateid 
            where p.projectid = %s
        """, (project_id,))
        conn.commit()
        cur.close()
        return project_id

    @staticmethod
    def create_task_in_master(task_name, function_id, weightage, email_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO taskmaster (taskName, functionId, weightage, is_obsolete, created_by, created_on, lastmodifiedby, lastmodifiedon)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING taskId
        """, (task_name, function_id, weightage, False, email_id,datetime.now(timezone.utc()), email_id,  datetime.now(timezone.utc).now() ))
        task_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return task_id
    
    @staticmethod
    def modify_task_in_master(**kwargs):
        
        # constructing set clause 
        set_clause = ",".join([f"{key}=%s" for key, value in kwargs.items() if (value != None) & ((key != "taskid") and (key!= "email_id"))])
        values = [val for key, val in kwargs.items() if (val != None) & ((key != "taskid") and (key!= "email_id"))]

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            f"""
            UPDATE taskmaster tm
            SET {set_clause},
            lastmodifiedon = \'{datetime.now(timezone.utc).now()}\',
            lastmodifiedby = \'{kwargs["email_id"]}\'
            WHERE tm.taskid = \'{kwargs["taskid"]}\'
            RETURNING taskid     
            """, values) 
        task_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return task_id


    @staticmethod
    def get_all_functions():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM functionMaster
        """)
        functions = cur.fetchall()
        cur.close()
        return [{
            'functionId': function[0],
            'functionName': function[1],
        } for function in functions]
    
    @staticmethod
    def get_modify_project_info(projectid):
        conn=get_db()
        cur = conn.cursor()
        cur.execute(f"""
                    SELECT pm.*, tm.templatename FROM projectmaster pm
                    JOIN templatemaster tm ON pm.projecttemplateid = tm.templateid
                    WHERE pm.projectid = \'{projectid}\';""")
        project_info =cur.fetchone()

        column_names = [desc[0] for desc in cur.description]
        cur.close()
        if project_info:
            project_info = dict(zip(column_names, project_info)) 
        modify_project_info = {"project_info": project_info, "function_info": UserRepository.get_project_functions(projectid=projectid)}
        return modify_project_info
        
    
    @staticmethod
    def get_project_functions(projectid):
        conn=get_db()
        cur = conn.cursor()
        cur.execute(f"""
                   SELECT  fm.functionid, fm.functionname, um.username AS functionlead FROM  projectfunctionmaster pfm 
                    JOIN functionmaster fm ON pfm.functionid = fm.functionid
                    JOIN usermaster um ON pfm.functionleademail = um.email
                    WHERE pfm.projectid = \'{projectid}\';""")
        functioninfo = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        functioninfo = [dict(zip(column_names, row)) for row in functioninfo]
        return functioninfo
    
    @staticmethod
    def get_functions_not_in_project(projectid):
        conn=get_db()
        cur = conn.cursor()
        cur.execute(f"""
            SELECT * from functionmaster fm
            WHERE fm.functionid NOT IN (SELECT pfm.functionid FROM projectfunctionmaster pfm WHERE pfm.projectid =\'{projectid}\');""")
        functioninfo=  cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        functioninfo = [dict(zip(column_names, row))for row in functioninfo]
        return functioninfo


    @staticmethod
    def modify_leads(project_id, functionalLeads):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("Delete from projectfunctionmaster where projectid = %s", (project_id,) )
        try:
            for function_id, lead_email in functionalLeads.items():
                print(project_id + function_id + lead_email)
                cur.execute("""
                    INSERT INTO projectFunctionMaster (projectid, functionid, functionleademail, completion)
                    VALUES (%s, %s, %s, 0)
                """, (project_id, function_id, lead_email,))
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        return project_id

    @staticmethod
    def get_all_projects():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT projectid, projectname
            FROM projectMaster
        """)
        projects = cur.fetchall()
        cur.close()
        return [{
            'projectId': project[0],
            'projectName': project[1],
        } for project in projects]

    @staticmethod
    def save_portfolio(portfolio_name, projects):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO portfoliomaster (portfolioName)
            VALUES (%s) RETURNING portfolioId
        """, (portfolio_name,))
        portfolio_id = cur.fetchone()[0]
        project_data = [(portfolio_id, project_id) for project_id in projects]
        cur.executemany("""
            INSERT INTO portfolioprojectmaster (portfolioId, projectId)
            VALUES (%s, %s)
        """, project_data)
        conn.commit()
        cur.close()
        return portfolio_id

    @staticmethod
    def get_all_portfolios():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM portfoliomaster
        """, ())
        projects = cur.fetchall()
        cur.close()
        return [ projects]

    @staticmethod
    def get_project_and_non_project_tasks(project_id):
        conn=get_db()
        cur = conn.cursor()
        get_tasks_in_project_query = """
        SELECT tm.taskid, tm.taskname
        FROM taskmaster tm
        JOIN projectTaskmaster ptm ON tm.taskid = ptm.taskid
        WHERE ptm.projectid = %s;
    """
        cur.execute(get_tasks_in_project_query, (project_id,))
        get_tasks_in_project= cur.fetchall()
        get_tasks_in_project= [{'taskId': taskid, 'taskName': taskname} for taskid, taskname in get_tasks_in_project]


        get_tasks_not_in_project_query = """
        SELECT tm.taskid, tm.taskname
        FROM taskmaster tm
        WHERE tm.taskid NOT IN (SELECT ptm.taskid FROM projectTaskmaster ptm WHERE ptm.projectid = %s);
    """
        cur.execute(get_tasks_not_in_project_query, (project_id,))
        get_tasks_not_in_project= cur.fetchall()
        cur.close()
        get_tasks_not_in_project =  [{'taskId': taskid, 'taskName': taskname} for taskid, taskname in get_tasks_not_in_project]
        return get_tasks_in_project, get_tasks_not_in_project

    @staticmethod
    def modify_project(project_id, added_tasks,removed_tasks,mail):
        conn= get_db()
        cur = conn.cursor()
        try:
            for task_id in removed_tasks:
                cur.execute("""
                    DELETE FROM projectTaskMaster
                    WHERE projectid = %s AND taskid = %s;
                """, (project_id, task_id))
            for task_id in added_tasks:
                cur.execute("""
                    INSERT INTO projectTaskMaster (projectid, taskid, functionid, completion, weightage, createdby, createdon, lastupdatedby, lastupdatedon, active)
                    Values (%s,%s, (SELECT functionid FROM taskmaster WHERE taskid = %s), False, (SELECT weightage FROM taskmaster WHERE taskid = %s), %s, %s, %s, %s, True)
                """, (project_id, task_id, task_id, task_id, mail, datetime.now(), mail, datetime.now()))
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            cur.close()
            conn.close()
            return False
        finally:
            cur.close()
            conn.close()
        return True






    

    





        

