import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import io

# مكتبات معالجة وتصحيح الكتابة العربية في ملفات الـ PDF
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 🎨 إعدادات واجهة الموقع لتكون عريضة واحترافية
st.set_page_config(page_title="نظام المبيعات الأسطوري المتكامل", layout="wide")

# 🖌️ الألوان السيبرانية الأسطورية المضيئة (Neon Cyberpunk)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    h1 {
        color: #00ffcc !important;
        font-family: 'Cairo', sans-serif;
        text-align: center;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
        font-weight: bold;
    }
    h2, h3 {
        color: #ff007f !important;
        text-shadow: 0 0 5px rgba(255, 0, 127, 0.5);
    }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #ff007f, #7f00ff);
        color: white; border-radius: 12px; border: none;
        padding: 12px 30px; font-size: 18px; font-weight: bold;
        box-shadow: 0 0 15px #ff007f; transition: 0.4s; width: 100%;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(45deg, #00ffcc, #007fff);
        box-shadow: 0 0 25px #00ffcc; color: #0d1117;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #161b22 !important; color: #ffffff !important;
        border: 2px solid #30363d !important; border-radius: 8px;
    }
    p, label, th, td { color: #c9d1d9 !important; }
    </style>
    """, unsafe_allow_html=True)

# 🏛️ ربط قاعدة البيانات المشتركة وتجهيز الجداول
conne = sqlite3.connect("invoices_master.db")
cursor = conne.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_invoices (
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

# دالة لتصحيح النصوص العربية لكي تظهر صحيحة وموصولة في جداول الـ PDF
def fix_arabic(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

# --- القائمة الجانبية للتنقل بين الأدوات ---
st.sidebar.markdown("<h2 style='color: #00ffcc; text-align: center; text-shadow: 0 0 10px #00ffcc;'>🛠️ التحكم</h2>", unsafe_allow_html=True)
choice = st.sidebar.radio("اختر الأداة التي تريد استخدامها:", [
    "✨ صانع الفواتير العربي (PDF)", 
    "🧼 مطهر ملفات المبيعات والرسوم البيانية"
])

# ========================================================
# الميزة الأولى: صانع الفواتير العربي وتوليد الـ PDF وفلاتر الداتا
# ========================================================
if choice == "✨ صانع الفواتير العربي (PDF)":
    st.write("<h1 style='font-size: 32px;'>📄 صانع الفواتير الأسطوري بدعم كامل للعربية</h1>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("🏪 معلومات المتجر والزبون")
        shop_name = st.text_input("اسم متجرك الإلكتروني:", "DZ Cyber Store")
        customer_name = st.text_input("اسم الزبون الكامل (عربي أو إنجليزي):")
        customer_phone = st.text_input("رقم هاتف الزبون:")
        customer_address = st.text_input("عنوان التوصيل والولاية:")

    with col_right:
        st.subheader("📦 تفاصيل السلعة والحسابات")
        product_name = st.text_input("اسم المنتج:")
        price = st.number_input("سعر القطعة (DA):", min_value=0, value=1200)
        quantity = st.number_input("الكمية:", min_value=1, value=1)
        shipping_cost = st.number_input("مصاريف الشحن (DA):", min_value=0, value=600)

    product_total = price * quantity
    final_total = product_total + shipping_cost
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_month = datetime.now().strftime("%Y-%m") # فلتر الشهر لقاعدة البيانات

    st.markdown("---")
    if st.button("🚀 إصدار وحفظ الفاتورة الأسطورية"):
        if not customer_name or not product_name:
            st.error("❌ خطأ: يرجى ملء اسم الزبون والمنتج أولاً!")
        else:
            # 1. حفظ في قاعدة البيانات مع دعم فلتر الشهر
            cursor.execute('''
                INSERT INTO customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, month_created, date_created)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (shop_name, customer_name, customer_phone, product_name, final_total, current_month, current_date))
            conne.commit()
            st.success("💾 تم حفظ الفاتورة بنجاح في نظام الأرشفة الأسطوري!")

            # 2. توليد ملف PDF متطور يدعم الكلمات والحسابات
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer)
            p.drawString(100, 800, f"INVOICE - {shop_name.upper()}")
            p.drawString(100, 780, "=========================================")
            p.drawString(100, 750, f"Date: {current_date}")
            p.drawString(100, 730, f"Customer: {customer_name}")
            p.drawString(100, 710, f"Phone: {customer_phone}")
            p.drawString(100, 690, f"Address: {customer_address}")
            p.drawString(100, 660, "-----------------------------------------")
            p.drawString(100, 640, f"Product: {product_name}")
            p.drawString(100, 620, f"Price: {price:,} DA x Qty: {quantity}")
            p.drawString(100, 600, f"Subtotal: {product_total:,} DA")
            p.drawString(100, 580, f"Shipping: {shipping_cost:,} DA")
            p.drawString(100, 550, "-----------------------------------------")
            p.drawString(100, 520, f"TOTAL TO PAY: {final_total:,} DA")
            p.showPage()
            p.save()
            
            st.download_button(
                label="📥 تحميل الفاتورة الرقمية الحالية (PDF)",
                data=buffer.getvalue(),
                file_name=f"invoice_{customer_name}.pdf",
                mime="application/pdf"
            )

    # 🗄️ نظام الفلاتر الذكي لاستعلامات قاعدة البيانات شهرياً
    st.markdown("---")
    st.subheader("🗄️ نظام أرشفة الفواتير المتقدم")
    
    # جلب قائمة الأشهر المتوفرة لتصفية البيانات بناءً عليها
    months_df = pd.read_sql("SELECT DISTINCT month_created FROM customer_invoices ORDER BY month_created DESC", conne)
    
    if not months_df.empty:
        filter_month = st.selectbox("🎯 اختر الشهر لفرز وحساب المبيعات الخاصة به:", months_df['month_created'])
        
        # استعلام مخصص للفلتر المختار
        filtered_invoices = pd.read_sql(f"SELECT * FROM customer_invoices WHERE month_created = '{filter_month}' ORDER BY invoice_id DESC", conne)
        
        st.dataframe(filtered_invoices, use_container_width=True)
        st.metric(label=f"📊 صافي أرباح شهر ({filter_month}) فقط:", value=f"{filtered_invoices['final_total'].sum():,.2f} DA")
    else:
        st.info("الأرشيف خالي تماماً حالياً.")

# ========================================================
# الميزة الثانية: مطهر ملفات المبيعات والرسوم البيانية النيون المضيئة
# ========================================================
elif choice == "🧼 مطهر ملفات المبيعات والرسوم البيانية":
    st.write("<h1 style='font-size: 32px;'>🧼 نظام التطهير والإحصائيات البصرية النيون</h1>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("اختر ملف المبيعات الجماعي لمتجرك (صيغة CSV)", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.subheader("📋 الملف المرفوع قبل الفحص:")
        st.dataframe(df.head())
        
        if 'item_price' in df.columns:
            df['item_price'] = df['item_price'].astype(str).str.replace(' DA', '').astype(float)
        
        # حذف التكرار وتصحيح القيم
        duplicated_rows = df[df.duplicated(subset=['product_name'], keep='first')]
        df.drop_duplicates(subset=['product_name'], keep='first', inplace=True)
        
        bad_prices = df[df['item_price'] <= 0]
        df = df[df['item_price'] > 0]
        
        if 'sale_date' in df.columns:
            df['sale_date'] = pd.to_datetime(df['sale_date'], dayfirst=True, format='mixed', errors='coerce')
            df.dropna(subset=['sale_date'], inplace=True)
            
        st.success("✅ تم تنظيف الداتا وتجهيز المخططات المضيئة للمتجر!")
        
        # 📈 قسم الرسوم البيانية المضيئة الجديد (Neon Charts)
        st.subheader("📈 المخططات البيانية الملونة للمبيعات:")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.write("💰 حجم المبيعات الإجمالي الحقيقي لكل منتج:")
            df['total_row_sales'] = df['item_price'] * df['quantity_sold']
            st.bar_chart(data=df, x='product_name', y='total_row_sales')
            
        with chart_col2:
            st.write("📦 مجموع الكميات المستلمة والمباعة:")
            st.bar_chart(data=df, x='product_name', y='quantity_sold')
            
        # تحميل الملف النظيف
        csv_buffer = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 تحميل تقرير المبيعات المطهّر بالكامل",
            data=csv_buffer,
            file_name="cleaned_neon_sales.csv",
            mime="text/csv"
        )

conne.close()

