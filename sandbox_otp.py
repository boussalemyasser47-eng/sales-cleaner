import random
import streamlit as st
import requests

st.set_page_config(page_title="OTP Verification App", page_icon="📧", layout="centered")

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

st.title("📧 نظام التحقق عبر رموز الـ OTP")
st.write("أدخل البريد الإلكتروني لأي مستخدم ليصلك رمز التحقق الخاص به فوراً.")

if "otp_code" not in st.session_state:
    st.session_state.otp_code = None

if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

# حقل إدخال البريد الإلكتروني لأي مستخدم
target_email = st.text_input("أدخل البريد الإلكتروني المستهدف:")

if st.button("📧 إرسال رمز التحقق العشوائي"):
    if not target_email or "@" not in target_email:
        st.error("الرجاء إدخال بريد إلكتروني صحيح.")
    else:
        # توليد رمز عشوائي مكون من 6 أرقام
        code = f"{random.randint(100000, 999999)}"
        st.session_state.otp_code = code

        # جلب المفتاح بأمان من أسرار المنصة
        api_key = st.secrets["RESEND_API_KEY"]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "from": "onboarding@resend.dev",
            "to": [target_email],
            "subject": "Your OTP Verification Code",
            "text": f"مرحباً،\n\nرمز التحقق العشوائي الخاص بك هو: {code}\n\nيرجى إدخاله في الموقع لإتمام عملية التحقق."
        }

        try:
            response = requests.post("https://api.resend.com/emails", json=payload, headers=headers)
            
            if response.status_code == 200:
                st.session_state.email_sent = True
                st.success(f"تم إرسال الرمز بنجاح إلى البريد: {target_email} 📬")
            else:
                st.error(f"خطأ من خادم البريد: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"حدث خطأ أثناء الإرسال: {e}")

if st.session_state.email_sent:
    st.markdown("---")
    user_input_code = st.text_input("أدخل الرمز الذي استقبلته للتحقق:")
    if st.button("التحقق من صحة الرمز"):
        if user_input_code.strip() == st.session_state.otp_code:
            st.success("🎉 الرمز صحيح 100% وتم التحقق بنجاح!")
        else:
            st.error("❌ الرمز غير صحيح، حاول مرة أخرى.")
