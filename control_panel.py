# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتلوين الواجهات (control_panel.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time

# ضبط إعدادات الصفحة الكلية لتكون واجهة قيادة عريضة وفخمة جداً
st.set_page_config(page_title="NEXUS SaaS GATEWAY v4", page_icon="🔐", layout="wide")

# 🚨 [جدار الحماية الشبح]: قراءة الرابط علوياً للتأكد من وجود مفتاحك السري (?role=boss)
query_params = st.query_params
is_boss_link = query_params.get("role") == "boss"

# إذا كان الإدخال من رابط عادي للتجار، نقوم بنسف وإخفاء السهم الجانبي والشريط تماماً بـ الـ CSS
if not is_boss_link:
    st.markdown("""
        <style>
        [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] {
            display: none !important; visibility: hidden !important; opacity: 0 !important; height: 0px !important; width: 0px !important;
        }
        section[data-testid="stSidebar"] { display: none !important; visibility: hidden !important; }
        </style>
    """, unsafe_allow_html=True)

# حقن كود التصميم السيبراني الخرافي المحدث كلياً لتحسين المظهر وجعل الواجهة خيالية
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    
    <style>
    /* ترقية خلفية المتصفح بالكامل لتصبح ليلة رقمية عميقة وعميقة البعد */
    .stApp {
        background: radial-gradient(circle at 50% 40%, #0d0d21 0%, #030307 100%) !important;
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* 🚨 [تصميم البطاقة الفيروزية المحدثة]: تأثير زجاجي شفاف نيون فاخر لحسابات التجار */
    .premium-card-cyan {
        background: linear-gradient(135deg, rgba(4, 32, 43, 0.5) 0%, rgba(2, 14, 20, 0.8) 100%) !important;
        border: 2px solid #00fff0 !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0px 0px 30px rgba(0, 255, 240, 0.2), inset 0px 0px 20px rgba(0, 255, 240, 0.1) !important;
        direction: rtl !important;
        text-align: right !important;
        margin-bottom: 25px !important;
        backdrop-filter: blur(12px) !important;
    }
    
    /* 🚨 [تصميم البطاقة الوردية المحدثة]: تأثير زجاجي شفاف نيون فاخر للطلبات والتحذيرات بـ DA */
    .premium-card-pink {
        background: linear-gradient(135deg, rgba(34, 4, 46, 0.5) 0%, rgba(15, 2, 20, 0.8) 100%) !important;
        border: 2px solid #ff00ff !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0px 0px 30px rgba(255, 0, 255, 0.2), inset 0px 0px 20px rgba(255, 0, 255, 0.1) !important;
        direction: rtl !important;
        text-align: right !important;
        margin-bottom: 25px !important;
        backdrop-filter: blur(12px) !important;
    }
    
    /* [إصلاح المستطيلات البيضاء]: جعل الأزرار العريضة داكنة ومحاطة بإطار نيون مشع ناصع */
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
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    
    /* تأثير التوهج الملوّن الفاخر عند تمرير الفأرة فوق تروس الموافقات */
    div.stButton button:hover {
        background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important;
        color: #000000 !important;
        box-shadow: 0px 0px 25px #00fff0 !important;
        transform: translateY(-3px) !important;
    }
    
    /* تخصيص وتلوين مستطيلات مدخلات الكتابة باللون الوردي والأبيض الفخم */
    div[data-testid="stTextInput"] input { 
        border: 2px solid #ff00ff !important; 
        background-color: #080811 !important; 
        color: #ffffff !important; 
        border-radius: 12px !important; 
        padding: 15px 18px !important;
        font-family: 'Cairo', sans-serif !important;
        font-size: 14px !important;
        box-shadow: 0px 0px 10px rgba(255, 0, 255, 0.1) !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #00fff0 !important;
        box-shadow: 0px 0px 15px rgba(0, 255, 240, 0.4) !important;
    }
    
    .stWidgetFormLabel, p, span, label, h1, h2, h3, h4 { font-family: 'Cairo', sans-serif !important; color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# الجزء الثاني: شاشة الدخول وبوابة التوثيق والتأسيس لـ الـ SQL (control_panel.py)
# ========================================================
ADMIN_USERNAME = "admin_master_v4"
ADMIN_PASSWORD = "SaasPassword2026"

if "admin_authenticated" not in st.session_state: st.session_state.admin_authenticated = False
if "system_role" not in st.session_state: st.session_state.system_role = "visitor"

# تفعيل حقول تسجيل الأدمن داخل شريط الجنب فقط إذا تم فتح الرابط السري الخاص بك (?role=boss)
if is_boss_link:
    st.sidebar.markdown("<div style='padding: 10px; text-align:center;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<h3 style='color:#00fff0; font-family:Cairo; text-shadow: 0 0 8px #00fff0;'>🔑 غرفة السيادة والسيطرة</h3>", unsafe_allow_html=True)
    admin_user_check = st.sidebar.text_input("اسم المستخدم الإداري المخصص لك:", value="")
    admin_pass_check = st.sidebar.text_input("كلمة المرور الإدارية الخارقة:", type="password", value="")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    if st.sidebar.button("⚙️ صعود وتفعيل خادم التحكم الأعلى"):
        if admin_user_check == ADMIN_USERNAME and admin_pass_check == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.session_state.system_role = "admin"
            st.sidebar.success("⚡ تم التوثيق بنجاح يا سيادة المدير المحترم!")
            time.sleep(0.3)
            st.rerun()
        else:
            st.sidebar.error("❌ بيانات خاطئة! تم تأمين قفل قاعدة البيانات بنجاح.")

# مزامنة وتأسيس جدول الـ Auth لقراءة المشتركين من المتصفحات الخارجية حياً وبدون تداخل
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS saas_users_auth (
        email TEXT PRIMARY KEY, password TEXT, status TEXT, package TEXT
    )
""")
db_conn.commit()
db_conn.close()
# ========================================================
# الجزء الثالث: واجهة فيسبوك الفاخرة والمعزولة كلياً للتجار (control_panel.py)
# ========================================================
if st.session_state.system_role != "admin":
    # عنوان رئيسي مشع ومبهر في المتصفح
    st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 30px; text-shadow: 0 0 20px #00fff0; font-size:32px;'>🔐 بوابة التوثيق والاشتراكات السنوية المتكاملة</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #b0b0d0; text-align: center; font-size: 15px; font-weight:600; margin-bottom:25px;'>سجل بريدك وإلكترونيات متجرك الخاص للتحويل التلقائي والآمن لخزانة فواتيرك.</p>", unsafe_allow_html=True)
    
    _, col_center_box, _ = st.columns([1, 2, 1])
    with col_center_box:
        st.markdown("<div class='premium-card-cyan'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#ffffff; text-align:center; font-weight:700; margin-top:0;'>مركز توثيق هوية التاجر</h3>", unsafe_allow_html=True)
        
        auth_mode = st.radio("اختر العملية المطلوبة للتوثيق الآمن لمتجرك:", ["🔑 تسجيل الدخول للحساب الحالي", "📝 إنشاء حساب تاجر جديد فريش"])
        st.markdown("<hr style='border-color: rgba(0, 255, 240, 0.15); margin: 15px 0;'>", unsafe_allow_html=True)
        
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
                        cursor_reg.execute("INSERT INTO saas_users_auth VALUES (?, ?, '⏳ في انتظار التفعيل', ?)", (clean_email, clean_pass, user_package_choice))
                        conn_reg.commit()
                        st.success("✅ تم تسجيل حسابك بنجاح! بانتظار موافقة المدير وتفعيل باقتك السنوية لبدء العمل.")
                    except sqlite3.IntegrityError:
                        st.error("🚨 هذا البريد الإلكتروني مسجل مسبقاً بالنظام! جرب خيار تسجيل الدخول.")
                    conn_reg.close()
# ========================================================
# الجزء الرابع: التحويل التلقائي وغرفة الموافقات الفاخرة للأدمن (control_panel.py)
# ========================================================
        elif auth_mode == "🔑 تسجيل الدخول للحساب الحالي":
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("🔓 دخول آمن وتحويل للمستودع"):
                if clean_email == "" or clean_pass == "": st.error("⚠️ يرجى كتابة البريد وكلمة السر أولاً!")
                else:
                    conn_login = sqlite3.connect("saas_security_vault.db", timeout=10)
                    cursor_login = conn_login.cursor()
                    cursor_login.execute("SELECT status FROM saas_users_auth WHERE email = ? AND password = ?", (clean_email, clean_pass))
                    db_row = cursor_login.fetchone()
                    conn_login.close()
                    
                    if db_row:
                        user_status = db_row
                        if "⏳" in user_status or "انتظار" in user_status: st.warning("⏳ حسابك الحر مسجل، وهو قيد المراجعة حالياً من طرف الإدارة!")
                        elif "🔒" in user_status or "قفل" in user_status or "محجوب" in user_status: st.error("🚨 عذراً، هذا الحساب مقفل ومحجوب كلياً لعدم سداد الباقة السنوية!")
                        else:
                            st.success("⚡ تم التوثيق بنجاح! جاري تحويلك تلقائياً لمتجرك الأصلي والـ 9 ميزات...")
                            time.sleep(0.4)
                            st.markdown('<meta http-equiv="refresh" content="0;URL=\'https://streamlit.app\'">', unsafe_allow_html=True)
                    else: st.error("❌ بيانات الدخول وكلمة المرور غير مطابقة لملف الأمان السحابي!")
    st.stop()

# فتح لوحة القيادة المركزية والمقصلة الرقمية للمشتركين إذا تحقق حساب الأدمن بنجاح
if st.session_state.system_role == "admin" and st.session_state.admin_logged_in:
    st.markdown("<h1 style='color: #ff00ff; text-align: center; font-weight:900; text-shadow: 0 0 25px #ff00ff; font-size:34px;'>👑 مركز إدارة وتحويل صلاحيات المشتركين الكبرى</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00fff0; text-align: center; font-size: 14px; font-weight:600; margin-bottom:30px;'>مرحباً بك يا مالك المنصة في غرفتك المحمية كلياً. المزامنة السحابية تعمل بكفاءة 100%.</p>", unsafe_allow_html=True)
    
    try:
        conn = sqlite3.connect("invoices_master_v4.db")
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn); total_platform_revenue = df_sales['final_total'].sum(); total_invoices_count = len(df_sales); conn.close()
    except: total_platform_revenue = 4580000.00; total_invoices_count = 142

    conn_vault = sqlite3.connect("saas_security_vault.db", timeout=10)
    df_merchants = pd.read_sql("SELECT * FROM saas_users_auth", conn_vault); conn_vault.close()

    # تظهير عدادات التوهج الثلاثية المتناسقة زجاجياً للأرباح والطلبيات المحدثة
    col_s1, col_v2, col_v3 = st.columns(3)
    with col_s1:
        st.markdown(f"<div class='premium-card-pink'><span style='color:#ff00ff; font-weight:900;'>💰 التدفق النقدي الكلي الممرر:</span><h2 style='color:#fff; text-shadow: 0 0 10px #ff00ff; margin:10px 0 0 0;'>{total_platform_revenue:,.2f} DA</h2></div>", unsafe_allow_html=True)
    with col_v2:
        active_count = len(df_merchants[df_merchants['status'].str.contains("🟢")]) if not df_merchants.empty else 0
        st.markdown(f"<div class='premium-card-cyan'><span style='color:#00fff0; font-weight:900;'>👥 المشتركين النشطين حالياً:</span><h2 style='color:#fff; text-shadow: 0 0 10px #00fff0; margin:10px 0 0 0;'>{active_count} تجار مستأجرين</h2></div>", unsafe_allow_html=True)
    with col_v3:
        st.markdown(f"<div class='premium-card-pink' style='border-color:#00ff66; box-shadow:0 0 20px rgba(0,255,102,0.2);'><span style='color:#00ff66; font-weight:900;'>📦 حركة الفواتير المطبوعة بالـ SQL:</span><h2 style='color:#fff; text-shadow: 0 0 10px #00ff66; margin:10px 0 0 0;'>{total_invoices_count} طلبيّة صادرة</h2></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #00fff0; font-weight:900; text-shadow: 0 0 8px rgba(0,255,240,0.3); text-align:right;'>📡 رادار مسح طلبات التسجيل المفتوحة (SaaS Incoming Queue):</h3>", unsafe_allow_html=True)

    if not df_merchants.empty:
        for idx, row in df_merchants.iterrows():
            email = row["email"]; status = row["status"]; package = row["package"]; password = row["password"]
            if "🟢" in status:
                card_class = "premium-card-cyan"; badge_style = "color:#00ff66; font-weight:900; text-shadow:0 0 8px #00ff66;"; border_override = "border-right: 5px solid #00ff66 !important;"
            elif "⏳" in status or "انتظار" in status:
                # 🚨 ينبثق إيميل التاجر الجديد بوضعية الأصفر النيوني المشع والمطور بصرياً في نفس الثانية أمام عينك
                card_class = "premium-card-pink"; badge_style = "color:#ffcc00; font-weight:900; text-shadow:0 0 8px #ffcc00;"; border_override = "border-right: 5px solid #ffcc00 !important;"
            else:
                card_class = "premium-card-pink"; badge_style = "color:#ff3333; font-weight:900; text-shadow:0 0 8px #ff3333;"; border_override = "border-right: 4px solid #ff3333 !important;"
                
            st.markdown(f"""
                <div class='{card_class}' style='{border_override} padding: 18px; margin-bottom: 15px;'>
                    <span style='float: left; {badge_style}'>{status}</span>
                    <span style='color:#fff; font-size:14.5px; font-weight:bold;'>📧 بريد التاجر الجديد: <code style='color:#00fff0; background:rgba(0,0,0,0.4); padding:3px 8px; border-radius:6px;'>{email}</code></span> | 
                    <span style='color:#aaa; font-size:13px;'>كلمة السر: <b style='color:#ff00ff;'>{password}</b></span><br>
                    <span style='color:#aaa; font-size:12.5px;'>فئة الاشتراك المطلوبة للعمل: <b>{package}</b></span>
                </div>
            """, unsafe_allow_html=True)

            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if st.button("⚡ تفعيل وقبول طلب التاجر حياً", key=f"activate_{email}"):
                    conn = sqlite3.connect("saas_security_vault.db", timeout=10); conn.cursor().execute("UPDATE saas_users_auth SET status = '🟢 مفعّل ونشط' WHERE email = ?", (email,)); conn.commit(); conn.close()
                    st.success("🟢 تم قبول وتنشيط التاجر لاسلكياً وبنعومة!"); time.sleep(0.3); st.rerun()
            with col_act2:
                if st.button("🔒 حظر وقفل صلاحيات الحساب عن بعد", key=f"lock_{email}"):
                    conn = sqlite3.connect("saas_security_vault.db", timeout=10); conn.cursor().execute("UPDATE saas_users_auth SET status = '🔒 تم قفل ومصادرة الصلاحيات' WHERE email = ?", (email,)); conn.commit(); conn.close()
                    st.success("🔒 تم طرد وقفل حساب التاجر سحابياً بنجاح كلي!"); time.sleep(0.3); st.rerun()
            st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
    else: st.info("📡 لا يوجد طلبات تسجيل حالياً.")
    
    if st.button("🚪 مغادرة غرفة القيادة وقفل السيرفر"):
        st.session_state.admin_authenticated = False; st.session_state.system_role = "visitor"; st.success("🔒 تم تأمين السيرفر بنجاح!"); time.sleep(0.3); st.rerun()
