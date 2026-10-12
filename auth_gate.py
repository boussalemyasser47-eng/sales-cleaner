# ==========================================
# الجزء الأول: التهيئة، حظر السايدبار، وإعدادات الجلسة الثابتة
# ==========================================
import streamlit as st

st.set_page_config(page_title="بوابة السيادة الكبرى 2026", layout="centered", initial_sidebar_state="collapsed")

# حظر السايدبار نهائياً بالـ CSS وحقن طراز الكتلة الموسطة الشبحية والتأثير النيوني الأصفر المضيء
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    .block-container { background-color: #0d0d11; padding: 40px; border-radius: 16px; text-align: center; max-width: 500px; margin: auto; }
    h1, h2, p, label { color: #ffffff !important; font-family: 'Segoe UI', sans-serif; text-align: center; }
    .neon-glow {
        margin-top: 25px; padding: 15px; border: 2px dashed #ccff00; border-radius: 8px;
        background: rgba(204, 255, 0, 0.05); color: #ccff00; font-weight: bold;
        text-shadow: 0 0 10px #ccff00, 0 0 20px #ccff00; font-size: 16px; text-align: center;
    }
    div.stButton > button { width: 100%; background-color: #3a3af2; color: white; font-weight: bold; border-radius: 8px; }
    div.stButton > button:hover { background-color: #5050ff; color: white; }
    .stTextInput input { background-color: #15151e !important; color: white !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ==========================================
# الجزء الثاني: جدار الفحص الذكي للرابط العلوي والتحقق الشرطي
# ==========================================
query_params = st.query_params

if query_params.get("role") != "boss":
    st.error("404 Not Found - السيادة تمنع الوصول العام.")
    st.stop()

# محاكاة الاستجابة الذكية لـ PocketBase مع معالجة مصفوفة الـ API وتجنب ترك "in" فارغة
mock_pocketbase_response = {"items": [{"email": "new_merchant_2026@saas.com", "password": "FreePass9988!"}]}
response_items = mock_pocketbase_response.get("items", [])

# تأمين فحص السطر 72: التحقق من وجود عناصر بالمصفوفة قبل القراءة لمنع أخطاء التركيب
if len(response_items) > 0:
    target_merchant = response_items[0]
else:
    target_merchant = {"email": "no_merchant_found@saas.com", "password": "N/A"}

# ==========================================
# الجزء الثالث: صندوق تحقق الأدمن وقفل الهوية الموسط
# ==========================================
if not st.session_state.authenticated:
    st.subheader("لوحة الموافقات السيادية الـ 9")
    st.write("نظام الحماية والأمن المتكامل: admin_master_v4")
    
    # نموذج فحص الهوية بمنتصف الشاشة
    with st.form("identity_lock_form"):
        username = st.text_input("اسم الهوية الأعلى", autocomplete="off")
        password = st.text_input("كلمة السر المشفرة", type="password")
        submit_btn = st.form_submit_button("تفعيل القفل والولوج")
        
        if submit_btn:
            if username == "admin_master_v4" and password == "SaasPassword2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("بيانات الهوية غير صالحة للسيادة الكبرى!")

# ==========================================
# الجزء الرابع: الانبثاق النيوني المضيء وزر الحذف الميكانيكي المعزول
# ==========================================
else:
    # انبثاق بيانات التاجر بالأصفر النيوني المضيء المستقر تماماً ضد الـ Refresh
    st.markdown(f"""
        <div class="neon-glow">
            🚀 تم فك مصفوفة PocketBase والاستدعاء بنجاح!<br><br>
            البريد السيادي: {target_merchant['email']}<br>
            الرمز الحر: {target_merchant['password']}
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.write("⚙️ إدارة الحالات الميكانيكية المعزولة (مفعل، محظور، منتظر)")
    
    # حقن زر الحذف النهائي الميكانيكي المعزول بـ st.form لكل الحالات لمنع الخلط كلياً
    with st.form("mechanical_purge_form"):
        st.caption("سيقوم هذا الإجراء بتطهير السجلات وإلغاء استجابة الـ API فوراً")
        purge_confirmed = st.form_submit_button("💥 إطلاق أمر الحذف الميكانيكي النهائي")
        
        if purge_confirmed:
            st.success("💥 تم تدمير وتطهير مصفوفة البيانات بنجاح لجميع الحالات!")
            st.session_state.authenticated = False
