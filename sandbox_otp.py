import random
import smtplib
from email.mime.text import MIMEText
import streamlit as st

st.set_page_config(page_title="OTP Sandbox", page_icon="📧", layout="centered")

st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #00bcd4;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0097a7;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📧 فحص واختبار رموز التحقق العشوائية")
st.write("ملف تجريبي معزول لفحص إرسال الرموز عبر بريد Gmail.")

if "otp_code" not in st.session_state:
  st.session_state.otp_code = None

if "email_sent" not in st.session_state:
  st.session_state.email_sent = False

target_email = st.text_input("البريد الإلكتروني للهدف (target_email):")

if st.button("📧 إرسال رمز التحقق العشوائي"):
  if not target_email or "@" not in target_email:
    st.error("الرجاء إدخال بريد إلكتروني صحيح.")
  else:
    code = f"{random.randint(100000, 999999)}"
    st.session_state.otp_code = code

    sender_email = "boussalemyasser47@gmail.com"
    sender_password = "cfcq hctz ehjw eazg"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # التبديل إلى المنفذ 587 مع STARTTLS

    subject = "رمز التحقق التجريبي الخاص بك"
    body = (
        f"مرحباً،\n\nرمز التحقق العشوائي الخاص بك هو:"
        f" {code}\n\nيرجى إدخاله في الموقع لإتمام الاختبار."
    )

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = target_email

    try:
      with smtplib.SMTP(smtp_server, smtp_port, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, target_email, msg.as_string())

      st.session_state.email_sent = True
      st.success(
          "تم إرسال رمز التحقق بنجاح إلى البريد الإلكتروني! تحقق من صندوق الوارد"
          " أو البريد المزعج (Spam)."
      )
    except Exception as e:
      st.error(
          f"فشل الاتصال: {e}\n\n💡 **ملاحظة حاسمة:** إذا استمر هذا الخطأ على"
          " المنصة السحابية، فهذا يعني أن الاستضافة تحظر منافذ الـ SMTP بالكامل."
          " الحل النهائي هو تشغيل التطبيق محلياً على حاسوبك عبر (streamlit run"
          " sandbox_otp.py) وسيعمل البريد فوراً وبدون أي أخطاء."
      )

if st.session_state.email_sent:
  st.markdown("---")
  user_input_code = st.text_input("أدخل الرمز الذي استقبلته للتحقق:")
  if st.button("تحقق من صحة الرمز"):
    if user_input_code.strip() == st.session_state.otp_code:
      st.success("الرمز صحيح 100% وتم تأكيد الاختبار بنجاح!")
    else:
      st.error("الرمز غير صحيح، حاول مرة أخرى.")
