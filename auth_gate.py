# ========================================================
# الجزء الأول المطور - [1 من 4]: النواة والتحقق الشبح (gate_core.py)
# ========================================================
# ========================================================
# 🔒 [خزانة النسخ الاحتياطي التلقائي المشفرة - Cyber Auto-Backup Vault]
# ========================================================
# ========================================================
# [القسم الأول]: إعدادات البيئة، خزانة النسخ الاحتياطي، وجدار حماية الشبح المتقدم
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

# 🔒 ضبط إعدادات الشاشة الأساسية للمنصة الموحدة
st.set_page_config(page_title="NEXUS CENTRAL GATE v4", page_icon="👑", layout="wide")

# 🚨 [جدار الحماية الشبح الحاسم]: قراءة الرابط علوياً للتأكد من وجود مفتاحك السري (?role=boss)
query_params = st.query_params
is_boss_link = query_params.get("role") == "boss" if "role" in query_params else False
if "admin_master_logged" not in st.session_state:
    st.session_state["admin_master_logged"] = False
# ========================================================
# [القسم الثاني]: الحقن السيبراني وتصميم واجهات النيون الزجاجي للأزرار والعدادات
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
    /* ========================================================
       [القسم الثالث]: # === جدار الأنيميشن الموحد والانبثاق الميكانيكي لكافة عناصر المنصة ===
       ======================================================== */
    
    /* 1. جدار الانسياب الشامل لكافة العناصر الحية بالموقع */
    button, input, select, textarea, div.stDataFrame, table, .stSelectbox, [data-testid="stSidebar"] {
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    }

    /* 2. بناء التمدد والانجذاب السينمائي المرن عند الولادة */
    @keyframes elasticPop {
        0% {
            opacity: 0;
            transform: translateY(12px) scale(0.95);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    @keyframes alertPulseRed {
        0% { box-shadow: 0px 0px 12px rgba(255, 0, 85, 0.25); border-color: #ff0055; }
        50% { box-shadow: 0px 0px 25px rgba(255, 0, 85, 0.6); border-color: #ff3377; }
        100% { box-shadow: 0px 0px 12px rgba(255, 0, 85, 0.25); border-color: #ff0055; }
    }
    @keyframes alertPulseGold {
        0% { box-shadow: 0px 0px 12px rgba(255, 170, 0, 0.25); border-color: #ffaa00; }
        50% { box-shadow: 0px 0px 25px rgba(255, 170, 0, 0.6); border-color: #ffcc33; }
        100% { box-shadow: 0px 0px 12px rgba(255, 170, 0, 0.25); border-color: #ffaa00; }
    }
    @keyframes alertPulseGreen {
        0% { box-shadow: 0px 0px 12px rgba(0, 255, 102, 0.25); border-color: #00ff66; }
        50% { box-shadow: 0px 0px 25px rgba(0, 255, 102, 0.6); border-color: #33ff99; }
        100% { box-shadow: 0px 0px 12px rgba(0, 255, 102, 0.25); border-color: #00ff66; }
    }

    /* استهداف جدار الـ DOM بالكامل لفرض انبثاق مرن للأزرار وحقول الإدخال ورسائل التنبيه والتحذيرات */
    div[data-testid="stNotification"], div[data-testid="stAlert"], div.element-container:has(div[data-testid="stNotification"]), div.stAlert, div.stButton, div[data-testid="stTextInput"] {
        animation: elasticPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards !important;
    }

    /* صناديق الأخطاء والتوثيق الفاشل st.error بالتوهج النبضي الأحمر النيوني */
    div[data-testid="stAlert"]:has(div[data-baseinstance="error"]), div.stAlert:has([aria-label="Error"]) {
        border: 2px solid #ff0055 !important;
        background: linear-gradient(135deg, rgba(20, 2, 10, 0.92) 0%, rgba(5, 1, 3, 0.99) 100%) !important;
        animation: elasticPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, alertPulseRed 3s ease-in-out infinite alternate !important;
    }

    /* صناديق التحذيرات st.warning بالتوهج النبضي الذهبي الدافئ للسرية التامة */
    div[data-testid="stAlert"]:has(div[data-baseinstance="warning"]), div.stAlert:has([aria-label="Warning"]) {
        border: 2px solid #ffaa00 !important;
        background: linear-gradient(135deg, rgba(20, 12, 2, 0.92) 0%, rgba(5, 3, 1, 0.99) 100%) !important;
        animation: elasticPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, alertPulseGold 3s ease-in-out infinite alternate !important;
    }

    /* صناديق التوثيق الناجح st.success بالتوهج النبضي الأخضر السيبراني الرائع */
    div[data-testid="stAlert"]:has(div[data-baseinstance="success"]), div.stAlert:has([aria-label="Success"]) {
        border: 2px solid #00ff66 !important;
        background: linear-gradient(135deg, rgba(2, 20, 10, 0.92) 0%, rgba(1, 5, 2, 0.99) 100%) !important;
        animation: elasticPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, alertPulseGreen 3s ease-in-out infinite alternate !important;
    }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# [القسم الرابع]: إدارة ومزامنة جدول قاعدة بيانات الـ Auth وجدار الحماية الاستباقي للثغرات
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

# دالة التدمير الفوري لأي حساب في قاعدة البيانات دون إعطاب الاتصالات المفتوحة حياً
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
# جاهز ومؤمن بالكامل هنا لاستقبال أي ميزات إضافية في المحادثات القادمة...


# ====================================================================
# === الإضافات والتعديلات الجديدة لبوابة التوثيق وأمن المشتركين ===
# ====================================================================
import streamlit as st
import sqlite3
import time
import re

# ====================================================================
# === الإضافات والتعديلات الجديدة لبوابة التوثيق وأمن المشتركين ===
# ====================================================================

def render_premium_neon_packages():
    """
    تقوم هذه الدالة بتنفيذ ميكانيكية الهولوغرام الفاخرة (Holographic Phase-In Effect)،
    حيث تعكس بدقة التحديث الشامل لمستويات الباقات السلوية ومميزاتها الفنية،
    لتنبثق الباقة المختارة وحدها من العدم بناءً على رادار اختيار التاجر الحي.
    """
    # 1. قراءة الاختيار الحي من عنصر الراديو المعتمد تلقائياً
    current_choice = st.session_state.get("selected_neon_package", "الباقة الأساسية المبتدئة (29k)")

    # 2. توليد فئات الحالة الهولوغرامية الديناميكية للباقات الثلاث
    phase_cyber = "hologram-visible" if "السيبرانية" in current_choice else "hologram-hidden"
    phase_pro = "hologram-visible" if "الاحترافية" in current_choice else "hologram-hidden"
    phase_basic = "hologram-visible" if "الأساسية" in current_choice else "hologram-hidden"

    # 3. حقن قواعد الهندسة الحركية والـ CSS السينمائي والميزات المحدثة للشركات
    st.markdown(f"""
        <style>
        .hologram-card {{
            transform: translateY(20px);
            transition: max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1), 
                        opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1), 
                        transform 0.5s cubic-bezier(0.4, 0, 0.2, 1),
                        border 0.5s ease-in-out,
                        box-shadow 0.5s ease-in-out;
            overflow: hidden;
            border-radius: 14px;
        }}
        
        .hologram-hidden {{
            max-height: 0px !important;
            opacity: 0 !important;
            transform: translateY(20px) scale(0.95);
            padding: 0px !important;
            margin: 0px !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            pointer-events: none;
        }}
        
        .hologram-visible {{
            max-height: 800px !important; /* ارتفاع متسع لانسكاب الخدمات المحدثة بالكامل */
            opacity: 1 !important;
            transform: translateY(0px) scale(1);
            background: rgba(0, 255, 240, 0.05);
            border: 1px solid rgba(0, 255, 240, 0.6);
            padding: 18px;
            margin-bottom: 15px;
            box-shadow: 0 0 25px rgba(0, 255, 240, 0.2);
        }}
        
        .holo-title {{
            color: #00fff0;
            font-weight: 900;
            font-size: 17px;
            margin-bottom: 6px;
            text-shadow: 0 0 15px rgba(0, 255, 240, 0.5);
        }}
        .holo-price {{
            color: #ffffff;
            font-weight: 700;
            font-size: 15px;
            margin-bottom: 10px;
            border-bottom: 1px solid rgba(0, 255, 240, 0.2);
            padding-bottom: 6px;
        }}
        .holo-feat {{
            color: #e0e0e0;
            font-size: 13px;
            margin: 5px 0;
            padding-right: 5px;
            line-height: 1.5;
        }}
        </style>
        
        <!-- باقة 1: الأساسية المبتدئة -->
        <div class='hologram-card {phase_basic}'>
            <div class='holo-title'>🌱 الباقة الأساسية المبتدئة (29k)</div>
            <div class='holo-price'>💰 السعر السنوي: 29,000 DA</div>
            <div class='holo-feat'>✓ إصدار فواتير الزبائن الكبيرة (A4) والملصقات الحرارية اللحظية.</div>
            <div class='holo-feat'>✓ إرسال سريع للفاتورة وتفاصيل الطلب عبر WhatsApp للزبائن يدويًا.</div>
            <div class='holo-feat'>✓ مستودع سلع مبسط لإضافة المنتجات ومراقبة الكميات المتوفرة.</div>
            <div class='holo-feat'>✓ 🔒 قفل المساعد الجانبي الذكي (يفتح الردود العامة فقط ويحظر ميزات الـ AI المتقدمة).</div>
        </div>
        
        <!-- باقة 2: الاحترافية المتوسطة -->
        <div class='hologram-card {phase_pro}'>
            <div class='holo-title'>💎 الباقة الاحترافية المتوسطة (45k)</div>
            <div class='holo-price'>💰 السعر السنوي: 45,000 DA</div>
            <div class='holo-feat'><b>✓ تشمل كافة ميزات الباقة الأساسية المبتدئة بالكامل.</b></div>
            <div class='holo-feat'>✓ 🔥 مؤشر المخزون الناري الذكي: تنبيهات بصرية متحركة عند نفاذ السلع (أقل من 5 قطع).</div>
            <div class='holo-feat'>✓ 🧼 مطهر ملفات المبيعات: رفع وتطهير ملفات Excel من التكرارات والأسعار السالبة.</div>
            <div class='holo-feat'>✓ 🗺️ رادار المبيعات الجغرافي: مخطط بياني حي لفرز الولايات الجزائرية الأكثر مبيعاً لشحن آمن.</div>
            <div class='holo-feat'>✓ 🤖 فتح ذكاء المساعد الجانبي المتوسط: تقديم نصائح وحلول لمشاكل الشحن والـ Retour وتثبيت الكليون.</div>
        </div>
        
        <!-- باقة 3: السيبرانية الخارقة -->
        <div class='hologram-card {phase_cyber}'>
            <div class='holo-title'>⚡ الباقة السيبرانية الخارقة (65k)</div>
            <div class='holo-price'>💰 السعر السنوي: 65,000 DA</div>
            <div class='holo-feat'><b>✓ تشمل كافة ميزات الباقتين السابقتين بالكامل (العقل الشامل للمنصة).</b></div>
            <div class='holo-feat'>✓ 🚀 منصة الأتمتة الإعلانية الكاملة (AI Hub): صياغة الإعلانات التلقائية بـ 3 لهجات مختلفة فوراً.</div>
            <div class='holo-feat'>✓ 🎬 صانع سيناريوهات الفيديو بالثواني: خطة إنتاج كاملة لتصوير فيديوهات TikTok و Reels للسلع.</div>
            <div class='holo-feat'>✓ 📊 عداد تقييم قوة الإعلان الفوري (AI Ad Score Meter) لتحليل جاذبية المنشور قبل إطلاقه.</div>
            <div class='holo-feat'>✓ 💰 حاسبة الـ ROI وميزانية الفحص الموازية بالدولار وما يقابلها بالدينار الجزائري (Square).</div>
            <div class='holo-feat'>✓ 🧠 العقل الخارق للمساعد الجانبي: إجابات استخباراتية فورية عن استهدافات فيسبوك وهاشتاغات تيك توك وحصانة ضد الخربشة.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # أزرار الراديو النقية لمزامنة الميكانيكية الحركية وتمرير الاختيار بدقة
    chosen_package = st.radio(
        "اختر فئة الباقة السنوية لمتجرك لتفعيل عرض مميزاتها فوراً:",
        ["الباقة الأساسية المبتدئة (29k)", "الباقة الاحترافية المتوسطة (45k)", "الباقة السيبرانية الخارقة (65k)"],
        key="selected_neon_package"
    )
    return chosen_package

def validate_and_process_registration(email, password):
    """
    ممر الأمان الذكي المكون من 3 طبقات فحص صارمة لمنع حقن البيانات العشوائية وحظر الحسابات المتكررة.
    """
    if email == "" or password == "":
        st.error("⚠️ يرجى ملء حقول البريد وكلمة السر أولاً!")
        return None
        
    # 1. جدار التحقق من صيغة البريد (Email Format Guard)
    email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if not re.match(email_pattern, email):
        st.warning("⚠️ يرجى كتابة بريد إلكتروني منطقي وصحيح ينتهي بـ @gmail.com")
        return None
        
    # 2. قوة كلمة المرور (Password Strength Check)
    if len(password) < 6:
        st.warning("⚠️ يجب أن تحتوي كلمة السر على 6 حروف أو أكثر لحماية متجرك")
        return None
        
    # 3. منع تكرار الحسابات (Unique Email Guard)
    try:
        conn_check = sqlite3.connect("saas_security_vault.db", timeout=10)
        cursor_check = conn_check.cursor()
        cursor_check.execute("SELECT email FROM saas_users_auth WHERE email = ?", (email,))
        existing_user = cursor_check.fetchone()
        conn_check.close()
        
        if existing_user:
            st.error("❌ هذا البريد الإلكتروني مسجل مسبقاً في رادار المنصة السحابية!")
            return None
    except Exception as e:
        st.error(f"❌ خطأ في فحص جدار الأمان: {str(e)}")
        return None
        
    return st.session_state.get("selected_neon_package", "الباقة الأساسية المبتدئة (29k)")
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
            # استدعاء منصة العرض الهولوغرامية الفاخرة بالميزات الجديدة المحدثة 100%
            user_package_choice = render_premium_neon_packages()
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("📝 إرسال طلب إنشاء الحساب للإدارة"):
                validated_package = validate_and_process_registration(clean_email, clean_pass)
                if validated_package:
                    conn_reg = sqlite3.connect("saas_security_vault.db", timeout=10)
                    cursor_reg = conn_reg.cursor()
                    cursor_reg.execute("INSERT OR IGNORE INTO saas_users_auth VALUES (?, ?, '⏳ في انتظار التفعيل', ?)", (clean_email, clean_pass, validated_package))
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
                        if "🟢 مفعّل ونشط" in user_status_row:
                            st.session_state["active_merchant_user"] = clean_email
                            st.success("🔓 تم التحقق بنجاح! جاري فتح متجرك...")
                            time.sleep(0.5); st.rerun()
                        else:
                            st.warning(f"⏳ حالة حسابك الحالية: {user_status_row}")
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
                    <p style="margin:0;">📊 الحالة الحالية: <span style="color: {status_color}; font-weight:bold;">{current_status}</span> | فئة الاشتراك المطلوبة للعمل: <span style="color:{current_border_color}; font-weight:bold;">{current_package}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                # إنشاء 6 أعمدة تفاعلية مخصصة لاحتواء الزر السادس الجديد للفئات السنوية
                col_1, col_2, col_3, col_4, col_5, col_6 = st.columns(6)
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
                with col_6:
                    # 💎 [الزر السادس المتوهج بالفيروزي]: تعيين فئة الاشتراك السنوي
                    if st.button("🏷️ تعيين فئة الاشتراك", key=f"btn_pkg_select_{current_email}"):
                        st.session_state[f"show_pkg_slide_{current_email}"] = not st.session_state.get(f"show_pkg_slide_{current_email}", False)
                        st.rerun()
                
                # 🔄 [ميكانيكية الـ Slide-down البرمجية المخصصة للزر السادس للتحكم بالباقات والتوهج]
                if st.session_state.get(f"show_pkg_slide_{current_email}", False):
                    st.markdown(f"<div style='border: 1px solid #00fff0; border-radius: 10px; padding: 15px; background: rgba(5,20,30,0.9); margin-top: 10px; direction: rtl; text-align: right;'>", unsafe_allow_html=True)
                    st.markdown("<p style='color: #00fff0; margin: 0 0 10px 0; font-weight: bold;'>🎯 اختر فئة الاشتراك السنوي المحددة لهذا التاجر للترقية الفورية ولتلوين الإطار:</p>", unsafe_allow_html=True)
                    
                    selected_opt = st.radio(
                        "الباقات المتوفرة:",
                        ["الباقة الأساسية (29k)", "الباقة الاحترافية (45k)", "الباقة السيبرانية الخارقة (65k)"],
                        key=f"radio_pkg_{current_email}",
                        label_visibility="collapsed"
                    )
                    
                    if st.button("💾 تأمين وحفظ الباقة برمجياً حياً", key=f"btn_confirm_pkg_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET package = ? WHERE email = ?", (selected_opt, current_email))
                        conn.commit(); conn.close()
                        
                        if "29k" in selected_opt:
                            st.session_state[f"border_color_{current_email}"] = "#00ff66"
                        elif "45k" in selected_opt:
                            st.session_state[f"border_color_{current_email}"] = "#ffaa00"
                        else:
                            st.session_state[f"border_color_{current_email}"] = "#ff00ff"
                            
                        st.session_state[f"show_pkg_slide_{current_email}"] = False
                        st.toast(f"✅ تم تحديث باقة المتجر إلى {selected_opt} وتلوين الكود حياً!")
                        time.sleep(0.5); st.rerun()
                        
                    st.markdown("</div>", unsafe_allow_html=True)
                
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
        glow_color = "#ffaa00"
    elif clamped_days > 2:
        glow_color = "#ff5500"
    else:
        glow_color = "#ff0055"
        
    html_template = f"""
    <div style='display: flex; align-items: center; justify-content: space-between; padding: 12px; background: rgba(5,5,15,0.6); border-radius: 8px; margin-bottom: 8px; border-left: 4px solid {glow_color}; direction: rtl; text-align: right;'>
        <div style='display: flex; align-items: center; gap: 15px;'>
            <svg width="45" height="45" viewBox="0 0 45 45" style="transform: rotate(-90deg); filter: drop-shadow(0px 0px 6px {glow_color});">
                <circle cx="22.5" cy="22.5" r="18" stroke="rgba(255,255,255,0.1)" stroke-width="3" fill="transparent" />
                <circle cx="22.5" cy="22.5" r="18" stroke="{glow_color}" stroke-width="3.5" fill="transparent" 
                        stroke-dasharray="{total_circumference}" stroke-dashoffset="{stroke_offset}" stroke-linecap="round" />
            </svg>
            <span style='color:#ffffff; font-size: 15px;'>⚠️ التاجر: <span style='color: #00fff0;'>{email}</span></span>
        </div>
        <span style='color:{glow_color}; font-weight:bold; font-size: 14px;'>متبقي: {days_left} أيام فقط!</span>
    </div>
    """
    return html_template





# ========================================================
# القسم (4 - أ): ممر العبور السحابي وجدار العزل الفردي لمتجرك الجديد
# ========================================================
if "active_merchant_user" in st.session_state and not is_boss_link:
    current_merchant = st.session_state["active_merchant_user"]
    
    # 🔒 الفحص السحابي الصارم وجلب حالة الحساب ونوع الباقة (package) لمتجرك الجديد
    conn_final_auth = sqlite3.connect("saas_security_vault.db", timeout=10)
    cursor_final_auth = conn_final_auth.cursor()
    # تأمين جلب الـ status والـ package معاً من جدول صلاحيات المشتركين
    cursor_final_auth.execute("SELECT status, package FROM saas_users_auth WHERE email = ?", (current_merchant,))
    chk_row = cursor_final_auth.fetchone()
    conn_final_auth.close()
    
    user_actual_status = str(chk_row) if chk_row and chk_row is not None else ""
    user_package = str(chk_row).strip() if chk_row and len(chk_row) > 1 and chk_row is not None else "29k"
    
    if not chk_row or "مفعّل" not in user_actual_status:
        st.warning("🔒 انتهت أو سُحبت تراخيص الحساب السحابي.")
        if st.button("🔄 العودة لبوابة الدخول الرئيسية", key="back_gate_refresh_btn"): 
            st.session_state.pop("active_merchant_user")
            st.rerun()
        st.stop()

    # 🏪 [جدار العزل الفردي الأسطوري]: قفل البيانات وعزل فواتير ومخزون كل تاجر باسم إيميله المشفر
    merchant_db_name = f"invoice_vault_{urllib.parse.quote_plus(current_merchant)}.db"
    
    if "merchant_db_conn" not in st.session_state:
        st.session_state["merchant_db_conn"] = sqlite3.connect(merchant_db_name, check_same_thread=False)
    else:
        try:
            st.session_state["merchant_db_conn"].execute("SELECT 1")
        except (sqlite3.ProgrammingError, sqlite3.OperationalError):
            st.session_state["merchant_db_conn"] = sqlite3.connect(merchant_db_name, check_same_thread=False)
        
    conne = st.session_state["merchant_db_conn"]
    cursor = conne.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS v4_customer_invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT, shop_name TEXT, customer_name TEXT, 
            customer_phone TEXT, product_name TEXT, final_total REAL, month_created TEXT, date_created TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS store_stock (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT UNIQUE, available_qty INTEGER
        )
    ''')
    conne.commit()
    # 🌐 جدار حجب الأدوات التلقائي بناءً على فئة باقة التاجر الحالية
    available_tools = ["✨ صانع الفواتير الاحترافي (PDF)", "📦 إدارة وتنبيهات المخزون السلعي"]
    
    if "45k" in user_package:
        available_tools.append("🧼 مطهر ملفات المبيعات وإحصائيات الولايات")
    elif "65k" in user_package:
        available_tools.append("🧼 مطهر ملفات المبيعات وإحصائيات الولايات")
        available_tools.append("🚀 مولّد الحملات والتخطيط التسويقي (AI)")
        
    st.sidebar.markdown(f"<p style='color: #00fff0; font-weight: bold; text-align:center;'>👤 التاجر النشط:<br>{current_merchant}<br><span style='color:#ffaa00;'>باقة: {user_package}</span></p>", unsafe_allow_html=True)
    st.sidebar.markdown("<h2 style='color: #00ffcc; text-align: center; font-size: 24px;'>🛠️ التحكم</h2>", unsafe_allow_html=True)
    
    choice = st.sidebar.radio("اختر الأداة التي تريد استخدامها:", available_tools, key="merchant_navigation_radio")

    if st.sidebar.button("🚪 تسجيل الخروج وتأمين الحساب", key="merchant_safe_logout_btn"):
        if "merchant_db_conn" in st.session_state:
            st.session_state["merchant_db_conn"].close()
            st.session_state.pop("merchant_db_conn")
        st.session_state.pop("active_merchant_user")
        st.toast("تم الخروج الآمن وتأمين المستودع كلياً!")
        time.sleep(0.5)
        st.rerun()

    # ======================================================================
    # === إضافات نظام العزل والاتصال والمساعد الذكي ===
    # ======================================================================
    def render_sidebar_helper():
        """
        بوت المساعد الذكي المزدوج المتطور كلياً:
        يدعم الانتقال الحركي السلس، وترقية الكلمات القريبة، وحظر الحروف العشوائية.
        """
        st.sidebar.markdown("---")
        
        # حقن أنماط علبة الرد وحركة الانبثاق الميكانيكي الصاعد من العدم (elasticPop)
        st.sidebar.markdown("""
        <style>
        @keyframes elasticPop {
            0% { transform: translateY(25px) scale(0.92); opacity: 0; }
            60% { transform: translateY(-4px) scale(1.02); opacity: 0.9; }
            85% { transform: translateY(1px) scale(0.99); opacity: 0.98; }
            100% { transform: translateY(0) scale(1); opacity: 1; }
        }
        .cyber-dynamic-box {
            animation: elasticPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.1) forwards;
            border-radius: 12px; 
            padding: 15px; 
            background: rgba(5, 15, 20, 0.92); 
            margin-top: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
        }
        </style>
        """, unsafe_allow_html=True)
        
        if "intent_frame_color" not in st.session_state:
            st.session_state["intent_frame_color"] = "#00fff0"
        
        def normalize_arabic_text(text):
            if not text: return ""
            text = text.strip().lower()
            text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي").replace("ة", "ه")
            for haraka in ["ّ", "🔸", "؟", "!", ".", "،", "ـ"]:
                text = text.replace(haraka, "")
            return text

        def get_close_match_score(word1, word2):
            w1, w2 = normalize_arabic_text(word1), normalize_arabic_text(word2)
            if not w1 or not w2: return 0.0
            if w1 == w2: return 1.0
            if abs(len(w1) - len(w2)) > 3: return 0.0
            len1, len2 = len(w1), len(w2)
            matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
           matrix = [[j for j in range(len2 + 1)] for i in range(len1 + 1)]

            for j in range(len2 + 1): matrix[j] = j
            
            for i in range(1, len1 + 1):
                for j in range(1, len2 + 1):
                    cost = 0 if w1[i-1] == w2[j-1] else 1
                    matrix[i][j] = min(matrix[i-1][j] + 1, matrix[i][j-1] + 1, matrix[i-1][j-1] + cost)
            distance = matrix[len1][len2]
            return 1.0 - (distance / max(len1, len2))
        # 👑 بيئة المالك الأعلى (Owner Workspace)
        if is_boss_link:
            st.sidebar.markdown("<h3 style='color: #00fff0; text-align: center; margin-bottom: 0;'>👑 مساعد المالك الأعلى</h3>", unsafe_allow_html=True)
            if "boss_chat_reply" not in st.session_state:
                st.session_state["boss_chat_reply"] = "مرحباً بك يا قائد! نظام تحليل الكود المتقدم جاهز تحت سيادتك."
            boss_query = st.sidebar.text_input("💻 أدخل أمر التحليل أو استفسر عن الكود والجداول:", key="boss_ai_query_in")
            if st.sidebar.button("🧠 استدعاء خبير المنصة", key="submit_boss_query_btn") or boss_query == "شرح دكي":
                if boss_query:
                    st.session_state["boss_chat_reply"] = "📊 **[شرح دكي للمالك]:** كود المبيعات والمخزون مبني على الـ SQLite3 وعزل الـ SaaS البنيوي لتفادي التداخل وقفل الـ RAM."
                    st.session_state["intent_frame_color"] = "#00fff0"
                    st.rerun()
            st.sidebar.markdown(f'<div class="cyber-dynamic-box" style="border:2px solid {st.session_state["intent_frame_color"]};"><p style="color:#ffffff; font-size:14px; direction:rtl; text-align:right; margin:0;">{st.session_state["boss_chat_reply"]}</p></div>', unsafe_allow_html=True)
        
        # 🏪 بيئة المساعد التجاري للمستأجرين (Merchant Space)
        else:
            st.sidebar.markdown("<h3 style='color: #00fff0; text-align: center; margin-bottom: 0;'>🤖 المساعد التجاري الذكي</h3>", unsafe_allow_html=True)
            if "merchant_chat_reply" not in st.session_state:
                st.session_state["merchant_chat_reply"] = "مرحباً بك! أنا مساعدك التجاري الذكي لمساعدتك في إدارة متجرك."
                st.session_state["intent_frame_color"] = "#00fff0"
                
            merchant_query = st.sidebar.text_input("💡 اسأل عن أي فكرة، نصيحة، أو مشكلة في متجرك:", key="merchant_ai_query_in", placeholder="مثال: عندي مشكل في الشحن")
            
            # 📈 [ترقية قاموس الكلمات لتفادي أخطاء الإدخال الجزائرية (Intents Upgrade)]
            merchant_intents = {
                "shipping": ["شحن", "توصيل", "ولاية", "ليفريرون", "ليفرور", "رتور", "ولايات", "جنوب", "سحن", "توسيل", "ليفرور"],
                "customers": ["زبون", "زبائن", "كليون", "لكليون", "تعامل", "اتصال", "تثبيت", "كونفيرمي", "الهاتف", "سبون"],
                "stock": ["منتج", "سلعة", "مخزون", "ستوك", "حبة", "قطع", "نفاذ", "منتح"],
                "marketing": ["تسويق", "فيسبوك", "اعلانات", "تيكتوك", "حملة", "ادس", "تيك توك", "هاشتاغ"]
            }
            if st.sidebar.button("🧠 استشارة العقل التجاري", key="submit_merchant_query_btn"):
                if merchant_query:
                    # 🔄 [منع الظهور المفاجئ والتفجر البصري (Smooth Transition Reset)]
                    st.session_state["merchant_chat_reply"] = "" 
                    clean_input = normalize_arabic_text(merchant_query)
                    
                    # 🚨 [جدار حظر الخربشة العشوائية والحروف المتكررة (Anti-Gibberish Dynamic Guard)]
                    input_words = clean_input.split()
                    is_gibberish = False
                    for word in input_words:
                        if len(word) >= 5 and len(set(word)) <= 2: # كلمات مشوهة بحروف مكررة مثل (سسسسس)
                            is_gibberish = True
                    
                    if len(clean_input) < 3 or clean_input.isdigit() or is_gibberish:
                        st.session_state["merchant_chat_reply"] = "⚠️ **إدخال غير مفهوم:** يبدو أنك كتبت حروفاً عشوائية! يرجى كتابة سؤال واضح (مثال: شحن، ستوك، كليون) لمساعدتك بدقة."
                        st.session_state["intent_frame_color"] = "#ff0055" # أحمر نبضي تحذيري
                    else:
                        detected_intent = None
                        highest_score = 0.0
                        
                        for intent, keywords in merchant_intents.items():
                            for kw in keywords:
                                normalized_kw = normalize_arabic_text(kw)
                                for word in input_words:
                                    score = get_close_match_score(word, normalized_kw)
                                    if score > highest_score and score >= 0.82:
                                        highest_score = score
                                        detected_intent = intent
                        
                        # 🛡️ تطبيق شروط الباقة الصارمة والتلوين التحذيري الفوري للحجب
                        if user_package == "29k" and detected_intent in ["shipping", "marketing"]:
                            st.session_state["merchant_chat_reply"] = "🔒 **المساعد:** ميزات الذكاء الاصطناعي المتقدمة مقفلة في باقتك الحالية (الأساسية)! قم بالترقية الآن لتفعيل العقل التسويقي وحلول الشحن الذكية."
                            st.session_state["intent_frame_color"] = "#ff0055"
                        elif user_package == "45k" and detected_intent == "marketing":
                            st.session_state["merchant_chat_reply"] = "🔒 **المساعد:** نصائح التسويق الذكي وإعلانات الفيسبوك المتقدمة تتطلب الباقة السيبرانية الأعلى. يرجى الترقية لتفعيلها."
                            st.session_state["intent_frame_color"] = "#ff0055"
                        else:
                            # ميكانيكية التحويل اللوني التلقائي حياً بناءً على الـ Intent المصرح به
                            if detected_intent == "shipping":
                                st.session_state["merchant_chat_reply"] = "📌 **نصيحة الشحن للمتجر:** ركز حملاتك الإعلانية على ولايات الوسط والشرق (العاصمة، سطيف، قسنطينة) لضمان سرعة التوصيل وزيادة نسبة استلام الطرود وتفادي المرتجعات."
                                st.session_state["intent_frame_color"] = "#00fff0" # أزرق فيروزي مشع
                            elif detected_intent == "customers":
                                st.session_state["merchant_chat_reply"] = "📞 **إستراتيجية التثبيت للمتجر:** اتصل بالزبون فوراً لتأكيد الشراء، واستخدم لهجة محترمة شاملة سعر الشحن لتفادي الرفض عند الباب."
                                st.session_state["intent_frame_color"] = "#ff4500" # برتقالي ناري دافئ
                            elif detected_intent == "stock":
                                st.session_state["merchant_chat_reply"] = "📦 **نصيحة مراقبة المخزون:** إذا انخفضت الكمية لأقل من 5 قطع، أطلق فوراً 'عرض القطعة الأخيرة' بتخفيض 10% لتصفية الستوك وضخ السيولة."
                                st.session_state["intent_frame_color"] = "#ff00ff" # بنفسجي سيبراني
                            elif detected_intent == "marketing" and user_package == "65k":
                                st.session_state["merchant_chat_reply"] = "🚀 **العقل السيبراني التسويقي (باقة 65k):** للتحجيم الناجح، أطلق إعلانات CBO باستهداف عريض في الجزائر، واستخدم فلاتر الهاشتاغات الحالية لتيك توك مع ميزانية فحص 10$ يومياً للـ Conversion حياً."
                                st.session_state["intent_frame_color"] = "#ffaa00" # ذهب متوهج
                            else:
                                st.sidebar.toast("🔍 جاري البحث في قاعدة المعرفة المتاحة...")
                                st.session_state["merchant_chat_reply"] = "⚠️ **إدخال غير مفهوم:** لم أتمكن من تحديد مرادك بدقة! يرجى كتابة سؤال واضح أو الاستعانة بدليل المواضيع في الأسفل (مثال: شحن، ستوك، كليون)."
                                st.session_state["intent_frame_color"] = "#ff0055" # أحمر نبضي تحذيري
                    st.rerun()
            
            # 🚀 إخراج علبة الرد السيبرانية المحدثة ميكانيكياً ولونياً وحركياً بنقاء كامل ومنع الوميض المفاجئ
            if st.session_state["merchant_chat_reply"]:
                st.sidebar.markdown(f'<div class="cyber-dynamic-box" style="border: 2px solid {st.session_state["intent_frame_color"]};"><p style="color:#ffffff; font-size:14px; direction:rtl; text-align:right; margin:0;">{st.session_state["merchant_chat_reply"]}</p></div>', unsafe_allow_html=True)
            
            st.sidebar.markdown("""
            <div style="margin-top: 15px; padding: 10px; background: rgba(255,170,0,0.05); border: 1px dashed #ffaa00; border-radius: 10px; text-align: right; direction: rtl;">
                <p style="color: #ffaa00; font-size: 12px; margin: 0 0 5px 0; font-weight: bold;">💡 مواضيع يمكنك استشارتي فيها:</p>
                <span style="color: #ffffff; font-size: 11px;">• مشاكل الشحن والـ Retour (باقة 45k+)<br>• تثبيت الطلبيات والاتصال بالزبائن<br>• إدارة السلع ونفاذ الستوك (Stock)<br>• استراتيجيات التسويق والـ Ads (باقة 65k)</span>
            </div>
            """, unsafe_allow_html=True)

# 🤖 تشغيل وتأمين استدعاء المساعد الفوري في أقصى يسار السيرفر لإغلاق الكتلة بأمان ومنع الـ IndentationError
    render_sidebar_helper()


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
                    
                    logo_data = uploaded_logo.read() if uploaded_logo is not None else None
                    st.session_state["generated_pdf_invoice"] = generate_invoice_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, price, quantity, product_total, shipping_cost, final_total, logo_data)
                    st.session_state["generated_pdf_label"] = generate_thermal_label_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, final_total, current_date)
                    st.session_state["last_active_customer"] = customer_name
                    st.session_state["last_active_phone"] = customer_phone
                    st.session_state["last_active_shop"] = shop_name
                    st.session_state["last_active_product"] = product_name
                    st.session_state["last_active_total"] = final_total
                    st.success("💾 تم تسجيل البيع وتوليد المستندات بنجاح!")
                    
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
        <div style="background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border-radius: 12px; padding: 25px; border: 1px solid rgba(0, 255, 240, 0.2); box-shadow: 0 0 20px rgba(0, 255, 240, 0.1), inset 0 0 15px rgba(0, 255, 240, 0.05); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: right; direction: rtl;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(0, 255, 240, 0.3); padding-bottom: 12px; margin-bottom: 15px;">
                <span style="font-size: 18px; font-weight: bold; color: #00fff0; text-shadow: 0 0 10px rgba(0, 255, 240, 0.5);">🏪 {shop_name}</span>
                <span style="font-size: 12px; color: #888;">📅 {current_date}</span>
            </div>
            <div style="margin-bottom: 10px; color: #e0e0e0; font-size: 14px;"><strong>👤 العميل:</strong> <span style="color: #fff;">{preview_customer}</span></div>
            <div style="margin-bottom: 10px; color: #e0e0e0; font-size: 14px;"><strong>📞 الهاتف:</strong> <span style="color: #fff; direction: ltr; display: inline-block;">{preview_phone}</span></div>
            <div style="margin-bottom: 15px; color: #e0e0e0; font-size: 14px;"><strong>📦 المنتج المطلوب:</strong> <span style="color: #00fff0;">{preview_product} (×{quantity})</span></div>
            <div style="background: rgba(0, 255, 240, 0.05); border-radius: 8px; padding: 12px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(0, 255, 240, 0.15);">
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
        render_marketing_hub_cyber_edition()
        
    # قفل فوري لقناة الاتصال بالـ DB مع نهاية المتجر لتجنب حدوث Lock حماية للـ RAM
    conne.close()
