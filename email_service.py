import requests

def send_otp_email(target_email, generated_otp):
    """
    إرسال رمز التحقق السري حياً عبر سيرفر Mailjet المفتوح والحر 
    باستخدام بروتوكول HTTP Basic Auth لتخطي جدران حظر الدومين كلياً
    وجعل الأكواد تطير لأي تاجر عشوائي في الجزائر فوراً.
    """
    url = "https://mailjet.com"
    
    # مفاتيح الربط الحرة لـ Mailjet المأخوذة حياً من شاشتك
    api_key = "cab2a932ad6ae9beffc913732beed7bf"
    secret_key = "848fd9390fa1beae930c0b7f7d3739e9"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "Messages": [
            {
                "From": {
                    "Email": "boussalemyasser47@gmail.com",
                    "Name": "NEXUS CENTRAL GATE"
                },
                "To": [
                    {
                        "Email": target_email,
                        "Name": "Active Merchant"
                    }
                ],
                "Subject": f"🔒 رمز التحقق السري الخاص بك: {generated_otp}",
                "HTMLPart": f"""
                <div style="direction: rtl; text-align: right; font-family: sans-serif; padding: 20px; background-color: #050f14; border: 2px solid #00fff0; border-radius: 12px; max-width: 500px; margin: 0 auto;">
                    <h2 style="color: #00fff0; border-bottom: 1px solid #00fff0; padding-bottom: 10px;">مرحباً بك في منصة NEXUS CENTRAL GATE v4</h2>
                    <p style="color: #ffffff; font-size: 16px;">رمز التوثيق السري الخاص بإنشاء متجرك الإلكتروني الجديد هو:</p>
                    <div style="background: rgba(0, 255, 240, 0.1); border: 1px dashed #00fff0; border-radius: 8px; padding: 15px; text-align: center; margin: 20px 0;">
                        <h1 style="color: #ffaa00; letter-spacing: 5px; font-size: 38px; margin: 0; font-family: monospace;">{generated_otp}</h1>
                    </div>
                    <p style="color: #ffffff; font-size: 14px;">يرجى إدخاله في الخانة المنبثقة حياً بالموقع لإتمام التسجيل الآمن ومباشرة البيع.</p>
                </div>
                """
            }
        ]
    }
    
    try:
        # الاتصال بخادم Mailjet عبر ميكانيكية الـ Basic Authentication الموثقة
        response = requests.post(
            url, 
            auth=(api_key, secret_key), 
            headers=headers, 
            json=payload, 
            timeout=10
        )
        if response.status_code == 200 or response.status_code == 201:
            return True
        return False
    except Exception:
        return False

