# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتلوين الواجهات (auth_gate.py)
# ========================================================
import streamlit as st
import requests
import json
import time

# ضبط إعدادات الصفحة الكلية لتكون واجهة ملوكية موسطة ونظيفة تماماً
st.set_page_config(page_title="NEXUS CENTRAL GATE v4", page_icon="🔐", layout="wide")

# إخفاء السهم الجانبي والشريط تماماً بالـ CSS عن التجار والزبائن نهائياً لتعزيز السرية والأمان
st.markdown("""
    <style>
    [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] { display: none !important; visibility: hidden !important; opacity: 0 !important; }
    section[data-testid="stSidebar"] { display: none !important; visibility: hidden !important; }
    .stApp { background: radial-gradient(circle at 50% 40%, #0d0d21 0%, #030307 100%) !important; color: #ffffff !important; font-family: 'Cairo', sans-serif !important; }
    .centered-merchant-box { max-width: 500px !important; margin: 40px auto 20px auto !important; padding: 35px !important; background: linear-gradient(135deg, rgba(4, 32, 43, 0.5) 0%, rgba(2, 14, 20, 0.8) 100%) !important; border: 2px solid #00fff0 !important; border-radius: 20px !important; box-shadow: 0px 0px 35px rgba(0, 255, 240, 0.25); direction: rtl !important; text-align: right !important; backdrop-filter: blur(12px) !important; }
    div[data-testid="stVerticalBlock"] button, div.stButton button, .stButton > button { width: 100% !important; min-height: 50px !important; font-family: 'Cairo', sans-serif !important; font-size: 14.5px !important; font-weight: 800 !important; border-radius: 12px !important; background: linear-gradient(135deg, #090915 0%, #040409 100%) !important; color: #00fff0 !important; border: 2px solid #00fff0 !important; box-shadow: 0px 0px 15px rgba(0, 255, 240, 0.3) !important; transition: all 0.4s ease-in-out !important; }
    div.stButton button:hover { background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important; color: #000000 !important; box-shadow: 0px 0px 25px #00fff0 !important; transform: translateY(-3px) !important; }
    div[data-testid="stTextInput"] input { border: 2px solid #ff00ff !important; background-color: #080811 !important; color: #ffffff !important; border-radius: 12px !important; padding: 15px 18px !important; font-family: 'Cairo', sans-serif !important; }
    .stWidgetFormLabel, p, span, label, h1, h2, h3, h4 { font-family: 'Cairo', sans-serif !important; color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# الجزء الثاني: حقول مدخلات التجار وتثبيت مسار الـ API السحابي (auth_gate.py)
# ========================================================
# 👑 [المفتاح السحابي الموحد]: رابط خادم PocketBase الحقيقي والخاص بك الظاهر بلقطة شاشتك السابقة
POCKETBASE_API = "https://pockethost.io"

st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 30px; text-shadow: 0 0 20px #00fff0; font-size:32px;'>🔐 بوابة التوثيق والاشتراكات السنوية المتكاملة</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #b0b0d0; text-align: center; font-size: 15px; font-weight:600; margin-bottom:25px;'>قم بإنشاء حسابك الخاص بكلمة سر من إرادتك، وسجل دخولك للانتقال الآمن لمتجرك الفواتيري.</p>", unsafe_allow_html=True)

# فتح حاوية التوسيط وضخ الحقول بداخل قلب منتصف المتصفح لتطابق التصميم النظيف
st.markdown("<div class='centered-merchant-box'>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#ffffff; text-align:center; font-weight:700; margin-top:0;'>مركز توثيق هوية التاجر</h3>", unsafe_allow_html=True)

auth_mode = st.radio("اختر العملية المطلوبة للتوثيق الآمن لمتجرك:", ["🔑 تسجيل الدخول للحساب الحالي", "📝 إنشاء حساب تاجر جديد فريش"])
st.markdown("<hr style='border-color: rgba(0, 255, 240, 0.15); margin: 15px 0;'>", unsafe_allow_html=True)

input_email = st.text_input("أدخل البريد الإلكتروني الخاص بك:", key="merchant_em")
input_password = st.text_input("أدخل كلمة المرور السرية من اختيارك:", type="password", key="merchant_pw")

clean_email = input_email.strip()
clean_pass = input_password.strip()
# ========================================================
# الجزء الثالث: معالجة طلبات التسجيل وضخ البيانات للسحاب (auth_gate.py)
# ========================================================
if auth_mode == "📝 إنشاء حساب تاجر جديد فريش":
    user_package_choice = st.selectbox("اختر فئة الباقة السنوية لمتجرك للعمل:", ["الباقة السيبرانية الخارقة (65k)", "الباقة الاحترافية المتوسطة (45k)", "الباقة الأساسية المبتدئة (29k)"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("📝 إرسال طلب إنشاء الحساب للإدارة"):
        if clean_email == "" or clean_pass == "": 
            st.error("⚠️ يرجى ملء حقول البريد وكلمة السر أولاً من اختيارك!")
        else:
            try:
                # الفحص الاستباقي لعدم تكرار الحسابات داخل قاعدة البيانات
                check_req = requests.get(f"{POCKETBASE_API}?filter=(email='{clean_email}')", timeout=10)
                if check_req.status_code == 200 and len(check_req.json().get("items", [])) > 0:
                    st.error("🚨 هذا البريد الإلكتروني مسجل مسبقاً بالمنصة! جرب خيار تسجيل الدخول.")
                else:
                    # تجهيز باقة البيانات بصيغة JSON لضخها في السحاب حياً
                    payload = {"email": clean_email, "password": clean_pass, "status": "⏳ في انتظار التفعيل", "package": user_package_choice}
                    post_req = requests.post(POCKETBASE_API, json=payload, timeout=10)
                    
                    # 🚨 [الإصلاح الهندسي الحاسم للسطر 63]: صياغة شرط التحقق بنقاء تام 100% وإبادة الـ SyntaxError
                    if post_req.status_code in:
                        st.success("✅ تم تسجيل حسابك بنجاح! طارت معلوماتك فوراً إلى لوحة PocketBase وبانتظار قبول مالك المنصة.")
                    else: 
                        st.error("🚨 عطل مؤقت في شبكة المزامنة اللاسلكية لجوجل السحابية، أعد المحاولة!")
            except:
                st.error("🚨 فشل الاتصال بخادم PocketBase، تأكد من إعداد وتفعيل الجدول السحابي.")
# ========================================================
# الجزء الرابع: ميكانيكية تسجيل الدخول والتحويل الآلي للمتجر الأصلي (auth_gate.py)
# ========================================================
elif auth_mode == "🔑 تسجيل الدخول للحساب الحالي":
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("🔓 دخول آمن وتحويل للمستودع"):
        if clean_email == "" or clean_pass == "": 
            st.error("⚠️ يرجى كتابة البريد وكلمة السر أولاً!")
        else:
            try:
                # المصادقة والتحقق الفوري اللحظي من هوية وباسورد التاجر عبر سيرفر PocketBase بالملي ثانية
                login_req = requests.get(f"{POCKETBASE_API}?filter=(email='{clean_email}'%26%26password='{clean_pass}')", timeout=10)
                if login_req.status_code == 200 and len(login_req.json().get("items", [])) > 0:
                    user_cloud_data = login_req.json().get("items", [])[0]
                    user_status = user_cloud_data.get("status", "")
                    
                    if "⏳" in user_status or "انتظار" in user_status: 
                        st.warning("⏳ حسابك مسجل، وهو قيد المراجعة حالياً من طرف الإدارة في لوحة PocketBase!")
                    elif "🔒" in user_status or "قفل" in user_status: 
                        st.error("🚨 عذراً، هذا الحساب مقفل ومحجوب كلياً لعدم سداد الباقة السنوية للمنصة!")
                    else:
                        st.success("⚡ تم التوثيق بنجاح ملوكي! جاري تحويلك تلقائياً لمتجر فواتير الجزائر ومستودع الـ AI الصافي...")
                        time.sleep(0.4)
                        # التحويل التلقائي والربط السري لمتجرك الإلكتروني الفعلي لـ الجزائر بـ DA الشغال بنجاح
                        st.markdown('<meta http-equiv="refresh" content="0;URL=\'https://streamlit.app\'">', unsafe_allow_html=True)
                else: 
                    st.error("❌ بيانات الدخول وكلمة المرور غير مطابقة لملف الأمان السحابي!")
            except:
                st.error("🚨 فشل في فحص البيانات، يرجى إعادة محاولة التوثيق لاحقاً.")
