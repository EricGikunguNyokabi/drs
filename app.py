from flask import Flask, render_template, request, session, redirect, flash, url_for
import pymysql
import os
import random #for OTP
import sms  # From module named sms with a send_sms function
from pymysql import connect, IntegrityError
from flask_mysqldb import MySQL
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt, check_password_hash #pip install Flask-MySQLdb flask-bcrypt   (This command will download and install the bcrypt library and its dependencies from the Python Package Index (PyPI) repository.) #Hash passwords before storing them
# from admin_app import admin_app #Blueprint 
# from co_app import co_app #Blueprint 
from drs_main import login_required, co_required, admin_required


app = Flask(__name__)
app.secret_key =  "Yg7b}6G9g[`MTwj#sbNM[$N&6N7^r$HXF:9l%=z%#zP'h_Vcj|{FA,ilM'$3]o2" # Setup a secret key for the session
# app.register_blueprint(admin_app) # connecting the blueprints
# app.register_blueprint(co_app)
# MySQL configurations
app.config["MySQL_HOST"] ="localhost" 
app.config["MySQL_USER"] ="root"
app.config["MySQL_PASSWORD"] ="" 
app.config["MySQL_DB"] ="doc_re_s"
# # FOR PYTHONANYWHERE 
# app.config["MySQL_HOST"] ="egn.mysql.pythonanywhere-services.com" 
# app.config["MySQL_USER"] ="egn"
# app.config["MySQL_PASSWORD"] ="12345678@#" 
# app.config["MySQL_DB"] ="egn$default"

mysql = MySQL(app) # Initialize MySQL
bcrypt = Bcrypt(app) # Initialize Bcrypt for password hashing


APP_ROOT = os.path.dirname(os.path.abspath(__file__))# Define the route path of the folder structure.This will determine where our file app.py is located
UPLOAD_FOLDER = os.path.join(APP_ROOT, "static//images") # Specify the upload folder.This is the folder we want our images uploaded to.
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER # Configure the two above.

# ============ INDEX.HTML =================================================================================
# 1.This is the home_page that anyone who visits the page gets this render template 
@app.route("/")
def index():
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    sql_images = "SELECT * FROM drs_general_images WHERE image_name = 'image' LIMIT 5"
    cur.execute(sql_images)
    carausel_image = cur.fetchall()
    return render_template("index.html", images=carausel_image, num_images=len(carausel_image))
    

# ============ DRS ABOUT =================================================================================
@app.route("/about")
def about():
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
    cur = conn.cursor()
    sql = "SELECT * FROM drs_general_images WHERE image_name = 'about' "
    cur.execute(sql)
    about_image = cur.fetchall()
    return render_template("users/about.html", about=about_image)


# ============ USER PROFILE REGISTRATION ======================================================================
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            id_number = request.form["id_number"]
            mobile_no = request.form["mobile_no"]
            email_address = request.form["email_address"]
            user_role = request.form["user_role"]
            password = request.form["password"]
            password_confirm = request.form["password_confirm"]
            
            if password != password_confirm: # password validation
                message = "Password do Not Match !"
                return render_template("users/register.html", message=message)
            
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8") #hashing the password
            
            conn = connect(host="localhost", user="root", password="", database="doc_re_s")
            # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
            cur = conn.cursor()
            sql = "INSERT INTO drs_users (first_name, last_name, id_number, mobile_no, email_address, user_role, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (first_name, last_name, id_number, mobile_no, email_address, user_role, hashed_password))
            conn.commit()
            
            return render_template("users/successfulreg.html")
        
        except IntegrityError as e: # Check if the error is due to duplicate primary key (ID number)
            if e.args[0] == 1062:  # MySQL error code for duplicate entry
                error_msg = "User with similar ID Number already exists"
                return render_template("users/register.html", message=error_msg)
            else: # Handle other IntegrityError cases if necessary
                error_msg = f"IntegrityError: {e}"
                app.logger.error(error_msg)
                return render_template("users/register.html", message=error_msg)
        
        except Exception as e: # Handle other exceptions
            error_msg = f"Error occurred during registration: {e}"
            app.logger.error(error_msg)
            return render_template("users/register.html", message=error_msg)

    else:
        return render_template("users/register.html")




# ============ USER LOGIN =================================================================================
@app.route("/login", methods=["POST", "GET"])
def login():
    print(session)
    if request.method == "POST":
        id_number = request.form["id_number"]
        password = request.form["password"]

        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
        # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
        cur = conn.cursor()

        # Check if the user exists in the database
        try:
            sql = "SELECT * FROM drs_users WHERE id_number = %s"
            cur.execute(sql, (id_number,))
            user_data = cur.fetchone()

            if user_data:
                # Check if the provided password matches the hashed password from the database
                if bcrypt.check_password_hash(user_data[7], password):
                    session["first_name"] = user_data[1]
                    session["last_name"] = user_data[2]
                    session["id_number"] = user_data[3]
                    session["mobile_no"] = user_data[4]
                    session["email_address"] = user_data[5]
                    session["logged_in"] = True
                    return redirect("/user_profile")
                else:
                    msg = "Invalid username and password combination"
                    return render_template('users/login.html', message=msg)
            else:
                msg = "Invalid username and password combination"
                return render_template('users/login.html', message=msg)
        except Exception as e:
            # Handle database errors
            print("Error:", e)
            msg = "An error occurred while processing your request. Please try again later."
            return render_template('users/login.html', message=msg)
        finally:
            # Close the database connection
            cur.close()
            conn.close()

    return render_template('users/login.html')

        
        



