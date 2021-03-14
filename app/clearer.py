from app import db
from app.models import *
import os

for metr in Metric.query.all():
    db.session.delete(metr)
db.session.commit()
