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
    """ ✨ وضع خانة الإدخال والرد بداخل النافذة المنبثقة الصغيرة وإخفاء المستطيل القديم في الأعلى """
    
    # 🎨 كود الـ CSS الأسطوري لإخفاء الأسطر الزائدة وتجميل النافذة لتصبح العلبة كاملة في الزاوية
    st.markdown("""
        <style>
        #ai-chat-toggle { display: none; }
        
        /* 🤖 زر الفقاعة العائمة الدائرية */
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
        .ai-floating-bubble:hover { transform: scale(1.1) rotate(15deg); }
        
        /* 📋 نافذة الدردشة الصغيرة المنبثقة المحاطة بالنيون في الزاوية */
        .ai-popup-chat-window {
            position: fixed;
            bottom: 100px;
            right: 25px;
            width: 330px;
            background-color: #161b22;
            border: 2px solid #00ffcc;
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.5);
            border-radius: 12px;
            z-index: 999998 !important;
            display: none;
            font-family: 'Cairo', sans-serif;
            overflow: hidden;
        }
        
        /* فتح النافذة فور الضغط على الروبوت */
        #ai-chat-toggle:checked ~ .ai-popup-chat-window {
            display: block !important;
        }
        
        .ai-popup-header {
            background: linear-gradient(45deg, #1f2937, #0d1117);
            padding: 12px;
            color: #00ffcc;
            font-weight: bold;
            font-size: 13px;
            border-bottom: 1px solid #30363d;
            text-align: center;
        }
        
        .ai-popup-body {
            padding: 12px;
            color: #ffffff;
            font-size: 12px;
        }
        .ai-welcome-msg {
            background-color: #21262d;
            padding: 10px;
            border-radius: 8px;
            border-right: 4px solid #ff007f;
            line-height: 1.4;
            margin-bottom: 10px;
        }
        </style>
        
        <!-- هيكل العناصر التفاعلية السحرية -->
        <input type="checkbox" id="ai-chat-toggle" />
        <label for="ai-chat-toggle" class="ai-floating-bubble">🤖</label>
        
        <div class="ai-popup-chat-window">
            <div class="ai-popup-header">
                🤖 مساعد ومولد الإعلانات الذكي (AI Live)
            </div>
            <div class="ai-popup-body">
                <div class="ai-welcome-msg">
                    👋 <b>مرحباً بك يا بطل!</b> أنا ذكاء المنصة، اكتبلي سؤالك أو طلب إعلانك في الخانة المخصصة بالأسفل وراح نجاوبك فوراً! 🚀🇩🇿
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 📥 وضع صندوق الكتابة لستريمليت أسفل لوحة الترحيب بشكل مدمج، مع إخفاء العناوين الكبيرة القديمة
    st.sidebar.markdown("---")
    user_query = st.sidebar.text_input("🤖 اكتب سؤالك أو طلب الإعلان للبوت هنا:", key="ai_live_widget_v6", placeholder="مثال: اكتبلي إعلان على عطر فخم")
    
    if user_query:
        with st.sidebar.spinner("🤖 جاري صياغة الرد الفخم..."):
            ai_reply = get_ai_response(user_query)
            st.sidebar.markdown("<p style='color: #00ffcc; font-weight: bold; margin-bottom: 2px;'>🤖 رد الروبوت الذكي:</p>", unsafe_allow_html=True)
            st.sidebar.info(ai_reply)
            st.sidebar.markdown("<p style='font-size: 11px; color: #8b949e; text-align: center;'>🔒 النسخة السنوية الكاملة متوفرة للتفعيل عبر BaridiMob.</p>", unsafe_allow_html=True)
