from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os
import psycopg2
# import nltk
import numpy as np
# import pandas as pd

conn = psycopg2.connect('dbname=postgres')

cur = conn.cursor()

app = Flask(__name__)
# app['debug'] = True

# UPLOAD_FOLDER ='./uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# CONFIG_FOLDER ='./config/'
# app.config['CONFIG_FOLDER'] = CONFIG_FOLDER
# PDF_FOLDER ='./pdfs/'
# app.config['PDF_FOLDER'] = PDF_FOLDER
# app.config['TMP'] = './tmp/'
currentStudentLoginId = ""  # the student who is currently logged in
currentProfLoginId = ""     # # the instructor who is currently logged in

@app.route("/")  #main webpage rendering
def main():
    return render_template("HomeScreen.html") #the main form

@app.route("/instructorScreen", methods = ["POST"])
def inst():
    global currentProfLoginId
    currentProfLoginId = request.form.get("ProfID")
    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = [],addGradeMsg = addGradeMsg, grades = [], room = "", facultyCode = "")

@app.route("/instructorScreen/AddCourse", methods = ["POST"])
def instAC():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    CID = request.form.get("CID")
    TC = request.form.get("TC")
    SN = request.form.get("SN")
    LM = request.form.get("LM")
    ST = request.form.get("ST")
    RoomReq = request.form.get("RoomReq")

    # EXECUTE DATABASE QUERY HERE
    try:
        query = "SELECT * from add_course_offering('%s',%s,%s,%s,%s,'%s',%s);" % (str(CID),str(TC),str(SN),str(LM),str(RoomReq),str(ST),str(currentProfLoginId))
        cur.execute(query)
    except Exception as e:
        print (e)

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = [],addGradeMsg = addGradeMsg, grades = [], room = "", facultyCode = "")

@app.route("/instructorScreen/Requests", methods = ["POST"])
def instRequests():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    COID = request.form.get("COID")
    # requests = [123,1231,13,144]

    # requests = EXECUTE DATABASE QUERY HERE
    try:
        query="SELECT * from get_pending_requests('%s');" % (str(COID))
        cur.execute(query)
        requests = cur.fetchall()
    except Exception as e:
        print (e)

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = requests, enrollment = [],addGradeMsg = addGradeMsg, grades = [], room = "", facultyCode = "")

@app.route("/instructorScreen/ProcessRequests", methods = ["POST"])
def instProcessRequests():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    COID = request.form.get("COID")
    requests = []

    # requests = EXECUTE DATABASE QUERY HERE

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = [],addGradeMsg = addGradeMsg, grades = [], room = "", facultyCode = "")

@app.route("/instructorScreen/Schedule", methods = ["POST"])
def instSchedule():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    TC = request.form.get("TC")
    schedule = []

    # schedule = EXECUTE DATABASE QUERY HERE
    try:
        query="SELECT * from get_instructor_schedule(%s,%s);" % (str(currentProfLoginId),str(TC))
        cur.execute(query)
        schedule=cur.fetchall()
    except Exception as e:
        print (e)
    #  Will make schedule.html once query is executed and exact form is known
    return render_template("schedule.html",currentProfLoginId = currentProfLoginId,schedule = schedule)

@app.route("/instructorScreen/enrollment", methods = ["POST"])
def instEnrollments():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    COID = request.form.get("COID")
    enrollment = ['Aniket','Aarunish','Jai']

    # enrollment = EXECUTE DATABASE QUERY HERE
    try:
        query="SELECT * from get_student_list('%s');" % (str(COID))
        cur.execute(query)
        enrollment=cur.fetchall()
    except Exception as e:
        print (e)

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = enrollment,addGradeMsg = addGradeMsg, grades = [], room = "", facultyCode = "")


@app.route("/instructorScreen/addGradeDistribution", methods = ["POST"])
def instAddGD():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    COID = request.form.get("COID")
    SN = request.form.get("SN")
    a = request.form.get("a")
    ab = request.form.get("ab")
    b = request.form.get("b")
    bc = request.form.get("bc")
    c = request.form.get("c")
    d = request.form.get("d")
    f = request.form.get("f")
    s = request.form.get("s")
    u = request.form.get("u")
    cr = request.form.get("cr")
    n = request.form.get("n")
    p = request.form.get("p")
    i = request.form.get("i")
    nw = request.form.get("nw")
    nr = request.form.get("nr")
    others = request.form.get("others")
    addGradeMsg = "Grade Distribution Updated"

    # addGradeMsg = EXECUTE DATABASE QUERY HERE

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = enrollment,addGradeMsg = addGradeMsg, grades = [], room = "", facultyCode = "")

@app.route("/instructorScreen/getGradeDistribution", methods = ["POST"])
def instGetGD():
    global currentProfLoginId
    grades = []
    # grades = EXECUTE DATABASE QUERY HERE
    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = enrollment,addGradeMsg = addGradeMsg, grades = grades, room = "", facultyCode = "")

@app.route("/instructorScreen/room", methods = ["POST"])
def instRoom():
    global currentProfLoginId
    ouput = []
    # output = EXECUTE DATABASE QUERY HERE
    room = output[0][0]
    facultyCode = output[0][1]
    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = enrollment,addGradeMsg = addGradeMsg, grades = grades, room = room, facultyCode = facultyCode)



if __name__ == '__main__':
    app.run()
