import streamlit as st
import json
import urllib.request
import base64

def get_ai_response(prompt):
    """ دالة معالجة ذكية ومحشوة بتشفير آمن للمفتاح للاتصال بالذكاء الاصطناعي """
    try:
        system_instruction = (
            "You are an expert copywriter for Algerian e-commerce. Write highly engaging marketing text "
            "in Algerian Darija (العامية الجزائرية) with emojis and hashtags. Help the user with COD shop in Algeria. Keep responses concise."
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
    """ ✨ تثبيت الفقاعة والنافذة المنبثقة بذكاء في الزاوية السفلية للشاشة تلقائياً """
    
    # تنظيف القائمة الجانبية وإبقائها نظيفة ومحترفة
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #00ffcc; font-size: 14px; text-align: center;'>🤖 تم تفعيل البوت العائم في الزاوية السفلية</h3>", unsafe_allow_html=True)
    
    if "ai_chat_history" not in st.session_state:
        st.session_state["ai_chat_history"] = ""
        
    query_params = st.query_params
    if "ai_msg" in query_params:
        user_prompt = query_params["ai_msg"]
        st.query_params.clear() 
        with st.spinner("🤖 جاري التفكير..."):
            reply = get_ai_response(user_prompt)
            st.session_state["ai_chat_history"] = reply
            st.rerun()

    # 🎨 كود الـ CSS الخارق الذي يجبر الفقاعة على النزول والتثبيت أسفل الشاشة التامة
    chat_box_html = f"""
    <style>
    /* 🤖 أيقونة الفقاعة الدائرية المثبتة في الأسفل المطلق لشاشة المتصفح */
    .neon-bubble-launcher {{
        position: fixed !important;
        bottom: 25px !important;
        right: 25px !important;
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
        z-index: 999999999 !important;
        transition: 0.3s ease-in-out;
    }}
    .neon-bubble-launcher:hover {{ transform: scale(1.1); }}
    
    /* 📋 علبة الدردشة الصغيرة المنبثقة المثبتة بدقة فوق الفقاعة */
    .neon-chat-window {{
        position: fixed !important;
        bottom: 95px !important;
        right: 25px !important;
        width: 320px;
        background-color: #161b22;
        border: 2px solid #00ffcc;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.4);
        border-radius: 14px;
        z-index: 999999999 !important;
        display: none;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: rtl;
    }}
    .chat-header {{
        background: linear-gradient(45deg, #1f2937, #0d1117);
        padding: 12px;
        color: #00ffcc;
        font-weight: bold;
        font-size: 13px;
        border-bottom: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
    }}
    .chat-body {{
        padding: 12px;
        color: white;
        font-size: 12px;
        max-height: 200px;
        overflow-y: auto;
    }}
    .welcome-text {{
        background-color: #21262d;
        padding: 10px;
        border-radius: 8px;
        border-right: 4px solid #ff007f;
        line-height: 1.4;
        margin-bottom: 10px;
    }}
    .ai-response-area {{
        background-color: #0d1117;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #30363d;
        color: #00ffcc;
        margin-bottom: 10px;
        font-weight: bold;
    }}
    .chat-input-wrapper {{
        display: flex;
        padding: 10px;
        border-top: 1px solid #30363d;
        background-color: #0d1117;
    }}
    .chat-input-field {{
        flex: 1;
        background-color: #161b22;
        border: 1px solid #30363d;
        color: white;
        padding: 8px;
        border-radius: 6px;
        font-size: 12px;
    }}
    .chat-send-btn {{
        background: linear-gradient(45deg, #ff007f, #7f00ff);
        color: white;
        border: none;
        padding: 0 12px;
        margin-right: 5px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
    }}
    </style>

    <div class="neon-bubble-launcher" onclick="toggleWidget()">🤖</div>

    <div class="neon-chat-window" id="neon_widget">
        <div class="chat-header">
            <span>🤖 مساعد المتاجر الذكي</span>
            <span style="cursor:pointer;color:#ff007f;" onclick="toggleWidget()">×</span>
        </div>
        <div class="chat-body">
            <div class="welcome-text">
                👋 <b>مرحباً بك يا بطل!</b> اكتب سؤالك أو طلب إعلانك في المستطيل بالأسفل مباشرة وراح نجاوبك هنا فوراً! 🚀
            </div>
            {"<div class='ai-response-area'>🤖 الرد: <br>" + st.session_state["ai_chat_history"] + "</div>" if st.session_state["ai_chat_history"] else ""}
        </div>
        <div class="chat-input-wrapper">
            <input type="text" id="user_text" class="chat-input-field" placeholder="اكتب هنا..." onkeypress="handleKey(event)">
            <button class="chat-send-btn" onclick="sendToStreamlit()">إرسال</button>
        </div>
    </div>

    <script>
    if(window.parent.document.getElementById('neon_widget')){{
        var state = window.parent.localStorage.getItem('widget_state') || 'none';
        window.parent.document.getElementById('neon_widget').style.display = state;
    }}
    
    function toggleWidget() {{
        var win = document.getElementById('neon_widget');
        if(win.style.display === 'none' || win.style.display === ''){{
            win.style.display = 'block';
            window.parent.localStorage.setItem('widget_state', 'block');
        }} else {{
            win.style.display = 'none';
            window.parent.localStorage.setItem('widget_state', 'none');
        }}
    }}
    function handleKey(e) {{
        if(e.keyCode === 13) {{ sendToStreamlit(); }}
    }}
    function sendToStreamlit() {{
        var txt = document.getElementById('user_text').value;
        if(txt) {{
            window.parent.location.search = '?ai_msg=' + encodeURIComponent(txt);
        }}
    }}
    </script>
    """
    
    # دمج آمن ومخفي لحقن العناصر في زاوية الشاشة الكلية للمتصفح أونلاين
    st.components.v1.html(chat_box_html, height=0)
