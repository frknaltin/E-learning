# forms.py

from flask_wtf import FlaskForm
from wtforms import SubmitField

class JoinCourseForm(FlaskForm):
    join_course = SubmitField('Join Now')
