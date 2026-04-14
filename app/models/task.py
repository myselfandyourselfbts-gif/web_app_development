import sqlite3
from datetime import datetime

class TaskModel:
    def __init__(self, db_path='instance/database.db'):
        self.db_path = db_path
        
    def _get_connection(self):
        """建立並回傳資料庫連線，同時設定 Row factory 方便以字典格式讀取"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, title):
        """新增任務"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, 0)", (title,))
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id

    def get_all(self):
        """取得所有任務，按建立時間由新到舊排序"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_by_id(self, task_id):
        """根據 ID 取得單一任務"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def update(self, task_id, title=None, completed=None):
        """更新任務標題或是完成狀態"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if completed is not None:
            updates.append("completed = ?")
            # SQLite 的 boolean 通常用 int 表示
            params.append(1 if completed else 0)
            
        if not updates:
            return False
            
        params.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def delete(self, task_id):
        """刪除指定 ID 的任務"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
