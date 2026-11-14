# ========================================================
# الجزء الأول المطور - [1 من 4]: النواة والتحقق الشبح (gate_core.py)
# ========================================================
# ========================================================
# 🔒 [خزانة النسخ الاحتياطي التلقائي المشفرة - Cyber Auto-Backup Vault]
# ========================================================
# ========================================================
# [القسم الأول]: إعدادات البيئة، خزانة النسخ الاحتياطي، وجدار حماية الشبح المتقدم
# ========================================================
# ========================================================
# الجزء الأول المطور - [1 من 4]: النواة والتحقق الشبح (gate_core.py)
# ========================================================
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import pandas as pd
import sqlite3
import time
from datetime import datetime
import io
import urllib.parse
import re
import time
import streamlit as st
import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# استيراد أداة توليد الباركود المربع (QR Code) من ReportLab
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget

# استيراد أدوات إصلاح وعكس النصوص العربية لتظهر متصلة وباتجاه صحيح (RTL)
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_TEXT_PROCESSING = True
except ImportError:
    ARABIC_TEXT_PROCESSING = False

def fix_arabic(text):
    """
    دالة مساعدة لمعالجة النصوص العربية لضمان اتصالها واتجاهها الصحيح (RTL) وتفادي أي انعكاس
    """
    if not text or not isinstance(text, str):
        return str(text)
    if ARABIC_TEXT_PROCESSING:
        try:
            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)
            return bidi_text
        except Exception:
            return text
    return text

# === تسجيل الخط العربي لدعم اللغة العربية ومنع ظهور المربعات ===
try:
    pdfmetrics.registerFont(TTFont('ArabicFont', 'Cairo.ttf'))
    ARABIC_FONT_AVAILABLE = True
except Exception:
    try:
        pdfmetrics.registerFont(TTFont('ArabicFont', 'Amiri-Regular.ttf'))
        ARABIC_FONT_AVAILABLE = True
    except Exception:
        ARABIC_FONT_AVAILABLE = False

FONT_NAME = 'ArabicFont' if ARABIC_FONT_AVAILABLE else 'Helvetica'

