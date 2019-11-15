from flask import Flask, render_template, request, redirect, url_for, flash, session, logging, jsonify
# import pymysql
import docx2txt, PyPDF2
import pathlib,smtplib,config
import re
import nltk, os, subprocess, code, glob, re, traceback, sys, inspect
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms.widgets import TextArea
import re

# paginate
from flask_paginate import Pagination, get_page_args


app = Flask(__name__, static_url_path='/static')

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cv_scanner'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='cv_scanner',autocommit=True)

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/signup", methods=["POST"])
# def signup():
#     firstname = str(request.form["firstname"])
#     lastname = str(request.form["lastname"])
#     emailid = str(request.form["emailid"])
#     password = str(request.form["password"])
#
#     cursor = conn.cursor()
#
#     cursor.execute("INSERT INTO user(firstname,lastname,emailid,password)VALUES(%s,%s,%s,%s)", (firstname, lastname, emailid, password))
#     conn.commit()
#     return redirect(url_for("login"))





# @app.route("/checkuser", methods=["POST"])
# def check():
#     emailid = str(request.form["emailid"])
#     password = str(request.form["password"])
#     cursor = conn.cursor()
#     cursor.execute("SELECT emailid FROM user WHERE emailid ='"+emailid+"'")
#     user = cursor.fetchone()
#
#     if len(user) is 1:
#         return redirect(url_for("main"))


@app.route('/poster')
def poster():
    return render_template("poster.html")


# @app.route('/jobpost')
# def jobpost():
#     return render_template("jobpost.html")
#
# @app.route('/jobpost2')
# def jobpost2():
#     return render_template("jobpost2.html")

# @app.route("/poster2", methods=["POST"])
# def poster2():
#     E_com = str(request.form["Com_Name"])
#     Job_title = str(request.form["JT"])
#     job_describtion = str(request.form["styled-textarea"])
#     E_sk = str(request.form["E_skills"])
#     Job_loc = str(request.form["JL"])
#     Min_Qual = str(request.form["MQ"])
#     Sal_range = str(request.form["Sal_r"])
#
#
#     cursor = conn.cursor()
#
#     cursor.execute("INSERT INTO job_posts(company_name,job_desc,job_loc,job_title,min_qual,sal_range,skills)VALUES(%s,%s,%s,%s,%s,%s,%s)", (E_com, Job_title, job_describtion, E_sk, Job_loc, Min_Qual, Sal_range))
#     conn.commit()
#     return "Successfully Inserted"

# @app.route("/home")
# def home():
#     return render_template("Default.html")


