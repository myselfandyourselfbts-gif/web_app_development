from flask import Blueprint, render_template, request, redirect, url_for

# 建立 Blueprint 實例以便於管理路由
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """
    任務列表首頁
    - 取得資料庫中所有任務
    - 渲染 index.html，並傳遞 tasks 給模板
    """
    pass

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    建立新任務
    - 接收表單傳來的 'title'
    - 驗證後呼叫 Model 寫入資料庫
    - 重新導向至首頁 index
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換任務完成狀態
    - 根據 task_id 查詢資料
    - 反轉目前的 completed 狀態並更新
    - 重新導向至首頁 index
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET'])
def edit_task(task_id):
    """
    顯示任務編輯頁面
    - 根據 task_id 查詢該筆任務資料
    - 若找不到則處理 404
    - 渲染 edit.html，提供表單修改
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """
    接收編輯並且更新任務資料
    - 接收表單傳來的更新內容 ('title')
    - 呼叫 Model 進行更新
    - 重新導向至首頁 index
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    刪除指定任務
    - 根據 task_id 刪除資料庫中的特定任務
    - 刪除完畢後重新導向至首頁 index
    """
    pass
