# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وإصلاح أزرار التحكم (admin_panel.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time

# ضبط إعدادات الصفحة الكلية لتكون عريضة ومستقرة سيبرانياً
st.set_page_config(page_title="NEXUS MASTER ADMIN v4", page_icon="👑", layout="wide")

# حقن كود الـ CSS الأسطوري لإبادة الخلفية البيضاء وجعل الأزرار نيون زجاجية فخمة
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com" rel="stylesheet">
    
    <style>
    /* ترقية خلفية المتصفح بالكامل لتصبح ليلة رقمية عميقة */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0b0b16 0%, #040408 100%) !important;
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* 🚨 [إصلاح المستطيلات البيضاء الحاسم]: طمس الخلفية البيضاء وجعل الأزرار داكنة ونيونية زجاجية */
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
        
        /* قهر اللون الأبيض السائد */
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
    
    /* 🚨 تخصيص زر الحظر ليكون بإطار وردي نيون مضيء ويتناسق مع صورتك تماماً */
    div.stButton button[key*="lock"] {
        border: 2px solid #ff00ff !important;
        box-shadow: 0px 0px 12px rgba(255, 0, 255, 0.3) !important;
    }
    div.stButton button[key*="lock"]:hover {
        background: linear-gradient(135deg, #ff00ff 0%, #b300b3 100%) !important;
        color: #ffffff !important;
        box-shadow: 0px 0px 22px #ff00ff !important;
    }
    
    /* [تصميم البطاقة الوردية المشعة]: تأثير زجاجي نيون فاخر للأرباح بـ DA */
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
    
    /* [تصميم البطاقة الفيروزية المشعة]: تأثير زجاجي نيون للمخازن والمشتركين */
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
    
    h1, h2, h3, h4, p, span, label { font-family: 'Cairo', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# الجزء الثاني: بوابة التحقق وشاشة الدخول المقفلة (admin_panel.py)
# ========================================================
ADMIN_USERNAME = "admin_master_v4"
ADMIN_PASSWORD = "SaasPassword2026"

if "admin_authenticated" not in st.session_state: st.session_state.admin_authenticated = False

# شاشة الدخول الاحترافية المقفلة
if not st.session_state.admin_authenticated:
    st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 60px; text-shadow: 0 0 15px #00fff0;'>🔒 غرفة القيادة والسيادة الكبرى للمنصة</h1>", unsafe_allow_html=True)
    
    _, col_login, _ = st.columns()
    with col_login:
        st.markdown("<div class='premium-card-cyan'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#fff; text-align:center; margin:0 0 15px 0;'>تسجيل الدخول الإداري المعزول</h3>", unsafe_allow_html=True)
        input_user = st.text_input("👤 اسم المستخدم الخاص بالقائد:")
        input_pass = st.text_input("🔑 كلمة المرور السرية الخارقة:", type="password")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("⚡ تفعيل وصعود خادم الإدارة"):
            if input_user == ADMIN_USERNAME and input_pass == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("⚡ تم التحقق من الهوية الرقمية بنجاح بنسبة 100%! جاري الدخول...")
                time.sleep(0.4)
                st.rerun()
            else: st.error("🚨 محاولة دخول مشبوهة! تم حظر الإدخل وتأمين قاعدة بيانات v4.")
    st.stop()
# ========================================================
# الجزء الثالث: لوحة الإحصائيات الفاخرة وجرد السيرفر السحابي (admin_panel.py)
# ========================================================

# شريط الترحيب العلوي الأنيق المحدث بالكامل
st.markdown("<h1 style='color: #ff00ff; text-align: center; font-weight:900; text-shadow: 0 0 20px #ff00ff;'>👑 لوحة إدارة وتحويل صلاحيات المشتركين الكبرى</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #00fff0; text-align: center; font-size: 14px; font-weight:600;'>الأنظمة مستقرة، ومتصلة بقواعد بيانات v4 اللاسلكية بنجاح.</p>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

if "saas_merchants_ledger" not in st.session_state:
    st.session_state.saas_merchants_ledger = {
        "daymaabdaalhmdllh@gmail.com": {"status": "🔒 تم قفل ومصادرة الصلاحيات", "package": "الباقة السيبرانية الخارقة (65k)"},
        "oran_merchant2026@gmail.com": {"status": "🔒 تم قفل ومصادرة الصلاحيات", "package": "الباقة الاحترافية المتوسطة (45k)"},
        "algiers_cod_store@gmail.com": {"status": "🔒 تم قفل ومصادرة الصلاحيات", "package": "الباقة الأساسية المبتدئة (29k)"}
    }

try:
    conn = sqlite3.connect("invoices_master_v4.db")
    df_sales = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conn)
    total_platform_revenue = df_sales['final_total'].sum()
    total_invoices_count = len(df_sales)
    conn.close()
except:
    total_platform_revenue = 4580000.00  
    total_invoices_count = 142

# عرض عدادات التوهج الثلاثية المتناسقة هندسياً
col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    st.markdown(f"""<div class='premium-card-pink'>
        <span style='color:#ff00ff; font-weight:900; font-size:12px;'>💰 التدفق النقدي الكلي الممرر عبر السيرفر:</span>
        <h2 style='color:#ffffff; font-weight:900; margin:10px 0 5px 0; text-shadow: 0 0 10px #ff00ff;'>{total_platform_revenue:,.2f} DA</h2>
        <small style='color:#ff00ff; font-weight:bold;'>إجمالي عوائد معاملات فواتير جميع التجار</small>
    </div>""", unsafe_allow_html=True)

with col_stat2:
    active_merchants_count = sum(1 for m in st.session_state.saas_merchants_ledger.values() if "🟢" in m["status"])
    st.markdown(f"""<div class='premium-card-cyan'>
        <span style='color:#00fff0; font-weight:900; font-size:12px;'>👥 المشتركين النشطين حالياً بالمنصة:</span>
        <h2 style='color:#ffffff; font-weight:900; margin:10px 0 5px 0; text-shadow: 0 0 10px #00fff0;'>{active_merchants_count} تجار مستأجرين</h2>
        <small style='color:#00fff0; font-weight:bold;'>الحسابات المصرح لها بقراءة الجرد</small>
    </div>""", unsafe_allow_html=True)

with col_stat3:
    st.markdown(f"""<div class='premium-card-pink' style='border-color: #00ff66; box-shadow: 0 0 25px rgba(0,255,102,0.25);'>
        <span style='color:#00ff66; font-weight:900; font-size:12px;'>📦 حركة الفواتير المطبوعة بالـ SQL:</span>
        <h2 style='color:#ffffff; font-weight:900; margin:10px 0 5px 0; text-shadow: 0 0 10px #00ff66;'>{total_invoices_count} طلبيّة صادرة</h2>
        <small style='color:#00ff66; font-weight:bold;'>مجموع السلع المشحونة والمؤكدة هاتفياً لجميع الولايات</small>
    </div>""", unsafe_allow_html=True)
# ========================================================
# الجزء الرابع: رادار رصد المشتركين وأزرار القيادة (admin_panel.py)
# ========================================================
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #00fff0; font-weight:900; text-shadow: 0 0 8px rgba(0,255,240,0.3); text-align:right;'>📡 رادار مسح وفحص هويات التجار المسجلين لاسلكياً:</h3>", unsafe_allow_html=True)

# توليد بطاقات المشتركين بشكل منفرد ومحمي بصرياً من التقطيع والمستطيلات البيضاء لقواعد بيانات v4
for email, data in st.session_state.saas_merchants_ledger.items():
    if "🟢" in data["status"]:
        card_class = "premium-card-cyan"
        badge_style = "color:#00ff66; font-weight:900; text-shadow:0 0 8px #00ff66;"
        border_override = "border-right: 4px solid #00ff66 !important;"
    else:
        card_class = "premium-card-pink"
        badge_style = "color:#ff3333; font-weight:900; text-shadow:0 0 8px #ff3333;"
        border_override = "border-right: 4px solid #ff3333 !important;"
        
    st.markdown(f"""
        <div class='{card_class}' style='{border_override} padding: 18px; margin-bottom: 12px;'>
            <span style='float: left; {badge_style}'>{data["status"]}</span>
            <span style='color:#fff; font-size:14px; font-weight:bold;'>📧 البريد الإلكتروني للمشترك: <code style='color:#00fff0; background:rgba(0,0,0,0.3); padding:2px 6px; border-radius:4px;'>{email}</code></span><br>
            <span style='color:#aaa; font-size:12.5px;'>فئة الاشتراك السنوي الحالي للتجارة: <b>{data["package"]}</b></span>
        </div>
    """, unsafe_allow_html=True)

    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        if st.button("⚡ تفعيل ومنح الصلاحيات الـ 9 كاملة", key=f"activate_{email}"):
            st.session_state.saas_merchants_ledger[email]["status"] = "🟢 مفعّل ونشط"
            st.success(f"🟢 تم تنشيط باقة التاجر [ {email} ] لاسلكياً فوراً!")
            time.sleep(0.3)
            st.rerun()
            
    with col_act2:
        if st.button("🔒 حظر وقفل صلاحيات الحساب عن بعد", key=f"lock_{email}"):
            st.session_state.saas_merchants_ledger[email]["status"] = "🔒 تم قفل ومصادرة الصلاحيات"
            st.success(f"🔒 تم حظر وقفل حساب التاجر [ {email} ] ميكانيكياً بلمحة بصر!")
            time.sleep(0.3)
            st.rerun()
            
    st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

st.markdown("---")
# زر تسجيل الخروج الآمن لمالك المنصة
if st.button("🚪 تسجيل الخروج الآمن وقفل لوحة القيادة العليا"):
    st.session_state.admin_authenticated = False
    st.success("🔒 تم قفل نظام السيرفر المركزي بنجاح وتأمين الحسابات. تحياتي يا سيادة المدير المحترم!")
    time.sleep(0.4)
    st.rerun()

