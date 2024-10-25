from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, Optional
from wtforms.widgets import DateTimeLocalInput


class RegisterForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('비밀번호', validators=[DataRequired(), Length(min=6, max=150)])
    confirm_password = PasswordField('비밀번호 확인', validators=[DataRequired(), EqualTo('password')])
    # 선택 사항 필드
    name = StringField('이름')
    age = StringField('나이')
    gender = StringField('성별')
    job = StringField('직업')
    company = StringField('회사명')
    work_hours = StringField('출퇴근 시간')
    lunch_time = StringField('점심시간')
    submit = SubmitField('회원가입')

class LoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('로그인')

class TodoForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])
    deadline = DateTimeField(
        '기한',
        format='%Y-%m-%dT%H:%M',
        validators=[Optional()],
        widget=DateTimeLocalInput()
    )
    submit = SubmitField('추가')
    
class AiMemoForm(FlaskForm):
    content = TextAreaField('자유롭게 내용을 추가하세요', validators=[DataRequired()])
    submit = SubmitField('추가')
    
class UpdateUserForm(FlaskForm):
    name = StringField('이름', validators=[Optional()])
    age = IntegerField('나이', validators=[Optional()])
    gender = SelectField('성별', choices=[('남성', '남성'), ('여성', '여성'), ('기타', '기타')], validators=[Optional()])
    job = StringField('직업', validators=[Optional(), Length(max=100)])
    company = StringField('회사', validators=[Optional(), Length(max=100)])
    work_hours = StringField('근무 시간', validators=[Optional(), Length(max=50)])
    lunch_time = StringField('점심 시간', validators=[Optional(), Length(max=50)])
    submit = SubmitField('업데이트')

