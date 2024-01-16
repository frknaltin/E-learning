from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin

if not 'Teacher' in locals():
    class Teacher(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        field = db.Column(db.String(100), nullable=False)
        photo_url = db.Column(db.String(250))

        def __repr__(self):
            return f'<Teacher {self.name}>'
        
if not 'Student' in locals():
    class Student(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        profession = db.Column(db.String(100), nullable=False)
        comment = db.Column(db.String(512), nullable=False)
        photo_url = db.Column(db.String(250))

        def __repr__(self):
            return f'<Student {self.name}>'
        
if not 'Course' in locals():
    class Course(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        category = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text, nullable=False)
        teacher = db.Column(db.String(100), nullable=False)
        cover_url = db.Column(db.String(250))
        students = db.Column(db.Integer, nullable=False)
        length = db.Column(db.Integer, nullable=False)
        price = db.Column(db.Float, nullable=False)
        comments = db.Column(db.Integer, nullable=False)
        points = db.Column(db.Integer, nullable=False)
        users = db.relationship('User', secondary='user_courses', back_populates='courses')

        def __repr__(self):
            return f'<Course {self.name}>'

if not 'User' in locals():
    class User(UserMixin, db.Model):
        table_args = {'extend_existing': True}
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(256))
        is_admin = db.Column(db.Boolean, default=False)

        courses = db.relationship('Course', secondary='user_courses', back_populates='users')

        def __repr__(self):
            return '<User {}>'.format(self.username)

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

user_courses = db.Table('user_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)
        
if not 'Newsletter' in locals():
    class Newsletter(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), nullable=False)

        def __repr__(self):
            return f'<Newsletter {self.email}>'
        
if not 'Contact' in locals():
    class Contact(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False)
        subject = db.Column(db.String(100), nullable=False)
        message = db.Column(db.Text, nullable=False)

        def __repr__(self):
            return f'<Contact {self.name}>'
# forms.py