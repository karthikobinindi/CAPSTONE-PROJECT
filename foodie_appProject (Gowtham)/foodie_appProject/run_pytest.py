import os
import datetime
import subprocess

# Ensure reports folder exists
os.makedirs("reports", exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

report_file = f"reports/pytest_{timestamp}.html"

print("Running Pytest with logging...")

subprocess.run([
    "pytest",
    "tests",
    f"--html={report_file}",
    "--self-contained-html"
])

print(f"\nReport generated: {report_file}")
print("Log file: reports/pytest.log")