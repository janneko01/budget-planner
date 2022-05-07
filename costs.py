from db import db
from datetime import datetime
from datetime import timedelta
import json

def get_costs_with_categories(user_id):
    sql = """SELECT * FROM costs ORDER BY eventdate"""
    return db.session.execute(sql, {"user_id":user_id}).fetchone()

def get_costs(user_id):
    sql = """SELECT eventdate, sum(price) FROM costs GROUP BY eventdate"""
    return db.session.execute(sql, {"user_id":user_id}).fetchone()

def get_costs_by_month(user_id):
    sql = """SELECT eventdate, sum(price) FROM costs WHERE date_trunc('month', eventdate) = date_trunc('month', CURRENT_DATE) GROUP BY eventdate ORDER BY eventdate"""
    costs = db.session.execute(sql, {"user_id":user_id}).fetchall()
    targetday = datetime.today().date().replace(day = 1)
    nextmonth = (targetday + timedelta(days = 32)).replace(day = 1)

    i = 0
    sum = 0
    result = []

    while targetday < nextmonth:
        if i < len(costs) and costs[i][0] == targetday:
            sum += costs[i][1]
            i += 1
        result.append([targetday.strftime('%d.%m.'), sum])
        targetday += timedelta(days = 1)
    return result