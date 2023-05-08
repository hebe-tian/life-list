from listProject import app
from flask import render_template


# 404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


# 400页面
@app.errorhandler(400)
def page_not_found(e):
    return render_template('errors/400.html'), 400


# 500页面
@app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'), 500
