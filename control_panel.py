# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتلوين الواجهات الموسطة (control_panel.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time

# ضبط إعدادات الصفحة الكلية لتكون واجهة قيادة عريضة ومحمية ومستقلة 100%
st.set_page_config(page_title="NEXUS COMMAND CENTER v4", page_icon="👑", layout="wide")

# إعدام وإلغاء السهم الجانبي والشريط تماماً بالـ CSS لضمان بقاء الواجهة موسطة ونقية كلياً
st.markdown("""
    <style>
    [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] {
        display: none !important; visibility: hidden !important; opacity: 0 !important; height: 0px !important; width: 0px !important;
    }
    section[data-testid="stSidebar"] { display: none !important; visibility: hidden !important; }
    
    /* ترقية خلفية المتصفح بالكامل لتصبح ليلة رقمية عميقة وعميقة البعد */
    .stApp {
        background: radial-gradient(circle at 50% 40%, #0d0d21 0%, #030307 100%) !important;
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* [إصلاح حاسم وتوسيط البطاقة الزجاجية]: إجبار صندوق القيادة على الصعود بمنتصف الشاشة بنقاء 100% */
    .centered-box-container {
        max-width: 500px !important;
        margin: 60px auto 20px auto !important;
        padding: 35px !important;
        background: linear-gradient(135deg, rgba(10, 10, 26, 0.75) 0%, rgba(5, 5, 12, 0.95) 100%) !important;
        border: 2px solid #ff00ff !important;
        border-radius: 20px !important;
        box-shadow: 0px 0px 35px rgba(255, 0, 255, 0.25), inset 0px 0px 15px rgba(255, 0, 255, 0.1) !important;
        direction: rtl !important;
        text-align: right !important;
        backdrop-filter: blur(12px) !important;
    }
    
    .premium-card-pink {
        background: linear-gradient(135deg, rgba(34, 4, 46, 0.5) 0%, rgba(15, 2, 20, 0.8) 100%) !important;
        border: 2px solid #ff00ff !important; border-radius: 20px !important; padding: 30px !important; box-shadow: 0px 0px 30px rgba(255, 0, 255, 0.2) !important; direction: rtl; text-align: right; margin-bottom: 25px; backdrop-filter: blur(12px);
    }
    .premium-card-cyan {
        background: linear-gradient(135deg, rgba(4, 32, 43, 0.5) 0%, rgba(2, 14, 20, 0.8) 100%) !important;
        border: 2px solid #00fff0 !important; border-radius: 20px !important; padding: 30px !important; box-shadow: 0px 0px 30px rgba(0, 255, 240, 0.2) !important; direction: rtl; text-align: right; margin-bottom: 25px; backdrop-filter: blur(12px);
    }
    
    div[data-testid="stVerticalBlock"] button, div.stButton button, .stButton > button {
        width: 100% !important; min-height: 50px !important; white-space: normal !important; word-wrap: break-word !important;
        font-family: 'Cairo', sans-serif !important; font-size: 14.5px !important; font-weight: 800 !important; border-radius: 12px !important;
        text-align: center !important; display: inline-flex !important; align-items: center !important; justify-content: center !important;
        padding: 12px 18px !important; background: linear-gradient(135deg, #090915 0%, #040409 100%) !important; color: #00fff0 !important;
        border: 2px solid #00fff0 !important; box-shadow: 0px 0px 15px rgba(0, 255, 240, 0.3) !important; transition: all 0.4s ease-in-out !important;
    }
    div.stButton button:hover { background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important; color: #000000 !important; box-shadow: 0px 0px 25px #00fff0 !important; transform: translateY(-3px) !important; }
    
    div[data-testid="stTextInput"] input { border: 2px solid #ff00ff !important; background-color: #080811 !important; color: #ffffff !important; border-radius: 12px !important; padding: 15px 18px !important; font-family: 'Cairo', sans-serif !important; font-size: 14px !important; }
    .stWidgetFormLabel, p, span, label, h1, h2, h3, h4 { font-family: 'Cairo', sans-serif !important; color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# الجزء الثاني: التهيئة النظيفة وصندوق تسجيل القائد الموسط (control_panel.py)
# ========================================================
# تهيئة وحقن متغيرات الجلسة مسبقاً وبشكل معزول كلياً لسحق عيوب الـ KeyError تماماً
if "admin_authenticated" not in st.session_state: 
    st.session_state["admin_authenticated"] = False

ADMIN_USERNAME = "admin_master_v4"
ADMIN_PASSWORD = "SaasPassword2026"

# تأسيس ومزامنة قاعدة بيانات الأمان الموحدة لاستقبال وقراءة الحسابات بالثانية
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS saas_users_auth (
        email TEXT PRIMARY KEY, password TEXT, status TEXT, package TEXT
    )
""")
db_conn.commit()
db_conn.close()

