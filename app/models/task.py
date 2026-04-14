import sqlite3
import traceback
from datetime import datetime

class TaskModel:
    def __init__(self, db_path='instance/database.db'):
        self.db_path = db_path
        
    def get_db_connection(self):
        """建立並回傳資料庫連線，同時設定 Row factory 方便以字典格式讀取"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, title):
        """
        新增任務
        
        Args:
            title (str): 任務標題
            
        Returns:
            int/None: 成功回傳 task_id，失敗回傳 None
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, 0)", (title,))
            conn.commit()
            task_id = cursor.lastrowid
            conn.close()
            return task_id
        except Exception as e:
            print(f"Error in TaskModel.create: {e}")
            traceback.print_exc()
            return None

    def get_all(self):
        """
        取得所有任務
        
        Returns:
            list: 包含任務字典的清單，按建立時間由新到舊排序
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error in TaskModel.get_all: {e}")
            return []

    def get_by_id(self, id):
        """
        根據 ID 取得單一任務
        
        Args:
            id (int): 任務 ID
            
        Returns:
            dict/None: 任務資料字典，找不到或錯誤時回傳 None
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error in TaskModel.get_by_id: {e}")
            return None

    def update(self, id, title=None, completed=None):
        """
        更新任務標題或是完成狀態
        
        Args:
            id (int): 任務 ID
            title (str, optional): 新的標題
            completed (bool, optional): 新的完成狀態
            
        Returns:
            bool: 是否更新成功
        """
        try:
            conn = self.get_db_connection()
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
                
            params.append(id)
            query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
            
            cursor.execute(query, params)
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error in TaskModel.update: {e}")
            return False

    def delete(self, id):
        """
        刪除指定 ID 的任務
        
        Args:
            id (int): 任務 ID
            
        Returns:
            bool: 是否刪除成功
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error in TaskModel.delete: {e}")
            return False
