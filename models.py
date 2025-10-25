from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2), nullable=False)

    gross_monthly_salary = db.Column(db.Float, nullable=False)
    est_state_tax_rate = db.Column(db.Float, nullable=False)
    est_state_tax_monthly = db.Column(db.Float, nullable=False)
    est_take_home = db.Column(db.Float, nullable=False)

    needs = db.Column(db.Float, nullable=False)
    wants = db.Column(db.Float, nullable=False)
    future = db.Column(db.Float, nullable=False)
    max_rent_util = db.Column(db.Float, nullable=False)

    emergency_goal_total = db.Column(db.Float, nullable=False)
    emergency_monthly = db.Column(db.Float, nullable=False)
    emergency_months_to_goal = db.Column(db.Float, nullable=True)
    debt_snowball = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
