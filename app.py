from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os
import psycopg2
# import students
from students import studentRoutes
from Admin import adminRoutes
# import nltk
# import numpy as np
# import pandas as pd

# conn = psycopg2.connect('dbname=postgres')
conn = psycopg2.connect('dbname=group_13 user=group_13 password=p0XvR8Ch4BAGb host=10.17.50.232 port=5432')

cur = conn.cursor()

app = Flask(__name__)
app.register_blueprint(studentRoutes)
app.register_blueprint(adminRoutes)
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
COID =""
SN = ""
schedule = []

@app.route("/")  #main webpage rendering
def main():
    return render_template("HomeScreen.html") #the main form

@app.route("/instructorScreen", methods = ["POST"])
def inst():
    global currentProfLoginId
    global schedule
    currentProfLoginId = request.form.get("ProfID")
    TC = ""

    try:
        query1="""
        BEGIN;
        SELECT * from current_term;
        """
        cur.execute(query1)
        TC=cur.fetchall()
        cur.execute("COMMIT;")
        TC=TC[0][0]
    except Exception as e:
        print(e)
        cur.execute("ROLLBACK;")
    # schedule = EXECUTE DATABASE QUERY HERE
    try:
        query="""
        BEGIN;
        SELECT * from get_instructor_schedule(%s,%s);
        """ % (str(currentProfLoginId),str(TC))
        cur.execute(query)
        schedule=cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")
        # try:
        #     query1="""
        #     BEGIN;
        #     SELECT * from current_term;
        #     """
        #     cur.execute(query1)
        #     TC=cur.fetchall()
        #     cur.execute("COMMIT;")
        #     TC=TC[0][0]
        # except Exception as e:
        #     print(e)
        # # schedule = EXECUTE DATABASE QUERY HERE
        # try:
        #     query="""
        #     BEGIN;
        #     SELECT * from get_instructor_schedule(%s,%s);
        #     """ % (str(currentProfLoginId),str(TC))
        #     cur.execute(query)
        #     schedule=cur.fetchall()
        #     cur.execute("COMMIT;")
        # except Exception as e:
        #     print (e)

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = [],addGradeMsg = "", grades = [], room = "", facultyCode = "", schedule = schedule, searchResults=[])

@app.route("/instructorScreen/AddCourse", methods = ["POST"])
def instAC():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    global schedule
    CID = request.form.get("CID")
    TC = ""
    # TC = request.form.get("TC")
    SN = request.form.get("SN")
    LM = request.form.get("LM")
    ST = request.form.get("ST")
    SC = request.form.get("SC")
    RoomReq = request.form.get("RoomReq")

    try:
        query1="""
        BEGIN;
        SELECT * from current_term;
        """
        cur.execute(query1)
        TC=cur.fetchall()
        cur.execute("COMMIT;")
        TC=TC[0][0]
    except Exception as e:
        print(e)
        cur.execute("ROLLBACK;")
    # EXECUTE DATABASE QUERY HERE
    try:
        query="""
        BEGIN;
        SELECT add_course_offering('%s',%s,%s,%s,%s,'%s',%s,'%s');
        COMMIT;
        """ % (str(CID),str(TC),str(SN),str(LM),str(RoomReq),str(ST),str(currentProfLoginId),str(SC))
        cur.execute(query)
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")
    try:
        query="""
        BEGIN;
        SELECT * from get_instructor_schedule(%s,%s);
        """ % (str(currentProfLoginId),str(TC))
        cur.execute(query)
        schedule=cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = [],addGradeMsg = "", grades = [], room = "", facultyCode = "", schedule = schedule, searchResults=[])

@app.route("/instructorScreen/Requests", methods = ["POST"])
def instRequests():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    global schedule
    global COID
    global SN
    COID = request.form.get("COID")
    SN = request.form.get("SN")
    requests = [(0,123),(0,1231),(0,13),(0,144),(0,123),(0,1231),(0,13),(0,144),(0,123),(0,1231),(0,13),(0,144)]


    # requests = EXECUTE DATABASE QUERY HERE
    try:
        query="""
        BEGIN;
        SELECT * from get_pending_requests('%s',%s);
        """ % (str(COID),str(SN))
        cur.execute(query)
        requests = cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")
    # print(requests)

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = requests, enrollment = [],addGradeMsg = "", grades = [], room = "", facultyCode = "", schedule = schedule, searchResults=[])

@app.route("/instructorScreen/ProcessRequests", methods = ["POST"])
def instProcessRequests():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    global schedule
    global COID
    global SN
    studentID = request.form.get("studentID")
    requests = []
    if request.form.get('Accept') == 'Accept':
        # a  = 2 # dummy line
        try:
            query="""
            BEGIN;
            SELECT process_pending_request('%s',%s,%s,%s);
            COMMIT;
            """ % (str(COID),str('true'),str(SN),str(studentID))
            cur.execute(query)
        except Exception as e:
            print (e)
            cur.execute("ROLLBACK;")
    else:
        # a  = 2 # dummy line
        try:
            query="""
            BEGIN;
            SELECT process_pending_request('%s',%s,%s,%s);
            COMMIT;
            """ % (str(COID),str('false'),str(SN),str(studentID))
            cur.execute(query)
        except Exception as e:
            print (e)
            cur.execute("ROLLBACK;")

    # requests = EXECUTE DATABASE QUERY HERE
    try:
        query="""
        BEGIN;
        SELECT * from get_pending_requests('%s',%s);
        """ % (str(COID),str(SN))
        cur.execute(query)
        requests = cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = requests, enrollment = [],addGradeMsg = "", grades = [], room = "", facultyCode = "", schedule = schedule, searchResults=[])




