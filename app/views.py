from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app import app, db
from app.models import Course, Teacher, Student

@app.route("/index.html")
@app.route("/")
def index():
    courses = Course.query.all()
    teachers = Teacher.query.all()
    students = Student.query.all()
    return render_template("index.html", courses=courses, teachers=teachers, students=students)

@app.route('/about.html')
def about():
    teachers = Teacher.query.all()
    return render_template('about.html', teachers=teachers)

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route("/courses.html")
def courses():
    students = Student.query.all()
    courses = Course.query.all()
    return render_template("courses.html", courses=courses, students=students)

@app.route("/team.html")
def team():
    teachers = Teacher.query.all()
    return render_template("team.html", teachers=teachers)

@app.route("/testimonial.html")
def testimonial():
    students = Student.query.all()
    return render_template("testimonial.html", students=students)

@app.route("/404.html")
def notfound():
    return render_template("404.html")

@app.route("/privacy.html")
def privacy():
    return render_template("privacy.html")

@app.route("/terms.html")
def terms():
    return render_template("terms.html")

@app.route("/faqs.html")
def faqs():
    return render_template("faqs.html")

@app.route('/course/<category>')
def course(category):
    courses = Course.query.all()
    return render_template('course.html', category=category, courses=courses)

@app.route('/my_courses')
@login_required
def my_courses():
    return render_template('my_courses.html', courses=current_user.courses)

@app.route('/join_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def join_course(course_id):
    course = Course.query.get(course_id)
    if course and course not in current_user.courses:
        current_user.courses.append(course)
        db.session.commit()
        flash('You have successfully joined the course!', 'success')
    else:
        flash('You are already enrolled in this course!', 'info')
    
        # Get the referrer (previous URL) from the request object
    previous_page = request.referrer
    
    # If the referrer is None or the join_course route itself, redirect to a default page
    if previous_page is None or previous_page.endswith(url_for('join_course', course_id=course.id)):
        return redirect(url_for('index'))
    
    return redirect(previous_page)

@app.route('/leave_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def leave_course(course_id):
    course = Course.query.get(course_id)

    if course and course in current_user.courses:
        current_user.courses.remove(course)
        db.session.commit()
        flash('You have successfully left the course.', 'success')
    else:
        flash('You are not enrolled in this course.', 'info')

    return redirect(url_for('my_courses'))

@app.route('/course_detail/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get(course_id)
    if course:
        return render_template('course_detail.html', course=course)
    else:
        flash('Course not found!', 'danger')
        return redirect(url_for('my_courses'))
