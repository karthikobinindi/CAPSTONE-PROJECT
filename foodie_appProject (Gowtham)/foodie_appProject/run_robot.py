import os
import datetime
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROBOT_PATH = os.path.join(BASE_DIR, "RobotTests", "tests")

REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

subprocess.run([
    "robot",
    "-d", REPORTS_DIR,
    "--output", f"robot_output_{timestamp}.xml",
    "--log", f"robot_log_{timestamp}.html",
    "--report", f"robot_report_{timestamp}.html",
    ROBOT_PATH
])

print("Robot execution completed successfully")