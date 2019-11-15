import os
from cs50 import SQL
from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ideas.db")


@app.route("/")
def index():
    """Show index page"""
    rows = db.execute("SELECT * from ideas")
    return render_template("index.html", data=rows)


@app.route("/ideas", methods=["POST"])
def ideas():
        title = request.form.get("title")
        details = request.form.get("details")
        
        db.execute("INSERT INTO ideas ('title', 'details') VALUES (:title, :details)", title=title, details=details)
        return redirect("/")

         
@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    # DELETE ITEM FROM database WITH ID
    db.execute("DELETE FROM ideas WHERE id = :id", id=id)
    return redirect("/")

 
@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id):
    if request.method == "POST":
        title = request.form.get("title")
        details = request.form.get("details")
        db.execute("UPDATE ideas SET title=:title, details=:details WHERE id= :id",
            title=title, details=details, id=id)
        return redirect("/")
    else:
        data= db.execute("select * FROM ideas WHERE id= :id", id=id)
        return render_template("edit.html", data=data)
 
