import requests
import json

def send_otp_email(target_email, generated_otp):
    """
    إرسال رمز التحقق السري حياً عبر سيرفر Resend العالمي 
    باستخدام مفتاح الـ API الجديد وتخطي جدران حظر جوجل بالكامل.
    """
    url = "https://resend.com"
    
    headers = {
        "Authorization": "Bearer re_SYfDR44y_9LFmhnXNHTH7aksjCAgN8XAU",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": "NEXUS CENTRAL GATE <onboarding@resend.dev>",
        "to": target_email,
        "subject": f"🔒 رمز التحقق السري الخاص بك: {generated_otp}",
        "html": f"""
        <div style="direction: rtl; text-align: right; font-family: sans-serif; padding: 20px;">
            <h2>مرحباً بك في منصة NEXUS CENTRAL GATE v4</h2>
            <p>رمز التوثيق السري الخاص بإنشاء متجرك الإلكتروني هو:</p>
            <h1 style="color: #00fff0; letter-spacing: 2px;">{generated_otp}</h1>
            <p>يرجى إدخاله في الخانة المنبثقة حياً بالموقع لإتمام التسجيل الآمن.</p>
        </div>
        """
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code in:
            return True
        return False
    except Exception:
        return False