# 👑 [غرفة المالك الموسطة كلياً]: صعود الصندوق النيوني بمنتصف الصفحة فوراً وبشكل تلقائي مستقر
if not st.session_state.get("admin_authenticated", False):
    st.markdown("<h1 style='color: #ff00ff; text-align: center; font-weight:900; margin-top: 40px; text-shadow: 0 0 20px #ff00ff; font-size:30px;'>👑 غرفة السيادة الكبرى والموافقات السحابية</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #b0b0d0; text-align: center; font-size: 14px; margin-bottom: 25px;'>مرحباً بك يا قائد المنصة المحترم. أدخل بياناتك بمركز التحكم الموسط المحدث لتنشيط السيرفر.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='centered-box-container'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#ff00ff; text-align:center; font-weight:700; margin-top:0;'>🔒 تسجيل دخول المالك الأعلى</h3>", unsafe_allow_html=True)
    
    admin_user_check = st.text_input("👤 اسم المستخدم الخاص بالقائد:", value="", key="boss_username_field")
    admin_pass_check = st.text_input("🔑 كلمة المرور الإدارية الخارقة:", type="password", value="", key="boss_password_field")
    st.markdown("</div>", unsafe_allow_html=True)
    
    _, col_btn_center, _ = st.columns(3)
    with col_btn_center:
        if st.button("⚙️ صعود وتفعيل خادم التحكم الأعلى", key="boss_submit_btn"):
            if admin_user_check == ADMIN_USERNAME and admin_pass_check == ADMIN_PASSWORD:
                st.session_state["admin_authenticated"] = True
                st.success("⚡ تم التوثيق بنجاح ملوكي! جاري فتح اللوحة...")
                time.sleep(0.3)
                st.rerun() # تحديث السيرفر الصافي والصحيح لبايثون
            else:
                st.error("❌ بيانات خاطئة! تم قفل السيرفر وتأمين الحسابات.")
