import os
import base64


from flask import Flask, request, session
from model import Grade


app = Flask(__name__)

app.secret_key = os.urandom(16)


@app.route('/', methods=['GET', 'POST'])
def home():

    if 'csrftoken' not in session:
        session['csrftoken'] = app.secret_key

    if request.method == 'POST':

        if str(request.form.get('_csrf_token', None)) == str(app.secret_key):
            g = Grade(
                student=request.form['student'],
                assignment=request.form['assignment'],
                grade=request.form['grade'],
            )
            g.save()

    body = """
<html>
<body>
<h1>Enter Grades</h1>
<h2>Enter a Grade</h2>
<form method="POST">
    <input name=_csrf_token type="hidden" value="{}">

    <label for="student">Student</label>
    <input type="text" name="student"><br>


    <label for="assignment">Assignment</label>
    <input type="text" name="assignment"><br>

    <label for="grade">Grade</label>
    <input type="text" name="grade"><br>

    <input type="submit" value="Submit">
</form>

<h2>Existing Grades</h2>
""".format(session['csrftoken'])

    for g in Grade.select():
        body += """
<div class="grade">
{}, {}: {}
</div>
""".format(g.student,
           g.assignment,
           g.grade)

    return body


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6779))
    app.run(host='0.0.0.0', port=port)
