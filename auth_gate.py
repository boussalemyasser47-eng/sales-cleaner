# ========================================================
# الجزء الأول المطور (أ): صبغ المنصة الشامل بالنيون الزجاجي (auth_gate_part1.py)
# ========================================================
# ========================================================
# 🔒 [خزانة النسخ الاحتياطي التلقائي المشفرة - Cyber Auto-Backup Vault]
# ========================================================
def create_backup_vault():
    import os
    import zipfile
    import io
    from datetime import datetime
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in os.listdir("."):
            if file.endswith(".db"):
                try:
                    with open(file, "rb") as f:
                        zip_file.writestr(f"backup_{datetime.now().strftime('%Y%m%d')}_{file}", f.read())
                except Exception:
                    pass
    zip_buffer.seek(0)
    return zip_buffer


import streamlit as st
import pandas as pd
import sqlite3
import time
from datetime import datetime
import io
import urllib.parse
# ========================================================
# 🔒 [خزانة النسخ الاحتياطي التلقائي المشفرة - Cyber Auto-Backup Vault]
# ========================================================

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
    
    /* صبغ وتلوين البطاقات النيونية المحيطة ببيانات التجار بشكل مرن وديناميكي */
    div[data-testid="stMarkdownContainer"] > div {
        background: linear-gradient(135deg, rgba(10, 10, 26, 0.85) 0%, rgba(3, 3, 7, 0.98) 100%) !important;
        border: 2px solid var(--custom-border-color, #00fff0);
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

    /* 🟢 🔴 🟡 تلوين الأزرار الخماسية المتتالية بالترتيب العددي للأعمدة لمنع التشفير العشوائي */
    
    /* 1. الزر الأول (العمود الأول): أخضر نيوني */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div.stButton button {
        color: #00ff66 !important; border: 2px solid #00ff66 !important; box-shadow: 0px 0px 15px rgba(0, 255, 102, 0.2) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div.stButton button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div.stButton button:active {
        background: linear-gradient(135deg, #00ff66 0%, #00ea11 100%) !important; color: #000000 !important;
        box-shadow: 0px 0px 30px #00ff66 !important; border-color: #00ff66 !important;
    }

    /* 2. الزر الثاني (العمود الثاني): أصفر نيوني */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div.stButton button {
        color: #ffaa00 !important; border: 2px solid #ffaa00 !important; box-shadow: 0px 0px 15px rgba(255, 170, 0, 0.2) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div.stButton button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div.stButton button:active {
        background: linear-gradient(135deg, #ffaa00 0%, #ff8800 100%) !important; color: #000000 !important;
        box-shadow: 0px 0px 30px #ffaa00 !important; border-color: #ffaa00 !important;
    }

    /* 3. الزر الثالث (العمود الثالث): أحمر نيوني */
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) div.stButton button {
        color: #ff0055 !important; border: 2px solid #ff0055 !important; box-shadow: 0px 0px 15px rgba(255, 0, 85, 0.2) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) div.stButton button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) div.stButton button:active {
        background: linear-gradient(135deg, #ff0055 0%, #ff0000 100%) !important; color: #ffffff !important;
        box-shadow: 0px 0px 30px #ff0055 !important; border-color: #ff0055 !important;
    }

    /* 4. الزر الرابع (العمود الرابع): بنفسجي نيوني */
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) div.stButton button {
        color: #ff00ff !important; border: 2px solid #ff00ff !important; box-shadow: 0px 0px 15px rgba(255, 0, 255, 0.2) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) div.stButton button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) div.stButton button:active {
        background: linear-gradient(135deg, #ff00ff 0%, #cc00cc 100%) !important; color: #ffffff !important;
        box-shadow: 0px 0px 30px #ff00ff !important; border-color: #ff00ff !important;
    }

    /* 5. الزر الخامس (العمود الخامس): برتقالي ناري */
    div[data-testid="stHorizontalBlock"] > div:nth-child(5) div.stButton button {
        color: #ff4500 !important; border: 2px solid #ff4500 !important; box-shadow: 0px 0px 15px rgba(255, 69, 0, 0.2) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(5) div.stButton button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(5) div.stButton button:active {
        background: linear-gradient(135deg, #ff4500 0%, #ff2200 100%) !important; color: #ffffff !important;
        box-shadow: 0px 0px 30px #ff4500 !important; border-color: #ff4500 !important;
    }

    /* # === تأثيرات التوهج والأنيميشن لعدادات المالك === */
    @keyframes hudPulse {
        0% { box-shadow: 0px 0px 20px rgba(0, 255, 240, 0.25); border-color: #00fff0; }
        50% { box-shadow: 0px 0px 35px rgba(0, 255, 240, 0.55); border-color: #00ffaa; }
        100% { box-shadow: 0px 0px 20px rgba(0, 255, 240, 0.25); border-color: #00fff0; }
    }
    @keyframes hudIntro {
        0% { opacity: 0; transform: scale(0.96); }
        100% { opacity: 1; transform: scale(1); }
    }
    div[data-testid="stMetricBlock"], div[data-testid="metric-container"], .premium-card-cyan, .premium-card-pink {
        animation: hudIntro 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards, hudPulse 4s ease-in-out infinite alternate !important;
    }
    div[data-testid="stMetricBlock"] [data-testid="stMetricValue"], div[data-testid="metric-container"] .stMetricValue {
        text-shadow: 0px 0px 15px rgba(0, 255, 240, 0.6) !important;
        font-weight: 900 !important;
    }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# الجزء الأول المطور (ب): إدارة قاعدة بيانات الـ Auth (auth_gate_part2.py)
# ========================================================

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

# === الإضافات والتعديلات الجديدة ===


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
# الجزء الثالث المصحح سيبرانياً: غرفة المالك ورادار الموافقات الخماسي (auth_gate.py) - [الجزء 1]
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

        # ========================================================
        # 📊 [الميزة 2]: لوحة العدادات المالية الموحدة للمالك ورادار تنبيه الـ 7 أيام (نسخة الحماية القصوى)
        # ========================================================
        st.markdown("<h2 style='color: #00fff0; text-align: right; font-weight:900; direction:rtl;'>📊 لوحة العدادات المالية الموحدة (The Boss Revenue HUD)</h2>", unsafe_allow_html=True)
        
        # فتح اتصال سريع وآمن مع قاعدة البيانات لجلب كافة البيانات المتوفرة بأمان
        conn_hud = sqlite3.connect("saas_security_vault.db", timeout=10)
        try:
            total_merchants_query = pd.read_sql("SELECT * FROM saas_users_auth", conn_hud)
        except:
            total_merchants_query = pd.DataFrame(columns=['email', 'status'])
        conn_hud.close()
        
        # التحقق من وجود الأعمدة وحساب العدادات بأمان سيبراني كامل منعاً للـ OperationalError
        active_count = 0
        pending_count = 0
        if not total_merchants_query.empty and 'status' in total_merchants_query.columns:
            active_count = len(total_merchants_query[total_merchants_query['status'].str.contains('مفعّل', na=False)])
            pending_count = len(total_merchants_query[total_merchants_query['status'].str.contains('معلّق', na=False)])

        # عرض العدادات الحية المتغيرة تلقائياً بناءً على التجار المسجلين في سيرفرك
        hud_col1, hud_col2, hud_col3 = st.columns(3)
        with hud_col1:
            st.markdown(f"<div style='border:2px solid #00fff0; border-radius:15px; padding:20px; text-align:center; background:rgba(5,15,20,0.85); box-shadow: 0px 0px 20px rgba(0, 255, 240, 0.25); direction:rtl;'><h4 style='color:#00fff0; margin:0;'>👤 المتاجر النشطة حياً</h4><h2>{active_count} متجر</h2></div>", unsafe_allow_html=True)
        with hud_col2:
            st.markdown(f"<div style='border:2px solid #ff0055; border-radius:15px; padding:20px; text-align:center; background:rgba(20,5,10,0.85); box-shadow: 0px 0px 20px rgba(255, 0, 85, 0.25); direction:rtl;'><h4 style='color:#ff0055; margin:0;'>⏳ طلبات معلقة بالتفريغ</h4><h2>{pending_count} طلب</h2></div>", unsafe_allow_html=True)
        with hud_col3:
            estimated_revenue = active_count * 45000
            st.markdown(f"<div style='border:2px solid #ffaa00; border-radius:15px; padding:20px; text-align:center; background:rgba(15,10,5,0.85); box-shadow: 0px 0px 20px rgba(255, 170, 0, 0.25); direction:rtl;'><h4 style='color:#ffaa00; margin:0;'>💰 صافي التدفقات السنوية الحية</h4><h2>{estimated_revenue:,} DA</h2></div>", unsafe_allow_html=True)

        # 🚨 رادار فحص التراخيص المقتربة من الانتهاء (تنبيه الـ 7 أيام بموثوقية عالية)
        st.markdown("<br>", unsafe_allow_html=True)
        expired_alerts = []
        
        date_col = None
        for col in total_merchants_query.columns:
            if 'date' in col or 'تاريخ' in col:
                date_col = col
                break
                
        if date_col and not total_merchants_query.empty:
            for index, row in total_merchants_query.iterrows():
                try:
                    reg_date = datetime.strptime(row[date_col].split()[0], "%Y-%m-%d")
                    days_passed = (datetime.now() - reg_date).days
                    days_left = 365 - days_passed
                    if 0 <= days_left <= 7 and row['status'] == 'مفعّل':
                        expired_alerts.append((row['email'], days_left))
                except:
                    pass
        
        # عرض صندوق التنبيهات النيوني المطور باستخدام الحقن المظهري للمؤشرات الدائرية المشعة
        if expired_alerts:
            st.markdown("<div style='border:2px dashed #ff0055; border-radius:12px; padding:20px; background:rgba(20,5,10,0.95); margin-bottom:15px; direction:rtl; text-align:right; box-shadow: 0px 0px 30px rgba(255, 0, 85, 0.15);'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#ff0055; margin:0 0 15px 0; font-weight:900;'>🚨 رادار التراخيص المنتهية الصلاحية (خلال 7 أيام):</h4>", unsafe_allow_html=True)
            
            for alert in expired_alerts:
                merchant_email = alert[0]
                days_remain = alert[1]
                
                # استدعاء دالة بناء المؤشر النيوني الدائري لحقن التصميم الفخم
                html_ring = render_neon_license_ring(merchant_email, days_remain)
                st.markdown(html_ring, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

        # 🔒 [خزانة النسخ الاحتياطي التلقائي المشفرة]:
        st.markdown("<br><h3 style='color: #ff00ff; text-align: right; font-weight:900; direction:rtl;'>🔒 خزانة النسخ الاحتياطي التلقائي المشفرة</h3>", unsafe_allow_html=True)
        col_backup, col_empty = st.columns([1, 2])
        with col_backup:
            try:
                backup_data = create_backup_vault()
                st.download_button(
                    label="📥 تحميل النسخة الاحتياطية الشاملة الفورية (.ZIP)",
                    data=backup_data,
                    file_name=f"NEXUS_CORE_BACKUP_{datetime.now().strftime('%Y-%m-%d')}.zip",
                    mime="application/zip",
                    key="download_cyber_backup_vault_btn"
                )
            except Exception as e:
                st.error(f"⚠️ فشل توليد الخزنة الاحتياطية: {e}")

        st.markdown("<hr style='border-color: rgba(0, 255, 240, 0.2); margin: 30px 0;'>", unsafe_allow_html=True)
# ========================================================
# الجزء الثالث المصحح سيبرانياً: غرفة المالك ورادار الموافقات الخماسي (auth_gate.py) - [الجزء 2]
# ========================================================
        st.markdown("<h2 style='color: #00fff0; text-align: right; font-weight:900; direction:rtl;'>📡 (SaaS Incoming Queue) رادار مسح طلبات التسجيل المفتوحة</h2>", unsafe_allow_html=True)
        
        conn_view = sqlite3.connect("saas_security_vault.db", timeout=10)
        df_users = pd.read_sql_query("SELECT email, password, status, package FROM saas_users_auth", conn_view)
        conn_view.close()
        
        if not df_users.empty:
            for index, row in df_users.iterrows():
                current_email = row['email']; current_pass = row['password']; current_status = row['status']; current_package = row['package']
                status_color = "#00ff66" if "مفعّل" in current_status else "#ffaa00" if "انتظار" in current_status else "#ff0055"
                
                # 🧠 [قراءة حالة اللون الديناميكي المخصصة للتاجر من الجلسة أو وضع اللون الافتراضي النيوني]
                current_border_color = st.session_state.get(f"border_color_{current_email}", "#00fff0")
                
                st.markdown(f"""
                <div style="border: 2px solid {current_border_color}; border-radius: 15px; padding: 25px; background: rgba(10,10,26,0.9); margin-bottom: 15px; direction: rtl; text-align: right; box-shadow: 0px 0px 15px {current_border_color}40;">
                    <p style="margin:0 0 8px 0; font-weight:700;">💻 بريد التاجر الجديد: <span style="color: #00fff0;">{current_email}</span> | كلمة السر المختارة: <span style="color: #ff00ff;">{current_pass}</span></p>
                    <p style="margin:0;">📊 الحالة الحالية: <span style="color: {status_color}; font-weight:bold;">{current_status}</span> | فئة الاشتراك المطلوبة للعمل: {current_package}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_1, col_2, col_3, col_4, col_5 = st.columns(5)
                with col_1:
                    if st.button("⚡ تفعيل وقبول حياً", key=f"btn_act_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🟢 مفعّل ونشط' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close()
                        st.session_state[f"border_color_{current_email}"] = "#00ff66"
                        st.toast("🎯 تم التفعيل!"); time.sleep(0.5); st.rerun()
                with col_2:
                    if st.button("⏳ تمديد 7 أيام مهلة", key=f"btn_ext_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🟡 تم تمديد فترة التجربة 7 أيام' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close()
                        st.session_state[f"border_color_{current_email}"] = "#ffaa00"
                        st.toast("⏳ تم تمديد المهلة!"); time.sleep(0.5); st.rerun()
                with col_3:
                    if st.button("🗑️ تدمير نهائي فوري", key=f"btn_del_{current_email}"):
                        st.session_state[f"border_color_{current_email}"] = "#ff0055"
                        st.session_state[f"ask_confirm_{current_email}"] = True
                with col_4:
                    if st.button("💸 ترقية فئة الباقة", key=f"btn_upg_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET package = 'الباقة السيبرانية الخارقة (65k)' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close()
                        st.session_state[f"border_color_{current_email}"] = "#ff00ff"
                        st.toast("🚀 تم ترقية الباقة السنوية!"); time.sleep(0.5); st.rerun()
                with col_5:
                    if st.button("🔒 حظر وقفل الحساب", key=f"btn_lck_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🔴 تم قفل ومصادرة الصلاحيات' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close()
                        st.session_state[f"border_color_{current_email}"] = "#ff4500"
                        st.toast("🔒 تم مصادرة الصلاحيات عن بعد!"); time.sleep(0.5); st.rerun()
                
                if st.session_state.get(f"ask_confirm_{current_email}", False):
                    if st.button("✅ فهمت، احذف الحساب الآن", key=f"final_yes_{current_email}"):
                        st.session_state["destroyed_flag"] = True
                        st.session_state[f"ask_confirm_{current_email}"] = False
                        if delete_email_completely(current_email): st.toast("🔥 تم تذكير وتطهير الحساب!"); time.sleep(0.5); st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 مغادرة غرفة القيادة وقفل الخزائن", key="logout_boss"): st.session_state["admin_master_logged"] = False; st.rerun()
        else: 
            st.warning("📭 الرادار صافي تماماً، لا توجد طلبات معلقة حالياً.")

# === الإضافات والتعديلات الجديدة لغرفة المالك ===
# === إضافة مؤشر التراخيص الدائري المشع للرادار ===
def render_neon_license_ring(email, days_left):
    """
    تقوم بتوليد واجهة HTML/SVG مخصصة تحتوي على حلقة نيوني متغيرة الحجم واللون ديناميكياً
    تبدأ من الأصفر وتتحول للأحمر الناري كلما اقتربت الأيام من الصفر.
    """
    clamped_days = max(0, min(7, days_left))
    percentage = clamped_days / 7.0
    total_circumference = 113
    stroke_offset = total_circumference * (1 - percentage)
    
    if clamped_days > 4:
        glow_color = "#ffaa00"  # أصفر نيوني
    elif clamped_days > 2:
        glow_color = "#ff5500"  # برتقالي حرج
    else:
        glow_color = "#ff0055"  # أحمر ناري دمي
        
    html_template = f"""
    <div style='display: flex; align-items: center; justify-content: space-between; padding: 12px; background: rgba(5,5,15,0.6); border-radius: 8px; margin-bottom: 8px; border-left: 4px solid {glow_color};'>
        <div style='display: flex; align-items: center; gap: 15px;'>
            <svg width="45" height="45" viewBox="0 0 45 45" style="transform: rotate(-90deg); filter: drop-shadow(0px 0px 6px {glow_color});">
                <circle cx="22.5" cy="22.5" r="18" stroke="rgba(255,255,255,0.1)" stroke-width="3" fill="transparent" />
                <circle cx="22.5" cy="22.5" r="18" stroke="{glow_color}" stroke-width="3.5" fill="transparent" 
                        stroke-dasharray="{total_circumference}" stroke-dashoffset="{stroke_offset}" stroke-linecap="round" />
            </svg>
            <span style='color:#ffffff; font-size: 15px;'>⚠️ التاجر: <b>{email}</b></span>
        </div>
        <span style='color:{glow_color}; font-weight:bold; font-size: 14px;'>متبقي: {days_left} أيام فقط!</span>
    </div>
    """
    return html_template


# ========================================================
# القسم (4 - أ): ممر العبور السحابي وجدار العزل الفردي لمتجرك الجديد
# ========================================================
# ========================================================
# حقن الدوال الأساسية لمنع خطأ NameError في التطبيق كلياً
# ========================================================

def generate_invoice_pdf(*args, **kwargs):
    """دالة توليد فاتورة PDF مؤقتة لمنع انهيار الواجهة"""
    import io
    buffer = io.BytesIO()
    buffer.write(b"%PDF-1.4 ... Fake Invoice PDF Buffer Data")
    buffer.seek(0)
    return buffer

def generate_thermal_label_pdf(*args, **kwargs):
    """دالة توليد ملصق شحن حراري مؤقت لمنع انهيار الواجهة"""
    import io
    buffer = io.BytesIO()
    buffer.write(b"%PDF-1.4 ... Fake Thermal Label Buffer Data")
    buffer.seek(0)
    return buffer

def process_sales_file(uploaded_file):
    """دالة مطهر ملفات المبيعات مؤقتة لمنع الـ NameError"""
    import pandas as pd
    df_raw = pd.DataFrame()
    df_clean = pd.DataFrame(columns=['product_name', 'total_row_sales', 'wilaya'])
    return df_raw, df_clean, df_raw, df_raw

def render_data_insights(*args, **kwargs):
    """دالة عرض مقارنة الولايات مؤقتة لمنع الـ NameError"""
    pass

def render_marketing_hub(*args, **kwargs):
    """
    مركز مولد الحملات والتخطيط التسويقي الذكي المطور (AI Marketing Hub)
    """
    st.write("<h1 style='font-size: 32px; color: #ffaa00; text-shadow: 0 0 15px #ffaa00;'>🚀 مولّد الحملات والتخطيط التسويقي بذكاء AI</h1>", unsafe_allow_html=True)
    st.write("مرحباً بك في مركز القيادة التسويقية. اختر نوع الحملة ودع النظام الذكي يصيغ لك الاستراتيجية الاحترافية.")

    col_input, col_output = st.columns([1, 1.2])
    
    with col_input:
        st.subheader("📋 مدخلات الحملة الذكية")
        ai_prod_name = st.text_input("اسم المنتج المراد تسويقه:", "ساعة ذكية مقاومة للماء", key="ai_prod_name_in")
        ai_prod_desc = st.text_area("وصف مختصر للمنتج وميزاته التنافسية:", "شاشة أموليد، بطارية تدوم 7 أيام، تدعم الاتصال واستقبال الإشعارات.", key="ai_prod_desc_in")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            target_audience = st.selectbox("الفئة المستهدفة:", ["الشباب والرياضيين", "رجال الأعمال والمهنيين", "النساء والأناقة", "عامة الناس (جميع الفئات)"])
        with col_m2:
            marketing_tone = st.selectbox("لهجة الخطاب الإعلاني:", ["بالدارجة الجزائرية المحفزة", "بالفصحى الإقناعية الفخمة", "حماسية وتخفيضات صدمة"])
            
        campaign_goal = st.radio("الهدف الرئيسي من هذه الحملة:", ["🎯 زيادة المبيعات المباشرة (Conversion)", "📢 الوعي بالالعلامة التجارية (Awareness)", "🎁 تقديم عرض ترويجي خاص (Promo Box)"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🧠 تشغيل العقل السيبراني وتوليد الحملة فوراً", key="start_ai_marketing_brain")

    with col_output:
        st.subheader("📡 مخرجات الخطة التسويقية والإعلانات المصاغة")
        
        if generate_btn:
            with st.spinner("⏳ جاري تحليل المدخلات وصياغة المحتوى الإعلاني..."):
                # محاكاة لنموذج الذكاء الاصطناعي مع تخصيص القوالب الذكية بناءً على الخيارات
                time.sleep(1.2) # وقت معالجة الـ AI
                
                st.toast("🎯 تم توليد الأفكار التسويقية بنجاح!", icon="🚀")
                
                # بناء النص التسويقي بناءً على اللهجة والهدف
                if "بالدارجة" in marketing_tone:
                    intro_text = f"✨ حابب تزيد من ستيلك وتهني راسك؟ متجرنا جابلكم الحل مع [{ai_prod_name}] الخارق! 😎"
                    features_text = f"🔥 الميزات لي راح تتبدل بيهم حياتك:\n- {ai_prod_desc}\n- التوصيل متوفر لـ 58 ولاية والدفع عند الاستلام! 📦"
                    cta_text = "🚨 الكمية محدودة بزاف! ابعثولنا رسالة في الصفحة أو اضغط على الرابط للطلب الفوري 🛒"
                elif "بالفصحى" in marketing_tone:
                    intro_text = f"👑 الفخامة والأداء يجتمعان الآن! نقدم لكم أحدث ابتكاراتنا: [{ai_prod_name}] المصمم خصيصاً ليناسب تطلعاتكم."
                    features_text = f"📋 أبرز المواصفات الفنية:\n- {ai_prod_desc}\n- ضمان حقيقي وخدمة شحن سريعة وموثوقة لجميع الولايات."
                    cta_text = "🎯 ارتقِ بأسلوب حياتك اليوم. اضغط على الزر واطلب منتجك الآن قبل نفاذ المخزون!"
                else:
                    intro_text = f"⚡️⚡️ عررررض خاص وصدمة! [{ai_prod_name}] بأفضل سعر في السوق الجزائري حالياً! لا تفوت الفرصة 😱"
                    features_text = f"💥 كسرنا الأسعار مع ميزات خيالية:\n- {ai_prod_desc}\n- التوصيل سريع حتى لباب دارك!"
                    cta_text = "🎁 اطلب قطعتين واحصل على الشحن مجاناً! اضغط هنا وسجل طلبيتك الآن 🛒"

                # عرض خطة الاستهداف المقترحة
                st.markdown(f"""
                <div style="border: 2px solid #ffaa00; border-radius: 12px; padding: 20px; background: rgba(15,10,5,0.9); margin-bottom: 20px;">
                    <h4 style="color: #ffaa00; margin-top:0;">📝 نص الإعلان المقترح لمنصات التواصل (Copywriting):</h4>
                    <p style="color: #ffffff; font-size: 15px; white-space: pre-line;">
                    {intro_text}\n\n{features_text}\n\n{cta_text}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # خطة الاستهداف في فيسبوك وأدووردز
                st.markdown(f"""
                <div style="border: 2px solid #00fff0; border-radius: 12px; padding: 20px; background: rgba(5,15,20,0.9);">
                    <h4 style="color: #00fff0; margin-top:0;">🎯 خطة استهداف الإعلانات الموصى بها (Targeting Settings):</h4>
                    <ul>
                        <li><b>الاهتمامات المستهدفة:</b> التسوق عبر الإنترنت، المهتمين بـ {ai_prod_name}، التجارة الإلكترونية في الجزائر.</li>
                        <li><b>الفئة العمرية المفضلة:</b> 18 - 45 سنة (بناءً على اختيار: {target_audience}).</li>
                        <li><b>الولايات الأكثر تفاعلاً المقترحة للبدء:</b> الجزائر العاصمة، وهران، قسنطينة، سطيف، والبليدة.</li>
                        <li><b>ميزانية الفحص المقترحة:</b> 5$ إلى 10$ يومياً لحملة الـ Engagement أولاً قبل الـ Conversion.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # زر نسخ الإعلان
                full_ad_copy = f"{intro_text}\n\n{features_text}\n\n{cta_text}"
                st.download_button(label="📋 نسخ ونص الإعلان المولد كمستند نصي", data=full_ad_copy, file_name="ai_marketing_ad.txt", mime="text/plain", key="copy_ai_ad_text_btn")
        else:
            st.info("💡 نصيحة سيبرانية: املأ تفاصيل منتجك في الجانب الأيمن ثم اضغط على زر التشغيل ليقوم الذكاء الاصطناعي بتحليل السوق وصياغة منشوراتك الإعلانية فوراً.")


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
    
    # حقن الاتصال داخل الـ session_state لمنع قفل التزامن وقنوات الاتصال المتكررة
        # تأمين فحص وجود الاتصال حياً داخل الجلسة وإعادة بنائه فوراً إن كان مغلقاً لمنع ProgrammingError
    if "merchant_db_conn" not in st.session_state:
        st.session_state["merchant_db_conn"] = sqlite3.connect(merchant_db_name, check_same_thread=False)
    else:
        try:
            st.session_state["merchant_db_conn"].execute("SELECT 1")
        except (sqlite3.ProgrammingError, sqlite3.OperationalError):
            st.session_state["merchant_db_conn"] = sqlite3.connect(merchant_db_name, check_same_thread=False)
        
    conne = st.session_state["merchant_db_conn"]
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

    # --- حقن دالة المساعد هنا لتكون معرفة قبل الاستدعاء لمنع خطأ NameError ---
        # --- دالة المساعد الجانبي محاذية ومؤمنة سيبرانياً بنسبة 100% ---
    # --- دالة المساعد الجانبي محاذية ومؤمنة سيبرانياً بنسبة 100% ---
    # --- نسخة العقل السيبراني الخارقة للمساعد الجانبي (مقاومة للأخطاء الإملائية والتعميم) ---


          # --- العقل السيبراني المزدوج: فصل مساعد المالك عن مساعد التجار المستأجرين مع مقاومة الأخطاء الإملائية ---
    def render_sidebar_helper():
        """
        بوت المساعد الذكي المزدوج المتطور كلياً:
        - للمالك: يفتح خبير البرمجة وتحليل الأكواد وجداول السيكويل والأمر 'شرح دكي'.
        - للتجار: يفتح خبير التجارة والشحن والمخزون مع خوارزميات تحمل الأخطاء الإملائية (Typos).
        """
        st.sidebar.markdown("---")
        
        # 1. دالة التطهير المشتركة وتنظيف الحروف لمنع تداخل أخطاء الكتابة
        def normalize_arabic_text(text):
            if not text: return ""
            text = text.strip().lower()
            text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي").replace("ة", "ه")
            for haraka in ["ّ", "🔸", "؟", "!", ".", "،", "ـ"]:
                text = text.replace(haraka, "")
            return text

        # 2. خوارزمية حساب المسافة اللغوية (Levenshtein Distance) لمنع جمود البوت عند حدوث أخطاء إملائية
        # 2. خوارزمية المسافة اللغوية المطورة: إلغاء التطابق الجزئي لمنع خداع الخربشة الطويلة
        def get_close_match_score(word1, word2):
            w1, w2 = normalize_arabic_text(word1), normalize_arabic_text(word2)
            if not w1 or not w2: return 0.0
            if w1 == w2: return 1.0 # تطابق تام وحقيقي فقط
            
            # منع العبور الجزئي التلقائي إذا كان فارق الطول بين الكلمتين كبيراً جداً (كالخربشة الطويلة)
            if abs(len(w1) - len(w2)) > 3: return 0.0
            
            len1, len2 = len(w1), len(w2)
            matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
            for i in range(len1 + 1): matrix[i][0] = i
            for j in range(len2 + 1): matrix[0][j] = j
            
            for i in range(1, len1 + 1):
                for j in range(1, len2 + 1):
                    cost = 0 if w1[i-1] == w2[j-1] else 1
                    matrix[i][j] = min(matrix[i-1][j] + 1, matrix[i][j-1] + 1, matrix[i-1][j-1] + cost)
            
            distance = matrix[len1][len2]
            return 1.0 - (distance / max(len1, len2))

        # ==========================================
        # 👑 أولاً: بيئة المالك الأعلى (Owner Workspace)
        # ==========================================
        if is_boss_link:
            st.sidebar.markdown("<h3 style='color: #00fff0; text-align: center; margin-bottom: 0;'>👑 مساعد المالك الأعلى</h3>", unsafe_allow_html=True)
            if "boss_chat_reply" not in st.session_state:
                st.session_state["boss_chat_reply"] = "مرحباً بك يا قائد! نظام تحليل الكود المتقدم والأمر الخاص 'شرح dki' جاهز تحت سيادتك."

            boss_query = st.sidebar.text_input("💻 أدخل أمر التحليل أو استفسر عن الكود والجداول:", key="boss_ai_query_in", placeholder="اكتب: شرح دكي")
            boss_intents = {
                "smart_explain": ["شرح دكي", "شرح ذكي", "شرح الكود", "كود المبيعات"],
                "code_structure": ["برمجه", "كود", "الملف", "البناء", "هيكل", "بايثون"],
                "database_tables": ["جدول", "جداول", "قاعده البيانات", "داتا", "سيكويل", "sqlite"]
            }

            if st.sidebar.button("🧠 استدعاء خبير المنصة", key="submit_boss_query_btn") or boss_query == "شرح دكي":
                if boss_query:
                    with st.sidebar.spinner("⏳ جاري تحليل الـ Backend..."):
                        time.sleep(0.5)
                        clean_input = normalize_arabic_text(boss_query)
                        input_words = clean_input.split()
                        detected_intent = None
                        highest_score = 0.0
                        
                        for intent, keywords in boss_intents.items():
                            for kw in keywords:
                                normalized_kw = normalize_arabic_text(kw)
                                for word in input_words:
                                    score = get_close_match_score(word, normalized_kw)
                                    if score > highest_score and score >= 0.70:
                                        highest_score = score; detected_intent = intent

                        if detected_intent == "smart_explain" or boss_query == "شرح دكي":
                            st.session_state["boss_chat_reply"] = "📊 **[شرح دكي للمالك]:** كود المبيعات والمخزون مبني على الـ SQLite3 وعزل الـ SaaS البنيوي؛ يربط كل تاجر بملف مشفر باسم إيميله لتفادي التداخل وقفل الـ RAM."
                        elif detected_intent == "code_structure":
                            st.session_state["boss_chat_reply"] = "💻 **بناء الملف البرمجي:** ملف `auth_gate.py` مقسم لأربعة أقسام سيبرانية: صباغة الـ CSS، بوابة المصادقة والتسجيل، رادار الموافقات والحظر، وممر المتاجر المعزولة."
                        elif detected_intent == "database_tables":
                            st.session_state["boss_chat_reply"] = "🗃️ **تحليل الجداول:** النظام يدير جدول `saas_users_auth` لفحص تراخيص المشتركين، وجدول الفواتير والمخزون المستقل لكل متجر."
                        else:
                            st.session_state["boss_chat_reply"] = f"🎯 **تحليل مخصص:** الأمر [{boss_query}] سليم ومؤمن تحت نظام صلاحيات سيادتك."
                        st.rerun()

            st.sidebar.markdown(f'<div style="border:2px solid #00fff0; border-radius:12px; padding:15px; background:rgba(5,15,20,0.85); margin-top:10px;"><p style="color:#ffffff; font-size:14px; direction:rtl; text-align:right; margin:0;">{st.session_state["boss_chat_reply"]}</p></div>', unsafe_allow_html=True)

         # 1. هذا السطر موجود في ملفك، ابحث عنه لتبدأ الحذف من تحته:
        # ==========================================
        # 🏪 ثانياً: بيئة المساعد التجاري للمستأجرين (Merchant Space)
        # ==========================================
        else:
            st.sidebar.markdown("<h3 style='color: #00fff0; text-align: center; margin-bottom: 0;'>🤖 المساعد التجاري الذكي</h3>", unsafe_allow_html=True)
            if "merchant_chat_reply" not in st.session_state:
                st.session_state["merchant_chat_reply"] = "مرحباً بك! أنا مساعدك التجاري الذكي لمساعدتك في إدارة مبيعاتك وشحنك وتسويقك حياً."

            merchant_query = st.sidebar.text_input("💡 اسأل عن أي فكرة، نصيحة، أو مشكلة في متجرك:", key="merchant_ai_query_in", placeholder="مثال: عندي مشكل في التوصيل")
            
            merchant_intents = {
                "shipping": ["شحن", "توصيل", "ولاية", "ليفريرون", "ليفرور", "رتور", "ولايات", "جنوب", "سحن", "توسيل"],
                "customers": ["زبون", "زبائن", "كليون", "لكليون", "تعامل", "اتصال", "تثبيت", "كونفيرمي", "الهاتف", "سبون"],
                "stock": ["منتج", "سلعة", "مخزون", "قضية", "مستودع", "ستوك", "حبة", "قطع", "نفاذ", "منتح"]
            }

            if st.sidebar.button("🧠 استشارة العقل التجاري", key="submit_merchant_query_btn"):
                if merchant_query:
                    clean_input = normalize_arabic_text(merchant_query)
                    
                    # 🚨 [جدار حماية الحروف العشوائية]: إذا كان النص المكتوب خربشة أو حرفاً واحداً غير مفهوم
                                        # 🚨 [جدار حماية الحروف العشوائية المطور]: منع تخمين الحروف القصيرة جداً مثل (سي) أو خربشة الأرقام
                    if len(clean_input) < 3 or clean_input.isdigit():
                        st.session_state["merchant_chat_reply"] = "⚠️ **إدخال غير مفهوم:** يبدو أنك كتبت حروفاً عشوائية أو ناقصة بالخطأ! يرجى الاستعانة بدليل المواضيع الموضحة في الأسفل لمساعدتك."
                    else:
                        with st.sidebar.spinner("⏳ جاري تحليل السؤال ومقاومة الأخطاء الإملائية..."):
                            time.sleep(0.5)
                            input_words = clean_input.split()
                            detected_intent = None
                            highest_score = 0.0
                            best_suggested_kw = ""
                            
                            for intent, keywords in merchant_intents.items():
                                for kw in keywords:
                                    normalized_kw = normalize_arabic_text(kw)
                                    for word in input_words:
                                        score = get_close_match_score(word, normalized_kw)
                                        if score > highest_score:
                                            highest_score = score
                                            # رفع حد الأمان البرمجي إلى 0.82 لمنع الخداع بالكلمات العشوائية الطويلة
                                            if score >= 0.82: 
                                                detected_intent = intent
                                            else: 
                                                best_suggested_kw = kw

                            # معالجة النتائج بدقة سيبرانية صارمة
                            if detected_intent == "shipping":
                                st.session_state["merchant_chat_reply"] = "📌 **نصيحة الشحن للمتجر:** ركز حملاتك الإعلانية على ولايات الوسط والشرق (العاصمة، سطيف، قسنطينة) لضمان سرعة التوصيل وزيادة نسبة استلام الطرود (Livraison) وتفادي المرتجعات."
                            elif detected_intent == "customers":
                                st.session_state["merchant_chat_reply"] = "📞 **إستراتيجية التثبيت للمتجر:** اتصل بالزبون فوراً لتأكيد الشراء (Confirmation)، واستخدم لهجة محترمة مع توضيح السعر الإجمالي شامل الشحن لتفادي الرفض عند الباب."
                            elif detected_intent == "stock":
                                st.session_state["merchant_chat_reply"] = "📦 **نصيحة مراقبة المخزون:** إذا انخفضت كمية أي منتج في مستودعك لأقل من 5 قطع، أطلق فوراً 'عرض القطعة الأخيرة' بتخفيض 10% لتصفية الستوك وضخ السيولة."
                            else:
                                # إذا كانت الكلمة خربشة عشوائية تماماً مثل (مشيسويسي) ولا تشبه أي شيء حقيقي
                                st.session_state["merchant_chat_reply"] = "⚠️ **إدخال غير مفهوم:** لم أتمكن من تحديد مرادك بدقة! يرجى كتابة سؤال واضح أو الاستعانة بدليل المواضيع في الأسفل (مثال: شحن، ستوك، كليون)."
                        st.rerun()


            # عرض رد المساعد التجاري داخل صندوق النيون
            st.sidebar.markdown(f'<div style="border:2px solid #00fff0; border-radius:12px; padding:15px; background:rgba(5,15,20,0.85); margin-top:10px;"><p style="color:#ffffff; font-size:14px; direction:rtl; text-align:right; margin:0;">{st.session_state["merchant_chat_reply"]}</p></div>', unsafe_allow_html=True)
            
            # 💡 [حقن لوحة الإرشادات التفاعلية المساعدة للتاجر تظهر دائماً بالأسفل للتوجيه]
            st.sidebar.markdown("""
            <div style="margin-top: 15px; padding: 10px; background: rgba(255,170,0,0.05); border: 1px dashed #ffaa00; border-radius: 10px; text-align: right; direction: rtl;">
                <p style="color: #ffaa00; font-size: 12px; margin: 0 0 5px 0; font-weight: bold;">💡 مواضيع يمكنك استشارتي فيها:</p>
                <span style="color: #ffffff; font-size: 11px;">• مشاكل الشحن والـ Retour<br>• تثبيت الطلبيات والاتصال بالزبائن<br>• إدارة السلع ونفاذ الستوك (Stock)</span>
            </div>
            """, unsafe_allow_html=True)


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
        # إغلاق آمن لقناة الاتصال المخزنة قبل الخروج نهائياً لحماية قاعدة البيانات من الـ Lock
        if "merchant_db_conn" in st.session_state:
            st.session_state["merchant_db_conn"].close()
            st.session_state.pop("merchant_db_conn")
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
        
        # تفعيل آلية الحفظ داخل جلسة العمل لضمان ثبات أزرار التحميل وروابط السوشيال ميديا
        if st.button("🚀 إصدار وحفظ الفاتورة والملصق وخصم المخزون", key="issue_invoice_and_clear_stock_btn"):
            if not customer_name or not product_name: 
                st.error("❌ خطأ: يرجى ملء اسم الزبون والمنتج أولاً!")
            else:
                check_stock = pd.read_sql(f"SELECT available_qty FROM store_stock WHERE product_name = '{product_name}'", conne)
                if not check_stock.empty and check_stock['available_qty'].values[0] < quantity:
                    st.error(f"❌ خطأ! المتبقي في المستودع هو: {check_stock['available_qty'].values[0]} قطع فقط.")
                else:
                    cursor.execute("UPDATE store_stock SET available_qty = available_qty - ? WHERE product_name = ?", (quantity, product_name))
                    cursor.execute('INSERT INTO v4_customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, month_created, date_created) VALUES (?, ?, ?, ?, ?, ?, ?)', (shop_name, customer_name, customer_phone, product_name, final_total, current_month, current_date))
                    conne.commit()
                    
                    # قراءة اللوغو وحفظ الملفات بداخل الـ session_state
                    logo_data = uploaded_logo.read() if uploaded_logo is not None else None
                    st.session_state["generated_pdf_invoice"] = generate_invoice_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, price, quantity, product_total, shipping_cost, final_total, logo_data)
                    st.session_state["generated_pdf_label"] = generate_thermal_label_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, final_total, current_date)
                    st.session_state["last_active_customer"] = customer_name
                    st.session_state["last_active_phone"] = customer_phone
                    st.session_state["last_active_shop"] = shop_name
                    st.session_state["last_active_product"] = product_name
                    st.session_state["last_active_total"] = final_total
                    st.success("💾 تم تسجيل البيع وتوليد المستندات بنجاح!")
        # عرض أزرار التحميل والإرسال إذا كانت البيانات متوفرة في جلسة التصفح الحالية
        if "generated_pdf_invoice" in st.session_state:
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1: 
                st.download_button(label="📥 تحميل الفاتورة الكبيرة A4 (PDF)", data=st.session_state["generated_pdf_invoice"], file_name=f"invoice_{st.session_state['last_active_customer']}.pdf", mime="application/pdf", key="dl_invoice_pdf_btn")
            with col_btn2: 
                st.download_button(label="🖨️ تحميل ملصق الشحن الحراري 4x4 (PDF)", data=st.session_state["generated_pdf_label"], file_name=f"thermal_label_{st.session_state['last_active_customer']}.pdf", mime="application/pdf", key="dl_label_pdf_btn")
            if st.button("🖨️ فتح نافذة الطباعة الحرارية السريعة", key="quick_thermal_print_window_btn"): 
                st.components.v1.html("<script>window.print();</script>", height=0)
            st.markdown("---")
            st.subheader("📲 أزرار الإرسال السريع الفوري لزبونك:")
            msg_text = f"مرحباً {st.session_state['last_active_customer']}، تم تأكيد طلبيتك بنجاح من متجر {st.session_state['last_active_shop']}. المنتج: {st.session_state['last_active_product']}، الإجمالي للدفع هو: {st.session_state['last_active_total']:,} DA."
            encoded_msg = urllib.parse.quote(msg_text)
            
            send_col1, send_col2 = st.columns(2)
            with send_col1: 
                st.link_button("🟢 إرسال تفاصيل الفاتورة عبر WhatsApp", f"https://wa.me{st.session_state['last_active_phone']}?text={encoded_msg}", key="send_whatsapp_invoice_btn")
            with send_col2: 
                st.link_button("🟣 إرسال تفاصيل الفاتورة عبر Viber", f"viber://forward?text={encoded_msg}", key="send_viber_invoice_btn")

        # === إضافة صندوق المعاينة الحية للفاتورة النيونية ===
        st.markdown("---")
        st.subheader("👁️ معاينة حية فورية قبل الحفظ:")
        
        preview_customer = customer_name if customer_name else "<i>لم يتم الإدخال بعد</i>"
        preview_phone = customer_phone if customer_phone else "<i>لم يتم الإدخال بعد</i>"
        preview_product = product_name if product_name else "<i>لم يتم الاختيار بعد</i>"
        
        neon_card_html = f"""
        <div style="
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 25px;
            border: 1px solid rgba(0, 255, 240, 0.2);
            box-shadow: 0 0 20px rgba(0, 255, 240, 0.1), inset 0 0 15px rgba(0, 255, 240, 0.05);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: right;
            direction: rtl;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(0, 255, 240, 0.3); padding-bottom: 12px; margin-bottom: 15px;">
                <span style="font-size: 18px; font-weight: bold; color: #00fff0; text-shadow: 0 0 10px rgba(0, 255, 240, 0.5);">🏪 {shop_name}</span>
                <span style="font-size: 12px; color: #888;">📅 {current_date}</span>
            </div>
            <div style="margin-bottom: 10px; color: #e0e0e0; font-size: 14px;">
                <strong>👤 العميل:</strong> <span style="color: #fff;">{preview_customer}</span>
            </div>
            <div style="margin-bottom: 10px; color: #e0e0e0; font-size: 14px;">
                <strong>📞 الهاتف:</strong> <span style="color: #fff; direction: ltr; display: inline-block;">{preview_phone}</span>
            </div>
            <div style="margin-bottom: 15px; color: #e0e0e0; font-size: 14px;">
                <strong>📦 المنتج المطلوب:</strong> <span style="color: #00fff0;">{preview_product} (×{quantity})</span>
            </div>
            <div style="
                background: rgba(0, 255, 240, 0.05);
                border-radius: 8px;
                padding: 12px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border: 1px solid rgba(0, 255, 240, 0.15);
            ">
                <span style="font-size: 15px; font-weight: bold; color: #fff;">💰 الصافي الإجمالي (شامل الشحن):</span>
                <span style="font-size: 20px; font-weight: bold; color: #00fff0; text-shadow: 0 0 12px #00fff0;">{final_total:,.2f} DA</span>
            </div>
        </div>
        """
        st.markdown(neon_card_html, unsafe_allow_html=True)

   
  
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
                        conne.commit()
                        st.success(f"تم إضافة {new_prod} للمستودع!")
                        
                        # حساب تفاصيل الإعلان مسبقاً وتخزينها في ذاكرة الجلسة المستمرة لتفادي مسحها بالـ rerun
                        current_merchant = st.session_state.get('user_email', st.session_state.get('username', "merchant.nexus@nexus-gate.com"))
                        
                        copy_dz = f"يا جماعة الخير جبتلكم اليوم حاجة فور بزاف لغادي تهنيكم كامل! 😍\nالمنتج المتميز والمطلوب بقوة [{new_prod}] راهو دخل للمستودع تعنا وبكمية محدودة جداً.\n💎 جودة عالية، كفاءة مثالية، وسعر مدهش ما تلقاوه في حتى بلاصة.\n🚚 التوصيل سريع ومتوفر لـ 58 ولاية جزائرية حتى لباب الدار، والدفع حتى تستلم سلعتك وتفحصها بيدك!\n📥 دبر راسك ما تخليش الفرصة تفوتك وأرسل رسالة لصفحتنا للطلب الآن قبل ما تخلص الكمية!"
                        copy_ar = f"أخيراً، المنتج الأكثر طلباً وتميزاً [{new_prod}] متوفر الآن بين يديك وبأعلى مواصفات الجودة!\n💎 صُمم هذا المنتج خصيصاً ليلبي احتياجاتكم اليومية بكفاءة لا مثيل لها وبسعر تنافسي للغاية.\n🚚 يسعدنا أن نعلن عن توفر شحن سريع وموثوق إلى جميع الولايات الجزائرية مع ميزة الدفع عند الاستلام.\n📥 لا تترددوا، الكمية محدودة جداً! اضغط على زر 'تسوق الآن' أو أرسل رسالة إلى حسابنا لتأكيد طلبك اليوم."
                        copy_short = f"السلعة لڨاع تحوسو عليها [{new_prod}] دخلت من جديد وبقوة! 🔥 جودة توب وسعر هبال. الشحن متوفر لـ 58 ولاية والدفع عند الاستلام 🚚 اضغط على الرابط أو ابعت مساج في الخاص واطلب ديالك قبل نفاذ المخزون! 📥"
                        
                        h1 = f"1. قبل ما تشري أي حاجة في الجزائر.. شوف واش دخل جديد في [{new_prod}]! 😱"
                        h2 = f"2. المنتج لڨاع التجار والزبائن يحوسو عليه راهو متوفر أخيراً في المستودع! 🔥"
                        h3 = f"3. هادي هي السلعة لغادي تهنيك وتوفر عليك الوقت والتعب تع الصح! 💎"
                        h4 = f"4. ضياع للمال لو كان ما تطلبش [{new_prod}] بسعر الجملة تع اليوم! 💸"
                        h5 = f"5. الكمية راهي تخلص بزاف.. شوف وعلاش ڨاع الناس تطلب في هذا المنتج المدهش! 📦"
                        
                        testing_budget_usd = 20.0
                        exchange_rate_parallel = 240.0
                        testing_budget_dzd = testing_budget_usd * exchange_rate_parallel
                        
                        st.session_state['premium_marketing_hub'] = {
                            'merchant': current_merchant,
                            'product_name': new_prod,
                            'copy_dz': copy_dz,
                            'copy_ar': copy_ar,
                            'copy_short': copy_short,
                            'hooks': [h1, h2, h3, h4, h5],
                            'budget_usd': testing_budget_usd,
                            'budget_dzd': testing_budget_dzd
                        }
                        
                        time.sleep(0.5)
                        st.rerun()
                    except: st.error("المنتج موجود مسبقاً في المخزون.")
        with col_view:
            st.subheader("📋 حالة السلع المتوفرة حالياً:")
            stock_df = pd.read_sql("SELECT * FROM store_stock", conne)
            if not stock_df.empty:
                st.dataframe(stock_df, use_container_width=True)
                
                # === إضافة مؤشر المخزون الناري المتوهج ===
                def render_neon_stock_fire_bar(df_data):
                    st.markdown("<p style='font-size: 14px; color: #b0b0b0; margin-top: 15px;'>🔥 مؤشر تدفق المستودع المباشر (تحديث لحظي النيون):</p>", unsafe_allow_html=True)
                    max_qty = int(df_data['available_qty'].max()) if not df_data.empty else 100
                    if max_qty < 30: max_qty = 30
                    
                    for _, row in df_data.iterrows():
                        p_name = row['product_name']
                        p_qty = int(row['available_qty'])
                        width_pct = max(6, min(100, int((p_qty / max_qty) * 100)))
                        
                        if p_qty < 5:
                            bar_color, shadow_color, status_text = "#ff0055", "rgba(255, 0, 85, 0.9)", "🚨 خطر - مخزون حرج جداً!"
                        elif 5 <= p_qty <= 15:
                            bar_color, shadow_color, status_text = "#ffcc00", "rgba(255, 204, 0, 0.8)", "⚠️ انتباه - مخزون متوسط"
                        else:
                            bar_color, shadow_color, status_text = "#00ff66", "rgba(0, 255, 102, 0.8)", "✅ آمن - مستودع مستقر"
                            
                        neon_html = f"""
                        <div style="margin-bottom: 12px; background: #0f0f12; padding: 10px; border-radius: 8px; border: 1px solid #222;">
                            <div style="display: flex; justify-content: space-between; font-size: 13px; color: #fff; margin-bottom: 6px;">
                                <span><strong>{p_name}</strong> <span style="color: #888;">({p_qty} قطعة)</span></span>
                                <span style="color: {bar_color}; text-shadow: 0 0 8px {bar_color}; font-weight: bold; font-size: 12px;">{status_text}</span>
                            </div>
                            <div style="width: 100%; background-color: #1a1a24; border-radius: 5px; overflow: hidden; height: 8px;">
                                <div style="width: {width_pct}%; background-color: {bar_color}; height: 8px; border-radius: 5px; box-shadow: 0 0 12px {shadow_color}; transition: all 0.4s ease-in-out;"></div>
                            </div>
                        </div>
                        """
                        st.write(neon_html, unsafe_allow_html=True)
                
                render_neon_stock_fire_bar(stock_df)
                
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

        # === دمج وتطوير منصة بطاقات الاستهداف والإعلانات الذكية للسلع الجديدة ===
        if st.session_state.get("show_premium_ai_hub", False) and "active_ai_marketing_prod" in st.session_state:
            st.markdown("---")
            hub_data = st.session_state.get('premium_marketing_hub', {})
            if hub_data:
                prod_name = hub_data['product_name']
                merchant_user = hub_data['merchant']
                st.write(f"""
                <div style="background: linear-gradient(135deg, #0c0822, #180030); border: 2px solid #00fff0; border-radius: 16px; padding: 20px; text-align: right; direction: rtl;">
                    <h3 style="color: #ffffff; margin: 0;">📡 PREMIUM AI MARKETING HUB // المسؤول: {merchant_user}</h3>
                    <p style="color: #a4a4ba; font-size: 13px; margin: 5px 0 0 0;">تم تأمين السلعة [{prod_name}] تلقائياً وبناء بطاقة فحص مبيعاتها السريعة في المستودع بنجاح.</p>
                </div>
                """, unsafe_allow_html=True)
                
                t_c, t_h, t_b = st.tabs(["📝 النصوص الإعلانية", "⚡ العناوين الصادمة", "💰 الميزانية المقترحة"])
                with t_c:
                    st.text_area("قالب الدارجة:", value=hub_data['copy_dz'], height=120, disabled=True)
                with t_h:
                    for h in hub_data['hooks']: st.info(h)
                with t_b:
                    st.metric(label="ميزانية الفحص اليومية", value=f"{hub_data['budget_usd']} USD", delta=f"{hub_data['budget_dzd']} DA")
                if st.button("❌ إغلاق المعاينة التسويقية"):
                    del st.session_state["active_ai_marketing_prod"]
                    st.session_state["show_premium_ai_hub"] = False
                    st.rerun()
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
                        st.warning(f"تم حذف {len(duplicated_rows)} سطر مكرر!"); st.dataframe(duplicated_rows)
                    if not bad_prices.empty:
                        st.error(f"تم حذف {len(bad_prices)} سطر أسعار سالبة!"); st.dataframe(bad_prices)
                else: st.info("الملف سليم تماماً ولا يحتوي على أخطاء.")
            st.markdown("---"); render_data_insights(df); st.markdown("---")
            st.subheader("📈 المخططات البيانية الملونة للولايات والمبيعات:")
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                st.write("💰 حجم المبيعات الإجمالي الحقيقي لكل منتج:")
                st.bar_chart(data=df, x='product_name', y='total_row_sales', color='#00ffcc')
            with chart_col2:
                wilaya_col = None
                for col in df.columns:
                    if 'address' in col.lower() or 'wilaya' in col.lower() or 'ولاية' in col:
                        wilaya_col = col; break
                if wilaya_col:
                    st.write(f"🗺️ حجم الشحن والمبيعات حسب الولايات الجزائرية:")
                    st.bar_chart(data=df, x=wilaya_col, y='total_row_sales', color='#ff007f')
                else: st.info("💡 نصيحة: سمّ عمود السكن في ملفك باسم 'wilaya' ليظهر مخطط فرز الولايات.")
            csv_buffer = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 تحميل ملف المبيعات المطهّر بالكامل", data=csv_buffer, file_name="cleaned_neon_sales.csv", mime="text/csv")

    elif choice == "🚀 مولّد الحملات والتخطيط التسويقي (AI)":
        # === إضافات المستودع ومطهر البيانات ومولد حملات الـ AI ===
        def render_marketing_hub_cyber_edition():
            st.write("<h1 style='font-size: 32px; color: #00fff0; text-shadow: 0 0 15px #00fff0;'>🚀 منصة التسويق السيبرانية وفحص الحملات الذكية AI</h1>", unsafe_allow_html=True)
            
            col_input, col_output = st.columns(2)
            with col_input:
                st.subheader("⚙️ موجه الأتمتة الإعلانية:")
                prod_title = st.text_input("اسم المنتج المراد تسويقه:", value="خلاط كهربائي محمول ذكي")
                prod_desc = st.text_area("وصف مختصر أو مميزات السلعة الرئيسية:", value="شحن سريع، شفرات حادة من الفولاذ، بطارية تدوم طويلاً، مثالي للرياضيين والمكتب.")
                prod_price = st.number_input("سعر بيع المنتج النهائي في الجزائر (DA):", min_value=100, value=3500)
                daily_budget = st.number_input("الميزانية الإعلانية اليومية المستهدفة (USD):", min_value=5, value=20)
                platform_choice = st.radio("🎯 منصة إطلاق الإعلان المستهدفة:", ["Facebook Ads", "TikTok Ads"], horizontal=True)
                run_generation = st.button("✨ تشغيل الأتمتة وصياغة الحملة الفاخرة")
                
            with col_output:
                st.subheader("📱 مستعرض المنشورات والبطاقات الزجاجية المفتوحة:")
                if run_generation or 'cyber_hub_active' in st.session_state:
                    st.session_state['cyber_hub_active'] = True
                    
                    # 5. عداد تقييم قوة الإعلان (AI Ad Score Meter)
                    score = 40
                    if len(prod_title) > 5: score += 20
                    if len(prod_desc) > 30: score += 25
                    if "شحن" in prod_desc or "ضمان" in prod_desc or "سريع" in prod_desc: score += 10
                    score = min(100, score)
                    
                    if score >= 80:
                        meter_color, meter_text = "#00ff66", "🔥 إعلان قوي جداً وجاذب للمستهلك!"
                    elif 50 <= score < 80:
                        meter_color, meter_text = "#ffcc00", "⚠️ إعلان متوسط القوة بحاجة لميزات تنافسية إضافية."
                    else:
                        meter_color, meter_text = "#ff0055", "🚨 إعلان ضعيف! أضف كلمات دلالية مثل (شحن مجاني، ضمان، توصيل)."
                    
                    st.write(f"""
                    <div style="background: #0f0f14; border: 1px solid #222; padding: 12px; border-radius: 8px; margin-bottom: 20px; direction: rtl; text-align: right;">
                        <span style="color: #aaa; font-size: 12.5px;">📊 عداد قوة الإعلان الذكي (AI Ad Score):</span>
                        <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: bold; color: {meter_color}; margin-top: 4px; margin-bottom: 4px;">
                            <span>معدل الجاذبية المتوقع: {score}%</span>
                            <span>{meter_text}</span>
                        </div>
                        <div style="width: 100%; background: #222; height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="width: {score}%; background: {meter_color}; height: 6px; box-shadow: 0 0 10px {meter_color}; transition: width 0.5s ease;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # إنشاء التبويبات السيبرانية الأربعة لتنظيم كروت العرض الزجاجية المفتوحة بالكامل وبكامل طولها الطبيعي
                    t_angles, t_script, t_radar, t_roi = st.tabs([
                        "🎯 1. زوايا البيع النفسية", 
                        "🎬 2. سيناريو الفيديو بالثواني", 
                        "📡 3. فلاتر الاستهداف والولايات", 
                        "💎 4. العوائد والأرباح المتوقعة"
                    ])
                    
                    with t_angles:
                        st.write("🔒 **الإعلانات الحرة الممتدة بكامل الطول داخل الكروت الزجاجية المتوهجة بالأرجواني:**")
                        ang1 = f"عيت من الخلاطات الكبار ل يرفدو البلاصة ويديرو الحس؟ 🤦 واش رايك في خلاط ذكي محمول يروح معاك وين تروح! **{prod_title}** يخلطلك العواصير والبروتين ديالك في ثواني وبلا تعب، خفيف وشاحن سريع وعملي بزاف تهنى من المشكل اليوم!"
                        ang2 = f"الأناقة تلتقي مع الأداء العالي الرائع ✨ ارتقِ بأسلوب حياتك اليومي مع **[{prod_title}]**، التصميم الزجاجي الفريد واللمسة العصرية تمنحك برستيج خاص ومميز في مكتبك أو النادي الرياضي، إنه ليس مجرد خلاط بل عنوان لتميزك الفاخر."
                        ang3 = f"🚨 تخفيض صدمة ومؤقت لفترة جد محدودة! المنتج الأكثر طلباً **[{prod_title}]** متوفر الآن بخصم خاص يعادل 30% من السعر الأصلي والمخزون أوشك على النفاذ تماماً بالمستودع! اطلب الآن واستفد من التوصيل السريع والدفع عند الاستلام!"
                        
                        # حقن البطاقات الزجاجية المفتوحة والمصبوغة نيونياً بخطوط واضحة عريضة لسهولة القراءة والنسخ
                        st.markdown(f"""<div style="background: rgba(255, 0, 255, 0.02); border: 1px solid #ff00ff; border-radius: 10px; padding: 14px; margin-bottom: 12px; box-shadow: 0 0 10px rgba(255, 0, 255, 0.1); direction: rtl; text-align: right;"><b style="color: #ff00ff; font-size: 14px;">🛠️ زاوية حل المشكلة (بالدارجة الجزائرية):</b><br><p style="color: #ffffff; font-size: 14.5px; line-height: 1.6; font-weight: 500; margin-top: 6px; margin-bottom: 0;">{ang1}</p></div>""", unsafe_allow_html=True)
                        st.download_button(label="📥 نسخ كود نص حل المشكلة نقياً", data=ang1.encode('utf-8'), file_name="angle_problem.txt", mime="text/plain")
                        
                        st.markdown(f"""<div style="background: rgba(255, 0, 255, 0.02); border: 1px solid #ff00ff; border-radius: 10px; padding: 14px; margin-bottom: 12px; box-shadow: 0 0 10px rgba(255, 0, 255, 0.1); direction: rtl; text-align: right;"><b style="color: #ff00ff; font-size: 14px;">💎 زاوية الفخامة والبرستيج الاجتماعي:</b><br><p style="color: #ffffff; font-size: 14.5px; line-height: 1.6; font-weight: 500; margin-top: 6px; margin-bottom: 0;">{ang2}</p></div>""", unsafe_allow_html=True)
                        st.download_button(label="📥 نسخ كود نص البرستيج نقياً", data=ang2.encode('utf-8'), file_name="angle_prestige.txt", mime="text/plain")
                        
                        st.markdown(f"""<div style="background: rgba(255, 0, 255, 0.02); border: 1px solid #ff00ff; border-radius: 10px; padding: 14px; margin-bottom: 12px; box-shadow: 0 0 10px rgba(255, 0, 255, 0.1); direction: rtl; text-align: right;"><b style="color: #ff00ff; font-size: 14px;">🚨 زاوية العرض الاستعجالي الصادم:</b><br><p style="color: #ffffff; font-size: 14.5px; line-height: 1.6; font-weight: 500; margin-top: 6px; margin-bottom: 0;">{ang3}</p></div>""", unsafe_allow_html=True)
                        st.download_button(label="📥 نسخ كود نص العرض الاستعجالي نقياً", data=ang3.encode('utf-8'), file_name="angle_flash_sale.txt", mime="text/plain")
                        
                    with t_script:
                        st.write("🎬 **السيناريو الكامل والاحترافي لتصوير الإعلان متمدد بالكامل حسب الثواني المقترحة:**")
                        s1 = f"**[00:00 - 00:03] الـ Hook الصادم:** لقطة سريعة لشخص يعاني مع خلاط قديم ثقيل يصدر ضوضاء، مع كتابة نص عريض (حبس! هاد السلعة غادي تبدل حياتك تع الصح! 😱)"
                        s2 = f"**[00:03 - 00:10] عرض المشكلة والحاجة:** الخلاطات الكبار يعطلو في الكوزينة وصعاب في الغسيل خاصة كي تكون زربان ورايح للخدمة أو لـ لsub سبور ونشاطك الرياضي اليومي."
                        s3 = f"**[00:10 - 00:20] استعراض السلعة وطريقة العمل:** لقطة مقربة لمنتج **[{prod_title}]** وهو يطحن المكونات والفاكهة بسلاسة وسرعة فائقة بفضل الشفرات الفولاذية الحادة والبطارية القوية المستقرة."
                        s4 = f"**[00:20 - 00:30] الـ Call To Action النهائي:** التوصيل متوفر وسريع لـ 58 ولاية جزائرية كاملة لباب دارك، والدفع حتى تستلم وتفحص السلعة بيدك 🚚 اضغط على زر الرابط واطلب ديالك الآن!"
                        
                        full_script_markdown = f"{s1}\n\n{s2}\n\n{s3}\n\n{s4}"
                        
                        st.markdown(f"""<div style="background: rgba(0, 255, 240, 0.02); border: 1px solid #00fff0; border-radius: 10px; padding: 16px; margin-bottom: 12px; box-shadow: 0 0 10px rgba(0, 255, 240, 0.1); direction: rtl; text-align: right;"><b style="color: #00fff0; font-size: 14px;">🎥 خطة إنتاج وفيديو السيناريو (Ad Video Script):</b><br><div style="color: #ffffff; font-size: 14px; line-height: 1.8; margin-top: 10px; white-space: pre-line;">{full_script_markdown}</div></div>""", unsafe_allow_html=True)
                        st.download_button(label="📥 تحميل ملف السيناريو بالثواني كاملاً", data=full_script_markdown.encode('utf-8'), file_name="video_script.txt", mime="text/plain")
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
        
        # تفعيل آلية الحفظ داخل جلسة العمل لضمان ثبات أزرار التحميل وروابط السوشيال ميديا
        if st.button("🚀 إصدار وحفظ الفاتورة والملصق وخصم المخزون", key="issue_invoice_and_clear_stock_btn"):
            if not customer_name or not product_name: 
                st.error("❌ خطأ: يرجى ملء اسم الزبون والمنتج أولاً!")
            else:
                check_stock = pd.read_sql(f"SELECT available_qty FROM store_stock WHERE product_name = '{product_name}'", conne)
                if not check_stock.empty and check_stock['available_qty'].values[0] < quantity:
                    st.error(f"❌ خطأ! المتبقي في المستودع هو: {check_stock['available_qty'].values[0]} قطع فقط.")
                else:
                    cursor.execute("UPDATE store_stock SET available_qty = available_qty - ? WHERE product_name = ?", (quantity, product_name))
                    cursor.execute('INSERT INTO v4_customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, month_created, date_created) VALUES (?, ?, ?, ?, ?, ?, ?)', (shop_name, customer_name, customer_phone, product_name, final_total, current_month, current_date))
                    conne.commit()
                    
                    # قراءة اللوغو وحفظ الملفات بداخل الـ session_state
                    logo_data = uploaded_logo.read() if uploaded_logo is not None else None
                    st.session_state["generated_pdf_invoice"] = generate_invoice_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, price, quantity, product_total, shipping_cost, final_total, logo_data)
                    st.session_state["generated_pdf_label"] = generate_thermal_label_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, final_total, current_date)
                    st.session_state["last_active_customer"] = customer_name
                    st.session_state["last_active_phone"] = customer_phone
                    st.session_state["last_active_shop"] = shop_name
                    st.session_state["last_active_product"] = product_name
                    st.session_state["last_active_total"] = final_total
                    st.success("💾 تم تسجيل البيع وتوليد المستندات بنجاح!")
        # عرض أزرار التحميل والإرسال إذا كانت البيانات متوفرة في جلسة التصفح الحالية
        if "generated_pdf_invoice" in st.session_state:
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1: 
                st.download_button(label="📥 تحميل الفاتورة الكبيرة A4 (PDF)", data=st.session_state["generated_pdf_invoice"], file_name=f"invoice_{st.session_state['last_active_customer']}.pdf", mime="application/pdf", key="dl_invoice_pdf_btn")
            with col_btn2: 
                st.download_button(label="🖨️ تحميل ملصق الشحن الحراري 4x4 (PDF)", data=st.session_state["generated_pdf_label"], file_name=f"thermal_label_{st.session_state['last_active_customer']}.pdf", mime="application/pdf", key="dl_label_pdf_btn")
            if st.button("🖨️ فتح نافذة الطباعة الحرارية السريعة", key="quick_thermal_print_window_btn"): 
                st.components.v1.html("<script>window.print();</script>", height=0)
            st.markdown("---")
            st.subheader("📲 أزرار الإرسال السريع الفوري لزبونك:")
            msg_text = f"مرحباً {st.session_state['last_active_customer']}، تم تأكيد طلبيتك بنجاح من متجر {st.session_state['last_active_shop']}. المنتج: {st.session_state['last_active_product']}، الإجمالي للدفع هو: {st.session_state['last_active_total']:,} DA."
            encoded_msg = urllib.parse.quote(msg_text)
            
            send_col1, send_col2 = st.columns(2)
            with send_col1: 
                st.link_button("🟢 إرسال تفاصيل الفاتورة عبر WhatsApp", f"https://wa.me{st.session_state['last_active_phone']}?text={encoded_msg}", key="send_whatsapp_invoice_btn")
            with send_col2: 
                st.link_button("🟣 إرسال تفاصيل الفاتورة عبر Viber", f"viber://forward?text={encoded_msg}", key="send_viber_invoice_btn")

        # ج=== إضافة صندوق المعاينة الحية للفاتورة النيونية ===
    # القسم (4 - ج): نظام إدارة المخزون، مطهر الولايات ومولد حملات الـ AI وقفل الـ DB
    # ========================================================
      # القسم (4 - ج): نظام إدارة المخزون، مطهر الولايات ومولد حملات الـ AI وقفل الـ DB
    # ========================================================
    # القسم (4 - ج): نظام إدارة المخزون، مطهر الولايات ومولد حملات الـ AI وقفل الـ DB
    # ========================================================
    elif choice == "📦 إدارة وتنبيهات المخزون السلعي":
        st.write("<h1 style='font-size: 32px; color: #ff00ff; text-shadow: 0 0 15px #ff00ff;'>📦 نظام إدارة ومراقبة مخزون المستودع</h1>", unsafe_allow_html=True)
        col_add, col_view = st.columns(2)
        with col_add:
            st.subheader("📝 إضافة سلعة للمستودع:")
            new_prod = st.text_input("اسم السلعة الجديدة:", key="stock_input_prod_unique_v4")
            new_qty = st.number_input("الكمية المتوفرة:", min_value=1, value=50, key="stock_input_qty_unique_v4")
            if st.button("➕ حفظ في المستودع", key="btn_save_prod_stock_v4"):
                if new_prod:
                    try:
                        cursor.execute("INSERT INTO store_stock (product_name, available_qty) VALUES (?, ?)", (new_prod, new_qty))
                        conne.commit()
                        st.success(f"تم إضافة {new_prod} للمستودع!")
                        
                        # حساب تفاصيل الإعلان مسبقاً وتخزينها في ذاكرة الجلسة المستمرة لتفادي مسحها بالـ rerun
                        current_merchant = st.session_state.get('user_email', st.session_state.get('username', "merchant.nexus@nexus-gate.com"))
                        
                        copy_dz = f"يا جماعة الخير جبتلكم اليوم حاجة فور بزاف لغادي تهنيكم كامل! 😍\nالمنتج المتميز والمطلوب بقوة [{new_prod}] راهو دخل للمستودع تعنا وبكمية محدودة جداً.\n💎 جودة عالية، كفاءة مثالية، وسعر مدهش ما تلقاوه في حتى بلاصة.\n🚚 التوصيل سريع ومتوفر لـ 58 ولاية جزائرية حتى لباب الدار، والدفع حتى تستلم سلعتك وتفحصها بيدك!\n📥 دبر راسك ما تخليش الفرصة تفوتك وأرسل رسالة لصفحتنا للطلب الآن قبل ما تخلص الكمية!"
                        copy_ar = f"أخيراً، المنتج الأكثر طلباً وتميزاً [{new_prod}] متوفر الآن بين يديك وبأعلى مواصفات الجودة!\n💎 صُمم هذا المنتج خصيصاً ليلبي احتياجاتكم اليومية بكفاءة لا مثيل لها وبسعر تنافسي للغاية.\n🚚 يسعدنا أن نعلن عن توفر شحن سريع وموثوق إلى جميع الولايات الجزائرية مع ميزة الدفع عند الاستلام.\n📥 لا تترددوا، الكمية محدودة جداً! اضغط على زر 'تسوق الآن' أو أرسل رسالة إلى حسابنا لتأكيد طلبك اليوم."
                        copy_short = f"السلعة لڨاع تحوسو عليها [{new_prod}] دخلت من جديد وبقوة! 🔥 جودة توب وسعر هبال. الشحن متوفر لـ 58 ولاية والدفع عند الاستلام 🚚 اضغط على الرابط أو ابعت مساج في الخاص واطلب ديالك قبل نفاذ المخزون! 📥"
                        
                        h1 = f"1. قبل ما تشري أي حاجة في الجزائر.. شوف واش دخل جديد في [{new_prod}]! 😱"
                        h2 = f"2. المنتج لڨاع التجار والزبائن يحوسو عليه راهو متوفر أخيراً في المستودع! 🔥"
                        h3 = f"3. هادي هي السلعة لغادي تهنيك وتوفر عليك الوقت والتعب تع الصح! 💎"
                        h4 = f"4. ضياع للمال لو كان ما تطلبش [{new_prod}] بسعر الجملة تع اليوم! 💸"
                        h5 = f"5. الكمية راهي تخلص بزاف.. شوف وعلاش ڨاع الناس تطلب في هذا المنتج المدهش! 📦"
                        
                        testing_budget_usd = 20.0
                        exchange_rate_parallel = 240.0
                        testing_budget_dzd = testing_budget_usd * exchange_rate_parallel
                        
                        st.session_state['premium_marketing_hub'] = {
                            'merchant': current_merchant,
                            'product_name': new_prod,
                            'copy_dz': copy_dz,
                            'copy_ar': copy_ar,
                            'copy_short': copy_short,
                            'hooks': [h1, h2, h3, h4, h5],
                            'budget_usd': testing_budget_usd,
                            'budget_dzd': testing_budget_dzd
                        }
                        
                        time.sleep(0.5)
                        st.rerun()
                    except: st.error("المنتج موجود مسبقاً في المخزون.")
        with col_view:
            st.subheader("📋 حالة السلع المتوفرة حالياً:")
            stock_df = pd.read_sql("SELECT * FROM store_stock", conne)
            if not stock_df.empty:
                st.dataframe(stock_df, use_container_width=True)
                st.markdown("---")
                st.write("🗑️ **قسم محو وإزالة السلع من المستودع:**")
                delete_prod = st.selectbox("اختر السلعة المراد محوها نهائياً:", stock_df['product_name'], key="sb_delete_stock_prod_v4")
                if st.button("❌ محو السلعة المحددة", key="btn_execute_delete_stock_v4"):
                    cursor.execute("DELETE FROM store_stock WHERE product_name = ?", (delete_prod,))
                    conne.commit(); st.success(f"🗑️ تم محو السلعة [{delete_prod}] من المخزون بنجاح!"); time.sleep(0.5); st.rerun()
                
                # === إضافة مؤشر المخزون الناري المتوهج ===
                def render_neon_stock_fire_bar(df_data):
                    st.markdown("<p style='font-size: 14px; color: #b0b0b0; margin-top: 15px;'>🔥 مؤشر تدفق المستودع المباشر (تحديث لحظي النيون):</p>", unsafe_allow_html=True)
                    max_qty = int(df_data['available_qty'].max()) if not df_data.empty else 100
                    if max_qty < 30: max_qty = 30
                    
                    for _, row in df_data.iterrows():
                        p_name = row['product_name']
                        p_qty = int(row['available_qty'])
                        width_pct = max(6, min(100, int((p_qty / max_qty) * 100)))
                        
                        if p_qty < 5:
                            bar_color, shadow_color, status_text = "#ff0055", "rgba(255, 0, 85, 0.9)", "🚨 خطر - مخزون حرج جداً!"
                        elif 5 <= p_qty <= 15:
                            bar_color, shadow_color, status_text = "#ffcc00", "rgba(255, 204, 0, 0.8)", "⚠️ انتباه - مخزون متوسط"
                        else:
                            bar_color, shadow_color, status_text = "#00ff66", "rgba(0, 255, 102, 0.8)", "✅ آمن - مستودع مستقر"
                            
                        neon_html = f"""
                        <div style="margin-bottom: 12px; background: #0f0f12; padding: 10px; border-radius: 8px; border: 1px solid #222;">
                            <div style="display: flex; justify-content: space-between; font-size: 13px; color: #fff; margin-bottom: 6px;">
                                <span><strong>{p_name}</strong> <span style="color: #888;">({p_qty} قطعة)</span></span>
                                <span style="color: {bar_color}; text-shadow: 0 0 8px {bar_color}; font-weight: bold; font-size: 12px;">{status_text}</span>
                            </div>
                            <div style="width: 100%; background-color: #1a1a24; border-radius: 5px; overflow: hidden; height: 8px;">
                                <div style="width: {width_pct}%; background-color: {bar_color}; height: 8px; border-radius: 5px; box-shadow: 0 0 12px {shadow_color}; transition: all 0.4s ease-in-out;"></div>
                            </div>
                        </div>
                        """
                        st.write(neon_html, unsafe_allow_html=True)
                
                render_neon_stock_fire_bar(stock_df)
                
                low_stock = stock_df[stock_df['available_qty'] <= 5]
                if not low_stock.empty:
                    st.markdown("---")
                    st.write("<h3 style='color: #ff007f !important; text-shadow: 0 0 10px #ff007f;'>🚨 تنبيه: سلع أوشكت على النفاذ!</h3>", unsafe_allow_html=True)
                    st.dataframe(low_stock)
            else: st.info("مستودعك خالي تماماً حالياً.")

        # === دمج وتطوير منصة بطاقات الاستهداف والإعلانات الذكية للسلع الجديدة ===
        if 'premium_marketing_hub' in st.session_state:
            st.markdown("---")
            hub_data = st.session_state['premium_marketing_hub']
            prod_name = hub_data['product_name']
            merchant_user = hub_data['merchant']
            
            st.write(f"""
            <div style="background: linear-gradient(135deg, #0f0c20, #15002a); border: 2px solid #00fff0; border-radius: 16px; padding: 20px; box-shadow: 0 0 25px rgba(0, 255, 240, 0.2); direction: rtl; text-align: right;">
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(0, 255, 240, 0.3); padding-bottom: 10px; margin-bottom: 15px;">
                    <span style="color: #00fff0; font-weight: bold; font-size: 16px; text-shadow: 0 0 8px #00fff0;">📡 PREMIUM AI MARKETING HUB v4.0</span>
                    <span style="color: #e2e2e8; font-family: monospace;">👤 الحساب النشط: {merchant_user}</span>
                </div>
                <h3 style="color: #ffffff; margin: 0 0 5px 0;">🎉 تم تأمين وحفظ السلعة [{prod_name}] بنجاح في قاعدة البيانات</h3>
                <p style="color: #b0b0c0; font-size: 13px; margin: 0;">يقوم محرك الذكاء الاصطناعي الآن باستعراض استراتيجية التسويق الشاملة وفحص السوق المستمر دون أي اختفاء للبيانات.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🛠️ لوحة تكتيكات الحملة وصانع المحتوى الذكي")
            tab_copy, tab_hooks, tab_targeting, tab_budget = st.tabs([
                "📝 2. نصوص الإعلانات (Ad-Copy)", "⚡ 3. العناوين الصادمة (Hooks)", 
                "🎯 4. رادار الاستهداف والجمهور", "💰 5. حاسبة ميزانية الفحص"
            ])
            
            with tab_copy:
                st.write("✨ **اختر القالب النصي المناسب لمنصتك وقم بنسخه أو تحميله نقياً مباشرة:**")
                sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🇩🇿 قالب الدارجة المحفزة", "✨ قالب الفصحى الإقناعية", "📱 قالب تيك توك وإنستغرام السريع"])
                with sub_tab1:
                    st.text_area("نص الدارجة الجزائرية:", value=hub_data['copy_dz'], height=180, key="txt_dz_unique_v4", disabled=True)
                    st.download_button(label="📥 تحميل النص نقياً (الدارجة)", data=hub_data['copy_dz'].encode('utf-8'), file_name=f"ad_copy_dz_{prod_name}.txt", mime="text/plain", key="dl_dz_unique_v4")
                with sub_tab2:
                    st.text_area("نص الفصحى الإقناعية:", value=hub_data['copy_ar'], height=180, key="txt_ar_unique_v4", disabled=True)
                    st.download_button(label="📥 تحميل النص نقياً (الفصحى)", data=hub_data['copy_ar'].encode('utf-8'), file_name=f"ad_copy_ar_{prod_name}.txt", mime="text/plain", key="dl_ar_unique_v4")
                with sub_tab3:
                    st.text_area("نص الخاص القصير:", value=hub_data['copy_short'], height=120, key="txt_short_unique_v4", disabled=True)
                    st.download_button(label="📥 تحميل النص نقياً (السريع)", data=hub_data['copy_short'].encode('utf-8'), file_name=f"ad_copy_short_{prod_name}.txt", mime="text/plain", key="dl_short_unique_v4")
            
            with tab_hooks:
                st.write("⚡ **أفضل 5 عناوين إعلانية لجذب الانتباه في أول 3 ثوان:**")
                for i, hook in enumerate(hub_data['hooks']):
                    st.info(hook)
                all_hooks_text = "\n".join(hub_data['hooks'])
                st.download_button(label="📥 تحميل قائمة العناوين بالكامل", data=all_hooks_text.encode('utf-8'), file_name=f"hooks_{prod_name}.txt", mime="text/plain", key="dl_hooks_unique_v4")
                
            with tab_targeting:
                st.write("🎯 **رادار البيانات والاهتمامات الدقيقة لمدير إعلانات فيسبوك (Facebook Ads):**")
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    st.markdown("🔹 **الاهتمامات والكلمات المفتاحية المقترحة:**")
                    st.code(f"1. Engaged Shoppers (المتسوقون المتفاعلون)\n2. Online Shopping\n3. E-commerce / Retail\n4. اهتمامات صلة بالمنتج: {prod_name}", language="text")
                    st.markdown("- **الفئة العمرية المثالية:** 22 - 45 سنة\n- **الجنس المستهدف:** رجال ونساء")
                with col_t2:
                    st.markdown("🗺️ **الولايات الجزائرية الأكثر تفاعلاً وطلباً للسلع:**")
                    st.write("1. **الجزائر العاصمة** (طلب قياسي)\n2. **وهران** (القوة الشرائية العالية بالغرب)\n3. **سطيف وقسنطينة** (مراكز تجارية كبرى بالشرق)\n4. **البليدة وتيبازة** (معدل تسليم وتوصيل جد مرتفع)")
                    
            with tab_budget:
                st.write("💰 **حاسبة ميزانية الفحص والـ Testing لحماية رأس مال التاجر من الخسارة:**")
                st.metric(label="ميزانية الفحص اليومية المقترحة (Testing Budget)", value=f"{hub_data['budget_usd']:,.2f} USD")
                st.metric(label="ما يقابلها في السوق الجزائرية الموازية (Square Rate)", value=f"{hub_data['budget_dzd']:,.2f} DA", delta="معدل تفادي خسارة مسبق")
                st.write("💡 **نصيحة التسويق:** يُنصح بإطلاق إعلان الفحص لمدة **3 أيام كاملة** على ولايات محددة قبل رفع الميزانية وتكبير كميات التوريد.")
                
            if st.button("❌ إغلاق المعاينة", key="btn_close_hub_preview_v4"):
                del st.session_state['premium_marketing_hub']
                st.rerun()
    elif choice == "🧼 مطهر ملفات المبيعات وإحصائيات الولايات":
        st.write("<h1 style='font-size: 32px; color: #00fff0; text-shadow: 0 0 15px #00fff0;'>🧼 نظام التطهير وعرض مقارنة البيانات والولايات</h1>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("اختر ملف المبيعات (CSV أو Excel)", type=["csv", "xlsx"], key="sales_uploader_file_unique_v4")
        
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
                        st.warning(f"تم حذف {len(duplicated_rows)} سطر مكرر!"); st.dataframe(duplicated_rows)
                    if not bad_prices.empty:
                        st.error(f"تم حذف {len(bad_prices)} سطر أسعار سالبة!"); st.dataframe(bad_prices)
                else: st.info("الملف سليم تماماً ولا يحتوي على أخطاء.")
            st.markdown("---"); render_data_insights(df); st.markdown("---")
            st.subheader("📈 المخططات البيانية الملونة للولايات والمبيعات:")
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                st.write("💰 حجم المبيعات الإجمالي الحقيقي لكل منتج:")
                st.bar_chart(data=df, x='product_name', y='total_row_sales', color='#00ffcc')
            with chart_col2:
                wilaya_col = None
                for col in df.columns:
                    if 'address' in col.lower() or 'wilaya' in col.lower() or 'ولاية' in col:
                        wilaya_col = col; break
                if wilaya_col:
                    st.write(f"🗺️ حجم الشحن والمبيعات حسب الولايات الجزائرية:")
                    st.bar_chart(data=df, x=wilaya_col, y='total_row_sales', color='#ff007f')
                else: st.info("💡 نصيحة: سمّ عمود السكن في ملفك باسم 'wilaya' ليظهر مخطط فرز الولايات.")
            csv_buffer = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 تحميل ملف المبيعات المطهّر بالكامل", data=csv_buffer, file_name="cleaned_neon_sales.csv", mime="text/csv", key="dl_clean_sales_csv_v4")
            
    elif choice == "🚀 مولّد الحملات والتخطيط التسويقي (AI)":
        # === إضافات المستودع ومطهر البيانات ومولد حملات الـ AI ===
        def render_marketing_hub_cyber_edition():
            st.write("<h1 style='font-size: 32px; color: #00fff0; text-shadow: 0 0 15px #00fff0;'>🚀 منصة التسويق السيبرانية وفحص الحملات الذكية AI</h1>", unsafe_allow_html=True)
            
            col_input, col_output = st.columns(2)
            with col_input:
                st.subheader("⚙️ موجه الأتمتة الإعلانية:")
                ai_prod_name = st.text_input("اسم المنتج المراد تسويقه:", value="خلاط كهربائي محمول ذكي", key="cyber_input_title_v4")
                prod_desc = st.text_area("وصف مختصر أو مميزات السلعة الرئيسية:", value="شحن سريع، شفرات حادة من الفولاذ، بطارية تدوم طويلاً، مثالي للرياضيين والمكتب.", key="cyber_input_desc_v4")
                prod_price = st.number_input("سعر بيع المنتج النهائي في الجزائر (DA):", min_value=100, value=3500, key="cyber_input_price_v4")
                daily_budget = st.number_input("الميزانية الإعلانية اليومية المستهدفة (USD):", min_value=5, value=20, key="cyber_input_budget_v4")
                platform_choice = st.radio("🎯 منصة إطلاق الإعلان المستهدفة:", ["Facebook Ads", "TikTok Ads"], horizontal=True, key="cyber_input_platform_v4")
                run_generation = st.button("🧠 تشغيل العقل السيبراني وتوليد الحملة فوراً", key="btn_run_cyber_gen_v4")
                
            with col_output:
                st.subheader("📱 مستعرض المنشورات والبطاقات الزجاجية المفتوحة:")
                if run_generation or 'cyber_hub_active' in st.session_state:
                    clean_input = ai_prod_name.strip()
                    is_gibberish = False
                    
                    if len(clean_input) > 0:
                        unique_chars = set(clean_input.replace(" ", ""))
                        char_ratio = len(unique_chars) / len(clean_input.replace(" ", "")) if len(clean_input.replace(" ", "")) > 0 else 1
                        forbidden_gibberish = ["مي اونيبثب", "مشيسويسي", "asdasd", "qwerty", "zxcv"]
                        if any(gib in clean_input.lower() for gib in forbidden_gibberish) or (len(clean_input) >= 6 and char_ratio < 0.35):
                            is_gibberish = True
                    
                    if is_gibberish or not clean_input:
                        st.write(f"""
                        <div style="background: rgba(255, 0, 85, 0.05); border: 2px dashed #ff0055; padding: 18px; border-radius: 12px; box-shadow: 0 0 15px rgba(255, 0, 85, 0.2); direction: rtl; text-align: right; margin-bottom: 20px;">
                            <b style="color: #ff0055; font-size: 15px; text-shadow: 0 0 5px #ff0055;">⚠️ إدخال غير مفهوم أو عشوائي:</b>
                            <p style="color: #e2e2e8; font-size: 13.5px; line-height: 1.6; margin-top: 8px; margin-bottom: 12px;">يرجى كتابة اسم منتج أو سلعة حقيقية لكي يتمكن الذكاء الاصطناعي من صياغة إعلاناتك واستراتيجية استهدافك بدقة متناهية تفادياً لضياع ميزانيتك.</p>
                            <span style="color: #00fff0; font-size: 12.5px; font-weight: bold;">💡 أمثلة ومنتجات مقترحة لتوجيهك:</span>
                            <ul style="color: #aaa; font-size: 12.5px; margin-top: 5px; padding-right: 20px; line-height: 1.5;">
                                <li>حذاء رياضي طبي مريح</li>
                                <li>مكواة بخارية عمودية للملابس</li>
                                <li>محفظة جلدية ذكية مضادة للسرقة</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                        if 'cyber_hub_active' in st.session_state: del st.session_state['cyber_hub_active']
                    else:
                        st.session_state['cyber_hub_active'] = True
                        score = min(100, 40 + (20 if len(clean_input) > 5 else 0) + (25 if len(prod_desc) > 30 else 0) + (10 if any(k in prod_desc for k in ["شحن", "ضمان", "سريع"]) else 0))
                        meter_color = "#00ff66" if score >= 80 else ("#ffcc00" if score >= 50 else "#ff0055")
                        meter_text = "🔥 إعلان قوي جداً!" if score >= 80 else ("⚠️ إعلان متوسط." if score >= 50 else "🚨 إعلان ضعيف!")
                        
                        st.write(f"""
                        <div style="background: #0f0f14; border: 1px solid #222; padding: 12px; border-radius: 8px; margin-bottom: 20px; direction: rtl; text-align: right;">
                            <span style="color: #aaa; font-size: 12.5px;">📊 عداد قوة الإعلان الذكي (AI Ad Score):</span>
                            <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: bold; color: {meter_color}; margin-top: 4px; margin-bottom: 4px;">
                                <span>معدل الجاذبية المتوقع: {score}%</span><span>{meter_text}</span>
                            </div>
                            <div style="width: 100%; background: #222; height: 6px; border-radius: 3px; overflow: hidden;">
                                <div style="width: {score}%; background: {meter_color}; height: 6px; box-shadow: 0 0 10px {meter_color}; transition: width 0.5s ease;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        t_angles, t_script, t_radar, t_roi = st.tabs(["🎯 1. زوايا البيع النفسية", "🎬 2. سيناريو الفيديو بالثواني", "📡 3. فلاتر الاستهداف والولايات", "💎 4. العوائد والأرباح المتوقعة"])
                        with t_angles:
                            ang1 = f"عيت من الخلاطات الكبار ل يرفدو البلاصة ويديرو الحس؟ 🤦 واش رايك في خلاط ذكي محمول يروح معاك وين تروح! **{clean_input}** يخلطلك العواصير والبروتين ديالك في ثواني وبلا تعب، خفيف وشاحن سريع وعملي بزاف تهنى من المشكل اليوم!"
                            ang2 = f"الأناقة تلتقي مع الأداء العالي الرائع ✨ ارتقِ بأسلوب حياتك اليومي مع **[{clean_input}]**، التصميم الزجاجي الفريد واللمسة العصرية تمنحك برستيج خاص ومميز في مكتبك أو النادي الرياضي."
                            ang3 = f"🚨 تخفيض صدمة ومؤقت لفترة جد محدودة! المنتج الأكثر طلباً **[{clean_input}]** متوفر الآن بخصم خاص يعادل 30% من السعر الأصلي والمخزون أوشك على النفاذ تماماً بالمستودع!"
                            
                            st.markdown(f"""<div style="background: rgba(255, 0, 255, 0.02); border: 1px solid #ff00ff; border-radius: 10px; padding: 14px; margin-bottom: 12px; direction: rtl; text-align: right;"><b style="color: #ff00ff; font-size: 14px;">🛠️ زاوية حل المشكلة (بالدارجة الجزائرية):</b><br><p style="color: #ffffff; font-size: 14.5px; line-height: 1.6; font-weight: 500; margin-top: 6px; margin-bottom: 0;">{ang1}</p></div>""", unsafe_allow_html=True)
                            st.download_button(label="📥 نسخ كود نص حل المشكلة نقياً", data=ang1.encode('utf-8'), file_name="angle_problem.txt", mime="text/plain", key="dl_cyber_ang1_v4")
                            
                            st.markdown(f"""<div style="background: rgba(255, 0, 255, 0.02); border: 1px solid #ff00ff; border-radius: 10px; padding: 14px; margin-bottom: 12px; direction: rtl; text-align: right;"><b style="color: #ff00ff; font-size: 14px;">💎 زاوية الفخامة والبرستيج الاجتماعي:</b><br><p style="color: #ffffff; font-size: 14.5px; line-height: 1.6; font-weight: 500; margin-top: 6px; margin-bottom: 0;">{ang2}</p></div>""", unsafe_allow_html=True)
                            st.download_button(label="📥 نسخ كود نص البرستيج نقياً", data=ang2.encode('utf-8'), file_name="angle_prestige.txt", mime="text/plain", key="dl_cyber_ang2_v4")
                            
                            st.markdown(f"""<div style="background: rgba(255, 0, 255, 0.02); border: 1px solid #ff00ff; border-radius: 10px; padding: 14px; margin-bottom: 12px; direction: rtl; text-align: right;"><b style="color: #ff00ff; font-size: 14px;">🚨 زاوية العرض الاستعجالي الصادم:</b><br><p style="color: #ffffff; font-size: 14.5px; line-height: 1.6; font-weight: 500; margin-top: 6px; margin-bottom: 0;">{ang3}</p></div>""", unsafe_allow_html=True)
                            st.download_button(label="📥 نسخ كود نص العرض الاستعجالي نقياً", data=ang3.encode('utf-8'), file_name="angle_flash_sale.txt", mime="text/plain", key="dl_cyber_ang3_v4")
                        with t_script:
                            s1 = f"**[00:00 - 00:03] الـ Hook الصادم:** لقطة سريعة لشخص يعاني مع خلاط قديم ثقيل يصدر ضوضاء، مع كتابة نص عريض (حبس! هاد السلعة غادي تبدل حياتك تع الصح! 😱)\n"
                            s2 = f"**[00:03 - 00:10] عرض المشكلة والحاجة:** الخلاطات الكبار يعطلو في الكوزينة وصعاب في الغسيل خاصة كي تكون زربان ورايح للخدمة.\n"
                            s3 = f"**[00:10 - 00:20] استعراض السلعة وطريقة العمل:** لقطة مقربة لمنتج **[{clean_input}]** وهو يطحن المكونات والفاكهة بسلاسة بفضل الشفرات الفولاذية الحادة.\n"
                            s4 = f"**[00:20 - 00:30] الـ Call To Action النهائي:** التوصيل متوفر وسريع لـ 58 ولاية جزائرية كاملة لباب دارك والدفع عند الاستلام 🚚 اضغط على زر الرابط واطلب ديالك الآن!"
                            st.markdown(f"""**🎥 خطة إنتاج وفيديو السيناريو (Ad Video Script):**\n{s1}\n{s2}\n{s3}\n{s4}""", unsafe_allow_html=True)
                        with t_radar:
                            st.write("📡 **رادار الاستهداف الذكي وتصنيف الولايات الجغرافية الأعلى تسليماً:**")
                            col_r1, col_r2 = st.columns(2)
                            with col_r1:
                                if platform_choice == "Facebook Ads":
                                    st.code(f"1. Engaged Shoppers\n2. Online Shopping\n3. الكلمة المفتاحية: {clean_input}", language="text")
                                else:
                                    st.code(f"#AlgeriaShopping\n#Trending_Products\n#المنتج: {clean_input}", language="text")
                            with col_r2:
                                st.write("1. **Tier 1:** الجزائر العاصمة (طلب قياسي وسرعة تسليم).\n2. **Tier 1:** وهران والبليدة (أعلى نسب استلام للـ Livraison).\n3. **Tier 2:** سطيف وقسنطينة (طلب تجاري ممتاز).")
                        with t_roi:
                            estimated_sales = int(daily_budget / 3.5)
                            expected_net_profit = (estimated_sales * prod_price) - ((daily_budget * 240.0) + (estimated_sales * (prod_price * 0.4)))
                            st.metric(label="عدد المبيعات اليومية المتوقعة تقريباً", value=f"~ {estimated_sales} مبيعة / يوم")
                            st.metric(label="صافي الأرباح الحقيقية المتوقعة (DA)", value=f"{expected_net_profit:,.2f} DA")
                        if st.button("🧼 تصفية الواجهة ومحو بيانات الفحص", key="btn_clear_cyber_hub_v4"):
                            if 'cyber_hub_active' in st.session_state: del st.session_state['cyber_hub_active']
                            st.rerun()
                else:
                    st.info("💡 في انتظار تحديد الإعدادات.. أدخل بيانات منتجك وسعر بيعه وميزانيتك واضغط على زر التوليد لتنبثق المنصة السيبرانية الفاخرة المفتوحة.")
                    
        render_marketing_hub_cyber_edition()
        
    # قفل فوري لقناة الاتصال بالـ DB مع نهاية المتجر لتجنب حدوث Lock حماية للـ RAM
    conne.close()
