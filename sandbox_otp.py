import random
import streamlit as st
import resend

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
st.write("ملف تجريبي معزول لإرسال الرموز بسلاسة عبر الإنترنت باستخدام Resend API.")

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

        # ربط مفتاح الـ API الخاص بك الذي استخرجته للتو
        resend.api_key = "re_867ocWMe_5ZoorUd4y7P2trxRmxoKGXQm"

        try:
            params = {
                "from": "onboarding@resend.dev",
                "to": [target_email],
                "subject": "رمز التحقق التجريبي الخاص بك",
                "text": f"مرحباً،\n\nرمز التحقق العشوائي الخاص بك هو: {code}\n\nيرجى إدخاله في الموقع لإتمام الاختبار.",
            }
            
            email = resend.Emails.send(params)
            st.session_state.email_sent = True
            st.success("تم إرسال رمز التحقق بنجاح إلى البريد الإلكتروني عبر السحاب! تحقق من صندوق الوارد.")
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