class RegisterForm(Form):
    first_name = StringField(u'First Name', validators=[validators.input_required()])
    last_name = StringField(u'Last Name', validators=[validators.input_required()])
    email = EmailField(u'Email', validators=[validators.input_required()])
    password = PasswordField(u'Password', validators=[validators.input_required()])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        email_list = []

        cur = mysql.connection.cursor()

        cur.execute("SELECT emailid FROM user")
        email_in_db = cur.fetchall()
        print('email_in_db:',email_in_db)
        for mail in email_in_db:
            print('for loop output:', mail['emailid'])
            email_list.append(mail['emailid'])

        print('outside for loop output:',email_list)

        if len(form.password.data) >= 6 and email not in email_list:
            password = sha256_crypt.encrypt(str(form.password.data))

            cur.execute("INSERT INTO user(firstname,lastname,emailid,password) VALUES(%s,%s,%s,%s)", (first_name, last_name, email, password))

            mysql.connection.commit()

            cur.close()

            flash('You are now registered', 'success')

        elif email in email_list:
            flash('Email already exists', 'danger')

        else:
            flash('Password length should be minimum 6 characters', 'danger')

        # return redirect(url_for('login'))

    return render_template('register.html', form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM user WHERE emailid = %s", [email])

        if result > 0:
            data = cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['email'] = email


                # CHECK IF USER IS NEW OR NOT
                cur.execute("SELECT user_id FROM user WHERE emailid = '{_email}'".format(_email = email))
                user_id = cur.fetchone()
                user_id = user_id['user_id']

                uid_list = []
                cur.execute("SELECT user_id FROM profile WHERE user_id = '{_user_id}'".format(_user_id = user_id))
                uid_in_db = cur.fetchall()
                # print('email_in_db:',email_in_db)
                for uid in uid_in_db:
                    # print('for loop output:', mail['emailid'])
                    uid_list.append(uid['user_id'])

                if user_id not in uid_list:
                    flash('You are logged in. Please complete your profile to continue', 'success')
                    return redirect(url_for('createprofile'))

                else:
                    return redirect(url_for('welcome_page'))

            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)



        else:
            error = 'User not found'
            return render_template('login.html', error=error)


    return render_template('login.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))

@app.route('/home')
@is_logged_in
def home():

    # u_id = session['email']

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(id) FROM job_posts")
    count = cur.fetchone()
    count = count['COUNT(id)']
    # print("count:",count)

    return render_template('home.html', count=count)

class CreateProfileForm(Form):

    # Education Form
    dob = StringField(u'School Name', validators=[validators.input_required()])
    gender = StringField(u'Degree', validators=[validators.input_required()])
    maritalstatus = StringField(u'Feild_of_study', validators=[validators.input_required()])
    country = StringField(u'Grade', validators=[validators.input_required()])
    city = StringField(u'Acti_Soci', validators=[validators.input_required()])
    phone = StringField(u'To', validators=[validators.input_required()])

    # cv = StringField(u'To', validators=[validators.input_required()])

    # qualification = StringField(u'To', validators=[validators.input_required()])
    # institute = StringField(u'To', validators=[validators.input_required()])
    # graduated = StringField(u'To', validators=[validators.input_required()])
    # grade = StringField(u'To', validators=[validators.input_required()])
    # experience = StringField(u'To', validators=[validators.input_required()])
    # careerlevel = StringField(u'To', validators=[validators.input_required()])
    # industry = StringField(u'To', validators=[validators.input_required()])
    # skills = StringField(u'To', validators=[validators.input_required()])

@app.route('/createprofile', methods=['GET', 'POST'])
@is_logged_in
def createprofile():
    form = CreateProfileForm(request.form)
    if request.method == 'POST' and form.validate():

        dob = form.dob.data
        gender = form.gender.data
        maritalstatus = form.maritalstatus.data
        country = form.country.data
        city = form.city.data
        phone = form.phone.data
        file = request.files['resume']
        # cv = docx2txt.process(cv_file)
        file_extension = pathlib.Path(file.filename).suffix
        print('extension is ',file_extension)

        if (file_extension == '.docx'):
            cv = docx2txt.process(file)

        elif (file_extension == ".pdf"):

            cv = ''

            read_PDF = PyPDF2.PdfFileReader(file)

            for i in range(read_PDF.getNumPages()):

                page = read_PDF.getPage(i)
                cv += page.extractText()
            print("----------------------------")
            print(cv)
            print("----------------------------")
            print("PDF file is uploaded")
        else:
            flash("Sorry! Only .PDF and .DOCX file formats are acceptable",'danger')


        # qualification = form.qualification.data
        # institute = form.institute.data
        # graduated = form.graduated.data
        # grade = form.grade.data
        # experience = form.experience.data
        # careerlevel = form.careerlevel.data
        # industry = form.industry.data
        # skills = form.skills.data

        u_id = session['email']

        cur = mysql.connection.cursor()

        cur.execute("SELECT user_id FROM user WHERE emailid='{userid}'".format(userid=u_id))
        uid = cur.fetchone()
        uid = uid['user_id']

        # cur.execute("INSERT INTO profile (user_id, job_id) SELECT user_id, id FROM user INNER JOIN job_posts WHERE user.emailid='{email}' AND job_posts.id={id}".format(email=email0, id=id))



        # get user id from email of session
        # id_from_email = session['email']
        # cur.execute("SELECT user_id FROM user WHERE emailid='{emailid}'".format(emailid=id_from_email))
        # data0 = cur.fetchone()
        # data0 = data0['user_id']

        # get cv for extraction
        # cur.execute("SELECT cv FROM profile WHERE user_id='{userid}'".format(userid=data0))
        # get_CV=cur.fetchall()
        get_CV = cv

        # cv_for_email=str(get_CV)
        # cv_for_Phno = str(get_CV)
        # cv_for_name = str(get_CV)
        cv_for_exp = str(get_CV)
        cv_for_skills = str(get_CV)



        # Cv's extraction work goes here
        mfile = open("C:\\Users\\Talal\\PycharmProjects\\cv\\degrees.txt", "r")
        re_qualification = mfile.read()

        mfile = open("C:\\Users\\Talal\\PycharmProjects\\cv\\degrees2.txt", "r")
        re_qualification2 = mfile.read()

        # reading resume/cv
        Req_Qualification1 = ""
        # my_text = docx2txt.process("D:\\KIET\\CV DATA\\abdul hadi CV.docx")

        # extracting
        m = re.search(re_qualification, str(get_CV))
        # Req_Qualification1.append(m.group(0))
        while m != None:
            Req_Qualification1 += m.group(0) + " "
            get_CV = str(get_CV)[m.end():len(str(get_CV))]
            m = re.search(re_qualification, str(get_CV))
            break

        m2 = re.search(re_qualification2, str(get_CV))
        # Req_Qualification1.append(m2.group(0))

        while m2 != None:
            Req_Qualification1 += m2.group(0) + " "
            get_CV = str(get_CV)[m2.end():len(str(get_CV))]
            m2 = re.search(re_qualification2, str(get_CV))
            break





        #
        # ---experience
        #

        # lines = str(get_CV).split("\n")
        req_Exp = ""
        # for sent_ in str(cv_for_exp):
        #     sent_.lower()
        #     print (sent_)

        if re.search('[eE]xperience|[wW]orked|[wW]orking|[wW]ork|[yY]ear', cv_for_exp):

            m = re.search('[0-9]+[ ]?[yY]ear[s]?', cv_for_exp)
            while (m != None):

                req_Exp += m.group(0)
                cv_for_exp = cv_for_exp[m.end():len(cv_for_exp)]
                m = re.search('[0-9]+[ ]?[yY]ear[s]?', cv_for_exp)
                break
            m2 = re.search('[0-9]{4}-[0-9]{4}', cv_for_exp)
            while (m2 != None):
                cv_for_exp = cv_for_exp[m2.end():len(cv_for_exp)]
                m2 = re.search('[0-9]{4}-[0-9]{4}', cv_for_exp)
                if m2 is None:
                    break
                exp_ = m2.group(0).split("-")
                e1 = int(exp_[1]) - int(exp_[0])
                req_Exp += str(e1)
                break





        #
        # Skills
        #

        req_skills = ""
        skill_set = open("C:\\Users\\Talal\\PycharmProjects\\cv\\skill_set.txt", "r")
        reg_skill = skill_set.read()

        m = re.search(reg_skill, str(cv_for_skills))
        while (m != None):
            if (m.group(0) not in req_skills):
                req_skills += m.group(0)
                req_skills += " "
            cv_for_skills = cv_for_skills[m.end():len(cv_for_skills)]
            m = re.search(reg_skill, str(cv_for_skills))

        req_skills = req_skills.replace(" ",",")

        cur.execute("INSERT INTO profile(user_id, dob, gender, maritalstatus, country, city, phone, cv, qual, exp, skills) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (uid, dob, gender, maritalstatus, country, city, phone, cv, Req_Qualification1, req_Exp, req_skills))

        mysql.connection.commit()

        cur.close()

        flash('Profile is Submitted', 'success')

        return redirect(url_for('editprofile'))

    return render_template('createprofile.html', form = form)











class EditProfileForm(Form):

    # Education Form
    dob = StringField(u'School Name', validators=[validators.input_required()])
    gender = StringField(u'Degree', validators=[validators.input_required()])
    maritalstatus = StringField(u'Feild_of_study', validators=[validators.input_required()])
    country = StringField(u'Grade', validators=[validators.input_required()])
    city = StringField(u'Acti_Soci', validators=[validators.input_required()])
    phone = StringField(u'To', validators=[validators.input_required()])
    resume = StringField(u'Too', validators=[validators.input_required()])

    # USER TABLE INFO
    # email = StringField(u'School Name', validators=[validators.input_required()])
    # registerdate = StringField(u'Degree', validators=[validators.input_required()])
    firstname = StringField(u'Feild_of_study', validators=[validators.input_required()])
    lastname = StringField(u'Grade', validators=[validators.input_required()])
    # password = StringField(u'Acti_Soci', validators=[validators.input_required()])


    # cv = StringField(u'To', validators=[validators.input_required()])

    # qualification = StringField(u'To', validators=[validators.input_required()])
    # institute = StringField(u'To', validators=[validators.input_required()])
    # graduated = StringField(u'To', validators=[validators.input_required()])
    # grade = StringField(u'To', validators=[validators.input_required()])
    # experience = StringField(u'To', validators=[validators.input_required()])
    # careerlevel = StringField(u'To', validators=[validators.input_required()])
    # industry = StringField(u'To', validators=[validators.input_required()])
    # skills = StringField(u'To', validators=[validators.input_required()])

@app.route('/editprofile', methods=['GET', 'POST'])
@is_logged_in
def editprofile():

    email = session['email']

    cur = mysql.connection.cursor()

    # CHECK IF USER IS NEW OR NOT
    cur.execute("SELECT user_id FROM user WHERE emailid = '{_email}'".format(_email = email))
    user_id = cur.fetchone()
    user_id = user_id['user_id']

    cur.execute("SELECT user_id FROM profile WHERE user_id = '{_user_id}'".format(_user_id = user_id))
    uid_in_db = cur.fetchone()
    uid_in_db = uid_in_db['user_id']
    print('uid_in_db:',uid_in_db)


    # FETCH ALL DATA FOR EDITING PROFILE
    cur.execute("SELECT * FROM profile WHERE user_id = '{_user_id}'".format(_user_id = uid_in_db))
    profile_data = cur.fetchone()
    # print(profile_data)


    # FETCH DATA FROM USER TABLE TO EDIT USER'S EMAIL, PASSWORD ETC.
    cur.execute("SELECT * FROM user WHERE user_id = '{_user_id}'".format(_user_id = user_id))
    user_table_data = cur.fetchone()
    print("user_table_data:",user_table_data)

    # for uid in uid_in_db:
    #     # print('for loop output:', mail['emailid'])
    #     uid_list.append(uid['user_id'])
    #
    # if user_id not in uid_list:
    #     flash('Please complete your profile to continue', 'success')
    #     return redirect(url_for('createprofile'))
    #
    # else:
    #     return redirect(url_for('editprofile'))


    form = EditProfileForm(request.form)



    # THIS CODE BLOCK ONLY RUNS WHEN DATA IS CALLED FROM DATABASE
    if request.method == 'GET':

        form.dob.data = profile_data['dob']
        form.gender.data = profile_data['gender']
        form.maritalstatus.data = profile_data['maritalstatus']
        form.country.data = profile_data['country']
        form.city.data = profile_data['city']
        form.phone.data = profile_data['phone']
        form.resume.data = profile_data['cv']


        # USER TABLE DATABASE DATA

        # form.email.data = user_table_data['emailid']
        # form.registerdate.data = user_table_data['registerdate']
        form.firstname.data = user_table_data['firstname']
        form.lastname.data = user_table_data['lastname']
        # form.password.data = ""
        # form.phone.data = user_table_data['phone']
        # form.resume.data = user_table_data['cv']



    elif request.method == 'POST' or request.method == 'GET' and form.validate():

        # DATA FROM USER TABLE
        # email = form.email.data
        # registerdate = form.registerdate.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        # password = form.password.data


        dob = form.dob.data
        gender = form.gender.data
        maritalstatus = form.maritalstatus.data
        country = form.country.data
        city = form.city.data
        phone = form.phone.data
        # file = form.resume.data
        file = request.files['resume']
        # cv = docx2txt.process(cv_file)
        file_extension = pathlib.Path(file.filename).suffix
        print('extension is ',file_extension)

        if (file_extension == '.docx'):
            cv = docx2txt.process(file)

        elif (file_extension == ".pdf"):

            cv = ''

            read_PDF = PyPDF2.PdfFileReader(file)

            for i in range(read_PDF.getNumPages()):

                page = read_PDF.getPage(i)
                cv += page.extractText()
            print("----------------------------")
            print(cv)
            print("----------------------------")
            print("PDF file is uploaded")
        else:
            flash("Sorry! Only .PDF and .DOCX file formats are acceptable",'danger')


        # qualification = form.qualification.data
        # institute = form.institute.data
        # graduated = form.graduated.data
        # grade = form.grade.data
        # experience = form.experience.data
        # careerlevel = form.careerlevel.data
        # industry = form.industry.data
        # skills = form.skills.data

        u_id = session['email']

        cur.execute("SELECT user_id FROM user WHERE emailid='{userid}'".format(userid=u_id))
        uid = cur.fetchone()
        uid = uid['user_id']

        # cur.execute("INSERT INTO profile (user_id, job_id) SELECT user_id, id FROM user INNER JOIN job_posts WHERE user.emailid='{email}' AND job_posts.id={id}".format(email=email0, id=id))



        # get user id from email of session
        # id_from_email = session['email']
        # cur.execute("SELECT user_id FROM user WHERE emailid='{emailid}'".format(emailid=id_from_email))
        # data0 = cur.fetchone()
        # data0 = data0['user_id']

        # get cv for extraction
        # cur.execute("SELECT cv FROM profile WHERE user_id='{userid}'".format(userid=data0))
        # get_CV=cur.fetchall()
        get_CV = cv

        # cv_for_email=str(get_CV)
        # cv_for_Phno = str(get_CV)
        # cv_for_name = str(get_CV)
        cv_for_exp = str(get_CV)
        cv_for_skills = str(get_CV)



        # Cv's extraction work goes here
        mfile = open("C:\\Users\\Talal\\PycharmProjects\\cv\\degrees.txt", "r")
        re_qualification = mfile.read()

        mfile = open("C:\\Users\\Talal\\PycharmProjects\\cv\\degrees2.txt", "r")
        re_qualification2 = mfile.read()

        # reading resume/cv
        Req_Qualification1 = ""
        # my_text = docx2txt.process("D:\\KIET\\CV DATA\\abdul hadi CV.docx")

        # extracting
        m = re.search(re_qualification, str(get_CV))
        # Req_Qualification1.append(m.group(0))
        while m != None:
            Req_Qualification1 += m.group(0) + " "
            get_CV = str(get_CV)[m.end():len(str(get_CV))]
            m = re.search(re_qualification, str(get_CV))
            break

        m2 = re.search(re_qualification2, str(get_CV))
        # Req_Qualification1.append(m2.group(0))

        while m2 != None:
            Req_Qualification1 += m2.group(0) + " "
            get_CV = str(get_CV)[m2.end():len(str(get_CV))]
            m2 = re.search(re_qualification2, str(get_CV))
            break





        #
        # ---experience
        #

        # lines = str(get_CV).split("\n")
        req_Exp = ""
        # for sent_ in str(cv_for_exp):
        #     sent_.lower()
        #     print (sent_)

        if re.search('[eE]xperience|[wW]orked|[wW]orking|[wW]ork|[yY]ear', cv_for_exp):

            m = re.search('[0-9]+[ ]?[yY]ear[s]?', cv_for_exp)
            while (m != None):

                req_Exp += m.group(0)
                cv_for_exp = cv_for_exp[m.end():len(cv_for_exp)]
                m = re.search('[0-9]+[ ]?[yY]ear[s]?', cv_for_exp)
                break
            m2 = re.search('[0-9]{4}-[0-9]{4}', cv_for_exp)
            while (m2 != None):
                cv_for_exp = cv_for_exp[m2.end():len(cv_for_exp)]
                m2 = re.search('[0-9]{4}-[0-9]{4}', cv_for_exp)
                if m2 is None:
                    break
                exp_ = m2.group(0).split("-")
                e1 = int(exp_[1]) - int(exp_[0])
                req_Exp += str(e1)
                break

        print("Experience:",req_Exp)





        #
        # Skills
        #

        req_skills = ""
        skill_set = open("C:\\Users\\Talal\\PycharmProjects\\cv\\skill_set.txt", "r")
        reg_skill = skill_set.read()

        m = re.search(reg_skill, str(cv_for_skills))
        while (m != None):
            if (m.group(0) not in req_skills):
                req_skills += m.group(0)
                req_skills += " "
            cv_for_skills = cv_for_skills[m.end():len(cv_for_skills)]
            m = re.search(reg_skill, str(cv_for_skills))

        # SKILLS TURN FROM STRING INTO COMMA SEPARATED STRING
        req_skills = req_skills.replace(" ",",")

        # ELIMINATE EMPTY SPACES
        Req_Qualification1 = Req_Qualification1.replace("  "," ")
        Req_Qualification1 = Req_Qualification1.lstrip()
        Req_Qualification1 = Req_Qualification1.rstrip()
        print("Req_Qualification1:",Req_Qualification1)


        cur.execute("UPDATE profile, user SET profile.user_id='{user_id}', profile.dob='{dob}', profile.gender='{gender}', profile.maritalstatus='{maritalstatus}', profile.country='{country}', profile.city='{city}', profile.phone='{phone}', profile.cv='{cv}', profile.qual='{qual}', profile.exp='{exp}', profile.skills='{skills}', user.firstname='{firstname}', user.lastname='{lastname}' WHERE profile.user_id='{uid_in_db}' AND user.user_id='{uid_in_db}'".format(user_id=uid, dob=dob, gender=gender, maritalstatus=maritalstatus, country=country, city=city, phone=phone, cv=cv, qual=Req_Qualification1, exp=req_Exp, skills=req_skills, firstname=firstname, lastname=lastname, uid_in_db=uid_in_db))

        mysql.connection.commit()

        cur.close()

        flash('Profile is Submitted', 'success')

        # return redirect(url_for('login'))

    return render_template('editprofile.html', form = form)






@app.route('/profile', methods=['GET', 'POST'])
@is_logged_in
def profile():
    cur = mysql.connection.cursor()

    email = session['email']


    # CHECK IF USER IS NEW OR NOT
    cur.execute("SELECT user_id FROM user WHERE emailid = '{_email}'".format(_email = email))
    user_id = cur.fetchone()
    user_id = user_id['user_id']

    uid_list = []
    cur.execute("SELECT user_id FROM profile WHERE user_id = '{_user_id}'".format(_user_id = user_id))
    uid_in_db = cur.fetchall()
    # print('email_in_db:',email_in_db)
    for uid in uid_in_db:
        # print('for loop output:', mail['emailid'])
        uid_list.append(uid['user_id'])

    if user_id not in uid_list:
        flash('Please complete your profile to continue', 'success')
        return redirect(url_for('createprofile'))

    else:
        return redirect(url_for('editprofile'))

    cur.close()





@app.route('/welcome_page', methods=['GET', 'POST'])
@is_logged_in
def welcome_page():
    email = session['email']
    cur = mysql.connection.cursor()
    cur.execute("SELECT firstname FROM user WHERE emailid = '{_email}'".format(_email = email))
    user = cur.fetchone()
    user = user['firstname']
    print(user)

    return render_template('welcome.html', user = user)




@app.route('/posted_jobs', methods=['GET', 'POST'])
@is_logged_in
def posted_jobs():

    email = session['email']

    cur = mysql.connection.cursor()

    cur.execute("SELECT user_id FROM user WHERE emailid = '{_email}'".format(_email = email))
    user_id = cur.fetchone()
    user_id = user_id['user_id']
    # print(user_id)

    job_data_list = []
    cur.execute("SELECT job_id FROM posted_jobs WHERE user_id='{user_id}'".format(user_id=user_id))
    job_id = cur.fetchall()

    for item in job_id:
        jobs = item['job_id']
        print(jobs)



        cur.execute("SELECT * FROM job_posts WHERE id='{job_id}'".format(job_id=jobs))
        job_data = cur.fetchall()
        job_data_list.append(job_data)

        print("job_data_list:",job_data_list)

    return render_template('posted_jobs.html', job_data=job_data_list)






@app.route('/applied_jobs', methods=['GET', 'POST'])
@is_logged_in
def applied_jobs():

    email = session['email']

    cur = mysql.connection.cursor()

    cur.execute("SELECT user_id FROM user WHERE emailid = '{_email}'".format(_email = email))
    user_id = cur.fetchone()
    user_id = user_id['user_id']
    # print(user_id)

    applied_jobs_data_list = []
    cur.execute("SELECT job_id FROM applied_jobs WHERE user_id='{user_id}'".format(user_id=user_id))
    applied_jobs_id = cur.fetchall()

    for item in applied_jobs_id:
        applied_jobs = item['job_id']
        print('applied_jobs:',applied_jobs)



        cur.execute("SELECT * FROM job_posts INNER JOIN applied_jobs WHERE job_posts.id='{job_id}' AND applied_jobs.user_id='{user_id}' AND applied_jobs.job_id='{job_id}'".format(job_id=applied_jobs, user_id=user_id))
        job_data = cur.fetchall()
        applied_jobs_data_list.append(job_data)

        print("job_data_list:",applied_jobs_data_list)

    if applied_jobs_data_list != "":
        return render_template('applied_jobs.html', job_data=applied_jobs_data_list)
    else:
        print("empity")






@app.route('/view_applications=<id>', methods=['GET', 'POST'])
@is_logged_in
def view_applications(id):

    id = id
    # email = session['email']

    cur = mysql.connection.cursor()

    job_data_list = []
    cur.execute("SELECT user_id FROM applied_jobs WHERE job_id = '{job_id}'".format(job_id = id))
    user_id = cur.fetchall()

    for item in user_id:
        ids = item['user_id']
        print(ids)



        cur.execute("SELECT * FROM profile INNER JOIN user ON profile.user_id=user.user_id INNER JOIN applied_jobs ON profile.user_id=applied_jobs.user_id INNER JOIN job_posts WHERE profile.user_id='{id}' AND applied_jobs.job_id='{job_id}' AND job_posts.id='{job_id}'".format(id=ids, job_id=id))
        job_data = cur.fetchall()
        job_data_list.append(job_data)

        print("job_data_list:",job_data_list)

    return render_template('view_app.html', user_data=job_data_list)





@app.route('/delete_job=<id>', methods=['GET', 'POST'])
@is_logged_in
def delete_job(id):

    id = id
    # email = session['email']

    cur = mysql.connection.cursor()


    cur.execute("DELETE job_posts,posted_jobs FROM job_posts JOIN posted_jobs ON job_posts.id=posted_jobs.job_id WHERE job_posts.id = '{job_id}'".format(job_id = id))
    mysql.connection.commit()

    cur.execute("SELECT job_id FROM applied_jobs WHERE job_id = '{job_id}'".format(job_id = id))
    job_id = cur.fetchone()
    print("job_id:",job_id)
    if job_id != None:
        # WORKS WHEN JOB FOUND IN APPLIED_JOBS TABLE
        # print("exists")
        cur.execute("DELETE FROM applied_jobs WHERE job_id = '{job_id}'".format(job_id = id))

        mysql.connection.commit()

    else:
        # WORKS WHEN JOB "NOT" FOUND IN APPLIED_JOBS TABLE
        print("not exists")


    flash('Job Deleted Successfully','success')
    print('Job Deleted Successfully')


    return redirect('posted_jobs')





@app.route('/delete_applied_job=<id>', methods=['GET', 'POST'])
@is_logged_in
def delete_applied_job(id):

    id = id
    email = session['email']

    cur = mysql.connection.cursor()

    cur.execute("SELECT user_id FROM user WHERE emailid = '{_email}'".format(_email = email))
    user_id = cur.fetchone()
    user_id = user_id['user_id']


    cur.execute("DELETE FROM applied_jobs WHERE job_id = '{job_id}' AND user_id='{user_id}'".format(job_id = id, user_id=user_id))

    mysql.connection.commit()


    flash('Applied Job Deleted Successfully','success')
    print('Applied Job Deleted Successfully')


    return redirect('applied_jobs')







@app.route('/send_email',methods=['POST'])
def send_email():
    try:

        subject = "Appointment for Job Interview"
        FROM_EMAIL_ADDRESS = "cv.ranker.paf@gmail.com"
        to_email = request.form['user_email']
        candidate_name = request.form['user_name']
        company_name = request.form['company_name']
        company_email = request.form['company_email']
        job_title = request.form['job_title']
        msg = "Dear " + candidate_name + " We are pleased to inform you that you have been selected for interview of " + job_title + " at " + company_name + ". \n\nKindly send an acknowledgement email for further information at " + company_email + ". Looking forward to welcome you! \n\n\n\nTHIS IS AN AUTO GENERATED MAIL PLEASE DON'T REPLY AT THIS EMAIL ADDRESS"
        # TO_EMAIL_ADDRESS = "waqar8758@gmail.com"
        print(msg)
        PASSWORD = "PAKistan37"

        server = smtplib.SMTP('smtp.gmail.com:587')
        print("user email  ", to_email)
        server.ehlo()
        server.starttls()
        server.login(FROM_EMAIL_ADDRESS, PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(FROM_EMAIL_ADDRESS, to_email, message)
        server.quit()
        print("Success: Email sent!")
        flash("Email successfully sent to ",candidate_name,"success")
    except:
        print("Something happened.")

    return redirect('posted_jobs')



# class ProfileForm(Form):
#
#     # Skills Form
#     skill = StringField(u'Skill', validators=[validators.input_required()])
#
#
#
# @app.route('/profile', methods=['GET', 'POST'])
# def profile():
#
#     form = ProfileForm(request.form)
#
#     if request.method == 'POST' and form.validate():
#
#         skill = form.skill.data
#
#         cur = mysql.connection.cursor()
#
#         cur.execute("INSERT INTO skills(skill) VALUES(%s)", [skill])
#
#         mysql.connection.commit()
#
#         cur.close()
#
#         flash('Job Post is Submitted. Click Here to view', 'success')
#
#
#     return render_template('profile.html', form = form)

# class EducationForm(Form):
#
#     # company info form
#
#     School = StringField(u'Company Name', validators=[validators.input_required()])
#     Degree = StringField(u'Company Location', validators=[validators.input_required()])
#     FieldOfStudy = StringField(u'Company Description', validators=[validators.input_required()])
#     Grade = EmailField(u'Email', validators=[validators.input_required()])
#     Act_Soc = StringField(u'Contact', validators=[validators.input_required()])
#     _From = StringField(u'Contact', validators=[validators.input_required()])
#     to = StringField(u'Contact', validators=[validators.input_required()])

#















class JobPostForm(Form):

    # company info form

    company_name = StringField(u'Company Name', validators=[validators.input_required()])
    company_loc = StringField(u'Company Location', validators=[validators.input_required()])
    company_desc = StringField(u'Company Description', validators=[validators.input_required()], widget=TextArea())
    company_email = EmailField(u'Email', validators=[validators.input_required()])
    company_contact = StringField(u'Contact', validators=[validators.input_required()])

    # job form

    job_title = StringField(u'Job Title', validators=[validators.input_required()])
    job_loc = StringField(u'Job Location', validators=[validators.input_required()])
    job_desc = StringField(u'Job Description', validators=[validators.input_required()], widget=TextArea())
    job_skill = StringField(u'Skills Required (Separate by comma)', validators=[validators.input_required()])
    job_qual = StringField(u'Qualification Required (Write only highest required Qualification)', validators=[validators.input_required()])
    job_exp = StringField(u'Experience Required (Write year only)', validators=[validators.input_required()])


@app.route('/jobpost', methods=['GET', 'POST'])
@is_logged_in
def jobpost():

    email0 = session['email']
    form = JobPostForm(request.form)
    if request.method == 'POST' and form.validate():

        company_name = form.company_name.data
        company_loc = form.company_loc.data
        company_desc = form.company_desc.data
        company_email = form.company_email.data
        company_contact = form.company_contact.data
        job_title = form.job_title.data
        job_loc = form.job_loc.data
        job_desc = form.job_desc.data
        job_skill = form.job_skill.data
        job_qual = form.job_qual.data
        job_exp = form.job_exp.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO job_posts(company_name, company_loc, company_desc, company_email, company_contact, job_title, job_loc, job_desc, job_skill, job_qual, job_exp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (company_name, company_loc, company_desc, company_email, company_contact, job_title, job_loc, job_desc, job_skill, job_qual, job_exp))

        mysql.connection.commit()

        cur.execute("SELECT id FROM job_posts ORDER BY id DESC LIMIT 1")
        job_id = cur.fetchone()
        job_id = job_id['id']
        print(job_id)



        cur.execute("INSERT INTO posted_jobs (user_id, job_id) SELECT user_id, id FROM user INNER JOIN job_posts WHERE user.emailid='{email}' AND job_posts.id='{id}'".format(email=email0, id=job_id))
        mysql.connection.commit()

        mysql.connection.commit()

        cur.close()

        flash('Job Post is Submitted', 'success')

        # return redirect(url_for('login'))

    return render_template('jobpost.html', form = form)


# @app.route('/findjob')
# @is_logged_in
# def findjob():
#     return render_template('findjob.html')


# def count_jobs():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT COUNT id FROM job_posts")
#     count = cur.fetchall()
#     global users
#     users = list(range(count))
#
# count_jobs()
#
#
# def get_users(offset=0, per_page=10):
#     return users[offset: offset + per_page]


@app.route('/jobs')
# @is_logged_in
def jobs():

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, job_title, company_name, job_desc, job_loc FROM job_posts")
    data = cur.fetchall()
    return render_template('jobs.html', data=data)


@app.route('/job_detail=<id>')
# @is_logged_in
def job_detail(id):

    id = id

    style = ''
    style2 = ''

    if 'logged_in' in session:
        sess = session['logged_in']

    else:
        sess = ''

    # j_id = request.args.get('job_id', 0, type=str)

    # print("job_id ye hai ", j_id)

    if 'logged_in' in session:

        id_from_email = session['email']

        cur = mysql.connection.cursor()

        cur.execute("SELECT user_id FROM user WHERE emailid='{emailid}'".format(emailid=id_from_email))
        data0 = cur.fetchone()
        data0 = data0['user_id']

        cur.execute("SELECT DISTINCT job_id FROM applied_jobs WHERE job_id='{jobid}' AND user_id='{uid}'".format(jobid=id, uid=data0))
        data = cur.fetchone()
        cur.close()

    # print("data ye ha",data)

    # print("id",id)

        if data != None:
            style = "display:none;"

        else:
            style2 = "display:none;"

    else:
        style2 = "display:none;"



    cur = mysql.connection.cursor()
    cur.execute("SELECT id, job_title, company_name, job_desc, job_loc, job_qual, job_exp FROM job_posts WHERE id ={id}".format(id=id))
    data = cur.fetchall()

    cur.execute("SELECT job_skill FROM job_posts WHERE id ={id}".format(id=id))
    data_skills = cur.fetchone()
    data_skills = data_skills['job_skill']
    data_skills = data_skills.split(',')

    print(data_skills)

    return render_template('job_detail.html', data=data, data_skills=data_skills, style=style, style2=style2, sess=sess)



@app.route('/apply', methods=['GET', 'POST'])
# @is_logged_in
def apply():


    if 'logged_in' in session:

        # id = id
        # id = request.form['job_id']
        id = request.args.get('job_id', 0, type=str)
        email0 = session['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO applied_jobs (user_id, job_id) SELECT user_id, id FROM user INNER JOIN job_posts WHERE user.emailid='{email}' AND job_posts.id='{id}'".format(email=email0, id=id))
        mysql.connection.commit()







        # JOB POST MATCH EDUCATION
        cur.execute("SELECT job_qual FROM job_posts WHERE id='{jobid}'".format(jobid = id))
        res = cur.fetchone()
        res = res['job_qual']
        print('jobpost qual:',res)


        cur.execute("SELECT id, data, score FROM edu_data")
        res1 = cur.fetchall()

        # for item in res1:
            # print(item['data'])

        jobpost_match_temp = ''

        for item in res1: #will run until length of data in edu_data

            if res in item['data']:
                jobpost_match_temp = item['data']
                print("jobpost qual found")
            else:
                # jobpost_match_temp = ''
                print('jobpost qual NOT FOUND')


        print('jobpost_match_temp:',jobpost_match_temp)

        job_edu_data_id = ''

        if jobpost_match_temp != '':

            cur.execute("SELECT id, score FROM edu_data WHERE data='{_data}'".format(_data=jobpost_match_temp))
            res2 = cur.fetchone()

            # print("kuch ha bhi ya nahi", res2['id'])

            job_edu_data_id = res2['id']

            # print("result",job_edu_data_id)



        # CV MATCH EDUCATION
        cur.execute("SELECT qual FROM profile WHERE user_id=(SELECT user_id FROM user WHERE emailid='{e_id}')".format(e_id = email0))
        res_user = cur.fetchone()
        print('res_user',res_user)
        res_user = res_user['qual']
        res_user = " ".join(res_user.split())
        # res_user = res_user.replace(" ", "")



        user_match_temp = ''

        for item in res1: #will run until length of data in edu_data

            if res_user in item['data']:
                user_match_temp = item['data']
                # print("found")
            # else:
            #     print('not found')


        # print(user_match_temp)
        user_edu_data_id = ''

        if user_match_temp != '':

            cur.execute("SELECT id, score FROM edu_data WHERE data='{_data}'".format(_data=user_match_temp))
            res2 = cur.fetchone()

            user_edu_data_id = res2['id']

            print("result",user_edu_data_id)
            print("result222",job_edu_data_id)

        temp_rank = 0
        temp_rank_list = []


        if job_edu_data_id == user_edu_data_id:
            temp_rank = res2['score']
            temp_rank_list.append(temp_rank)
            print("temp rank", temp_rank)

        else:
            print("not matched")









        # JOB POST MATCH EXPERIENCE
        cur.execute("SELECT job_exp FROM job_posts WHERE id='{jobid}'".format(jobid = id))
        res_jobpost = cur.fetchone()
        res_jobpost = res_jobpost['job_exp']
        print('exp_jobpost:'+res_jobpost)


        # CV MATCH EXPERIENCE
        cur.execute("SELECT exp FROM profile WHERE user_id=(SELECT user_id FROM user WHERE emailid='{e_id}')".format(e_id = email0))
        res_user = cur.fetchone()
        res_user = res_user['exp']
        sliced = slice(2)
        res_user = res_user[sliced].rstrip()
        print('exp_user:'+res_user)


        try:
            res_jobpost = int(res_jobpost)
            res_user = int(res_user)

            if res_jobpost == res_user:
                temp_rank = 10
                temp_rank_list.append(temp_rank)

            elif res_jobpost <= res_user:
                print("res_jobpost <= res_user:",res_jobpost <= res_user)
                temp_rank = 15
                temp_rank_list.append(temp_rank)


            elif res_jobpost >= res_user:
                temp_rank = 5
                temp_rank_list.append(temp_rank)

            else:
                temp_rank = 0
                temp_rank_list.append(temp_rank)
                print("temp_rank = 0")

        except:
            print("experience not match because string")






        print('Experience temp rank:',temp_rank)















        # JOB POST MATCH SKILLS
        cur.execute("SELECT job_skill FROM job_posts WHERE id='{jobid}'".format(jobid = id))
        res = cur.fetchone()
        res = res['job_skill']
        res = res.split(',')
        print('job_skill:',res)


        cur.execute("SELECT id, data, score FROM skill_data")
        res1 = cur.fetchall()

        for item in res1:
            print(item['data'])

        jobpost_match_temp = ''
        job_edu_data_id = []

        for item in res1: #will run until length of data in skill_data

            for list_item in res: #will run until length of data in job_skill in job_posts table

                print('list item:',list_item)

                if list_item in item['data']:
                    jobpost_match_temp = item['data']
                    print("found")

                    cur.execute("SELECT id, score FROM skill_data WHERE data='{_data}'".format(_data=jobpost_match_temp))

                    res2 = cur.fetchone()

                    print("kuch ha bhi ya nahi", res2['id'])

                    job_edu_data_id.append(res2['id'])


                else:
                    # jobpost_match_temp = ''
                    print('jobpost_match_temp NOT FOUND')

        print("result",job_edu_data_id)
            # print('0jobpost_match_temp:',jobpost_match_temp)



            # if jobpost_match_temp != '':





        # CV MATCH SKILLS
        user_edu_data_id = []


        cur.execute("SELECT skills FROM profile WHERE user_id=(SELECT user_id FROM user WHERE emailid='{e_id}')".format(e_id = email0))
        res_user = cur.fetchone()
        res_user = res_user['skills']
        print("res user before comma remove: " + res_user)
        # res_user = " ".join(res_user.split())
        res_user = res_user.rstrip(",")
        print("res user after comma remove: " + res_user)
        # res_user = res_user.replace(" ", "")
        res_user = res_user.split(',')
        print('res_user',res_user)


        cur.execute("SELECT id, data, score FROM skill_data")
        res1 = cur.fetchall()

        user_match_temp = ''
        temp_rank = 0


        for item in res1: #will run until length of data in skill_data

            for list_item_user_skills in res_user: #will run until length of data in skills in profile table

                print('list_item_user_skills:',list_item_user_skills)
                print("item['data']:", item['data'])

                if list_item_user_skills in item['data']:
                    user_match_temp = item['data']
                    print("found")


                    cur.execute("SELECT id, score FROM skill_data WHERE data='{_data}'".format(_data=user_match_temp))
                    res2 = cur.fetchone()

                    print("score and id:",res2)

                    # if res2 != None:
                    user_edu_data_id.append(res2['id'])


                else:
                    # user_match_temp = ''
                    print('not found')


            print('user_match_temp',user_match_temp)





        print('\nuser_edu_data_id:',user_edu_data_id)
        print('\njob_edu_data_id:',job_edu_data_id)


        # if job_edu_data_id == user_edu_data_id:
        # print(i in job_edu_data_id for i in user_edu_data_id)
        print(set(job_edu_data_id) & set(user_edu_data_id))

        both_ids_list = []

        if (set(job_edu_data_id) & set(user_edu_data_id)):
            # temp_rank += res2['score']
            both_ids = set(job_edu_data_id) & set(user_edu_data_id)

            for id in both_ids:
                cur.execute("SELECT score FROM skill_data WHERE id='{_data}'".format(_data=id))
                both_ids_score = cur.fetchone()
                both_ids_list.append(both_ids_score['score'])

            temp_rank = sum(both_ids_list)
            print("temp rank", temp_rank)
            temp_rank_list.append(temp_rank)

        else:
            print("not matched")

        print("temp_rank_list:",temp_rank_list)
        final_rank = sum(temp_rank_list)
        print("final rank:",final_rank)
        id = request.args.get('job_id', 0, type=str)

        email = session['email']

        # GET USER ID
        cur.execute("SELECT user_id FROM user WHERE emailid = '{_email}'".format(_email = email))
        user_id = cur.fetchone()
        user_id = user_id['user_id']

        cur.execute("UPDATE applied_jobs SET rank='{rank}' WHERE job_id = '{id}' AND user_id='{user_id}'".format(rank=final_rank, id=id, user_id=user_id))
        mysql.connection.commit()
        cur.close()


        return jsonify(result='<div class="alert alert-success">Job Applied</div>')
    else:
        return jsonify(result='<div class="alert alert-danger">Please Login First</div>')
        # return render_template('login.html')







if __name__ == "__main__":
    app.secret_key='abc123'
    app.run(debug=True)