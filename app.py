import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import io
import urllib.parse

# استدعاء الدوال من الملفات الفرعية المخصصة الثابتة
from styles import apply_neon_theme
from pdf_helper import generate_invoice_pdf
from cleaner_helper import process_sales_file
from ai_helper import render_ai_chatbot

# تطبيق التنسيق والواجهة العريضة
st.set_page_config(page_title="نظام المبيعات والمخزون الأسطوري", layout="wide")
apply_neon_theme()

# 🏛️ ربط قاعدة البيانات وتجهيز جداول المبيعات والمخزون
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

# --- القائمة الجانبية للتنقل بين الأدوات ---
st.sidebar.markdown("<h2 style='color: #00ffcc; text-align: center; text-shadow: 0 0 10px #00ffcc; font-size: 24px;'>🛠️ التحكم</h2>", unsafe_allow_html=True)
choice = st.sidebar.radio("اختر الأداة التي تريد استخدامها:", [
    "✨ صانع الفواتير الاحترافي (PDF)", 
    "📦 إدارة وتنبيهات المخزون السلعي",
    "🧼 مطهر ملفات المبيعات وإحصائيات الولايات"
])

# تشغيل مساعد الذكاء الاصطناعي تلقائياً في أسفل القائمة الجانبية
render_ai_chatbot()

