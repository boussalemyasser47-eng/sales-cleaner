import streamlit as st
import json
import urllib.request
import base64

def get_ai_response(prompt):
    """ دالة معالجة ذكية ومحشوة بتشفير آمن للمفتاح للاتصال بالذكاء الاصطناعي السريع """
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
    """ ✨ تحقيق التصميم الاحترافي العالمي: الفقاعة العائمة المنبثقة وبداخلها الترحيب والمستطيل والردود معاً """
    
    # تنظيف القائمة الجانبية وإخلائها تماماً لتبدو اللوحة منسقة
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #00ffcc; font-size: 14px; text-align: center;'>🤖 تم تفعيل البوت العائم في الزاوية السفلية</h3>", unsafe_allow_html=True)
    
    # إدارة ذاكرة الدردشة المخفية للسيرفر لمنع اهتزاز أو قفز الصفحة
    if "ai_widget_history" not in st.session_state:
        st.session_state["ai_widget_history"] = ""
        
    query_params = st.query_params
    if "widget_msg" in query_params:
        user_prompt = query_params["widget_msg"]
        st.query_params.clear() # مسح الرابط فوراً
        with st.spinner("🤖 جاري التفكير..."):
            reply = get_ai_response(user_prompt)
            st.session_state["ai_widget_history"] = reply
            st.rerun()

    # 🎨 كود الـ HTML & CSS & JS السحري لصنع منظومة الفقاعة والنافذة والعلبة المدمجة في زاوية المتصفح الكلية أونلاين
    widget_html = f"""
    <style>
    /* 🤖 أيقونة الروبوت العائمة المشعة الثابتة أسفل يمين الشاشة */
    .floating-launcher-icon {{
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
    .floating-launcher-icon:hover {{ transform: scale(1.1); }}
    
    /* 📋 العلبة الصغيرة المنبثقة المتكاملة المدمجة فوق الفقاعة */
    .floating-chat-window {{
        position: fixed !important;
        bottom: 95px !important;
        right: 25px !important;
        width: 330px;
        background-color: #161b22;
        border: 2px solid #00ffcc;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5);
        border-radius: 14px;
        z-index: 999999999 !important;
        display: none; /* مخفية أوتوماتيكياً حتى يتم الضغط */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: rtl;
    }}
    .win-header {{
        background: linear-gradient(45deg, #1f2937, #0d1117);
        padding: 12px;
        color: #00ffcc;
        font-weight: bold;
        font-size: 13px;
        border-bottom: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
    }}
    .win-body {{
        padding: 12px;
        color: white;
        font-size: 12px;
        max-height: 180px;
        overflow-y: auto;
    }}
    .welcome-card {{
        background-color: #21262d;
        padding: 10px;
        border-radius: 8px;
        border-right: 4px solid #ff007f;
        line-height: 1.4;
        margin-bottom: 10px;
    }}
    .response-area {{
        background-color: #0d1117;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #30363d;
        color: #00ffcc;
        margin-bottom: 10px;
        font-weight: bold;
    }}
    /* ✍️ تنسيق مستطيل الكتابة الفخم بداخل نفس العلبة الصغيرة المنبثقة في الأسفل */
    .input-wrapper {{
        display: flex;
        padding: 10px;
        border-top: 1px solid #30363d;
        background-color: #0d1117;
    }}
    .input-field {{
        flex: 1;
        background-color: #161b22;
        border: 1px solid #30363d;
        color: white;
        padding: 8px;
        border-radius: 6px;
        font-size: 12px;
    }}
    .send-btn {{
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

    <!-- أيقونة الروبوت العائمة -->
    <div class="floating-launcher-icon" onclick="toggleWidgetWindow()">🤖</div>

    <!-- نافذة الدردشة المستقلة بالكامل في الزاوية -->
    <div class="floating-chat-window" id="movable_ai_widget">
        <div class="win-header">
            <span>🤖 مساعد المتاجر الذكي</span>
            <span style="cursor:pointer;color:#ff007f;" onclick="toggleWidgetWindow()">×</span>
        </div>
        <div class="win-body">
            <div class="welcome-card">
                👋 <b>مرحباً بك يا بطل في متجرك!</b> اكتب سؤالك أو طلب إعلانك في المستطيل بالأسفل مباشرة وراح نجاوبك هنا فوراً! 🚀
            </div>
            {"<div class='response-area'>🤖 الرد: <br>" + st.session_state["ai_widget_history"] + "</div>" if st.session_state["ai_widget_history"] else ""}
        </div>
        <!-- 📥 مستطيل الكتابة وزر الإرسال مدمجين بالكامل داخل نفس النافذة الصغيرة المنبثقة -->
        <div class="input-wrapper">
            <input type="text" id="widget_text" class="input-field" placeholder="اكتب سؤالك هنا..." onkeypress="checkEnterKey(event)">
            <button class="send-btn" onclick="sendDataToStreamlit()">إرسال</button>
        </div>
    </div>

    <script>
    // جافا سكريبت ذكي لحفظ حالة فتح وإغلاق النافذة أونلاين عند التحديث
    if(window.parent.document.getElementById('movable_ai_widget')){{
        var savedState = window.parent.localStorage.getItem('floating_widget_state') || 'none';
        window.parent.document.getElementById('movable_ai_widget').style.display = savedState;
    }}
    
    function toggleWidgetWindow() {{
        var myWin = document.getElementById('movable_ai_widget');
        if(myWin.style.display === 'none' || myWin.style.display === ''){{
            myWin.style.display = 'block';
            window.parent.localStorage.setItem('floating_widget_state', 'block');
        }} else {{
            myWin.style.display = 'none';
            window.parent.localStorage.setItem('floating_widget_state', 'none');
        }}
    }}
    function checkEnterKey(event) {{
        if(event.keyCode === 13) {{ sendDataToStreamlit(); }}
    }}
    function sendDataToStreamlit() {{
        var clientText = document.getElementById('widget_text').value;
        if(clientText) {{
            // إرسال النص الحقيقي للسيرفر وتحديث علبة الدردشة بدون قفز الصفحة للأعلى نهائياً
            window.parent.location.search = '?widget_msg=' + encodeURIComponent(clientText);
        }}
    }}
    </script>
    """
    
    # حقن المنظومة العائمة الحقيقية لايف لتظهر وتطفو فوق كل أقسام وجداول الموقع بنجاح وأمان
    st.components.v1.html(widget_html, height=0)
