from flask import Blueprint, Flask, render_template, send_from_directory, request, redirect, url_for
import os
import psycopg2

adminRoutes = Blueprint('adminRoutes',__name__,template_folder='templates',
    static_folder='static')

@adminRoutes.route("/adminScreen", methods = ["POST"])
def adminMain():
    return render_template("Admin.html", StartMsg = "", endMsg="", checkMsg = "", addMsg = "", addStudentMsg = "")


@adminRoutes.route("/adminScreen/startAddDrop", methods = ["POST"])
def adminStartAddDrop():
    TC = request.form.get("TC")
    startMsg = "Add Drop Started"

    # startMsg = EXECUTE QUERY HERE

    return render_template("Admin.html",startMsg = startMsg, endMsg="", checkMsg = "", addMsg = "", addStudentMsg = "")


@adminRoutes.route("/adminScreen/endAddDrop", methods = ["POST"])
def adminEndAddDrop():
    TC = request.form.get("TC")
    endMsg = "Add Drop Ended"

    # endMsg = EXECUTE QUERY HERE

    return render_template("Admin.html",startMsg = "", endMsg=endMsg, checkMsg = "", addMsg = "", addStudentMsg = "")


@adminRoutes.route("/adminScreen/isAddDropOn", methods = ["POST"])
def adminIsAddDropOn():
    TC = request.form.get("TC")
    checkMsg = "Add Drop is not on"

    # checkMsg = EXECUTE QUERY HERE

    return render_template("Admin.html",startMsg = "", endMsg="", checkMsg = checkMsg, addMsg = "", addStudentMsg = "")


@adminRoutes.route("/adminScreen/addNewCourse", methods = ["POST"])
def adminaddCourse():
    CID = request.form.get("CID") # course id
    CN = request.form.get("CN") # course name
    addMsg = "Course Added"

    # addMsg = EXECUTE QUERY HERE

    return render_template("Admin.html",startMsg = "", endMsg="", checkMsg = "", addMsg = addMsg, addStudentMsg = "")


@adminRoutes.route("/adminScreen/addNewStudent", methods = ["POST"])
def adminaddStudent():
    SID = request.form.get("SID")  # student ID
    SN = request.form.get("SN")  # student name
    addStudentMsg = "Student Added"

    # addStudentMsg = EXECUTE QUERY HERE

    return render_template("Admin.html",startMsg = "", endMsg="", checkMsg = "", addMsg = "", addStudentMsg = addStudentMsg)