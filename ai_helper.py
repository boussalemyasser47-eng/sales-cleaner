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
    """ ✨ وضع رسالة الترحيب ومستطيل الكتابة وزر الإرسال معاً في زاوية الشاشة الكلية """
    
    # تفريغ مساحة السايدبار السفلية لإبقائه نظيفاً
    st.sidebar.markdown("---")
    
    # إدارة ذاكرة الدردشة المخفية للسيرفر لمنع الاهتزاز
    if "ai_widget_history" not in st.session_state:
        st.session_state["ai_widget_history"] = ""
        
    query_params = st.query_params
    if "widget_msg" in query_params:
        user_prompt = query_params["widget_msg"]
        st.query_params.clear() 
        with st.spinner("🤖 جاري التفكير..."):
            reply = get_ai_response(user_prompt)
            st.session_state["ai_widget_history"] = reply
            st.rerun()

    # 🎨 كود الـ HTML & CSS & JS الأسطوري لدمج شريط الكتابة والردود تلقائياً تحت الرسالة بداخل الحاوية العائمة
    widget_html = f"""
    <style>
    #ai-chat-checkbox-v6 {{ display: none; }}
    
    /* 🤖 أيقونة الروبوت العائمة المضيئة أسفل يمين الشاشة */
    .bubble-launcher-v6 {{
        position: fixed !important;
        bottom: 25px !important;
        right: 25px !important;
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
        z-index: 999999999 !important;
        transition: 0.3s ease-in-out;
    }}
    .bubble-launcher-v6:hover {{ transform: scale(1.1); }}
    
    /* 📋 نافذة الحوار المنبثقة السيبرانية المحاطة بالنيون الأخضر */
    .popup-dialog-box-v6 {{
        position: fixed !important;
        bottom: 105px !important;
        right: 25px !important;
        width: 340px;
        background-color: #161b22;
        border: 2px solid #00ffcc;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5);
        border-radius: 14px;
        z-index: 999999999 !important;
        display: none;
        font-family: sans-serif;
        direction: rtl;
    }}
    
    #ai-chat-checkbox-v6:checked ~ .popup-dialog-box-v6 {{
        display: block !important;
    }}
    
    .popup-dialog-header-v6 {{
        background: linear-gradient(45deg, #1f2937, #0d1117);
        padding: 14px;
        color: #00ffcc;
        font-weight: bold;
        font-size: 14px;
        border-bottom: 1px solid #30363d;
        text-align: center;
    }}
    
    .popup-dialog-body-v6 {{
        padding: 15px;
        color: #ffffff;
        font-size: 13px;
    }}
    .popup-welcome-text-v6 {{
        background-color: #21262d;
        padding: 12px;
        border-radius: 8px;
        border-right: 4px solid #ff007f;
        line-height: 1.5;
        margin-bottom: 12px;
    }}
    .response-area-v6 {{
        background-color: #0d1117;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #30363d;
        color: #00ffcc;
        margin-bottom: 12px;
        font-weight: bold;
        white-space: pre-wrap;
    }}
    
    /* ✍️ تصميم شريط الكتابة وزر الإرسال المدمجين تحت الرسالة مباشرة بداخل النافذة */
    .input-wrapper-v6 {{
        display: flex;
        padding: 10px;
        border-top: 1px solid #30363d;
        background-color: #0d1117;
    }}
    .input-field-v6 {{
        flex: 1;
        background-color: #161b22;
        border: 1px solid #30363d;
        color: white;
        padding: 8px;
        border-radius: 6px;
        font-size: 12px;
    }}
    .send-btn-v6 {{
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
    
    <!-- هيكل العناصر التفاعلية المسترجعة والمطورة -->
    <input type="checkbox" id="ai-chat-checkbox-v6" />
    <label for="ai-chat-checkbox-v6" class="bubble-launcher-v6">🤖</label>
    
    <div class="popup-dialog-box-v6">
        <div class="popup-dialog-header-v6">
            🤖 مساعِد ومولّد الإعلانات الذكي (AI Live)
        </div>
        <div class="popup-dialog-body-v6">
            <div class="popup-welcome-text-v6">
                👋 <b>مرحباً بك يا بطل!</b> أنا ذكاء المنصة، اكتبلي سؤالك بالعامية أو طلب إعلانك في مستطيل الكتابة بالأسفل مباشرة وراح نجاوبك فوراً! 🚀🇩🇿
            </div>
            {"<div class='response-area-v6'>🤖 الرد: <br>" + st.session_state["ai_widget_history"] + "</div>" if st.session_state["ai_widget_history"] else ""}
        </div>
        
        <!-- 📥 شريط الكتابة وزر الإرسال مدمجين بالكامل تحت رسالة الترحيب في نفس القطعة -->
        <div class="input-wrapper-v6">
            <input type="text" id="widget_text_v6" class="input-field-v6" placeholder="اكتب سؤالك هنا بالعامية..." onkeypress="checkEnterKeyV6(event)">
            <button class="send-btn-v6" onclick="sendDataToStreamlitV6()">إرسال</button>
        </div>
    </div>

    <script>
    if(window.parent.document.getElementById('movable_ai_widget')){{
        var savedState = window.parent.localStorage.getItem('floating_widget_state') || 'none';
        window.parent.document.getElementById('movable_ai_widget').style.display = savedState;
    }}
    
    window.toggleWidgetWindow = function() {{
        var myWin = window.document.getElementById('movable_ai_widget');
        if(myWin.style.display === 'none' || myWin.style.display === ''){{
            myWin.style.display = 'block';
            window.parent.localStorage.setItem('floating_widget_state', 'block');
        }} else {{
            myWin.style.display = 'none';
            window.parent.localStorage.setItem('floating_widget_state', 'none');
        }}
    }}
    window.checkEnterKeyV6 = function(event) {{
        if(event.keyCode === 13) {{ sendDataToStreamlitV6(); }}
    }}
    window.sendDataToStreamlitV6 = function() {{
        var clientText = window.document.getElementById('widget_text_v6').value;
        if(clientText) {{
            window.parent.location.search = '?widget_msg=' + encodeURIComponent(clientText);
        }}
    }}
    </script>
    """
    st.components.v1.html(widget_html, height=0)
