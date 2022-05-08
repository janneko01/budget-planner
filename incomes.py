import imp
from db import db
import json

def get_incomes(userid):
    sql = """SELECT source, income, eventdate FROM income WHERE userid =:userid AND date_trunc('month', eventdate) = date_trunc('month', CURRENT_DATE) ORDER BY eventdate DESC"""
    return db.session.execute(sql, {"userid":userid}).fetchall()