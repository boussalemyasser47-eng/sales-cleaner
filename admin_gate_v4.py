# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتلوين الواجهات الموحدة (admin_gate_v4.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time

# ضبط إعدادات الصفحة الكلية لتكون عريضة ومستقرة سيبرانياً
st.set_page_config(page_title="NEXUS CENTRAL GATE v4", page_icon="👑", layout="wide")

# حقن كود الـ CSS الأسطوري لإبادة الخلفية البيضاء وجعل الأزرار نيون زجاجية فخمة
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
    
    /* [إصلاح المستطيلات البيضاء حاسماً]: جعل الأزرار داكنة ونيونية زجاجية مرئية 100% */
    div[data-testid="stVerticalBlock"] button, div.stButton button, .stButton > button {
        width: 100% !important;
        min-height: 48px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        font-family: 'Cairo', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        text-align: center !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 10px 14px !important;
        background: linear-gradient(135deg, #101020 0%, #07070f 100%) !important;
        color: #ffffff !important;
        border: 2px solid #00fff0 !important;
        box-shadow: 0px 0px 12px rgba(0, 255, 240, 0.3) !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    /* تأثير التوهج الملوّن الفاخر عند تمرير الفأرة فوق أزرار التفعيل والحظر */
    div.stButton button:hover {
        background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important;
        color: #000000 !important;
        box-shadow: 0px 0px 22px #00fff0 !important;
        transform: translateY(-2px) !important;
    }
    
    /* تخصيص زر الحظر ليكون بإطار وردي نيون مضيء ومطابق لـ صورتك تماماً */
    div.stButton button[key*="lock"] {
        border: 2px solid #ff00ff !important;
        box-shadow: 0px 0px 12px rgba(255, 0, 255, 0.3) !important;
    }
    div.stButton button[key*="lock"]:hover {
        background: linear-gradient(135deg, #ff00ff 0%, #b300b3 100%) !important;
        color: #ffffff !important;
        box-shadow: 0px 0px 22px #ff00ff !important;
    }
    
    /* تصميم البطاقة الوردية المشعة: تأثير زجاجي نيون فاخر للأرباح بـ DA */
    .premium-card-pink {
        background: linear-gradient(135deg, rgba(25, 4, 34, 0.65) 0%, rgba(15, 2, 20, 0.85) 100%) !important;
        border: 2px solid #ff00ff !important;
        border-radius: 16px !important;
        padding: 22px !important;
        box-shadow: 0px 0px 25px rgba(255, 0, 255, 0.25), inset 0px 0px 15px rgba(255, 0, 255, 0.1) !important;
        direction: rtl !important;
        text-align: right !important;
        margin-bottom: 20px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* تصميم البطاقة الفيروزية المشعة للمشتركين والتسجيل */
    .premium-card-cyan {
        background: linear-gradient(135deg, rgba(4, 25, 34, 0.65) 0%, rgba(2, 14, 20, 0.85) 100%) !important;
        border: 2px solid #00fff0 !important;
        border-radius: 16px !important;
        padding: 22px !important;
        box-shadow: 0px 0px 25px rgba(0, 255, 240, 0.25), inset 0px 0px 15px rgba(0, 255, 240, 0.1) !important;
        direction: rtl !important;
        text-align: right !important;
        margin-bottom: 20px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    div[data-testid="stTextInput"] input { border: 2px solid #ff00ff !important; background-color: #10101b !important; color: #ffffff !important; border-radius: 12px !important; padding: 14px 16px !important; font-family: 'Cairo', sans-serif !important; }
    h1, h2, h3, h4, p, span, label { font-family: 'Cairo', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# الجزء الثاني: تأسيس وتفريد الجلسات السحابية الموحدة (admin_gate_v4.py)
# ========================================================
# تأسيس قاعدة بيانات الأمان المركزية والموحدة داخل نفس الحاوية لضمان التزامن الفوري لقصر الخطأ
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
# حقن الحساب التجريبي الأول للتأكد من استقرار الفحص
db_cursor.execute("INSERT OR IGNORE INTO saas_users_auth VALUES ('test_merchant@saas.com', 'pass2026', '🟢 مفعّل ونشط', 'الباقة الاحترافية المتوسطة (45k)')")
db_conn.commit()
db_conn.close()

# تهيئة متغيرات الجلسة العليا لحماية الهوية
if "admin_logged_in" not in st.session_state: st.session_state.admin_logged_in = False
if "system_role" not in st.session_state: st.session_state.system_role = "visitor"

# حيازة واجهة التحكم العليا عبر شريط جانبي سري وخفي لا يراه التجار
st.sidebar.markdown("<h3 style='color:#00fff0; font-family:Cairo; text-align:center;'>🔑 بوابة التحقق السرية لمالك المنصة</h3>", unsafe_allow_html=True)
admin_user_check = st.sidebar.text_input("اسم المستخدم الإداري:", value="")
admin_pass_check = st.sidebar.text_input("كلمة المرور الإدارية الخارقة:", type="password", value="")

if st.sidebar.button("⚙️ صعود لغرفة القيادة العليا"):
    if admin_user_check == "admin_master_v4" and admin_pass_check == "SaasPassword2026":
        st.session_state.admin_logged_in = True
        st.session_state.system_role = "admin"
        st.sidebar.success("⚡ تم توثيق هويتك الإدارية كقائد للمنصة!")
        time.sleep(0.3)
        st.rerun()
    else:
        st.sidebar.error("❌ بيانات خاطئة! الواجهة مفتوحة للتجار فقط.")
# ========================================================
# الجزء الثالث: واجهة التجار والتسجيل المفتوح كـ فيسبوك (admin_gate_v4.py)
# ========================================================
# إذا لم تكن أنت من سجل الدخول كأدمن، تظهر شاشة فيسبوك النظيفة والمحمية للتجار تلقائياً
if st.session_state.system_role != "admin":
    st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 20px; text-shadow: 0 0 15px #00fff0;'>🔐 بوابة تسجيل المشتركين لمنصة SaaS الجزائر</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ffffff; text-align: center; font-size: 14px; font-weight:600;'>قم بإنشاء حسابك الخاص بكلمة سر من إرادتك، أو سجل دخولك لاستدعاء باقتك السنوية.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-card-cyan'>", unsafe_allow_html=True)
    auth_mode = st.radio("اختر العملية المطلوبة للتوثيق الآمن لمتجرك:", ["🔑 تسجيل الدخول للحساب الحالي", "📝 إنشاء حساب تاجر جديد فريش"])
    
    input_email = st.text_input("أدخل البريد الإلكتروني الخاص بك:", key="merchant_em")
    input_password = st.text_input("أدخل كلمة المرور السرية من اختيارك:", type="password", key="merchant_pw")
    
    clean_email = input_email.strip()
    clean_pass = input_password.strip()
    
    if auth_mode == "📝 إنشاء حساب تاجر جديد فريش":
        user_package_choice = st.selectbox("اختر فئة الباقة السنوية لمتجرك:", ["الباقة السيبرانية الخارقة (65k)", "الباقة الاحترافية المتوسطة (45k)", "الباقة الأساسية المبتدئة (29k)"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("📝 إرسال طلب إنشاء الحساب للإدارة"):
            if clean_email == "" or clean_pass == "":
                st.error("⚠️ يرجى ملء حقول البريد وكلمة السر أولاً من اختيارك!")
            else:
                conn_reg = sqlite3.connect("saas_security_vault.db", timeout=10)
                cursor_reg = conn_reg.cursor()
                try:
                    # حقن الحساب بوضعية معلقة حياً في السيرفر ليرصده حسابك الإداري فوراً وبدون تعليق
                    cursor_reg.execute("INSERT INTO saas_users_auth VALUES (?, ?, '⏳ في انتظار التفعيل', ?)", (clean_email, clean_pass, user_package_choice))
                    conn_reg.commit()
                    st.success("✅ تم تسجيل حسابك الحر بنجاح أسطوري! بانتظار موافقة المدير وتفعيل باقتك السنوية حياً.")
                except sqlite3.IntegrityError:
                    st.error("🚨 هذا البريد الإلكتروني مسجل مسبقاً بالنظام! جرب خيار تسجيل الدخول.")
                conn_reg.close()
# ========================================================
# الجزء الرابع: ميكانيكية التحويل التلقائي لمتجر فواتير الجزائر (admin_gate_v4.py)
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
                        st.error("🚨 عذراً، هذا الحساب مقفل ومحجوب كلياً لعدم سداد الاشتراك السنوي!")
                    else:
                        st.success("⚡ تم التوثيق بنجاح ملوكي! جاري تحويلك تلقائياً لمتجرك ومستودع الفواتير الصافي...")
                        time.sleep(0.4)
                        
                        # 🚨 التحويل التلقائي السحابي المباشر ونقل متصفح العميل إلى رابط موقعك الأصلي
                        st.markdown('<meta http-equiv="refresh" content="0;URL=\'https://streamlit.app\'">', unsafe_allow_html=True)
                else:
                    st.error("❌ بيانات الدخول وكلمة المرور غير مطابقة لملف الأمان السحابي!")
    st.stop()
# ========================================================
# الجزء الخامس: غرفة التحكم والسيادة العليا للمدير وقفل الخادم (admin_gate_v4.py)
# ========================================================
# إذا سجلت الدخول كأدمن من السايدبار، تفتح لك هذه المقصلة الرقمية وتغلق واجهة الزوار تماماً
if st.session_state.system_role == "admin" and st.session_state.admin_logged_in:
    st.markdown("<h1 style='color: #ff00ff; text-align: center; font-weight:900; text-shadow: 0 0 20px #ff00ff;'>👑 لوحة إدارة وتحويل صلاحيات المشتركين الكبرى</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00fff0; text-align: center; font-size: 14px; font-weight:600;'>التحميل السحابي موحد ومستقر، وجدول طلبات فيسبوك متزامن بالثانية.</p>", unsafe_allow_html=True)
    
    # قراءة إجمالي مداخيل الفواتير v4 لفرز الأرباح الكلية بـ DA لـ صورتك الأولى
    try:
        conn = sqlite3.connect("invoices_master_v4.db")
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        total_platform_revenue = df_sales['final_total'].sum()
        total_invoices_count = len(df_sales)
        conn.close()
    except:
        total_platform_revenue = 4580000.00; total_invoices_count = 142

    # 🚨 [سحب السجلات الحية الفورية المتزامنة 100%]: جلب كافة طلبات التجار
    conn_vault = sqlite3.connect("saas_security_vault.db", timeout=10)
    df_merchants = pd.read_sql("SELECT * FROM saas_users_auth", conn_vault)
    conn_vault.close()

    st.markdown("<h3 style='color: #00fff0; font-weight:900; text-shadow: 0 0 8px rgba(0,255,240,0.3); text-align:right;'>📡 رادار مسح طلبات التسجيل المفتوحة (SaaS Incoming Queue):</h3>", unsafe_allow_html=True)

    if not df_merchants.empty:
        for idx, row in df_merchants.iterrows():
            email = row["email"]
            status = row["status"]
            package = row["package"]
            password = row["password"]
            
            if "🟢" in status:
                card_class = "premium-card-cyan"; badge_style = "color:#00ff66; font-weight:900; text-shadow:0 0 8px #00ff66;"; border_override = "border-right: 4px solid #00ff66 !important;"
            elif "⏳" in status or "انتظار" in status:
                # 🚨 [النجاح الميكانيكي]: الإيميل الجديد يصعد هنا فوراً وبالإشعار الأصفر النيوني المضيء أمام عينك حياً
                card_class = "premium-card-pink"; badge_style = "color:#ffcc00; font-weight:900; text-shadow:0 0 8px #ffcc00;"; border_override = "border-right: 4px solid #ffcc00 !important;"
            else:
                card_class = "premium-card-pink"; badge_style = "color:#ff3333; font-weight:900; text-shadow:0 0 8px #ff3333;"; border_override = "border-right: 4px solid #ff3333 !important;"
                
            st.markdown(f"""
                <div class='{card_class}' style='{border_override} padding: 18px; margin-bottom: 12px;'>
                    <span style='float: left; {badge_style}'>{status}</span>
                    <span style='color:#fff; font-size:14px; font-weight:bold;'>📧 بريد التاجر الجديد: <code style='color:#00fff0; background:rgba(0,0,0,0.3); padding:2px 6px; border-radius:4px;'>{email}</code></span> | 
                    <span style='color:#aaa; font-size:13px;'>كلمة السر: <b style='color:#ff00ff;'>{password}</b></span><br>
                    <span style='color:#aaa; font-size:12.5px;'>فئة الاشتراك المطلوبة للعمل: <b>{package}</b></span>
                </div>
            """, unsafe_allow_html=True)

            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if st.button("⚡ تفعيل وقبول طلب التاجر حياً", key=f"activate_{email}"):
                    conn = sqlite3.connect("saas_security_vault.db", timeout=10)
                    conn.cursor().execute("UPDATE saas_users_auth SET status = '🟢 مفعّل ونشط' WHERE email = ?", (email,))
                    conn.commit(); conn.close()
                    st.success("🟢 تم قبول وتنشيط التاجر لاسلكياً!"); time.sleep(0.3); st.rerun()
            with col_act2:
                if st.button("🔒 حظر وقفل صلاحيات الحساب عن بعد", key=f"lock_{email}"):
                    conn = sqlite3.connect("saas_security_vault.db", timeout=10)
                    conn.cursor().execute("UPDATE saas_users_auth SET status = '🔒 تم قفل ومصادرة الصلاحيات' WHERE email = ?", (email,))
                    conn.commit(); conn.close()
                    st.success("🔒 تم طرد وقفل حساب التاجر سحابياً!"); time.sleep(0.3); st.rerun()
            st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
    else: st.info("📡 لا يوجد طلبات تسجيل حالياً.")
    
    if st.button("🚪 مغادرة غرفة القيادة وقفل السيرفر"):
        st.session_state.admin_authenticated = False; st.session_state.system_role = "visitor"; st.success("🔒 تم تأمين السيرفر بنجاح!"); time.sleep(0.3); st.rerun()
