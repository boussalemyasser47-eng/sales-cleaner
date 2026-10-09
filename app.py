# ========================================================
# الجزء الأول: المكتبات، قواعد البيانات المتقدمة والقائمة الجانبية (v4)
# ========================================================
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import io
import urllib.parse

# استدعاء الدوال من الملفات الفرعية المخصصة الثابتة والموجودة في مشروعك
from styles import apply_neon_theme
from pdf_helper import generate_invoice_pdf, generate_thermal_label_pdf
from cleaner_helper import process_sales_file
from ai_helper import render_marketing_hub, render_data_insights, render_sidebar_helper

# تطبيق التنسيق والواجهة العريضة وحقن الألوان السيبرانية
st.set_page_config(page_title="نظام المبيعات والمخزون الأسطوري", layout="wide")
apply_neon_theme()

# الاتصال بالإصدار المطور الرابع من قاعدة البيانات Master
conne = sqlite3.connect("invoices_master_v4.db")
cursor = conne.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS v4_customer_invoices (
        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_name TEXT, customer_name TEXT, customer_phone TEXT,
        product_name TEXT, final_total REAL, month_created TEXT, date_created TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS store_stock (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT UNIQUE, available_qty INTEGER
    )
''')
conne.commit()

# --- القائمة الجانبية للتنقل بين الأدوات الذكية للمتجر ---
st.sidebar.markdown("<h2 style='color: #00ffcc; text-align: center; font-size: 24px;'>🛠️ التحكم</h2>", unsafe_allow_html=True)
choice = st.sidebar.radio("اختر الأداة التي تريد استخدامها:", [
    "✨ صانع الفواتير الاحترافي (PDF)", 
    "📦 إدارة وتنبيهات المخزون السلعي",
    "🧼 مطهر ملفات المبيعات وإحصائيات الولايات",
    "🚀 مولّد الحملات والتخطيط التسويقي (AI)"
])

# 🤖 تشغيل الميزة الثالثة: بوت خدمة العملاء والمساعد الفوري في الجنب
render_sidebar_helper()
# ========================================================
# الجزء الثاني: منطق واجهة إصدار الفواتير والملصقات الذكية
# ========================================================

if choice == "✨ صانع الفواتير الاحترافي (PDF)":
    st.write("<h1 style='font-size: 32px;'>📄 صانع الفواتير والملصقات الحرارية الذكي</h1>", unsafe_allow_html=True)
    st.markdown("### 📊 إحصائيات متجرك الشاملة:")
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    total_sales_db = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conne)
    total_stock_db = pd.read_sql("SELECT SUM(available_qty) as total_qty FROM store_stock", conne)
    
    with stat_col1: st.metric(label="💰 إجمالي مداخيل المبيعات", value=f"{total_sales_db['final_total'].sum():,.2f} DA")
    with stat_col2: st.metric(label="🧾 عدد الفواتير الصادرة", value=f"{len(total_sales_db)} فاتورة")
    with stat_col3:
        try: stock_val = int(total_stock_db['total_qty'].values) if not total_stock_db.empty and total_stock_db['total_qty'].values is not None else 0
        except: stock_val = 0
        st.metric(label="📦 قطع متوفرة بالمستودع", value=f"{stock_val} حبة")
        
    st.markdown("---")
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("🏪 معلومات المتجر والزبون")
        shop_name = st.text_input("اسم متجرك الإلكتروني:", "DZ Cyber Store")
        customer_name = st.text_input("اسم الزبون الكامل:")
        customer_phone = st.text_input("رقم هاتف الزبون:")
        customer_address = st.text_input("عنوان التوصيل والولاية:")
        uploaded_logo = st.file_uploader("اختر لوغو متجرك (اختياري)", type=["png", "jpg", "jpeg"])

    with col_right:
        st.subheader("📦 تفاصيل السلعة والحسابات")
        stock_products = pd.read_sql("SELECT product_name FROM store_stock", conne)
        if not stock_products.empty: 
            product_name = st.selectbox("اختر المنتج من المخزون:", stock_products['product_name'])
        else: 
            product_name = st.text_input("اسم المنتج (قم بإضافته للمخزون أولاً):")
        price = st.number_input("سعر القطعة (DA):", min_value=0, value=1200)
        quantity = st.number_input("الكمية المبيعة:", min_value=1, value=1)
        shipping_cost = st.number_input("مصاريف الشحن (DA):", min_value=0, value=600)

    product_total = price * quantity
    final_total = product_total + shipping_cost
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_month = datetime.now().strftime("%Y-%m")

    st.markdown("---")
    if st.button("🚀 إصدار وحفظ الفاتورة والملصق وخصم المخزون"):
        if not customer_name or not product_name: st.error("❌ خطأ: يرجى ملء اسم الزبون والمنتج أولاً!")
        else:
            check_stock = pd.read_sql(f"SELECT available_qty FROM store_stock WHERE product_name = '{product_name}'", conne)
            if not check_stock.empty and check_stock['available_qty'].values < quantity:
                st.error(f"❌ خطأ! المتبقي في المستودع هو: {check_stock['available_qty'].values} قطع فقط.")
            else:
                cursor.execute("UPDATE store_stock SET available_qty = available_qty - ? WHERE product_name = ?", (quantity, product_name))
                cursor.execute('INSERT INTO v4_customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, month_created, date_created) VALUES (?, ?, ?, ?, ?, ?, ?)', (shop_name, customer_name, customer_phone, product_name, final_total, current_month, current_date))
                conne.commit()
                st.success("💾 تم تسجيل البيع وتوليد المستندات بنجاح!")

                logo_data = uploaded_logo.read() if uploaded_logo is not None else None
                pdf_invoice = generate_invoice_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, price, quantity, product_total, shipping_cost, final_total, current_date, logo_data)
                pdf_label = generate_thermal_label_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, final_total, current_date)
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1: st.download_button(label="📥 تحميل الفاتورة الكبيرة A4 (PDF)", data=pdf_invoice, file_name=f"invoice_{customer_name}.pdf", mime="application/pdf")
                with col_btn2: st.download_button(label="🖨️ تحميل ملصق الشحن الحراري 4x4 (PDF)", data=pdf_label, file_name=f"thermal_label_{customer_name}.pdf", mime="application/pdf")

                if st.button("🖨️ فتح نافذة الطباعة الحرارية السريعة"): st.components.v1.html("<script>window.print();</script>", height=0)

                st.markdown("---")
                st.subheader("📲 أزرار الإرسال السريع الفوري لزبونك:")
                msg_text = f"مرحباً {customer_name}، تم تأكيد طلبيتك بنجاح من متجر {shop_name}. المنتج: {product_name}، الإجمالي للدفع هو: {final_total:,} DA."
                encoded_msg = urllib.parse.quote(msg_text)
                send_col1, send_col2 = st.columns(2)
                with send_col1: st.link_button("🟢 إرسال تفاصيل الفاتورة عبر WhatsApp", f"https://wa.me{customer_phone}?text={encoded_msg}")
                with send_col2: st.link_button("🟣 إرسال تفاصيل الفاتورة عبر Viber", f"viber://forward?text={encoded_msg}")
# ========================================================
# الجزء الثالث: إدارة المخزون، والمميزات الثالثة والرابعة بعد اكتمالها
# ========================================================

elif choice == "📦 إدارة وتنبيهات المخزون السلعي":
    st.write("<h1 style='font-size: 32px;'>📦 نظام إدارة ومراقبة مخزون المستودع</h1>", unsafe_allow_html=True)
    col_add, col_view = st.columns(2)
    with col_add:
        st.subheader("📝 إضافة سلعة للمستودع:")
        new_prod = st.text_input("اسم السلعة الجديدة:")
        new_qty = st.number_input("الكمية المتوفرة:", min_value=1, value=50)
        if st.button("➕ حفظ في المستودع"):
            if new_prod:
                try:
                    cursor.execute("INSERT INTO store_stock (product_name, available_qty) VALUES (?, ?)", (new_prod, new_qty))
                    conne.commit()
                    st.success(f"تم إضافة {new_prod} للمستودع!")
                    st.rerun()
                except: st.error("المنتج موجود مسبقاً في المخزون.")
                    
    with col_view:
        st.subheader("📋 حالة السلع المتوفرة حالياً:")
        stock_df = pd.read_sql("SELECT * FROM store_stock", conne)
        if not stock_df.empty:
            st.dataframe(stock_df, use_container_width=True)
            st.markdown("---")

# --- الميزة الثالثة بعد تفعيلها بالحرف: مطهر ملفات المبيعات وإحصائيات الولايات ---
elif choice == "🧼 مطهر ملفات المبيعات وإحصائيات الولايات":
    st.write("<h1 style='font-size: 32px;'>🧼 مطهر ملفات المبيعات وإحصائيات الولايات الذكي</h1>", unsafe_allow_html=True)
    st.info("👋 مرحباً بك في قسم التطهير المتقدم للبيانات وتوزيع المبيعات على الولايات الجزائريّة.")
    
    # تشغيل خوارزمية تصفية الملفات المرفوعة وحساب إحصائيات التوصيل
    process_sales_file(conne)

# --- الميزة الرابعة بعد تفعيلها بالحرف: مولّد الحملات والتخطيط التسويقي (AI) ---
elif choice == "🚀 مولّد الحملات والتخطيط التسويقي (AI)":
    st.write("<h1 style='font-size: 32px;'>🚀 مركز التسويق الذكي وتوليد الحملات بالإستعانة بالـ AI</h1>", unsafe_allow_html=True)
    
    # تفعيل واجهة الـ AI التسويقية وتحليل البيانات الاستقصائية
    render_marketing_hub()
    render_data_insights(conne)
