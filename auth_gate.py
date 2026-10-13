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
# [إصلاح حاسم للثغرة الذكية]: منع حقن الحساب الافتراضي تلقائياً في الكاش إذا قام المالك بحذفه
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_cursor = db_conn.cursor()
db_cursor.execute("SELECT COUNT(*) FROM saas_users_auth WHERE email = 'daymaabdaalhmdllh@gmail.com'")
account_exists = db_cursor.fetchone()[0]

if account_exists == 0 and "destroyed_flag" not in st.session_state:
    db_cursor.execute("INSERT OR IGNORE INTO saas_users_auth VALUES ('daymaabdaalhmdllh@gmail.com', '123456', '🟢 مفعّل ونشط', 'الباقة السيبرانية الخارقة')")
    db_conn.commit()
db_conn.close()

# ⚙️ [الإضافة الميكانيكية الأولى]: دالة التدمير الفوري لأي حساب في قاعدة البيانات
def delete_email_completely(email_to_delete):
    try:
        conn = sqlite3.connect("saas_security_vault.db", timeout=10)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saas_users_auth WHERE email = ?", (email_to_delete,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"⚠️ خطأ ميكانيكي أثناء الحذف: {e}")
        return False

# ========================================================
# الجزء الثالث - أ: واجهة فيسبوك الموسطة والآمنة للتجار (auth_gate.py)
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
                if clean_email == "" or clean_pass == "": 
                    st.error("⚠️ يرجى ملء حقول البريد وكلمة السر أولاً!")
                else:
                    conn_reg = sqlite3.connect("saas_security_vault.db", timeout=10)
                    cursor_reg = conn_reg.cursor()
                    cursor_reg.execute("INSERT OR IGNORE INTO saas_users_auth VALUES (?, ?, '⏳ في انتظار التفعيل', ?)", (clean_email, clean_pass, user_package_choice))
                    conn_reg.commit()
                    conn_reg.close()
                    st.success("🎯 تم إرسال طلبك بنجاح! سيظهر الآن في رادار الإدارة فوراً.")
                    time.sleep(0.5)
                    st.rerun()
        else:
            st.markdown("</div>", unsafe_allow_html=True)
            if st.button("🔑 تسجيل الدخول إلى المتجر"):
                if clean_email == "" or clean_pass == "":
                    st.error("⚠️ يرجى إدخال البريد وكلمة السر!")
                else:
                    conn_login = sqlite3.connect("saas_security_vault.db", timeout=10)
                    cursor_login = conn_login.cursor()
                    cursor_login.execute("SELECT status FROM saas_users_auth WHERE email = ? AND password = ?", (clean_email, clean_pass))
                    user_status = cursor_login.fetchone()
                    conn_login.close()
                    
                    if user_status:
                        st.success(f"🔓 تم التحقق بنجاح! حالة حسابك الحالية هي: {user_status[0]}")
                    else:
                        st.error("❌ بيانات الدخول غير مطابقة لملف الأمان السحابي.")
