import streamlit as st

def render_ai_chatbot():
    """ ✨ تحقيق حلم الفقاعة المنبثقة: فقاعة عائمة تفتح نافذة نيون صغيرة ترحيبية وبداخلها زر التكلم المباشر """
    
    # تنظيف القائمة الجانبية لإبقاء الموقع منسقاً واحترافياً
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #00ffcc; font-size: 14px; text-align: center;'>🤖 تم تفعيل البوت العائم في الزاوية السفلية</h3>", unsafe_allow_html=True)

    # 🎨 كود الـ HTML & CSS & JS الأسطوري لحقن الفقاعة والنافذة المنبثقة التفاعلية في زاوية المتصفح
    widget_html = """
    <style>
    /* 🤖 أيقونة الروبوت العائمة المضيئة الثابتة أسفل يمين الشاشة */
    .floating-launcher-bubble {
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
    }
    .floating-launcher-bubble:hover { transform: scale(1.1); }
    
    /* 📋 العلبة الصغيرة المنبثقة المتكاملة المدمجة فوق الفقاعة بدقة */
    .floating-chat-window {
        position: fixed !important;
        bottom: 95px !important;
        right: 25px !important;
        width: 320px;
        background-color: #161b22;
        border: 2px solid #00ffcc;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.4);
        border-radius: 14px;
        z-index: 999999999 !important;
        display: none; /* مخفية تلقائياً حتى يتم الضغط */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: rtl;
    }
    .chat-header {
        background: linear-gradient(45deg, #1f2937, #0d1117);
        padding: 12px;
        color: #00ffcc;
        font-weight: bold;
        font-size: 13px;
        border-bottom: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
    }
    .chat-body {
        padding: 15px;
        color: white;
        font-size: 12px;
    }
    .welcome-card {
        background-color: #21262d;
        padding: 12px;
        border-radius: 8px;
        border-right: 4px solid #ff007f;
        line-height: 1.5;
        margin-bottom: 12px;
        color: #ffffff;
    }
    /* 🚀 زر التواصل السريع الليزري المطور للتكلم المباشر مع المطور */
    .chat-action-btn {
        display: block;
        background: linear-gradient(45deg, #ff007f, #7f00ff);
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        font-weight: bold;
        text-decoration: none;
        box-shadow: 0 0 10px #ff007f;
        transition: 0.3s;
        font-size: 13px;
    }
    .chat-action-btn:hover {
        background: linear-gradient(45deg, #00ffcc, #007fff);
        box-shadow: 0 0 15px #00ffcc;
        color: #0d1117 !important;
    }
    </style>

    <!-- أيقونة الروبوت العائمة -->
    <div class="floating-launcher-bubble" onclick="toggleWidgetWindow()">🤖</div>

    <!-- نافذة الدردشة المستقلة بالكامل في الزاوية -->
    <div class="floating-chat-window" id="movable_ai_widget">
        <div class="chat-header">
            <span>🤖 مساعد ومولد الإعلانات (AI Live)</span>
            <span style="cursor:pointer;color:#ff007f;font-size:16px;" onclick="toggleWidgetWindow()">×</span>
        </div>
        <div class="chat-body">
            <div class="welcome-card">
                👋 <b>مرحباً بك يا بطل في لوحة تحكم متجرك!</b><br><br>
                أنا ذكاء المنصة المساعد، يمكنك استخدام باقة الذكاء الاصطناعي الكاملة لتوليد نصوص إعلانية بالعامية الجزائرية وصياغة حملات Facebook Ads لمتجرك حياً!
            </div>
            <!-- زر التكلم المباشر المدمج تحت رسالة الترحيب -->
            <a href="https://wa.me" target="_parent" class="chat-action-btn">💬 اضغط هنا للتكلم معي وتفعيل البوت الكامل 🚀</a>
        </div>
    </div>

    <script>
    function toggleWidgetWindow() {
        var myWin = document.getElementById('movable_ai_widget');
        if(myWin.style.display === 'none' || myWin.style.display === '') {
            myWin.style.display = 'block';
        } else {
            myWin.style.display = 'none';
        }
    }
    </script>
    """
    # حقن المنظومة العائمة لتظهر وتطير وتفتح بسلام أونلاين
    st.components.v1.html(widget_html, height=120)


