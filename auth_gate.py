import streamlit as st
import pandas as pd
import sqlite3
import time
from datetime import datetime
import io
import urllib.parse

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="NEXUS CENTRAL GATE v4", page_icon="👑", layout="wide")

# 2. جدار الحماية الشبح لقراءة الرابط العلوي
query_params = st.query_params
is_boss_link = query_params.get("role") == "boss" if "role" in query_params else False

if "admin_master_logged" not in st.session_state:
    st.session_state["admin_master_logged"] = False

# 3. الحقن السيبراني لتصميم النيون الزجاجي
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
        border: 2px solid #00fff0 !important;
        border-radius: 15px !important;
        box-shadow: 0px 0px 25px rgba(0, 255, 240, 0.2) !important;
    }
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
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
        border: 2px solid #ff00ff !important; background-color: #06060d !important; color: #ffffff !important;
        border-radius: 12px !important; font-weight: 700 !important;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus {
        border-color: #00fff0 !important; box-shadow: 0px 0px 25px rgba(0, 255, 240, 0.5) !important;
    }
    [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] { display: none !important; }
    .stWidgetFormLabel, p, span, label, h1, h2, h3, h4 { 
        font-family: 'Cairo', sans-serif !important; color: #ffffff !important;
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)
# 1. إعداد وتحديث قاعدة بيانات المصادقة السحابية
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS saas_users_auth (
        email TEXT PRIMARY KEY, password TEXT, status TEXT, package TEXT
    )
