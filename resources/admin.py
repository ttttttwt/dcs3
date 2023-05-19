import os
import functools
import datetime

from flask import request, render_template, redirect, url_for, session
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_


from db import db
from models import ActiveModel
from models import LocationModel
from models import AdminModel
from models import UserModel


blp = Blueprint("Admin", "admin", description="Admin operations")


def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("id") is None:
            return redirect(url_for("Admin.login"))

        return route(*args, **kwargs)

    return route_wrapper


@blp.route("/admin/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        admin = AdminModel.query.filter_by(
            username=username, password=password).first()
        if admin:
            session["username"] = username
            session["id"] = admin.id
            return redirect(url_for("Admin.home"))

    return render_template("login.html")


@blp.route("/admin/home", methods=["POST", "GET"])
@login_required
def home():
    name = session["username"]
    users = UserModel.query.all()
    num_users = len(users)

    return render_template("user.html", users=users, num_users=num_users)


@blp.route("/admin/logout")
@login_required
def logout():
    session.clear()

    return redirect(url_for("Admin.login"))


@blp.route("/admin/user/delete/<int:id>")
@login_required
def delete_user(id):
    user = UserModel.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("Admin.home"))


@blp.route("/admin/user/update/<int:id>", methods=["POST", "GET"])
@login_required
def update_user(id):
    if request.method == "GET":

        return render_template("update_user.html", id=id)
    else:
        username = request.form["username"]
        email = request.form["email"]

        has_user = UserModel.query.filter(
            or_(
                UserModel.username == username,
                UserModel.email == email
            )
        ).first()

        if has_user:
            return render_template("update_user.html", id=id, error="Username or Email already exists")
        else:

            user = UserModel.query.filter_by(id=id).first()
            user.username = username or user.username
            user.email = email or user.email

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("Admin.home"))


@blp.route("/admin/user/create", methods=["POST", "GET"])
def create_user():
    if request.method == "GET":
        return render_template("create_user.html")
    else:
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        has_user = UserModel.query.filter(
            or_(
                UserModel.username == username,
                UserModel.email == email
            )
        ).first()

        if has_user:
            return render_template("create_user.html", error="Username or Email already exists")
        else:
            user = UserModel(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("Admin.home"))


@blp.route("/admin/user/statiscal/<int:id>", methods=["POST", "GET"])
@login_required
def statiscal(id):

    distance = []
    result = {"day_0": 0, "day_1": 0, "day_2": 0,
              "day_3": 0, "day_4": 0, "day_5": 0, "day_6": 0}
    current_date = datetime.datetime.now()
    start_of_week = current_date - \
        datetime.timedelta(days=current_date.weekday())

    for i in range(7):
        target_date = start_of_week + datetime.timedelta(days=i)
        actives = ActiveModel.query.filter_by(
            user_id=id, date=target_date.strftime('%Y-%m-%d')).all()

        if actives:
            for active in actives:
                if active.distance:
                    result[f"day_{i}"] += active.distance
                    
                    
    for key, value in result.items():
        distance.append(value)
        
    return render_template("statiscal_user.html", distance=distance)

@blp.route("/admin/statiscal")
@login_required
def admin_statiscal():
    distance = []
    result = {"day_0": 0, "day_1": 0, "day_2": 0,
              "day_3": 0, "day_4": 0, "day_5": 0, "day_6": 0}
    current_date = datetime.datetime.now()
    start_of_week = current_date - \
        datetime.timedelta(days=current_date.weekday())

    for i in range(7):
        target_date = start_of_week + datetime.timedelta(days=i)
        actives = ActiveModel.query.filter_by(date=target_date.strftime('%Y-%m-%d')).all()

        if actives:
            for active in actives:
                if active.distance:
                    result[f"day_{i}"] += active.distance
                    
                    
    for key, value in result.items():
        distance.append(value)
        # print(value)
        
    return render_template("statiscal_user.html", distance=distance)
