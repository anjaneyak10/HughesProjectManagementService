from app.extensions import get_db

class UserRepository:

    @staticmethod
    def get_all_templates():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT templateid,templateName,taskid
            FROM templateTaskList
        """)
        templates = cur.fetchall()
        cur.close()
        return [{
            'templateid': template[0],
            'templateName': template[1],
            'taskid': template[2]
        } for template in templates
        ]

    @staticmethod
    def get_all_tasks():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT taskid,taskName,function
            FROM taskmaster
        """)
        tasks = cur.fetchall()
        cur.close()
        return [{
            'taskid': task[0],
            'taskName': task[1],
            'function': task[2]
        } for task in tasks]


    @staticmethod
    def save_template(template_id,templateName,taskid):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO templateTaskList (templateid,templateName,taskid)
            VALUES (%s,%s,%s) RETURNING templateId
        """, (template_id,templateName,taskid))
        template_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return template_id

    @staticmethod
    def save_task(task_id,task_name,funcation):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO taskmaster (taskid, taskName,function)
            VALUES (%s,%s,%s) RETURNING taskid
        """, (task_id,task_name,funcation))
        task_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return task_id

    @staticmethod
    def save_project(project_name, project_template_id, project_created_by, project_portfolio,project_created_time):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO projectmaster (projectid,projectName, projectTemplateId, dueDate, createdBy, portfolio)
            VALUES (100,%s,%s,%s,%s,%s) RETURNING projectId
        """, (project_name, project_template_id, project_created_by, project_portfolio,project_created_time))
        project_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return project_id

    @staticmethod
    def get_all_functions():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT tm.function
            FROM templatetasklist ttl
            JOIN taskmaster tm ON ttl.taskid = tm.taskid
            WHERE ttl.templateid = 1;
        """)
        functions = cur.fetchall()
        cur.close()
        print(functions)
        return [{
            'function': function[0]
        } for function in functions
        ]
    @staticmethod
    def save_project():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO projectmaster (projectName, projectTemplateId, dueDate, createdBy, portfolio)
            VALUES ('project1', 1, '2021-06-01', '2021-06-30', 'portfolio1') RETURNING projectId
        """)
        project_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return project_id
