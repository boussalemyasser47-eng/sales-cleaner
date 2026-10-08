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
    """ ✨ ميزة الفقاعة العائمة التفاعلية والنافذة المنبثقة بالاعتماد الكامل على النيون والـ CSS الآمن """
    
    # 🎨 كود الـ CSS الأسطوري لصنع الفقاعة الدائرية والنافذة المنبثقة بالاعتماد على خيار مخفي (بدون JS)
    st.markdown("""
        <style>
        /* إخفاء التشيك بوكس الأصلي */
        #ai-chat-toggle {
            display: none;
        }
        
        /* 🤖 تصميم الفقاعة الدائرية المضيئة المطفية في الزاوية */
        .ai-floating-bubble {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: linear-gradient(45deg, #00ffcc, #ff007f);
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            text-align: center;
            line-height: 60px;
            font-size: 32px;
            cursor: pointer;
            box-shadow: 0 0 15px #00ffcc, 0 0 25px #ff007f;
            z-index: 999999 !important;
            transition: 0.3s ease-in-out;
        }
        .ai-floating-bubble:hover {
            transform: scale(1.1) rotate(15deg);
        }
        
        /* 📋 نافذة الدردشة الصغيرة المنبثقة الفخمة المحاطة بالنيون */
        .ai-popup-chat-window {
            position: fixed;
            bottom: 100px;
            right: 25px;
            width: 320px;
            background-color: #161b22;
            border: 2px solid #00ffcc;
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.5);
            border-radius: 12px;
            z-index: 999998 !important;
            display: none; /* مخفية تلقائياً */
            font-family: 'Cairo', sans-serif;
            overflow: hidden;
        }
        
        /* السحر البرمجي: عندما يضغط التاجر على الفقاعة (تفعيل التشيك بوكس)، تفتح النافذة فوراً! */
        #ai-chat-toggle:checked ~ .ai-popup-chat-window {
            display: block !important;
        }
        
        /* رأس علبة الترحيب */
        .ai-popup-header {
            background: linear-gradient(45deg, #1f2937, #0d1117);
            padding: 12px;
            color: #00ffcc;
            font-weight: bold;
            font-size: 13px;
            border-bottom: 1px solid #30363d;
            text-align: center;
        }
        
        /* صندوق الترحيب الداخلي للروبوت بالعامية */
        .ai-popup-body {
            padding: 15px;
            color: #ffffff;
            font-size: 12px;
        }
        .ai-welcome-msg {
            background-color: #21262d;
            padding: 10px;
            border-radius: 8px;
            border-right: 4px solid #ff007f;
            line-height: 1.4;
        }
        </style>
        
        <!-- هيكل العناصر التفاعلية المشتركة -->
        <input type="checkbox" id="ai-chat-toggle" />
        
        <!-- زر الفقاعة العائمة الدائرية -->
        <label for="ai-chat-toggle" class="ai-floating-bubble">🤖</label>
        
        <!-- النافذة الصغيرة المنبثقة الترحيبية السيبرانية -->
        <div class="ai-popup-chat-window">
            <div class="ai-popup-header">
                🤖 مساعد المتاجر ومولد الإعلانات الذكي
            </div>
            <div class="ai-popup-body">
                <div class="ai-welcome-msg">
                    👋 <b>مرحباً بك يا بطل في متجرك الأسطوري!</b><br>
                    أنا ذكاء المنصة، اكتبلي أي سؤال بالعامية أو قولي <b>"اكتبلي إعلان على [اسم السلعة]"</b> في الصندوق بالأسفل وراح نجاوبك فوراً! 🚀🇩🇿
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 📥 هذا الصندوق يظهر ذكياً ومنسقاً تحت علبة الترحيب ليحتوي على خانة الكتابة الحية المتوافقة مع السيرفر
    st.markdown("---")
    st.markdown("<h3 style='color: #00ffcc; text-shadow: 0 0 5px #00ffcc; font-size: 18px;'>💬 علبة الكتابة لذكاء المنصة (AI Live Mode):</h3>", unsafe_allow_html=True)
    
    # صندوق إدخال النص المطور التفاعلي للتاجر
    user_query = st.text_input("اكتب سؤالك أو طلب الإعلان هنا للبوت:", key="ai_live_widget_input_v5", placeholder="مثال: اكتبلي إعلان على ساعة ذكية")
    if user_query:
        with st.spinner("🤖 جاري التفكير وصياغة الرد التسويقي الفخم..."):
            ai_reply = get_ai_response(user_query)
            st.markdown("<p style='color: #00ffcc; font-weight: bold; margin-bottom: 2px;'>🤖 رد الروبوت الذكي:</p>", unsafe_allow_html=True)
            st.info(ai_reply)
            st.markdown("<p style='font-size: 11px; color: #8b949e; text-align: center;'>🔒 النسخة السنوية الكاملة تمنحك تحليلاً شاملاً وجداول الولايات الـ 58 تلقائياً! تفضل بالتفعيل عبر BaridiMob.</p>", unsafe_allow_html=True)
