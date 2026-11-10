# ========================================================
# الجزء الأول المطور - [1 من 4]: النواة والتحقق الشبح (gate_core.py)
# ========================================================
import os
import zipfile
import io
from datetime import datetime
import streamlit as st
import pandas as pd
import sqlite3
import time
import urllib.parse
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def create_backup_vault():
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

# 🔒 ضبط إعدادات الشاشة الأساسية للمنصة الموحدة
st.set_page_config(page_title="NEXUS CENTRAL GATE v4", page_icon="👑", layout="wide")

# 📧 دالة إرسال البريد الإلكتروني الموحدة عبر Gmail SMTP (تدعم OTP والرسائل الترحيبية)
def send_gmail_notification(target_email, subject, body_text):
    try:
        sender_email = st.secrets["GMAIL_USER"]
        sender_password = st.secrets["GMAIL_APP_PASSWORD"]

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = target_email

        message.attach(MIMEText(body_text, "plain", "utf-8"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, target_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"⚠️ خطأ في إرسال البريد الإلكتروني: {e}")
        return False

# 🚨 [جدار الحماية الشبح الحاسم]: قراءة الرابط علوياً للتأكد من وجود مفتاحك السري (?role=boss)
query_params = st.query_params
is_boss_link = query_params.get("role") == "boss" if "role" in query_params else False
if "admin_master_logged" not in st.session_state:
    st.session_state["admin_master_logged"] = False

# ========================================================
# [القسم الثاني]: الحقن السيبراني وتصميم واجهات النيون الزجاجي
# ========================================================
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
    div[data-testid="stMetricBlock"], div[data-testid="metric-container"], .premium-card-cyan, .premium-card-pink {
        background: linear-gradient(135deg, rgba(15, 2, 20, 0.85) 0%, rgba(5, 5, 12, 0.98) 100%) !important;
        border: 2px solid #00fff0 !important;
        border-radius: 16px !important;
        box-shadow: 0px 0px 30px rgba(0, 255, 240, 0.35) !important;
        backdrop-filter: blur(15px) !important;
    }
    div[data-testid="stMarkdownContainer"] > div {
        background: linear-gradient(135deg, rgba(10, 10, 26, 0.85) 0%, rgba(3, 3, 7, 0.98) 100%) !important;
        border: 2px solid var(--custom-border-color, #00fff0);
        border-radius: 15px !important;
        box-shadow: 0px 0px 25px rgba(0, 255, 240, 0.2) !important;
    }
    div.stButton button, .stButton > button {
        width: 100% !important; min-height: 48px !important;
        font-family: 'Cairo', sans-serif !important; font-size: 14px !important; font-weight: 900 !important; border-radius: 12px !important;
        background: linear-gradient(135deg, #0d0d21 0%, #05050c 100%) !important; color: #00fff0 !important;
        border: 2px solid #00fff0 !important; box-shadow: 0px 0px 15px rgba(0, 255, 240, 0.3) !important;
    }
    div.stButton button:hover { 
        background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important; color: #000000 !important;
        box-shadow: 0px 0px 30px #00fff0 !important; transform: translateY(-2px) !important;
    }
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
        border: 2px solid #ff00ff !important; background-color: #06060d !important; color: #ffffff !important;
        border-radius: 12px !important; font-weight: 700 !important;
    }
    [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] { display: none !important; }
    .stWidgetFormLabel, p, span, label, h1, h2, h3, h4 { 
        font-family: 'Cairo', sans-serif !important; color: #ffffff !important;
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================================
# [القسم الرابع]: إدارة ومزامنة قاعدة بيانات الـ Auth
# ========================================================
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS saas_users_auth (
        email TEXT PRIMARY KEY, password TEXT, status TEXT, package TEXT
    )
""")
db_conn.commit()

db_cursor.execute("SELECT COUNT(*) FROM saas_users_auth WHERE email = 'daymaabdaalhmdllh@gmail.com'")
account_exists = db_cursor.fetchone()
if account_exists[0] == 0 and "destroyed_flag" not in st.session_state:
    db_cursor.execute("INSERT OR IGNORE INTO saas_users_auth VALUES ('daymaabdaalhmdllh@gmail.com', '123456', '🟢 مفعّل ونشط', 'الباقة السيبرانية الخارقة')")
    db_conn.commit()
db_conn.close()

def delete_email_completely(email_to_delete):
    try:
        conn = sqlite3.connect("saas_security_vault.db", timeout=10)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saas_users_auth WHERE email = ?", (email_to_delete,))
        conn.commit(); conn.close()
        return True
    except Exception as e:
        st.error(f"⚠️ خطأ ميكانيكي أثناء الحذف: {e}"); return False

import re

def render_premium_neon_packages():
    current_choice = st.session_state.get("selected_neon_package", "الباقة الأساسية المبتدئة (29k)")
    phase_cyber = "hologram-visible" if "السيبرانية" in current_choice else "hologram-hidden"
    phase_pro = "hologram-visible" if "الاحترافية" in current_choice else "hologram-hidden"
    phase_basic = "hologram-visible" if "الأساسية" in current_choice else "hologram-hidden"
    
    st.markdown(f"""
        <style>
        .hologram-card {{
            transform: translateY(20px);
            transition: all 0.5s ease-in-out;
            overflow: hidden;
            border-radius: 14px;
        }}
        .hologram-hidden {{
            max-height: 0px !important; opacity: 0 !important; padding: 0px !important; margin: 0px !important; border: 1px solid transparent !important; pointer-events: none;
        }}
        .hologram-visible {{
            max-height: 800px !important; opacity: 1 !important; transform: translateY(0px) scale(1);
            background: rgba(0, 255, 240, 0.05); border: 1px solid rgba(0, 255, 240, 0.6);
            padding: 18px; margin-bottom: 15px; box-shadow: 0 0 25px rgba(0, 255, 240, 0.2);
        }}
        .holo-title {{ color: #00fff0; font-weight: 900; font-size: 17px; margin-bottom: 6px; }}
        .holo-price {{ color: #ffffff; font-weight: 700; font-size: 15px; margin-bottom: 10px; border-bottom: 1px solid rgba(0, 255, 240, 0.2); padding-bottom: 6px; }}
        .holo-feat {{ color: #e0e0e0; font-size: 13px; margin: 5px 0; line-height: 1.5; }}
        </style>
        
        <div class='hologram-card {phase_basic}'>
            <div class='holo-title'>🌱 الباقة الأساسية المبتدئة (29k)</div>
            <div class='holo-price'>💰 السعر السنوي: 29,000 DA</div>
            <div class='holo-feat'>✓ إصدار فواتير الزبائن الكبيرة (A4) والملصقات الحرارية اللحظية.</div>
        </div>
        <div class='hologram-card {phase_pro}'>
            <div class='holo-title'>💎 الباقة الاحترافية المتوسطة (45k)</div>
            <div class='holo-price'>💰 السعر السنوي: 45,000 DA</div>
            <div class='holo-feat'>✓ تشمل كافة ميزات الباقة الأساسية بالكامل + رادار المبيعات.</div>
        </div>
        <div class='hologram-card {phase_cyber}'>
            <div class='holo-title'>⚡ الباقة السيبرانية الخارقة (65k)</div>
            <div class='holo-price'>💰 السعر السنوي: 65,000 DA</div>
            <div class='holo-feat'>✓ العقل الشامل للمنصة + الأتمتة الإعلانية الكاملة AI Hub.</div>
        </div>
    """, unsafe_allow_html=True)
    
    chosen_package = st.radio(
        "اختر فئة الباقة السنوية لمتجرك:",
        ["الباقة الأساسية المبتدئة (29k)", "الباقة الاحترافية المتوسطة (45k)", "الباقة السيبرانية الخارقة (65k)"],
        key="selected_neon_package"
    )
    return chosen_package

def validate_registration_inputs(email, password):
    if email == "" or password == "":
        st.error("⚠️ يرجى ملء حقول البريد وكلمة السر أولاً!")
        return False
    email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if not re.match(email_pattern, email):
        st.warning("⚠️ يرجى كتابة بريد إلكتروني منطقي وصحيح ينتهي بـ @gmail.com")
        return False
    if len(password) < 6:
        st.warning("⚠️ يجب أن تحتوي كلمة السر على 6 حروف أو أكثر لحماية متجرك")
        return False
    try:
        conn_check = sqlite3.connect("saas_security_vault.db", timeout=10)
        cursor_check = conn_check.cursor()
        cursor_check.execute("SELECT email FROM saas_users_auth WHERE email = ?", (email,))
        existing_user = cursor_check.fetchone()
        conn_check.close()
        if existing_user:
            st.error("❌ هذا البريد الإلكتروني مسجل مسبقاً في رادار المنصة السحابية!")
            return False
    except Exception as e:
        st.error(f"❌ خطأ في فحص جدار الأمان: {str(e)}")
        return False
    return True

# ========================================================
# الجزء الثاني: مركز توثيق هوية التاجر وعزل البوابات (مع تكامل الـ OTP)
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
            user_package_choice = render_premium_neon_packages()
            st.markdown("</div>", unsafe_allow_html=True)
            
            # تهيئة جلسة إرسال الرمز للتاجر الجديد
            if "otp_pending_verification" not in st.session_state:
                st.session_state["otp_pending_verification"] = False

            if not st.session_state["otp_pending_verification"]:
                if st.button("📝 إرسال رمز التحقق (OTP) إلى بريدك"):
                    if validate_registration_inputs(clean_email, clean_pass):
                        # توليد رمز عشوائي من 6 أرقام
                        generated_otp = f"{random.randint(100000, 999999)}"
                        st.session_state["temp_reg_otp"] = generated_otp
                        st.session_state["temp_reg_email"] = clean_email
                        st.session_state["temp_reg_pass"] = clean_pass
                        st.session_state["temp_reg_package"] = user_package_choice
                        
                        # إرسال البريد عبر دالة Gmail SMTP
                        email_subject = "رمز التحقق (OTP) لإنشاء حساب متجرك الجديد"
                        email_body = f"مرحباً بك,\n\nرمز التحقق العشوائي الخاص بك هو: {generated_otp}\n\nيرجى إدخاله في التطبيق لإتمام طلب إنشاء الحساب وإرساله للإدارة."
                        
                        if send_gmail_notification(clean_email, email_subject, email_body):
                            st.session_state["otp_pending_verification"] = True
                            st.success(f"📬 تم إرسال رمز التحقق بنجاح إلى البريد: {clean_email}")
                            time.sleep(0.5)
                            st.rerun()
            else:
                st.info(f"تم إرسال رمز التحقق إلى: {st.session_state.get('temp_reg_email')}")
                entered_otp = st.text_input("أدخل رمز التحقق (6 أرقام) الذي استقبلته:", key="entered_otp_box")
                
                if st.button("✅ تأكيد الرمز وإرسال الطلب للإدارة"):
                    if entered_otp.strip() == st.session_state.get("temp_reg_otp"):
                        reg_email = st.session_state["temp_reg_email"]
                        reg_pass = st.session_state["temp_reg_pass"]
                        reg_pkg = st.session_state["temp_reg_package"]
                        
                        conn_reg = sqlite3.connect("saas_security_vault.db", timeout=10)
                        cursor_reg = conn_reg.cursor()
                        cursor_reg.execute("INSERT OR IGNORE INTO saas_users_auth VALUES (?, ?, '⏳ في انتظار التفعيل', ?)", (reg_email, reg_pass, reg_pkg))
                        conn_reg.commit(); conn_reg.close()
                        
                        # مسح المتغيرات المؤقتة
                        st.session_state["otp_pending_verification"] = False
                        st.success("🎯 تم التحقق من الرمز وإرسال طلبك بنجاح للإدارة! سيظهر في الرادار فوراً.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ الرمز غير صحيح، حاول مرة أخرى.")
        else:
            st.markdown("</div>", unsafe_allow_html=True)
            if st.button("🔑 تسجيل الدخول إلى المتجر"):
                if clean_email == "" or clean_pass == "": 
                    st.error("⚠️ يرجى إدخال البريد وكلمة السر!")
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
# الجزء الثالث: غرفة المالك ورادار الموافقات (مع إرسال بريد القبول الترحيبي تلقائياً)
# ========================================================
if is_boss_link:
    ADMIN_USERNAME = "admin_master_v4"
    ADMIN_PASSWORD = "SaasPassword2026"
    
    if not st.session_state["admin_master_logged"]:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div style='max-width: 500px; margin: 60px auto 20px auto; padding: 40px; background: rgba(5, 5, 15, 0.95); border: 2px solid #00fff0; border-radius: 20px; box-shadow: 0px 0px 40px rgba(0, 255, 240, 0.35); direction: rtl; text-align: right;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #ff00ff; text-align: center; font-weight: 900; margin-top: 0;'>🔒 غرفة السيادة الكبرى والموافقات السحابية</h2>", unsafe_allow_html=True)
        
        boss_user = st.text_input("User:", key="boss_leader_user").strip()
        boss_pass = st.text_input("Password:", type="password", key="boss_leader_pass").strip()
        
        if st.button("⚙️ صعود وتفعيل خادم التحكم الأعلى", key="submit_boss_login_btn"):
            if boss_user == ADMIN_USERNAME and boss_pass == ADMIN_PASSWORD:
                st.session_state["admin_master_logged"] = True
                st.toast("👑 مرحباً بك يا قائد! تم تفعيل لوحة السيادة والموافقات.", icon="🔓")
                time.sleep(0.5); st.rerun()
            else:
                st.error("❌ بيانات خاطئة! يرجى إعادة التحقق.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='color: #ffffff; text-align: center; font-weight:900;'>👑 غرفة المالك والسيادة العليا v4</h1>", unsafe_allow_html=True)
        
        conn_view = sqlite3.connect("saas_security_vault.db", timeout=10)
        df_users = pd.read_sql_query("SELECT email, password, status, package FROM saas_users_auth", conn_view)
        conn_view.close()
        
        if not df_users.empty:
            for index, row in df_users.iterrows():
                current_email = row['email']; current_pass = row['password']; current_status = row['status']; current_package = row['package']
                status_color = "#00ff66" if "مفعّل" in current_status else "#ffaa00" if "انتظار" in current_status else "#ff0055"
                
                current_border_color = st.session_state.get(f"border_color_{current_email}", "#00fff0")
                
                st.markdown(f"""
                <div style="border: 2px solid {current_border_color}; border-radius: 15px; padding: 25px; background: rgba(10,10,26,0.9); margin-bottom: 15px; direction: rtl; text-align: right;">
                    <p style="margin:0 0 8px 0; font-weight:700;">💻 بريد التاجر: <span style="color: #00fff0;">{current_email}</span></p>
                    <p style="margin:0;">📊 الحالة: <span style="color: {status_color}; font-weight:bold;">{current_status}</span> | الباقة: <span style="color:{current_border_color}; font-weight:bold;">{current_package}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                col_1, col_2, col_3, col_4, col_5, col_6 = st.columns(6)
                with col_1:
                    if st.button("⚡ تفعيل وقبول حياً", key=f"btn_act_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🟢 مفعّل ونشط' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close()
                        
                        # إرسال رسالة ترحيب وقبول تلقائية عبر Gmail للتاجر
                        welcome_subject = "🎉 مبروك! تم قبول وتفعيل حساب متجرك بنجاح"
                        welcome_body = f"مرحباً بك يا تاجرنا العزيز,\n\nيسعدنا إبلاغك بأنه تم قبول وتفعيل حسابك في المنصة بنجاح تامة!\nيمكنك الآن تسجيل الدخول إلى متجرك والبدء في استغلال كافة الميزات المتاحة في باقتك.\n\nنتمنى لك كل التوفيق والنجاح في تجارتك!"
                        send_gmail_notification(current_email, welcome_subject, welcome_body)
                        
                        st.session_state[f"border_color_{current_email}"] = "#00ff66"
                        st.toast("🎯 تم التفعيل وإرسال إيميل الترحيب بالقبول للتاجر!"); time.sleep(0.5); st.rerun()
                with col_2:
                    if st.button("⏳ تمديد 7 أيام مهلة", key=f"btn_ext_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🟡 تم تمديد فترة التجربة 7 أيام' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close()
                        st.session_state[f"border_color_{current_email}"] = "#ffaa00"
                        st.toast("⏳ تم تمديد المهلة!"); time.sleep(0.5); st.rerun()
                with col_3:
                    if st.button("🗑️ تدمير نهائي فوري", key=f"btn_del_{current_email}"):
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
                        st.toast("🔒 تم مصادرة الصلاحيات!"); time.sleep(0.5); st.rerun()
                with col_6:
                    if st.button("🏷️ تعيين فئة الاشتراك", key=f"btn_pkg_select_{current_email}"):
                        st.session_state[f"show_pkg_slide_{current_email}"] = not st.session_state.get(f"show_pkg_slide_{current_email}", False)
                        st.rerun()
                
                if st.session_state.get(f"ask_confirm_{current_email}", False):
                    if st.button("✅ فهمت، احذف الحساب الآن", key=f"final_yes_{current_email}"):
                        st.session_state["destroyed_flag"] = True
                        if delete_email_completely(current_email): 
                            st.toast("🔥 تم حذف الحساب!"); time.sleep(0.5); st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 مغادرة غرفة القيادة وقفل الخزائن", key="logout_boss"): 
                st.session_state["admin_master_logged"] = False; st.rerun()
        else: 
            st.warning("📭 الرادار صافي تماماً، لا توجد طلبات معلقة حالياً.")

# ========================================================
# القسم (4): عزل البوابات وتشغيل متجر التاجر بعد القبول
# ========================================================
if "active_merchant_user" in st.session_state and not is_boss_link:
    current_merchant = st.session_state["active_merchant_user"]
    st.success(f"🔓 أهلاً بك يا تاجرنا المعتمد: {current_merchant} (المتجر مفتوح ويعمل بنجاح)")
    if st.button("🚪 تسجيل الخروج وتأمين الحساب", key="merchant_safe_logout_btn"):
        st.session_state.pop("active_merchant_user")
        st.rerun()
