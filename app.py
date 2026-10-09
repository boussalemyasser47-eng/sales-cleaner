# =========================================================
# الجزء الثاني: الهوية البصرية، العناوين، ورفع الملفات
# =========================================================

# تصميم مخصص متوافق مع الواجهة البرمجية للموقع
st.markdown("""
    <style>
    .main-title { font-family: 'Cairo', sans-serif; text-align: center; color: #00fff0; padding-bottom: 20px; }
    .stButton>button { background-color: #00fff0; color: #10101a; font-weight: bold; border-radius: 8px; width: 100%; }
    .stSuccess { background-color: #161625; border: 1px solid #00fff0; color: #ffffff; }
    </style>
""", unsafe_allow_index=True)

st.markdown("<h1 class='main-title'>📊 لوحة تحكم مبيعات متجر تجار 📊</h1>", unsafe_allow_index=True)

# أداة رفع ملفات المبيعات الإلكترونية للمدير محمد
uploaded_file = st.file_uploader("📂 ارفع ملف مبيعات المتجر الحالي لفحصه وتطهيره", type=["csv", "xlsx"])

# منطق التحقق والتبديل بين الملف المرفوع والبيانات الافتراضية الكلية
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    st.info("💡 يتم عرض البيانات الافتراضية الكاملة للمتجر الآن. يمكنك رفع ملفك الخاص لتطهيره.")
# =========================================================
# الجزء الثالث: خوارزمية التطهير، الاتصال بـ SQLite3، والحساب
# =========================================================

st.subheader("⚙️ حالة البيانات الحالية في النظام")

# صندوق فحص لإظهار الجدول الأولي قبل الفلترة والتنظيف
show_raw = st.checkbox("عرض البيانات الأصلية الكاملة قبل معالجة الأخطاء")
if show_raw:
    st.write("📋 البيانات الخام غير المصفاة:")
    st.dataframe(df)

# تطبيق معايير التطهير الخاصة بالمتجر:
# 1. التخلص من تكرار المنتجات غير المبرر لضبط الحسابات
df.drop_duplicates('product_name', inplace=True)

# 2. إصلاح ومعالجة التواريخ المخلطة ورفض التواريخ الفارغة (None)
df['sale_date'] = pd.to_datetime(df['sale_date'], dayfirst=True, format='mixed', errors='coerce')
df.dropna(subset=['sale_date'], inplace=True)

# 3. تطهير قيم الأسعار وتحويلها إلى أرقام عشرية صحيحة حقيقية
if df['item_price'].dtype == 'object':
    df['item_price'] = df['item_price'].str.replace(' DA', '').str.replace(',', '').astype(float)
else:
    df['item_price'] = df['item_price'].astype(float)

# تصفية واستبعاد الأسعار السالبة الناتجة عن أخطاء الإدخال بالمتجر لضمان ربح حقيقي
df = df[df['item_price'] > 0]

# تخزين السجلات المصفاة داخل جدول الـ SQL
df.to_sql("electronics_shop", conne, if_exists="replace", index=False)

# استدعاء البيانات المطهرة والآمنة ماليًا من قاعدة البيانات لعرضها للمدير محمد
ddf = pd.read_sql("SELECT * FROM electronics_shop", conne)

st.write("✨ جدول المبيعات المطهر والآمن ماليًا داخل قاعدة البيانات:")
st.dataframe(ddf, use_container_width=True)

# زر المعالجة وحساب صافي الأرباح والإجمالي الكلي
if st.button("Calculate Total Sales | حساب إجمالي المبيعات"):
    ddff = (ddf['item_price'] * ddf['quantity_sold']).sum()
    st.success(f"📊 إجمالي المبيعات الحقيقي للمتجر بعد التطهير: {ddff:,.2f} DA")
    st.balloons()
