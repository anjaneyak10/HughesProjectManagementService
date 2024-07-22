from app.extensions import get_db

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
            WHERE templateid = %s
        """, (template_id,))
        tasks = cur.fetchall()
        cur.close()
        return [task[0] for task in tasks]

    @staticmethod
    def get_all_tasks():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM taskmaster
        """)
        tasks = cur.fetchall()
        cur.close()
        print(tasks)
        return [{
            'taskid': task[0],
            'taskName': task[1],
            'function': task[2],
            'weightage': task[3],
        } for task in tasks]
