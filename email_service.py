import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp_email(target_email, generated_otp):
    """
    تشغيل خادم بايثون الداخلي المستقل والمباشر للاتصال بجوجل
    وتخطي كافة جدران الحظر الخارجية لإرسال الرمز العشوائي لبريد التاجر فوراً.
    """
    # تجميع الرابط الموثق لخادم جوجل بدون أخطاء مطبعية
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    
    # مفاتيح السيادة والربط السحابي الخاصة بجهازك الموثق
    server_user = "boussalemyasser47@gmail.com"
    server_pass = "cfcq hctz ehjw eazg"
    
    msg = MIMEMultipart()
    msg["Subject"] = f"🔒 رمز التحقق السري الخاص بك: {generated_otp}"
    msg["From"] = f"NEXUS GATE <{server_user}>"
    msg["To"] = target_email
    
    body = f"مرحباً بك في المنصة السحابية.\n\nرمز التوثيق العشوائي السري الخاص بإنشاء متجرك الإلكتروني هو: {generated_otp}\n\nيرجى إدخاله في الموقع لإتمام التسجيل الآمن."
    msg.attach(MIMEText(body, "plain", "utf-8"))
    
    try:
        # إطلاق اتصال نقي ومشفر عبر منفذ SSL المباشر لحماية السيرفر
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=15)
        server.login(server_user, server_pass)
        server.sendmail(server_user, target_email, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False
