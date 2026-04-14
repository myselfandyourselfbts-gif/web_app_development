from flask import Flask
from app.routes import init_app as init_routes
import os
import sqlite3

def init_db(app):
    """初始化 SQLite 資料庫，執行 database/schema.sql 內的語法"""
    with app.app_context():
        db_path = os.path.join(app.instance_path, 'database.db')
        # 確保 instance 資料夾存在
        os.makedirs(app.instance_path, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        # 讀取並執行建表語法
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_default_key')
    
    # 註冊所有的 Blueprints 路由
    init_routes(app)
    
    # 初始化資料庫表格 (僅在未建立時自動建立)
    init_db(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
