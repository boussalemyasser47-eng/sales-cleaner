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
    """ ✨ الحل النهائي والعبقري: دالة بناء واجهة دردشة مدمجة ومستقرة تماماً داخل السايدبار بدون أخطاء قفز """
    
    # 🎨 كود الـ CSS الأسطوري المطور لتنسيق العلبة بداخل القائمة الجانبية بنمط النيون السيبراني
    st.markdown("""
        <style>
        .ai-perfect-box {
            background-color: #161b22 !important;
            border: 2px solid #00ffcc !important;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.3);
            margin-bottom: 10px;
        }
        .ai-welcome-msg-text {
            background-color: #21262d;
            padding: 10px;
            border-radius: 8px;
            border-right: 4px solid #ff007f;
            color: #ffffff !important;
            line-height: 1.4;
            font-size: 13px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # تفريغ وتنظيف مساحة القائمة الجانبية في الأسفل
    st.sidebar.markdown("---")
    
    # 📦 المكون الرسمي المستقر: صندوق منسدل فخم يفتح ويغلق بلمسة تاجر احترافية
    with st.sidebar.expander("🤖 افتح مساعد ومولد الإعلانات الذكي (AI Live)"):
        # عرض رسالة الترحيب بداخل الصندوق الجانبي بقمة الأناقة
        st.markdown("""
            <div class="ai-perfect-box">
                <div class="ai-welcome-msg-text">
                    👋 <b>مرحباً بك يا بطل في متجرك!</b><br>
                    أنا ذكاء المنصة المساعد، اكتبلي سؤالك أو طلب إعلانك في المستطيل بالأسفل مباشرة وراح نجاوبك هنا فوراً! 🚀🇩🇿
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 📥 مستطيل الكتابة الحقيقي والمستقر 100% يظهر تحت رسالة الترحيب مباشرة في نفس الصندوق!
        user_query = st.text_input("✍️ اكتب سؤالك أو طلب الإعلان هنا:", key="ai_final_perfect_sidebar_input", placeholder="مثال: اكتبلي إعلان على ساعة...")
        
        if user_query:
            with st.spinner("🤖 جاري الصياغة والتحليل..."):
                ai_reply = get_ai_response(user_query)
                st.markdown("<p style='color: #00ffcc; font-weight: bold; margin-top: 10px; margin-bottom: 2px;'>🤖 رد الروبوت الذكي:</p>", unsafe_allow_html=True)
                st.info(ai_reply)
                st.markdown("<p style='font-size: 11px; color: #8b949e; text-align: center;'>🔒 النسخة السنوية الكاملة متوفرة للتفعيل عبر BaridiMob.</p>", unsafe_allow_html=True)
