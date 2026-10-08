def render_ai_chatbot():
    """ ✨ تثبيت الفقاعة والنافذة المنبثقة الترحيبية في زاوية الشاشة السفلية وثقب حظر سيرفر ستريمليت """
    
    # تنظيف مساحة السايدبار السفلية
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

    # 🎨 كود الـ HTML & CSS & JS الأسطوري المعدل لحقن وتثبيت الفقاعة في الأسفل المطلق للمتصفح (Fixed CSS Injection)
    widget_html = f"""
    <style>
    /* 🤖 أيقونة الروبوت العائمة المضيئة مجبرة ومثبتة في زاوية الشاشة السفلية اليمنى */
    .floating-launcher-bubble {{
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
        z-index: 999999999 !important; /* رفع الترتيب البصري فوق كل عناصر الواجهة */
        transition: 0.3s ease-in-out;
    }}
    .floating-launcher-bubble:hover {{ transform: scale(1.1); }}
    
    /* 📋 النافذة الصغيرة المنبثقة الترحيبية مثبتة بدقة فوق الفقاعة السفلية */
    .floating-chat-window {{
        position: fixed !important;
        bottom: 95px !important;
        right: 25px !important;
        width: 320px;
        background-color: #161b22;
        border: 2px solid #00ffcc;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5);
        border-radius: 14px;
        z-index: 999999999 !important;
        display: none;
        font-family: sans-serif;
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
    /* ✍️ مستطيل الكتابة وزر الإرسال مدمجين في أسفل العلبة الصغيرة */
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

    <div class="floating-launcher-bubble" onclick="toggleWidgetWindow()">🤖</div>

    <div class="floating-chat-window" id="movable_ai_widget">
        <div class="chat-header">
            <span>🤖 مساعد المتاجر الذكي</span>
            <span style="cursor:pointer;color:#ff007f;" onclick="toggleWidgetWindow()">×</span>
        </div>
        <div class="win-body">
            <div class="welcome-card">
                👋 <b>مرحباً بك يا بطل في متجرك!</b> اكتب سؤالك أو طلب إعلانك في المستطيل بالأسفل مباشرة وراح نجاوبك هنا فوراً! 🚀
            </div>
            {"<div class='response-area'>🤖 الرد: <br>" + st.session_state["ai_widget_history"] + "</div>" if st.session_state["ai_widget_history"] else ""}
        </div>
        <div class="input-wrapper">
            <input type="text" id="widget_text" class="input-field" placeholder="اكتب سؤالك هنا..." onkeypress="checkEnterKey(event)">
            <button class="send-btn" onclick="sendDataToStreamlit()">إرسال</button>
        </div>
    </div>

    <script>
    // الحفاظ على حالة الفتح والإغلاق في جذور الصفحة لمنع القفز للأعلى
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
            window.parent.location.search = '?widget_msg=' + encodeURIComponent(clientText);
        }}
    }}
    </script>
    """
    
    # حيلة الـ iFrame المطلق لفرض حقن ونزول الفقاعة أسفل يمين الشاشة الكلية للموقع
    st.components.v1.html(widget_html, height=0)
