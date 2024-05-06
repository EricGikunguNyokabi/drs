# Middleware for Authentication: Create middleware to check for authentication on routes that require authentication. If a user attempts to access a restricted route without being authenticated, redirect them to the login page.
from flask import session, redirect
from functools import wraps
from pymysql import connect


# user validation
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        id_number = session.get("id_number")
        if "id_number" not in session:
            return redirect("/login")
        else:
            conn = connect(host="localhost", user="root", password="", database="doc_re_s")
            cur = conn.cursor()
            cur.execute("SELECT user_role FROM drs_users WHERE id_number = %s", (id_number,))
            user_role = cur.fetchone()
            if user_role[0] != 'user':  # Compare the value in the tuple
                try:
                    if user_role[0] == 'admin':
                        return func(*args, **kwargs)
                except: 
                    return redirect("/login")
            return func(*args, **kwargs)
    return decorated_function

# officer validation
def co_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        id_number = session.get("id_number")
        if "id_number" not in session:
            return redirect("/c_o_login")
        else:
            conn = connect(host="localhost", user="root", password="", database="doc_re_s")
            cur = conn.cursor()
            cur.execute("SELECT user_role FROM drs_collection_officers WHERE id_number = %s", (id_number,))
            user_role = cur.fetchone()
            if user_role[0] != 'Constituency Collection Officer':  # Compare the value in the tuple
                return redirect("/c_o_login")
            return func(*args, **kwargs)
    return decorated_function


# admin validation
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        id_number = session.get("id_number")
        if "id_number" not in session:
            return redirect("/admin_login")
        else:
            conn = connect(host="localhost", user="root", password="", database="doc_re_s")
            cur = conn.cursor()
            cur.execute("SELECT user_role FROM drs_users WHERE id_number = %s", (id_number,))
            user_role = cur.fetchone()
            if user_role[0] != 'admin':  # Compare the value in the tuple
                return redirect("/admin_login")
            return func(*args, **kwargs)
    return decorated_function






# from flask import Flask, render_template, request, session, redirect, flash, Blueprint
# from pymysql import connect, IntegrityError, MySQLError
# from flask_mysqldb import MySQL
# import os
# from werkzeug.utils import secure_filename
# from flask_bcrypt import Bcrypt, check_password_hash #pip install Flask-MySQLdb flask-bcrypt   (This command will download and install the bcrypt library and its dependencies from the Python Package Index (PyPI) repository.) #Hash passwords before storing them
# from waitress import serve
# from admin_app import admin_app #Blueprint 
# from co_app import co_app #Blueprint 
# from drs_main import login_required