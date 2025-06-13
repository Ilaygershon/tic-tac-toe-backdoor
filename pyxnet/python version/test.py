import subprocess
import threading


def run_tunnel():
    response = subprocess.Popen(
        ["ssh", "-R", "80:127.0.0.1:5000", "serveo.net"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    for line in response.stdout:
        if "http" in line:
            url = line.split(" ")[-1]


if __name__ == '__main__':
    response = run_tunnel()
