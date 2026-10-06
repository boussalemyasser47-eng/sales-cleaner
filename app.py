import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from fpdf import FPDF

# 🎨 إعدادات واجهة الموقع لتكون عريضة واحترافية
st.set_page_config(page_title="نظام المبيعات والفواتير المتكامل", layout="wide")

# 🏛️ ربط قاعدة البيانات المشتركة
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
        date_created TEXT
    )
''')
conne.commit()

# --- القائمة الجانبية للتنقل بين الأدوات ---
st.sidebar.title("🛠️ لوحة التحكم الذكية")
choice = st.sidebar.radio("اختر الأداة التي تريد استخدامها:", [
    "✨ صانع الفواتير السريع (PDF)", 
    "🧼 مطهر ملفات المبيعات (حذف التكرار)"
])

# ========================================================
# الميزة الأولى: صانع الفواتير وتوليد الـ PDF وحفظها
# ========================================================
if choice == "✨ صانع الفواتير السريع (PDF)":
    st.title("📄 صانع الفواتير الرقمية وتوليد ملفات PDF 🇩🇿")
    st.write("اصنع فاتورتك فردية، احفظها في قاعدة البيانات، وحمّلها لزبونك فوراً.")
    
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

    product_total = price * quantity
    final_total = product_total + shipping_cost
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    st.markdown("---")
    if st.button("🚀 إصدار وحفظ الفاتورة الحالية"):
        if not customer_name or not product_name:
            st.error("❌ خطأ: يرجى ملء اسم الزبون والمنتج أولاً!")
        else:
            cursor.execute('''
                INSERT INTO customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, date_created)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (shop_name, customer_name, customer_phone, product_name, final_total, current_date))
            conne.commit()
            st.success("💾 تم حفظ الفاتورة بنجاح في الأرشيف!")

            # توليد ملف PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            
            def clean_txt(text):
                return str(text).encode('utf-8', 'ignore').decode('utf-8')

            pdf.cell(200, 10, txt=f"INVOICE - {clean_txt(shop_name).upper()}", ln=True, align='C')
            pdf.cell(200, 10, txt="=========================================", ln=True, align='C')
            pdf.cell(200, 10, txt=f"Date: {current_date}", ln=True)
            pdf.cell(200, 10, txt=f"Customer Name: {clean_txt(customer_name)}", ln=True)
            pdf.cell(200, 10, txt=f"Phone: {clean_txt(customer_phone)}", ln=True)
            pdf.cell(200, 10, txt=f"Address: {clean_txt(customer_address)}", ln=True)
            pdf.cell(200, 10, txt="-----------------------------------------", ln=True)
            pdf.cell(200, 10, txt=f"Product: {clean_txt(product_name)}", ln=True)
            pdf.cell(200, 10, txt=f"Price: {price:,} DA  x  Qty: {quantity}", ln=True)
            pdf.cell(200, 10, txt=f"Subtotal: {product_total:,} DA", ln=True)
            pdf.cell(200, 10, txt=f"Shipping Cost: {shipping_cost:,} DA", ln=True)
            pdf.cell(200, 10, txt="-----------------------------------------", ln=True)
            pdf.set_font("Helvetica", size=14)
            pdf.cell(200, 10, txt=f"TOTAL TO PAY: {final_total:,} DA", ln=True)
            
            try:
                pdf_bytes = bytes(pdf.output())
                st.download_button(
                    label="📥 تحميل الفاتورة بصيغة PDF لـ إرسالها للزبون",
                    data=pdf_bytes,
                    file_name=f"invoice_{customer_name}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error("💡 يرجى استخدام الحروف اللاتينية والأرقام لتوليد ملف الـ PDF بنجاح.")

    # عرض أرشيف الفواتير الفردية
    st.markdown("---")
    st.subheader("📋 أرشيف الفواتير الفردية المحفوظة:")
    all_invoices = pd.read_sql("SELECT * FROM customer_invoices ORDER BY invoice_id DESC", conne)
    if not all_invoices.empty:
        st.dataframe(all_invoices, use_container_width=True)
        st.metric(label="📊 إجمالي المداخيل المسجلة بالفواتير", value=f"{all_invoices['final_total'].sum():,.2f} DA")

# ========================================================
# الميزة الثانية: مطهر ملفات المبيعات المرفوعة من التكرار
# ========================================================
elif choice == "🧼 مطهر ملفات المبيعات (حذف التكرار)":
    st.title("🧼 نظام فحص وتطهير ملفات المبيعات الجماعية")
    st.write("ارفع ملف الـ CSV الخاص بمتجرك لحذف التكرار وتطهير الأسعار السالبة والأخطاء فوراً.")
    
    uploaded_file = st.file_uploader("اختر ملف المبيعات المراد تنظيفه (صيغة CSV)", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.subheader("📋 الملف المرفوع (قبل التطهير):")
        st.dataframe(df.head())
        
        # 🛡️ عملية فحص وتطهير التكرار والأخطاء
        # 1. تنظيف الأسعار وتحويلها
        if 'item_price' in df.columns:
            df['item_price'] = df['item_price'].astype(str).str.replace(' DA', '').astype(float)
        
        # 2. كشف وعزل الأسطر المكررة بناءً على اسم المنتج أو أرقام الهواتف
        # قمنا بحذف التكرار والاحتفاظ بأول عملية بيع فقط لحماية البيانات
        duplicated_rows = df[df.duplicated(subset=['product_name'], keep='first')]
        df.drop_duplicates(subset=['product_name'], keep='first', inplace=True)
        
        # 3. عزل الأسعار السالبة
        bad_prices = df[df['item_price'] <= 0]
        df = df[df['item_price'] > 0]
        
        # 4. تنظيف التواريخ الناقصة
        if 'sale_date' in df.columns:
            df['sale_date'] = pd.to_datetime(df['sale_date'], dayfirst=True, format='mixed', errors='coerce')
            df.dropna(subset=['sale_date'], inplace=True)
            
        st.success("✅ تم تنظيف وتطهير الملف بنجاح من كافة الأخطاء والتكرارات!")
        
        col_clean, col_trash = st.columns(2)
        with col_clean:
            st.subheader("💎 جدول البيانات النظيف تماماً:")
            st.dataframe(df)
        with col_trash:
            st.subheader("⚠️ التكرارات والأخطاء المحذوفة:")
            if not duplicated_rows.empty or not bad_prices.empty:
                if not duplicated_rows.empty:
                    st.warning(f"تم حذف {len(duplicated_rows)} سطر مكرر!")
                    st.dataframe(duplicated_rows)
                if not bad_prices.empty:
                    st.error(f"تم حذف {len(bad_prices)} سطر يحتوي على قيم سالبة!")
                    st.dataframe(bad_prices)
            else:
                st.info("الملف سليم تماماً ولا يحتوي على تكرارات أو أخطاء شاذة.")
                
        # إمكانية تحميل الملف النظيف مجدداً كملف CSV
        csv_buffer = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 تحميل ملف المبيعات المطهّر (Cleaned CSV)",
            data=csv_buffer,
            file_name="cleaned_sales_report.csv",
            mime="text/csv"
        )

conne.close()