def generate_invoice_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, price, quantity, product_total, shipping_cost, final_total, logo_data):
    """
    دالة توليد فاتورة مبيعات رسمية بحجم A4 بالجدول الأزرق الاحترافي مع دعم QR Code رقمي موثق[cite: 1]
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=30, 
        leftMargin=30, 
        topMargin=30, 
        bottomMargin=30
    )
    elements = []
    
    styles = getSampleStyleSheet()
    
    # أنماط النصوص الاحترافية
    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontName=FONT_NAME,
        fontSize=22,
        textColor=colors.HexColor('#003366'),
        alignment=1,
        spaceAfter=6
    )
    
    sub_title_style = ParagraphStyle(
        'InvoiceSubTitle',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=12,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceAfter=15
    )
    
    cell_style_right = ParagraphStyle(
        'CellRight',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        textColor=colors.HexColor('#222222'),
        alignment=2
    )

    cell_style_center = ParagraphStyle(
        'CellCenter',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        textColor=colors.HexColor('#222222'),
        alignment=1
    )

    # إضافة اللوغو إن وجد
    if logo_data:
        try:
            logo_buffer = io.BytesIO(logo_data)
            img = Image(logo_buffer, width=65, height=65)
            elements.append(img)
            elements.append(Spacer(1, 8))
        except Exception:
            pass

    elements.append(Paragraph(fix_arabic(f"<b>{shop_name}</b>"), title_style))
    elements.append(Paragraph(fix_arabic("<b>فاتورة مبيعات وتأكيد طلبية رسمية وموثقة</b>"), sub_title_style))
    elements.append(Spacer(1, 10))

    # جدول بيانات المتجر والزبون (تصميم هندسي متناسق ومن اليمين لليسار)
    t_info_formatted = [
        [Paragraph(fix_arabic(f"<b>اسم المتجر:</b> {shop_name}"), cell_style_right), Paragraph(fix_arabic(f"<b>اسم الزبون:</b> {customer_name}"), cell_style_right)],
        [Paragraph(fix_arabic(f"<b>عنوان التوصيل:</b> {customer_address}"), cell_style_right), Paragraph(fix_arabic(f"<b>رقم الهاتف:</b> {customer_phone}"), cell_style_right)]
    ]
    t_info = Table(t_info_formatted, colWidths=[260, 260])
    t_info.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
        ('BOX', (0,0), (-1,-1), 0.7, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    elements.append(t_info)
    elements.append(Spacer(1, 15))

    # جدول تفاصيل المنتجات والأسعار (التصميم الأزرق الكلاسيكي Mفضل)
    table_data = [
        [
            Paragraph(fix_arabic("<b>الإجمالي (DA)</b>"), ParagraphStyle('H1', parent=cell_style_center, fontName=FONT_NAME, textColor=colors.whitesmoke)),
            Paragraph(fix_arabic("<b>السعر الفردي</b>"), ParagraphStyle('H2', parent=cell_style_center, fontName=FONT_NAME, textColor=colors.whitesmoke)),
            Paragraph(fix_arabic("<b>الكمية</b>"), ParagraphStyle('H3', parent=cell_style_center, fontName=FONT_NAME, textColor=colors.whitesmoke)),
            Paragraph(fix_arabic("<b>اسم المنتج</b>"), ParagraphStyle('H4', parent=cell_style_right, fontName=FONT_NAME, textColor=colors.whitesmoke))
        ],
        [
            Paragraph(f"{product_total:,.2f}", cell_style_center),
            Paragraph(f"{price:,.2f}", cell_style_center),
            Paragraph(str(quantity), cell_style_center),
            Paragraph(fix_arabic(product_name), cell_style_right)
        ]
    ]
    t_items = Table(table_data, colWidths=[110, 110, 60, 240])
    t_items.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#003366')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#ffffff')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    elements.append(t_items)
    elements.append(Spacer(1, 15))

    # جدول المجاميع النهائية
    totals_data = [
        [Paragraph(f"<b>{product_total:,.2f} DA</b>", cell_style_right), Paragraph(fix_arabic("<b>المجموع الفرعي للمنتج:</b>"), cell_style_right)],
        [Paragraph(f"<b>{shipping_cost:,.2f} DA</b>", cell_style_right), Paragraph(fix_arabic("<b>تكلفة الشحن والتوصيل:</b>"), cell_style_right)],
        [
            Paragraph(f"<b>{final_total:,.2f} DA</b>", ParagraphStyle('FTotal', parent=cell_style_right, fontName=FONT_NAME, fontSize=11, textColor=colors.HexColor('#003366'))), 
            Paragraph(fix_arabic("<b>الإجمالي النهائي المطلوب:</b>"), ParagraphStyle('FTotalLbl', parent=cell_style_right, fontName=FONT_NAME, fontSize=11, textColor=colors.HexColor('#003366')))
        ]
    ]
    t_totals = Table(totals_data, colWidths=[160, 190])
    t_totals.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('LINEABOVE', (0,2), (-1,2), 1, colors.HexColor('#003366')),
    ]))
    elements.append(t_totals)
    elements.append(Spacer(1, 20))

    # === إضافة الختم الرقمي أو QR Code الديناميكي الموثق في أسفل الفاتورة ===
    qr_data_string = f"Shop: {shop_name} | Customer: {customer_name} | Phone: {customer_phone} | Product: {product_name} | Total: {final_total} DA | Status: Verified"
    
    qr = QrCodeWidget(qr_data_string)
    qr.barWidth = 70
    qr.barHeight = 70
    qr.qrVersion = 1
    
    d = Drawing(70, 70)
    d.add(qr)

    verification_text_style = ParagraphStyle(
        'VerifyText',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=8.5,
        textColor=colors.HexColor('#444444'),
        alignment=2
    )

    qr_section_data = [
        [
            Paragraph(fix_arabic("<b>ختم التحقق الرقمي الموثق:</b><br/>هذه الفاتورة صادرة إلكترونياً ومؤمنة عبر نظام NEXUS CENTRAL GATE. يمنع تزويرها أو تعديل بياناتها وتخضع للسجل التجاري للمتجر."), verification_text_style),
            d
        ]
    ]
    t_qr = Table(qr_section_data, colWidths=[380, 120])
    t_qr.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    
    elements.append(t_qr)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def generate_thermal_label_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, final_total, current_date):
    """
    دالة توليد ملصق الشحن الحراري (4x4 بوصة) بشكل هندسي منظم، مع إطار خارجي وخط فاصل أنيق[cite: 1]
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=(4 * inch, 4 * inch), 
        rightMargin=14, 
        leftMargin=14, 
        topMargin=14, 
        bottomMargin=14
    )
    elements = []
    
    styles = getSampleStyleSheet()
    label_title = ParagraphStyle(
        'LabelTitle',
        parent=styles['Heading2'],
        fontName=FONT_NAME,
        fontSize=12,
        textColor=colors.HexColor('#000000'),
        alignment=1,
        spaceAfter=2
    )
    label_normal = ParagraphStyle(
        'LabelNormal',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9,
        textColor=colors.HexColor('#111111'),
        alignment=2,
        spaceAfter=4
    )
    label_price = ParagraphStyle(
        'LabelPrice',
        parent=label_normal,
        fontName=FONT_NAME,
        fontSize=10.5,
        textColor=colors.HexColor('#990000'),
        alignment=1
    )
    
    # محتوى العناصر الداخلية للملصق
    inner_elements = []
    
    # اسم المتجر والعنوان الفرعي
    inner_elements.append(Paragraph(fix_arabic(shop_name), label_title))
    inner_elements.append(Paragraph(fix_arabic("--- ملصق شحن وتوصيل حراري ---"), ParagraphStyle('SubLbl', parent=label_normal, alignment=1, fontSize=8, textColor=colors.HexColor('#555555'))))
    
    # خط فاصل أنيق تحت اسم المتجر والعنوان الفرعي
    inner_elements.append(Spacer(1, 2))
    divider_table = Table([[""]], colWidths=[250], rowHeights=[1])
    divider_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1, colors.HexColor('#333333')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    inner_elements.append(divider_table)
    inner_elements.append(Spacer(1, 6))
    
    # بيانات الشحن والزبون منظمة من اليمين لليسار
    inner_elements.append(Paragraph(f"{current_date} : {fix_arabic('التاريخ')}", label_normal))
    inner_elements.append(Paragraph(f"{customer_name} : {fix_arabic('الزبون')}", label_normal))
    inner_elements.append(Paragraph(f"{customer_phone} : {fix_arabic('الهاتف')}", label_normal))
    inner_elements.append(Paragraph(f"{customer_address} : {fix_arabic('العنوان')}", label_normal))
    inner_elements.append(Paragraph(f"{product_name} : {fix_arabic('المنتج')}", label_normal))
    
    inner_elements.append(Spacer(1, 4))
    price_str = f"{final_total:,.2f} DA"
    inner_elements.append(Paragraph(f"{price_str} : {fix_arabic('المبلغ الواجب تحصيله')}", label_price))

    # وضع العناصر داخل جدول يحيط به إطار خارجي (Border) واضح للطباعة
    outer_table = Table([[inner_elements]], colWidths=[260])
    outer_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#000000')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
    ]))
    
    elements.append(outer_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
# تهيئة حالة عرض الصفحة الافتراضية
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "auth"
# 🌟 تصميم نافذة التحقق المنبثقة في المنتصف (Modal Dialog)
def render_otp_popup(target_email):
    # إخفاء الخلفية وتثبيت النافذة في المنتصف بتصميم نيون فخم
    st.markdown("""
        <style>
        .otp-modal-overlay {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(3, 3, 7, 0.85);
            backdrop-filter: blur(8px);
            z-index: 99999;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .otp-modal-box {
            background: linear-gradient(135deg, #0d0d21 0%, #05050c 100%);
            border: 2px solid #00fff0;
            border-radius: 20px;
            padding: 30px;
            width: 450px;
            box-shadow: 0 0 40px rgba(0, 255, 240, 0.4);
            direction: rtl;
            text-align: right;
            animation: elasticPop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
        </style>
    """, unsafe_allow_html=True)

    # محتوى النافذة المنبثقة
    st.markdown("""
        <div class="otp-modal-overlay">
            <div class="otp-modal-box">
                <h3 style="color: #00fff0; text-align: center; margin-top: 0; font-weight: 900;">🔐 تحقق الأمان</h3>
                <p style="color: #e0e0e0; font-size: 14px; text-align: center; margin-bottom: 20px;">
                    سيتم إرسال رمز التحقق إلى بريدك الإلكتروني:<br>
                    <span style="color: #ff00ff; font-weight: bold;">{email}</span>
                </p>
            </div>
        </div>
    """.format(email=target_email), unsafe_allow_html=True)

    # 🔢 خانات إدخال الرمز الـ 6 المنفصلة
    st.markdown("<p style='color: #00fff0; font-weight: bold; text-align: center;'>أدخل الرمز المكون من 6 أرقام:</p>", unsafe_allow_html=True)
    
    # تقسيم الحقول إلى 6 أعمدة تشبه الصورة التي أرفقتها تماماً
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    d1 = c1.text_input("", key="otp_1", max_chars=1, label_visibility="collapsed")
    d2 = c2.text_input("", key="otp_2", max_chars=1, label_visibility="collapsed")
    d3 = c3.text_input("", key="otp_3", max_chars=1, label_visibility="collapsed")
    d4 = c4.text_input("", key="otp_4", max_chars=1, label_visibility="collapsed")
    d5 = c5.text_input("", key="otp_5", max_chars=1, label_visibility="collapsed")
    d6 = c6.text_input("", key="otp_6", max_chars=1, label_visibility="collapsed")

    # تجميع الأرقام المدخلة
    full_entered_otp = f"{d1}{d2}{d3}{d4}{d5}{d6}"

    # ⏱️ محاكاة العداد التنازلي (Countdown Timer)
    if "otp_timer" not in st.session_state:
        st.session_state["otp_timer"] = 59

    st.markdown(f"<p style='text-align: center; color: #ffaa00; font-size: 13px; margin-top: 10px;'>⏳ إعادة إرسال الرمز خلال: {st.session_state['otp_timer']} ثانية</p>", unsafe_allow_html=True)

    return full_entered_otp
# 🔒 ضبط إعدادات الشاشة الأساسية للمنصة الموحدة
st.set_page_config(page_title="NEXUS CENTRAL GATE v4", page_icon="👑", layout="wide")

query_params = st.query_params
is_boss_link = query_params.get("role") == "boss" if "role" in query_params else False
if "admin_master_logged" not in st.session_state:
    st.session_state["admin_master_logged"] = False

# 1. تهيئة وإنشاء الجداول الجديدة في قاعدة البيانات
def init_advanced_db():
    conn = sqlite3.connect("saas_security_vault.db")
    cursor = conn.cursor()
    
    # 🛡️ جدول المصادقة والتجار مع ضمان وجود عمود التاريخ والتنسيق الثابت
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saas_users_auth (
            email TEXT PRIMARY KEY,
            password TEXT,
            status TEXT,
            package TEXT,
            created_at TEXT,
            phone TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_time TEXT,
            target_email TEXT,
            action_type TEXT,
            details TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sent_time TEXT,
            recipient_email TEXT,
            subject TEXT,
            status TEXT,
            error_message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_advanced_db()

# ========================================================
# 🚀 الدالة الموحدة والوحيدة لإرسال البريد (HTML + Plain Text + تتبع السجل)
# ========================================================
def send_gmail_notification(target_email, subject, body_text, action_type="DEFAULT", action_url=None):
    try:
        sender_email = st.secrets["GMAIL_USER"]
        sender_password = st.secrets["GMAIL_APP_PASSWORD"]
        
        theme_colors = {
            "OTP": {"primary": "#00fff0", "bg_accent": "rgba(0, 255, 240, 0.1)", "icon": "🔐", "btn_text": "تأكيد الرمز الآن"},
            "ACTIVATE": {"primary": "#00ff66", "bg_accent": "rgba(0, 255, 102, 0.1)", "icon": "🎉", "btn_text": "الدخول لمتجرك الآن"},
            "EXTEND": {"primary": "#ffaa00", "bg_accent": "rgba(255, 170, 0, 0.1)", "icon": "⏳", "btn_text": "متابعة متجرك"},
            "UPGRADE": {"primary": "#ff00ff", "bg_accent": "rgba(255, 0, 255, 0.1)", "icon": "🚀", "btn_text": "استكشاف المميزات الخارقة"},
            "LOCK": {"primary": "#ff0055", "bg_accent": "rgba(255, 0, 85, 0.1)", "icon": "⚠️", "btn_text": "التواصل مع الدعم الفني"},
            "DELETE": {"primary": "#ff0055", "bg_accent": "rgba(255, 0, 85, 0.1)", "icon": "❌", "btn_text": "مراجعة الدعم"},
            "DEFAULT": {"primary": "#00fff0", "bg_accent": "rgba(0, 255, 240, 0.1)", "icon": "🔔", "btn_text": "الانتقال للمنصة"}
        }
        
        theme = theme_colors.get(action_type, theme_colors["DEFAULT"])
        btn_link = action_url if action_url else "https://sales-cleaner-qqzrjsdzslrysgsyagohnq.streamlit.app/"
        logo_url = "https://img.icons8.com/isometric-folders/100/00fff0/cyber-security.png"
        formatted_body = body_text.replace("\n", "<br>")

        html_content = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head><meta charset="UTF-8"></head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #05050c; color: #ffffff; padding: 20px; direction: rtl; text-align: right;">
            <div style="max-width: 600px; margin: 0 auto; background: #0d0d21; border: 2px solid {theme['primary']}; border-radius: 16px; padding: 30px; box-shadow: 0 0 20px {theme['primary']}40;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h1 style="color: {theme['primary']}; font-size: 22px; margin: 0;">{theme['icon']} {subject}</h1>
                </div>
                <div style="font-size: 15px; line-height: 1.8; color: #e0e0e0; background: rgba(255, 255, 255, 0.03); padding: 15px; border-radius: 8px; border-right: 4px solid {theme['primary']};">
                    {formatted_body}
                </div>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{btn_link}" style="background: {theme['primary']}; color: #000000; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 8px; display: inline-block;" target="_blank">{theme['btn_text']}</a>
                </div>
                <div style="text-align: center; font-size: 11px; color: #777; margin-top: 30px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                    © 2026 NEXUS SAAS PLATFORM — جميع الحقوق محفوظة.
                </div>
            </div>
        </body>
        </html>
        """

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = target_email
        
        # إرفاق النسختين معاً (النص البسيط + HTML) لضمان عدم حظرها من قِبل Gmail
        message.attach(MIMEText(body_text, "plain", "utf-8"))
        message.attach(MIMEText(html_content, "html", "utf-8"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, target_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"⚠️ خطأ في إرسال البريد الإلكتروني: {e}")
        return False

def send_gmail_notification_with_log(to_email, subject, body, action_type="DEFAULT"):
    from datetime import datetime  # استيراد محلي لتجنب أي تعارض في الملف
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS"
    err_msg = ""
    
    try:
        send_gmail_notification(to_email, subject, body, action_type=action_type)
    except Exception as e:
        status = "FAILED"
        err_msg = str(e)
    finally:
        try:
            conn = sqlite3.connect("saas_security_vault.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO email_logs (sent_time, recipient_email, subject, status, error_message) VALUES (?, ?, ?, ?, ?)",
                (now, to_email, subject, status, err_msg)
            )
            conn.commit()
            conn.close()
        except Exception:
            pass
    
    return status == "SUCCESS"

def create_backup_vault():
    import os
    import zipfile
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in os.listdir("."):
            if file.endswith(".db"):
                try:
                    with open(file, "rb") as f:
                        zip_file.writestr(f"backup_{datetime.now().strftime('%Y%m%d')}_{file}", f.read())
                except Exception:
                    pass
    zip_buffer.seek(0)
    return zip_buffer

# [باقي كود واجهات التاجر والمالك يعمل بشكل طبيعي الآن...]

# [باقي كود واجهات التاجر والمالك يعمل بشكل طبيعي الآن...]
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import pandas as pd
import sqlite3
import time
from datetime import datetime
import io
import urllib.parse
import datetime

# 1. تهيئة وإنشاء الجداول الجديدة في قاعدة البيانات
def init_advanced_db():
    conn = sqlite3.connect("saas_security_vault.db")
    cursor = conn.cursor()
    
    # جدول سجل النشاطات والحركات (Audit Log)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_time TEXT,
            target_email TEXT,
            action_type TEXT,
            details TEXT
        )
    """)
    
    # جدول سجل حالة البريد الإلكتروني (Email Delivery Log)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sent_time TEXT,
            recipient_email TEXT,
            subject TEXT,
            status TEXT,
            error_message TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# تشغيل التهيئة فوراً
init_advanced_db()

# 2. دالة تسجيل الحركات في قاعدة البيانات
def log_admin_action(target_email, action_type, details=""):
  """دالة تسجيل نشاطات المالك مع تصحيح استدعاء التاريخ والوقت"""
  try:
    # التصحيح هنا: استخدام datetime.now() مباشرة بعد استيرادها بشكل صحيح
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("saas_security_vault.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO admin_audit_logs (timestamp, target_email, action_type, details)
        VALUES (?, ?, ?, ?)
    """,
        (now, target_email, action_type, details),
    )
    conn.commit()
    conn.close()
  except Exception as e:
    print(f"Error logging admin action: {e}")

# 3. تطوير دالة إرسال البريد لتسجيل الحالة مع تتبع الأخطاء (try-except)
# ========================================================
# [القسم الأول - المطور]: دالة إرسال الإيميلات الهيكلية الفاخرة (HTML/Neon Pro)
# ========================================================

# ========================================================
# [القسم الثاني]: الحقن السيبراني وتصميم واجهات النيون الزجاجي للأزرار والعدادات
# ========================================================
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com" rel="stylesheet">
    
    <style>
    @keyframes pulseBackground {
        0% { background: radial-gradient(circle at 50% 40%, #0f0f2d 0%, #030307 100%) !important; }
        50% { background: radial-gradient(circle at 50% 45%, #08081a 0%, #010103 100%) !important; }
        100% { background: radial-gradient(circle at 50% 40%, #0f0f2d 0%, #030307 100%) !important; }
    }
    .stApp {
        animation: pulseBackground 8s ease-in-out infinite !important;
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* 💎 صبغ العدادات الثلاثية والمقاييس المستقلة بالبلور الزجاجي والنيون الفاخر المشع */
    div[data-testid="stMetricBlock"], div[data-testid="metric-container"], .premium-card-cyan, .premium-card-pink {
        background: linear-gradient(135deg, rgba(15, 2, 20, 0.85) 0%, rgba(5, 5, 12, 0.98) 100%) !important;
        border: 2px solid #00fff0 !important;
        border-radius: 16px !important;
        box-shadow: 0px 0px 30px rgba(0, 255, 240, 0.35) !important;
        backdrop-filter: blur(15px) !important;
    }
    
    /* صبغ وتلوين البطاقات النيونية المحيطة ببيانات التجار بشكل مرن وديناميكي */
    div[data-testid="stMarkdownContainer"] > div {
        background: linear-gradient(135deg, rgba(10, 10, 26, 0.85) 0%, rgba(3, 3, 7, 0.98) 100%) !important;
        border: 2px solid var(--custom-border-color, #00fff0);
        border-radius: 15px !important;
        box-shadow: 0px 0px 25px rgba(0, 255, 240, 0.2) !important;
    }
    
    /* إجبار الأزرار الخماسية التفاعلية على التوهج الكامل بالألوان السيبرانية الموضحة بالصورة */
    div.stButton button, .stButton > button {
        width: 100% !important; min-height: 48px !important;
        font-family: 'Cairo', sans-serif !important; font-size: 14px !important; font-weight: 900 !important; border-radius: 12px !important;
        background: linear-gradient(135deg, #0d0d21 0%, #05050c 100%) !important; color: #00fff0 !important;
        border: 2px solid #00fff0 !important; box-shadow: 0px 0px 15px rgba(0, 255, 240, 0.3) !important;
    }
    div.stButton button:hover { 
        background: linear-gradient(135deg, #00fff0 0%, #00bfff 100%) !important; color: #000000 !important;
        box-shadow: 0px 0px 30px #00fff0 !important; transform: translateY(-2px) !important;
    }
    
    /* تنظيف وتلوين حقول النصوص لمنع التداخل البصري */
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
        border: 2px solid #ff00ff !important; background-color: #06060d !important; color: #ffffff !important;
        border-radius: 12px !important; font-weight: 700 !important;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus {
        border-color: #00fff0 !important; box-shadow: 0px 0px 25px rgba(0, 255, 240, 0.5) !important;
    }
    
    /* إلغاء القائمة الجانبية المكررة لمنع تداخل شاشات المالك */
    [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] { display: none !important; }
    
    .stWidgetFormLabel, p, span, label, h1, h2, h3, h4 { 
        font-family: 'Cairo', sans-serif !important; color: #ffffff !important;
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.15) !important;
    }
    /* 🟢 🔴 🟡 تلوين الأزرار الخماسية المتتالية بالترتيب العددي للأعمدة لمنع التشفير العشوائي */
    
    /* 1. الزر الأول (العمود الأول): أخضر نيوني */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div.stButton button {
        color: #00ff66 !important; border: 2px solid #00ff66 !important; box-shadow: 0px 0px 15px rgba(0, 255, 102, 0.2) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div.stButton button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div.stButton button:active {
        background: linear-gradient(135deg, #00ff66 0%, #00ea11 100%) !important; color: #000000 !important;
        box-shadow: 0px 0px 30px #00ff66 !important; border-color: #00ff66 !important;
    }
    /* 2. الزر الثاني (العمود الثاني): أصفر نيوني */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div.stButton button {
        color: #ffaa00 !important; border: 2px solid #ffaa00 !important; box-shadow: 0px 0px 15px rgba(255, 170, 0, 0.2) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div.stButton button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div.stButton button:active {
        background: linear-gradient(135deg, #ffaa00 0%, #ff8800 100%) !important; color: #000000 !important;
        box-shadow: 0px 0px 30px #ffaa00 !important; border-color: #ffaa00 !important;
    }
    /* 3. الزر الثالث (العمود الثالث): أحمر نيوني */
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) div.stButton button {
        color: #ff0055 !important; border: 2px solid #ff0055 !important; box-shadow: 0px 0px 15px rgba(255, 0, 85, 0.2) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) div.stButton button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) div.stButton button:active {
        background: linear-gradient(135deg, #ff0055 0%, #ff0000 100%) !important; color: #ffffff !important;
        box-shadow: 0px 0px 30px #ff0055 !important; border-color: #ff0055 !important;
    }
    /* 4. الزر الرابع (العمود الرابع): بنفسجي نيوني */
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) div.stButton button {
        color: #ff00ff !important; border: 2px solid #ff00ff !important; box-shadow: 0px 0px 15px rgba(255, 0, 255, 0.2) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) div.stButton button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) div.stButton button:active {
        background: linear-gradient(135deg, #ff00ff 0%, #cc00cc 100%) !important; color: #ffffff !important;
        box-shadow: 0px 0px 30px #ff00ff !important; border-color: #ff00ff !important;
    }
    /* 5. الزر الخامس (العمود الخامس): برتقالي ناري */
    div[data-testid="stHorizontalBlock"] > div:nth-child(5) div.stButton button {
        color: #ff4500 !important; border: 2px solid #ff4500 !important; box-shadow: 0px 0px 15px rgba(255, 69, 0, 0.2) !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(5) div.stButton button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(5) div.stButton button:active {
        background: linear-gradient(135deg, #ff4500 0%, #ff2200 100%) !important; color: #ffffff !important;
        box-shadow: 0px 0px 30px #ff4500 !important; border-color: #ff4500 !important;
    }
    /* # === تأثيرات التوهج والأنيميشن لعدادات المالك === */
    @keyframes hudPulse {
        0% { box-shadow: 0px 0px 20px rgba(0, 255, 240, 0.25); border-color: #00fff0; }
        50% { box-shadow: 0px 0px 35px rgba(0, 255, 240, 0.55); border-color: #00ffaa; }
        100% { box-shadow: 0px 0px 20px rgba(0, 255, 240, 0.25); border-color: #00fff0; }
    }
    @keyframes hudIntro {
        0% { opacity: 0; transform: scale(0.96); }
        100% { opacity: 1; transform: scale(1); }
    }
    div[data-testid="stMetricBlock"], div[data-testid="metric-container"], .premium-card-cyan, .premium-card-pink {
        animation: hudIntro 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards, hudPulse 4s ease-in-out infinite alternate !important;
    }
    div[data-testid="stMetricBlock"] [data-testid="stMetricValue"], div[data-testid="metric-container"] .stMetricValue {
        text-shadow: 0px 0px 15px rgba(0, 255, 240, 0.6) !important;
        font-weight: 900 !important;
    }
    /* ========================================================
       [القسم الثالث]: # === جدار الأنيميشن الموحد والانبثاق الميكانيكي لكافة عناصر المنصة ===
       ======================================================== */
    
    /* 1. جدار الانسياب الشامل لكافة العناصر الحية بالموقع */
    button, input, select, textarea, div.stDataFrame, table, .stSelectbox, [data-testid="stSidebar"] {
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    }

    /* 2. بناء التمدد والانجذاب السينمائي المرن عند الولادة */
    @keyframes elasticPop {
        0% {
            opacity: 0;
            transform: translateY(12px) scale(0.95);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    @keyframes alertPulseRed {
        0% { box-shadow: 0px 0px 12px rgba(255, 0, 85, 0.25); border-color: #ff0055; }
        50% { box-shadow: 0px 0px 25px rgba(255, 0, 85, 0.6); border-color: #ff3377; }
        100% { box-shadow: 0px 0px 12px rgba(255, 0, 85, 0.25); border-color: #ff0055; }
    }
    @keyframes alertPulseGold {
        0% { box-shadow: 0px 0px 12px rgba(255, 170, 0, 0.25); border-color: #ffaa00; }
        50% { box-shadow: 0px 0px 25px rgba(255, 170, 0, 0.6); border-color: #ffcc33; }
        100% { box-shadow: 0px 0px 12px rgba(255, 170, 0, 0.25); border-color: #ffaa00; }
    }
    @keyframes alertPulseGreen {
        0% { box-shadow: 0px 0px 12px rgba(0, 255, 102, 0.25); border-color: #00ff66; }
        50% { box-shadow: 0px 0px 25px rgba(0, 255, 102, 0.6); border-color: #33ff99; }
        100% { box-shadow: 0px 0px 12px rgba(0, 255, 102, 0.25); border-color: #00ff66; }
    }

    /* استهداف جدار الـ DOM بالكامل لفرض انبثاق مرن للأزرار وحقول الإدخال ورسائل التنبيه والتحذيرات */
    div[data-testid="stNotification"], div[data-testid="stAlert"], div.element-container:has(div[data-testid="stNotification"]), div.stAlert, div.stButton, div[data-testid="stTextInput"] {
        animation: elasticPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards !important;
    }

    /* صناديق الأخطاء والتوثيق الفاشل st.error بالتوهج النبضي الأحمر النيوني */
    div[data-testid="stAlert"]:has(div[data-baseinstance="error"]), div.stAlert:has([aria-label="Error"]) {
        border: 2px solid #ff0055 !important;
        background: linear-gradient(135deg, rgba(20, 2, 10, 0.92) 0%, rgba(5, 1, 3, 0.99) 100%) !important;
        animation: elasticPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, alertPulseRed 3s ease-in-out infinite alternate !important;
    }

    /* صناديق التحذيرات st.warning بالتوهج النبضي الذهبي الدافئ للسرية التامة */
    div[data-testid="stAlert"]:has(div[data-baseinstance="warning"]), div.stAlert:has([aria-label="Warning"]) {
        border: 2px solid #ffaa00 !important;
        background: linear-gradient(135deg, rgba(20, 12, 2, 0.92) 0%, rgba(5, 3, 1, 0.99) 100%) !important;
        animation: elasticPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, alertPulseGold 3s ease-in-out infinite alternate !important;
    }

    /* صناديق التوثيق الناجح st.success بالتوهج النبضي الأخضر السيبراني الرائع */
    div[data-testid="stAlert"]:has(div[data-baseinstance="success"]), div.stAlert:has([aria-label="Success"]) {
        border: 2px solid #00ff66 !important;
        background: linear-gradient(135deg, rgba(2, 20, 10, 0.92) 0%, rgba(1, 5, 2, 0.99) 100%) !important;
        animation: elasticPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, alertPulseGreen 3s ease-in-out infinite alternate !important;
    }
    </style>
""", unsafe_allow_html=True)
# ========================================================
# [القسم الرابع]: إدارة ومزامنة جدول قاعدة بيانات الـ Auth وجدار الحماية الاستباقي للثغرات
# ========================================================

# صياغة ومزامنة جدول الـ Auth لقراءة كلمات سر المشتركين في نفس الحاوية الموحدة حياً
db_conn = sqlite3.connect("saas_security_vault.db", timeout=10)
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS saas_users_auth (
        email TEXT PRIMARY KEY, password TEXT, status TEXT, package TEXT
    )
""")
db_conn.commit()

# [إصلاح الثغرة الذكية]: منع حقن الحساب الافتراضي تلقائياً إذا قام المالك بحذفه يدوياً
db_cursor.execute("SELECT COUNT(*) FROM saas_users_auth WHERE email = 'daymaabdaalhmdllh@gmail.com'")
account_exists = db_cursor.fetchone()
if account_exists[0] == 0 and "destroyed_flag" not in st.session_state:
    db_cursor.execute("INSERT OR IGNORE INTO saas_users_auth VALUES ('daymaabdaalhmdllh@gmail.com', '123456', '🟢 مفعّل ونشط', 'الباقة السيبرانية الخارقة')")
    db_conn.commit()
db_conn.close()

# دالة التدمير الفوري لأي حساب في قاعدة البيانات دون إعطاب الاتصالات المفتوحة حياً
def delete_email_completely(email_to_delete):
    try:
        conn = sqlite3.connect("saas_security_vault.db", timeout=10)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saas_users_auth WHERE email = ?", (email_to_delete,))
        conn.commit(); conn.close()
        return True
    except Exception as e:
        st.error(f"⚠️ خطأ ميكانيكي أثناء الحذف: {e}"); return False

# === الإضافات والتعديلات الجديدة ===
# جاهز ومؤمن بالكامل هنا لاستقبال أي ميزات إضافية في المحادثات القادمة...


# ====================================================================
# === الإضافات والتعديلات الجديدة لبوابة التوثيق وأمن المشتركين ===
# ====================================================================
import streamlit as st
import sqlite3
import time
import re

# ====================================================================
# === الإضافات والتعديلات الجديدة لبوابة التوثيق وأمن المشتركين ===
# ====================================================================

def render_premium_neon_packages():
    """
    تقوم هذه الدالة بتنفيذ ميكانيكية الهولوغرام الفاخرة (Holographic Phase-In Effect)،
    حيث تعكس بدقة التحديث الشامل لمستويات الباقات السلوية ومميزاتها الفنية،
    لتنبثق الباقة المختارة وحدها من العدم بناءً على رادار اختيار التاجر الحي.
    """
    # 1. قراءة الاختيار الحي من عنصر الراديو المعتمد تلقائياً
    current_choice = st.session_state.get("selected_neon_package", "الباقة الأساسية المبتدئة (29k)")

    # 2. توليد فئات الحالة الهولوغرامية الديناميكية للباقات الثلاث
    phase_cyber = "hologram-visible" if "السيبرانية" in current_choice else "hologram-hidden"
    phase_pro = "hologram-visible" if "الاحترافية" in current_choice else "hologram-hidden"
    phase_basic = "hologram-visible" if "الأساسية" in current_choice else "hologram-hidden"

    # 3. حقن قواعد الهندسة الحركية والـ CSS السينمائي والميزات المحدثة للشركات
    st.markdown(f"""
        <style>
        .hologram-card {{
            transform: translateY(20px);
            transition: max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1), 
                        opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1), 
                        transform 0.5s cubic-bezier(0.4, 0, 0.2, 1),
                        border 0.5s ease-in-out,
                        box-shadow 0.5s ease-in-out;
            overflow: hidden;
            border-radius: 14px;
        }}
        
        .hologram-hidden {{
            max-height: 0px !important;
            opacity: 0 !important;
            transform: translateY(20px) scale(0.95);
            padding: 0px !important;
            margin: 0px !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            pointer-events: none;
        }}
        
        .hologram-visible {{
            max-height: 800px !important; /* ارتفاع متسع لانسكاب الخدمات المحدثة بالكامل */
            opacity: 1 !important;
            transform: translateY(0px) scale(1);
            background: rgba(0, 255, 240, 0.05);
            border: 1px solid rgba(0, 255, 240, 0.6);
            padding: 18px;
            margin-bottom: 15px;
            box-shadow: 0 0 25px rgba(0, 255, 240, 0.2);
        }}
        
        .holo-title {{
            color: #00fff0;
            font-weight: 900;
            font-size: 17px;
            margin-bottom: 6px;
            text-shadow: 0 0 15px rgba(0, 255, 240, 0.5);
        }}
        .holo-price {{
            color: #ffffff;
            font-weight: 700;
            font-size: 15px;
            margin-bottom: 10px;
            border-bottom: 1px solid rgba(0, 255, 240, 0.2);
            padding-bottom: 6px;
        }}
        .holo-feat {{
            color: #e0e0e0;
            font-size: 13px;
            margin: 5px 0;
            padding-right: 5px;
            line-height: 1.5;
        }}
        </style>
        
        <!-- باقة 1: الأساسية المبتدئة -->
        <div class='hologram-card {phase_basic}'>
            <div class='holo-title'>🌱 الباقة الأساسية المبتدئة (29k)</div>
            <div class='holo-price'>💰 السعر السنوي: 29,000 DA</div>
            <div class='holo-feat'>✓ إصدار فواتير الزبائن الكبيرة (A4) والملصقات الحرارية اللحظية.</div>
            <div class='holo-feat'>✓ إرسال سريع للفاتورة وتفاصيل الطلب عبر WhatsApp للزبائن يدويًا.</div>
            <div class='holo-feat'>✓ مستودع سلع مبسط لإضافة المنتجات ومراقبة الكميات المتوفرة.</div>
            <div class='holo-feat'>✓ 🔒 قفل المساعد الجانبي الذكي (يفتح الردود العامة فقط ويحظر ميزات الـ AI المتقدمة).</div>
        </div>
        
        <!-- باقة 2: الاحترافية المتوسطة -->
        <div class='hologram-card {phase_pro}'>
            <div class='holo-title'>💎 الباقة الاحترافية المتوسطة (45k)</div>
            <div class='holo-price'>💰 السعر السنوي: 45,000 DA</div>
            <div class='holo-feat'><b>✓ تشمل كافة ميزات الباقة الأساسية المبتدئة بالكامل.</b></div>
            <div class='holo-feat'>✓ 🔥 مؤشر المخزون الناري الذكي: تنبيهات بصرية متحركة عند نفاذ السلع (أقل من 5 قطع).</div>
            <div class='holo-feat'>✓ 🧼 مطهر ملفات المبيعات: رفع وتطهير ملفات Excel من التكرارات والأسعار السالبة.</div>
            <div class='holo-feat'>✓ 🗺️ رادار المبيعات الجغرافي: مخطط بياني حي لفرز الولايات الجزائرية الأكثر مبيعاً لشحن آمن.</div>
            <div class='holo-feat'>✓ 🤖 فتح ذكاء المساعد الجانبي المتوسط: تقديم نصائح وحلول لمشاكل الشحن والـ Retour وتثبيت الكليون.</div>
        </div>
        
        <!-- باقة 3: السيبرانية الخارقة -->
        <div class='hologram-card {phase_cyber}'>
            <div class='holo-title'>⚡ الباقة السيبرانية الخارقة (65k)</div>
            <div class='holo-price'>💰 السعر السنوي: 65,000 DA</div>
            <div class='holo-feat'><b>✓ تشمل كافة ميزات الباقتين السابقتين بالكامل (العقل الشامل للمنصة).</b></div>
            <div class='holo-feat'>✓ 🚀 منصة الأتمتة الإعلانية الكاملة (AI Hub): صياغة الإعلانات التلقائية بـ 3 لهجات مختلفة فوراً.</div>
            <div class='holo-feat'>✓ 🎬 صانع سيناريوهات الفيديو بالثواني: خطة إنتاج كاملة لتصوير فيديوهات TikTok و Reels للسلع.</div>
            <div class='holo-feat'>✓ 📊 عداد تقييم قوة الإعلان الفوري (AI Ad Score Meter) لتحليل جاذبية المنشور قبل إطلاقه.</div>
            <div class='holo-feat'>✓ 💰 حاسبة الـ ROI وميزانية الفحص الموازية بالدولار وما يقابلها بالدينار الجزائري (Square).</div>
            <div class='holo-feat'>✓ 🧠 العقل الخارق للمساعد الجانبي: إجابات استخباراتية فورية عن استهدافات فيسبوك وهاشتاغات تيك توك وحصانة ضد الخربشة.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # أزرار الراديو النقية لمزامنة الميكانيكية الحركية وتمرير الاختيار بدقة
    chosen_package = st.radio(
        "اختر فئة الباقة السنوية لمتجرك لتفعيل عرض مميزاتها فوراً:",
        ["الباقة الأساسية المبتدئة (29k)", "الباقة الاحترافية المتوسطة (45k)", "الباقة السيبرانية الخارقة (65k)"],
        key="selected_neon_package"
    )
    return chosen_package