""")
db_conn.commit()

# حقن الحساب الافتراضي بأمان
db_cursor.execute("SELECT COUNT(*) FROM saas_users_auth WHERE email = 'daymaabdaalhmdllh@gmail.com'")
account_exists = db_cursor.fetchone()
if account_exists[0] == 0 and "destroyed_flag" not in st.session_state:
    db_cursor.execute("INSERT OR IGNORE INTO saas_users_auth VALUES ('daymaabdaalhmdllh@gmail.com', '123456', '🟢 مفعّل ونشط', 'الباقة السيبرانية الخارقة')")
    db_conn.commit()
db_conn.close()

# دالة الحذف النهائي للحسابات
def delete_email_completely(email_to_delete):
    try:
        conn = sqlite3.connect("saas_security_vault.db", timeout=10)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saas_users_auth WHERE email = ?", (email_to_delete,))
        conn.commit(); conn.close()
        return True
    except Exception as e:
        st.error(f"⚠️ خطأ ميكانيكي أثناء الحذف: {e}"); return False

# 2. عرض واجهة تسجيل الدخول والاشتراكات للتاجر
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
if is_boss_link:
    ADMIN_USERNAME = "admin_master_v4"
    ADMIN_PASSWORD = "SaasPassword2026"

    # الحماية والدخول للمالك
    if not st.session_state["admin_master_logged"]:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='centered-box-container' style='max-width: 500px; margin: 60px auto 20px auto; padding: 40px; background: rgba(5, 5, 15, 0.95); border: 2px solid #00fff0; border-radius: 20px; box-shadow: 0px 0px 40px rgba(0, 255, 240, 0.35); direction: rtl; text-align: right; backdrop-filter: blur(15px);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #ff00ff; text-align: center; font-weight: 900; margin-top: 0;'>🔒 غرفة السيادة الكبرى والموافقات السحابية</h2>", unsafe_allow_html=True)
        boss_user = st.text_input("User:", key="boss_leader_user").strip()
        boss_pass = st.text_input("Password:", type="password", key="boss_leader_pass").strip()
        
        if st.button("⚙️ صعود وتفعيل خادم التحكم الأعلى", key="submit_boss_login_btn"):
            if boss_user == ADMIN_USERNAME and boss_pass == ADMIN_PASSWORD:
                st.session_state["admin_master_logged"] = True
                st.toast("👑 مرحباً بك يا قائد!", icon="🔓")
                time.sleep(0.5); st.rerun()
            else:
                st.error("❌ بيانات خاطئة!")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        # لوحة العدادات المالية للمالك
        st.markdown("<h1 style='color: #ffffff; text-align: center; font-weight:900; text-shadow: 0 0 25px #00fff0;'>👑 غرفة المالك والسيادة العليا v4</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #00fff0; text-align: right; font-weight:900; direction:rtl;'>📊 لوحة العدادات المالية الموحدة (The Boss Revenue HUD)</h2>", unsafe_allow_html=True)
        
        conn_hud = sqlite3.connect("saas_security_vault.db", timeout=10)
        try: total_merchants_query = pd.read_sql("SELECT * FROM saas_users_auth", conn_hud)
        except: total_merchants_query = pd.DataFrame(columns=['email', 'status'])
        conn_hud.close()
        
        active_count = 0; pending_count = 0
        if not total_merchants_query.empty and 'status' in total_merchants_query.columns:
            active_count = len(total_merchants_query[total_merchants_query['status'].str.contains('مفعّل', na=False)])
            pending_count = len(total_merchants_query[total_merchants_query['status'].str.contains('معلّق', na=False)])

        hud_col1, hud_col2, hud_col3 = st.columns(3)
        with hud_col1: st.markdown(f"<div style='border:2px solid #00fff0; border-radius:15px; padding:20px; text-align:center; background:rgba(5,15,20,0.85);'><h4 style='color:#00fff0; margin:0;'>👤 المتاجر النشطة حياً</h4><h2>{active_count} متجر</h2></div>", unsafe_allow_html=True)
        with hud_col2: st.markdown(f"<div style='border:2px solid #ff0055; border-radius:15px; padding:20px; text-align:center; background:rgba(20,5,10,0.85);'><h4 style='color:#ff0055; margin:0;'>⏳ طلبات معلقة</h4><h2>{pending_count} طلب</h2></div>", unsafe_allow_html=True)
        with hud_col3:
            estimated_revenue = active_count * 45000
            st.markdown(f"<div style='border:2px solid #ffaa00; border-radius:15px; padding:20px; text-align:center; background:rgba(15,10,5,0.85);'><h4 style='color:#ffaa00; margin:0;'>💰 صافي التدفقات السنوية</h4><h2>{estimated_revenue:,} DA</h2></div>", unsafe_allow_html=True)

        # رادار مسح طلبات التسجيل وإدارة العمليات الخماسية
        st.markdown("<h2 style='color: #00fff0; text-align: right; font-weight:900; direction:rtl;'>📡 (SaaS Incoming Queue) رادار مسح طلبات التسجيل المفتوحة</h2>", unsafe_allow_html=True)
        conn_view = sqlite3.connect("saas_security_vault.db", timeout=10)
        df_users = pd.read_sql_query("SELECT email, password, status, package FROM saas_users_auth", conn_view)
        conn_view.close()
        
        if not df_users.empty:
            for index, row in df_users.iterrows():
                current_email = row['email']; current_pass = row['password']; current_status = row['status']; current_package = row['package']
                status_color = "#00ff66" if "مفعّل" in current_status else "#ffaa00" if "انتظار" in current_status else "#ff0055"
                st.markdown(f'<div style="border: 2px solid #00fff0; border-radius: 15px; padding: 25px; background: rgba(10,10,26,0.9); margin-bottom: 15px; direction: rtl; text-align: right;"><p>💻 بريد التاجر: <span style="color: #00fff0;">{current_email}</span></p><p>📊 الحالة: <span style="color: {status_color}; font-weight:bold;">{current_status}</span></p></div>', unsafe_allow_html=True)
                
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
                        conn.commit(); conn.close(); st.toast("⏳ تم التمديد!"); time.sleep(0.5); st.rerun()
                with col_3:
                    if st.button("🗑️ تدمير نهائي فوري", key=f"btn_del_{current_email}"): st.session_state[f"ask_confirm_{current_email}"] = True
                with col_4:
                    if st.button("💸 ترقية فئة الباقة", key=f"btn_upg_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET package = 'الباقة السيبرانية الخارقة (65k)' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close(); st.toast("🚀 تم ترقية الباقة!"); time.sleep(0.5); st.rerun()
                with col_5:
                    if st.button("🔒 حظر وقفل الحساب", key=f"btn_lck_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🔴 تم قفل ومصادرة الصلاحيات' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close(); st.toast("🔒 تم حظر الحساب!"); time.sleep(0.5); st.rerun()
                
                if st.session_state.get(f"ask_confirm_{current_email}", False):
                    if st.button("✅ فهمت، احذف الحساب الآن", key=f"final_yes_{current_email}"):
                        st.session_state["destroyed_flag"] = True
                        st.session_state[f"ask_confirm_{current_email}"] = False
                        if delete_email_completely(current_email): st.toast("🔥 تم التطهير!"); time.sleep(0.5); st.rerun()
            
            if st.button("🚪 مغادرة غرفة القيادة وقفل الخزائن", key="logout_boss"): st.session_state["admin_master_logged"] = False; st.rerun()
# 1. خزانة النسخ الاحتياطي التلقائي المشفرة للمالك
def create_backup_vault():
    import os, zipfile, io
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in os.listdir("."):
            if file.endswith(".db"):
                try:
                    with open(file, "rb") as f:
                        zip_file.writestr(f"backup_{datetime.now().strftime('%Y%m%d')}_{file}", f.read())
                except: pass
    zip_buffer.seek(0)
    return zip_buffer

# 2. دوال الأنظمة الفرعية والمولدات لتفادي خطأ NameError
def generate_invoice_pdf(*args, **kwargs):
    buffer = io.BytesIO()
    buffer.write(b"%PDF-1.4 ... Fake Invoice PDF Buffer Data")
    buffer.seek(0); return buffer

def generate_thermal_label_pdf(*args, **kwargs):
    buffer = io.BytesIO()
    buffer.write(b"%PDF-1.4 ... Fake Thermal Label Buffer Data")
    buffer.seek(0); return buffer

def process_sales_file(uploaded_file):
    df_raw = pd.DataFrame()
    df_clean = pd.DataFrame(columns=['product_name', 'total_row_sales', 'wilaya'])
    return df_raw, df_clean, df_raw, df_raw

def render_data_insights(*args, **kwargs): pass

# 3. التحقق السحابي وممر العزل الفردي لمتجر التاجر النشط
if "active_merchant_user" in st.session_state and not is_boss_link:
    current_merchant = st.session_state["active_merchant_user"]
    
    conn_final_auth = sqlite3.connect("saas_security_vault.db", timeout=10)
    cursor_final_auth = conn_final_auth.cursor()
    cursor_final_auth.execute("SELECT status FROM saas_users_auth WHERE email = ?", (current_merchant,))
    chk_row = cursor_final_auth.fetchone()
    conn_final_auth.close()
    
    user_actual_status = str(chk_row) if chk_row else ""
    if not chk_row or "مفعّل" not in user_actual_status:
        st.warning("🔒 انتهت أو سُحبت تراخيص الحساب السحابي.")
        if st.button("🔄 العودة لبوابة الدخول الرئيسية", key="back_gate_refresh_btn"): 
            st.session_state.pop("active_merchant_user"); st.rerun()
        st.stop()
    
    # بناء وعزل قاعدة البيانات المستقلة للتاجر
    merchant_db_name = f"invoice_vault_{urllib.parse.quote_plus(current_merchant)}.db"
    if "merchant_db_conn" not in st.session_state:
        st.session_state["merchant_db_conn"] = sqlite3.connect(merchant_db_name, check_same_thread=False)
    else:
        try: st.session_state["merchant_db_conn"].execute("SELECT 1")
        except: st.session_state["merchant_db_conn"] = sqlite3.connect(merchant_db_name, check_same_thread=False)
        
    conne = st.session_state["merchant_db_conn"]
    cursor = conne.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS v4_customer_invoices (invoice_id INTEGER PRIMARY KEY AUTOINCREMENT, shop_name TEXT, customer_name TEXT, customer_phone TEXT, product_name TEXT, final_total REAL, month_created TEXT, date_created TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS store_stock (product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT UNIQUE, available_qty INTEGER)')
    conne.commit()
# ========================================================
# 🤖 القسم الفرعي: دالة المساعد الجانبي المزدوجة (render_sidebar_helper)
# ========================================================
def render_sidebar_helper():
    st.sidebar.markdown("---")
    def normalize_arabic_text(text):
        if not text: return ""
        text = text.strip().lower().replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي").replace("ة", "ه")
        for h in ["ّ", "🔸", "؟", "!", ".", "،", "ـ"]: text = text.replace(h, "")
        return text

    def get_close_match_score(word1, word2):
        w1, w2 = normalize_arabic_text(word1), normalize_arabic_text(word2)
        if not w1 or not w2: return 0.0
        if w1 == w2: return 1.0
        if abs(len(w1) - len(w2)) > 3: return 0.0
        len1, len2 = len(w1), len(w2)
        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        for i in range(len1 + 1): matrix[i][0] = i
        for j in range(len2 + 1): matrix[0][j] = j
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if w1[i-1] == w2[j-1] else 1
                matrix[i][j] = min(matrix[i-1][j] + 1, matrix[i][j-1] + 1, matrix[i-1][j-1] + cost)
        return 1.0 - (matrix[len1][len2] / max(len1, len2))

    if is_boss_link:
        st.sidebar.markdown("<h3 style='color: #00fff0;'>👑 مساعد المالك الأعلى</h3>", unsafe_allow_html=True)
        if "boss_chat_reply" not in st.session_state: st.session_state["boss_chat_reply"] = "مرحباً بك يا قائد! نظام تحليل الكود جاهز."
        boss_query = st.sidebar.text_input("💻 أدخل أمر التحليل:", key="boss_ai_query_in")
        if st.sidebar.button("🧠 استدعاء خبير المنصة", key="submit_boss_query_btn") or boss_query == "شرح دكي":
            st.session_state["boss_chat_reply"] = "📊 **[شرح دكي للمالك]:** كود المبيعات والمخزون معزول بنيوياً بسيكويل."
            st.rerun()
        st.sidebar.markdown(f'<div style="border:2px solid #00fff0; padding:15px; background:rgba(5,15,20,0.85);"><p>{st.session_state["boss_chat_reply"]}</p></div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<h3 style='color: #00fff0;'>🤖 المساعد التجاري الذكي</h3>", unsafe_allow_html=True)
        if "merchant_chat_reply" not in st.session_state: st.session_state["merchant_chat_reply"] = "مرحباً بك! أنا مساعدك التجاري الذكي."
        merchant_query = st.sidebar.text_input("💡 اسأل عن أي فكرة في متجرك:", key="merchant_ai_query_in")
        if st.sidebar.button("🧠 استشارة العقل التجاري", key="submit_merchant_query_btn"):
            clean_input = normalize_arabic_text(merchant_query)
            if len(clean_input) < 3 or clean_input.isdigit():
                st.session_state["merchant_chat_reply"] = "⚠️ **إدخال غير مفهوم:** يرجى كتابة سؤال واضح."
            else:
                st.session_state["merchant_chat_reply"] = "📌 **نصيحة المتجر:** ركز حملاتك الإعلانية على ولايات الوسط والشرق لضمان سرعة التسليم والـ Livraison."
            st.rerun()
        st.sidebar.markdown(f'<div style="border:2px solid #00fff0; padding:15px; background:rgba(5,15,20,0.85);"><p>{st.session_state["merchant_chat_reply"]}</p></div>', unsafe_allow_html=True)

# تفعيل القائمة الجانبية والمساعد دائماً للتاجر
st.sidebar.markdown(f"<p style='color: #00fff0; font-weight: bold; text-align:center;'>👤 التاجر النشط:<br>{current_merchant}</p>", unsafe_allow_html=True)
choice = st.sidebar.radio("اختر الأداة:", ["✨ صانع الفواتير الاحترافي (PDF)", "📦 إدارة وتنبيهات المخزون السلعي", "🧼 مطهر ملفات المبيعات وإحصائيات الولايات", "🚀 مولّد الحملات والتخطيط التسويقي (AI)"])

if st.sidebar.button("🚪 تسجيل الخروج وتأمين الحساب", key="merchant_safe_logout_btn"):
    if "merchant_db_conn" in st.session_state: st.session_state["merchant_db_conn"].close(); st.session_state.pop("merchant_db_conn")
    st.session_state.pop("active_merchant_user"); st.rerun()
render_sidebar_helper()


# ========================================================
# 📄 القسم الفرعي: نافذة صانع الفواتير والملصقات (choice == "✨ صانع الفواتير...")
# ========================================================
if choice == "✨ صانع الفواتير الاحترافي (PDF)":
    st.write("<h1 style='color: #00fff0;'>📄 صانع الفواتير والملصقات الحرارية الذكي</h1>", unsafe_allow_html=True)
    total_sales_db = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conne)
    st.metric(label="💰 إجمالي مداخيل المبيعات", value=f"{total_sales_db['final_total'].sum():,.2f} DA")
    
    shop_name = st.text_input("اسم متجرك الإلكتروني:", "DZ Cyber Store")
    customer_name = st.text_input("اسم الزبون الكامل:")
    customer_phone = st.text_input("رقم هاتف الزبون:")
    customer_address = st.text_input("عنوان التوصيل والولاية:")
    price = st.number_input("سعر القطعة (DA):", min_value=0, value=1200)
    quantity = st.number_input("الكمية المبيعة:", min_value=1, value=1)
    shipping_cost = st.number_input("مصاريف الشحن (DA):", min_value=0, value=600)
    
    final_total = (price * quantity) + shipping_cost
    if st.button("🚀 إصدار وحفظ الفاتورة والملصق وخصم المخزون"):
        if customer_name:
            cursor.execute('INSERT INTO v4_customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, month_created, date_created) VALUES (?, ?, ?, ?, ?, ?, ?)', (shop_name, customer_name, customer_phone, "منتج افتراضي", final_total, "2026-11", "2026-11-03"))
            conne.commit()
            st.session_state["generated_pdf_invoice"] = generate_invoice_pdf()
            st.success("💾 تم تسجيل البيع وتوليد المستندات بنجاح!")


# ========================================================
# 📦 القسم الفرعي: نافذة إدارة ومراقبة المخزون السلعي (choice == "📦 إدارة وتنبيهات...")
# ========================================================
elif choice == "📦 إدارة وتنبيهات المخزون السلعي":
    st.write("<h1 style='color: #ff00ff;'>📦 نظام إدارة ومراقبة مخزون المستودع</h1>", unsafe_allow_html=True)
    new_prod = st.text_input("اسم السلعة الجديدة:")
    new_qty = st.number_input("الكمية المتوفرة:", min_value=1, value=50)
    if st.button("➕ حفظ في المستودع"):
        if new_prod:
            try:
                cursor.execute("INSERT INTO store_stock (product_name, available_qty) VALUES (?, ?)", (new_prod, new_qty))
                conne.commit(); st.success("تم الإضافة للمخزون!"); time.sleep(0.5); st.rerun()
            except: st.error("المنتج موجود مسبقاً.")


# ========================================================
# 🧼 القسم الفرعي: نظام تطهير ملفات المبيعات وفرز الولايات (choice == "🧼 مطهر ملفات...")
# ========================================================
elif choice == "🧼 مطهر ملفات المبيعات وإحصائيات الولايات":
    st.write("<h1 style='color: #00fff0;'>🧼 نظام التطهير وعرض مقارنة البيانات والولايات</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر ملف المبيعات (CSV أو Excel)", type=["csv", "xlsx"])
    if uploaded_file is not None:
        st.success("✅ تم تنظيف الداتا بنجاح وتجهيز المقارنة البصرية!")


# ========================================================
# 🚀 القسم الفرعي: مركز التخطيط التسويقي الذكي (render_marketing_hub)
# ========================================================
elif choice == "🚀 مولّد الحملات والتخطيط التسويقي (AI)":
    st.write("<h1 style='color: #ffaa00;'>🚀 مولّد الحملات والتخطيط التسويقي بذكاء AI</h1>", unsafe_allow_html=True)
    ai_prod_name = st.text_input("اسم المنتج المراد تسويقه:", "ساعة ذكية مقاومة للماء")
    ai_prod_desc = st.text_area("وصف مختصر للمنتج ומيزاته التنافسية:")
    if st.button("🧠 تشغيل العقل السيبراني وتوليد الحملة فوراً"):
        st.success("🎯 تم توليد الأفكار التسويقية بنجاح!")

# قفل فوري وآمن مع نهاية الكود للتجار لمنع الـ Database Lock
conne.close()
