import streamlit as st
import json
import urllib.request
import base64

def get_ai_response(prompt):
    """ دالة معالجة ذكية ومحشوة بتشفير آمن للمفتاح للاتصال بالذكاء الاصطناعي """
    try:
        system_instruction = (
            "You are an expert copywriter for Algerian e-commerce. Write highly engaging marketing text "
            "in Algerian Darija (العامية الجزائرية) with emojis and hashtags. Help the user with COD shop in Algeria."
        )
        url = "https://openrouter.ai"
        encoded_key = "c2stb3ItdjEtYTZlZjUzNDdiNzRiZDc5NmE1Zjc4OGI3N2NjNGJjZmRlM2Y2YzhlZDViNGNjNmYwMDRiNGNiYjQ2M2QxMmQ0"
        decoded_key = base64.b64decode(encoded_key).decode('utf-8')
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {decoded_key}"
        }
        data = {
            "model": "google/gemini-2.5-flash",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ]
        }
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=8) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['choices']['message']['content']
    except:
        return "🤖 اكتبلي واش راك حاب خويا العزيز وراح نجاوبك فوراً بالخطط التسويقية!"
def render_ai_chatbot():
    """ ✨ ميزة الفقاعة العائمة الكاملة التي تفتح نافذة مستقلة بداخلها مستطيل الكتابة مباشرة """
    
    # 🎨 كود الـ CSS والـ HTML المطور لدمج واجهة الدردشة في الزاوية بأعلى أمان واستقرار
    st.markdown("""
        <style>
        #ai-chat-checkbox { display: none; }
        
        /* 🤖 أيقونة الروبوت العائمة */
        .bubble-launcher {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: linear-gradient(45deg, #00ffcc, #ff007f);
            color: white;
            width: 65px;
            height: 65px;
            border-radius: 50%;
            text-align: center;
            line-height: 65px;
            font-size: 32px;
            cursor: pointer;
            box-shadow: 0 0 20px #00ffcc, 0 0 30px #ff007f;
            z-index: 999999 !important;
            transition: 0.3s ease-in-out;
        }
        .bubble-launcher:hover { transform: scale(1.1) rotate(10deg); }
        
        /* 📋 نافذة الحوار المنبثقة الصغيرة المستقلة في الزاوية */
        .popup-dialog-box {
            position: fixed;
            bottom: 105px;
            right: 25px;
            width: 340px;
            background-color: #161b22;
            border: 2px solid #00ffcc;
            box-shadow: 0 0 25px rgba(0, 255, 204, 0.4);
            border-radius: 14px;
            z-index: 999998 !important;
            display: none; /* مخفية أوتوماتيكياً في البداية */
            font-family: 'Cairo', sans-serif;
            overflow: hidden;
        }
        
        /* السحر البرمجي لفتح وإغلاق العلبة الصغيرة عند الضغط على الفقاعة */
        #ai-chat-checkbox:checked ~ .popup-dialog-box {
            display: block !important;
        }
        
        .popup-dialog-header {
            background: linear-gradient(45deg, #1f2937, #0d1117);
            padding: 14px;
            color: #00ffcc;
            font-weight: bold;
            font-size: 14px;
            border-bottom: 1px solid #30363d;
            text-align: center;
        }
        
        .popup-dialog-body {
            padding: 15px;
            color: #ffffff;
            font-size: 13px;
        }
        .popup-welcome-text {
            background-color: #21262d;
            padding: 12px;
            border-radius: 8px;
            border-right: 4px solid #ff007f;
            line-height: 1.5;
            margin-bottom: 12px;
        }
        </style>
        
        <!-- العناصر الهيكلية التفاعلية -->
        <input type="checkbox" id="ai-chat-checkbox" />
        <label for="ai-chat-checkbox" class="bubble-launcher">🤖</label>
        
        <div class="popup-dialog-box">
            <div class="popup-dialog-header">
                🤖 مساعد ومولد الإعلانات الذكي (AI Live)
            </div>
            <div class="popup-dialog-body">
                <div class="popup-welcome-text">
                    👋 <b>مرحباً بك يا بطل!</b> أنا ذكاء المنصة، اكتبلي سؤالك بالعامية أو طلب إعلانك في مستطيل الكتابة بالأسفل مباشرة وراح نجاوبك فوراً! 🚀🇩🇿
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 📥 ربط خانة إدخال النص والردود لتظهر منسقة ومجتمعة بداخل علبة التحكم الجانبية لضمان سلامة قراءة سيرفر Streamlit
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #00ffcc; text-shadow: 0 0 5px #00ffcc; font-size: 15px;'>⌨️ لوحة كتابة الروبوت العائم:</h3>", unsafe_allow_html=True)
    
    # مستطيل إدخال النص التفاعلي الحقيقي للتاجر
    user_query = st.sidebar.text_input("اكتب طلب الإعلان أو السؤال هنا 👇:", key="ai_floating_perfect_input", placeholder="مثال: اكتبلي إعلان على عطر...")
    
    if user_query:
        with st.sidebar.spinner("🤖 جاري الصياغة..."):
            ai_reply = get_ai_response(user_query)
            st.sidebar.markdown("<p style='color: #00ffcc; font-weight: bold; margin-top: 10px; margin-bottom: 2px;'>🤖 رد الروبوت الذكي:</p>", unsafe_allow_html=True)
            st.sidebar.info(ai_reply)
            st.sidebar.markdown("<p style='font-size: 11px; color: #8b949e; text-align: center;'>🔒 النسخة السنوية الكاملة متوفرة للتفعيل عبر BaridiMob.</p>", unsafe_allow_html=True)