def validate_and_process_registration(email, password):
    """
    ممر الأمان الذكي المكون من 3 طبقات فحص صارمة لمنع حقن البيانات العشوائية وحظر الحسابات المتكررة.
    """
    if email == "" or password == "":
        st.error("⚠️ يرجى ملء حقول البريد وكلمة السر أولاً!")
        return None
        
    # 1. جدار التحقق من صيغة البريد (Email Format Guard)
    email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if not re.match(email_pattern, email):
        st.warning("⚠️ يرجى كتابة بريد إلكتروني منطقي وصحيح ينتهي بـ @gmail.com")
        return None
        
    # 2. قوة كلمة المرور (Password Strength Check)
    if len(password) < 6:
        st.warning("⚠️ يجب أن تحتوي كلمة السر على 6 حروف أو أكثر لحماية متجرك")
        return None
        
    # 3. منع تكرار الحسابات (Unique Email Guard)
    try:
        conn_check = sqlite3.connect("saas_security_vault.db", timeout=10)
        cursor_check = conn_check.cursor()
        cursor_check.execute("SELECT email FROM saas_users_auth WHERE email = ?", (email,))
        existing_user = cursor_check.fetchone()
        conn_check.close()
        
        if existing_user:
            st.error("❌ هذا البريد الإلكتروني مسجل مسبقاً في رادار المنصة السحابية!")
            return None
    except Exception as e:
        st.error(f"❌ خطأ في فحص جدار الأمان: {str(e)}")
        return None
        
    return st.session_state.get("selected_neon_package", "الباقة الأساسية المبتدئة (29k)")
# ========================================================
# الجزء الثاني: مركز توثيق هوية التاجر وعزل البوابات (auth_gate.py)
# ========================================================




