import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import io

# استدعاء الدوال من الملفات الفرعية المخصصة التي أنشأناها
from styles import apply_neon_theme
from pdf_helper import generate_invoice_pdf

# 🎨 تطبيق التنسيق والواجهة العريضة
st.set_page_config(page_title="نظام المبيعات الأسطوري المتكامل", layout="wide")
apply_neon_theme()

# 🏛️ ربط قاعدة البيانات وتجهيز الجداول
conne = sqlite3.connect("invoices_master_v3.db")
cursor = conne.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS v3_customer_invoices (
        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_name TEXT,
        customer_name TEXT,
        customer_phone TEXT,
        product_name TEXT,
        final_total REAL,
        month_created TEXT,
        date_created TEXT
    )
''')
conne.commit()

# --- القائمة الجانبية للتنقل بين الأدوات ---
st.sidebar.markdown("<h2 style='color: #00ffcc; text-align: center; text-shadow: 0 0 10px #00ffcc; font-size: 24px;'>🛠️ التحكم</h2>", unsafe_allow_html=True)
choice = st.sidebar.radio("اختر الأداة التي تريد استخدامها:", [
    "✨ صانع الفواتير الاحترافي (PDF)", 
    "🧼 مطهر ملفات المبيعات والرسوم البيانية"
])

# ========================================================
# الميزة الأولى: واجهة صانع الفواتير الفردية
# ========================================================
if choice == "✨ صانع الفواتير الاحترافي (PDF)":
    st.write("<h1 style='font-size: 32px;'>📄 صانع الفواتير الأسطوري مع الشعار ودعم العربية</h1>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("🏪 معلومات المتجر والزبون")
        shop_name = st.text_input("اسم متجرك الإلكتروني:", "DZ Cyber Store")
        customer_name = st.text_input("اسم الزبون الكامل:")
        customer_phone = st.text_input("رقم هاتف الزبون:")
        customer_address = st.text_input("عنوان التوصيل والولاية:")
        uploaded_logo = st.file_uploader("اختر لوغو متجرك لإضافته في الفاتورة (اختياري)", type=["png", "jpg", "jpeg"])

    with col_right:
        st.subheader("📦 تفاصيل السلعة والحسابات")
        product_name = st.text_input("اسم المنتج:")
        price = st.number_input("سعر القطعة (DA):", min_value=0, value=1200)
        quantity = st.number_input("الكمية:", min_value=1, value=1)
        shipping_cost = st.number_input("مصاريف الشحن (DA):", min_value=0, value=600)

    product_total = price * quantity
    final_total = product_total + shipping_cost
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_month = datetime.now().strftime("%Y-%m")

    st.markdown("---")
    if st.button("🚀 إصدار وحفظ الفاتورة الأسطورية"):
        if not customer_name or not product_name:
            st.error("❌ خطأ: يرجى ملء اسم الزبون والمنتج أولاً!")
        else:
            cursor.execute('''
                INSERT INTO v3_customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, month_created, date_created)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (shop_name, customer_name, customer_phone, product_name, final_total, current_month, current_date))
            conne.commit()
            st.success("💾 تم حفظ الفاتورة بنجاح في قاعدة البيانات المحدثة!")

            logo_data = uploaded_logo.read() if uploaded_logo is not None else None

            pdf_data = generate_invoice_pdf(
                shop_name, customer_name, customer_phone, customer_address,
                product_name, price, quantity, product_total, shipping_cost, final_total,
                current_date, logo_data
            )
            
            st.download_button(
                label="📥 تحميل الفاتورة الرقمية الأسطورية (PDF)",
                data=pdf_data,
                file_name=f"invoice_{customer_name}.pdf",
                mime="application/pdf"
            )

    st.markdown("---")
    st.subheader("🗄️ نظام أرشفة الفواتير المتقدم")
    months_df = pd.read_sql("SELECT DISTINCT month_created FROM v3_customer_invoices ORDER BY month_created DESC", conne)
    if not months_df.empty:
        filter_month = st.selectbox("🎯 اختر الشهر لفرز وحساب المبيعات الخاصة به:", months_df['month_created'])
        filtered_invoices = pd.read_sql(f"SELECT * FROM v3_customer_invoices WHERE month_created = '{filter_month}' ORDER BY invoice_id DESC", conne)
        st.dataframe(filtered_invoices, use_container_width=True)
        st.metric(label=f"📊 صافي أرباح شهر ({filter_month}) فقط:", value=f"{filtered_invoices['final_total'].sum():,.2f} DA")

