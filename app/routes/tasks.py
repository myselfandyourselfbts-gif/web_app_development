from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import TaskModel

# 建立 Blueprint 實例以便於管理路由
tasks_bp = Blueprint('tasks', __name__)
task_model = TaskModel()

@tasks_bp.route('/')
def index():
    """
    任務列表首頁
    - 取得資料庫中所有任務
    - 渲染 index.html，並傳遞 tasks 給模板
    """
    tasks = task_model.get_all()
    return render_template('index.html', tasks=tasks)

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    建立新任務
    - 接收表單傳來的 'title'
    - 驗證後呼叫 Model 寫入資料庫
    - 重新導向至首頁 index
    """
    title = request.form.get('title', '').strip()
    if not title:
        flash('新增失敗：任務名稱不能包含空白！', 'error')
        return redirect(url_for('tasks.index'))
        
    task_id = task_model.create(title)
    if not task_id:
        flash('新增任務時發生了未知的資料庫錯誤，請稍後再試。', 'error')
        
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換任務完成狀態
    - 根據 task_id 查詢資料
    - 反轉目前的 completed 狀態並更新
    - 重新導向至首頁 index
    """
    task = task_model.get_by_id(task_id)
    if not task:
        flash('找不到該筆任務，可能已被刪除。', 'error')
        return redirect(url_for('tasks.index'))
        
    # SQLite 儲存的時候通常會被回傳為 int 型態的 0 或是 1
    new_status = not bool(task['completed'])
    success = task_model.update(task_id, completed=new_status)
    if not success:
        flash('更新狀態失敗，系統發生了未知的錯誤。', 'error')
        
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET'])
def edit_task(task_id):
    """
    顯示任務編輯頁面
    - 根據 task_id 查詢該筆任務資料
    - 若找不到則處理 404
    - 渲染 edit.html，提供表單修改
    """
    task = task_model.get_by_id(task_id)
    if not task:
        flash('找不到該筆任務。', 'error')
        return redirect(url_for('tasks.index'))
        
    return render_template('edit.html', task=task)

@tasks_bp.route('/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """
    接收編輯並且更新任務資料
    - 接收表單傳來的更新內容 ('title')
    - 呼叫 Model 進行更新
    - 重新導向至首頁 index
    """
    title = request.form.get('title', '').strip()
    if not title:
        flash('編輯失敗：任務名稱不能為空白字元！', 'error')
        # 依據 Skill 規定，表單驗證失敗時要回到表單頁並顯示錯誤
        return redirect(url_for('tasks.edit_task', task_id=task_id))
        
    success = task_model.update(task_id, title=title)
    if not success:
        flash('更新任務時發生錯誤。', 'error')
        
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    刪除指定任務
    - 根據 task_id 刪除資料庫中的特定任務
    - 刪除完畢後重新導向至首頁 index
    """
    success = task_model.delete(task_id)
    if not success:
        flash('刪除任務發生錯誤，請稍後再重試。', 'error')
        
    return redirect(url_for('tasks.index'))