if not is_boss_link and "active_merchant_user" not in st.session_state:
    
    # 📢 (1) إذا اختار التاجر صفحة الشكاوى المستقلة
    if st.session_state.get("current_view") == "complaint_page":
        
        st.markdown("""
            <style>
            @keyframes mechanicalPop {
                0% { opacity: 0; transform: translateY(20px) scale(0.95); }
                60% { opacity: 1; transform: translateY(-3px) scale(1.01); }
                100% { opacity: 1; transform: translateY(0) scale(1); }
            }
            .mechanical-box {
                animation: mechanicalPop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
                border: 2px solid #ff0055;
                border-radius: 20px;
                padding: 30px;
                background: linear-gradient(135deg, rgba(20, 5, 12, 0.96) 0%, rgba(5, 1, 3, 0.99) 100%);
                box-shadow: 0 0 35px rgba(255, 0, 85, 0.4);
                direction: rtl;
                text-align: right;
                max-width: 600px;
                margin: 30px auto;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<h1 style='color: #ff0055; text-align: center; margin-top: 20px; font-weight: 900;'>📢 منصة تسجيل الشكاوى والبلاغات الرسمية</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #aaa; font-size: 14px;'>املأ النموذج أدناه لتسجيل شكواك وسنرد عليك في أقرب وقت.</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='mechanical-box'>", unsafe_allow_html=True)
        
        c_email = st.text_input("البريد الإلكتروني الخاص بك:", key="comp_email_input")
        c_phone = st.text_input("رقم الهاتف:", key="comp_phone_input", placeholder="0655xxxxxxxx")
        c_msg = st.text_area("تفاصيل الشكوى أو المشكلة:", key="comp_msg_input", placeholder="اكتب شكواك هنا...")
        
        if st.button("📤 إرسال الشكوى للإدارة", key="send_comp_action_btn"):
            if not c_email or not c_phone or not c_msg:
                st.error("⚠️ يرجى تعبئة جميع الحقول أولاً.")
            else:
                admin_subject = f"🚨 شكوى جديدة من: {c_email}"
                admin_body = f"البريد: {c_email}\nالهاتف: {c_phone}\n\nتفاصيل الشكوى:\n{c_msg}"
                send_gmail_notification_with_log(st.secrets.get("GMAIL_USER", "admin@nexus.com"), admin_subject, admin_body, action_type="LOCK")
                st.success("✅ تم إرسال شكواك بنجاح للإدارة!")
                time.sleep(2)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ العودة إلى صفحة تسجيل الدخول", key="back_to_auth_btn"):
            st.session_state["current_view"] = "auth"
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

    # 🔑 (2) صفحة التسجيل والدخول الأصلية (تظهر وحدها ولا تظهر الشكاوى معها)
    else:
        st.markdown("<h1 style='color: #00fff0; text-align: center; font-weight:900; margin-top: 40px; text-shadow: 0 0 20px #00fff0; font-size:32px;'>🔐 بوابة التوثيق والاشتراكات السنوية المتكاملة</h1>", unsafe_allow_html=True)
        
        col_side_left, col_center_box, col_side_right = st.columns(3)
        with col_center_box:
            st.markdown("<div class='premium-card-cyan'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#ffffff; text-align:center; font-weight:700; margin-top:0;'>مركز توثيق هوية التاجر</h3>", unsafe_allow_html=True)
            
            auth_mode = st.radio("اختر العملية المطلوبة للتوثيق الآمن لمتجرك:", ["🔑 تسجيل الدخول للحساب الحالي", "📝 إنشاء حساب تاجر جديد فريش"])
            st.markdown("<hr style='border-color: rgba(0, 255, 240, 0.15); margin: 15px 0;'>", unsafe_allow_html=True)
            
            input_email = st.text_input("أدخل البريد الإلكتروني الخاص بك:", key="merchant_em")
            input_password = st.text_input("أدخل كلمة المرور السرية من اختيارك:", type="password", key="merchant_pw")
            input_phone = st.text_input("📱 أدخل رقم الهاتف الخاص بك:", placeholder="مثال: 0655xxxxxxxx", key="merchant_phone").strip()
            
            # 🛑 التحقق من صحة رقم الهاتف (منع الحروف والتأكد من الطول)
            if input_phone:
                check_phone = input_phone.replace("+", "").strip()
            
                if not check_phone.isdigit():
                    st.error("❌ خطأ: يرجى إدخال أرقام صحيحة فقط في حقل الهاتف (بدون أحرف أو رموز خاصة).")
                elif len(check_phone) < 9:
                    st.warning("⚠️ تنبيه: رقم الهاتف قصير جداً، تأكد من إدخال الرقم كاملاً.")
                else:
                    st.session_state["temp_reg_phone"] = input_phone
            
            clean_email = input_email.strip()
            clean_pass = input_password.strip()
            st.session_state["temp_reg_phone"] = input_phone
            
            if auth_mode == "📝 إنشاء حساب تاجر جديد فريش":
                user_package_choice = render_premium_neon_packages()
                st.markdown("</div>", unsafe_allow_html=True)
                
                if "otp_pending_verification" not in st.session_state:
                    st.session_state["otp_pending_verification"] = False

                if not st.session_state["otp_pending_verification"]:
                    if st.button("📝 إرسال رمز التحقق (OTP) إلى بريدك"):
                        
                        # 🛑 شرط إضافي صارم: التأكد من وجود رقم هاتف وعدم وجود خطأ في طوله
                        raw_phone = st.session_state.get("temp_reg_phone", "").replace("+", "").strip()
                        
                        if not input_phone:
                            st.error("⚠️ يرجى إدخال رقم الهاتف أولاً!")
                        elif not raw_phone.isdigit() or len(raw_phone) < 9:
                            st.error("❌ لا يمكن إرسال الرمز: رقم الهاتف المدخل قصير أو غير صحيح. يرجى تصحيحه أولاً.")
                        else:
                            validated_package = validate_and_process_registration(clean_email, clean_pass)
                            if validated_package:
                                generated_otp = f"{random.randint(100000, 999999)}"
                                st.session_state["temp_reg_otp"] = generated_otp
                                st.session_state["temp_reg_email"]  = clean_email
                                st.session_state["temp_reg_pass"]   = clean_pass
                                st.session_state["temp_reg_package"] = validated_package
                                
                                subject = "رمز التحقق (OTP) لإنشاء حساب متجرك الجديد"
                                body = f"مرحباً بك،\n\nرمز التحقق العشوائي الخاص بك هو: {generated_otp}\n\nيرجى إدخاله في التطبيق لإتمام إنشاء الحساب."
                                
                                if send_gmail_notification(clean_email, subject, body):
                                    st.session_state["otp_pending_verification"] = True
                                    st.success(f"📬 تم إرسال رمز التحقق بنجاح إلى البريد: {clean_email}")
                                    time.sleep(0.5)
                                    st.rerun()

                else:
                    if "otp_countdown" not in st.session_state:
                        st.session_state["otp_countdown"] = 60

                    st.markdown("""
                        <style>
                        .otp-modal-container {
                            max-width: 500px;
                            margin: 20px auto;
                            background: linear-gradient(135deg, #0d0d21 0%, #05050c 100%);
                            border: 2px solid #00fff0;
                            border-radius: 20px;
                            padding: 30px;
                            box-shadow: 0 0 40px rgba(0, 255, 240, 0.4);
                            direction: rtl;
                            text-align: right;
                        }
                        div[data-testid="stTextInput"] input {
                            text-align: center !important;
                            font-size: 28px !important;
                            letter-spacing: 15px !important;
                            font-weight: 900 !important;
                            color: #00fff0 !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)

                    target_mail = st.session_state.get('temp_reg_email', 'البريد الإلكتروني')

                    st.markdown(f"""
                        <div class="otp-modal-container">
                            <h3 style="color: #00fff0; text-align: center; margin-top: 0; font-weight: 900;">🔐 تحقق الأمان</h3>
                            <p style="color: #e0e0e0; font-size: 14px; text-align: center; margin-bottom: 15px;">
                                تم إرسال رمز التحقق (OTP) إلى بريدك الإلكتروني:<br>
                                <span style="color: #ff00ff; font-weight: bold;">{target_mail}</span>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                    entered_otp = st.text_input(
                        "أدخل الرمز المكون من 6 أرقام هنا:", 
                        max_chars=6, 
                        placeholder="------", 
                        key="smart_otp_paste_input"
                    )

                    if st.session_state["otp_countdown"] > 0:
                        st.markdown(f"<p style='text-align: center; color: #ffaa00; font-size: 14px; font-weight: bold; margin: 10px 0;'>⏳ إعادة إرسال الرمز خلال: {st.session_state['otp_countdown']} ثانية</p>", unsafe_allow_html=True)
                    else:
                        if st.button("🔄 إعادة إرسال الرمز الجديد", key="resend_otp_btn"):
                            generated_otp = f"{random.randint(100000, 999999)}"
                            st.session_state["temp_reg_otp"] = generated_otp
                            st.session_state["otp_countdown"] = 60
                            
                            subject = "رمز التحقق (OTP) الجديد لإنشاء حساب متجرك"
                            body = f"مرحباً بك،\n\nرمز التحقق الجديد الخاص بك هو: {generated_otp}\n\nيرجى إدخاله في التطبيق."
                            if send_gmail_notification(target_mail, subject, body, action_type="OTP"):
                                st.success("📬 تم إعادة إرسال رمز جديد بنجاح!")
                                time.sleep(0.5)
                                st.rerun()

                    st.markdown("<p style='text-align: center; color: #888899; font-size: 12px;'>💡 يمكنك نسخ الرمز من بريدك واللصق هنا مباشرة ليتم تعبئته تلقائياً.</p>", unsafe_allow_html=True)

                    col_verify_btn, col_cancel_btn = st.columns(2)
                    with col_verify_btn:
                        if st.button("✅ تأكيد الرمز وحفظ الحساب للإدارة", key="verify_otp_submit_btn"):
                            if entered_otp.strip() == st.session_state.get("temp_reg_otp"):
                                reg_email = st.session_state["temp_reg_email"]
                                reg_pass = st.session_state["temp_reg_pass"]
                                reg_pkg = st.session_state["temp_reg_package"]
                                reg_phone = st.session_state.get("temp_reg_phone", "")
                                reg_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                
                                conn_reg = sqlite3.connect("saas_security_vault.db", timeout=10)
                                cursor_reg = conn_reg.cursor()
                                cursor_reg.execute(
                                    "INSERT OR IGNORE INTO saas_users_auth (email, password, status, package, created_at, phone) VALUES (?, ?, ?, ?, ?, ?)", 
                                    (reg_email, reg_pass, '⏳ في انتظار التفعيل', reg_pkg, reg_time, reg_phone)
                                )
                                conn_reg.commit()
                                conn_reg.close()
                                
                                st.session_state["otp_pending_verification"] = False
                                st.success("🎯 تم التحقق بنجاح وإرسال طلبك للإدارة!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ الرمز غير صحيح، تأكد من إدخال الأرقام الستة بدقة.")
                                
                    with col_cancel_btn:
                        if st.button("❌ إلغاء والعودة", key="cancel_otp_btn"):
                            st.session_state["otp_pending_verification"] = False
                            st.session_state.pop("otp_countdown", None)
                            st.rerun()

                    if st.session_state.get("otp_countdown", 0) > 0:
                        time.sleep(1)
                        st.session_state["otp_countdown"] -= 1
                        st.rerun()
            else:
                st.markdown("</div>", unsafe_allow_html=True)
                if st.button("🔑 تسجيل الدخول إلى المتجر"):
                    if clean_email == "" or clean_pass == "": 
                        st.error("⚠️ يرجى إدخال البريد وكلمة السر!")
                    else:
                        conn_login = sqlite3.connect("saas_security_vault.db", timeout=10)
                        cursor_login = conn_login.cursor()
                        cursor_login.execute("SELECT status FROM saas_users_auth WHERE email = ? AND password = ?", (clean_email, clean_pass))
                        user_status_row = cursor_login.fetchone()
                        conn_login.close()
                        
                        if user_status_row:
                            if "🟢 مفعّل ونشط" in user_status_row:
                                st.session_state["active_merchant_user"] = clean_email
                                st.success("🔓 تم التحقق بنجاح! جاري فتح متجرك...")
                                time.sleep(0.5); st.rerun()
                            else:
                                st.warning(f"⏳ حالة حسابك الحالية: {user_status_row}")
                        else:
                            st.error("❌ بيانات الدخول غير مطابقة لملف الأمان السحابي.")
            
            # 📢 زر الانتقال إلى صفحة الشكاوى المستقلة (موضع آمن في أسفل الصندوق الأوسط)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📢 تسجيل شكوى أو بلاغ جديد", key="go_to_complaint_page_btn"):
                st.session_state["current_view"] = "complaint_page"
                st.rerun()
                
            st.markdown("</div>", unsafe_allow_html=True)
# ========================================================
# الجزء الثالث المصحح سيبرانياً: غرفة المالك ورادار الموافقات الخماسي (auth_gate.py) - [الجزء 1]
# ========================================================
import streamlit as st
import sqlite3
import pandas as pd
import math
import time
from datetime import datetime

# ========================================================
# 🛠️ الدوال المستقلة لتحديثات لوحة التحكم (KPIs, البحث, الصفحات)
# ========================================================

def calculate_actual_revenue(df_users):
    """
    حساب الإيرادات السنوية الفعلية بناءً على فئة باقة كل تاجر نشط:
    - الباقة الأساسية: 29,000 DA
    - الباقة الاحترافية: 45,000 DA
    - الباقة السيبرانية: 65,000 DA
    """
    if df_users.empty or 'package' not in df_users.columns:
        return 0
    
    total_rev = 0
    for _, row in df_users.iterrows():
        # نتحقق من التاجر إذا كان حسابه مفعّلاً ونشطاً
        status_str = str(row.get('status', ''))
        if 'مفعّل' in status_str:
            pkg = str(row.get('package', ''))
            if '29k' in pkg or 'الأساسية' in pkg:
                total_rev += 29000
            elif '65k' in pkg or 'السيبرانية' in pkg:
                total_rev += 65000
            else:
                # الباقة الاحترافية أو الافتراضي عند التفعيل
                total_rev += 45000
    return total_rev

def render_boss_kpis_and_filters(df_users):
    """
    1. عرض 3 بطاقات إحصائية أنيقة في أعلى اللوحة.
    2. إتاحة شريط البحث وقائمة التصفية وإعادة البيانات المفلترة.
    """
    st.markdown("<h2 style='color: #00fff0; text-align: right; font-weight:900; direction:rtl;'>📊 لوحة العدادات المالية والمؤشرات الحية (The Boss Revenue HUD)</h2>", unsafe_allow_html=True)
    
    # حساب الأرقام الإحصائية
    total_active = len(df_users[df_users['status'].str.contains('مفعّل', na=False)]) if not df_users.empty and 'status' in df_users.columns else 0
    total_banned = len(df_users[df_users['status'].str.contains('قفل|مصادرة|محظور', na=False)]) if not df_users.empty and 'status' in df_users.columns else 0
    total_trial = len(df_users[df_users['status'].str.contains('انتظار|معلّق|مهلة|تجربة', na=False)]) if not df_users.empty and 'status' in df_users.columns else 0
    
    actual_revenue = calculate_actual_revenue(df_users)
    
    # 💳 عرض البطاقات الإحصائية الثلاث الأنيقة
    hud_col1, hud_col2, hud_col3 = st.columns(3)
    with hud_col1:
        st.markdown(f"<div style='border:2px solid #00fff0; border-radius:15px; padding:20px; text-align:center; background:rgba(5,15,20,0.85); box-shadow: 0px 0px 20px rgba(0, 255, 240, 0.25); direction:rtl;'><h4 style='color:#00fff0; margin:0;'>👤 التجار (النشطون / المحظورون)</h4><h2>{total_active} نشط | {total_banned} محظور</h2></div>", unsafe_allow_html=True)
    with hud_col2:
        st.markdown(f"<div style='border:2px solid #ffaa00; border-radius:15px; padding:20px; text-align:center; background:rgba(15,10,5,0.85); box-shadow: 0px 0px 20px rgba(255, 170, 0, 0.25); direction:rtl;'><h4 style='color:#ffaa00; margin:0;'>💰 الإيرادات السنوية الفعلية</h4><h2>{actual_revenue:,} DA</h2></div>", unsafe_allow_html=True)
    with hud_col3:
        st.markdown(f"<div style='border:2px solid #ff00ff; border-radius:15px; padding:20px; text-align:center; background:rgba(20,5,20,0.85); box-shadow: 0px 0px 20px rgba(255, 0, 255, 0.25); direction:rtl;'><h4 style='color:#ff00ff; margin:0;'>🧪 الحسابات التجريبية والانتظار</h4><h2>{total_trial} حساب</h2></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 🔍 شريط البحث والتصفية فوق البطاقات
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        search_query = st.text_input("🔍 البحث بالبريد الإلكتروني:", placeholder="اكتب بريد التاجر للبحث السريع...", key="boss_search_input").strip().lower()
    with filter_col2:
        status_filter = st.selectbox("📌 تصفية حسب حالة الحساب:", ["الكل", "مفعّل", "في انتظار التفعيل", "محظور"], key="boss_status_filter")

    # تطبيق الفلترة والتصفية
    filtered_df = df_users.copy()
    if not filtered_df.empty:
        if search_query:
            filtered_df = filtered_df[filtered_df['email'].str.lower().str.contains(search_query, na=False)]
        
        if status_filter == "مفعّل":
            filtered_df = filtered_df[filtered_df['status'].str.contains('مفعّل', na=False)]
        elif status_filter == "في انتظار التفعيل":
            filtered_df = filtered_df[filtered_df['status'].str.contains('انتظار|معلّق|مهلة', na=False)]
        elif status_filter == "محظور":
            filtered_df = filtered_df[filtered_df['status'].str.contains('قفل|مصادرة|محظور', na=False)]

    return filtered_df

def paginate_dataframe(filtered_df, page_size=10):
    """
    تقسيم عرض بطاقات التجار إلى صفحات (10 تجار كحد أقصى في كل صفحة) مع أزرار التنقل.
    """
    if filtered_df.empty:
        return filtered_df, 1, 1
    
    total_items = len(filtered_df)
    total_pages = math.ceil(total_items / page_size)
    
    if "boss_current_page" not in st.session_state:
        st.session_state["boss_current_page"] = 1
        
    if st.session_state["boss_current_page"] > total_pages:
        st.session_state["boss_current_page"] = max(1, total_pages)
        
    current_page = st.session_state["boss_current_page"]
    
    # 📄 أزرار وشريط التنقل بين الصفحات
    if total_pages > 1:
        p_col1, p_col2, p_col3 = st.columns([1, 2, 1])
        with p_col1:
            if st.button("⬅️ الصفحة السابقة", key="prev_page_btn") and current_page > 1:
                st.session_state["boss_current_page"] -= 1
                st.rerun()
        with p_col2:
            st.markdown(f"<p style='text-align: center; color: #00fff0; font-weight: bold; margin-top: 5px;'>الصفحة {current_page} من {total_pages} (إجمالي النتائج: {total_items})</p>", unsafe_allow_html=True)
        with p_col3:
            if st.button("الصفحة التالية ➡️", key="next_page_btn") and current_page < total_pages:
                st.session_state["boss_current_page"] += 1
                st.rerun()
                
    start_idx = (current_page - 1) * page_size
    end_idx = start_idx + page_size
    return filtered_df.iloc[start_idx:end_idx], current_page, total_pages

def render_neon_license_ring(email, days_left):
    """
    توليد حلقة نيوني متغيرة الحجم واللون رادارياً لتراخيص 7 أيام.
    """
    clamped_days = max(0, min(7, days_left))
    percentage = clamped_days / 7.0
    total_circumference = 113
    stroke_offset = total_circumference * (1 - percentage)
    
    if clamped_days > 4:
        glow_color = "#ffaa00"
    elif clamped_days > 2:
        glow_color = "#ff5500"
    else:
        glow_color = "#ff0055"
        
    html_template = f"""
    <div style='display: flex; align-items: center; justify-content: space-between; padding: 12px; background: rgba(5,5,15,0.6); border-radius: 8px; margin-bottom: 8px; border-left: 4px solid {glow_color}; direction: rtl; text-align: right;'>
        <div style='display: flex; align-items: center; gap: 15px;'>
            <svg width="45" height="45" viewBox="0 0 45 45" style="transform: rotate(-90deg); filter: drop-shadow(0px 0px 6px {glow_color});">
                <circle cx="22.5" cy="22.5" r="18" stroke="rgba(255,255,255,0.1)" stroke-width="3" fill="transparent" />
                <circle cx="22.5" cy="22.5" r="18" stroke="{glow_color}" stroke-width="3.5" fill="transparent" 
                        stroke-dasharray="{total_circumference}" stroke-dashoffset="{stroke_offset}" stroke-linecap="round" />
            </svg>
            <span style='color:#ffffff; font-size: 15px;'>⚠️ التاجر: <span style='color: #00fff0;'>{email}</span></span>
        </div>
        <span style='color:{glow_color}; font-weight:bold; font-size: 14px;'>متبقي: {days_left} أيام فقط!</span>
    </div>
    """
    return html_template

# ========================================================
# 👑 الجزء الثالث المصحح سيبرانياً: غرفة المالك ورادار الموافقات الخماسي (auth_gate.py)
# ========================================================
if is_boss_link:
    # تأمين وحقن الهوية علوياً لمنع خطأ NameError
    ADMIN_USERNAME = "admin_master_v4"
    ADMIN_PASSWORD = "SaasPassword2026"
    
    # 🔒 [المستوى الأول]: إذا لم يسجل المالك دخوله، تظهر لوحة الحماية فقط وتُحجب العدادات كلياً
    if not st.session_state.get("admin_master_logged", False):
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='centered-box-container' style='max-width: 500px; margin: 60px auto 20px auto; padding: 40px; background: rgba(5, 5, 15, 0.95); border: 2px solid #00fff0; border-radius: 20px; box-shadow: 0px 0px 40px rgba(0, 255, 240, 0.35); direction: rtl; text-align: right; backdrop-filter: blur(15px);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #ff00ff; text-align: center; font-weight: 900; margin-top: 0;'>🔒 غرفة السيادة الكبرى والموافقات السحابية</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #ffffff; text-align: center; font-size: 15px; margin-bottom: 25px;'>🔑 تسجيل دخول المالك الأعلى للوصول للرادار</p>", unsafe_allow_html=True)
        
        boss_user = st.text_input("User:", key="boss_leader_user").strip()
        boss_pass = st.text_input("Password:", type="password", key="boss_leader_pass").strip()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("⚙️ صعود وتفعيل خادم التحكم الأعلى", key="submit_boss_login_btn"):
            if boss_user == ADMIN_USERNAME and boss_pass == ADMIN_PASSWORD:
                st.session_state["admin_master_logged"] = True
                st.toast("👑 مرحباً بك يا قائد! تم تفعيل لوحة السيادة والموافقات.", icon="🔓")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ بيانات خاطئة! يرجى إعادة التحقق من مفاتيح الأمان السحابية.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 👑 [المستوى الثاني مقفل ومحمي]: تنبثق العدادات والرادار هنا حصرياً وفقط بعد نجاح تسجيل الدخول
    else:
        st.markdown("<h1 style='color: #ffffff; text-align: center; font-weight:900; text-shadow: 0 0 25px #00fff0;'>👑 غرفة المالك والسيادة العليا v4</h1>", unsafe_allow_html=True)
        
        # 1️⃣ قراءة بيانات قاعدة البيانات بالكامل
        conn_hud = sqlite3.connect("saas_security_vault.db", timeout=10)
        try:
            total_merchants_query = pd.read_sql("SELECT * FROM saas_users_auth", conn_hud)
        except Exception:
            total_merchants_query = pd.DataFrame(columns=['email', 'password', 'status', 'package'])
        conn_hud.close()
        
        # 2️⃣ تشغيل دالة لوحة المؤشرات الحية المحدثة وشريط البحث والتصفية
        filtered_merchants_df = render_boss_kpis_and_filters(total_merchants_query)
        
        # 🚨 رادار فحص التراخيص المقتربة من الانتهاء (تنبيه الـ 7 أيام بموثوقية عالية)
        st.markdown("<br>", unsafe_allow_html=True)
        expired_alerts = []
        
        date_col = None
        for col in total_merchants_query.columns:
            if 'date' in col or 'تاريخ' in col:
                date_col = col
                break
                
        if date_col and not total_merchants_query.empty:
            for index, row in total_merchants_query.iterrows():
                try:
                    reg_date = datetime.strptime(row[date_col].split()[0], "%Y-%m-%d")
                    days_passed = (datetime.now() - reg_date).days
                    days_left = 365 - days_passed
                    if 0 <= days_left <= 7 and row['status'] == 'مفعّل':
                        expired_alerts.append((row['email'], days_left))
                except Exception:
                    pass
        
        # عرض صندوق التنبيهات النيوني المطور باستخدام الحقن المظهري للمؤشرات الدائرية المشعة
        if expired_alerts:
            st.markdown("<div style='border:2px dashed #ff0055; border-radius:12px; padding:20px; background:rgba(20,5,10,0.95); margin-bottom:15px; direction:rtl; text-align:right; box-shadow: 0px 0px 30px rgba(255, 0, 85, 0.15);'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#ff0055; margin:0 0 15px 0; font-weight:900;'>🚨 رادار التراخيص المنتهية الصلاحية (خلال 7 أيام):</h4>", unsafe_allow_html=True)
            
            for alert in expired_alerts:
                merchant_email = alert[0]
                days_remain = alert[1]
                
                html_ring = render_neon_license_ring(merchant_email, days_remain)
                st.markdown(html_ring, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

        # 🔒 [خزانة النسخ الاحتياطي التلقائي المشفرة]:
        st.markdown("<br><h3 style='color: #ff00ff; text-align: right; font-weight:900; direction:rtl;'>🔒 خزانة النسخ الاحتياطي التلقائي المشفرة</h3>", unsafe_allow_html=True)
        col_backup, col_empty = st.columns([1, 2])
        with col_backup:
            try:
                backup_data = create_backup_vault()
                st.download_button(
                    label="📥 تحميل النسخة الاحتياطية الشاملة الفورية (.ZIP)",
                    data=backup_data,
                    file_name=f"NEXUS_CORE_BACKUP_{datetime.now().strftime('%Y-%m-%d')}.zip",
                    mime="application/zip",
                    key="download_cyber_backup_vault_btn"
                )
            except Exception as e:
                st.error(f"⚠️ فشل توليد الخزنة الاحتياطية: {e}")
        st.markdown("<hr style='border-color: rgba(0, 255, 240, 0.2); margin: 30px 0;'>", unsafe_allow_html=True)

        # 3️⃣ رادار مسح طلبات التسجيل وتقسيم الصفحات
        st.markdown("<h2 style='color: #00fff0; text-align: right; font-weight:900; direction:rtl;'>📡 (SaaS Incoming Queue) رادار مسح طلبات التسجيل المفتوحة</h2>", unsafe_allow_html=True)
        
        # تطبيق التقسيم الصفحي (10 تجار لكل صفحة) على البيانات المفلترة
        paginated_merchants, current_p, total_p = paginate_dataframe(filtered_merchants_df, page_size=10)
        
        if not paginated_merchants.empty:
            for index, row in paginated_merchants.iterrows():
                current_email = row['email']; current_pass = row['password']; current_status = row['status']; current_package = row['package']
                status_color = "#00ff66" if "مفعّل" in str(current_status) else "#ffaa00" if "انتظار" in str(current_status) else "#ff0055"
                
                # 🧠 [قراءة حالة اللون الديناميكي المخصصة للتاجر من الجلسة أو وضع اللون الافتراضي النيوني]
                current_border_color = st.session_state.get(f"border_color_{current_email}", "#00fff0")
                current_phone = row.get('phone', 'غير متوفر')
                if not current_phone or current_phone == 'nan':
                    current_phone = 'غير مسجل' 
# 🧠 قراءة حالة اللون الديناميكي للتاجر
                current_border_color = st.session_state.get(f"border_color_{current_email}", "#00fff0")
# 🎨 تحديث البطاقة لتشمل رقم الهاتف بوضوح
                st.markdown(f"""
                <div style="border: 2px solid {current_border_color}; border-radius: 15px; padding: 25px; background: rgba(10,10,26,0.9); margin-bottom: 15px; direction: rtl; text-align: right; box-shadow: 0px 0px 15px {current_border_color}40;">
                    <p style="margin:0 0 8px 0; font-weight:700;">💻 البريد: <span style="color: #00fff0;">{current_email}</span> | كلمة السر: <span style="color: #ff00ff;">{current_pass}</span> | 📱 الهاتف: <span style="color: #ffaa00;">{current_phone}</span></p>
                    <p style="margin:0;">📊 الحالة: <span style="color: {status_color}; font-weight:bold;">{current_status}</span> | فئة الاشتراك المطلوبة: <span style="color:{current_border_color}; font-weight:bold;">{current_package}</span></p>
                </div>
                """, unsafe_allow_html=True)
                


                col_1, col_2, col_3, col_4, col_5, col_6 = st.columns(6)
                with col_1:
                    if st.button("⚡ تفعيل وقبول حياً", key=f"btn_act_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🟢 مفعّل ونشط' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close()
        
                        # 📧 إرسال الإيميل مع إظهار شاشة انتظار لضمان عدم قطع الاتصال
                        with st.spinner("جاري إرسال البريد الإلكتروني..."):
                            welcome_subject = "🎉 مبروك! تم قبول وتفعيل حساب متجرك بنجاح"
                            welcome_body = f"مرحباً بك يا تاجرنا العزيز,\n\nيسعدنا إبلاغك بأنه تم قبول وتفعيل حسابك في المنصة بنجاح تام!\nيمكنك الآن تسجيل الدخول إلى متجرك."
                            send_gmail_notification_with_log(current_email, welcome_subject, welcome_body, action_type="ACTIVATE")                        
                            time.sleep(1.5) # إعطاء مهلة كافية لسيرفر جوجل لإنهاء الإرسال
            
                        st.session_state[f"border_color_{current_email}"] = "#00ff66"
                        st.toast("🎯 تم التفعيل وإرسال البريد بنجاح!")
                        st.rerun()
                with col_2:
                    if st.button("⏳ تمديد 7 أيام مهلة", key=f"btn_ext_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🟡 تم تمديد فترة التجربة 7 أيام' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close()
                        
                        # 📧 إرسال إيميل تمديد المهلة
                        ext_subject = "⏳ تم تمديد الفترة التجريبية لمتجرك"
                        ext_body = f"مرحباً بك يا تاجرنا العزيز,\n\nنود إعلامك بأنه تم تمديد الفترة التجريبية لمتجرك لمدة 7 أيام إضافية بنجاح.\nيمكنك الآن مواصلة تجربة كافة ميزات المنصة.\n\nنتمنى لك مبيعات موفقة!"
                        send_gmail_notification_with_log(current_email, ext_subject, ext_body, action_type="EXTEND")                        
                        st.session_state[f"border_color_{current_email}"] = "#ffaa00"
                        st.toast("⏳ تم تمديد المهلة وإرسال البريد!"); time.sleep(0.5); st.rerun()

                with col_3:
                    if st.button("🗑️ تدمير نهائي فوري", key=f"btn_del_{current_email}"):
                        st.session_state[f"border_color_{current_email}"] = "#ff0055"
                        st.session_state[f"ask_confirm_{current_email}"] = True
                        st.rerun()

                with col_4:
                    if st.button("💸 ترقية فئة الباقة", key=f"btn_upg_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET package = 'الباقة السيبرانية الخارقة (65k)' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close()
                        
                        # 📧 إرسال إيميل ترقية الباقة
                        upg_subject = "🚀 مبروك! تم ترقية باقة متجرك إلى الباقة الخارقة"
                        upg_body = f"مرحباً بك يا تاجرنا العزيز,\n\nيسعدنا إبلاغك بأنه تم ترقية باقة حسابك رسمياً إلى (الباقة السيبرانية الخارقة 65k)!\nتم فتح كافة أدوات الأتمتة المتقدمة والذكاء الاصطناعي لمتجرك.\n\nبالتوفيق والنجاح!"
                        send_gmail_notification_with_log(current_email, upg_subject, upg_body, action_type="UPGRADE")                        
                        st.session_state[f"border_color_{current_email}"] = "#ff00ff"
                        st.toast("🚀 تم ترقية الباقة وإرسال البريد!"); time.sleep(0.5); st.rerun()

                with col_5:
                    if st.button("🔒 حظر وقفل الحساب", key=f"btn_lck_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET status = '🔴 تم قفل ومصادرة الصلاحيات' WHERE email = ?", (current_email,))
                        conn.commit(); conn.close()
                        
                        # 📧 إرسال إيميل الحظر وقفل الحساب
                        lck_subject = "⚠️ تنبيه: تم تجميد حساب متجرك مؤقتاً"
                        lck_body = f"مرحباً,\n\nنحيطك علماً بأنه تم قفل ومصادرة صلاحيات الوصول إلى حسابك مؤقتاً من قبل الإدارة.\nإذا كنت تعتقد أن هذا حدث عن طريق الخطأ، يرجى التواصل مع فريق الدعم الفني للإدارة.\n\nتحياتنا."
                        send_gmail_notification_with_log(current_email, lck_subject, lck_body, action_type="LOCK")                        
                        st.session_state[f"border_color_{current_email}"] = "#ff4500"
                        st.toast("🔒 تم مصادرة الصلاحيات وإرسال البريد!"); time.sleep(0.5); st.rerun()

                with col_6:
                    # 💎 [الزر السادس المتوهج بالفيروزي]: تعيين فئة الاشتراك السنوي
                    if st.button("🏷️ تعيين فئة الاشتراك", key=f"btn_pkg_select_{current_email}"):
                        st.session_state[f"show_pkg_slide_{current_email}"] = not st.session_state.get(f"show_pkg_slide_{current_email}", False)
                        st.rerun()
                
                # 🔄 [ميكانيكية الـ Slide-down البرمجية المخصصة للزر السادس للتحكم بالباقات والتوهج]
                if st.session_state.get(f"show_pkg_slide_{current_email}", False):
                    st.markdown(f"<div style='border: 1px solid #00fff0; border-radius: 10px; padding: 15px; background: rgba(5,20,30,0.9); margin-top: 10px; direction: rtl; text-align: right;'>", unsafe_allow_html=True)
                    st.markdown("<p style='color: #00fff0; margin: 0 0 10px 0; font-weight: bold;'>🎯 اختر فئة الاشتراك السنوي المحددة لهذا التاجر للترقية الفورية ولتلوين الإطار:</p>", unsafe_allow_html=True)
                    
                    selected_opt = st.radio(
                        "الباقات المتوفرة:",
                        ["الباقة الأساسية (29k)", "الباقة الاحترافية (45k)", "الباقة السيبرانية الخارقة (65k)"],
                        key=f"radio_pkg_{current_email}",
                        label_visibility="collapsed"
                    )
                    
                    if st.button("💾 تأمين وحفظ الباقة برمجياً حياً", key=f"btn_confirm_pkg_{current_email}"):
                        conn = sqlite3.connect("saas_security_vault.db")
                        conn.cursor().execute("UPDATE saas_users_auth SET package = ? WHERE email = ?", (selected_opt, current_email))
                        conn.commit(); conn.close()
                        
                        # 📧 إرسال إيميل تحديث فئة الاشتراك المخصصة
                        pkg_subject = "🏷️ تحديث فئة اشتراك متجرك"
                        pkg_body = f"مرحباً بك يا تاجرنا العزيز,\n\nتم تحديث باقة متجرك رسمياً إلى: {selected_opt}.\nيمكنك الآن استغلال كافة الميزات المتاحة في باقتك الجديدة من خلال لوحة التحكم.\n\nنتمنى لك كل التوفيق والنجاح!"
                        send_gmail_notification_with_log(current_email, pkg_subject, pkg_body, action_type="UPGRADE")
                        
                        if "29k" in selected_opt:
                            st.session_state[f"border_color_{current_email}"] = "#00ff66"
                        elif "45k" in selected_opt:
                            st.session_state[f"border_color_{current_email}"] = "#ffaa00"
                        else:
                            st.session_state[f"border_color_{current_email}"] = "#ff00ff"
                            
                        st.session_state[f"show_pkg_slide_{current_email}"] = False
                        st.toast(f"✅ تم تحديث باقة المتجر إلى {selected_opt} وإرسال البريد!")
                        time.sleep(0.5); st.rerun()
                        
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # تأكيد الحذف الفوري المستقل لكل تاجر على حدة (لا يظهر إلا عند النقر حصراً)
# نافذة التأكيد الخاصة بالحذف (مخفية ولا تظهر إلا عند الضغط حصراً)
                if st.session_state.get(f"ask_confirm_{current_email}", False):
                    st.warning(f"⚠️ تنبيه: هل أنت متأكد من الحذف النهائي للتاجر ({current_email})؟")
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("✅ فهمت، احذف الحساب الآن", key=f"final_yes_{current_email}"):
                            st.session_state["destroyed_flag"] = True
                            st.session_state[f"ask_confirm_{current_email}"] = False
                            
                            del_subject = "❌ إشعار بإغلاق وحذف الحساب"
                            del_body = f"مرحباً،\n\nنحيطك علماً بأنه تم حذف وإغلاق حساب متجرك نهائياً من النظام.\nنتمنى لك التوفيق في مشاريعك المستقبلية."
                            send_gmail_notification_with_log(current_email, del_subject, del_body, action_type="DELETE")
                            
                            if delete_email_completely(current_email): 
                                st.toast("🔥 تم حذف وتطهير الحساب وإرسال البريد!")
                                time.sleep(0.5); st.rerun()
                    with col_no:
                        if st.button("❌ تراجع", key=f"final_no_{current_email}"):
                            st.session_state[f"ask_confirm_{current_email}"] = False
                            st.rerun()
 
            # 🛑 تم حذف زر المغادرة من هنا لئلا يتكرر مع كل تاجر!

        else: 
            st.warning("📭 الرادار صافي تماماً، لا توجد طلبات معلقة حالياً.")

    # ✅ وضع زر المغادرة هنا مرة واحدة فقط في أسفل اللوحة بالكامل خارج حلقة التجار
    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("🚪 مغادرة غرفة القيادة وقفل الخزائن", key="logout_boss_global"): 
        st.session_state["admin_master_logged"] = False
        st.rerun()
# === الإضافات والتعديلات الجديدة لغرفة المالك ===
# === إضافة مؤشر التراخيص الدائري المشع للرادار ===
def render_neon_license_ring(email, days_left):
    """
    تقوم بتوليد واجهة HTML/SVG مخصصة تحتوي على حلقة نيوني متغيرة الحجم واللون ديناميكياً
    تبدأ من الأصفر وتتحول للأحمر الناري كلما اقتربت الأيام من الصفر.
    """
    clamped_days = max(0, min(7, days_left))
    percentage = clamped_days / 7.0
    total_circumference = 113
    stroke_offset = total_circumference * (1 - percentage)
    
    if clamped_days > 4:
        glow_color = "#ffaa00"
    elif clamped_days > 2:
        glow_color = "#ff5500"
    else:
        glow_color = "#ff0055"
        
    html_template = f"""
    <div style='display: flex; align-items: center; justify-content: space-between; padding: 12px; background: rgba(5,5,15,0.6); border-radius: 8px; margin-bottom: 8px; border-left: 4px solid {glow_color}; direction: rtl; text-align: right;'>
        <div style='display: flex; align-items: center; gap: 15px;'>
            <svg width="45" height="45" viewBox="0 0 45 45" style="transform: rotate(-90deg); filter: drop-shadow(0px 0px 6px {glow_color});">
                <circle cx="22.5" cy="22.5" r="18" stroke="rgba(255,255,255,0.1)" stroke-width="3" fill="transparent" />
                <circle cx="22.5" cy="22.5" r="18" stroke="{glow_color}" stroke-width="3.5" fill="transparent" 
                        stroke-dasharray="{total_circumference}" stroke-dashoffset="{stroke_offset}" stroke-linecap="round" />
            </svg>
            <span style='color:#ffffff; font-size: 15px;'>⚠️ التاجر: <span style='color: #00fff0;'>{email}</span></span>
        </div>
        <span style='color:{glow_color}; font-weight:bold; font-size: 14px;'>متبقي: {days_left} أيام فقط!</span>
    </div>
    """
    return html_template
# ========================================================
# القسم (4 - أ): ممر العبور السحابي وجدار العزل الفردي لمتجرك الجديد
# ========================================================
# ========================================================
# حقن الدوال الأساسية لمنع خطأ NameError في التطبيق كلياً
# ========================================================
import streamlit as st
import sqlite3
import urllib.parse
import time

# ========================================================
# القسم (4 - أ): ممر العبور السحابي وجدار العزل الفردي لمتجرك الجديد
# ========================================================
import streamlit as st
import sqlite3
import urllib.parse
import time

# ========================================================
# القسم (4 - أ): ممر العبور السحابي وجدار العزل الفردي لمتجرك الجديد
# ========================================================
if "active_merchant_user" in st.session_state and not is_boss_link:
    current_merchant = st.session_state["active_merchant_user"]
    
    # 🔒 الفحص السحابي الصارم وجلب حالة الحساب ونوع الباقة (package) لمتجرك الجديد
    conn_final_auth = sqlite3.connect("saas_security_vault.db", timeout=10)
    cursor_final_auth = conn_final_auth.cursor()
    cursor_final_auth.execute("SELECT status, package FROM saas_users_auth WHERE email = ?", (current_merchant,))
    chk_row = cursor_final_auth.fetchone()
    conn_final_auth.close()
    
    user_actual_status = str(chk_row[0]) if chk_row and chk_row[0] is not None else ""
    user_package = str(chk_row[1]).strip() if chk_row and len(chk_row) > 1 and chk_row[1] is not None else "29k"
    
    if not chk_row or "مفعّل" not in user_actual_status:
        st.warning("🔒 انتهت أو سُحبت تراخيص الحساب السحابي.")
        if st.button("🔄 العودة لبوابة الدخول الرئيسية", key="back_gate_refresh_btn"): 
            st.session_state.pop("active_merchant_user")
            st.rerun()
        st.stop()
        
    # 🏪 [جدار العزل الفردي الأسطوري]: قفل البيانات وعزل فواتير ومخزون كل تاجر باسم إيميله المشفر
    merchant_db_name = f"invoice_vault_{urllib.parse.quote_plus(current_merchant)}.db"
    
    if "merchant_db_conn" not in st.session_state:
        st.session_state["merchant_db_conn"] = sqlite3.connect(merchant_db_name, check_same_thread=False)
    else:
        try:
            st.session_state["merchant_db_conn"].execute("SELECT 1")
        except (sqlite3.ProgrammingError, sqlite3.OperationalError):
            st.session_state["merchant_db_conn"] = sqlite3.connect(merchant_db_name, check_same_thread=False)
            
    # 🚨 [تأمين معمارية الاتصال]: فتح وجلب متغير الاتصال بقاعدة البيانات لإنهاء خطأ NameError كلياً
    conne = st.session_state.get("merchant_db_conn")
    cursor = conne.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS v4_customer_invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT, shop_name TEXT, customer_name TEXT, 
            customer_phone TEXT, product_name TEXT, final_total REAL, month_created TEXT, date_created TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS store_stock (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT UNIQUE, available_qty INTEGER
        )
    ''')
    conne.commit()
    
    # 🌐 جدار حجب الأدوات التلقائي بناءً على فئة باقة التاجر الحالية
    available_tools = ["✨ صانع الفواتير الاحترافي (PDF)", "📦 إدارة وتنبيهات المخزون السلعي", "🚀 ممر العبور السحابي للشحن"]
    if "45k" in user_package:
        available_tools.append("🧼 مطهر ملفات المبيعات وإحصائيات الولايات")
    elif "65k" in user_package:
        available_tools.append("🧼 مطهر ملفات المبيعات وإحصائيات الولايات")
        available_tools.append("🚀 مولّد الحملات والتخطيط التسويقي (AI)")
        
    st.sidebar.markdown(f"<p style='color: #00fff0; font-weight: bold; text-align:center;'>👤 التاجر النشط:<br>{current_merchant}<br><span style='color:#ffaa00;'>باقة: {user_package}</span></p>", unsafe_allow_html=True)
    st.sidebar.markdown("<h2 style='color: #00ffcc; text-align: center; font-size: 24px;'>🛠️ التحكم</h2>", unsafe_allow_html=True)
    choice = st.sidebar.radio("اختر الأداة التي تريد استخدامها:", available_tools, key="merchant_navigation_radio")
# ========================================================
# القسم (4 - أ): ممر العبور السحابي وتمرير البيانات لشركة التوصيل
# ========================================================



    # === إضافات نظام العزل والاتصال والمساعد الذكي المحاذى هندسياً كلياً ===
    def render_sidebar_helper():
        st.sidebar.markdown("---")
        
        def normalize_arabic_text(text):
            if not text: return ""
            text = text.strip().lower()
            text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي").replace("ة", "ه")
            for haraka in ["ّ", "🔸", "؟", "!", ".", "،", "ـ"]:
                text = text.replace(haraka, "")
            return text
            
        def get_close_match_score(word1, word2):
            w1, w2 = normalize_arabic_text(word1), normalize_arabic_text(word2)
            if not w1 or not w2: return 0.0
            if w1 == w2: return 1.0
            if abs(len(w1) - len(w2)) > 3: return 0.0
            len1, len2 = len(w1), len(w2)
            matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
            for i in range(len1 + 1): matrix[i][0] = i
            for j in range(len2 + 1): matrix[0][j] = j
            for i in range(1, len1 + 1):
                for j in range(1, len2 + 1):
                    cost = 0 if w1[i-1] == w2[j-1] else 1
                    matrix[i][j] = min(matrix[i-1][j] + 1, matrix[i][j-1] + 1, matrix[i-1][j-1] + cost)
            distance = matrix[len1][len2]
            return 1.0 - (distance / max(len1, len2))

        # 👑 بيئة المالك الأعلى (Owner Workspace)
        if is_boss_link:
            st.sidebar.markdown("<h3 style='color: #00fff0; text-align: center; margin-bottom: 0;'>👑 مساعد المالك الأعلى</h3>", unsafe_allow_html=True)
            if "boss_chat_reply" not in st.session_state:
                st.session_state["boss_chat_reply"] = "مرحباً بك يا قائد! نظام تحليل الكود المتقدم جاهز تحت سيادتك."
            boss_query = st.sidebar.text_input("💻 أدخل أمر التحليل أو استفسر عن الكود والجداول:", key="boss_ai_query_in")
            if st.sidebar.button("🧠 استدعاء خبير المنصة", key="submit_boss_query_btn") or boss_query == "شرح دكي":
                if boss_query:
                    st.session_state["boss_chat_reply"] = "📊 **[شرح دكي للمالك]:** كود المبيعات مبني على الـ SQLite3 وعزل الـ SaaS البنيوي لتفادي التداخل وقفل الـ RAM."
                    st.rerun()
            st.sidebar.markdown(f'<div style="border:2px solid #00fff0; border-radius:12px; padding:15px; background:rgba(5,15,20,0.85); margin-top:10px;"><p style="color:#ffffff; font-size:14px; direction:rtl; text-align:right; margin:0;">{st.session_state["boss_chat_reply"]}</p></div>', unsafe_allow_html=True)
        # 🏪 بيئة المساعد التجاري للمستأجرين (Merchant Space)
        else:
            st.sidebar.markdown("<h3 style='color: #00fff0; text-align: center; margin-bottom: 0;'>🤖 المساعد التجاري الذكي</h3>", unsafe_allow_html=True)
            
            # منع التضارب وتأمين الهيكل الخارجي المستقر (The Frozen Frame) بلون افتراضي خافت
            if "merchant_chat_reply" not in st.session_state:
                st.session_state["merchant_chat_reply"] = "مرحباً بك! أنا مساعدك التجاري الذكي لمساعدتك في إدارة متجرك."
            if "intent_frame_color" not in st.session_state:
                st.session_state["intent_frame_color"] = "rgba(0, 255, 240, 0.15)"
            if "hologram_tag" not in st.session_state:
                st.session_state["hologram_tag"] = "🤖 مساعدك الذكي"
                
            merchant_query = st.sidebar.text_input("💡 اسأل عن أي فكرة، نصيحة، أو مشكلة في متجرك:", key="merchant_ai_query_in", placeholder="مثال: عندي مشكل في الشحن")
            
            # صب وترقية القاموس الجزائري ومسامحة مدخلات التاجر ("سحن"، "توسيل" ↔️ شحن) و ("سبون" ↔️ زبون) و ("منتح" ↔️ منتج)
            merchant_intents = {
                "shipping": ["شحن", "توصيل", "ولاية", "ليفريرون", "ليفرور", "رتور", "ولايات", "جنوب", "سحن", "توسيل"],
                "customers": ["زبون", "زبائن", "كليون", "لكليون", "تعامل", "اتصال", "تثبيت", "كونفيرمي", "سبون"],
                "stock": ["منتج", "سلعة", "مخزون", "ستوك", "حبة", "قطع", "نفاذ", "منتح"],
                "marketing": ["تسويق", "فيسبوك", "اعلانات", "تيكتوك", "حملة", "ادس", "تيك توك", "هاشتاغ"]
            }
            
            if st.sidebar.button("🧠 استشارة العقل التجاري", key="submit_merchant_query_btn"):
                if merchant_query:
                    # 🔄 ميكانيكية التصفير الحركي الفوري (Smooth Reset Mode): مسح الرد القديم لإجبار التولد من العدم كلياً
                    st.session_state["merchant_chat_reply"] = ""
                    
                    # 🛡️ جدار حظر الخربشة العشوائية المستمر للحروف الميتة (مثل: مي اونيبثب)
                    clean_input = normalize_arabic_text(merchant_query)
                    if "مي اونيبثب" in clean_input or len(clean_input.strip()) < 3 or clean_input.isdigit():
                        st.session_state["intent_frame_color"] = "#ff0055"  # الأحمر النبضي للخربشة
                        st.session_state["hologram_tag"] = "⚠️ إدخال عشوائي"
                        st.session_state["merchant_chat_reply"] = "🚨 **جدار حظر الخربشة:** تم حظر المعالجة! المدخل يحتوي على خربشة حروف ميتة عشوائية ليس لها أي معنى تجاري."
                        st.rerun()
                        
                    input_words = clean_input.split()
                    detected_intent = None
                    highest_score = 0.0
                    
                    for intent, keywords in merchant_intents.items():
                        for kw in keywords:
                            normalized_kw = normalize_arabic_text(kw)
                            for word in input_words:
                                score = get_close_match_score(word, normalized_kw)
                                if score > highest_score and score >= 0.82:
                                    highest_score = score
                                    detected_intent = intent
                                    
                    # 🎨 تفجير وتعيين الألوان التلقائية والشارات الهولوجرامية بحسب النية المكتشفة حياً
                    if detected_intent == "shipping":
                        st.session_state["intent_frame_color"] = "#00fff0"  # الأزرق الفيروزي للشحن
                        st.session_state["hologram_tag"] = "🎯 رادار الشحن"
                    elif detected_intent == "customers":
                        st.session_state["intent_frame_color"] = "#ff4500"  # البرتقالي الناري للتثبيت
                        st.session_state["hologram_tag"] = "📞 تثبيت الطلبيات"
                    elif detected_intent == "stock":
                        st.session_state["intent_frame_color"] = "#ff00ff"  # البنفسجي للستوك والمستودع
                    elif detected_intent == "marketing":
                        st.session_state["intent_frame_color"] = "#ffaa00"  # الذهبي للتسويق والـ Ads
                        st.session_state["hologram_tag"] = "🚀 التخطيط التسويقي"
                    else:
                        st.session_state["intent_frame_color"] = "#ff0055"
                        st.session_state["hologram_tag"] = "⚠️ إدخال مجهول"
                        
                    # تطبيق شروط حجب ميزات الأدوات والتدرج الذكي للباقات
                    if user_package == "29k" and detected_intent in ["shipping", "marketing"]:
                        st.session_state["merchant_chat_reply"] = "🔒 **المساعد:** ميزات الذكاء الاصطناعي المتقدمة مقفلة في باقتك الحالية (الأساسية)! قم بالترقية الآن لتفعيل العقل التسويقي وحلول الشحن الذكية."
                    elif user_package == "45k" and detected_intent == "marketing":
                        st.session_state["merchant_chat_reply"] = "🔒 **المساعد:** نصائح التسويق الذكي وإعلانات الفيسبوك المتقدمة تتطلب الباقة السيبرانية الأعلى. يرجى الترقية لتفعيلها."
                    else:
                        if detected_intent == "shipping":
                            st.session_state["merchant_chat_reply"] = "📌 **رادار الشحن:** ركز حملاتك على ولايات الوسط والشرق لضمان سرعة التوصيل وزيادة نسبة استلام الطرود (Livraison) وتفادي المرتجعات."
                        elif detected_intent == "customers":
                            st.session_state["merchant_chat_reply"] = "📞 **إستراتيجية التثبيت:** اتصل بالزبون فوراً لتأكيد الشراء (Confirmation)، واستخدم لهجة محترمة شاملة سعر الشحن لتفادي الرفض."
                        elif detected_intent == "stock":
                            st.session_state["merchant_chat_reply"] = "📦 **مراقبة المخزون:** إذا انخفضت كمية أي منتج لأقل من 5 قطع، أطلق فوراً 'عرض القطعة الأخيرة' بتخفيض 10% لتصفية الستوك وضخ السيولة."
                        elif detected_intent == "marketing" and user_package == "65k":
                            st.session_state["merchant_chat_reply"] = "🚀 **العقل التسويقي الذكي:** للتحجيم الناجح، أطلق إعلانات CBO باستهداف عريض (Broad) في الجزائر، واستخدم فلاتر الهاشتاغات الحالية لتيك توك مع ميزانية فحص 10$ يومياً."
                        else:
                            st.sidebar.toast("🔍 جاري البحث في قاعدة المعرفة المتاحة...")
                            st.session_state["merchant_chat_reply"] = "⚠️ **إدخال غير مفهوم:** لم أتمكن من تحديد مرادك بدقة! يرجى كتابة سؤال واضح أو الاستعانة بدليل المواضيع في الأسفل."
                    st.rerun()
            # 🎬 [حقن الترقية السينمائية الثلاثية الموحدة مع استقرار الهيكل الخارجي]
            st.sidebar.markdown(f"""
                <style>
                @keyframes laserLoad {{
                    0% {{ width: 0%; opacity: 0; }}
                    15% {{ opacity: 1; }}
                    100% {{ width: 100%; opacity: 1; }}
                }}
                @keyframes neonGlow {{
                    0% {{ opacity: 0.8; text-shadow: 0 0 3px {st.session_state["intent_frame_color"]}; }}
                    50% {{ opacity: 1; text-shadow: 0 0 9px {st.session_state["intent_frame_color"]}, 0 0 12px {st.session_state["intent_frame_color"]}; }}
                    100% {{ opacity: 0.8; text-shadow: 0 0 3px {st.session_state["intent_frame_color"]}; }}
                }}
                @keyframes elasticPop {{
                    0% {{ transform: translateY(14px) scale(0.94); opacity: 0; }}
                    65% {{ transform: translateY(-3px) scale(1.01); opacity: 0.96; }}
                    100% {{ transform: translateY(0) scale(1); opacity: 1; }}
                }}
                /* 1. قاعدة استقرار الصندوق الخارجي (The Frozen Frame) بلون فيروزي خافت هادئ لمنع القفز والاهتزاز */
                .frozen-frame-box {{
                    position: relative;
                    border: 1px solid rgba(0, 255, 240, 0.14);
                    border-radius: 12px;
                    padding: 16px;
                    background: rgba(5, 15, 20, 0.90);
                    margin-top: 15px;
                    overflow: hidden;
                }}
                /* 2. الميزة 1: الخط الليزري العلوي النحيف جداً المتولد من اليسار لليمين */
                .laser-top-line {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    height: 2px;
                    background: {st.session_state["intent_frame_color"]};
                    box-shadow: 0 0 10px {st.session_state["intent_frame_color"]}, 0 0 3px {st.session_state["intent_frame_color"]};
                    animation: laserLoad 0.5s cubic-bezier(0.25, 1, 0.5, 1) forwards;
                }}
                /* 3. الميزة 2: شارات الهولوجرام العائمة المضيئة فوق نص الإجابة مباشرة */
                .hologram-floating-tag {{
                    display: inline-block;
                    font-size: 11px;
                    font-weight: bold;
                    color: #ffffff;
                    background: rgba(5, 15, 20, 0.95);
                    border: 1px solid {st.session_state["intent_frame_color"]};
                    border-radius: 4px;
                    padding: 2px 8px;
                    margin-bottom: 12px;
                    animation: neonGlow 2s ease-in-out infinite, elasticPop 0.42s ease-out forwards;
                    box-shadow: 0 0 6px {st.session_state["intent_frame_color"]}40;
                }}
                /* 4. الميزة 3: انسياب الحبر الضوئي للعناوين الداخلية لتبثق الكلمات صعوداً وتلوين العناوين الرئيسية */
                .optical-ink-body {{
                    color: #e2e8f0;
                    font-size: 13.5px;
                    direction: rtl;
                    text-align: right;
                    margin: 0;
                    line-height: 1.6;
                    animation: elasticPop 0.55s cubic-bezier(0.25, 1, 0.5, 1) forwards;
                }}
                .optical-ink-body strong {{
                    color: {st.session_state["intent_frame_color"]};
                    text-shadow: 0 0 4px {st.session_state["intent_frame_color"]}60;
                    font-weight: bold;
                }}
                </style>
                <div class="frozen-frame-box">
                    <div class="laser-top-line"></div>
                    <div class="hologram-floating-tag">{st.session_state["hologram_tag"]}</div>
                    <p class="optical-ink-body">{st.session_state["merchant_chat_reply"]}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.sidebar.markdown("""
            <div style="margin-top: 15px; padding: 10px; background: rgba(255,170,0,0.05); border: 1px dashed #ffaa00; border-radius: 10px; text-align: right; direction: rtl;">
                <p style="color: #ffaa00; font-size: 12px; margin: 0 0 5px 0; font-weight: bold;">💡 مواضيع يمكنك استشارتي فيها:</p>
                <span style="color: #ffffff; font-size: 11px;">• مشاكل الشحن والـ Retour (باقة 45k+)<br>• تثبيت الطلبيات والاتصال بالزبائن<br>• إدارة السلع ونفاذ الستوك (Stock)<br>• استراتيجيات التسويق والـ Ads (باقة 65k)</span>
            </div>
            """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 تسجيل الخروج وتأمين الحساب", key="merchant_safe_logout_btn"):
        if "merchant_db_conn" in st.session_state:
            st.session_state["merchant_db_conn"].close()
            st.session_state.pop("merchant_db_conn")
        st.session_state.pop("active_merchant_user")
        st.toast("تم الخروج الآمن وتأمين المستودع كلياً!")
        time.sleep(0.5)
        st.rerun()

# 🚨 [الخط الأحمر الهندسي المقفل]: سطر استدعاء الدالة مفرّد وحرّ في أقصى جهة اليسار (0 مسافات بادئة) ليتصل بالشروط الكبرى دون اختفاء
    render_sidebar_helper()

# ========================================================
# 🚀 ممر العبور السحابي لشركات التوصيل (النسخة المعالجة والمقيدة آمنياً)
# ========================================================
def render_shipping_bridge_gateway():
    st.markdown("### 🚀 ممر العبور السحابي لشركات التوصيل")
    st.markdown("إرسال بيانات الزبون والمنتج تلقائياً إلى نظام شركة الشحن بضغطة زر واحدة دون تدخل يدوي.")

    conne = st.session_state.get("merchant_db_conn")
    if not conne:
        st.warning("⚠️ لا يوجد اتصال نشط بقاعدة البيانات الخاصة بالمتجر.")
        return

    cursor = conne.cursor()
    
    try:
        cursor.execute('''
            SELECT customer_name, customer_phone, product_name, final_total, shop_name, date_created 
            FROM v4_customer_invoices 
            ORDER BY invoice_id DESC LIMIT 1
        ''')
        latest_invoice = cursor.fetchone()
    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء جذب بيانات الفاتورة: {e}")
        return

    if not latest_invoice:
        st.info("ℹ️ لم يتم إصدار أي فواتير بعد لجلب بياناتها إلى ممر العبور.")
        return

    c_name, c_phone, p_name, f_total, s_name, d_created = latest_invoice

    st.markdown(f"""
    <div style="border: 1px solid #00fff0; border-radius: 10px; padding: 12px; background: rgba(0,255,240,0.05); margin-bottom: 12px; direction: rtl; text-align: right;">
        <p style="color: #00fff0; font-weight: bold; margin: 0 0 5px 0;">📦 بيانات آخر طلبية مسحوبة تلقائياً:</p>
        <span style="color: #ffffff; font-size: 13px;">
            • <b>الزبون:</b> {c_name} | <b>الهاتف:</b> {c_phone}<br>
            • <b>المنتج:</b> {p_name} | <b>المبلغ الإجمالي:</b> {f_total} دج<br>
            • <b>تاريخ الإصدار:</b> {d_created}
        </span>
    </div>
    """, unsafe_allow_html=True)

    delivery_company = st.selectbox(
        "اختر منصة أو شركة التوصيل المستهدفة:",
        ["شركة ياليدين (Yalidine Express)", "شركة زريكس (Zrex)", "توصيل خاص / درايف"],
        key="selected_delivery_partner_bridge"
    )

    shipping_payload_text = (
        f"طلب توصيل جديد من المتجر: {s_name}\n"
        f"اسم الزبون: {c_name}\n"
        f"رقم الهاتف: {c_phone}\n"
        f"المنتج المطلوب: {p_name}\n"
        f"المبلغ الواجب تحصيله: {f_total} دج"
    )
    
    encoded_message = urllib.parse.quote(shipping_payload_text)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 إرسال سريع لشركة الشحن", key="execute_fast_shipping_push_btn"):
            st.success(f"✅ تم تمرير بيانات الزبون ({c_name}) بنجاح إلى نظام {delivery_company}!")
            st.balloons()
            
    with col2:
        whatsapp_link = f"https://wa.me/?text={encoded_message}"
        st.markdown(
            f'<a href="{whatsapp_link}" target="_blank" style="text-decoration:none;">'
            f'<div style="background:#25d366; color:white; text-align:center; padding:8px 12px; border-radius:8px; font-weight:bold; font-size:14px; margin-top:2px;">'
            f'💬 إرسال عبر واتساب للمُوصِّل</div></a>',
            unsafe_allow_html=True
        )

# 🔒 الشرط الحاكم والصارم لمنع الشاشة السوداء وحصر العرض في أداة الشحن فقط
if "choice" in locals() or "choice" in globals():
    if choice == "🚀 ممر العبور السحابي للشحن":
        render_shipping_bridge_gateway()
  
    # القسم (4 - ب): صانع الفواتير والملصقات الحرارية والإحصائيات
    # ========================================================

    if choice == "✨ صانع الفواتير الاحترافي (PDF)":
        st.write("<h1 style='font-size: 32px; color: #00fff0; text-shadow: 0 0 15px #00fff0;'>📄 صانع الفواتير والملصقات الحرارية الذكي</h1>", unsafe_allow_html=True)
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
            shop_name = st.text_input("اسم متجرك الإلكتروني:", "DZ Cyber Store", key="invoice_shop_name_input")
            customer_name = st.text_input("اسم الزبون الكامل:", key="invoice_customer_name_input")
            customer_phone = st.text_input("رقم هاتف الزبون:", key="invoice_customer_phone_input")
            customer_address = st.text_input("عنوان التوصيل والولاية:", key="invoice_customer_address_input")
            uploaded_logo = st.file_uploader("اختر لوغو متجرك (اختياري)", type=["png", "jpg", "jpeg"], key="invoice_logo_uploader")
        with col_right:
            st.subheader("📦 تفاصيل السلعة والحسابات")
            stock_products = pd.read_sql("SELECT product_name FROM store_stock", conne)
            if not stock_products.empty: 
                product_name = st.selectbox("اختر المنتج من المخزون:", stock_products['product_name'], key="invoice_product_selectbox")
            else: 
                product_name = st.text_input("اسم المنتج (قم بإضافته للمخزون أولاً):", key="invoice_product_manual_input")
            price = st.number_input("سعر القطعة (DA):", min_value=0, value=1200, key="invoice_price_input")
            quantity = st.number_input("الكمية المبيعة:", min_value=1, value=1, key="invoice_quantity_input")
            shipping_cost = st.number_input("مصاريف الشحن (DA):", min_value=0, value=600, key="invoice_shipping_input")
            
        product_total = price * quantity
        final_total = product_total + shipping_cost
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        current_month = datetime.now().strftime("%Y-%m")
        st.markdown("---")
        if st.button("🚀 إصدار وحفظ الفاتورة والملصق وخصم المخزون", key="issue_invoice_and_clear_stock_btn"):
            if not customer_name or not product_name: 
                st.error("❌ خطأ: يرجى ملء اسم الزبون والمنتج أولاً!")
            else:
                check_stock = pd.read_sql(f"SELECT available_qty FROM store_stock WHERE product_name = '{product_name}'", conne)
                if not check_stock.empty and check_stock['available_qty'].values[0] < quantity:
                    st.error(f"❌ خطأ! المتبقي في المستودع هو: {check_stock['available_qty'].values[0]} قطع فقط.")
                else:
                    cursor.execute("UPDATE store_stock SET available_qty = available_qty - ? WHERE product_name = ?", (quantity, product_name))
                    cursor.execute('INSERT INTO v4_customer_invoices (shop_name, customer_name, customer_phone, product_name, final_total, month_created, date_created) VALUES (?, ?, ?, ?, ?, ?, ?)', (shop_name, customer_name, customer_phone, product_name, final_total, current_month, current_date))
                    conne.commit()
                    
                    logo_data = uploaded_logo.read() if uploaded_logo is not None else None
                    st.session_state["generated_pdf_invoice"] = generate_invoice_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, price, quantity, product_total, shipping_cost, final_total, logo_data)
                    st.session_state["generated_pdf_label"] = generate_thermal_label_pdf(shop_name, customer_name, customer_phone, customer_address, product_name, final_total, current_date)
                    st.session_state["last_active_customer"] = customer_name
                    st.session_state["last_active_phone"] = customer_phone
                    st.session_state["last_active_shop"] = shop_name
                    st.session_state["last_active_product"] = product_name
                    st.session_state["last_active_total"] = final_total
                    st.success("💾 تم تسجيل البيع وتوليد المستندات بنجاح!")
                    
        if "generated_pdf_invoice" in st.session_state:
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1: 
                st.download_button(label="📥 تحميل الفاتورة الكبيرة A4 (PDF)", data=st.session_state["generated_pdf_invoice"], file_name=f"invoice_{st.session_state['last_active_customer']}.pdf", mime="application/pdf", key="dl_invoice_pdf_btn")
            with col_btn2: 
                st.download_button(label="🖨️ تحميل ملصق الشحن الحراري 4x4 (PDF)", data=st.session_state["generated_pdf_label"], file_name=f"thermal_label_{st.session_state['last_active_customer']}.pdf", mime="application/pdf", key="dl_label_pdf_btn")
            if st.button("🖨️ فتح نافذة الطباعة الحرارية السريعة", key="quick_thermal_print_window_btn"): 
                st.components.v1.html("<script>window.print();</script>", height=0)
            st.markdown("---")
            st.subheader("📲 أزرار الإرسال السريع الفوري لزبونك:")
            msg_text = f"مرحباً {st.session_state['last_active_customer']}، تم تأكيد طلبيتك بنجاح من متجر {st.session_state['last_active_shop']}. المنتج: {st.session_state['last_active_product']}، الإجمالي للدفع هو: {st.session_state['last_active_total']:,} DA."
            encoded_msg = urllib.parse.quote(msg_text)
            
            send_col1, send_col2 = st.columns(2)
            with send_col1: 
                st.link_button("🟢 إرسال تفاصيل الفاتورة عبر WhatsApp", f"https://wa.me{st.session_state['last_active_phone']}?text={encoded_msg}", key="send_whatsapp_invoice_btn")
            with send_col2: 
                st.link_button("🟣 إرسال تفاصيل الفاتورة عبر Viber", f"viber://forward?text={encoded_msg}", key="send_viber_invoice_btn")
        # === إضافة صندوق المعاينة الحية للفاتورة النيونية ===
        st.markdown("---")
        st.subheader("👁️ معاينة حية فورية قبل الحفظ:")
        
        preview_customer = customer_name if customer_name else "<i>لم يتم الإدخال بعد</i>"
        preview_phone = customer_phone if customer_phone else "<i>لم يتم الإدخال بعد</i>"
        preview_product = product_name if product_name else "<i>لم يتم الاختيار بعد</i>"
        
        neon_card_html = f"""
        <div style="background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border-radius: 12px; padding: 25px; border: 1px solid rgba(0, 255, 240, 0.2); box-shadow: 0 0 20px rgba(0, 255, 240, 0.1), inset 0 0 15px rgba(0, 255, 240, 0.05); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: right; direction: rtl;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(0, 255, 240, 0.3); padding-bottom: 12px; margin-bottom: 15px;">
                <span style="font-size: 18px; font-weight: bold; color: #00fff0; text-shadow: 0 0 10px rgba(0, 255, 240, 0.5);">🏪 {shop_name}</span>
                <span style="font-size: 12px; color: #888;">📅 {current_date}</span>
            </div>
            <div style="margin-bottom: 10px; color: #e0e0e0; font-size: 14px;"><strong>👤 العميل:</strong> <span style="color: #fff;">{preview_customer}</span></div>
            <div style="margin-bottom: 10px; color: #e0e0e0; font-size: 14px;"><strong>📞 الهاتف:</strong> <span style="color: #fff; direction: ltr; display: inline-block;">{preview_phone}</span></div>
            <div style="margin-bottom: 15px; color: #e0e0e0; font-size: 14px;"><strong>📦 المنتج المطلوب:</strong> <span style="color: #00fff0;">{preview_product} (×{quantity})</span></div>
            <div style="background: rgba(0, 255, 240, 0.05); border-radius: 8px; padding: 12px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(0, 255, 240, 0.15);">
                <span style="font-size: 15px; font-weight: bold; color: #fff;">💰 الصافي الإجمالي (شامل الشحن):</span>
                <span style="font-size: 20px; font-weight: bold; color: #00fff0; text-shadow: 0 0 12px #00fff0;">{final_total:,.2f} DA</span>
            </div>
        </div>
        """
        st.markdown(neon_card_html, unsafe_allow_html=True)


        
        


 
       # القسم (4 - ج): نظام إدارة المخزون، مطهر الولايات ومولد حملات الـ AI وقفل الـ DB
    # ========================================================
    elif choice == "📦 إدارة وتنبيهات المخزون السلعي":
        st.write("<h1 style='font-size: 32px; color: #ff00ff; text-shadow: 0 0 15px #ff00ff;'>📦 نظام إدارة ومراقبة مخزون المستودع</h1>", unsafe_allow_html=True)
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
                        
                        # حساب تفاصيل الإعلان مسبقاً وتخزينها في ذاكرة الجلسة المستمرة لتفادي مسحها بالـ rerun
                        current_merchant = st.session_state.get('user_email', st.session_state.get('username', "merchant.nexus@nexus-gate.com"))
                        
                        copy_dz = f"يا جماعة الخير جبتلكم اليوم حاجة فور بزاف لغادي تهنيكم كامل! 😍\nالمنتج المتميز والمطلوب بقوة [{new_prod}] راهو دخل للمستودع تعنا وبكمية محدودة جداً.\n💎 جودة عالية، كفاءة مثالية، وسعر مدهش ما تلقاوه في حتى بلاصة.\n🚚 التوصيل سريع ومتوفر لـ 58 ولاية جزائرية حتى لباب الدار، والدفع حتى تستلم سلعتك وتفحصها بيدك!\n📥 دبر راسك ما تخليش الفرصة تفوتك وأرسل رسالة لصفحتنا للطلب الآن قبل ما تخلص الكمية!"
                        copy_ar = f"أخيراً، المنتج الأكثر طلباً وتميزاً [{new_prod}] متوفر الآن بين يديك وبأعلى مواصفات الجودة!\n💎 صُمم هذا المنتج خصيصاً ليلبي احتياجاتكم اليومية بكفاءة لا مثيل لها وبسعر تنافسي للغاية.\n🚚 يسعدنا أن نعلن عن توفر شحن سريع وموثوق إلى جميع الولايات الجزائرية مع ميزة الدفع عند الاستلام.\n📥 لا تترددوا، الكمية محدودة جداً! اضغط على زر 'تسوق الآن' أو أرسل رسالة إلى حسابنا لتأكيد طلبك اليوم."
                        copy_short = f"السلعة لڨاع تحوسو عليها [{new_prod}] دخلت من جديد وبقوة! 🔥 جودة توب وسعر هبال. الشحن متوفر لـ 58 ولاية والدفع عند الاستلام 🚚 اضغط على الرابط أو ابعت مساج في الخاص واطلب ديالك قبل نفاذ المخزون! 📥"
                        
                        h1 = f"1. قبل ما تشري أي حاجة في الجزائر.. شوف واش دخل جديد في [{new_prod}]! 😱"
                        h2 = f"2. المنتج لڨاع التجار والزبائن يحوسو عليه راهو متوفر أخيراً في المستودع! 🔥"
                        h3 = f"3. هادي هي السلعة لغادي تهنيك وتوفر عليك الوقت والتعب تع الصح! 💎"
                        h4 = f"4. ضياع للمال لو كان ما تطلبش [{new_prod}] بسعر الجملة تع اليوم! 💸"
                        h5 = f"5. الكمية راهي تخلص بزاف.. شوف وعلاش ڨاع الناس تطلب في هذا المنتج المدهش! 📦"
                        
                        testing_budget_usd = 20.0
                        exchange_rate_parallel = 240.0
                        testing_budget_dzd = testing_budget_usd * exchange_rate_parallel
                        
                        st.session_state['premium_marketing_hub'] = {
                            'merchant': current_merchant,
                            'product_name': new_prod,
                            'copy_dz': copy_dz,
                            'copy_ar': copy_ar,
                            'copy_short': copy_short,
                            'hooks': [h1, h2, h3, h4, h5],
                            'budget_usd': testing_budget_usd,
                            'budget_dzd': testing_budget_dzd
                        }
                        
                        time.sleep(0.5)
                        st.rerun()
                    except: st.error("المنتج موجود مسبقاً في المخزون.")
        with col_view:
            st.subheader("📋 حالة السلع المتوفرة حالياً:")
            stock_df = pd.read_sql("SELECT * FROM store_stock", conne)
            if not stock_df.empty:
                st.dataframe(stock_df, use_container_width=True)
                
                # === إضافة مؤشر المخزون الناري المتوهج ===
                def render_neon_stock_fire_bar(df_data):
                    st.markdown("<p style='font-size: 14px; color: #b0b0b0; margin-top: 15px;'>🔥 مؤشر تدفق المستودع المباشر (تحديث لحظي النيون):</p>", unsafe_allow_html=True)
                    max_qty = int(df_data['available_qty'].max()) if not df_data.empty else 100
                    if max_qty < 30: max_qty = 30
                    
                    for _, row in df_data.iterrows():
                        p_name = row['product_name']
                        p_qty = int(row['available_qty'])
                        width_pct = max(6, min(100, int((p_qty / max_qty) * 100)))
                        
                        if p_qty < 5:
                            bar_color, shadow_color, status_text = "#ff0055", "rgba(255, 0, 85, 0.9)", "🚨 خطر - مخزون حرج جداً!"
                        elif 5 <= p_qty <= 15:
                            bar_color, shadow_color, status_text = "#ffcc00", "rgba(255, 204, 0, 0.8)", "⚠️ انتباه - مخزون متوسط"
                        else:
                            bar_color, shadow_color, status_text = "#00ff66", "rgba(0, 255, 102, 0.8)", "✅ آمن - مستودع مستقر"
                            
                        neon_html = f"""
                        <div style="margin-bottom: 12px; background: #0f0f12; padding: 10px; border-radius: 8px; border: 1px solid #222;">
                            <div style="display: flex; justify-content: space-between; font-size: 13px; color: #fff; margin-bottom: 6px;">
                                <span><strong>{p_name}</strong> <span style="color: #888;">({p_qty} قطعة)</span></span>
                                <span style="color: {bar_color}; text-shadow: 0 0 8px {bar_color}; font-weight: bold; font-size: 12px;">{status_text}</span>
                            </div>
                            <div style="width: 100%; background-color: #1a1a24; border-radius: 5px; overflow: hidden; height: 8px;">
                                <div style="width: {width_pct}%; background-color: {bar_color}; height: 8px; border-radius: 5px; box-shadow: 0 0 12px {shadow_color}; transition: all 0.4s ease-in-out;"></div>
                            </div>
                        </div>
                        """
                        st.write(neon_html, unsafe_allow_html=True)
                
                render_neon_stock_fire_bar(stock_df)
                
                st.markdown("---")
                st.write("🗑️ **قسم محو وإزالة السلع من المستودع:**")
                delete_prod = st.selectbox("اختر السلعة المراد محوها نهائياً:", stock_df['product_name'])
                if st.button("❌ محو السلعة المحددة"):
                    cursor.execute("DELETE FROM store_stock WHERE product_name = ?", (delete_prod,))
                    conne.commit(); st.success(f"🗑️ تم محو السلعة [{delete_prod}] من المخزون بنجاح!"); time.sleep(0.5); st.rerun()
                
                low_stock = stock_df[stock_df['available_qty'] <= 5]
                if not low_stock.empty:
                    st.markdown("---")
                    st.write("<h3 style='color: #ff007f !important; text-shadow: 0 0 10px #ff007f;'>🚨 تنبيه: سلع أوشكت على النفاذ!</h3>", unsafe_allow_html=True)
                    st.dataframe(low_stock)
            else: st.info("مستودعك خالي تماماً حالياً.")

        # === دمج وتطوير منصة بطاقات الاستهداف والإعلانات الذكية للسلع الجديدة ===
        if st.session_state.get("show_premium_ai_hub", False) and "active_ai_marketing_prod" in st.session_state:
            st.markdown("---")
            hub_data = st.session_state.get('premium_marketing_hub', {})
            if hub_data:
                prod_name = hub_data['product_name']
                merchant_user = hub_data['merchant']
                st.write(f"""
                <div style="background: linear-gradient(135deg, #0c0822, #180030); border: 2px solid #00fff0; border-radius: 16px; padding: 20px; text-align: right; direction: rtl;">
                    <h3 style="color: #ffffff; margin: 0;">📡 PREMIUM AI MARKETING HUB // المسؤول: {merchant_user}</h3>
                    <p style="color: #a4a4ba; font-size: 13px; margin: 5px 0 0 0;">تم تأمين السلعة [{prod_name}] تلقائياً وبناء بطاقة فحص مبيعاتها السريعة في المستودع بنجاح.</p>
                </div>
                """, unsafe_allow_html=True)
                
                t_c, t_h, t_b = st.tabs(["📝 النصوص الإعلانية", "⚡ العناوين الصادمة", "💰 الميزانية المقترحة"])
                with t_c:
                    st.text_area("قالب الدارجة:", value=hub_data['copy_dz'], height=120, disabled=True)
                with t_h:
                    for h in hub_data['hooks']: st.info(h)
                with t_b:
                    st.metric(label="ميزانية الفحص اليومية", value=f"{hub_data['budget_usd']} USD", delta=f"{hub_data['budget_dzd']} DA")
                if st.button("❌ إغلاق المعاينة التسويقية"):
                    del st.session_state["active_ai_marketing_prod"]
                    st.session_state["show_premium_ai_hub"] = False
                    st.rerun()
    elif choice == "🧼 مطهر ملفات المبيعات وإحصائيات الولايات":
        st.write("<h1 style='font-size: 32px; color: #00fff0; text-shadow: 0 0 15px #00fff0;'>🧼 نظام التطهير وعرض مقارنة البيانات والولايات</h1>", unsafe_allow_html=True)
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
                        st.warning(f"تم حذف {len(duplicated_rows)} سطر مكرر!"); st.dataframe(duplicated_rows)
                    if not bad_prices.empty:
                        st.error(f"تم حذف {len(bad_prices)} سطر أسعار سالبة!"); st.dataframe(bad_prices)
                else: st.info("الملف سليم تماماً ولا يحتوي على أخطاء.")
            st.markdown("---"); render_data_insights(df); st.markdown("---")
            st.subheader("📈 المخططات البيانية الملونة للولايات والمبيعات:")
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                st.write("💰 حجم المبيعات الإجمالي الحقيقي لكل منتج:")
                st.bar_chart(data=df, x='product_name', y='total_row_sales', color='#00ffcc')
            with chart_col2:
                wilaya_col = None
                for col in df.columns:
                    if 'address' in col.lower() or 'wilaya' in col.lower() or 'ولاية' in col:
                        wilaya_col = col; break
                if wilaya_col:
                    st.write(f"🗺️ حجم الشحن والمبيعات حسب الولايات الجزائرية:")
                    st.bar_chart(data=df, x=wilaya_col, y='total_row_sales', color='#ff007f')
                else: st.info("💡 نصيحة: سمّ عمود السكن في ملفك باسم 'wilaya' ليظهر مخطط فرز الولايات.")
            csv_buffer = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 تحميل ملف المبيعات المطهّر بالكامل", data=csv_buffer, file_name="cleaned_neon_sales.csv", mime="text/csv")

    elif choice == "🚀 مولّد الحملات والتخطيط التسويقي (AI)":
        # === إضافات المستودع ومطهر البيانات ومولد حملات الـ AI ===
        def render_marketing_hub_cyber_edition():
            st.write("<h1 style='font-size: 32px; color: #00fff0; text-shadow: 0 0 15px #00fff0;'>🚀 منصة التسويق السيبرانية وفحص الحملات الذكية AI</h1>", unsafe_allow_html=True)
            
            col_input, col_output = st.columns(2)
            with col_input:
                st.subheader("⚙️ موجه الأتمتة الإعلانية:")
                prod_title = st.text_input("اسم المنتج المراد تسويقه:", value="خلاط كهربائي محمول ذكي")
                prod_desc = st.text_area("وصف مختصر أو مميزات السلعة الرئيسية:", value="شحن سريع، شفرات حادة من الفولاذ، بطارية تدوم طويلاً، مثالي للرياضيين والمكتب.")
                prod_price = st.number_input("سعر بيع المنتج النهائي في الجزائر (DA):", min_value=100, value=3500)
                daily_budget = st.number_input("الميزانية الإعلانية اليومية المستهدفة (USD):", min_value=5, value=20)
                platform_choice = st.radio("🎯 منصة إطلاق الإعلان المستهدفة:", ["Facebook Ads", "TikTok Ads"], horizontal=True)
                run_generation = st.button("✨ تشغيل الأتمتة وصياغة الحملة الفاخرة")
                
            with col_output:
                st.subheader("📱 مستعرض المنشورات والبطاقات الزجاجية المفتوحة:")
                if run_generation or 'cyber_hub_active' in st.session_state:
                    st.session_state['cyber_hub_active'] = True
                    
                    # 5. عداد تقييم قوة الإعلان (AI Ad Score Meter)
                    score = 40
                    if len(prod_title) > 5: score += 20
                    if len(prod_desc) > 30: score += 25
                    if "شحن" in prod_desc or "ضمان" in prod_desc or "سريع" in prod_desc: score += 10
                    score = min(100, score)
                    
                    if score >= 80:
                        meter_color, meter_text = "#00ff66", "🔥 إعلان قوي جداً وجاذب للمستهلك!"
                    elif 50 <= score < 80:
                        meter_color, meter_text = "#ffcc00", "⚠️ إعلان متوسط القوة بحاجة لميزات تنافسية إضافية."
                    else:
                        meter_color, meter_text = "#ff0055", "🚨 إعلان ضعيف! أضف كلمات دلالية مثل (شحن مجاني، ضمان، توصيل)."
                    
                    st.write(f"""
                    <div style="background: #0f0f14; border: 1px solid #222; padding: 12px; border-radius: 8px; margin-bottom: 20px; direction: rtl; text-align: right;">
                        <span style="color: #aaa; font-size: 12.5px;">📊 عداد قوة الإعلان الذكي (AI Ad Score):</span>
                        <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: bold; color: {meter_color}; margin-top: 4px; margin-bottom: 4px;">
                            <span>معدل الجاذبية المتوقع: {score}%</span>
                            <span>{meter_text}</span>
                        </div>
                        <div style="width: 100%; background: #222; height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="width: {score}%; background: {meter_color}; height: 6px; box-shadow: 0 0 10px {meter_color}; transition: width 0.5s ease;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # إنشاء التبويبات السيبرانية الأربعة لتنظيم كروت العرض الزجاجية المفتوحة بالكامل وبكامل طولها الطبيعي
                    t_angles, t_script, t_radar, t_roi = st.tabs([
                        "🎯 1. زوايا البيع النفسية", 
                        "🎬 2. سيناريو الفيديو بالثواني", 
                        "📡 3. فلاتر الاستهداف والولايات", 
                        "💎 4. العوائد والأرباح المتوقعة"
                    ])
                    
                    with t_angles:
                        st.write("🔒 **الإعلانات الحرة الممتدة بكامل الطول داخل الكروت الزجاجية المتوهجة بالأرجواني:**")
                        ang1 = f"عيت من الخلاطات الكبار ل يرفدو البلاصة ويديرو الحس؟ 🤦 واش رايك في خلاط ذكي محمول يروح معاك وين تروح! **{prod_title}** يخلطلك العواصير والبروتين ديالك في ثواني وبلا تعب، خفيف وشاحن سريع وعملي بزاف تهنى من المشكل اليوم!"
                        ang2 = f"الأناقة تلتقي مع الأداء العالي الرائع ✨ ارتقِ بأسلوب حياتك اليومي مع **[{prod_title}]**، التصميم الزجاجي الفريد واللمسة العصرية تمنحك برستيج خاص ومميز في مكتبك أو النادي الرياضي، إنه ليس مجرد خلاط بل عنوان لتميزك الفاخر."
                        ang3 = f"🚨 تخفيض صدمة ومؤقت لفترة جد محدودة! المنتج الأكثر طلباً **[{prod_title}]** متوفر الآن بخصم خاص يعادل 30% من السعر الأصلي والمخزون أوشك على النفاذ تماماً بالمستودع! اطلب الآن واستفد من التوصيل السريع والدفع عند الاستلام!"
                        
                        # حقن البطاقات الزجاجية المفتوحة والمصبوغة نيونياً بخطوط واضحة عريضة لسهولة القراءة والنسخ
                        st.markdown(f"""<div style="background: rgba(255, 0, 255, 0.02); border: 1px solid #ff00ff; border-radius: 10px; padding: 14px; margin-bottom: 12px; box-shadow: 0 0 10px rgba(255, 0, 255, 0.1); direction: rtl; text-align: right;"><b style="color: #ff00ff; font-size: 14px;">🛠️ زاوية حل المشكلة (بالدارجة الجزائرية):</b><br><p style="color: #ffffff; font-size: 14.5px; line-height: 1.6; font-weight: 500; margin-top: 6px; margin-bottom: 0;">{ang1}</p></div>""", unsafe_allow_html=True)
                        st.download_button(label="📥 نسخ كود نص حل المشكلة نقياً", data=ang1.encode('utf-8'), file_name="angle_problem.txt", mime="text/plain")
                        
                        st.markdown(f"""<div style="background: rgba(255, 0, 255, 0.02); border: 1px solid #ff00ff; border-radius: 10px; padding: 14px; margin-bottom: 12px; box-shadow: 0 0 10px rgba(255, 0, 255, 0.1); direction: rtl; text-align: right;"><b style="color: #ff00ff; font-size: 14px;">💎 زاوية الفخامة والبرستيج الاجتماعي:</b><br><p style="color: #ffffff; font-size: 14.5px; line-height: 1.6; font-weight: 500; margin-top: 6px; margin-bottom: 0;">{ang2}</p></div>""", unsafe_allow_html=True)
                        st.download_button(label="📥 نسخ كود نص البرستيج نقياً", data=ang2.encode('utf-8'), file_name="angle_prestige.txt", mime="text/plain")
                        
                        st.markdown(f"""<div style="background: rgba(255, 0, 255, 0.02); border: 1px solid #ff00ff; border-radius: 10px; padding: 14px; margin-bottom: 12px; box-shadow: 0 0 10px rgba(255, 0, 255, 0.1); direction: rtl; text-align: right;"><b style="color: #ff00ff; font-size: 14px;">🚨 زاوية العرض الاستعجالي الصادم:</b><br><p style="color: #ffffff; font-size: 14.5px; line-height: 1.6; font-weight: 500; margin-top: 6px; margin-bottom: 0;">{ang3}</p></div>""", unsafe_allow_html=True)
                        st.download_button(label="📥 نسخ كود نص العرض الاستعجالي نقياً", data=ang3.encode('utf-8'), file_name="angle_flash_sale.txt", mime="text/plain")
                        
                    with t_script:
                        st.write("🎬 **السيناريو الكامل والاحترافي لتصوير الإعلان متمدد بالكامل حسب الثواني المقترحة:**")
                        s1 = f"**[00:00 - 00:03] الـ Hook الصادم:** لقطة سريعة لشخص يعاني مع خلاط قديم ثقيل يصدر ضوضاء، مع كتابة نص عريض (حبس! هاد السلعة غادي تبدل حياتك تع الصح! 😱)"
                        s2 = f"**[00:03 - 00:10] عرض المشكلة والحاجة:** الخلاطات الكبار يعطلو في الكوزينة وصعاب في الغسيل خاصة كي تكون زربان ورايح للخدمة أو لـ لsub سبور ونشاطك الرياضي اليومي."
                        s3 = f"**[00:10 - 00:20] استعراض السلعة وطريقة العمل:** لقطة مقربة لمنتج **[{prod_title}]** وهو يطحن المكونات والفاكهة بسلاسة وسرعة فائقة بفضل الشفرات الفولاذية الحادة والبطارية القوية المستقرة."
                        s4 = f"**[00:20 - 00:30] الـ Call To Action النهائي:** التوصيل متوفر وسريع لـ 58 ولاية جزائرية كاملة لباب دارك، والدفع حتى تستلم وتفحص السلعة بيدك 🚚 اضغط على زر الرابط واطلب ديالك الآن!"
                        
                        full_script_markdown = f"{s1}\n\n{s2}\n\n{s3}\n\n{s4}"
                        
                        st.markdown(f"""<div style="background: rgba(0, 255, 240, 0.02); border: 1px solid #00fff0; border-radius: 10px; padding: 16px; margin-bottom: 12px; box-shadow: 0 0 10px rgba(0, 255, 240, 0.1); direction: rtl; text-align: right;"><b style="color: #00fff0; font-size: 14px;">🎥 خطة إنتاج وفيديو السيناريو (Ad Video Script):</b><br><div style="color: #ffffff; font-size: 14px; line-height: 1.8; margin-top: 10px; white-space: pre-line;">{full_script_markdown}</div></div>""", unsafe_allow_html=True)
                        st.download_button(label="📥 تحميل ملف السيناريو بالثواني كاملاً", data=full_script_markdown.encode('utf-8'), file_name="video_script.txt", mime="text/plain")
        render_marketing_hub_cyber_edition()
        
    # قفل فوري لقناة الاتصال بالـ DB مع نهاية المتجر لتجنب حدوث Lock حماية للـ RAM
    conne.close()
