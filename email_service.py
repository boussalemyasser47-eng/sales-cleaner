import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp_email(target_email, generated_otp):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    server_user = "boussalemyasser47@gmail.com"
    server_pass = "cfcq hctz ehjw eazg"
    
    msg = MIMEMultipart()
    msg["Subject"] = f"🔒 رمز التحقق السري الخاص بك: {generated_otp}"
    msg["From"] = server_user
    msg["To"] = target_email
    
    body = f"رمز التوثيق السري الخاص بإنشاء متجرك هو: {generated_otp}\nيرجى إدخاله لإتمام التسجيل."
    msg.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
        server.login(server_user, server_pass)
        server.sendmail(server_user, target_email, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False
