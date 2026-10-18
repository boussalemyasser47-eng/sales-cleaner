# ========================================================
# الجزء الأول المطور: صبغ المنصة الشامل بالنيون الزجاجي (auth_gate.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time
from datetime import datetime
import io
import urllib.parse

# ضبط إعدادات الصفحة الكلية لتكون واجهة قيادة عريضة وفخمة ومحمية كلياً
st.set_page_config(page_title="NEXUS CENTRAL GATE v4", page_icon="👑", layout="wide")

# 🚨 [جدار الحماية الشبح الحاسم]: قراءة الرابط علوياً للتأكد من وجود مفتاحك السري (?role=boss)
query_params = st.query_params
is_boss_link = query_params.get("role") == "boss" if "role" in query_params else False

if "admin_master_logged" not in st.session_state:
    st.session_state["admin_master_logged"] = False

# 🧠 [الحقن السيبراني الصافي]: كود CSS نقي 100% بدون f-string يخترق المتصفح ويصبغ العدادات والبطاقات بالنيون
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com" rel="stylesheet">
    
    <style>
    @keyframes pulseBackground {
        0% { background: radial-gradient(circle at 50% 40%, #0f0f2d 0%, #030307 100%) !important; }
        50% { background: radial-gradient(circle at 50% 45%, #08081a 0%, #010103 100%) !important; }
        100% { background: radial-gradient(circle at 50% 40%, #0f0f2d 0%, #030307 100%) !important; }
    }
    .stApp {
        animation: pulseBackground 8s ease-in-out infinite !important;
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* 💎 صبغ العدادات الثلاثية والمقاييس المستقلة بالبلور الزجاجي والنيون الفاخر المشع */
    div[data-testid="stMetricBlock"], div[data-testid="metric-container"], .premium-card-cyan, .premium-card-pink {
        background: linear-gradient(135deg, rgba(15, 2, 20, 0.85) 0%, rgba(5, 5, 12, 0.98) 100%) !important;
        border: 2px solid #00fff0 !important;
        border-radius: 16px !important;
        box-shadow: 0px 0px 30px rgba(0, 255, 240, 0.35) !important;
        backdrop-filter: blur(15px) !important;
    }
    
    /* صبغ وتلوين البطاقات النيونية المحيطة ببيانات التجار */
    div[data-testid="stMarkdownContainer"] > div {
        background: linear-gradient(135deg, rgba(10, 10, 26, 0.85) 0%, rgba(3, 3, 7, 0.98) 100%) !important;
        border: 2px solid #00fff0 !important;
        border-radius: 15px !important;
        box-shadow: 0px 0px 25px rgba(0, 255, 240, 0.2) !important;
    }
    
    /* إجبار الأزرار الخماسية التفاعلية على التوهج الكامل بالألوان السيبرانية الموضحة بالصورة */
    div.stButton button, .stButton > button {
        width: 100% !important; min-height: 48px !important;
        font-family: 'Cairo', sans-serif !important; font-size: 14px !important; font-weight: 900 !important; border-radius: 12px !important;
        background: linear-gradient(135deg, #0d0d21 0%, #05050c 100%) !important; color: #00fff0 !important;
        border: 2px solid #00fff0 !important; box-shadow: 0px 0px 15px rgba(0, 255, 240, 0.3) !important;
        transition: all 0.3s ease-in-out !important;
    }
    div.stButton button:hover { 
        background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important; color: #000000 !important;
        box-shadow: 0px 0px 30px #00fff0 !important; transform: translateY(-2px) !important;
    }
    
    /* تنظيف وتلوين حقول النصوص لمنع التداخل البصري */
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
        border: 2px solid #ff00ff !important; background-color: #06060d !important; color: #ffffff !important;
        border-radius: 12px !important; font-weight: 700 !important;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus {
        border-color: #00fff0 !important; box-shadow: 0px 0px 25px rgba(0, 255, 240, 0.5) !important;
    }
    
    /* إلغاء القائمة الجانبية المكررة لمنع تداخل شاشات المالك */
    [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] { display: none !important; }
    
    .stWidgetFormLabel, p, span, label, h1, h2, h3, h4 { 
        font-family: 'Cairo', sans-serif !important; color: #ffffff !important;
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)

# صياغة ومزامنة جدول الـ Auth لقراءة كلمات سر المشتركين في نفس الحاوية الموحدة حياً
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS saas_users_auth (
        email TEXT PRIMARY KEY, password TEXT, status TEXT, package TEXT
    )
""")
db_conn.commit()

# [إصلاح الثغرة الذكية]: منع حقن الحساب الافتراضي تلقائياً إذا قام المالك بحذفه يدوياً
db_cursor.execute("SELECT COUNT(*) FROM saas_users_auth WHERE email = 'daymaabdaalhmdllh@gmail.com'")
account_exists = db_cursor.fetchone()
if account_exists[0] == 0 and "destroyed_flag" not in st.session_state:
    db_cursor.execute("INSERT OR IGNORE INTO saas_users_auth VALUES ('daymaabdaalhmdllh@gmail.com', '123456', '🟢 مفعّل ونشط', 'الباقة السيبرانية الخارقة')")
    db_conn.commit()
db_conn.close()

# دالة التدمير الفوري لأي حساب في قاعدة البيانات
def delete_email_completely(email_to_delete):
    try:
        conn = sqlite3.connect("saas_security_vault.db", timeout=10)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saas_users_auth WHERE email = ?", (email_to_delete,))
        conn.commit(); conn.close()
        return True
    except Exception as e:
        st.error(f"⚠️ خطأ ميكانيكي أثناء الحذف: {e}"); return False


# ========================================================
# الجزء الثاني: مركز توثيق هوية التاجر وعزل البوابات (auth_gate.py)
# ========================================================
if not is_boss_link and "active_merchant_user" not in st.session_state:
    st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 40px; text-shadow: 0 0 20px #00fff0; font-size:32px;'>🔐 بوابة التوثيق والاشتراكات السنوية المتكاملة</h1>", unsafe_allow_html=True)
    
    col_side_left, col_center_box, col_side_right = st.columns(3)
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
                if clean_email == "" or clean_pass == "": st.error("⚠️ يرجى ملء حقول البريد وكلمة السر أولاً!")
                else:
                    conn_reg = sqlite3.connect("saas_security_vault.db", timeout=10)
                    cursor_reg = conn_reg.cursor()
                    cursor_reg.execute("INSERT OR IGNORE INTO saas_users_auth VALUES (?, ?, '⏳ في انتظار التفعيل', ?)", (clean_email, clean_pass, user_package_choice))
                    conn_reg.commit(); conn_reg.close()
                    st.success("🎯 تم إرسال طلبك بنجاح! سيظهر الآن في رادار الإدارة فوراً.")
                    time.sleep(0.5); st.rerun()
        else:
            st.markdown("</div>", unsafe_allow_html=True)
            if st.button("🔑 تسجيل الدخول إلى المتجر"):
                if clean_email == "" or clean_pass == "": st.error("⚠️ يرجى إدخال البريد وكلمة السر!")
                else:
                    conn_login = sqlite3.connect("saas_security_vault.db", timeout=10)
                    cursor_login = conn_login.cursor()
                    cursor_login.execute("SELECT status FROM saas_users_auth WHERE email = ? AND password = ?", (clean_email, clean_pass))
                    user_status_row = cursor_login.fetchone()
                    conn_login.close()
                    
                    if user_status_row:
                        if "🟢 مفعّل ونشط" in user_status_row[0]:
                            st.session_state["active_merchant_user"] = clean_email
                            st.success("🔓 تم التحقق بنجاح! جاري فتح متجرك...")
                            time.sleep(0.5); st.rerun()
                        else:
                            st.warning(f"⏳ حالة حسابك الحالية: {user_status_row[0]}")
                    else:
                        st.error("❌ بيانات الدخول غير مطابقة لملف الأمان السحابي.")

# ========================================================
# الجزء الثالث المصحح سيبرانياً: غرفة المالك ورادار الموافقات الخماسي (auth_gate.py)
# ========================================================
if is_boss_link:
    # تأمين وحقن الهوية علوياً لمنع خطأ NameError
    ADMIN_USERNAME = "admin_master_v4"
    ADMIN_PASSWORD = "SaasPassword2026"

    # 🔒 [المستوى الأول]: إذا لم يسجل المالك دخوله، تظهر لوحة الحماية فقط وتُحجب العدادات كلياً
    if not st.session_state["admin_master_logged"]:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='centered-box-container' style='max-width: 500px; margin: 60px auto 20px auto; padding: 40px; background: rgba(5, 5, 15, 0.95); border: 2px solid #00fff0; border-radius: 20px; box-shadow: 0px 0px 40px rgba(0, 255, 240, 0.35); direction: rtl; text-align: right; backdrop-filter: blur(15px);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #ff00ff; text-align: center; font-weight: 900; margin-top: 0;'>🔒 غرفة السيادة الكبرى والموافقات السحابية</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #ffffff; text-align: center; font-size: 15px; margin-bottom: 25px;'>🔑 تسجيل دخول المالك الأعلى للوصول للرادار</p>", unsafe_allow_html=True)
        
        boss_user = st.text_input("User:", key="boss_leader_user").strip()
        boss_pass = st.text_input("Password:", type="password", key="boss_leader_pass").strip()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("⚙️ صعود وتفعيل خادم التحكم الأعلى", key="submit_boss_login_btn"):
            if boss_user == ADMIN_USERNAME and boss_pass == ADMIN_PASSWORD:
                st.session_state["admin_master_logged"] = True
                st.toast("👑 مرحباً بك يا قائد! تم تفعيل لوحة السيادة والموافقات.", icon="🔓")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ بيانات خاطئة! يرجى إعادة التحقق من مفاتيح الأمان السحابية.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 👑 [المستوى الثاني مقفل ومحمي]: تنبثق العدادات والرادار هنا حصرياً وفقط بعد نجاح تسجيل الدخول
    else:
        st.markdown("<h1 style='color: #ffffff; text-align: center; font-weight:900; text-shadow: 0 0 25px #00fff0;'>👑 غرفة المالك والسيادة العليا v4</h1>", unsafe_allow_html=True)
        
        # العدادات الثلاثية المستقلة تظهر هنا بداخل الـ else المحمية
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1: 
            st.markdown("<div style='border:2px solid #ff00ff; border-radius:15px; padding:20px; text-align:center; background:rgba(5,5,15,0.85); box-shadow: 0px 0px 25px rgba(255, 0, 255, 0.35); direction:rtl;'><h4 style='color:#ff00ff; margin:0;'>📦 حركة الفواتير المطبوعة بالـ SQL</h4><h2>142 تلبية صادرة</h2></div>", unsafe_allow_html=True)
        with col_stat2: 
            st.markdown("<div style='border:2px solid #00fff0; border-radius:15px; padding:20px; text-align:center; background:rgba(5,5,15,0.85); box-shadow: 0px 0px 25px rgba(0, 255, 240, 0.35); direction:rtl;'><h4 style='color:#00fff0; margin:0;'>👥 المشتركين النشطين حالياً بالمنصة</h4><h2>1 تجار نشطين</h2></div>", unsafe_allow_html=True)
        with col_stat3: 
            st.markdown("<div style='border:2px solid #ffaa00; border-radius:15px; padding:20px; text-align:center; background:rgba(5,5,15,0.85); box-shadow: 0px 0px 25px rgba(255, 170, 0, 0.35); direction:rtl;'><h4 style='color:#ffaa00; margin:0;'>💰 التدفق النقدي الكلي الممرر عبر السيرفر</h4><h2>4,580,000.00 DA</h2></div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: rgba(0, 255, 240, 0.2); margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #00fff0; text-align: right; font-weight:900; direction:rtl;'>📡 (SaaS Incoming Queue) رادار مسح طلبات التسجيل المفتوحة</h2>", unsafe_allow_html=True)
        
        conn_view = sqlite3.connect("saas_security_vault.db", timeout=10)
        df_users = pd.read_sql_query("SELECT email, password, status, package FROM saas_users_auth", conn_view)
        conn_view.close()
        
        if not df_users.empty:
            for index, row in df_users.iterrows():
                current_email = row['email']; current_pass = row['password']; current_status = row['status']; current_package = row['package']
                
                status_color = "#00ff66" if "مفعّل" in current_status else "#ffaa00" if "انتظار" in current_status else "#ff0055"
                st.markdown(f"""
                <div style="border: 2px solid #00fff0; border-radius: 15px; padding: 25px; background: rgba(10,10,26,0.9); margin-bottom: 15px; direction: rtl; text-align: right;">
                    <p style="margin:0 0 8px 0; font-weight:700;">💻 بريد التاجر الجديد: <span style="color: #00fff0;">{current_email}</span> | كلمة السر المختارة: <span style="color: #ff00ff;">{current_pass}</span></p>
                    <p style="margin:0;">📊 الحالة الحالية: <span style="color: {status_color}; font-weight:bold;">{current_status}</span> | فئة الاشتراك المطلوبة للعمل: {current_package}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_1, col_2, col_3, col_4, col_5 = st.columns(5)
                with col_1:
                    if st.button("⚡ تفعيل وقبول حياً", key=f"btn_act_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🟢 مفعّل ونشط' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close(); st.toast("🎯 تم التفعيل!"); time.sleep(0.5); st.rerun()
                with col_2:
                    if st.button("⏳ تمديد 7 أيام مهلة", key=f"btn_ext_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🟡 تم تمديد فترة التجربة 7 أيام' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close(); st.toast("⏳ تم تمديد المهلة!"); time.sleep(0.5); st.rerun()
                with col_3:
                    if st.button("🗑️ تدمير نهائي فوري", key=f"btn_del_{current_email}"): st.session_state[f"ask_confirm_{current_email}"] = True
                with col_4:
                    if st.button("💸 ترقية فئة الباقة", key=f"btn_upg_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET package = 'الباقة السيبرانية الخارقة (65k)' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close(); st.toast("🚀 تم ترقية الباقة السنوية!"); time.sleep(0.5); st.rerun()
                with col_5:
                    if st.button("🔒 حظر وقفل الحساب", key=f"btn_lck_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🔴 تم قفل ومصادرة الصلاحيات' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close(); st.toast("🔒 تم مصادرة الصلاحيات عن بعد!"); time.sleep(0.5); st.rerun()
                
                if st.session_state.get(f"ask_confirm_{current_email}", False):
                    if st.button("✅ فهمت، احذف الحساب الآن", key=f"final_yes_{current_email}"):
                        st.session_state["destroyed_flag"] = True
                        st.session_state[f"ask_confirm_{current_email}"] = False
                        if delete_email_completely(current_email): st.toast("🔥 تم تذكير وتطهير الحساب!"); time.sleep(0.5); st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 مغادرة غرفة القيادة وقفل الخزائن", key="logout_boss"): st.session_state["admin_master_logged"] = False; st.rerun()
        else: 
            st.warning("📭 الرادار صافي تماماً، لا توجد طلبات معلقة حالياً.")


# ========================================================
# القسم (4 - أ): ممر العبور السحابي وجدار العزل الفردي لمتجرك الجديد
# ========================================================
if "active_merchant_user" in st.session_state and not is_boss_link:
    current_merchant = st.session_state["active_merchant_user"]
    
    # الفحص السحابي الصارم لاستمرار صلاحية التراخيص لقفل ثغرات المزامنة
    conn_final_auth = sqlite3.connect("saas_security_vault.db", timeout=10)
    cursor_final_auth = conn_final_auth.cursor()
    cursor_final_auth.execute("SELECT status FROM saas_users_auth WHERE email = ?", (current_merchant,))
    chk_row = cursor_final_auth.fetchone()
    conn_final_auth.close()
    
    user_actual_status = str(chk_row) if chk_row and chk_row is not None else ""
    
    if not chk_row or "مفعّل" not in user_actual_status:
        st.warning("🔒 انتهت أو سُحبت تراخيص الحساب السحابي.")
        if st.button("🔄 العودة لبوابة الدخول الرئيسية", key="back_gate_refresh_btn"): 
            st.session_state.pop("active_merchant_user")
            st.rerun()
        st.stop()
    
    # 🏪 [جدار العزل الفردي الأسطوري]: قفل البيانات وعزل فواتير ومخزون كل تاجر باسم إيميله المشفر
    merchant_db_name = f"invoice_vault_{urllib.parse.quote_plus(current_merchant)}.db"
    conne = sqlite3.connect(merchant_db_name)
    cursor = conne.cursor()
    
    # بناء وتحديث الجداول والمدخلات التلقائية المخصصة لمتجرك الجديد
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS v4_customer_invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_name TEXT, customer_name TEXT, customer_phone TEXT,
            product_name TEXT, final_total REAL, month_created TEXT, date_created TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS store_stock (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT UNIQUE, available_qty INTEGER
        )
    ''')
    conne.commit()

    # --- القائمة الجانبية المحدثة للتنقل بين أدواتك المحسنة ---
    st.sidebar.markdown(f"<p style='color: #00fff0; font-weight: bold; text-align:center;'>👤 التاجر النشط:<br>{current_merchant}</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<h2 style='color: #00ffcc; text-align: center; font-size: 24px;'>🛠️ التحكم</h2>", unsafe_allow_html=True)
    choice = st.sidebar.radio("اختر الأداة التي تريد استخدامها:", [
        "✨ صانع الفواتير الاحترافي (PDF)", 
        "📦 إدارة وتنبيهات المخزون السلعي",
        "🧼 مطهر ملفات المبيعات وإحصائيات الولايات",
        "🚀 مولّد الحملات والتخطيط التسويقي (AI)"
    ], key="merchant_navigation_radio")

    if st.sidebar.button("🚪 تسجيل الخروج وتأمين الحساب", key="merchant_safe_logout_btn"):
        st.session_state.pop("active_merchant_user")
        st.toast("تم الخروج الآمن وتأمين المستودع كلياً!")
        time.sleep(0.5)
        st.rerun()

    # 🤖 تشغيل الميزة الثالثة: بوت خدمة العملاء والمساعد الفوري الجانبي التابع لملفك المحسن
    render_sidebar_helper()
    # ========================================================
    # القسم (4 - ب): صانع الفواتير والملصقات الحرارية والإحصائيات
    # ========================================================
    if choice == "✨ صانع الفواتير الاحترافي (PDF)":
        st.write("<h1 style='font-size: 32px; color: #00fff0; text-shadow: 0 0 15px #00fff0;'>📄 صانع الفواتير والملصقات الحرارية الذكي</h1>", unsafe_allow_html=True)
        st.markdown("### 📊 إحصائيات متجرك الشاملة:")
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        total_sales_db = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conne)
        total_stock_db = pd.read_sql("SELECT SUM(available_qty) as total_qty FROM store_stock", conne)
        
        with stat_col1: st.metric(label="💰 إجمالي مداخيل المبيعات", value=f"{total_sales_db['final_total'].sum():,.2f} DA")
        with stat_col2: st.metric(label="🧾 عدد الفواتير الصادرة", value=f"{len(total_sales_db)} فاتورة")
        with stat_col3:
            try: stock_val = int(total_stock_db['total_qty'].values) if not total_stock_db.empty and total_stock_db['total_qty'].values is not None else 0
            except: stock_val = 0
            st.metric(label="📦 قطع متوفرة بالمستودع", value=f"{stock_val} حبة")
            
        st.markdown("---")
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("🏪 معلومات المتجر والزبون")
            shop_name = st.text_input("اسم متجرك الإلكتروني:", "DZ Cyber Store", key="invoice_shop_name_input")
            customer_name = st.text_input("اسم الزبون الكامل:", key="invoice_customer_name_input")
            customer_phone = st.text_input("رقم هاتف الزبون:", key="invoice_customer_phone_input")
            customer_address = st.text_input("عنوان التوصيل والولاية:", key="invoice_customer_address_input")
            uploaded_logo = st.file_uploader("اختر لوغو متجرك (اختياري)", type=["png", "jpg", "jpeg"], key="invoice_logo_uploader")

        with col_right:
            st.subheader("📦 تفاصيل السلعة والحسابات")
            stock_products = pd.read_sql("SELECT product_name FROM store_stock", conne)
            if not stock_products.empty: 
                product_name = st.selectbox("اختر المنتج من المخزون:", stock_products['product_name'], key="invoice_product_selectbox")
            else: 
                product_name = st.text_input("اسم المنتج (قم بإضافته للمخزون أولاً):", key="invoice_product_manual_input")
            price = st.number_input("سعر القطعة (DA):", min_value=0, value=1200, key="invoice_price_input")
            quantity = st.number_input("الكمية المبيعة:", min_value=1, value=1, key="invoice_quantity_input")
            shipping_cost = st.number_input("مصاريف الشحن (DA):", min_value=0, value=600, key="invoice_shipping_input")

        product_total = price * quantity
        final_total = product_total + shipping_cost
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        current_month = datetime.now().strftime("%Y-%m")

        st.markdown("---")
        if st.button("🚀 إصدار وحفظ الفاتورة والملصق وخصم المخزون", key="issue_invoice_and_clear_stock_btn"):
            if not customer_name or not product_name: st.error("❌ خطأ: يرجى ملء اسم الزبون والمنتج أولاً!")
            else:
                check_stock = pd.read_sql(f"SELECT available_qty FROM store_stock WHERE product_name = '{product_name}'", conne)
                if not check_stock.empty and check_stock['available_qty'].values < quantity:
                    st.error(f"❌ خطأ! المتبقي في المستودع هو: {check_stock['available_qty'].values} قطع فقط.")
                else:
                    cursor.execute("UPDATE store_stock SET available_qty = available_qty - ? WHERE product_name = ?", (quantity, product_name))
                    cursor.execute('INSERT INTO v4_customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, month_created, date_created) VALUES (?, ?, ?, ?, ?, ?, ?)', (shop_name, customer_name, customer_phone, product_name, final_total, current_month, current_date))
                    conne.commit()
                    st.success("💾 تم تسجيل البيع وتوليد المستندات بنجاح!")

                    logo_data = uploaded_logo.read() if uploaded_logo is not None else None
                    pdf_invoice = generate_invoice_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, price, quantity, product_total, shipping_cost, final_total, logo_data)
                    pdf_label = generate_thermal_label_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, final_total, current_date)
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1: st.download_button(label="📥 تحميل الفاتورة الكبيرة A4 (PDF)", data=pdf_invoice, file_name=f"invoice_{customer_name}.pdf", mime="application/pdf", key="dl_invoice_pdf_btn")
                    with col_btn2: st.download_button(label="🖨️ تحميل ملصق الشحن الحراري 4x4 (PDF)", data=pdf_label, file_name=f"thermal_label_{customer_name}.pdf", mime="application/pdf", key="dl_label_pdf_btn")

                    if st.button("🖨️ فتح نافذة الطباعة الحرارية السريعة", key="quick_thermal_print_window_btn"): st.components.v1.html("<script>window.print();</script>", height=0)

                    st.markdown("---")
                    st.subheader("📲 أزرار الإرسال السريع الفوري لزبونك:")
                    msg_text = f"مرحباً {customer_name}، تم تأكيد طلبيتك بنجاح من متجر {shop_name}. المنتج: {product_name}، الإجمالي للدفع هو: {final_total:,} DA."
                    encoded_msg = urllib.parse.quote(msg_text)
                    send_col1, send_col2 = st.columns(2)
                    with send_col1: st.link_button("🟢 إرسال تفاصيل الفاتورة عبر WhatsApp", f"https://wa.me{customer_phone}?text={encoded_msg}", key="send_whatsapp_invoice_btn")
                    with send_col2: st.link_button("🟣 إرسال تفاصيل الفاتورة عبر Viber", f"viber://forward?text={encoded_msg}", key="send_viber_invoice_btn")
    # ========================================================
    # القسم (4 - ج): نظام إدارة المخزون، مطهر الولايات ومولد حملات الـ AI وقفل الـ DB
    # ========================================================
    elif choice == "📦 إدارة وتنبيهات المخزون السلعي":
        st.write("<h1 style='font-size: 32px; color: #ff00ff; text-shadow: 0 0 15px #ff00ff;'>📦 نظام إدارة ومراقبة مخزون المستودع</h1>", unsafe_allow_html=True)
        col_add, col_view = st.columns(2)
        with col_add:
            st.subheader("📝 إضافة سلعة للمستودع:")
            new_prod = st.text_input("اسم السلعة الجديدة:")
            new_qty = st.number_input("الكمية المتوفرة:", min_value=1, value=50)
            if st.button("➕ حفظ في المستودع"):
                if new_prod:
                    try:
                        cursor.execute("INSERT INTO store_stock (product_name, available_qty) VALUES (?, ?)", (new_prod, new_qty))
                        conne.commit(); st.success(f"تم إضافة {new_prod} للمستودع!"); time.sleep(0.5); st.rerun()
                    except: st.error("المنتج موجود مسبقاً في المخزون.")
        with col_view:
            st.subheader("📋 حالة السلع المتوفرة حالياً:")
            stock_df = pd.read_sql("SELECT * FROM store_stock", conne)
            if not stock_df.empty:
                st.dataframe(stock_df, use_container_width=True)
                st.markdown("---")
                st.write("🗑️ **قسم محو وإزالة السلع من المستودع:**")
                delete_prod = st.selectbox("اختر السلعة المراد محوها نهائياً:", stock_df['product_name'])
                if st.button("❌ محو السلعة المحددة"):
                    cursor.execute("DELETE FROM store_stock WHERE product_name = ?", (delete_prod,))
                    conne.commit(); st.success(f"🗑️ تم محو السلعة [{delete_prod}] من المخزون بنجاح!"); time.sleep(0.5); st.rerun()
                
                low_stock = stock_df[stock_df['available_qty'] <= 5]
                if not low_stock.empty:
                    st.markdown("---")
                    st.write("<h3 style='color: #ff007f !important; text-shadow: 0 0 10px #ff007f;'>🚨 تنبيه: سلع أوشكت على النفاذ!</h3>", unsafe_allow_html=True)
                    st.dataframe(low_stock)
            else: st.info("مستودعك خالي تماماً حالياً.")

    elif choice == "🧼 مطهر ملفات المبيعات وإحصائيات الولايات":
        st.write("<h1 style='font-size: 32px; color: #00fff0; text-shadow: 0 0 15px #00fff0;'>🧼 نظام التطهير وعرض مقارنة البيانات والولايات</h1>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("اختر ملف المبيعات (CSV أو Excel)", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            df_raw, df, duplicated_rows, bad_prices = process_sales_file(uploaded_file)
            
            st.subheader("📋 1. جدول البيانات الأصلي المرفوع (قبل التطهير):")
            st.dataframe(df_raw, use_container_width=True)
            st.success("✅ تم تنظيف الداتا بنجاح وتجهيز المقارنة البصرية!")
            
            col_clean, col_trash = st.columns(2)
            with col_clean:
                st.subheader("💎 2. جدول البيانات النظيف (بعد التطهير):")
                st.dataframe(df, use_container_width=True)
                st.metric(label="صافي الأرباح الحقيقية المتوقعة", value=f"{df['total_row_sales'].sum():,.2f} DA")
            with col_trash:
                st.subheader("⚠️ 3. التكرارات والأخطاء المحذوفة:")
                if not duplicated_rows.empty or not bad_prices.empty:
                    if not duplicated_rows.empty:
                        st.warning(f"تم حذف {len(duplicated_rows)} سطر مكرر!")
                        st.dataframe(duplicated_rows)
                    if not bad_prices.empty:
                        st.error(f"تم حذف {len(bad_prices)} سطر أسعار سالبة!")
                        st.dataframe(bad_prices)
                else: st.info("الملف سليم تماماً ولا يحتوي على أخطاء.")
                    
            st.markdown("---")
            render_data_insights(df)
            
            st.markdown("---")
            st.subheader("📈 المخططات البيانية الملونة للولايات والمبيعات:")
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                st.write("💰 حجم المبيعات الإجمالي الحقيقي لكل منتج:")
                st.bar_chart(data=df, x='product_name', y='total_row_sales', color='#00ffcc')
            with chart_col2:
                wilaya_col = None
                for col in df.columns:
                    if 'address' in col.lower() or 'wilaya' in col.lower() or 'ولاية' in col:
                        wilaya_col = col
                        break
                if wilaya_col:
                    st.write(f"🗺️ حجم الشحن والمبيعات حسب الولايات الجزائرية:")
                    st.bar_chart(data=df, x=wilaya_col, y='total_row_sales', color='#ff007f')
                else: st.info("💡 نصيحة: سمّ عمود السكن في ملفك باسم 'wilaya' ليظهر مخطط فرز الولايات.")
                
            csv_buffer = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 تحميل ملف المبيعات المطهّر بالكامل", data=csv_buffer, file_name="cleaned_neon_sales.csv", mime="text/csv")

    elif choice == "🚀 مولّد الحملات والتخطيط التسويقي (AI)":
        render_marketing_hub()

    # قفل فوري لقناة الاتصال بالـ DB مع نهاية المتجر لتجنب حدوث Lock حماية للـ RAM
    conne.close()
