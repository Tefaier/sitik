# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, flash, send_file
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
import pandas as pd
from datetime import datetime
from io import BytesIO

def num_of_metrics(group):
    metrs = group.students[0].metrics
    num = 0
    for metr in metrs:
        if metr.time>=datetime.now().replace(minute=0, hour=0):
            num = num + 1
    return num


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/index1', methods=['GET', 'POST'])
@login_required
def index1():  # school
    return render_template('school.html', school=current_user)


@app.route('/report/<int:id>', methods=['GET'])
@login_required
def report(id):  # report
    sql = db.session.query(Metric, Student).filter(Student.group_id == id).join(Student).statement
    # sql = db.session.query(Metric, Student).filter(Metric.student.group.id==id, Student.group_id==id).join(Student).statement
    data = pd.read_sql(sql, db.engine)
    df_1 = pd.DataFrame([], columns=['Имя', 'Первое измерение', 'Второе измерение', 'Третье измерение'])
    date = datetime.now()
    date1 = date.replace(minute=0, hour=13)
    date2 = date.replace(minute=0, hour=15)
    for id, df in data.groupby("student_id"):
        v1 = df.loc[df.time < date1, "value"]
        v2 = df.loc[(df.time >= date1) & (df.time < date2), "value"]
        v3 = df.loc[df.time >= date2, "value"]
        v1 = v1.iloc[0] if not v1.empty else None
        v2 = v2.iloc[0] if not v2.empty else None
        v3 = v3.iloc[0] if not v3.empty else None
        df_1.loc[len(df_1)] = ([df.name.values[0], v1, v2, v3])
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df_1.to_excel(writer, index=False)
    writer.save()
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True,
                     attachment_filename='report.xlsx')

"""
@app.route('/index2/<int:id>', methods=['GET', 'POST'])
@login_required
def index2(id):  # class
    group1 = Group.query.get(id)
    if request.method == 'POST':
        if request.form['subm'] == 'Дополнить данные':
            for student in group1.students:
                a = request.form.get(str(student.id + 0.1))
                if a == '':
                    a = 0
                met = Metric(value=float(a), student=student)
                db.session.add(met)
            db.session.commit()

    date = datetime.now()
    date1 = date.replace(minute=0, hour=13)
    date2 = date.replace(minute=0, hour=15)
    if date <= date1:
        num = 1
    elif date >= date2:
        num = 3
    else:
        num = 2
    return render_template('class.html', groupq=group1, time=num)
"""

@app.route('/index2/<int:id>', methods=['GET', 'POST'])
@login_required
def index2(id):  # class
    group1 = Group.query.get(id)
    if request.method == 'POST':
        if request.form['subm'] == 'Дополнить данные':
            num = num_of_metrics(group1)
            if num<3:
                for student in group1.students:
                    a = request.form.get(str(student.id + 0.1))
                    if a == '':
                        a = 0
                    met = Metric(value=float(a), student=student)
                    if num==0:
                        met.time = datetime.now().replace(minute=0, hour=11)
                    elif num==1:
                        met.time = datetime.now().replace(minute=0, hour=14)
                    elif num==2:
                        met.time = datetime.now().replace(minute=0, hour=16)
                    db.session.add(met)
                db.session.commit()
            else:
                flash("Все отчеты за сегодня заполнены")

    num = num_of_metrics(group1) + 1
    return render_template('class.html', groupq=group1, time=num)





@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():  # enter
    if current_user.is_authenticated:
        return redirect(url_for('index1'))
    form = LoginForm()
    if request.method == 'POST':
        if request.form['subm'] == 'Войти':
            # checking if it is a class
            school = School.query.filter_by(name=form.username.data).first()
            if school is None or not school.password == form.password.data:
                flash('Invalid username or password')
                return redirect(url_for('index'))
            login_user(school)
            return redirect(url_for('index1'))
    return render_template('loging.html', form=form)