# ========================================================
# الميزة الأولى: صانع الفواتير والبطاقات والارسال السريع
# ========================================================
if choice == "✨ صانع الفواتير الاحترافي (PDF)":
    st.write("<h1 style='font-size: 32px;'>📄 صانع الفواتير الأسطوري الذكي</h1>", unsafe_allow_html=True)
    
    # بطاقات الإحصائيات الفخمة (Neon Metric Cards)
    st.markdown("### 📊 إحصائيات متجرك الشاملة:")
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    total_sales_db = pd.read_sql("SELECT final_total FROM v4_customer_invoices", conne)
    total_stock_db = pd.read_sql("SELECT SUM(available_qty) as total_qty FROM store_stock", conne)
    
    with stat_col1:
        st.metric(label="💰 إجمالي مداخيل المبيعات", value=f"{total_sales_db['final_total'].sum():,.2f} DA")
    with stat_col2:
        st.metric(label="🧾 عدد الفواتير الصادرة", value=f"{len(total_sales_db)} فاتورة")
    with stat_col3:
        stock_val = total_stock_db['total_qty'].values[0] if not total_stock_db.empty and total_stock_db['total_qty'].values[0] is not None else 0
        st.metric(label="📦 قطع متوفرة بالمستودع", value=f"{int(stock_val)} حبة")
        
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("🏪 معلومات المتجر والزبون")
        shop_name = st.text_input("اسم متجرك الإلكتروني:", "DZ Cyber Store")
        customer_name = st.text_input("اسم الزبون الكامل:")
        customer_phone = st.text_input("رقم هاتف الزبون:")
        customer_address = st.text_input("عنوان التوصيل والولاية:")
        uploaded_logo = st.file_uploader("اختر لوغو متجرك لإضافته (اختياري)", type=["png", "jpg", "jpeg"])

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
    if st.button("🚀 إصدار وحفظ الفاتورة وخصم المخزون"):
        if not customer_name or not product_name:
            st.error("❌ خطأ: يرجى ملء اسم الزبون والمنتج أولاً!")
        else:
            check_stock = pd.read_sql(f"SELECT available_qty FROM store_stock WHERE product_name = '{product_name}'", conne)
            if not check_stock.empty and check_stock['available_qty'].values[0] < quantity:
                st.error(f"❌ خطأ! المتبقي في المستودع هو: {check_stock['available_qty'].values[0]} قطع فقط.")
            else:
                cursor.execute(f"UPDATE store_stock SET available_qty = available_qty - {quantity} WHERE product_name = ?", (product_name,))
                cursor.execute('''
                    INSERT INTO v4_customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, month_created, date_created)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (shop_name, customer_name, customer_phone, product_name, final_total, current_month, current_date))
                conne.commit()
                st.success("💾 تم تسجيل البيع وحفظ الفاتورة بنجاح!")

                logo_data = uploaded_logo.read() if uploaded_logo is not None else None
                pdf_data = generate_invoice_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, price, quantity, product_total, shipping_cost, final_total, current_date, logo_data)
                
                pdf_col1, pdf_col2 = st.columns(2)
                with pdf_col1:
                    st.download_button(label="📥 تحميل الفاتورة الرسمية (PDF)", data=pdf_data, file_name=f"invoice_{customer_name}.pdf", mime="application/pdf")
                with pdf_col2:
                    if st.button("🖨️ فتح نافذة الطباعة المباشرة"):
                        st.components.v1.html("<script>window.print();</script>", height=0)

                st.markdown("---")
                st.subheader("📲 أزرار الإرسال السريع الفوري لزبونك:")
                msg_text = f"مرحباً {customer_name}، تم تأكيد طلبيتك بنجاح من متجر {shop_name}. المنتج: {product_name}، الإجمالي للدفع هو: {final_total:,} DA."
                encoded_msg = urllib.parse.quote(msg_text)
                
                send_col1, send_col2 = st.columns(2)
                with send_col1:
                    st.link_button("🟢 إرسال تفاصيل الفاتورة عبر WhatsApp", f"https://wa.me{customer_phone}?text={encoded_msg}")
                with send_col2:
                    st.link_button("🟣 إرسال تفاصيل الفاتورة عبر Viber", f"viber://forward?text={encoded_msg}")
# ========================================================
# الميزة الثانية: قسم إدارة المخزون السلعي والتنبيهات
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
                except:
                    st.error("المنتج موجود مسبقاً في المخزون.")
                    
    with col_view:
        st.subheader("📋 حالة السلع المتوفرة حالياً:")
        stock_df = pd.read_sql("SELECT * FROM store_stock", conne)
        if not stock_df.empty:
            st.dataframe(stock_df, use_container_width=True)
            low_stock = stock_df[stock_df['available_qty'] <= 5]
            if not low_stock.empty:
                st.markdown("---")
                st.write("<h3 style='color: #ff007f !important;'>🚨 تنبيه: سلع أوشكت على النفاذ!</h3>", unsafe_allow_html=True)
                st.dataframe(low_stock)
        else:
            st.info("مستودعك خالي تماماً حالياً.")

# ========================================================
# الميزة الثالثة: مطهر ملفات المبيعات وإحصائيات الولايات
# ========================================================
elif choice == "🧼 مطهر ملفات المبيعات وإحصائيات الولايات":
    st.write("<h1 style='font-size: 32px;'>🧼 نظام التطهير وعرض مقارنة البيانات والولايات</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("اختر ملف المبيعات (CSV أو Excel)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        df_raw, df, duplicated_rows, bad_prices = process_sales_file(uploaded_file)
        
        st.subheader("📋 1. جدول البيانات الأصلي المرفوع (قبل التطهير):")
        st.dataframe(df_raw, use_container_width=True)
        st.success("✅ تم تنظيف الداتا بنجاح وتجهيز المقارنة البصرية!")
        
        col_clean, col_trash = st.columns(2)
        with col_clean:
            st.subheader("💎 2. جدول البيانات النظيف (بعد التطهير):")
            st.dataframe(df, use_container_width=True)
            st.metric(label="صافي الأرباح الحقيقية المتوقعة", value=f"{df['total_row_sales'].sum():,.2f} DA")
        with col_trash:
            st.subheader("⚠️ 3. التكرارات والأخطاء المحذوفة:")
            if not duplicated_rows.empty or not bad_prices.empty:
                if not duplicated_rows.empty:
                    st.warning(f"تم حذف {len(duplicated_rows)} سطر مكرر!")
                    st.dataframe(duplicated_rows)
                if not bad_prices.empty:
                    st.error(f"تم حذف {len(bad_prices)} سطر أسعار سالبة!")
                    st.dataframe(bad_prices)
            else:
                st.info("الملف سليم تماماً ولا يحتوي على أخطاء.")
                
        st.markdown("---")
        st.subheader("📈 المخططات البيانية الملونة للولايات والمبيعات:")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.write("💰 حجم المبيعات الإجمالي الحقيقي لكل منتج:")
            st.bar_chart(data=df, x='product_name', y='total_row_sales', color='#00ffcc')
        with chart_col2:
            wilaya_col = None
            for col in df.columns:
                if 'address' in col.lower() or 'wilaya' in col.lower() or 'ولاية' in col:
                    wilaya_col = col
                    break
            if wilaya_col:
                st.write(f"🗺️ حجم الشحن والمبيعات حسب الولايات الجزائرية:")
                st.bar_chart(data=df, x=wilaya_col, y='total_row_sales', color='#ff007f')
            else:
                st.info("💡 نصيحة: سمّ عمود السكن في ملفك باسم 'wilaya' ليظهر مخطط فرز الولايات.")
            
        csv_buffer = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 تحميل ملف المبيعات المطهّر بالكامل", data=csv_buffer, file_name="cleaned_neon_sales.csv", mime="text/csv")

conne.close()
