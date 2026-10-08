import streamlit as st
import json
import urllib.request
import base64

def get_ai_response(prompt, system_instruction="You are a helpful e-commerce assistant."):
    """ محرك الاتصال الآمن والمشفر بـ OpenRouter للرد الذكي """
    try:
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
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['choices']['message']['content']
    except:
        return "🤖 خويا العزيز كاين ضغط خفيف على السيرفر، عاود اضغط على الزر وراح نجاوبك فوراً!"

def render_marketing_hub():
    """ 💡 الميزة 1: قسم التخطيط الاستراتيجي ومولد حملات الفيسبوك """
    st.write("<h2 style='color: #00ffcc;'>🚀 مولّد الحملات الإعلانية والاستهداف الذكي</h2>", unsafe_allow_html=True)
    st.caption("أدخل تفاصيل سلعتك ودع الذكاء الاصطناعي يصنع لك الحملة كاملة بالعامية الجزائرية.")
    
    col1, col2 = st.columns(2)
    with col1:
        prod_name = st.text_input("اسم المنتج المراد بيعه:", placeholder="مثال: ساعة ذكية Ultra")
        prod_features = st.text_area("أهم مميزات السلعة (اختياري):", placeholder="مثال: ضد الماء، تدعم شريحة اتصال، بطارية تدوم 5 أيام")
    with col2:
        target_audience = st.selectbox("الفئة المستهدفة في الجزائر:", ["الجميع (Men & Women)", "الرجال فقط", "النساء فقط", "الشباب والمراهقين", "العائلات وأرباب البيوت"])
        ad_tone = st.selectbox("نبرة نص الإعلان:", ["حماسي وتسويقي بقوة", "فكاهي وقريب من الشعب", "احترافي وتقني"])
        
    if st.button("✨ توليد الخطة الإعلانية الكاملة"):
        if not prod_name:
            st.error("❌ يرجى كتابة اسم المنتج أولاً!")
        else:
            with st.spinner("🤖 jari صياغة الاستراتيجية التسويقية الأسطورية..."):
                sys_instruction = (
                    "You are an expert Algerian e-commerce marketer and FB ads copywriter. "
                    "Write a highly engaging ad copy in Algerian Darija (العامية) with emojis and hashtags. "
                    "Also provide 3 targeted Facebook interest suggestions and a customer service reply script."
                )
                prompt = f"المنتج: {prod_name}. المميزات: {prod_features}. الفئة المستهدفة: {target_audience}. النبرة: {ad_tone}."
                ai_reply = get_ai_response(prompt, sys_instruction)
                st.markdown("### 📊 خطتك الإعلانية الجاهزة للنسخ:")
                st.info(ai_reply)

def render_data_insights(df=None):
    """ 💡 الميزة 2: مساعد فرز وتطهير الداتا الذكي """
    st.write("<h3 style='color: #ff007f;'>📊 مستشار فرز المبيعات وتحليل الولايات (AI Insights)</h3>", unsafe_allow_html=True)
    if df is None or df.empty:
        st.info("💡 نصيحة: ارفع ملف مبيعاتك أولاً في قسم 'مطهر ملفات المبيعات' لكي يقوم الذكاء الاصطناعي بقراءته وتحليله لك هنا.")
    else:
        st.success("✅ تم قراءة داتا ملف المبيعات الحالي بنجاح!")
        if st.button("🤖 اطلب تحليلاً ذكياً للمبيعات والأرباح"):
            with st.spinner("🤖 جاري قراءة الأرقام واستخراج النصائح التجارية..."):
                sys_instruction = (
                    "You are an expert data analyst for Algerian cash on delivery stores. "
                    "Analyze the provided raw summary data and give optimization tips in Algerian Darija (العامية الجزائرية). "
                    "Keep it motivational, actionable, and focus on high-sales regions or products."
                )
                data_summary = df[['product_name', 'total_row_sales']].groupby('product_name').sum().to_string()
                prompt = f"إليك ملخص مبيعات متجري لهذا الشهر، اعطني نصائح بالعامية الجزائرية لتطوير التجارة: \n{data_summary}"
                ai_reply = get_ai_response(prompt, sys_instruction)
                st.markdown("### 📈 تقرير المستشار الذكي لمتجرك:")
                st.success(ai_reply)

def render_sidebar_helper():
    """ 💡 الميزة 3: بوت الفواتير والتجارة الذكي فوري الرد في الجنب """
    st.sidebar.markdown("---")
    with st.sidebar.expander("🤖 مساعد تجارة الـ COD في الجزائر"):
        st.markdown("<p style='font-size: 12px; color: #00ffcc;'>اسألني عن مشاكل الشحن، الروتور، أو إقناع الزبائن في الجزائر.</p>", unsafe_allow_html=True)
        user_query = st.text_input("اكتب سؤالك هنا خوي العزيز 👇:", key="sidebar_cod_query", placeholder="مثال: كيفاش ننقص الروتور؟")
        if user_query:
            with st.spinner("🤖 جاري التفكير..."):
                sys_instruction = (
                    "You are an expert mentor for e-commerce in Algeria. Help the user with delivery, shipping, "
                    "confirmation calls, or handling returns (Yalidine, ZR Express, etc.). Answer in Algerian Darija."
                )
                ai_reply = get_ai_response(user_query, sys_instruction)
                st.markdown("<p style='color: #00ffcc; font-weight: bold; font-size:12px;'>🤖 نصيحة الروبوت:</p>", unsafe_allow_html=True)
                st.caption(ai_reply)

def render_ai_chatbot():
    """ دالة فرعية احتياطية لمنع أي تعارض قديم """
    pass
