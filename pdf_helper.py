import io
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def arabic_pdf_text(text):
    """ دالة ذكية لتصحيح وعكس الكلمات العربية لكي تظهر صحيحة وموصولة داخل ملف الـ PDF """
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def generate_invoice_pdf(shop_name, customer_name, customer_phone, customer_address,
                         product_name, price, quantity, product_total, shipping_cost, final_total,
                         current_date, logo_data=None):
    """ دالة معالجة خلفية لبناء وتوليد ملف PDF احترافي منسق يدعم الحروف العربية والشعار """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # رسم شعار اللوغو في أعلى الفاتورة على اليسار إذا تم رفعه من طرف التاجر
    if logo_data is not None:
        try:
            logo_bytes = io.BytesIO(logo_data)
            p.drawInlineImage(logo_bytes, 50, 700, width=80, height=80)
        except:
            pass
    
    # كتابة وتنسيق نصوص الفاتورة في مكانها الصحيح هندسياً داخل الصفحة
    p.setFont("Helvetica-Bold", 16)
    p.drawString(150, 750, f"INVOICE: {shop_name.upper()}")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 670, f"Date: {current_date}")
    p.drawString(50, 640, f"Customer: {customer_name}")
    p.drawString(50, 620, f"Phone: {customer_phone}")
    p.drawString(50, 600, f"Address: {customer_address}")
    p.drawString(50, 570, "--------------------------------------------------------")
    p.drawString(50, 550, f"Product Name: {product_name}")
    p.drawString(50, 530, f"Price per Item: {price:,} DA  x  Qty: {quantity}")
    p.drawString(50, 510, f"Subtotal: {product_total:,} DA")
    p.drawString(50, 490, f"Shipping Cost: {shipping_cost:,} DA")
    p.drawString(50, 460, "--------------------------------------------------------")
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 430, f"TOTAL TO PAY: {final_total:,} DA")
    
    # طباعة رسالة شكر باللغة العربية أسفل الفاتورة باستخدام دالة معالجة النصوص وعكسها
    p.setFont("Helvetica", 10)
    p.drawString(50, 350, arabic_pdf_text("شكراً لتسوقكم من متجرنا - تم إصدار وتطهير الفاتورة بنجاح"))
    
    p.showPage()
    p.save()
    
    return buffer.getvalue()
