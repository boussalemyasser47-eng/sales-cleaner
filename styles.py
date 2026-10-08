import streamlit as st

def apply_neon_theme():
    """ دالة لتطبيق ألوان السايبربانك الأسطورية وخلفية القائمة الجانبية والبطاقات المضيئة """
    st.markdown("""
        <style>
        /* 🌌 خلفية التطبيق العامة */
        .stApp { background-color: #0d1117; }
        
        /* 🛠️ تلوين لوحة التحكم الجانبية بالكامل باللون الداكن */
        [data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 2px solid #30363d !important;
        }
        
        /* تحسين النصوص داخل القائمة الجانبية لتكون بيضاء وواضحة جداً */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
            color: #ffffff !important;
            font-weight: bold !important;
            font-size: 16px !important;
        }
        
        /* تلوين العناوين الرئيسية بنظام النيون المشع الفسفوري */
        h1 {
            color: #00ffcc !important;
            font-family: 'Cairo', sans-serif;
            text-align: center;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
            font-weight: bold;
        }
        h2, h3 {
            color: #ff007f !important;
            text-shadow: 0 0 5px rgba(255, 0, 127, 0.5);
        }
        
        /* 🚀 تحسين الأزرار بتأثير نيون ليزري تفاعلي */
        div.stButton > button:first-child {
            background: linear-gradient(45deg, #ff007f, #7f00ff);
            color: white; border-radius: 12px; border: none;
            padding: 12px 30px; font-size: 18px; font-weight: bold;
            box-shadow: 0 0 15px #ff007f; transition: 0.4s; width: 100%;
        }
        div.stButton > button:first-child:hover {
            background: linear-gradient(45deg, #00ffcc, #007fff);
            box-shadow: 0 0 25px #00ffcc; color: #0d1117;
        }
        
        /* 📥 صناديق إدخال متطابقة مع الوضع الداكن */
        .stTextInput>div>div>input, .stSelectbox>div>div>div, .stFileUploader>div, .stNumberInput>div>div>input {
            background-color: #161b22 !important; color: #ffffff !important;
            border: 2px solid #30363d !important; border-radius: 8px;
        }
        p, label, th, td { color: #c9d1d9 !important; }
        
        /* 📊 صناديق الإحصائيات الفخمة المضيئة المحدثة */
        div[data-testid="stMetricValue"] {
            color: #00ffcc !important;
            font-family: 'Cairo', sans-serif;
            text-shadow: 0 0 5px #00ffcc;
            font-weight: bold;
        }
        div[data-testid="stMetricLabel"] {
            color: #ffffff !important;
        }
        </style>
        """, unsafe_allow_html=True)
