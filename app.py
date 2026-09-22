import streamlit as st

st.set_page_config(
    page_title="نبضة AI",
    page_icon="❤️",
    layout="centered"
)

# -----------------------------
# حالة الجلسة
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "started" not in st.session_state:
    st.session_state.started = False

if "answered" not in st.session_state:
    st.session_state.answered = False


# -----------------------------
# التصميم
# -----------------------------
st.markdown("""
<style>

.stApp {
    direction: rtl;
    text-align: right;
    background: linear-gradient(135deg, #fff7f9 0%, #f5f8ff 100%);
}

.block-container {
    max-width: 760px;
    padding-top: 2.5rem;
}

.nabda-title {
    text-align:center;
    font-size:46px;
    font-weight:800;
    color:#d94b68;
}

.nabda-subtitle {
    text-align:center;
    color:#64748b;
    font-size:19px;
    margin-bottom:30px;
}

.card {
    background:white;
    padding:28px;
    border-radius:24px;
    border:1px solid #f0d9df;
    box-shadow:0 8px 24px rgba(0,0,0,.05);
    margin:18px 0;
}

.student-card {
    background:#fff0f4;
    padding:18px 22px;
    border-radius:18px;
    margin-bottom:20px;
}

.question-number {
    color:#d94b68;
    font-weight:700;
    font-size:16px;
}

.question-text {
    color:#26364a;
    font-weight:700;
    font-size:22px;
    line-height:1.8;
}

.small-text {
    color:#64748b;
    font-size:14px;
}

div.stButton > button {
    width:100%;
    min-height:50px;
    border-radius:14px;
    font-size:17px;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# رأس الصفحة
# -----------------------------
st.markdown(
    '<div class="nabda-title">❤️ نبضة AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="nabda-subtitle">مساعدتك الذكية التكيفية في مادة العلوم</div>',
    unsafe_allow_html=True
)


# ==================================================
# الشاشة الأولى: الدخول
# ==================================================
if not st.session_state.logged_in:

    st.markdown("""
    <div class="card">
        <h2 style="text-align:center;color:#26364a;">
            مرحبًا بكِ 🌷
        </h2>

        <p style="text-align:center;color:#64748b;font-size:17px;">
            هذه البيئة التعليمية مخصصة للمشاركات المصرح لهن في الدراسة.
        </p>
    </div>
    """, unsafe_allow_html=True)

    access_code = st.text_input(
        "رمز الدخول الخاص بكِ",
        type="password",
        placeholder="أدخلي رمز الدخول"
    )

    if st.button("دخول إلى نبضة ❤️"):

        # دخول تجريبي مؤقت فقط
        if access_code.strip() == "":
            st.warning("يرجى إدخال رمز الدخول.")

        else:
            st.session_state.logged_in = True
            st.rerun()

    st.markdown(
        '<p class="small-text" style="text-align:center;">🔒 لا تكتبي اسمكِ أو أي بيانات شخصية.</p>',
        unsafe_allow_html=True
    )


# ==================================================
# الشاشة الثانية: الصفحة الرئيسية
# ==================================================
elif not st.session_state.started:

    st.markdown("""
    <div class="student-card">
        <b>🌷 أهلًا بكِ في جلسة اليوم</b><br>
        سنراجع بعض الأفكار، وستتغير الأسئلة حسب إجاباتكِ.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3 style="color:#26364a;">
            🫀 جهازا الدوران والمناعة
        </h3>

        <p style="color:#64748b;">
            في هذه الجلسة ستجيبِين عن مجموعة قصيرة من الأسئلة.
            إذا احتجتِ إلى مساعدة، ستقدم لكِ نبضة تلميحات تدريجية.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.progress(0)

    st.caption("التقدم في جلسة اليوم: 0%")

    if st.button("ابدئي جلسة اليوم ←"):
        st.session_state.started = True
        st.rerun()


# ==================================================
# الشاشة الثالثة: أول سؤال
# ==================================================
else:

    st.progress(0.10)
    st.caption("التقدم في جلسة اليوم: 10%")

    st.markdown("""
    <div class="card">

        <div class="question-number">
            السؤال 1
        </div>

        <div class="question-text">
            أيُّ مكوّن من مكوّنات الدم يساعد بصورة أساسية على تجلط الدم عند حدوث جرح؟
        </div>

    </div>
    """, unsafe_allow_html=True)

    answer = st.radio(
        "اختاري إجابة واحدة:",
        [
            "خلايا الدم الحمراء",
            "خلايا الدم البيضاء",
            "الصفائح الدموية",
            "البلازما"
        ],
        index=None
    )

    if st.button("تحققي من إجابتي"):

        if answer is None:

            st.warning("اختاري إجابة أولًا 🌷")

        elif answer == "الصفائح الدموية":

            st.session_state.answered = True

            st.success(
                "🌟 إجابة صحيحة! الصفائح الدموية تساعد على تجلط الدم وإيقاف النزيف."
            )

            st.markdown(
                "🟢 **مؤشر أولي:** أظهرتِ فهمًا جيدًا لهذه الفكرة."
            )

        else:

            st.session_state.answered = True

            st.warning("ليست الإجابة الأدق. حاولي التفكير مرة أخرى.")

            st.info(
                "💡 تلميح نبضة H1: فكري في المكوّن الذي يساعد الجسم على إيقاف النزيف بعد حدوث الجرح."
            )

    if st.session_state.answered:

        st.markdown("---")

        st.caption(
            "هذه النسخة تجريبية. في النسخة التكيفية ستحدد نبضة السؤال التالي وفق إجابتكِ ومحاولاتكِ."
        )
