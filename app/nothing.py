from app import db
from app.models import *

school = School(name="Петров Петрович", password="super_password")
db.session.add(school)
group = Group(name="10А", school=school)
db.session.add(group)
student = Student(name="человек_Y", group=group)
db.session.add(student)
num_1 = Metric(value=36.7, student=student)
num_2 = Metric(value=36.9, student=student)
num_3 = Metric(value=36.4, student=student)
db.session.add(num_1)
db.session.add(num_2)
db.session.add(num_3)
db.session.commit()


# df.loc[df.time>=date1 & df.time<=date2, "value"]