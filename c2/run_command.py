import sys
import re
import subprocess
import os


def set_message(message):
    file_lines = [line for line in open('cookie.txt', 'r')]
    with open('cookie.txt', 'w') as out:
        for line in file_lines:
            line = re.sub(r'secret_message.*',
                          r"secret_message\t\"{message}\"", line)
            out.write(line)


def send_message():
    command = ["curl", "-b", "cookie.txt", "-c", "cookie.txt", "-d",
               "user_id=1000", "--location", "http://localhost:5000/signin"]
    devnull = open(os.devnull, 'w')
    subprocess.call(command, stdout=devnull, stderr=devnull)


def read_message():
    for line in open('cookie.txt', 'r'):
        matches = re.findall(r'secret_message.*"(.*)"', line)
        if len(matches):
            return matches[0]


def clean_message(message):
    message = message.replace("\\\\n", "\n")
    message = message.replace("b'", "")
    message = message[:-1]
    return message


if __name__ == '__main__':
    arguments = sys.argv[1:]

    message = ""
    for arg in arguments:
        message += arg + " "

    set_message(message)

    send_message()
    response = read_message()
    print()
    print(clean_message(response))