# ============ USER PROFILE PAGE =================================================================================
@app.route("/user_profile", methods=["POST", "GET"])
@login_required
def user_profile():
    print(session)
    # Fetch user data from the session
    first_name = session.get("first_name")
    last_name = session.get("last_name")
    id_number = session.get("id_number")

    # fullname update form handling
    if request.method == "POST":
        full_name = request.form["full_name"]
        
        # Connect to MySQL
        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
        # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
        cur = conn.cursor()

        # Check if full_name exists in the database // tripple quotes for multiple lines in python
        sql_check = """SELECT full_name FROM drs_users_fullnames 
                       WHERE first_name = %s AND last_name = %s"""
        cur.execute(sql_check, (first_name, last_name))
        db_full_name = cur.fetchone()

        if db_full_name is None:
            # Add the full_name if it doesn't exist in the database
            sql_insert = """INSERT INTO drs_users_fullnames(first_name, last_name, id_number, full_name) 
                            VALUES (%s, %s, %s, %s)"""
            cur.execute(sql_insert, (first_name, last_name, id_number, full_name))
            conn.commit()
        else:
            # Update the full_name if it exists in the database and is different
            if full_name != db_full_name[0]:
                sql_update = """UPDATE drs_users_fullnames 
                                SET full_name = %s 
                                WHERE first_name = %s AND last_name = %s"""
                cur.execute(sql_update, (full_name, first_name, last_name))
                conn.commit()
        # Close MySQL connection
        cur.close()
        conn.close()
        return redirect("/user_profile")

    # Fetch fullnames if updated
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    sql = """SELECT lf.full_name
             FROM drs_users_fullnames lf
             WHERE lf.first_name = %s AND lf.last_name = %s"""
    cur.execute(sql, (first_name, last_name))
    full_names = cur.fetchall()

    # Fetch lost and found documents for the user
    sql = """SELECT *
             FROM drs_lost_and_found lf
             WHERE lf.first_name = %s AND lf.last_name = %s"""
    cur.execute(sql, (first_name, last_name))
    lost_and_found_data = cur.fetchall()

    # Fetch profile image path for the user
    profile_image_path = None
    sql_profile = "SELECT profile_image_path FROM drs_users_profile WHERE id_number = %s"
    cur.execute(sql_profile, (id_number,))
    profile_image_data = cur.fetchone()

    if profile_image_data:
        profile_image_path = profile_image_data[0]

    # Close MySQL connection
    cur.close()
    conn.close()

    return render_template("users/user_profile.html", full_names=full_names, lost_and_found_data=lost_and_found_data, profile_image_path=profile_image_path)


# ============ USER PROFILE IMAGE =================================================================================
@app.route("/edit_profile_photo", methods=["POST", "GET"])
@login_required
def edit_profile_photo():
    print("Session data:", session)
    if request.method == "POST":
        profile_image_path = request.files["profile_image_path"]
        id_number = session.get("id_number")

        image_filename = secure_filename(profile_image_path.filename)

        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
        # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
        cur = conn.cursor()

        # Check if user already has a profile image
        cur.execute("SELECT profile_image_path FROM drs_users_profile WHERE id_number = %s", (id_number,))
        existing_image = cur.fetchone()

        # If user has an existing profile image, delete it
        if existing_image:
            existing_image_path = os.path.join(app.config["UPLOAD_FOLDER"], existing_image[0].split("/")[-1])
            if os.path.isfile(existing_image_path):  # Check if it's a file
                os.remove(existing_image_path)
            elif os.path.isdir(existing_image_path):  # Check if it's a directory
                # Handle directory deletion if necessary
                pass

            sql = "UPDATE drs_users_profile SET profile_image_path = %s WHERE id_number = %s"
            cur.execute(sql, ("/../../static/images/" + image_filename, id_number))
        else:
            sql = "INSERT INTO drs_users_profile(id_number, profile_image_path) VALUES (%s, %s)"
            cur.execute(sql, (id_number, "/../../static/images/" + image_filename))

        conn.commit()

        profile_image_path.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))
        msg = "Profile Image Upload Successful"
        flash("Profile Image Upload Successful")
        return redirect(url_for("user_profile", message=msg, profile_image_path=profile_image_path, id_number=id_number))
    else:
        err = "Error Uploading Image"
        return redirect(url_for("user_profile", error=err, profile_image_path=profile_image_path, id_number=id_number))



# ========= REPORT LOST DOCUMENT ====================================================================================
@app.route("/report_lost_document", methods=["POST","GET"])
@login_required
def report_lost_document():
    print(session)
    if request.method == "POST":
        id_number = session.get("id_number")
        first_name = session.get("first_name")
        last_name = session.get("last_name")
        doc_fullname = request.form["doc_fullname"]
        document_type = request.form["document_type"]
        document_id = request.form["document_id"]
        status = request.form["status"]

        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
        # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
        cur = conn.cursor()
        sql = "INSERT INTO drs_users_lost_documents(id_number,first_name,last_name,doc_fullname,document_type,document_id,status)VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,(id_number,first_name,last_name,doc_fullname,document_type,document_id,status))
        conn.commit()
        msg = "Document Reported Successfuly."
        return render_template("users/user/reportlostdocument.html",message=msg)
    conn = connect(host="localhost", user="root", password="",database="doc_re_s")
    # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
    cur = conn.cursor()
    cur.execute("SELECT document_name FROM drs_document_types")
    document_types = cur.fetchall()
    return render_template("users/user/reportlostdocument.html",document_types=document_types)


# ========== USER DOCUMENT STATUS =============================================================================
@app.route("/check_document_status",methods=["POST","GET"])
@login_required
def check_document_status():
    print(session)
    if request.method == "POST":
        document_id = request.form.get("document_id")
        county = request.form.get("county")
        constituency = request.form.get("constituency")
        if document_id and county and constituency:
            conn = connect(host="localhost", user="root", password="", database="doc_re_s")
            # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
            cur = conn.cursor()
            cur.execute("UPDATE drs_lost_and_found SET county = %s, constituency = %s WHERE document_id = %s ",(county,constituency,document_id))
            conn.commit()
            message = "Document requested successfuly. You'll be alerted once the document is Transffered."
            return render_template("users/user/documentstatus.html",message=message)
        else:
            message_error = "Please select a document and specify the county and constituency."
            return render_template("users/user/documentstatus.html", message=message_error)
    
    counties = ["","Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita-Taveta", "Garissa", "Wajir", "Mandera", "Marsabit", "Isiolo", "Meru", "Tharaka-Nithi", "Embu", "Kitui", "Machakos", "Makueni", "Nyandarua", "Nyeri", "Kirinyaga", "Murang'a", "Kiambu", "Turkana", "West Pokot", "Samburu", "Trans-Nzoia", "Uasin Gishu", "Elgeyo-Marakwet", "Nandi", "Baringo", "Laikipia", "Nakuru", "Narok", "Kajiado", "Kericho", "Bomet", "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya", "Kisumu", "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi"]

    # Fetch user data from the session
    first_name = session.get("first_name")
    last_name = session.get("last_name")
    id_number = session.get("id_number")
    # Fetch lost and found documents for the user
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
    cur = conn.cursor()
    sql = """SELECT lf.first_name, lf.second_name, lf.last_name, lf.document_id, lf.document_type, lf.county, lf.constituency
             FROM drs_lost_and_found lf
             WHERE lf.first_name = %s AND lf.last_name = %s"""
    cur.execute(sql, (first_name, last_name))
    lost_and_found_data = cur.fetchall()

    # Fetch reported lost documents
    sql_reported_lost = "SELECT * FROM drs_users_lost_documents WHERE id_number = %s"
    cur.execute(sql_reported_lost, (id_number,))
    reported_lost = cur.fetchall()

    if reported_lost:
        try:
            sql = """
            UPDATE drs_users_lost_documents AS uld
            INNER JOIN drs_lost_and_found AS laf ON uld.document_id = laf.document_id
            SET uld.status = 'found'
            WHERE uld.status = 'lost'
            """
            cur.execute(sql)
            conn.commit()  # Commit changes to the database
            return redirect(url_for("/check_document_status",lost_and_found_data=lost_and_found_data, counties=counties, reported_lost=reported_lost))
        except Exception as e:
            # Handle specific exceptions here
            print("Error:", e)
            return render_template("users/user/documentstatus.html", lost_and_found_data=lost_and_found_data, counties=counties, reported_lost=reported_lost)
    else:
        return render_template("users/user/documentstatus.html", lost_and_found_data=lost_and_found_data, counties=counties, reported_lost=reported_lost)




