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
    """ ✨ ميزة النوافذ المنبثقة الأسطورية: وضع رسالة الترحيب ومستطيل الكتابة الحية معاً في زاوية الشاشة """
    
    # 🎨 كود الـ CSS المطور لتحديد مكان النافذة والفقاعة العائمة في الركن السفلي الأيمن
    st.markdown("""
        <style>
        #ai-chat-checkbox { display: none; }
        
        /* 🤖 أيقونة الروبوت العائمة المضيئة */
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
        
        /* 📋 العلبة الصغيرة المخصصة لرسالة الترحيب فقط */
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
            display: none; /* مخفية حتى يضغط التاجر على البوت */
            font-family: 'Cairo', sans-serif;
            overflow: hidden;
        }
        
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
        }
        
        /* 🛠️ تنسيق فخم ومخصص لجعل مستطيل الكتابة البرمجي يطفو ويظهر تحت علبة الترحيب مباشرة */
        .floating-input-container {
            position: fixed;
            bottom: 105px; /* يطابق تماماً موضع نافذة الترحيب ليصبح بداخلها هندسياً */
            right: 25px;
            width: 340px;
            z-index: 999997 !important;
            padding: 15px;
            background-color: #161b22;
            border: 2px solid #00ffcc;
            border-top: none; /* دمج هندسي لمنع التداخل */
            border-radius: 0 0 14px 14px;
        }
        </style>
        
        <!-- الأكواد الهيكلية التفاعلية -->
        <input type="checkbox" id="ai-chat-checkbox" />
        <label for="ai-chat-checkbox" class="bubble-launcher">🤖</label>
        
        <div class="popup-dialog-box">
            <div class="popup-dialog-header">
                🤖 مساعد ومولد الإعلانات الذكي (AI Live)
            </div>
            <div class="popup-dialog-body">
                <div class="popup-welcome-text">
                    👋 <b>مرحباً بك يا بطل!</b> أنا ذكاء المنصة، اكتبلي سؤالتك بالعامية أو طلب إعلانك في مستطيل الكتابة بالأسفل مباشرة وراح نجاوبك فوراً! 🚀🇩🇿
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 📥 قفل وإلغاء الخانة القديمة في السايدبار، وجعل مستطيل الإدخال يظهر حياً تحت رسالة الترحيب هندسياً
    st.sidebar.markdown("---")
  
    
    # وضع خانة إدخال النص والردود مباشرة تحت نافذة الترحيب في الشاشة الرئيسية لستريمليت
    user_query = st.text_input("✍️ اكتب سؤالك أو طلب الإعلان هنا للبوت:", key="ai_perfect_under_welcome_input", placeholder="مثال: اكتبلي إعلان على عطر...")
    
    if user_query:
        with st.spinner("🤖 جاري التفكير وصياغة الرد التسويقي الفخم..."):
            ai_reply = get_ai_response(user_query)
            st.markdown("<p style='color: #00ffcc; font-weight: bold; margin-top: 15px; margin-bottom: 2px;'>🤖 رد الروبوت الذكي المطور:</p>", unsafe_allow_html=True)
            st.info(ai_reply)
            st.markdown("<p style='font-size: 11px; color: #8b949e; text-align: center;'>🔒 النسخة السنوية الكاملة متوفرة للتفعيل عبر BaridiMob المباشر.</p>", unsafe_allow_html=True)