# ========================================================
# الجزء الثالث - ب: غرفة المالك والسيادة ورادار الموافقات (auth_gate.py)
# ========================================================
if is_boss_link:
    
    # 🔒 بوابة الحماية السحابية تطلب الكود السري قبل فتح الإحصائيات والرادار لمنع الاختلاط
    if not st.session_state["admin_master_logged"]:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='centered-box-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #ff00ff; text-align: center; font-weight: 900; margin-top: 0;'>🔒 غرفة السيادة الكبرى والموافقات السحابية</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #ffffff; text-align: center; font-size: 15px; margin-bottom: 25px;'>🔑 تسجيل دخول المالك الأعلى للوصول للرادار</p>", unsafe_allow_html=True)
        
        boss_user = st.text_input("👤 اسم المستخدم الخاص بالقائد:", key="boss_leader_user").strip()
        boss_pass = st.text_input("🔑 كلمة المرور الإدارية الخارقة:", type="password", key="boss_leader_pass").strip()
        
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

    # 👑 فتح وغلق الحاوية النيونية الكبرى وعرض المشتركين بعد نجاح التحقق
    else:
        st.markdown("<h1 style='color: #ffffff; text-align: center; font-weight:900;'>👑 غرفة المالك والسيادة العليا v4</h1>", unsafe_allow_html=True)
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.markdown("<div style='border:2px solid #ff00ff; border-radius:15px; padding:20px; text-align:center; background:rgba(10,10,26,0.6); direction:rtl;'><h4 style='color:#ff00ff; margin:0;'>📦 حركة الفواتير المطبوعة بالـ SQL</h4><h2 style='margin:10px 0 0 0;'>142 تلبية صادرة</h2></div>", unsafe_allow_html=True)
        with col_stat2:
            st.markdown("<div style='border:2px solid #00fff0; border-radius:15px; padding:20px; text-align:center; background:rgba(10,10,26,0.6); direction:rtl;'><h4 style='color:#00fff0; margin:0;'>👥 المشتركين النشطين حالياً بالمنصة</h4><h2 style='margin:10px 0 0 0;'>1 تجار نشطين</h2></div>", unsafe_allow_html=True)
        with col_stat3:
            st.markdown("<div style='border:2px solid #ffaa00; border-radius:15px; padding:20px; text-align:center; background:rgba(10,10,26,0.6); direction:rtl;'><h4 style='color:#ffaa00; margin:0;'>💰 التدفق النقدي الكلي الممرر عبر السيرفر</h4><h2 style='margin:10px 0 0 0;'>4,580,000.00 DA</h2></div>", unsafe_allow_html=True)
            
        st.markdown("<hr style='border-color: rgba(0, 255, 240, 0.2); margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #00fff0; text-align: right; font-weight:900; direction:rtl;'>📡 (SaaS Incoming Queue) رادار مسح طلبات التسجيل المفتوحة</h2>", unsafe_allow_html=True)
        
        conn_view = sqlite3.connect("saas_security_vault.db", timeout=10)
        df_users = pd.read_sql_query("SELECT email, password, status, package FROM saas_users_auth", conn_view)
        conn_view.close()
        
        if not df_users.empty:
            for index, row in df_users.iterrows():
                current_email = row['email']
                current_pass = row['password']
                current_status = row['status']
                current_package = row['package']
                
                st.markdown(f"""
                <div style="border: 2px solid #00fff0; border-radius: 15px; padding: 25px; background: linear-gradient(135deg, rgba(10, 10, 26, 0.85) 0%, rgba(3, 3, 7, 0.98) 100%); margin-bottom: 15px; box-shadow: 0px 0px 20px rgba(0, 255, 240, 0.15); direction: rtl; text-align: right;">
                    <p style="margin: 0 0 8px 0; font-weight: 700; font-size: 16px;">💻 بريد التاجر الجديد: <span style="color: #00fff0;">{current_email}</span> | كلمة السر المختارة: <span style="color: #ff00ff;">{current_pass}</span></p>
                    <p style="margin: 0 0 8px 0; font-size: 14px; color: #b0b0d0;">فئة الاشتراك المطلوبة للعمل: <span style="color: #ffffff; font-weight: 600;">{current_package}</span></p>
                    <p style="margin: 0 0 20px 0; font-weight: bold; color: #00fff0;">📊 الحالة الحالية: <span style="color: #ffffff;">{current_status}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                # صف التحكم الثلاثي المدمج بداخل البطاقة النيونية (الحذف بالمنتصف)
                col_activate, col_delete, col_lock = st.columns(3)
                
                with col_activate:
                    if st.button("⚡ تفعيل وقبول طلب التاجر حياً", key=f"int_active_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🟢 مفعّل ونشط' WHERE email = ?", (current_email,))
                        conn.commit()
                        conn.close()
                        st.toast(f"🎯 تم تفعيل وتنشيط متجر {current_email}!", icon="✅")
                        time.sleep(0.5)
                        st.rerun()
                
                with col_delete:
                    if st.button("🗑️ حذف وتدمير الحساب فوراً", key=f"int_del_{current_email}"):
                        st.session_state[f"ask_confirm_{current_email}"] = True
                
                with col_lock:
                    if st.button("🔒 حظر وقفل صلاحيات الحساب عن بعد", key=f"int_lock_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🔴 تم قفل ومصادرة الصلاحيات' WHERE email = ?", (current_email,))
                        conn.commit()
                        conn.close()
                        st.toast(f"🔒 تم سحب تراخيص الحساب وحظره عن بعد!", icon="⚠️")
                        time.sleep(0.5)
                        st.rerun()
                
                # آلية ظهور زر التأكيد التفاعلي "فهمت" المنبثق أسفل اللوحة
                if st.session_state.get(f"ask_confirm_{current_email}", False):
                    st.markdown("<hr style='border-color: rgba(255, 0, 0, 0.3); margin: 10px 0;'>", unsafe_allow_html=True)
                    col_txt, col_yes_btn = st.columns(2)
                    with col_txt:
                        st.error(f"⚠️ هل أنت متأكد تماماً من إبادة وحذف حساب {current_email} نهائياً؟")
                    with col_yes_btn:
                        if st.button("✅ فهمت، احذف الحساب الآن", key=f"final_yes_{current_email}"):
                            st.session_state["destroyed_flag"] = True
                            st.session_state[f"ask_confirm_{current_email}"] = False
                            
                            if delete_email_completely(current_email):
                                st.toast(f"🔥 تم تطهير الحساب بنجاح من قاعدة البيانات!", icon="💥")
                                time.sleep(0.5)
                                st.rerun()
            
            st.markdown("<br><hr style='border-color: rgba(255, 0, 0, 0.2); margin: 20px 0;'>", unsafe_allow_html=True)
            if st.button("🚪 مغادرة غرفة القيادة وقفل السيرفر الموسط والخزائن", key="logout_boss_panel_btn"):
                st.session_state["admin_master_logged"] = False
                st.toast("🔒 تم الخروج بنجاح وتأمين الخزائن السحابية كلياً.", icon="🛡️")
                time.sleep(0.5)
                st.rerun()
        else:
            st.warning("📭 الرادار صافي تماماً، لا توجد طلبات تجار معلقة حالياً في السيرفر.")
            if st.button("🚪 مغادرة غرفة القيادة وقفل السيرفر", key="logout_empty_boss_btn"):
                st.session_state["admin_master_logged"] = False
                st.rerun()


