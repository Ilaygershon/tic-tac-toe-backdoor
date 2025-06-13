import os
import time

mail = input("Enter your mail\n--> ")
with open("mail_sender.py", "r+") as f:
    lines = f.read().split("\n")
    lines[7] = f'        self.mail = "{mail}"'

with open("mail_sender.py", "w") as f:
    for line in lines:
        f.write(line + "\n")

print("mail added successfully")
print("\nconvert the file to exe with pyinstaller...")
time.sleep(3)
os.system("exe_conventor.bat")