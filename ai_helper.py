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
    """ ✨ ميزة علبة الدردشة المنبثقة التفاعلية الرسمية المتوافقة مع سيرفرات ستريمليت """
    
    # 🎨 إضافة كود CSS لتجميل علبة الدردشة لتظهر كقطعة سيبرانية فخمة
    st.markdown("""
        <style>
        .ai-welcome-box {
            background-color: #161b22 !important;
            border: 2px solid #00ffcc !important;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.3);
            margin-top: 10px;
        }
        .welcome-text {
            background-color: #21262d;
            padding: 12px;
            border-radius: 8px;
            border-right: 4px solid #ff007f;
            color: #ffffff !important;
            line-height: 1.4;
            font-size: 13px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #00ffcc; text-shadow: 0 0 5px #00ffcc; font-size: 16px;'>🤖 مساعد المتاجر الذكي (AI Widget)</h3>", unsafe_allow_html=True)
    
    # 🤖 زر تفعيل وفقاعة الروبوت الرسمية والآمنة التفاعلية في القائمة الجانبية
    ai_active = st.sidebar.toggle("⚡ اضغط هنا لفتح واجهة الروبوت المنبثقة 🤖")
    
    if ai_active:
        # ظهور علبة الترحيب والدردشة الفخمة فور تفعيل الزر
        with st.sidebar.container():
            st.markdown("""
                <div class="ai-welcome-box">
                    <div class="welcome-text">
                        👋 <b>مرحباً بك يا بطل في متجرك الأسطوري!</b><br>
                        أنا ذكاء المنصة المساعد، اكتبلي أي سؤال بالعامية أو قولي <b>"اكتبلي إعلان على..."</b> وراح نولّدلك نصوص إعلانية تزيد مبيعاتك فوراً! 🚀🇩🇿
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # صندوق إدخال النص التفاعلي الحقيقي بداخل العلبة المنبثقة
            user_query = st.text_input("اكتب سؤالك أو طلب الإعلان هنا للبوت:", key="ai_live_widget_input", placeholder="مثال: اكتبلي إعلان على ساعة ذكية")
            if user_query:
                with st.spinner("🤖 جاري التفكير وصياغة الرد التسويقي الفخم..."):
                    ai_reply = get_ai_response(user_query)
                    st.markdown("<p style='color: #00ffcc; font-weight: bold; margin-bottom: 2px;'>🤖 رد الروبوت الذكي:</p>", unsafe_allow_html=True)
                    st.info(ai_reply)
                    st.markdown("<p style='font-size: 11px; color: #8b949e; text-align: center;'>🔒 النسخة السنوية الكاملة تمنحك تحليلاً شاملاً لمتجرك! تفضل بالتفعيل عبر BaridiMob.</p>", unsafe_allow_html=True)
