import schedule
import time
import os


def push_to_github():
    os.chdir(os.getcwd())
    os.system("git add .")

    os.system("git commit -m 'Automated commit'")
    os.system("git push origin master")

schedule.every().hour.do(push_to_github)

while True:
    schedule.run_pending()
    time.sleep(1)
