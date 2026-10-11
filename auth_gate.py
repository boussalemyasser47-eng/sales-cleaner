# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتلوين واجهة التجار (auth_gate.py)
# ========================================================
import streamlit as st
import time
import os

# ضبط إعدادات الصفحة الكلية لتكون واجهة دخول ملوكية موسطة ونظيفة
st.set_page_config(page_title="NEXUS SaaS GATEWAY v4", page_icon="🔐", layout="wide")

# حقن كود الـ CSS المطور كلياً لتوسيط واجهة فيسبوك النظيفة وسحق المستطيلات البيضاء الافتراضية
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    
    <style>
    /* ترقية خلفية المتصفح بالكامل لتصبح ليلة رقمية عميقة ومريحة لعين العميل */
    .stApp {
        background: radial-gradient(circle at 50% 40%, #0d0d21 0%, #030307 100%) !important;
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* [إصلاح حاسم وتوسيط البطاقة]: صندوق التسجيل لـ فيسبوك يتوسط المتصفح بدقة متناهية بالبكسل */
    .centered-merchant-box {
        max-width: 500px !important;
        margin: 40px auto 20px auto !important;
        padding: 35px !important;
        background: linear-gradient(135deg, rgba(4, 32, 43, 0.5) 0%, rgba(2, 14, 20, 0.8) 100%) !important;
        border: 2px solid #00fff0 !important;
        border-radius: 20px !important;
        box-shadow: 0px 0px 35px rgba(0, 255, 240, 0.25), inset 0px 0px 20px rgba(0, 255, 240, 0.1) !important;
        direction: rtl !important;
        text-align: right !important;
        backdrop-filter: blur(12px) !important;
    }
    
    /* جعل أزرار الإرسال والدخول داكنة ومحاطة بإطار نيون فيروزي مشع */
    div[data-testid="stVerticalBlock"] button, div.stButton button, .stButton > button {
        width: 100% !important;
        min-height: 50px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        font-family: 'Cairo', sans-serif !important;
        font-size: 14.5px !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        text-align: center !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 12px 18px !important;
        background: linear-gradient(135deg, #090915 0%, #040409 100%) !important;
        color: #00fff0 !important;
        border: 2px solid #00fff0 !important;
        box-shadow: 0px 0px 15px rgba(0, 255, 240, 0.3) !important;
        transition: all 0.4s ease-in-out !important;
    }
    
    div.stButton button:hover {
        background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important;
        color: #000000 !important;
        box-shadow: 0px 0px 25px #00fff0 !important;
        transform: translateY(-3px) !important;
    }
    
    /* تخصيص مستطيلات مدخلات الكتابة باللون الوردي والأبيض الفخم لمنع التداخل */
    div[data-testid="stTextInput"] input { 
        border: 2px solid #ff00ff !important; 
        background-color: #080811 !important; 
        color: #ffffff !important; 
        border-radius: 12px !important; 
        padding: 15px 18px !important;
        font-family: 'Cairo', sans-serif !important;
        font-size: 14px !important;
    }
    
    .stWidgetFormLabel, p, span, label, h1, h2, h3, h4 { font-family: 'Cairo', sans-serif !important; color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# الجزء الثاني: حقول مدخلات التجار وتثبيت مسار التخزين الموحد (auth_gate.py)
# ========================================================
# اسم ملف التخزين التشاركي الموحد والثابت داخل نفس مجلد المشروع لضمان نقل البيانات الفوري
VAULT_FILE = "merchants_vault.txt"

# إنشاء الملف تلقائياً إذا لم يكن موجوداً مسبقاً لمنع أي خطأ قراءة
if not os.path.exists(VAULT_FILE):
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        f.write("daymaabdaalhmdllh@gmail.com|123456|🟢 مفعّل ونشط|الباقة الخارقة\n")

st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 30px; text-shadow: 0 0 20px #00fff0; font-size:32px;'>🔐 بوابة التوثيق والاشتراكات السنوية المتكاملة</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #b0b0d0; text-align: center; font-size: 15px; font-weight:600; margin-bottom:25px;'>قم بإنشاء حسابك الخاص بكلمة سر من إرادتك، وسجل دخولك للتحويل التلقائي والآمن لمتجرك الفواتيري.</p>", unsafe_allow_html=True)

# فتح حاوية التوسيط وضخ الحقول بداخل قلب منتصف المتصفح لتطابق صورتك الناجحة تماماً
st.markdown("<div class='centered-merchant-box'>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#ffffff; text-align:center; font-weight:700; margin-top:0;'>مركز توثيق هوية التاجر</h3>", unsafe_allow_html=True)

auth_mode = st.radio("اختر العملية المطلوبة للتوثيق الآمن لمتجرك:", ["🔑 تسجيل الدخول للحساب الحالي", "📝 إنشاء حساب تاجر جديد فريش"])
st.markdown("<hr style='border-color: rgba(0, 255, 240, 0.15); margin: 15px 0;'>", unsafe_allow_html=True)

input_email = st.text_input("أدخل البريد الإلكتروني الخاص بك:", key="merchant_em_gate")
input_password = st.text_input("أدخل كلمة المرور السرية من اختيارك:", type="password", key="merchant_pw_gate")

clean_email = input_email.strip()
clean_pass = input_password.strip()
# ========================================================
# الجزء الثالث: معالجة حقن طلبات التسجيل وحظر التكرار (auth_gate.py)
# ========================================================
if auth_mode == "📝 إنشاء حساب تاجر جديد فريش":
    user_package_choice = st.selectbox("اختر فئة الباقة السنوية لمتجرك للعمل:", ["الباقة السيبرانية الخارقة (65k)", "الباقة الاحترافية المتوسطة (45k)", "الباقة الأساسية المبتدئة (29k)"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    _, col_btn_sub, _ = st.columns(3)
    with col_btn_sub:
        if st.button("📝 إرسال طلب إنشاء الحساب للإدارة", key="merchant_submit_reg_btn"):
            if clean_email == "" or clean_pass == "":
                st.error("⚠️ يرجى ملء حقول البريد وكلمة السر أولاً من اختيارك!")
            else:
                # التحقق الحاسم من عدم تكرار الحساب داخل ملف الأمان المشترك
                email_exists = False
                with open(VAULT_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip() and line.split("|")[0] == clean_email:
                            email_exists = True
                            break
                
                if email_exists:
                    st.error("🚨 هذا البريد الإلكتروني مسجل مسبقاً بالنظام! جرب خيار تسجيل الدخول.")
                else:
                    # حقن العميل حياً بداخل مسار التخزين الموحد بصيغة معزولة لحين مراجعته وقبوله من طرفك
                    with open(VAULT_FILE, "a", encoding="utf-8") as f:
                        f.write(f"{clean_email}|{clean_pass}|⏳ في انتظار التفعيل|{user_package_choice}\n")
                    st.success("✅ تم تسجيل حسابك الحر بنجاح! طارت معلوماتك للإدارة وبانتظار تفعيل باقتك السنوية حياً.")
# ========================================================
# الجزء الرابع: التوثيق والمصادقة والتحويل الآلي للمستودع (auth_gate.py)
# ========================================================
elif auth_mode == "🔑 تسجيل الدخول للحساب الحالي":
    st.markdown("</div>", unsafe_allow_html=True)
    
    _, col_btn_log, _ = st.columns(3)
    with col_btn_log:
        if st.button("🔓 دخول آمن وتحويل للمستودع", key="merchant_login_execute_btn"):
            if clean_email == "" or clean_pass == "": 
                st.error("⚠️ يرجى كتابة البريد وكلمة السر أولاً!")
            else:
                # قراءة ومصادقة هويات التجار من ملف الأمان التشاركي الموحد بالثانية
                account_found = False
                user_status = ""
                user_password_cloud = ""
                
                with open(VAULT_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            parts = line.strip().split("|")
                            if parts[0] == clean_email:
                                account_found = True
                                user_password_cloud = parts[1]
                                user_status = parts[2]
                                break
                
                if account_found:
                    if user_password_cloud == clean_pass:
                        if "⏳" in user_status or "انتظار" in user_status:
                            st.warning("⏳ حسابك مسجل، وهو قيد المراجعة حالياً من طرف الإدارة! يرجى التواصل مع المدير لتنشيط باقتك.")
                        elif "🔒" in user_status or "قفل" in user_status or "محجوب" in user_status:
                            st.error("🚨 عذراً، هذا الحساب مقفل ومحجوب كلياً لعدم سداد الاشتراك السنوي للمنصة!")
                        else:
                            st.success("⚡ تم التوثيق بنجاح ملوكي! جاري تحويلك تلقائياً لمتجر فواتير الجزائر والمستودع الصافي...")
                            time.sleep(0.4)
                            # التحويل التلقائي والربط السري لمتجرك الإلكتروني الفعلي لـ الجزائر
                            st.markdown('<meta http-equiv="refresh" content="0;URL=\'https://streamlit.app\'">', unsafe_allow_html=True)
                    else:
                        st.error("❌ كلمة المرور السرية غير مطابقة لملف الأمان السحابي!")
                else:
                    st.error("❌ هذا البريد الإلكتروني غير مسجل بالمنصة! اذهب لإنشاء حساب جديد أولاً.")
