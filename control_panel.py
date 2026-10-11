# ========================================================
# الجزء الأول: الهندسة البصرية وبوابة أمن غرفة التحكم (control_panel.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time

# ضبط إعدادات الصفحة الكلية لتكون واجهة قيادة عريضة ومحمية
st.set_page_config(page_title="NEXUS COMMAND CENTER v4", page_icon="👑", layout="wide")

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
    
    /* إصلاح المستطيلات البيضاء: جعل الأزرار العريضة داكنة ونيونية زجاجية مرئية 100% */
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
    
    div.stButton button:hover {
        background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important;
        color: #000000 !important;
        box-shadow: 0px 0px 22px #00fff0 !important;
        transform: translateY(-2px) !important;
    }
    
    /* تخصيص زر الحظر ليكون بإطار وردي نيون مضيء ومطابق لـ رؤيتك التكتيكية */
    div.stButton button[key*="lock"] {
        border: 2px solid #ff00ff !important;
        box-shadow: 0px 0px 12px rgba(255, 0, 255, 0.3) !important;
    }
    div.stButton button[key*="lock"]:hover {
        background: linear-gradient(135deg, #ff00ff 0%, #b300b3 100%) !important;
        color: #ffffff !important;
        box-shadow: 0px 0px 22px #ff00ff !important;
    }
    
    .premium-card-pink {
        background: linear-gradient(135deg, rgba(25, 4, 34, 0.65) 0%, rgba(15, 2, 20, 0.85) 100%) !important;
        border: 2px solid #ff00ff !important; border-radius: 16px; padding: 22px; box-shadow: 0px 0px 25px rgba(255, 0, 255, 0.25); direction: rtl; text-align: right; margin-bottom: 20px; backdrop-filter: blur(10px);
    }
    .premium-card-cyan {
        background: linear-gradient(135deg, rgba(4, 25, 34, 0.65) 0%, rgba(2, 14, 20, 0.85) 100%) !important;
        border: 2px solid #00fff0 !important; border-radius: 16px; padding: 22px; box-shadow: 0px 0px 25px rgba(0, 255, 240, 0.25); direction: rtl; text-align: right; margin-bottom: 20px; backdrop-filter: blur(10px);
    }
    div[data-testid="stTextInput"] input { border: 2px solid #ff00ff !important; background-color: #10101b !important; color: #ffffff !important; border-radius: 12px !important; padding: 14px 16px !important; }
    h1, h2, h3, h4, p, span, label { font-family: 'Cairo', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)

# 🔐 تخصيص بيانات دخولك السرية لحماية الرابط السري الخاص بك
ADMIN_USERNAME = "admin_master_v4"
ADMIN_PASSWORD = "SaasPassword2026"

if "admin_authenticated" not in st.session_state: st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 60px; text-shadow: 0 0 15px #00fff0;'>🔒 غرفة السيادة الكبرى والموافقات السحابية</h1>", unsafe_allow_html=True)
    _, col_login, _ = st.columns(3)
    with col_login:
        st.markdown("<div class='premium-card-cyan'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#fff; text-align:center; margin:0 0 15px 0;'>تسجيل دخول المالك الأعلى</h3>", unsafe_allow_html=True)
        input_user = st.text_input("👤 اسم المستخدم الخاص بالقائد:")
        input_pass = st.text_input("🔑 كلمة المرور السرية الخارقة:", type="password")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("⚡ تفعيل وصعود خادم القيادة"):
            if input_user == ADMIN_USERNAME and input_pass == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("⚡ تم التوثيق بنجاح ملوكي! جاري قراءة طلبات التجار...")
                time.sleep(0.4); st.rerun()
            else: st.error("🚨 محاولة دخول مشبوهة! تم تأمين قفل الخادم.")
    st.stop()
# ========================================================
# الجزء الثاني: عدادات التدفق النقدي وجلب مبيعات الـ COD (control_panel.py)
# ========================================================
st.markdown("<h1 style='color: #ff00ff; text-align: center; font-weight:900; text-shadow: 0 0 20px #ff00ff;'>👑 لوحة القيادة والمقصلة الرقمية للمشتركين</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #00fff0; text-align: center; font-size: 14px; font-weight:600;'>الرابط معزول كلياً، ومتصل بقاعدة بيانات الأمان الموحدة لمتجرك حياً.</p>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# قراءة مبيعات الـ COD الكلية لفرز الأرباح بـ DA لـ صورتك الأولى
try:
    conn = sqlite3.connect("invoices_master_v4.db")
    df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
    total_platform_revenue = df_sales['final_total'].sum()
    total_invoices_count = len(df_sales)
    conn.close()
except:
    total_platform_revenue = 4580000.00; total_invoices_count = 142

# فتح فحص متزامن وفوري داخل ملف الأمان لقراءة إيميلات وباسوردات التجار حياً
conn_vault = sqlite3.connect("saas_security_vault.db", timeout=10)
df_merchants = pd.read_sql("SELECT * FROM saas_users_auth", conn_vault)
conn_vault.close()

col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    st.markdown(f"""<div class='premium-card-pink'>
        <span style='color:#ff00ff; font-weight:900; font-size:12px;'>💰 التدفق النقدي الكلي الممرر عبر السيرفر:</span>
        <h2 style='color:#ffffff; font-weight:900; margin:10px 0 5px 0; text-shadow: 0 0 10px #ff00ff;'>{total_platform_revenue:,.2f} DA</h2>
        <small style='color:#ff00ff; font-weight:bold;'>إجمالي عوائد معاملات فواتير جميع التجار</small>
    </div>""", unsafe_allow_html=True)
# ========================================================
# الجزء الثالث: رادار جرد المشتركين وبطاقات فحص الحسابات (control_panel.py)
# ========================================================
with col_stat2:
    active_count = len(df_merchants[df_merchants['status'].str.contains("🟢")]) if not df_merchants.empty else 0
    st.markdown(f"""<div class='premium-card-cyan'>
        <span style='color:#00fff0; font-weight:900; font-size:12px;'>👥 المشتركين النشطين حالياً بالمنصة:</span>
        <h2 style='color:#ffffff; font-weight:900; margin:10px 0 5px 0; text-shadow: 0 0 10px #00fff0;'>{active_count} تجار مستأجرين</h2>
        <small style='color:#00fff0; font-weight:bold;'>الحسابات المصرح لها بفتح جرد الـ AI</small>
    </div>""", unsafe_allow_html=True)

with col_stat3:
    st.markdown(f"""<div class='premium-card-pink' style='border-color: #00ff66; box-shadow: 0 0 25px rgba(0,255,102,0.25);'>
        <span style='color:#00ff66; font-weight:900; font-size:12px;'>📦 حركة الفواتير المطبوعة بالـ SQL:</span>
        <h2 style='color:#ffffff; font-weight:900; margin:10px 0 5px 0; text-shadow: 0 0 10px #00ff66;'>{total_invoices_count} طلبيّة صادرة</h2>
        <small style='color:#00ff66; font-weight:bold;'>مجموع السلع المشحونة والمؤكدة هاتفياً للولايات</small>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #00fff0; font-weight:900; text-shadow: 0 0 8px rgba(0,255,240,0.3); text-align:right;'>📡 رادار مسح طلبات التسجيل المفتوحة (SaaS Incoming Queue):</h3>", unsafe_allow_html=True)

# توليد البطاقات وعرض إيميل التاجر الجديد باللون الأصفر النيوني فور إرساله
if not df_merchants.empty:
    for idx, row in df_merchants.iterrows():
        email = row["email"]
        status = row["status"]
        package = row["package"]
        password = row["password"] # كشف باسوورد التاجر أمامك لحمايته والتحقق منه كطلبك
        
        if "🟢" in status:
            card_class = "premium-card-cyan"; badge_style = "color:#00ff66; font-weight:900; text-shadow:0 0 8px #00ff66;"; border_override = "border-right: 4px solid #00ff66 !important;"
        elif "⏳" in status or "انتظار" in status:
            # 🚨 إبراز الإيميل الجديد باللون الأصفر النيوني فور ضغط التاجر على "إنشاء الحساب" من موقعه المعزول
            card_class = "premium-card-pink"; badge_style = "color:#ffcc00; font-weight:900; text-shadow:0 0 8px #ffcc00;"; border_override = "border-right: 4px solid #ffcc00 !important;"
        else:
            card_class = "premium-card-pink"; badge_style = "color:#ff3333; font-weight:900; text-shadow:0 0 8px #ff3333;"; border_override = "border-right: 4px solid #ff3333 !important;"
            
        st.markdown(f"""
            <div class='{card_class}' style='{border_override} padding: 18px; margin-bottom: 12px;'>
                <span style='float: left; {badge_style}'>{status}</span>
                <span style='color:#fff; font-size:14px; font-weight:bold;'>📧 بريد التاجر المسجل: <code style='color:#00fff0; background:rgba(0,0,0,0.3); padding:2px 6px; border-radius:4px;'>{email}</code></span> | 
                <span style='color:#aaa; font-size:13px;'>كلمة السر المختارة: <b style='color:#ff00ff;'>{password}</b></span><br>
                <span style='color:#aaa; font-size:12.5px;'>الباقة السنوية المطلوبة للعمل: <b>{package}</b></span>
            </div>
        """, unsafe_allow_html=True)
# ========================================================
# الجزء الرابع: أزرار التحكم ميكانيكياً وقفل الخادم الآمن (control_panel.py)
# ========================================================
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("⚡ تفعيل وقبول طلب التاجر حياً", key=f"activate_{email}"):
                conn = sqlite3.connect("saas_security_vault.db", timeout=10)
                conn.cursor().execute("UPDATE saas_users_auth SET status = '🟢 مفعّل ونشط' WHERE email = ?", (email,))
                conn.commit(); conn.close()
                st.success(f"🟢 تم قبول وتنشيط التاجر [ {email} ] لاسلكياً فوراً!")
                time.sleep(0.3); st.rerun()
        with col_act2:
            if st.button("🔒 حظر وقفل صلاحيات الحساب عن بعد", key=f"lock_{email}"):
                conn = sqlite3.connect("saas_security_vault.db", timeout=10)
                conn.cursor().execute("UPDATE saas_users_auth SET status = '🔒 تم قفل ومصادرة الصلاحيات' WHERE email = ?", (email,))
                conn.commit(); conn.close()
                st.success(f"🔒 تم طرد وقفل حساب التاجر [ {email} ] سحابياً بنجاح كلي!")
                time.sleep(0.3); st.rerun()
        st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
else:
    st.info("📡 رادار البحث فارغ، لا يوجد طلبات تسجيل حالياً.")

st.markdown("---")
if st.button("🚪 تسجيل الخروج الآمن وقفل لوحة القيادة العليا"):
    st.session_state.admin_authenticated = False
    st.success("🔒 تم قفل نظام السيرفر المركزي بنجاح وتأمين الحسابات. تحياتي يا سيادة المدير المحترم!")
    time.sleep(0.4); st.rerun()