@app.route("/instructorScreen/Schedule", methods = ["POST"])
def instSchedule():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    global schedule
    TC=""
    # TC = request.form.get("TC")
    schedule = []

    try:
        query1="""
        BEGIN;
        SELECT * from current_term;
        """
        cur.execute(query1)
        TC=cur.fetchall()
        cur.execute("COMMIT;")
        TC=TC[0][0]
    except Exception as e:
        print(e)
        cur.execute("ROLLBACK;")
    # schedule = EXECUTE DATABASE QUERY HERE
    try:
        query="""
        BEGIN;
        SELECT * from get_instructor_schedule(%s,%s);
        """ % (str(currentProfLoginId),str(TC))
        cur.execute(query)
        schedule=cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")
    # print(schedule);
    #  Will make schedule.html once query is executed and exact form is known
    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = [],addGradeMsg = "", grades = [], room = "", facultyCode = "", schedule = schedule, searchResults=[])


@app.route("/instructorScreen/enrollment", methods = ["POST"])
def instEnrollments():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    global schedule
    COID = request.form.get("COID")
    SN = request.form.get("SN")
    enrollment = ['Aniket','Aarunish','Jai']

    # enrollment = EXECUTE DATABASE QUERY HERE
    try:
        query="""
        BEGIN;
        SELECT * from get_student_list('%s',%s);
        """ % (str(COID),str(SN))
        cur.execute(query)
        enrollment=cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = enrollment,addGradeMsg = "", grades = [], room = "", facultyCode = "", schedule = schedule, searchResults=[])


@app.route("/instructorScreen/addGradeDistribution", methods = ["POST"])
def instAddGD():
    # See what is to be done with AddCourseMsg
    global currentProfLoginId
    global schedule
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
    try:
        query="""
        BEGIN;
        SELECT set_grade_distribution('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        COMMIT;
        """ % (str(COID),str(SN),str(a),str(ab),str(b),str(bc),str(c),str(d),str(f),str(s),str(u),str(cr),str(n),str(p),str(i),str(nw),str(nr),str(others))
        cur.execute(query)
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")
        addGradeMsg="Error occured while updating"

    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = [],addGradeMsg = addGradeMsg, grades = [], room = "", facultyCode = "", schedule = schedule, searchResults=[])

@app.route("/instructorScreen/getGradeDistribution", methods = ["POST"])
def instGetGD():
    global currentProfLoginId
    global schedule
    grades = [1,2,3,4,5,6,7,7,8,8,34,2,6,42,6634,24,523]
    COID = request.form.get("COID")
    SN = request.form.get("SN")
    # grades = EXECUTE DATABASE QUERY HER
    try:
        query="""
        BEGIN;
        SELECT * from get_grade_distribution('%s',%s);
        """ % (str(COID),str(SN))
        cur.execute(query)
        grades = cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")
    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = [],addGradeMsg = "", grades = grades, room = "", facultyCode = "", schedule = schedule, searchResults=[])

@app.route("/instructorScreen/room", methods = ["POST"])
def instRoom():
    global currentProfLoginId
    global schedule
    COID = request.form.get("COID")
    SN = request.form.get("SN")
    output = [('LH121','Narula101')]
    # output = EXECUTE DATABASE QUERY HERE
    try:
        query="""
        BEGIN;
        SELECT * from get_room_instr('%s',%s);
        """ % (str(COID),str(SN))
        cur.execute(query)
        output=cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")

    room = output[0][0]
    facultyCode = output[0][1]
    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = [],addGradeMsg = "", grades = [], room = room, facultyCode = facultyCode, schedule = schedule, searchResults=[])


@app.route("/instructorScreen/searchCourse", methods = ["POST"])
def instsearchCourse():
    global currentProfLoginId
    global schedule
    CName = request.form.get("CName")
    searchResults = [(1,"course A"), (2,"Course B"),(1,"course A"), (2,"Course B"),(1,"course A"), (2,"Course B")]
    #  searchResults = EXECUTE DATABASE QUERY HERE
    try:
        query="""
        BEGIN;
        SELECT * from search_course_instructor('%s');
        """ % (str(CName))
        cur.execute(query)
        searchResults=cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print (e)
        cur.execute("ROLLBACK;")
    return render_template("instructor.html",currentProfLoginId = currentProfLoginId,AddCourseMsg="", requests = [], enrollment = [],addGradeMsg = "", grades = [], room = "", facultyCode = "", schedule = schedule, searchResults=searchResults)




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5013)
