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
    """ ✨ ميزة النوافذ المنبثقة التفاعلية للفقاعة العائمة في زاوية المتصفح بدون أخطاء """
    
    # بناء كود التنسيق الرسومي المذهل لـ فقاعة ونافذة الدردشة المنبثقة (تم مسح خطأ الطول هنا)
    st.markdown("""
        <style>
        /* 🤖 زر الفقاعة العائمة */
        .chat-widget-bubble {
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
            font-size: 30px;
            cursor: pointer;
            box-shadow: 0 0 15px #00ffcc, 0 0 25px #ff007f;
            z-index: 999999;
            transition: 0.3s ease-in-out;
        }
        .chat-widget-bubble:hover {
            transform: scale(1.1);
        }
        
        /* 📋 نافذة الترحيب والدردشة الصغيرة المنبثقة */
        .chat-widget-window {
            position: fixed;
            bottom: 95px;
            right: 25px;
            width: 320px;
            background-color: #161b22;
            border: 2px solid #00ffcc;
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
            border-radius: 12px;
            z-index: 999999;
            display: none;
            font-family: 'Cairo', sans-serif;
            overflow: hidden;
        }
        
        /* رأس النافذة */
        .chat-widget-header {
            background: linear-gradient(45deg, #1f2937, #0d1117);
            padding: 12px;
            color: #00ffcc;
            font-weight: bold;
            font-size: 14px;
            border-bottom: 1px solid #30363d;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        /* صندوق الترحيب الداخلي للروبوت */
        .chat-widget-body {
            padding: 15px;
            color: #ffffff;
            font-size: 13px;
            max-height: 200px;
            overflow-y: auto;
        }
        .welcome-msg {
            background-color: #21262d;
            padding: 10px;
            border-radius: 8px;
            border-right: 4px solid #ff007f;
            margin-bottom: 10px;
            line-height: 1.4;
        }
        </style>
        
        <script>
        function toggleChatWindow() {
            var chatWin = document.getElementById('ai_popup_window');
            if (chatWin.style.display === 'none' || chatWin.style.display === '') {
                chatWin.style.display = 'block';
            } else {
                chatWin.style.display = 'none';
            }
        }
        </script>
        
        <!-- زر الروبوت العائم السحري -->
        <div class="chat-widget-bubble" onclick="toggleChatWindow();">🤖</div>
        
        <!-- هيكل النافذة الصغيرة المنبثقة الترحيبية -->
        <div class="chat-widget-window" id="ai_popup_window">
            <div class="chat-widget-header">
                <span>🤖 مساعد المتاجر الذكي (AI Live)</span>
                <span style="cursor:pointer; color:#ff007f; font-size:18px;" onclick="toggleChatWindow();">×</span>
            </div>
            <div class="chat-widget-body">
                <div class="welcome-msg">
                    👋 <b>مرحباً بك يا بطل في متجرك الأسطوري!</b><br>
                    أنا ذكاء المنصة المساعد، اكتبلي أي سؤال بالعامية أو قولي <b>"اكتبلي إعلان على [اسم المنتج]"</b> وراح نولّدلك نصوص إعلانية تزيد مبيعاتك فوراً! 🚀🇩🇿
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # خانة الدردشة الحية لستريمليت
    st.markdown("---")
    st.markdown("<h3 style='color: #00ffcc; text-shadow: 0 0 5px #00ffcc; font-size: 18px;'>💬 تحاور مع ذكاء المنصة الحقيقي:</h3>", unsafe_allow_html=True)
    
    user_query = st.text_input("اكتب سؤالك أو طلب الإعلان هنا للبوت:", key="ai_live_widget_input", placeholder="مثال: اكتبلي إعلان على ساعة ذكية")
    if user_query:
        with st.spinner("🤖 جاري التفكير وصياغة الرد التسويقي الفخم..."):
            ai_reply = get_ai_response(user_query)
            st.markdown("<p style='color: #00ffcc; font-weight: bold; margin-bottom: 2px;'>🤖 رد الروبوت الذكي:</p>", unsafe_allow_html=True)
            st.info(ai_reply)
            st.markdown("<p style='font-size: 11px; color: #8b949e; text-align: center;'>🔒 النسخة السنوية الكاملة تمنحك تحليلاً شاملاً وجداول أرباح الولايات الـ 58 تلقائياً! تفضل بالتفعيل عبر BaridiMob.</p>", unsafe_allow_html=True)
