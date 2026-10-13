# ========================================================
# الجزء الأول: الهندسة البصرية المتقدمة وتلوين الواجهات الأسطوري (auth_gate.py)
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

# تفعيل علم وميض الخطأ السيبراني الأحمر في الجلسة في حال الفشل
if "cyber_lockout_aura" not in st.session_state:
    st.session_state["cyber_lockout_aura"] = False

# تهيئة ألوان وصور الحركة النيونية المعزولة ميكانيكياً خارج النص
box_border_color = "#ff0055" if st.session_state["cyber_lockout_aura"] else "#00fff0"
box_shadow_glow = "0px 0px 45px rgba(255, 0, 85, 0.65), inset 0px 0px 20px rgba(255, 0, 85, 0.2)" if st.session_state["cyber_lockout_aura"] else "0px 0px 40px rgba(0, 255, 240, 0.4), inset 0px 0px 20px rgba(0, 255, 240, 0.15)"
animation_trigger = "animation: cyberPulseAlert 1.5s infinite !important;" if st.session_state["cyber_lockout_aura"] else ""

# 🛡️ تم إزالة حرف الـ f هنا وجعل النص صافي ومضاعفة الأقواس أصبحت غير مطلوبة لمنع الأخطاء نهائياً
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com" rel="stylesheet">
    
    <style>
    @keyframes pulseBackground {
        0% { background: radial-gradient(circle at 50% 40%, #0f0f2d 0%, #030307 100%); }
        50% { background: radial-gradient(circle at 50% 45%, #08081a 0%, #010103 100%); }
        100% { background: radial-gradient(circle at 50% 40%, #0f0f2d 0%, #030307 100%); }
    }
    @keyframes cyberPulseAlert {
        0% { box-shadow: 0px 0px 20px rgba(255, 0, 85, 0.4); border-color: #ff0055; }
        50% { box-shadow: 0px 0px 45px rgba(255, 0, 85, 0.8); border-color: #ff3377; }
        100% { box-shadow: 0px 0px 20px rgba(255, 0, 85, 0.4); border-color: #ff0055; }
    }

    .stApp {
        animation: pulseBackground 8s ease-in-out infinite !important;
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* ترقية البطاقات الزجاجية الملونة بالتأثير البلوري والظلال المشعة */
    .premium-card-pink {
        background: linear-gradient(135deg, rgba(34, 4, 46, 0.6) 0%, rgba(15, 2, 20, 0.9) 100%) !important;
        border: 2px solid #ff00ff !important; border-radius: 20px !important; padding: 30px !important; box-shadow: 0px 0px 35px rgba(255, 0, 255, 0.25) !important; direction: rtl; text-align: right; margin-bottom: 25px; backdrop-filter: blur(15px);
    }
    .premium-card-cyan {
        background: linear-gradient(135deg, rgba(4, 32, 43, 0.6) 0%, rgba(2, 14, 20, 0.9) 100%) !important;
        border: 2px solid #00fff0 !important; border-radius: 20px !important; padding: 30px !important; box-shadow: 0px 0px 35px rgba(0, 255, 240, 0.25) !important; direction: rtl; text-align: right; margin-bottom: 25px; backdrop-filter: blur(15px);
    }
    
    div[data-testid="stVerticalBlock"] button, div.stButton button, .stButton > button {
        width: 100% !important; min-height: 48px !important; white-space: normal !important; word-wrap: break-word !important;
        font-family: 'Cairo', sans-serif !important; font-size: 13.5px !important; font-weight: 900 !important; border-radius: 12px !important;
        text-align: center !important; display: inline-flex !important; align-items: center !important; justify-content: center !important;
        padding: 10px 14px !important; background: linear-gradient(135deg, #0d0d21 0%, #05050c 100%) !important; color: #00fff0 !important;
        border: 2px solid #00fff0 !important; box-shadow: 0px 0px 14px rgba(0, 255, 240, 0.25) !important; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    div.stButton button:hover { background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important; color: #000000 !important; box-shadow: 0px 0px 25px #00fff0 !important; transform: translateY(-2px) !important; }
    
    div[data-testid="stTextInput"] input { border: 2px solid #ff00ff !important; background-color: #06060d !important; color: #ffffff !important; border-radius: 14px !important; padding: 15px 18px !important; font-family: 'Cairo', sans-serif !important; font-size: 14.5px !important; box-shadow: 0px 0px 10px rgba(255, 0, 255, 0.1) !important; }
    div[data-testid="stTextInput"] input:focus { border-color: #00fff0 !important; box-shadow: 0px 0px 20px rgba(0, 255, 240, 0.4) !important; }
    
    [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] { display: none !important; visibility: hidden !important; opacity: 0 !important; height: 0px !important; width: 0px !important; }
    section[data-testid="stSidebar"] { display: none !important; visibility: hidden !important; }
    
    .stWidgetFormLabel, p, span, label, h1, h2, h3, h4 { font-family: 'Cairo', sans-serif !important; color: #ffffff !important; text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.1) !important; }
    </style>
""", unsafe_allow_html=True)

# 🧠 حقن الجزء الشرطي المعزول الخاص بغرفة المالك بشكل منفصل تماماً ومحمي لمنع انهيار الـ f-string
st.markdown(f"""
    <style>
    .centered-box-container {{
        max-width: 500px !important;
        margin: 60px auto 20px auto !important;
        padding: 40px !important;
        background: rgba(5, 5, 15, 0.93) !important;
        border: 2px solid {box_border_color} !important;
        border-radius: 20px !important;
        box-shadow: {box_shadow_glow} !important;
        direction: rtl !important;
        text-align: right !important;
        backdrop-filter: blur(15px) !important;
        {animation_trigger}
    }}
    </style>
""", unsafe_allow_html=True)

# ========================================================
# الجزء الثاني: حقول مدخلات التجار وبناء جدول الـ SQL الموحد (auth_gate.py)
# ========================================================
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

# [إصلاح حاسم للثغرة الذكية]: منع حقن الحساب الافتراضي تلقائياً في الكاش إذا قام المالك بحذفه
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_cursor = db_conn.cursor()
db_cursor.execute("SELECT COUNT(*) FROM saas_users_auth WHERE email = 'daymaabdaalhmdllh@gmail.com'")
account_exists = db_cursor.fetchone()[0]

if account_exists == 0 and "destroyed_flag" not in st.session_state:
    db_cursor.execute("INSERT OR IGNORE INTO saas_users_auth VALUES ('daymaabdaalhmdllh@gmail.com', '123456', '🟢 مفعّل ونشط', 'الباقة السيبرانية الخارقة')")
    db_conn.commit()
db_conn.close()

# ⚙️ دالة التدمير الفوري لأي حساب في قاعدة البيانات
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
                    cursor_reg.execute("INSERT OR IGNORE INTO saas_users_auth VALUES (?, ?, '⏳ في انتظار التفعيل', ?)", (clean_email, clean_pass, user_package_choice))
                    conn_reg.commit()
                    conn_reg.close()
                    st.success("🎯 تم إرسال طلبك بنجاح! سيظهر الآن في رادار الإدارة فوراً.")
                    time.sleep(0.5)
                    st.rerun()
        else:
            st.markdown("</div>", unsafe_allow_html=True)
            if st.button("🔑 تسجيل الدخول إلى المتجر"):
                if clean_email == "" or clean_pass == "": st.error("⚠️ يرجى إدخال البريد وكلمة السر!")
                else:
                    conn_login = sqlite3.connect("saas_security_vault.db", timeout=10)
                    cursor_login = conn_login.cursor()
                    cursor_login.execute("SELECT status FROM saas_users_auth WHERE email = ? AND password = ?", (clean_email, clean_pass))
                    user_status = cursor_login.fetchone()
                    conn_login.close()
                    if user_status: st.success(f"🔓 تم التحقق بنجاح! حالة حسابك الحالية هي: {user_status[0]}")
                    else: st.error("❌ بيانات الدخول غير مطابقة لملف الأمان السحابي.")
                # 2️⃣ [تكملة مصفوفة التحكم الخماسية المدمجة]: توزيع بقية الأعمدة التفاعلية حياً
                with col_2:
                    if st.button("⏳ تمديد 7 أيام", key=f"btn_ext_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🟡 تم تمديد فترة التجربة 7 أيام' WHERE email = ?", (current_email,))
                        conn.commit()
                        conn.close()
                        st.toast("⏳ تم منح المشترك مهلة إضافية!", icon="⏱️")
                        time.sleep(0.5)
                        st.rerun()
                
                with col_3: # الحذف والتدمير الفوري في المنتصف تماماً لسيادة لوحة التحكم
                    if st.button("🗑️ تدمير نهائي", key=f"btn_del_{current_email}"):
                        st.session_state[f"ask_confirm_{current_email}"] = True
                
                with col_4:
                    if st.button("💸 ترقية الباقة", key=f"btn_upg_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET package = 'الباقة السيبرانية الخارقة (65k)' WHERE email = ?", (current_email,))
                        conn.commit()
                        conn.close()
                        st.toast("💸 تم ترقية حساب التاجر للباقة القصوى!", icon="🚀")
                        time.sleep(0.5)
                        st.rerun()
                
                with col_5:
                    if st.button("🔒 حظر وقفل", key=f"btn_lck_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🔴 تم قفل ومصادرة الصلاحيات' WHERE email = ?", (current_email,))
                        conn.commit()
                        conn.close()
                        st.toast("🔒 تم مصادرة الصلاحيات عن بعد!", icon="⚠️")
                        time.sleep(0.5)
                        st.rerun()
                
                # إغلاق حاوية الـ HTML للبطاقة النيونية لضمان حبس الأزرار الخمسة بالداخل 100%
                st.markdown("</div>", unsafe_allow_html=True)
                
                # صندوق التأكيد التفاعلي الصارم "فهمت" لحذف البريد ومنع ثغرة الـ INSERT الافتراضية
                if st.session_state.get(f"ask_confirm_{current_email}", False):
                    st.markdown("<hr style='border-color: rgba(255, 0, 0, 0.3); margin: 10px 0;'>", unsafe_allow_html=True)
                    col_txt, col_yes_btn = st.columns(2)
                    with col_txt:
                        st.error(f"⚠️ هل أنت متأكد تماماً من إبادة وحذف حساب {current_email} نهائياً؟")
                    with col_yes_btn:
                        if st.button("✅ فهمت، احذف الآن", key=f"final_yes_{current_email}"):
                            st.session_state["destroyed_flag"] = True
                            st.session_state[f"ask_confirm_{current_email}"] = False
                            if delete_email_completely(current_email):
                                st.toast("🔥 تم تطهير الحساب بنجاح من خادم المنصة!", icon="💥")
                                time.sleep(0.5)
                                st.rerun()
            
            # زر الخروج الآمن الموحد في نهاية الصفحة لإغلاق الجلسة واللوحة كلياً لحماية الأمان السحابي
            st.markdown("<br><hr style='border-color: rgba(255, 0, 0, 0.2); margin: 20px 0;'>", unsafe_allow_html=True)
            if st.button("🚪 مغادرة غرفة القيادة وقفل السيرفر الموسط والخزائن", key="logout_boss_panel_btn"):
                st.session_state["admin_master_logged"] = False
                st.toast("🔒 تم الخروج وتأمين السيرفر كلياً.", icon="🛡️")
                time.sleep(0.5)
                st.rerun()
            else:
             st.warning("📭 الرادار صافي تماماً، لا توجد طلبات تجار معلقة حالياً في السيرفر.")
             if st.button("🚪 مغادرة غرفة القيادة وقفل السيرفر", key="logout_empty_boss_btn"):
                st.session_state["admin_master_logged"] = False
                st.rerun()


