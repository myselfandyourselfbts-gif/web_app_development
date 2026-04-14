from .tasks import tasks_bp

def init_app(app):
    """將此目錄下的所有 Blueprint 註冊到 Flask App"""
    app.register_blueprint(tasks_bp)