# ============ USER PROFILE CHARGERS =================================================================================
@app.route("/charges", methods=["GET", "POST"])
@login_required
def charges():
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
    cur = conn.cursor()
    cur.execute("SELECT document_name FROM drs_document_types")
    document_types = cur.fetchall()
    conn.close()
 
    if request.method == "POST":
        # Get the selected document type from the form
        selected_document_type = request.form.get("document_type")

        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default") # Database connection and cursor
        cur = conn.cursor()

        # Fetch charges from the database based on the selected document type
        cur.execute("SELECT document_name, default_charges, replacement_charges FROM drs_document_types WHERE document_name = %s", (selected_document_type,))
        charges_data = cur.fetchone()  # Assuming there's only one row for the selected document type
        conn.close()
        return render_template("users/user/charges.html", charges_data=charges_data,document_types =document_types )

    # If the request method is GET, simply render the template with the document types
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
    cur = conn.cursor()
    cur.execute("SELECT document_name FROM drs_document_types")
    document_types = cur.fetchall()
    conn.close()
    return render_template("users/user/charges.html", document_types=document_types)


# ============ USER PROFILE CONTACT US =============================================================================
@app.route("/contact_us")
@login_required
def contact_us():
    return render_template("users/user/contactus.html")


# ============ USER PROFILE FORGOT PASSWORD =========================================================================
@app.route("/forgot_password")
def forgot_password():
    return render_template("users/forgot_password.html")


# ============ REQUEST OTP =========================================================================================
# Route for storing id_in session
@app.route("/id_number_session", methods=["POST","GET"])
def id_number_session():
    id_number = request.form.get("id_number")
    session["id_number"] = id_number #Store id_number in session
    # Connect to the database
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
    cur = conn.cursor()
    
    sql = "SELECT * FROM drs_users WHERE id_number = %s"
    cur.execute(sql, (id_number,))  # Corrected parameter substitution
    user = cur.fetchone()
    if user:
        return redirect("/verify_otp")
    else:
        msg = "ID Number NOT Registered"
        return render_template("users/forgot_password.html", message=msg)


@app.route("/get_otp",methods=["POST","GET"])
def get_otp():
    otp = str(random.randint(1000, 9999)) # Generate a random 4-digit OTP
    session["otp"] = otp # Store the OTP in the session
    print("OTP Requested: ",otp)
    id_number = session.get("id_number")  # Retrieve id_number from session
    # print("ID in session : ", id_number)
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    cur.execute("SELECT mobile_no FROM drs_users WHERE id_number = %s",(id_number,))
    phone = cur.fetchone()
    print("phone : ", phone)
    if phone:
        phone_number = phone[0]  # Extract phone number from the tuple
        phone_number = "+254" + str(phone_number) # Prepend "+254" to the phone number
        print("OTP Mobile Number Fetched", phone_number)
        otp_message = f" DRS OTP : {otp} , Contact +254701838170,Eric:for more info." #f-string (formatted string literal), allows to directly insert the value of otp 
        print(otp_message)
        sms.send_sms(phone_number, otp_message)
    else:
        pass
    return redirect(url_for("verify_otp"))

# ============ ENTER OTP FOR VERIFICATION ==========================================================================
@app.route("/verify_otp", methods=["POST", "GET"])
def verify_otp():
    id_number = session.get("id_number") #retrieve id_number from session
    otp = session.get("otp") #retrieve otp from session
    if id_number:
        if request.method == "POST":
            user_otp = request.form.get("otp")
            if user_otp == otp: #if OTP is correct, redirect to reset password page
                try:
                    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
                    # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
                    cur = conn.cursor()
                    cur.execute("UPDATE drs_users SET password = '' WHERE id_number = %s", (id_number,))
                    conn.commit()
                    return redirect("/reset_password")
                except Exception as e:
                    msg = "Error: " + str(e)
                    return render_template("users/otp/verify_otp.html", message=msg)
            else:
                msg = "Invalid OTP"
                return render_template("users/otp/verify_otp.html", message=msg)
        else:
            # If it's a GET request, render the OTP verification page
            return render_template("users/otp/verify_otp.html")
    else:
        msg = "Session Not Valid"
        return render_template("users/otp/verify_otp.html", message=msg)
    

@app.route("/reset_password", methods=["POST","GET"])
def reset_password():
    id_number = session.get("id_number")
    if id_number:
        if request.method == "POST":
            # Confirm id_number from form is equal to id in session
            form_id_number = request.form.get("id_number")
            if form_id_number == id_number:
                # Check if password is equal to password confirm
                password = request.form.get("password")
                confirm_password = request.form.get("confirm_password")
                if password == confirm_password:
                    try:
                        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8") #hashing the password
                        # Connect to the database and update the password
                        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
                        # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
                        cur = conn.cursor()
                        cur.execute("UPDATE drs_users SET password = %s WHERE id_number = %s", (hashed_password, id_number))
                        conn.commit()
                        msg = "Password reset successfully"
                        return render_template("users/otp/reset_password.html", messagesuccess=msg)
                    except Exception as e:
                        msg = "Error: " + str(e)
                        return render_template("users/otp/reset_password.html", message=msg)
                else:
                    msg = "Passwords do not match"
                    return render_template("users/otp/reset_password.html", message=msg)
            else:
                msg = "ID Number Not in Session"
                return render_template("users/otp/reset_password.html", message=msg)
        else:
            # If it's a GET request, render the reset password page
            return render_template("users/otp/reset_password.html")
    else:
        msg = "Session Not Valid"
        return render_template("users/otp/reset_password.html", message=msg)
    return render_template("users/otp/reset_password.html")



