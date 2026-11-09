import random
import streamlit as st
import requests

st.set_page_config(page_title="OTP Sandbox Cloud", page_icon="📧", layout="centered")

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

st.title("📧 فحص واختبار رموز التحقق (عبر السحاب)")
st.write("ملف تجريبي معزول لإرسال الرموز بسلاسة عبر الإنترنت باستخدام Resend API المباشر.")

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

        # جلب المفتاح بأمان من إعدادات الـ Secrets
        api_key = st.secrets["RESEND_API_KEY"]

        # إعداد الاتصال المباشر عبر HTTP لمنع مشاكل الترميز (latin-1) نهائياً
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "from": "onboarding@resend.dev",
            "to": [target_email],
            "subject": "Your OTP Verification Code",
            "text": f"مرحباً،\n\nرمز التحقق العشوائي الخاص بك هو: {code}\n\nيرجى إدخاله في الموقع لإتمام الاختبار."
        }

        try:
            response = requests.post("https://api.resend.com/emails", json=payload, headers=headers)
            
            if response.status_code == 200:
                st.session_state.email_sent = True
                st.success("تم إرسال رمز التحقق بنجاح إلى البريد الإلكتروني عبر السحاب! تحقق من صندوق الوارد.")
            else:
                st.error(f"خطأ من خادم Resend: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"حدث خطأ أثناء الإرسال السحابي: {e}")

if st.session_state.email_sent:
    st.markdown("---")
    user_input_code = st.text_input("أدخل الرمز الذي استقبلته للتحقق:")
    if st.button("تحقق من صحة الرمز"):
        if user_input_code.strip() == st.session_state.otp_code:
            st.success("الرمز صحيح 100% وتم تأكيد الاختبار بنجاح!")
        else:
            st.error("الرمز غير صحيح، حاول مرة أخرى.")
