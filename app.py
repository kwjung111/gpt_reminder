from flask_migrate import Migrate
from flask import Flask, render_template, redirect, url_for, flash, request
from forms import RegisterForm, LoginForm, TodoForm, UpdateUserForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db  # 수정된 부분
import secrets
from flask import jsonify
from flask_wtf.csrf import CSRFProtect, generate_csrf


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gpt_user:2024!@3456&*haha@localhost:3309/gpt_reminder'
db.init_app(app)
migrate = Migrate(app, db)

csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 여기에서 models를 임포트합니다.
from models import User, Todo


# 데이터베이스 생성
with app.app_context():
    db.create_all()

@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)

@app.route('/service_worker.js')
def service_worker():
    return app.send_static_file('service_worker.js')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            password=hashed_password,
            age=form.age.data,
            gender=form.gender.data,
            job=form.job.data,
            company=form.company.data,
            work_hours=form.work_hours.data,
            lunch_time=form.lunch_time.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('회원가입이 완료되었습니다!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('로그인 정보가 올바르지 않습니다.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃되었습니다.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.deadline.desc()).all()
    return render_template('dashboard.html', todos=todos)

@app.route('/add_todo', methods=['GET', 'POST'])
@login_required
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        new_todo = Todo(
            title=form.title.data,
            content=form.content.data,
            deadline=form.deadline.data,
            owner=current_user
        )
        db.session.add(new_todo)
        db.session.commit()
        flash('새로운 To-Do가 추가되었습니다!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('todo.html', form=form, action='저장')

# 마이페이지 라우트
@app.route('/my_page', methods=['GET', 'POST'])
@login_required
def my_page():
    form = UpdateUserForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.age = form.age.data
        current_user.gender = form.gender.data
        current_user.job = form.job.data
        current_user.company = form.company.data
        current_user.work_hours = form.work_hours.data
        current_user.lunch_time = form.lunch_time.data
        # 비밀번호 변경 로직 추가 (선택 사항)
        # if form.password.data:
        #     current_user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('유저 정보가 업데이트되었습니다!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('my_page.html', form=form)

from datetime import datetime

@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d %H:%M'):
    if isinstance(value, str):
        # 문자열을 datetime 객체로 변환
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return value.strftime(format)
        except ValueError:
            return value
    else:
        return value
    
# To-Do 수정 라우트
@app.route('/edit_todo/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.owner != current_user:
        flash('수정 권한이 없습니다.', 'danger')
        return redirect(url_for('dashboard'))
    form = TodoForm(obj=todo)
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.content = form.content.data
        todo.deadline = form.deadline.data
        db.session.commit()
        flash('To-Do가 수정되었습니다!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('todo.html', form=form, action='수정')

# To-Do 완료 토글 라우트 (AJAX)
@app.route('/toggle_todo/<int:todo_id>', methods=['POST'])
@login_required
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.owner != current_user:
        return jsonify({'success': False}), 403
    todo.is_completed = not todo.is_completed
    db.session.commit()
    return jsonify({'success': True})

# To-Do 삭제 라우트 (AJAX)
@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.owner != current_user:
        return jsonify({'success': False}), 403
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