# ============ PRIVACY POLICY ======================================================================================
@app.route("/privacy_policy")
def privacy_policy():
    return render_template("users/privacy_policy.html")


# ============ TERMS AND CONDITIONS ================================================================================
@app.route("/terms_and_conditions")
def terms_and_conditions():
    return render_template("users/terms_and_conditions.html")

    
# ============ LOGOUT =============================================================================================
@app.route("/logout")
def logout():
    session.clear()
    # redirect takes in route name as opposed to render template that takes file name
    return redirect("/") #redirect home



# ========================================================================================================
# ========================================================================================================
# COLLECTION OFFICER ROUTES ==============================================================================
@app.route("/c_o_registration", methods=["POST", "GET"])
def c_o_registration():
    counties = ["", "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita-Taveta", "Garissa", "Wajir", "Mandera", "Marsabit", "Isiolo", "Meru", "Tharaka-Nithi", "Embu", "Kitui", "Machakos", "Makueni", "Nyandarua", "Nyeri", "Kirinyaga", "Murang'a", "Kiambu", "Turkana", "West Pokot", "Samburu", "Trans-Nzoia", "Uasin Gishu", "Elgeyo-Marakwet", "Nandi", "Baringo", "Laikipia", "Nakuru", "Narok", "Kajiado", "Kericho", "Bomet", "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya", "Kisumu", "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi"]

    if request.method == "POST":
        try:
            # Extract form data
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            id_number = request.form["id_number"]
            mobile_no = request.form["mobile_no"]
            email_address = request.form["email_address"]
            user_role = request.form["user_role"]
            county = request.form["county"]
            constituency = request.form["constituency"]
            password = request.form["password"]
            password_confirm = request.form["password_confirm"]

            # Password validation
            if password != password_confirm:
                msg = "Passwords do not match!"
                return render_template("c_officers/c_o_registration.html", message=msg, counties=counties, form_data=request.form)

            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8") #hashing the password
            conn = connect(host="localhost", user="root", password="", database="doc_re_s")
            # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
            cur = conn.cursor()
            # Insert registration data into the drs_collection_officers table
            sql = "INSERT INTO drs_collection_officers (first_name, last_name, id_number, mobile_no, email_address, user_role, county, constituency, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (first_name, last_name, id_number, mobile_no, email_address, user_role, county, constituency, hashed_password))
            conn.commit()
            # Render success template if data insertion is successful
            return render_template("c_officers/c_o_successfulreg.html", counties=counties)

        except IntegrityError as e: # Check if the error is due to duplicate primary key (ID number)
            if e.args[0] == 1062:  # MySQL error code for duplicate entry
                error_msg = "User with similar ID Number already exists"
                return render_template("c_officers/c_o_registration.html", message=error_msg)
            else: # Handle other IntegrityError cases if necessary
                error_msg = f"IntegrityError: {e}"
                app.logger.error(error_msg)
                return render_template("c_officers/c_o_registration.html", message=error_msg)
        except Exception as e: # Handle other exceptions
            error_msg = f"Error occurred during registration: {e}"
            app.logger.error(error_msg)
            return render_template("c_officers/c_o_registration.html", message=error_msg)
    else:
        return render_template("c_officers/c_o_registration.html", counties=counties)
    



            
        

        




# AFTER SUCCESSFUL REGISTRATION OF COLLECTION OFFICER THEY'RE DIRECTED TO C_0_SUCCESSFULREG.HTML ===========
@app.route("/co_success")
def co_success():
    return render_template("c_officers/c_o_successfulreg.html")


# COLLECTION OFFICER LOGIN ROUTE ===========================================================================
@app.route("/c_o_login", methods=["POST", "GET"])
def c_o_login():
    print(session)
    if request.method == "POST":
        id_number = request.form["id_number"]
        password = request.form["password"]
        
        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
        cur = conn.cursor()
        try:
            sql = "SELECT * FROM drs_collection_officers WHERE id_number=%s"
            cur.execute(sql, (id_number,))
            user_data = cur.fetchone()

            if user_data:
                # Check if the provided password matches the hashed password from the database
                if bcrypt.check_password_hash(user_data[9], password):
                    session["first_name"] = user_data[1]
                    session["last_name"] = user_data[2]
                    session["id_number"] = user_data[3]
                    session["mobile_no"] = user_data[4]
                    session["email_address"] = user_data[5]
                    session["logged_in"] = True
                    return redirect("/c_o_dashboard")
                else:
                    msg = "Invalid username and password combination"
                    return render_template("c_officers/c_o_login.html", message=msg)
            else:
                msg = "Invalid Email Password combination!"
                return render_template("c_officers/c_o_login.html", message=msg)
        except Exception as e:
            # Handle database errors
            print("Error:", e)
            msg = "An error occurred while processing your request. Please try again later."
            return render_template("c_officers/c_o_login.html", message=msg)
        finally:
            cur.close()
            conn.close()
    return render_template("c_officers/c_o_login.html")




# Collection Officer's dashboard ===========================================================================
@app.route("/c_o_dashboard", methods =["GET"])
@co_required
def c_o_dashboard():
    print(session)
    user_role = session.get("user_role")
    # if session.get("user_role") != "Constituency Collection Officer": # Check if the user is a collection officer
    #     return redirect("/c_o_login") #redirect unauthorized users to the login page
    return render_template("c_officers/c_o_dashboard.html")


