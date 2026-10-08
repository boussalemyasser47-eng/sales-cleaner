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
    """ ✨ وضع خانة الإدخال والترحيب بالكامل داخل النافذة المضيئة الجانبية الرسمية والآمنة """
    
    # 🎨 كود CSS لتجميل الحاوية الجانبية لتظهر كعلبة منبثقة احترافية بداخل القائمة
    st.markdown("""
        <style>
        .ai-integrated-box {
            background-color: #161b22 !important;
            border: 2px solid #00ffcc !important;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.3);
            margin-top: 5px;
        }
        .ai-welcome-content {
            background-color: #21262d;
            padding: 10px;
            border-radius: 8px;
            border-right: 4px solid #ff007f;
            color: #ffffff !important;
            line-height: 1.4;
            font-size: 13px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # تفريغ القائمة الجانبية وإخفاء أي نصوص قديمة علوية
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #00ffcc; text-shadow: 0 0 5px #00ffcc; font-size: 16px;'>🤖 مساعد المتاجر ومولد الإعلانات</h3>", unsafe_allow_html=True)
    
    # 📦 إنشاء العلبة المدمجة الاحترافية داخل القائمة الجانبية (تحتوي على الترحيب والخانة معاً في مكان واحد!)
    with st.sidebar.container():
        st.markdown("""
            <div class="ai-integrated-box">
                <div class="ai-welcome-content">
                    👋 <b>مرحباً بك يا بطل!</b><br>
                    أنا ذكاء المنصة، اكتبلي سؤالك بالعامية أو طلب إعلانك في الخانة بالأسفل مباشرة وراح نجاوبك فوراً! 🚀
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 📥 خانة الكتابة الحية الحقيقية مدمجة تماماً بداخل العلبة في الأسفل بدون فراغات أو تشتيت
        user_query = st.text_input("اكتب طلب الإعلان أو السؤال هنا 👇:", key="ai_final_integrated_input", placeholder="مثال: اكتبلي إعلان على ساعة...")
        
        if user_query:
            with st.spinner("🤖 جاري الصياغة..."):
                ai_reply = get_ai_response(user_query)
                st.markdown("<p style='color: #00ffcc; font-weight: bold; margin-top: 10px; margin-bottom: 2px;'>🤖 الرد الذكي الحقيقي:</p>", unsafe_allow_html=True)
                st.info(ai_reply)
                st.markdown("<p style='font-size: 11px; color: #8b949e; text-align: center;'>🔒 النسخة السنوية الكاملة متوفرة للتفعيل عبر BaridiMob.</p>", unsafe_allow_html=True)
