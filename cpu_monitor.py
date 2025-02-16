import psutil
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Define system processes (Example: adjust according to your system)
system_processes = ['System', 'smss.exe', 'wininit.exe', 'services.exe', 'lsass.exe', 'svchost.exe']

# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'rohit2024cs@gmail.com'
receiver_email = 'itz4rohit@gmail.com'
password = 'nxsr oocw suli ytfl'

def send_email(subject, body):
    """ Send email function """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def restart_process(process_name):
    """ Restart the application process if it's an application """
    try:
        print(f"Restarting {process_name}")
        os.system(f"taskkill /f /im {process_name}")
        time.sleep(2)  # Wait for process to terminate
        os.system(f"{process_name}")  # Restart process (assuming it is in the PATH)
    except Exception as e:
        print(f"Error restarting {process_name}: {e}")

def kill_process(process_name):
    """ Kill any other processes that are not system/application """
    try:
        print(f"Killing process {process_name}")
        os.system(f"taskkill /f /im {process_name}")
    except Exception as e:
        print(f"Error killing {process_name}: {e}")

def monitor_cpu():
    """ Monitor CPU and check process usage """
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"CPU Utilization: {cpu_percent}%")
        
        if cpu_percent > 10:  # If CPU usage goes beyond 60%
            # Get all processes sorted by CPU usage
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] > 60:  # If the process is using more than 10% CPU
                        process_name = proc.info['name']
                        pid = proc.info['pid']
                        cpu_usage = proc.info['cpu_percent']

                        print(f"Process: {process_name}, PID: {pid}, CPU Usage: {cpu_usage}%")

                        if process_name in system_processes:
                            send_email(f"High CPU Alert: {process_name}", f"The system process {process_name} is using {cpu_usage}% CPU.")
                        elif process_name != 'python.exe':  # Restart only non-system, non-Python processes
                            restart_process(process_name)
                            send_email(f"High CPU Alert: {process_name}", f"The system process {process_name} is using {cpu_usage}% CPU.")
                        else:
                            kill_process(process_name)
                            send_email(f"High CPU Alert: {process_name}", f"The system process {process_name} is using {cpu_usage}% CPU.")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        time.sleep(5)  # Sleep for a while before checking again

if __name__ == '__main__':
    monitor_cpu()