# Route for posting data of lost and found document ===========================================================
@app.route("/receive_documents", methods=["POST", "GET"])
@co_required
def receive_documents():
    counties = ["", "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita-Taveta", "Garissa", "Wajir", "Mandera", "Marsabit", "Isiolo", "Meru", "Tharaka-Nithi", "Embu", "Kitui", "Machakos", "Makueni", "Nyandarua", "Nyeri", "Kirinyaga", "Murang'a", "Kiambu", "Turkana", "West Pokot", "Samburu", "Trans-Nzoia", "Uasin Gishu", "Elgeyo-Marakwet", "Nandi", "Baringo", "Laikipia", "Nakuru", "Narok", "Kajiado", "Kericho", "Bomet", "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya", "Kisumu", "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi"]
    # session["id_number"] = id_number
    id_number = session.get("id_number") # Get the ID Number from the session
    first_name = session.get("first_name")

    conn = connect(host="localhost", user="root", password="", database="doc_re_s")# Database connection and cursor
    cur = conn.cursor()
    # Fetch the county from the database based on the ID Number
    cur.execute("SELECT county FROM drs_collection_officers WHERE first_name = %s AND id_number= %s", (first_name,id_number)) 
    row = cur.fetchone()
    if row:
        county = row[0]
    else:
        county = None

    if request.method == "POST":
        # Processing form submission
        first_name = request.form["first_name"]
        second_name = request.form.get("second_name") #this is to avoid getting a KeyError if the value is empty
        last_name = request.form["last_name"]
        document_id = request.form["document_id"]
        document_type = request.form["document_type"]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Getting current timestamp during receiving of document
        county = request.form["county"]
        constituency = request.form["constituency"]
        good_samaritan_name = request.form.get("good_samaritan_name")
        mobile_no = request.form.get("mobile_no")

        # Inserting data into the database
        sql = "INSERT INTO drs_lost_and_found(first_name, second_name, last_name, document_id, document_type, date_received, county,constituency, good_samaritan_name, mobile_no) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        if mobile_no:
            cur.execute(sql,(first_name, second_name, last_name, document_id, document_type, current_time, county,constituency, good_samaritan_name, mobile_no))
        else:
            cur.execute(sql,(first_name, second_name, last_name, document_id, document_type, current_time, county,constituency, good_samaritan_name, None)) # Insert NULL if mobile_no is not provided
        
        conn.commit()
        msg = "Document Received Successfully"
        # =================================================================================
        # GET MOBILE NO FROM drs_users TABLE WHERE f_name, l_name ARE EQUAL TO f_name, l_name in drs_lost_and_found
        # to activate promotional messages, dial *456*9*5# then  select option 5.
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        conn = connect(host="localhost", user="root", password="", database="doc_re_s", cursorclass=pymysql.cursors.DictCursor)
        message_suc = None  # Default value in case no message is sent
        phone_number = None  # Default value in case no phone number is fetched
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT drs_users.mobile_no FROM drs_users 
                    INNER JOIN drs_lost_and_found 
                    ON drs_users.first_name = drs_lost_and_found.first_name 
                    AND drs_users.last_name = drs_lost_and_found.last_name
                    WHERE drs_users.first_name = %s AND drs_users.last_name = %s
                    LIMIT 1  -- Limit the result to one row
                """,(first_name,last_name))
                phone = cur.fetchone()
                if phone:
                    phone_number = phone["mobile_no"]  # Access the mobile_no value directly from the dictionary
                    phone_number = "+254" + str(phone_number) # Prepend "+254" to the phone number
                    print("Mobile Number Fetched", phone_number)
                    # MESSAGE SENT TO THE OWNER IF REGISTERED
                    message_suc = "Your Document was Retrieved Successfully, Login to get more info at https://egn.pythonanywhere.com/ , Eric DRS Test Msg"
                    print(phone_number)
                    sms.send_sms(phone_number, message_suc)
                    # sms.send_sms("+254701838170","Your Document was Retrieved Successfully, Login to get more info at, https://egn.pythonanywhere.com/")
                else:
                    pass
        finally:
            conn.close()
        
        # ====================================================================================
        # passing collected details to the success page
        return render_template("c_officers/co_handoversuccess.html", message_suc=message_suc, message=msg, first_name=first_name, second_name=second_name, last_name=last_name, document_id=document_id, document_type=document_type, date_received=current_time,county=county, constituency=constituency, good_samaritan_name=good_samaritan_name, mobile_no=mobile_no, phone_number=phone_number)

    # Fetching document types from the database
    cur.execute("SELECT document_name FROM drs_document_types")
    document_types = cur.fetchall()
    return render_template("c_officers/co_receivedocuments.html", document_types=document_types, counties=counties, county=county)



@app.route("/successful_collection")
@co_required
def successful_collection():
    return render_template("c_officers/co_handoversuccess.html")


# 2.Handover documents to owners
@app.route("/handover_requests")
@co_required
def handover_requests():
    return render_template("c_officers/co_handoverrequests.html",)


# Define the route for handling the search
@app.route("/search_lost", methods=["POST"])
@co_required
def search_lost():
    document_id = request.form.get("document_id") # Get the ID number from the form data
    # Fetch data from the database based on the provided ID number
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    sql = "SELECT * FROM drs_lost_and_found WHERE document_id = %s"
    cur.execute(sql, (document_id,))
    user_data = cur.fetchone()
    if user_data:
        # Document ID found, fetch additional data
        document_type = user_data[5]  # Assuming document type is at index 5
        sql = "SELECT default_charges FROM drs_document_types WHERE document_name = %s"
        cur.execute(sql, (document_type,))
        charges_data = cur.fetchone()
        charges = charges_data[0] if charges_data else None     
        conn.close()
        # Render a template to display the user data
        return render_template("/c_officers/c_officers2/user_details.html", user_data=user_data, charges=charges)
    else:
        conn.close()
        # Document ID not found, render the same page with an error message
        return render_template("/c_officers/c_officers2/user_details.html", message="Document ID not found.")



# co_handover_search.html
@app.route("/handover_initiate_pay")
@co_required
def handover_initiate_pay():
    # if session.get("user_role") != "Constituency Collection Officer": # Check if the user is a collection officer
    #     return redirect("/c_o_login") #redirect unauthorized users to the login page
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    document_id = request.args.get("document_id")
    sql = "SELECT * FROM drs_lost_and_found WHERE document_id = %s"
    cur.execute(sql, (document_id,))
    single_user = cur.fetchone()
    conn.close()
    session["single_user"] = single_user
    return render_template("/c_officers/c_officers2/co_handover_initiate.html", single_user=single_user)


@app.route("/mpesa", methods=["POST","GET"])
@co_required
def mpesa():
    if request.method == "POST":
        mobile_no = request.form["mobile_no"]
        amount = request.form["price"]
        import mpesa
        mpesa.stk_push(mobile_no,amount)
        return render_template("/c_officers/c_officers2/co_mpesa_success.html")
    else:
        return redirect("/c_o_login")



# Define the route for sending to another collection center
@app.route("/center_redirect", methods=["GET", "POST"])
@co_required
def center_redirect():
    counties = ["","Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita-Taveta", "Garissa", "Wajir", "Mandera", "Marsabit", "Isiolo", "Meru", "Tharaka-Nithi", "Embu", "Kitui", "Machakos", "Makueni", "Nyandarua", "Nyeri", "Kirinyaga", "Murang'a", "Kiambu", "Turkana", "West Pokot", "Samburu", "Trans-Nzoia", "Uasin Gishu", "Elgeyo-Marakwet", "Nandi", "Baringo", "Laikipia", "Nakuru", "Narok", "Kajiado", "Kericho", "Bomet", "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya", "Kisumu", "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi"]
    if request.method == "POST":
        # Get the document ID from the form data
        document_id = request.form["document_id"]  
        session["document_id"] = document_id
        # Fetch data from the lost_and_found table based on the document ID
        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
        cur = conn.cursor()
        sql = "SELECT * FROM drs_lost_and_found WHERE document_id = %s"
        cur.execute(sql, (document_id,))
        document_data = cur.fetchone()
        if document_data:
            # Update location and collection center for the selected document
            new_county = request.form["new_county"]
            new_collection_constituency = request.form["new_collection_constituency"]
            sql = "UPDATE drs_lost_and_found SET county = %s, constituency = %s WHERE document_id = %s"
            cur.execute(sql, (new_county, new_collection_constituency, document_id))
            conn.commit()
            conn.close()    
            # Redirect to a success page or render a template with transit details
            return redirect("/transit")
        else:
            # Document ID not found, render a template with an error message
            return render_template("c_officers/co_centerredirect.html", message="Document ID not found.")
    # Render the form to enter document ID and transit details
    return render_template("c_officers/co_centerredirect.html", counties=counties)


@app.route("/transit", methods=["GET", "POST"])
@co_required
def transit():
    document_id = session.get("document_id")
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    sql = "SELECT * FROM drs_lost_and_found WHERE document_id = %s"
    cur.execute(sql, (document_id,))
    document_data = cur.fetchone()
    # Render the form to enter document ID and transit details
    return render_template("c_officers/transit.html", document_data=document_data)

# 4.Document Statistics
@app.route("/document_statistics")
@co_required
def document_statistics():
    return render_template("c_officers/co_documentstatistics.html")


@app.route("/request_permissions", methods=["POST","GET"])
@co_required
def request_permissions():
    reason = request.form.get("reason")
    # Save the reason for the permission request, notify the admin, etc.
    flash("Permission request sent successfully!", "success")
    return redirect("/document_statistics")



# 5.Track progress
@app.route("/track_progress", methods =["POST","GET"])
@co_required
def track_progress():
    document_id = request.form.get("document_id") # Get the ID number from the form data
    # Fetch data from the database based on the provided ID number
    conn = connect(host="localhost",user="root",password="",database="doc_re_s")
    cur = conn.cursor()
    sql = "SELECT * FROM drs_lost_and_found WHERE document_id = %s"
    cur.execute(sql, (document_id,))
    user_data = cur.fetchone()
    if user_data:
        # Document ID found, fetch additional data
        document_type = user_data[5]  # Assuming document type is at index 5
        sql = "SELECT default_charges FROM drs_document_types WHERE document_name = %s"
        cur.execute(sql, (document_type,))
        charges_data = cur.fetchone()
        charges = charges_data[0] if charges_data else None
        conn.close()
        # Render a template to display the user data
        return render_template("c_officers/co_trackprogress.html", documents=[user_data], charges=charges)
    else:
        conn.close()
        # Document ID not found, render the lost and found page with an error message
        return render_template("c_officers/co_trackprogress.html", message="Document ID not found.")


# 6.Report claims
@app.route("/report_claims", methods=["POST", "GET"])
@co_required
def report_claims():
    if request.method == "POST":
        claimant_name = request.form.get("claimant_name")
        contact_info = request.form.get("contact_info")
        description = request.form.get("description")

        # Save data to the database
        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
        cur = conn.cursor()
        sql = "INSERT INTO drs_officer_claims(claimant_name, contact_info, description) VALUES (%s, %s, %s)"
        cur.execute(sql, (claimant_name, contact_info, description))
        conn.commit()
        
        flash("Claim report submitted successfully!", "info")
        return redirect("/report_claims")
    
    # Retrieve officer information from the session
    officer_name = session.get("first_name")
    
    # Fetch officer_id from the database based on officer_name
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    sql = "SELECT id_number FROM drs_users WHERE first_name = %s"
    cur.execute(sql, (officer_name,))
    result = cur.fetchone()
    
    if result:
        officer_id = result[0]
    else:
        # Handle the case where officer_id is not found
        officer_id = None
    
    conn.close()
    
    return render_template("c_officers/co_reportclaims.html", fullname=officer_name, officer_id=officer_id)






# ================================================================================================================
# ======= ADMIN ROUTE ============================================================================================

# === ADMIN_LOGIN.HTML ========================================================================================
@app.route("/admin_login", methods=["POST","GET"])
def admin_login():
    if request.method == "POST":
        id_number = request.form["id_number"]
        password = request.form["password"]

        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
        cur = conn.cursor()
        cur.execute("SELECT user_role FROM drs_users WHERE id_number = %s", (id_number,)) # Fetch the user_role first
        user_role = cur.fetchone()
        
        if user_role and user_role[0] == 'admin':
            session["id_number"] = id_number
            id_number = session.get("id_number")
            # Execute SQL query with user_role included in WHERE clause
            cur.execute("SELECT * FROM drs_users WHERE id_number = %s AND user_role = 'admin'", (id_number,))
            user_data = cur.fetchone()
            if user_data:
                # Check if the provided password matches the hashed password from the database
                if check_password_hash(user_data[7], password):
                    session["first_name"] = user_data[1]
                    session["last_name"] = user_data[2]
                    session["id_number"] = user_data[3]
                    session["mobile_no"] = user_data[4]
                    session["email_address"] = user_data[5]
                    session["logged_in"] = True
                    return redirect("/admin")
                else:
                    msg = "Invalid username and password combination"
                    return render_template("admin/admin_login.html", message=msg)
            else:
                msg = "Invalid username and password combination"
                return render_template("admin/admin_login.html", message=msg)
        else:
            msg = "You are not authorized to access this page."
            return render_template("admin/admin_login.html", message=msg)
    return render_template("admin/admin_login.html")





# ==== INDEX_ADMIN.HTML (admin dashboard after loging)===========================================================
@app.route("/admin")
@admin_required
def admin():
    return render_template("admin/index_admin.html")


# ==== DB_STATISTICS.HTML    ===================================================================================
@app.route('/db_statistics')
@admin_required
def db_statistics():
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    # Count registered collection officers
    sql = "SELECT COUNT(*) FROM drs_collection_officers WHERE user_role = 'Constituency Collection Officer' "
    cur.execute(sql)
    officers_statistic = cur.fetchall()

    sql_officers_data = "SELECT first_name, last_name, id_number,county, COUNT(*) FROM drs_collection_officers GROUP BY first_name ORDER BY first_name ASC"
    cur.execute(sql_officers_data)
    officers_data = cur.fetchall()

    # Count registered users
    sql = "SELECT COUNT(*) FROM drs_users WHERE user_role = 'user' "
    cur.execute(sql)
    users_statistic = cur.fetchall()

    sql_users_data = "SELECT first_name, last_name, id_number, COUNT(user_role) FROM drs_users GROUP BY first_name, last_name, id_number ORDER BY first_name ASC"
    cur.execute(sql_users_data)
    users_data = cur.fetchall()

    return render_template("admin/db_statistics.html", users_statistic=users_statistic, officers_statistic=officers_statistic,users_data=users_data,officers_data=officers_data)


# ===== USER_MANAGEMENT.HTML =======================================================================================
@app.route("/user_management")
@admin_required
def user_management():
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    sql = "SELECT * FROM drs_users ORDER BY first_name, last_name, id_number ASC"
    cur.execute(sql)
    user_details = cur.fetchall()
    print(user_details[1])
    return render_template("admin/user_management.html", user_details=user_details)


@app.route("/search_user", methods=["POST", "GET"])
@admin_required
def search_user():
    # Get the ID number from the form data
    id_number = request.form.get("id_number")
    # Connect to the database
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    sql_query = "SELECT * FROM drs_users WHERE id_number = %s"
    # Execute the SQL query with the ID number as a parameter
    cur.execute(sql_query, (id_number,))
    user_details = cur.fetchall()  
    return render_template("admin/user_management.html", user_details=user_details)




# ===== MODAL-POP-UP on USER_MANAGEMENT.HTML ===============================================================
# For adding a new user:
@app.route("/add_user", methods=["POST","GET"])
@admin_required
def add_user():
    if request.method == "POST":
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            id_number = request.form["id_number"]
            mobile_no = request.form["mobile_no"]
            email_address = request.form["email_address"]
            user_role = request.form["user_role"]
            password = request.form["password"]
            
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8") #hashing the password
            
            conn = connect(host="localhost", user="root", password="", database="doc_re_s")
            cur = conn.cursor()
            sql = "INSERT INTO drs_users (first_name, last_name, id_number, mobile_no, email_address, user_role, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (first_name, last_name, id_number, mobile_no, email_address, user_role, hashed_password))
            conn.commit()
            message = "User Registered Successfully"
            return render_template("admin/user_management.html", message=message)
        
        except IntegrityError as e: # Check if the error is due to duplicate primary key (ID number)
            if e.args[0] == 1062:  # MySQL error code for duplicate entry
                error_msg = "User with similar ID Number already exists"
                return render_template("admin/user_management.html", message=error_msg)
            else: # Handle other IntegrityError cases if necessary
                error_msg = f"IntegrityError: {e}"
                app.logger.error(error_msg)
                return render_template("admin/user_management.html", message=error_msg)
        
        except Exception as e: # Handle other exceptions
            error_msg = f"Error occurred during registration: {e}"
            app.logger.error(error_msg)
            return render_template("admin/user_management.html", message=error_msg)
    else:
        return render_template("admin/user_management.html")  # Redirect back to user management page
    

@app.route("/delete_user", methods=["POST","GET"])
@admin_required
def delete_user():
    if request.method == "POST":
        id_number = request.form["id_number"]
        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
        cur = conn.cursor()
        cur.execute("DELETE FROM drs_users WHERE id_number = %s",(id_number,))
        conn.commit()
        message = "User Deleted Successfully"
    return render_template("admin/user_management.html",message=message) 


# ===== OFFICERCLAIMREPORTS.HTML ================================================================================
@app.route("/admin/officer_claim_reports", methods=["POST","GET"])
@admin_required
def officer_claim_reports():
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()

    if request.method == "POST":
        # Get the user_id of the message to mark as read from the form
        user_id = request.form.get("user_id")
        
        # Update the status of the specific message to 'read'
        cur.execute("UPDATE drs_officer_claims SET status = 'read' WHERE user_id = %s", (user_id,))
        conn.commit()

    # Fetch all unread messages
    sql = "SELECT user_id, claimant_name, contact_info, description FROM drs_officer_claims WHERE status = 'unread'"
    cur.execute(sql)
    officer_claims = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("admin/officerclaimreports.html", officer_claims=officer_claims)



# ==== DOCUMENTTYPE.HTML =========================================================================================
@app.route("/admin/manage_document_types", methods=["POST", "GET"])
@admin_required
def manage_document_types():
    if request.method == "POST":
        document_name = request.form["document_name"]
        default_charges = request.form["default_charges"]
        replacement_charges = request.form["replacement_charges"]
        
        conn = connect(host="localhost", user="root", password="", database="doc_re_s") # Connect to the database
        cur = conn.cursor()
        sql = "INSERT INTO drs_document_types (document_name, default_charges, replacement_charges) VALUES (%s, %s, %s)"# Insert data into the database
        cur.execute(sql, (document_name, default_charges, replacement_charges))
        conn.commit()
        conn.close()
        flash("Document Type Added Successfully!", "success") # Flash message and clear session
        return redirect("/admin/manage_document_types") # Redirect to the same page to avoid form resubmission
    return render_template("admin/documenttype.html") # Render the template for the form



# ROUTE FOR DISPLAYING ALL LOST AND FOUND DOCUMENTS IN THE DATABASE ===============================================
@app.route("/lost_and_found")
@admin_required
def lost_and_found():
    # Fetch all documents from the database
    conn = connect(host="localhost", user="root", password="", database="doc_re_s")
    cur = conn.cursor()
    sql = "SELECT * FROM drs_lost_and_found"
    cur.execute(sql)
    documents = cur.fetchall()
    conn.close()
    # Render the template with the documents
    return render_template("admin/lostandfound.html", documents=documents)



# SEARCHING A SPECIFIC DOCUMENT IN "/lost_and_found" route 
@app.route("/search_lost_and_found", methods =["POST","GET"])
@login_required
def search_lost_and_found():
    document_id = request.form.get("document_id") # Get the ID number from the form data
    # Fetch data from the database based on the provided ID number
    conn = connect(host="localhost",user="root",password="",database="doc_re_s")
    cur = conn.cursor()
    sql = "SELECT * FROM drs_lost_and_found WHERE document_id = %s"
    cur.execute(sql, (document_id,))
    user_data = cur.fetchone()
    if user_data:
        # Document ID found, fetch additional data
        document_type = user_data[5]  # Assuming document type is at index 5
        sql = "SELECT default_charges FROM drs_document_types WHERE document_name = %s"
        cur.execute(sql, (document_type,))
        charges_data = cur.fetchone()
        charges = charges_data[0] if charges_data else None
        conn.close()
        # Render a template to display the user data
        return render_template("admin/lostandfound.html", documents=[user_data], charges=charges)
    else:
        conn.close()
        # Document ID not found, render the lost and found page with an error message
        return render_template("admin/lostandfound.html", message="Document ID not found.")





# ======= ADMIN GENERAL IMAGE UPLOADS ============================================================================
@app.route("/drs_general_image_uploads", methods=["POST", "GET"])
def drs_general_image_uploads():
    if request.method == "POST":
        image_name = request.form["document_type"]  # Change to document_name
        general_image_path = request.files["general_image_path"]
        image_filename = secure_filename(general_image_path.filename)

        conn = connect(host="localhost", user="root", password="", database="doc_re_s")
        # conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
        cur = conn.cursor()
        sql = "INSERT INTO drs_general_images(image_name, general_image_path) VALUES (%s, %s)"

        cur.execute(sql, (image_name, "/../../static/images/" + image_filename))
        conn.commit()
        general_image_path.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))
        msg = "Image Upload Successful"
        return render_template("admin/general_images.html", message=msg, general_image_path=general_image_path)
    else:
        err = "Error Uploading Image"
        return render_template("admin/general_images.html", error=err)
    

#==== ADMIN ROUTES END HERE =======================================================================================

# ================================================================================================================


# USING API ======================================================================================================
# ================================================================================================================
from flask import jsonify
from flask_restful import Resource, Api # pip install flask-restful
from pymysql import cursors


api = Api(app)


# create a class for our resourse
class Employee(Resource):
    # a GET a request for this resource
    # ==== GET ==============================================================================================
    def get(self):
        conn = connect(host="egn.mysql.pythonanywhere-services.com",user="egn",password="12345678@#",database="egn$default")
        # cur = conn.cursor()
        cur = conn.cursor(cursors.DictCursor)
        sql = "SELECT * FROM employees"
        cur.execute(sql)
        if cur.rowcount > 0:
            users = cur.fetchall()
            return jsonify(users)
        else:
            return jsonify({"message":"No records were found"})

    # ====== POST =============================================================================================
    def post(self):
        data = request.json

        full_name = data["full_name"]
        email = data["email"]
        department = data["department"]
        salary = data["salary"]

        conn = connect(host="egn.mysql.pythonanywhere-services.com",user="egn",password="12345678@#",database="egn$default")
        cur =conn.cursor()
        sql = "INSERT INTO employees(full_name,email,department,salary)VALUES(%s,%s,%s,%s)"
        try:
            cur.execute(sql,(full_name,email,department,salary))
            conn.commit()
            return jsonify({"message":"POST successful"})
        except:
            conn.rollback()
            return jsonify({"message":"POST FAILED."})

    # ====== PUT =============================================================================
    def put(self):
        data = request.json

        full_name = data["full_name"]
        email = data["email"]
        department = data["department"]
        salary = data["salary"]
        employee_id = data["employee_id"]

        conn = connect(host="egn.mysql.pythonanywhere-services.com",user="egn",password="12345678@#",database="egn$default")
        cur = conn.cursor()
        sql = "UPDATE employees SET full_name=%s, email=%s, department=%s, salary=%s WHERE employee_id=%s"
        try:
            cur.execute(sql,(full_name,email,department,salary,employee_id))
            conn.commit()
            return jsonify({"message":"PUT SUCCESSFUL. Record updated successfully."})
        except:
            conn.rollback()
            return jsonify({"message":"PUT FAILED. Record update not successful."})

    # === DELETE ====================================================================================
    def delete(self):
        data = request.json
        employee_id = data["employee_id"]

        conn = connect(host="egn.mysql.pythonanywhere-services.com",user="egn",password="12345678@#",database="egn$default")
        cur = conn.cursor()
        sql = "DELETE FROM employees WHERE employee_id=%s"
        try:
            cur.execute(sql,employee_id)
            conn.commit()
            return jsonify({"message":"DELETE SUCCESSFUL.Record deleted successfully"})
        except:
            conn.rollback()
            return jsonify({"message":"DELETE FAILED!.Record deleted successfully"})

    # ===== END =====================================================================================

api.add_resource(Employee,"/employees")




class User(Resource):
    def get(self):
        conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
        cur = conn.cursor(cursors.DictCursor)
        sql = "SELECT * FROM drs_users"
        cur.execute(sql)
        if cur.rowcount > 0:
            users = cur.fetchall()
            return jsonify(users)
        else:
            return jsonify({"message": "No records were found"})




    def post(self):
        data = request.json
        first_name = data["first_name"]
        last_name = data["last_name"]
        id_number = data["id_number"]
        mobile_no = data["mobile_no"]
        email = data["email"]
        password = data["password"]
        conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
        cur = conn.cursor()
        sql = "INSERT INTO drs_users(first_name, last_name, id_number, mobile_no, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (first_name, last_name, id_number, mobile_no, email, password))
            conn.commit()
            return jsonify({"message": "Successful User Registration"})
        except:
            conn.rollback()
            return jsonify({"message": "Registration Failed"})


    def put(self):
        data = request.json
        first_name = data["first_name"]
        last_name = data["last_name"]
        id_number = data["id_number"]
        mobile_no = data["mobile_no"]
        email = data["email"]
        password = data["password"]
        conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
        cur = conn.cursor()
        sql = "UPDATE drs_users SET first_name=%s, last_name=%s, id_number=%s, mobile_no=%s, email=%s, password=%s WHERE id_number=%s"
        try:
            cur.execute(sql, (first_name, last_name, id_number, mobile_no, email, password))
            conn.commit()
            return jsonify({"message": "User Records Updated Successfully."})
        except:
            conn.rollback()
        return jsonify({"message": "User Record Update Failed!"})


    def delete(self):
        data = request.json
        id_number = data["id_number"]
        conn = connect(host="egn.mysql.pythonanywhere-services.com", user="egn", password="12345678@#", database="egn$default")
        cur = conn.cursor()
        sql = "DELETE FROM drs_users WHERE id_number=%s"
        try:
            cur.execute(sql, id_number)
            conn.commit()
            return jsonify({"message": "User deleted successfully"})
        except:
            conn.rollback()
            return jsonify({"message": "Delete attempt Failed!"})

api.add_resource(User, "/users")



if __name__ == ("__main__"):
    app.run(debug=True)

# How to run this app For Linux mint and #activate the app.py environment
    # a)open vscode Terminal
    # For Linux
    # b)source env/bin/activate
    # c)python3 app.py


#  pip install waitress #To remove warning that this is not a development server
# pip freeze > requirements.txt