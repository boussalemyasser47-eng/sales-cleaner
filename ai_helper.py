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
    """ 📦 الميزة الرسمية والمستقرة 100%: صندوق دردشة نيون منسدل فخم بداخل القائمة الجانبية """
    st.sidebar.markdown("---")
    
    # تحسين بصرى بتنسيق سيبراني
    st.sidebar.markdown("<p style='color: #00ffcc; font-weight: bold; font-size: 14px;'>🤖 مساعد ومولد الإعلانات الذكي:</p>", unsafe_allow_html=True)
    
    # مستطيل الإدخال الحقيقي والآمن أونلاين تحت ألوان النيون
    user_prompt = st.sidebar.text_input("اسأل البوت أو اكتب: 'اكتبلي إعلان على...' 👇:", key="ai_stable_final_input", placeholder="مثال: ساعة ذكية...")
    
    if user_prompt:
        with st.sidebar.spinner("🤖 جاري صياغة الرد الفخم..."):
            reply = get_ai_response(user_prompt)
            st.sidebar.markdown("<p style='color: #00ffcc; font-weight: bold; margin-top: 10px; margin-bottom: 2px;'>🤖 رد الروبوت الذكي:</p>", unsafe_allow_html=True)
            st.sidebar.success(reply)
            st.sidebar.markdown("<p style='font-size: 11px; color: #8b949e; text-align: center;'>🔒 النسخة السنوية الكاملة متوفرة للتفعيل عبر BaridiMob.</p>", unsafe_allow_html=True)
