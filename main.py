import smtplib
from datetime import datetime
import subprocess

sender = "" # Add your sender's email address here
recipient_list = [
    "" # Add the recipients' email addresses here, separated by commas
]

my_password = "" # Add your application password here

dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
subject = f"Server Report [{dt}]"

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# Run commands and capture the output
usage_of_root = run_command("df -h / | awk 'NR==2 {print $5 \" of \" $2}'")
memory_usage = run_command("free -m | awk '/Mem:/ {printf \"%.0f%%\", $3/$2*100}'")
swap_usage = run_command("free -m | awk '/Swap:/ {printf \"%.0f%%\", $3/$2*100}'")
temperature = run_command("sensors | grep 'Core 0' | awk '{print $3}'")
process_count = run_command("ps aux | wc -l")
users_logged_in = run_command("who | wc -l")

message = f"""\
Subject: {subject}

💽  Root memory (/) → {usage_of_root}
💾  Total memory → {memory_usage}
🔥  Temperature → {temperature} [+82.0°C, +102.0°C]
⚡  Number of processes → {process_count}
🔄  Swap usage → {swap_usage}
👥  Users logged in → {users_logged_in}
"""

# Send the email
for recipient in recipient_list:
    try:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=sender, password=my_password)
            connection.sendmail(
                from_addr=sender,
                to_addrs=recipient,
                msg=message.encode("utf-8") 
            )
    except smtplib.SMTPException:
        print("The email could not be sent")
    else:
        print("The email was sent successfully")
