import streamlit as st

# إعداد الصفحة
st.set_page_config(
    page_title="نبضة AI",
    page_icon="❤️",
    layout="centered"
)

# تنسيق الواجهة
st.markdown("""
<style>

.stApp {
    direction: rtl;
    text-align: right;
    background: linear-gradient(135deg, #fff7f9 0%, #f4f8ff 100%);
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: #d94b68;
    margin-top: 30px;
}

.subtitle {
    text-align: center;
    font-size: 22px;
    color: #475569;
    margin-bottom: 35px;
}

.welcome-box {
    background-color: white;
    padding: 30px;
    border-radius: 24px;
    border: 1px solid #f1d5dc;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}

.security {
    text-align: center;
    color: #64748b;
    font-size: 15px;
    margin-top: 25px;
}

div.stButton > button {
    width: 100%;
    border-radius: 14px;
    height: 52px;
    font-size: 19px;
    font-weight: bold;
    background-color: #d94b68;
    color: white;
    border: none;
}

div.stButton > button:hover {
    background-color: #bd3d59;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# عنوان التطبيق
st.markdown(
    '<div class="main-title">❤️ نبضة AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">مساعدتك الذكية التكيفية في مادة العلوم</div>',
    unsafe_allow_html=True
)


# صندوق الترحيب
st.markdown("""
<div class="welcome-box">

<h2 style="text-align:center; color:#26364a;">
مرحبًا بكِ 🌷
</h2>

<p style="text-align:center; font-size:18px; color:#526173;">
هذه البيئة التعليمية مخصصة للمشاركات المصرح لهن في الدراسة.
</p>

</div>
""", unsafe_allow_html=True)


# رمز الدخول
access_code = st.text_input(
    "رمز الدخول الخاص بكِ",
    type="password",
    placeholder="أدخلي رمز الدخول"
)


# زر الدخول
if st.button("دخول إلى نبضة ❤️"):

    if access_code == "":
        st.warning("يرجى إدخال رمز الدخول.")

    else:
        st.success("تم استقبال رمز الدخول بنجاح 🌷")
        st.info("في النسخة القادمة سيتم التحقق من الرمز وفتح جلسة التعلم الخاصة بكِ.")


# تنبيه الخصوصية
st.markdown(
    '<div class="security">🔒 لا تكتبي اسمكِ أو أي بيانات شخصية.</div>',
    unsafe_allow_html=True
)
