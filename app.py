import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from fpdf import FPDF
import io

st.set_page_config(page_title="صانع الفواتير المحترف", layout="wide")

# 🏛️ ربط قاعدة البيانات لحفظ الفواتير
conne = sqlite3.connect("invoices_data.db")
cursor = conne.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_invoices (
        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_name TEXT,
        customer_name TEXT,
        customer_phone TEXT,
        product_name TEXT,
        final_total REAL,
        date_created TEXT
    )
''')
conne.commit()

st.title("📄 صانع الفواتير الرقمية الذكي وتوليد ملفات PDF 🇩🇿")
st.write("اصنع فاتورتك، احفظها في قاعدة البيانات، وحمّلها كملف PDF احترافي لزبونك!")

# واجهة إدخال البيانات
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏪 معلومات المتجر والزبون")
    shop_name = st.text_input("اسم متجرك الإلكتروني:", "DZ Store")
    customer_name = st.text_input("اسم الزبون الكامل:")
    customer_phone = st.text_input("رقم هاتف الزبون:")
    customer_address = st.text_input("عنوان التوصيل والولاية:")

with col_right:
    st.subheader("📦 تفاصيل السلعة والحسابات")
    product_name = st.text_input("اسم المنتج:")
    price = st.number_input("سعر القطعة (DA):", min_value=0, value=1200)
    quantity = st.number_input("الكمية:", min_value=1, value=1)
    shipping_cost = st.number_input("مصاريف الشحن (DA):", min_value=0, value=600)

# عمليات الحساب الرياضية
product_total = price * quantity
final_total = product_total + shipping_cost
current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

st.markdown("---")

if st.button("🚀 إصدار وحفظ الفاتورة الحالية"):
    if not customer_name or not product_name:
        st.error("❌ خطأ: يرجى ملء اسم الزبون والمنتج أولاً!")
    else:
        # 1. حفظ البيانات في SQLite3
        cursor.execute('''
            INSERT INTO customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, date_created)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (shop_name, customer_name, customer_phone, product_name, final_total, current_date))
        conne.commit()
        st.success("💾 تم حفظ الفاتورة بنجاح في قاعدة بيانات المتجر!")

        # 2. بناء وتوليد ملف PDF احترافي في الذاكرة
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        
        # تصميم الفاتورة
        pdf.cell(200, 10, txt=f"INVOICE - {shop_name.upper()}", ln=True, align='C')
        pdf.cell(200, 10, txt="=========================================", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Date: {current_date}", ln=True)
        pdf.cell(200, 10, txt=f"Customer Name: {customer_name}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {customer_phone}", ln=True)
        pdf.cell(200, 10, txt=f"Address: {customer_address}", ln=True)
        pdf.cell(200, 10, txt="-----------------------------------------", ln=True)
        pdf.cell(200, 10, txt=f"Product: {product_name}", ln=True)
        pdf.cell(200, 10, txt=f"Price: {price:,} DA  x  Qty: {quantity}", ln=True)
        pdf.cell(200, 10, txt=f"Subtotal: {product_total:,} DA", ln=True)
        pdf.cell(200, 10, txt=f"Shipping Cost: {shipping_cost:,} DA", ln=True)
        pdf.cell(200, 10, txt="-----------------------------------------", ln=True)
        pdf.set_font("Helvetica", style='B', size=14)
        pdf.cell(200, 10, txt=f"TOTAL TO PAY: {final_total:,} DA", ln=True)
        
        # تحويل الـ PDF إلى بايتس ليتم تحميله بـ Streamlit
        pdf_output = pdf.output()
        
        # زر تحميل ملف الـ PDF للتاجر
        st.download_button(
            label="📥 تحميل الفاتورة بصيغة PDF لـ إرسالها للزبون",
            data=bytes(pdf_output),
            file_name=f"invoice_{customer_name}.pdf",
            mime="application/pdf"
        )

# 📊 قسم عرض الفواتير السابقة للتاجر لمراقبة مبيعاته
st.markdown("---")
st.subheader("📋 أرشيف الفواتير المحفوظة في متجرك:")
all_invoices = pd.read_sql("SELECT * FROM customer_invoices ORDER BY invoice_id DESC", conne)

if not all_invoices.empty:
    st.dataframe(all_invoices, use_container_width=True)
    st.metric(label="📊 إجمالي المداخيل المسجلة بالفواتير", value=f"{all_invoices['final_total'].sum():,.2f} DA")
else:
    st.info("لا توجد فواتير محفوظة في الأرشيف حتى الآن.")

conne.close()

