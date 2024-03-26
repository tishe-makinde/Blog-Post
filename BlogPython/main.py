from flask import Flask, render_template, request
import requests
import smtplib as smt
import time

posts = requests.get("https://api.npoint.io/9bb3f7fded80f3fd83cd").json()
my_email = "*********@gmail.com"
my_password = "******"

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        number = request.form["number"]
        message = request.form["message"]
        returned_message = "Successfully sent message!"
        with smt.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=email,
                                to_addrs=my_email,
                                msg=f"\n\nName: {username}\n\nNumber: {number}\n\n Email: {email}\n\n Message: {message}")
        return render_template("contact.html", success=returned_message)
    else:
        returned_message = "Contact Me"
        return render_template("contact.html",  success=returned_message)



# @app.route("/form-entry", methods=["POST"])
# def receive_data():
#     username = request.form["username"]
#     email = request.form["email"]
#     number = request.form["number"]
#     message = request.form["message"]
#     print(username)
#     print(email)
#     print(number)
#     print(message)
#     return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
