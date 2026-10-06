import pandas as pd
import streamlit as st
import sqlite3
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="محلل مبيعات المتاجر الذكي", layout="wide")

st.title("📊 نظام فحص وتطهير بيانات المبيعات الذكي")
st.write("قم برفع ملف مبيعاتك للكشف عن الثغرات وحساب الأرباح الصافية الحقيقية.")

# 📂 ميزة رفع الملفات من طرف المستخدم
uploaded_file = st.file_uploader("اختر ملف المبيعات (صيغة CSV حالياً)", type=["csv"])

if uploaded_file is not None:
    # قراءة الملف المرفوع
    df = pd.read_csv(uploaded_file)
    
    st.subheader("📋 البيانات المستلمة (قبل التنظيف)")
    st.dataframe(df.head())
    
    # حساب الإيرادات قبل الفحص للمقارنة
    total_raw = 0
    if 'item_price' in df.columns and 'quantity_sold' in df.columns:
        try:
            temp_price = df['item_price'].astype(str).str.replace(' DA', '').astype(float)
            total_raw = (temp_price * df['quantity_sold']).sum()
        except:
            total_raw = 0

    # 🛠️ عمليات التطهير الذكي للبيانات
    conne = sqlite3.connect("electronics_shop.db")
    
    # 1. تنظيف عمود السعر وتحويله لأرقام
    if 'item_price' in df.columns:
        df['item_price'] = df['item_price'].astype(str).str.replace(' DA', '').astype(float)
    
    # 2. عزل وفحص الأخطاء (الأسعار السالبة) لإظهارها للتاجر
    bad_rows = df[df['item_price'] <= 0]
    df = df[df['item_price'] > 0]
    
    # 3. توحيد صيغ التواريخ وحذف الأسطر التالفة
    if 'sale_date' in df.columns:
        df['sale_date'] = pd.to_datetime(df['sale_date'], dayfirst=True, format='mixed', errors='coerce')
        df.dropna(subset=['sale_date'], inplace=True)
    
    # حفظ وتخزين البيانات النظيفة في قاعدة بيانات SQLite
    df.to_sql("cleaned_sales", conne, if_exists="replace", index=False)
    
    # قراءة البيانات النظيفة للعرض
    ddf = pd.read_sql("SELECT * FROM cleaned_sales", conne)
    
    # 🟢 عرض النتائج بعد التنظيف
    st.success("✅ تم فحص وتطهير البيانات بنجاح وتخزينها في قاعدة البيانات!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💎 البيانات المطهّرة والجاهزة للحساب:")
        st.dataframe(ddf)
    
    with col2:
        st.subheader("⚠️ الأخطاء المكتشفة والمحذوفة:")
        if not bad_rows.empty:
            st.warning(f"تم اكتشاف {len(bad_rows)} سطر يحتوي على أسعار سالبة أو أخطاء إدخال!")
            st.dataframe(bad_rows)
        else:
            st.info("لا توجد أسعار سالبة في هذا الملف.")

    # 💰 حساب الإجمالي بضغطة زر
    if st.button("حساب إجمالي المبيعات الصافية"):
        total_sales = (ddf['item_price'] * ddf['quantity_sold']).sum()
        
        # عرض مقارنة مالية ذكية تبهر العميل
        st.metric(label="إجمالي المبيعات الحقيقية الصافية", value=f"{total_sales:,.2f} DA")
        if total_raw > total_sales:
            diff = total_raw - total_sales
            st.error(f"⚠️ انتبه: كان هناك أخطاء بقيمة {diff:,.2f} DA في ملفك الأصلي تم تصحيحها لحمايتك من الخسارة!")

    conne.close()
else:
    st.info("💡 في انتظار رفع ملف CSV لبدء الفحص الحقيقي...")