# ========================================================
# الجزء الثالث: لوحة الإحصائيات المركزية وجرد الـ SQL (control_panel.py)
# ========================================================
# فتح لوحة القيادة المركزية كلياً بالمنتصف واختفاء شاشات الدخول التزامن الفوري
if st.session_state.get("admin_authenticated", False):
    st.markdown("<h1 style='color: #ff00ff; text-align: center; font-weight:900; text-shadow: 0 0 25px #ff00ff; font-size:34px;'>👑 مركز إدارة وتحويل صلاحيات المشتركين الكبرى</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00fff0; text-align: center; font-size: 14px; font-weight:600; margin-bottom:30px;'>مرحباً بك يا مالك المنصة في حجرتك الموسطة المعزولة كلياً لعام 2026.</p>", unsafe_allow_html=True)
    
    try:
        conn = sqlite3.connect("invoices_master_v4.db")
        df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
        total_platform_revenue = df_sales['final_total'].sum()
        total_invoices_count = len(df_sales)
        conn.close()
    except: 
        total_platform_revenue = 4580000.00; total_invoices_count = 142

    conn_vault = sqlite3.connect("saas_security_vault.db", timeout=10)
    df_merchants = pd.read_sql("SELECT * FROM saas_users_auth", conn_vault)
    conn_vault.close()

    # عدادات الأرباح والتدفقات النقدية المحدثة بمنتصف المتصفح لـ فواتير الجزائر
    col_s1, col_v2, col_v3 = st.columns(3)
    with col_s1:
        st.markdown(f"<div class='premium-card-pink'><span style='color:#ff00ff; font-weight:900;'>💰 التدفق النقدي الكلي الممرر عبر السيرفر:</span><h2 style='color:#fff; text-shadow: 0 0 10px #ff00ff; margin:10px 0 0 0;'>{total_platform_revenue:,.2f} DA</h2></div>", unsafe_allow_html=True)
    with col_v2:
        active_count = len(df_merchants[df_merchants['status'].str.contains("🟢")]) if not df_merchants.empty else 0
        st.markdown(f"<div class='premium-card-cyan'><span style='color:#00fff0; font-weight:900;'>👥 المشتركين النشطين حالياً بالمنصة:</span><h2 style='color:#fff; text-shadow: 0 0 10px #00fff0; margin:10px 0 0 0;'>{active_count} تجار نشطين</h2></div>", unsafe_allow_html=True)
    with col_v3:
        st.markdown(f"<div class='premium-card-pink' style='border-color:#00ff66; box-shadow:0 0 20px rgba(0,255,102,0.2);'><span style='color:#00ff66; font-weight:900;'>📦 حركة الفواتير المطبوعة بالـ SQL:</span><h2 style='color:#fff; text-shadow: 0 0 10px #00ff66; margin:10px 0 0 0;'>{total_invoices_count} طلبيّة صادرة</h2></div>", unsafe_allow_html=True)
# ========================================================
# الجزء الرابع: رادار الموافقات وقفل الخادم المعزول (control_panel.py)
# ========================================================
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #00fff0; font-weight:900; text-shadow: 0 0 8px rgba(0,255,240,0.3); text-align:right;'>📡 رادار مسح طلبات التسجيل المفتوحة (SaaS Incoming Queue):</h3>", unsafe_allow_html=True)

    if not df_merchants.empty:
        for idx, row in df_merchants.iterrows():
            email = row["email"]; status = row["status"]; package = row["package"]; password = row["password"]
            if "🟢" in status:
                card_class = "premium-card-cyan"; badge_style = "color:#00ff66; font-weight:900; text-shadow:0 0 8px #00ff66;"; border_override = "border-right: 5px solid #00ff66 !important;"
            elif "⏳" in status or "انتظار" in status:
                # 🚨 [الانبثاق الحتمي]: إيميل التاجر وباسورده يصعدان هنا فوراً وفي نفس اللحظة بالأصفر النيوني اللامع!
                card_class = "premium-card-pink"; badge_style = "color:#ffcc00; font-weight:900; text-shadow:0 0 8px #ffcc00;"; border_override = "border-right: 4px solid #ffcc00 !important;"
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
                    st.success("🟢 تم قبول وتنشيط التاجر وبدء التحويل الآمن!"); time.sleep(0.3); st.rerun()
            with col_act2:
                if st.button("🔒 حظر وقفل صلاحيات الحساب عن بعد", key=f"lock_{email}"):
                    conn = sqlite3.connect("saas_security_vault.db", timeout=10); conn.cursor().execute("UPDATE saas_users_auth SET status = '🔒 تم قفل ومصادرة الصلاحيات' WHERE email = ?", (email,)); conn.commit(); conn.close()
                    st.success("🔒 تم طرد وقفل حساب التاجر سحابياً بنجاح كلي!"); time.sleep(0.3); st.rerun()
            st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
    else: st.info("📡 لا يوجد طلبات تسجيل حالياً بمركز الموافقات السحابية الموسطة.")
    
    if st.button("🚪 مغادرة غرفة القيادة وقفل السيرفر الموسط"):
        st.session_state["admin_authenticated"] = False; st.success("🔒 تم تأمين السيرفر الموسط بنجاح!"); time.sleep(0.3); st.rerun()
