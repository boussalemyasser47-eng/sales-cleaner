import streamlit as st

def apply_neon_theme():
    """ دالة لحقن ألوان السايبربانك والفقاعة العائمة القابلة للتحريك باليد في أي اتجاه """
    st.markdown("""
        <style>
        /* 🌌 خلفية التطبيق العامة الداكنة */
        .stApp { background-color: #0d1117; }
        
        /* 🛠️ لوحة التحكم الجانبية */
        [data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 2px solid #30363d !important;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
            color: #ffffff !important; font-weight: bold !important; font-size: 16px !important;
        }
        
        /* 🟢 العناوين والأزرار النيون */
        h1 { color: #00ffcc !important; text-align: center; text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc; font-weight: bold; }
        h2, h3 { color: #ff007f !important; text-shadow: 0 0 5px rgba(255, 0, 127, 0.5); }
        div.stButton > button:first-child {
            background: linear-gradient(45deg, #ff007f, #7f00ff); color: white; border-radius: 12px; border: none;
            padding: 12px 30px; font-size: 18px; font-weight: bold; box-shadow: 0 0 15px #ff007f; transition: 0.4s; width: 100%;
        }
        div.stButton > button:first-child:hover { background: linear-gradient(45deg, #00ffcc, #007fff); box-shadow: 0 0 25px #00ffcc; color: #0d1117; }
        .stTextInput>div>div>input, .stSelectbox>div>div>div, .stFileUploader>div, .stNumberInput>div>div>input {
            background-color: #161b22 !important; color: #ffffff !important; border: 2px solid #30363d !important; border-radius: 8px;
        }
        p, label, th, td { color: #c9d1d9 !important; }
        div[data-testid="stMetricValue"] { color: #00ffcc !important; text-shadow: 0 0 5px #00ffcc; font-weight: bold; }

        /* 🤖 1. تصميم الفقاعة العائمة المتحركة في أسفل يمين المتصفح */
        #draggable-ai-bubble {
            position: fixed !important;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(45deg, #00ffcc, #ff007f);
            color: white;
            width: 65px;
            height: 65px;
            border-radius: 50%;
            text-align: center;
            line-height: 65px;
            font-size: 32px;
            cursor: move; /* تغيير الماوس لشكل التحريك باليد */
            box-shadow: 0 0 20px #00ffcc, 0 0 30px #ff007f;
            z-index: 999999999 !important;
            user-select: none;
        }

        /* 📋 2. تصميم نافذة الترحيب الصغيرة المنبثقة التفاعلية */
        #ai-movable-window {
            position: fixed !important;
            bottom: 110px;
            right: 30px;
            width: 320px;
            background-color: #161b22;
            border: 2px solid #00ffcc;
            box-shadow: 0 0 25px rgba(0, 255, 204, 0.5);
            border-radius: 14px;
            z-index: 999999998 !important;
            display: none; /* مخفية حتى يضغط العميل */
            font-family: sans-serif;
            direction: rtl;
        }
        .win-header { background: linear-gradient(45deg, #1f2937, #0d1117); padding: 12px; color: #00ffcc; font-weight: bold; font-size: 13px; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; }
        .win-body { padding: 15px; color: white; font-size: 12px; }
        .welcome-card { background-color: #21262d; padding: 10px; border-radius: 8px; border-right: 4px solid #ff007f; line-height: 1.4; }
        </style>

        <!-- 🪐 هيكل الفقاعة والنافذة المنبثقة الذكية -->
        <div id="draggable-ai-bubble" onmousedown="startDrag(event)" onclick="toggleMovableWindow()">🤖</div>

        <div id="ai-movable-window">
            <div class="win-header">
                <span>🤖 مساعد ومولد الإعلانات الذكي</span>
                <span style="cursor:pointer;color:#ff007f;font-size:16px;" onclick="toggleMovableWindow()">×</span>
            </div>
            <div class="win-body">
                <div class="welcome-card">
                    👋 <b>مرحباً بك يا بطل في متجرك الأسطوري!</b><br>
                    أنا ذكاء المنصة المساعد، اكتبلي سؤالك بالعامية أو طلب إعلانك في الخانة المخصصة بالأسفل وراح نجاوبك فوراً! 🚀🇩🇿
                </div>
            </div>
        </div>

        <!-- 🛠️ جافا سكريبت الأسطوري المسؤول عن تحريك الفقاعة باليد في أي اتجاه وفتح النافذة -->
        <script>
        var bubble = window.parent.document.getElementById('draggable-ai-bubble');
        var win = window.parent.document.getElementById('ai_popup_window');
        var isDragging = false;
        var offsetX, offsetY;

        // دالة فتح وإغلاق النافذة المنبثقة عند الضغط
        window.toggleMovableWindow = function() {
            if (isDragging) return; // منع الفتح أثناء السحب باليد
            var w = window.parent.document.getElementById('ai-movable-window');
            if (w.style.display === 'none' || w.style.display === '') {
                w.style.display = 'block';
                // جعل النافذة تفتح دائماً متناسقة فوق مكان الفقاعة الجديد
                var bRect = bubble.getBoundingClientRect();
                w.style.left = bRect.left - 130 + 'px';
                w.style.top = bRect.top - 160 + 'px';
            } else {
                w.style.display = 'none';
            }
        }

        // دالة بدء السحب والتحريك باليد
        window.startDrag = function(e) {
            isDragging = false;
            offsetX = e.clientX - bubble.getBoundingClientRect().left;
            offsetY = e.clientY - bubble.getBoundingClientRect().top;
            
            window.parent.document.addEventListener('mousemove', dragBubble);
            window.parent.document.addEventListener('mouseup', stopDrag);
        }

        function dragBubble(e) {
            isDragging = true;
            bubble.style.left = (e.clientX - offsetX) + 'px';
            bubble.style.top = (e.clientY - offsetY) + 'px';
            bubble.style.bottom = 'auto';
            bubble.style.right = 'auto';
            
            // إخفاء نافذة الترحيب مؤقتاً أثناء التحريك لراحة العين
            var w = window.parent.document.getElementById('ai-movable-window');
            if(w) w.style.display = 'none';
        }

        function stopDrag() {
            window.parent.document.removeEventListener('mousemove', dragBubble);
            window.parent.document.removeEventListener('mouseup', stopDrag);
            // مهلة صغيرة للتفريق بين السحب والضغط
            setTimeout(function() { isDragging = false; }, 100);
        }
        </script>
    """, unsafe_allow_html=True)
