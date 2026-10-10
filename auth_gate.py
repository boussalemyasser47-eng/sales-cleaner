# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة لبوابة التوثيق المستقلة (auth_gate.py)
# ========================================================
import streamlit as st
import sqlite3
import time

# ضبط إعدادات الصفحة الكلية لتكون واجهة دخول ملوكية
st.set_page_config(page_title="NEXUS SaaS GATEWAY v4", page_icon="🔐", layout="centered")

# حقن كود الـ CSS الأسطوري لإبادة الخلفية البيضاء وجعل الأزرار نيون زجاجية فخمة ومريحة للعين
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    
    <style>
    /* ترقية خلفية المتصفح بالكامل لتصبح ليلة رقمية عميقة */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0b0b16 0%, #040408 100%) !important;
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* [إصلاح المستطيلات البيضاء]: طمس الخلفية الافتراضية وجعل حقول الدخول نيون زجاجية فخمة */
    div[data-testid="stVerticalBlock"] button, div.stButton button, .stButton > button {
        width: 100% !important;
        min-height: 48px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        font-family: 'Cairo', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        text-align: center !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 10px 14px !important;
        background: linear-gradient(135deg, #101020 0%, #07070f 100%) !important;
        color: #ffffff !important;
        border: 2px solid #00fff0 !important;
        box-shadow: 0px 0px 15px rgba(0, 255, 240, 0.3) !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    /* تأثير التوهج الملوّن الفاخر عند تمرير الفأرة فوق تروس التوثيق */
    div.stButton button:hover {
        background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important;
        color: #000000 !important;
        box-shadow: 0px 0px 25px #00fff0 !important;
        transform: translateY(-2px) !important;
    }
    
    /* تخصيص حاوية البطاقة الزجاجية المشعة للتسجيل */
    .premium-auth-card {
        background: linear-gradient(135deg, rgba(4, 25, 34, 0.65) 0%, rgba(2, 14, 20, 0.85) 100%) !important;
        border: 2px solid #00fff0 !important;
        border-radius: 16px !important;
        padding: 25px !important;
        box-shadow: 0px 0px 30px rgba(0, 255, 240, 0.25) !important;
        direction: rtl !important;
        text-align: right !important;
        margin-bottom: 20px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    div[data-testid="stTextInput"] input { border: 2px solid #ff00ff !important; background-color: #10101b !important; color: #ffffff !important; border-radius: 12px !important; padding: 14px 16px !important; }
    h1, h2, h3, h4, p, span, label { font-family: 'Cairo', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# الجزء الثاني: خيارات فيسبوك المفتوحة وإنشاء الحسابات الحرة (auth_gate.py)
# ========================================================
# تأسيس خزانة الأمان المستقلة لاستقبال وبناء حسابات التجار الجدد حياً
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS saas_users_auth (
        email TEXT PRIMARY KEY,
        password TEXT,
        status TEXT,
        package TEXT
    )
""")
db_conn.commit()
db_conn.close()

st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 20px; text-shadow: 0 0 15px #00fff0;'>🔐 بوابة تسجيل المشتركين لمنصة SaaS الجزائر</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #ffffff; text-align: center; font-size: 14px; font-weight:600;'>قم بإنشاء حسابك الخاص بكلمة سر من إرادتك، أو سجل دخولك لاستدعاء باقتك السنوية.</p>", unsafe_allow_html=True)

st.markdown("<div class='premium-auth-card'>", unsafe_allow_html=True)
# ميكانيكية تبديل الواجهات على طريقة فيسبوك الشهيرة
auth_mode = st.radio("اختر العملية المطلوبة للتوثيق الآمن:", ["🔑 تسجيل الدخول للحساب الحالي", "📝 إنشاء حساب تاجر جديد فريش"])

input_email = st.text_input("أدخل البريد الإلكتروني الخاص بك:")
input_password = st.text_input("أدخل كلمة المرور السرية من اختيارك:", type="password")

clean_email = input_email.strip()
clean_pass = input_password.strip()
# ========================================================
# الجزء الثالث: معالجة طلبات التسجيل وحقن الـ SQL السحابي (auth_gate.py)
# ========================================================
if auth_mode == "إنشاء حساب تاجر جديد فريش":
    user_package_choice = st.selectbox("اختر فئة الباقة السنوية لمتجرك:", ["الباقة السيبرانية الخارقة (65k)", "الباقة الاحترافية المتوسطة (45k)", "الباقة الأساسية المبتدئة (29k)"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("📝 إرسال طلب إنشاء الحساب للإدارة"):
        if clean_email == "" or clean_pass == "":
            st.error("⚠️ يرجى ملء حقول البريد وكلمة السر أولاً من اختيارك!")
        else:
            conn_reg = sqlite3.connect("saas_security_vault.db", timeout=10)
            cursor_reg = conn_reg.cursor()
            try:
                # حقن الحساب بوضعية معلقة ليصعد باللون الأصفر في لوحة إدارتك السريّة للتحكم به
                cursor_reg.execute("INSERT INTO saas_users_auth VALUES (?, ?, '⏳ في انتظار التفعيل', ?)", (clean_email, clean_pass, user_package_choice))
                conn_reg.commit()
                st.success("✅ تم تسجيل حسابك الحر بنجاح أسطوري! بانتظار موافقة المدير وتفعيل باقتك السنوية.")
            except sqlite3.IntegrityError:
                st.error("🚨 هذا البريد الإلكتروني مسجل مسبقاً بالنظام! جرب خيار تسجيل الدخول.")
            conn_reg.close()
# ========================================================
# الجزء الرابع: ميكانيكية التحويل التلقائي للموقع الأصلي (auth_gate.py)
# ========================================================
elif auth_mode == "🔑 تسجيل الدخول للحساب الحالي":
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🔓 دخول آمن وتحويل للمستودع"):
        if clean_email == "" or clean_pass == "":
            st.error("⚠️ يرجى كتابة البريد وكلمة السر أولاً!")
        else:
            conn_login = sqlite3.connect("saas_security_vault.db", timeout=10)
            cursor_login = conn_login.cursor()
            cursor_login.execute("SELECT status FROM saas_users_auth WHERE email = ? AND password = ?", (clean_email, clean_pass))
            db_row = cursor_login.fetchone()
            conn_login.close()
            
            if db_row:
                user_status = db_row[0]
                if "⏳" in user_status or "انتظار" in user_status:
                    st.warning("⏳ حسابك الحر مسجل، وهو قيد المراجعة حالياً! يرجى التواصل مع المدير لتنشيط باقتك السنوية.")
                elif "🔒" in user_status or "قفل" in user_status or "محجوب" in user_status:
                    st.error("🚨 عذراً، هذا الحساب مقفل ومحجوب كلياً من لوحة القيادة العليا لعدم سداد المستحقات!")
                else:
                    st.success("⚡ تم التوثيق بنجاح ملوكي! جاري تحويلك تلقائياً لمتجرك ومستودع الفواتير الصافي...")
                    time.sleep(0.4)
                    
                    # 🚨 [التحويل التلقائي السحابي]: توجيه المتصفح ونقله فوراً لـ رابط موقعك الأصلي الظاهر بصورتك تماماً
                    # سيقوم هذا السطر بتحويل العميل الموثق لمتجر فواتير الجزائر ليبدأ العمل بنقاء وأمان كلي
                    st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'https://streamlit.app\'">', unsafe_allow_html=True)
            else:
                st.error("❌ بيانات الدخول وكلمة المرور غير مطابقة لملف الأمان السحابي!")