# ========================================================
# الميزة الثانية: مطهر ملفات المبيعات والرسوم البيانية المضيئة
# ========================================================
elif choice == "🧼 مطهر ملفات المبيعات والرسوم البيانية":
    st.write("<h1 style='font-size: 32px;'>🧼 نظام تطهير ملفات المبيعات الجماعية (Excel & CSV)</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر ملف المبيعات الجماعي لمتجرك (صيغة CSV أو Excel)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.subheader("📋 الملف المرفوع قبل الفحص:")
        st.dataframe(df.head())
        
        if 'item_price' in df.columns:
            df['item_price'] = df['item_price'].astype(str).str.replace(' DA', '').astype(float)
        
        duplicated_rows = df[df.duplicated(subset=['product_name'], keep='first')].copy()
        df.drop_duplicates(subset=['product_name'], keep='first', inplace=True)
        
        bad_prices = df[df['item_price'] <= 0].copy()
        df = df[df['item_price'] > 0]
        
        if 'sale_date' in df.columns:
            df['sale_date'] = pd.to_datetime(df['sale_date'], dayfirst=True, format='mixed', errors='coerce')
            df.dropna(subset=['sale_date'], inplace=True)
        
        # حساب الأرباح وضمان الحفظ قبل العرض لضمان سلامة الجدول
        df['total_row_sales'] = df['item_price'] * df['quantity_sold']
        if not duplicated_rows.empty and 'item_price' in duplicated_rows.columns:
             duplicated_rows['total_row_sales'] = duplicated_rows['item_price'] * duplicated_rows['quantity_sold']
            
        st.success("✅ تم تنظيف الداتا وتجهيز المخططات المضيئة للمتجر!")
        
        st.subheader("💎 جدول البيانات النظيف تماماً والمصفى:")
        st.dataframe(df, use_container_width=True)
        
        col_clean, col_trash = st.columns(2)
        with col_clean:
            st.subheader("📊 إجمالي المبيعات الصافية بعد الفحص:")
            st.metric(label="صافي الأرباح الحقيقية المتوقعة", value=f"{df['total_row_sales'].sum():,.2f} DA")
        with col_trash:
            st.subheader("⚠️ التكرارات والأخطاء المحذوفة:")
            if not duplicated_rows.empty or not bad_prices.empty:
                if not duplicated_rows.empty:
                    st.warning(f"تم عزل وحذف {len(duplicated_rows)} سطر مكرر لحمايتك!")
                    st.dataframe(duplicated_rows)
                if not bad_prices.empty:
                    st.error(f"تم حذف {len(bad_prices)} سطر أسعار سالبة!")
                    st.dataframe(bad_prices)
            else:
                st.info("الملف سليم تماماً ولا يحتوي على تكرارات.")
                
        # الرسوم البيانية النيون الملونة
        st.subheader("📈 المخططات البيانية الملونة للمبيعات:")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.write("💰 حجم المبيعات الإجمالي الحقيقي لكل منتج (باللون الأخضر الفسفوري المشع):")
            st.bar_chart(data=df, x='product_name', y='total_row_sales', color='#00ffcc')
        with chart_col2:
            st.write("📦 مجموع الكميات المستلمة والمباعة (باللون البنفسجي الليزري):")
            st.bar_chart(data=df, x='product_name', y='quantity_sold', color='#ff007f')
            
        csv_buffer = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 تحميل تقرير المبيعات المطهّر بالكامل",
            data=csv_buffer,
            file_name="cleaned_neon_sales.csv",
            mime="text/csv"
        )

conne.close()

