from db import db
from datetime import datetime
from datetime import timedelta
import json

def get_costs_with_categories(userid):
    sql = """SELECT * FROM costs WHERE userid=:userid ORDER BY eventdate"""
    return db.session.execute(sql, {"userid":userid}).fetchall()

def get_costs(userid):
    sql = """SELECT eventdate, sum(price) FROM costs WHERE userid=:userid GROUP BY eventdate"""
    return db.session.execute(sql, {"userid":userid}).fetchall()

def get_costs_by_month(userid):
    sql = """SELECT eventdate, sum(price) FROM costs WHERE userid=:userid AND date_trunc('month', eventdate) = date_trunc('month', CURRENT_DATE) GROUP BY eventdate ORDER BY eventdate"""
    costs = db.session.execute(sql, {"userid":userid}).fetchall()
    targetday = datetime.today().date().replace(day = 1)
    nextmonth = (targetday + timedelta(days = 32)).replace(day = 1)

    sql = "SELECT targetbudget FROM usersettings WHERE userid=:userid"
    budget = db.session.execute(sql, {"userid":userid}).fetchone()
    budget = budget[0] / 30 if budget else None

    i = 0
    sum = 0
    result = []
    budgetSum = budget

    while targetday < nextmonth:
        if i < len(costs) and costs[i][0] == targetday:
            sum += costs[i][1]
            i += 1
        if budget:
            result.append([targetday.strftime('%d.%m.'), sum, budgetSum])
            budgetSum += budget
        else:
            result.append([targetday.strftime('%d.%m.'), sum])
        targetday += timedelta(days = 1)
    return result

def get_this_month_costs(userid):
    sql = """SELECT category, product, price, eventdate FROM costs WHERE userid =:userid AND date_trunc('month', eventdate) = date_trunc('month', CURRENT_DATE) ORDER BY eventdate DESC"""
    return db.session.execute(sql, {"userid":userid}).fetchall()
