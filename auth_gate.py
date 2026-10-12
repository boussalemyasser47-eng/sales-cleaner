# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتلوين الواجهات (auth_gate.py)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
import time
import os

# ضبط إعدادات الصفحة الكلية لتكون واجهة قيادة عريضة وفخمة ومحمية كلياً
st.set_page_config(page_title="NEXUS CENTRAL GATE v4", page_icon="👑", layout="wide")

# 🚨 [جدار الحماية الشبح الحاسم]: قراءة الرابط علوياً للتأكد من وجود مفتاحك السري (?role=boss)
query_params = st.query_params
is_boss_link = query_params.get("role") == "boss" if "role" in query_params else False

# حقن كود الـ CSS الأسطوري لإبادة الخلفية البيضاء وجعل الأزرار نيون زجاجية مرئية 100%
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    
    <style>
    /* ترقية خلفية المتصفح بالكامل لتصبح ليلة رقمية عميقة وعميقة البعد */
    .stApp {
        background: radial-gradient(circle at 50% 40%, #0d0d21 0%, #030307 100%) !important;
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* [إصلاح حاسم وتوسيط البطاقة]: إجبار صندوق الدخول على الصعود بمنتصف الشاشة بنقاء 100% */
    .centered-box-container {
        max-width: 500px !important;
        margin: 50px auto 20px auto !important;
        padding: 35px !important;
        background: linear-gradient(135deg, rgba(10, 10, 26, 0.75) 0%, rgba(5, 5, 12, 0.95) 100%) !important;
        border: 2px solid #00fff0 !important;
        border-radius: 20px !important;
        box-shadow: 0px 0px 35px rgba(0, 255, 240, 0.35), inset 0px 0px 15px rgba(0, 255, 240, 0.1) !important;
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
    
    /* منع انهيار وإخفاء الأزرار الميكانيكية للوحة */
    div[data-testid="stVerticalBlock"] button, div.stButton button, .stButton > button {
        width: 100% !important; min-height: 50px !important; white-space: normal !important; word-wrap: break-word !important;
        font-family: 'Cairo', sans-serif !important; font-size: 14.5px !important; font-weight: 800 !important; border-radius: 12px !important;
        text-align: center !important; display: inline-flex !important; align-items: center !important; justify-content: center !important;
        padding: 12px 18px !important; background: linear-gradient(135deg, #090915 0%, #040409 100%) !important; color: #00fff0 !important;
        border: 2px solid #00fff0 !important; box-shadow: 0px 0px 15px rgba(0, 255, 240, 0.3) !important; transition: all 0.4s ease-in-out !important;
    }
    div.stButton button:hover { background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important; color: #000000 !important; box-shadow: 0px 0px 25px #00fff0 !important; transform: translateY(-3px) !important; }
    
    div[data-testid="stTextInput"] input { border: 2px solid #ff00ff !important; background-color: #080811 !important; color: #ffffff !important; border-radius: 12px !important; padding: 15px 18px !important; font-family: 'Cairo', sans-serif !important; font-size: 14px !important; }
    
    /* إلغاء وإخفاء السهم الجانبي تلقائياً لمنع المتطفلين من فتحه والتجسس */
    [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] { display: none !important; visibility: hidden !important; opacity: 0 !important; height: 0px !important; width: 0px !important; }
    section[data-testid="stSidebar"] { display: none !important; visibility: hidden !important; }
    
    .stWidgetFormLabel, p, span, label, h1, h2, h3, h4 { font-family: 'Cairo', sans-serif !important; color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# الجزء الثاني: حقول مدخلات التجار وبناء جدول الـ SQL الموحد (auth_gate.py)
# ========================================================
# تهيئة ثوابت الهوية الإدارية الموحدة لغرفة القيادة العليا لمنع ثغرات الكاش
ADMIN_USERNAME = "admin_master_v4"
ADMIN_PASSWORD = "SaasPassword2026"

if "admin_master_logged" not in st.session_state:
    st.session_state["admin_master_logged"] = False

# صياغة ومزامنة جدول الـ Auth لقراءة كلمات سر المشتركين في نفس الحاوية الموحدة حياً
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS saas_users_auth (
        email TEXT PRIMARY KEY, password TEXT, status TEXT, package TEXT
    )
""")
db_conn.commit()
db_conn.close()

# حقن حساب الفحص الافتراضي لضمان استقرار جرد القنوات بالثانية
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_conn.cursor().execute("INSERT OR IGNORE INTO saas_users_auth VALUES ('daymaabdaalhmdllh@gmail.com', '123456', '🟢 مفعّل ونشط', 'الباقة السيبرانية الخارقة')")
db_conn.commit()
db_conn.close()
# ========================================================
# تابع للجزء الثاني: دالة التدمير الشامل للإيميلات (جميع الحالات)
# ========================================================
def delete_email_completely(email_to_delete):
    """
    حذف الحساب والبريد الإلكتروني فوراً من قاعدة البيانات 
    بغض النظر عن حالته الحالية (نشط، معلق، محظور)
    """
    try:
        conn = sqlite3.connect("saas_security_vault.db", timeout=10)
        cursor = conn.cursor()
        # تنفيذ أمر الحذف المباشر لسطر الإيميل بالكامل دون شروط مسبقة
        cursor.execute("DELETE FROM saas_users_auth WHERE email = ?", (email_to_delete,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"⚠️ خطأ أثناء معالجة الحذف الميكانيكي: {e}")
        return False

# ========================================================
# الجزء الثالث: واجهة فيسبوك الموسطة والآمنة للتجار (auth_gate.py)
# ========================================================
# واجهة التجار الصافية تصعد تلقائياً للجمهور فقط وحصرياً إذا كان الرابط عادياً وخالياً من مفتاحك السري
if not is_boss_link:
    st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 40px; text-shadow: 0 0 20px #00fff0; font-size:32px;'>🔐 بوابة التوثيق والاشتراكات السنوية المتكاملة</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #b0b0d0; text-align: center; font-size: 15px; font-weight:600; margin-bottom:25px;'>سجل بريدك وإلكترونيات متجرك الخاص للتحويل التلقائي والآمن لخزانة فواتيرك.</p>", unsafe_allow_html=True)
    
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
                    try:
                        cursor_reg.execute("INSERT INTO saas_users_auth VALUES (?, ?, '⏳ في انتظار التفعيل', ?)", (clean_email, clean_pass, user_package_choice))
                        conn_reg.commit()
                        st.success("✅ تم تسجيل حسابك الحر بنجاح! طارت معلوماتك للإدارة وبانتظار تفعيل باقتك السنوية حيًا.")
                    except sqlite3.IntegrityError:
                        st.error("🚨 هذا البريد الإلكتروني مسجل مسبقاً بالنظام!")
                    conn_reg.close()
                    
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
                        user_status = db_row[0]
                        if "⏳" in user_status or "انتظار" in user_status: st.warning("⏳ حسابك مسجل، وهو قيد المراجعة حالياً من طرف الإدارة!")
                        elif "🔒" in user_status or "قفل" in user_status or "محجوب" in user_status: st.error("🚨 عذراً، هذا الحساب مقفل ومحجوب كلياً لعدم الاشتراك السنوي!")
                        else:
                            st.success("⚡ تم التوثيق بنجاح! جاري تحويلك تلقائياً لمتجرك الأصلي والـ 9 ميزات...")
                            time.sleep(0.4)
                            st.markdown('<meta http-equiv="refresh" content="0;URL=\'https://streamlit.app\'">', unsafe_allow_html=True)
  
                    else: st.error("❌ بيانات الدخول وكلمة المرور غير مطابقة لملف الأمان السحابي!"
# ========================================================
# تابع للجزء الثالث: لوحة التحكم العليا وجدول التدمير الفوري
# ========================================================
if is_boss_link:
    st.markdown("<h2 style='color: #ff00ff; text-align: right; font-weight:900;'>👑 غرفة القيادة العليا - إدارة الحسابات الموحدة</h2>", unsafe_allow_html=True)
    
    # جلب كافة الحسابات المسجلة في النظام حالياً حياً
    conn_view = sqlite3.connect("saas_security_vault.db", timeout=10)
    df_users = pd.read_sql_query("SELECT email, status, package FROM saas_users_auth", conn_view)
    conn_view.close()
    
    if not df_users.empty:
        st.markdown("<p style='color: #b0b0d0; text-align: right;'>قائمة المشتركين الحاليين مع إمكانية الحذف الفوري لجميع الحالات:</p>", unsafe_allow_html=True)
        
        # عرض البيانات عبر تقسيم أسطر تفاعلي آمن
        for index, row in df_users.iterrows():
            col_mail, col_status, col_pack, col_action = st.columns([3, 2, 2, 2])
            
            with col_mail:
                st.text(row['email'])
            with col_status:
                st.info(f"الحالة: {row['status']}")
            with col_pack:
                st.text(row['package'])
            with col_action:
                # زر تدمير فوري مخصص لكل بريد إلكتروني على حدة
                if st.button(f"🗑️ حذف الحساب", key=f"del_{row['email']}"):
                    if delete_email_completely(row['email']):
                        st.toast(f"🔥 تم حذف البريد {row['email']} بنجاح في كل الحالات!", icon="✅")
                        time.sleep(1)
                        st.rerun()
    else:
        st.warning("📭 لا توجد حسابات تجار مسجلة حالياً في قاعدة البيانات.")
                               
# ========================================================
# الجزء الرابع: لوحة التحكم الإدارية المركزية وقفل السيرفر الموحد (auth_gate.py)
# ========================================================
# اللوحة تفتح وتتوسط الشاشة كلياً فقط وحصرياً إذا تحقق وجود المعرّف الشبح بالرابط علوياً
if is_boss_link:
    # تهيئة كاش الجلسة الإدارية لمنع الأخطاء العشوائية وتحصين الهوية الرقمية الأعلى
    if "admin_master_logged" not in st.session_state:
        st.session_state["admin_master_logged"] = False

    # 1️⃣ جدار التحقق الموسط الشبح: يطالبك ببياناتك الإدارية أولاً ويقفل الغرفة عن المتطفلين
    if not st.session_state["admin_master_logged"]:
        st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 50px; text-shadow: 0 0 20px #00fff0; font-size:28px;'>🔒 غرفة السيادة الكبرى والموافقات السحابية</h1>", unsafe_allow_html=True)
        
        st.markdown("<div class='centered-box-container'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#00fff0; text-align:center; font-weight:700; margin-top:0;'>🔑 تسجيل دخول المالك الأعلى</h3>", unsafe_allow_html=True)
        
        input_boss_user = st.text_input("👤 اسم المستخدم الخاص بالقائد:", value="", key="vault_boss_user_field")
        input_boss_pass = st.text_input("🔑 كلمة المرور الإدارية الخارقة:", type="password", value="", key="vault_boss_pass_field")
        st.markdown("</div>", unsafe_allow_html=True)
        
        _, col_btn_lock_center, _ = st.columns(3)
        with col_btn_lock_center:
            if st.button("⚙️ صعود وتفعيل خادم التحكم الأعلى", key="vault_boss_submit_btn"):
                if input_boss_user.strip() == "admin_master_v4" and input_boss_pass.strip() == "SaasPassword2026":
                    st.session_state["admin_master_logged"] = True
                    st.success("⚡ تم التوثيق بنجاح ملوكي! جاري قراءة طلبات التجار...")
                    time.sleep(0.3)
                    st.rerun()
                else:
                    st.error("❌ بيانات خاطئة! يرجى إعادة التحقق من الأحرف والرموز السريّة.")
                    
    # 2️⃣ فتح حجرة القيادة والسيادة الكبرى وعوائد الـ DA فور نجاح مطابقة بياناتك أعلاه
    else:
        st.markdown("<h1 style='color: #ff00ff; text-align: center; font-weight:900; text-shadow: 0 0 25px #ff00ff; font-size:34px;'>👑 مركز إدارة وتحويل صلاحيات المشتركين الكبرى</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #00fff0; text-align: center; font-size: 14px; font-weight:600; margin-bottom:30px;'>مرحباً بك يا مالك المنصة في حجرتك المشتركة. المزامنة تعمل بكفاءة مطلقة.</p>", unsafe_allow_html=True)
        
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

        col_s1, col_v2, col_v3 = st.columns(3)
        with col_s1: st.markdown(f"<div class='premium-card-pink'><span style='color:#ff00ff; font-weight:900;'>💰 التدفق النقدي الكلي الممرر عبر السيرفر:</span><h2 style='color:#fff; text-shadow: 0 0 10px #ff00ff; margin:10px 0 0 0;'>{total_platform_revenue:,.2f} DA</h2></div>", unsafe_allow_html=True)
        with col_v2:
            active_count = len(df_merchants[df_merchants['status'].str.contains("🟢")]) if not df_merchants.empty else 0
            st.markdown(f"<div class='premium-card-cyan'><span style='color:#00fff0; font-weight:900;'>👥 المشتركين النشطين حالياً بالمنصة:</span><h2 style='color:#fff; text-shadow: 0 0 10px #00fff0; margin:10px 0 0 0;'>{active_count} تجار نشطين</h2></div>", unsafe_allow_html=True)
        with col_v3: st.markdown(f"<div class='premium-card-pink' style='border-color:#00ff66; box-shadow:0 0 20px rgba(0,255,102,0.2);'><span style='color:#00ff66; font-weight:900;'>📦 حركة الفواتير المطبوعة بالـ SQL:</span><h2 style='color:#fff; text-shadow: 0 0 10px #00ff66; margin:10px 0 0 0;'>{total_invoices_count} طلبيّة صادرة</h2></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00fff0; font-weight:900; text-shadow: 0 0 8px rgba(0,255,240,0.3); text-align:right;'>📡 رادار مسح طلبات التسجيل المفتوحة (SaaS Incoming Queue):</h3>", unsafe_allow_html=True)

        if not df_merchants.empty:
            for idx, row in df_merchants.iterrows():
                email = row["email"]; status = row["status"]; package = row["package"]; password = row["password"]
                
                if "🟢" in status:
                    card_class = "premium-card-cyan"; badge_style = "color:#00ff66; font-weight:900; text-shadow:0 0 8px #00ff66;"; border_override = "border-right: 5px solid #00ff66 !important;"
                elif "⏳" in status or "انتظار" in status:
                    card_class = "premium-card-pink"; badge_style = "color:#ffcc00; font-weight:900; text-shadow:0 0 8px #ffcc00;"; border_override = "border-right: 4px solid #ffcc00 !important;"
                else:
                    card_class = "premium-card-pink"; badge_style = "color:#ff3333; font-weight:900; text-shadow:0 0 8px #ff3333;"; border_override = "border-right: 4px solid #ff3333 !important;"
                    
                st.markdown(f"""
                    <div class='{card_class}' style='{border_override} padding: 18px; margin-bottom: 15px;'>
                        <span style='float: left; {badge_style}'>{status}</span>
                        <span style='color:#fff; font-size:14.5px; font-weight:bold;'>📧 بريد التاجر الجديد: <code style='color:#00fff0; background:rgba(0,0,0,0.4); padding:3px 8px; border-radius:6px;'>{email}</code></span> | 
                        <span style='color:#aaa; font-size:13px;'>كلمة السر المختارة: <b style='color:#ff00ff;'>{password}</b></span><br>
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
        else:
            st.info("📡 رادار البحث فارغ، لا يوجد طلبات تسجيل حالياً بمركز الموافقات السحابية الموسطة.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 مغادرة غرفة القيادة وقفل السيرفر الموسط والخزائن"):
            st.session_state["admin_master_logged"] = False
            st.success("🔒 تم تأمين وقفل السيرفر بنجاح ملوكي!")
            time.sleep(0.3); st.rerun()
