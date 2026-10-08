import io
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def arabic_pdf_text(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def generate_invoice_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, price, quantity, product_total, shipping_cost, final_total, current_date, logo_data=None):
    """ دالة الفاتورة العادية A4 """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    if logo_data is not None:
        try:
            p.drawInlineImage(io.BytesIO(logo_data), 50, 700, width=80, height=80)
        except: pass
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
    p.setFont("Helvetica", 10)
    p.drawString(50, 350, arabic_pdf_text("شكراً لتسوقكم من متجرنا - تم إصدار وتطهير الفاتورة بنجاح"))
    p.showPage()
    p.save()
    return buffer.getvalue()

def generate_thermal_label_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, final_total, current_date):
    """ ✨ الميزة الجديدة: دالة توليد ملصق الشحن الحراري بمقاس صغير (4x4 إنش) مخصص للطابعات الحرارية السريعة """
    buffer = io.BytesIO()
    # تحديد المقاس الصغير للملصق (288x288 نقطة هندسية تعادل 4x4 إنش)
    p = canvas.Canvas(buffer, pagesize=(288, 288))
    
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(144, 265, f"📄 {shop_name.upper()} SHIPPING LABEL")
    p.setFont("Helvetica", 10)
    p.drawString(20, 245, "================================")
    p.drawString(20, 225, f"Date: {current_date}")
    p.setFont("Helvetica-Bold", 11)
    p.drawString(20, 195, f"To: {customer_name}")
    p.drawString(20, 175, f"Phone: {customer_phone}")
    p.setFont("Helvetica", 10)
    p.drawString(20, 155, f"Wilaya: {customer_address}")
    p.drawString(20, 130, "--------------------------------")
    p.drawString(20, 110, f"Product: {product_name}")
    p.drawString(20, 90, "--------------------------------")
    p.setFont("Helvetica-Bold", 13)
    p.drawString(20, 60, f"COD TOTAL: {final_total:,} DA")
    p.setFont("Helvetica", 8)
    p.drawCentredString(144, 25, arabic_pdf_text("يرجى التحقق من المبلغ قبل الاستلام - Yalidine / ZR"))
    
    p.showPage()
    p.save()
    return buffer.getvalue()

