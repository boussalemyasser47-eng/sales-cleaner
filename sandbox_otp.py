import random
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Gmail OTP Authenticator", page_icon="📧", layout="centered")

st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📧 نظام التحقق عبر بريد Gmail (إيميلات عشوائية)")
st.write("أدخل أي بريد إلكتروني في العالم، وسيقوم النظام بإرسال رمز التحقق إليه فوراً مجاناً.")

if "otp_code" not in st.session_state:
    st.session_state.otp_code = None

if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

# حقل إدخال أي بريد إلكتروني عشوائي
target_email = st.text_input("أدخل البريد الإلكتروني المستهدف لأي شخص:")

if st.button("📧 إرسال رمز التحقق"):
    if not target_email or "@" not in target_email:
        st.error("الرجاء إدخال بريد إلكتروني صحيح.")
    else:
        # توليد رمز عشوائي مكون من 6 أرقام
        code = f"{random.randint(100000, 999999)}"
        st.session_state.otp_code = code

        # جلب بيانات Gmail الآمنة من الـ Secrets
        sender_email = st.secrets["GMAIL_USER"]
        sender_password = st.secrets["GMAIL_APP_PASSWORD"]

        # إعداد محتوى الرسالة يدعم اللغة العربية تماماً
        message = MIMEMultipart("alternative")
        message["Subject"] = "رمز التحقق الخاص بك (OTP)"
        message["From"] = sender_email
        message["To"] = target_email

        text_content = f"مرحباً،\n\nرمز التحقق العشوائي الخاص بك هو: {code}\n\nيرجى إدخاله في التطبيق لإتمام العملية."
        message.attach(MIMEText(text_content, "plain", "utf-8"))

        try:
            # الاتصال بخادم Gmail SMTP الآمن عبر البورت 587
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()  # تأمين الاتصال
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, target_email, message.as_string())
            server.quit()

            st.session_state.email_sent = True
            st.success(f"تم إرسال الرمز بنجاح إلى البريد: {target_email} 📬")
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء الإرسال عبر Gmail: {e}")

if st.session_state.email_sent:
    st.markdown("---")
    user_input_code = st.text_input("أدخل الرمز الذي استقبله المستخدم للتحقق:")
    if st.button("التحقق من صحة الرمز"):
        if user_input_code.strip() == st.session_state.otp_code:
            st.success("🎉 الرمز صحيح 100% وتم التحقق بنجاح!")
        else:
            st.error("❌ الرمز غير صحيح، حاول مرة أخرى.")
