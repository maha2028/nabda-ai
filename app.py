import streamlit as st

# =========================================================
# إعداد الصفحة
# =========================================================

st.set_page_config(
    page_title="نبضة AI",
    page_icon="❤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# حالة الجلسة
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "started" not in st.session_state:
    st.session_state.started = False

if "answered" not in st.session_state:
    st.session_state.answered = False


# =========================================================
# تنسيق الصفحة
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        direction: rtl;
        background: linear-gradient(135deg, #fff8fa 0%, #f7f9ff 100%);
    }

    .block-container {
        max-width: 720px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label {
        direction: rtl;
        text-align: right;
    }

    div.stButton > button {
        width: 100%;
        min-height: 50px;
        border-radius: 14px;
        font-size: 17px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# رأس نبضة
# =========================================================

st.markdown(
    "<h1 style='text-align:center;color:#d94b68;'>❤️ نبضة AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:#64748b;font-size:18px;'>مساعدتك الذكية التكيفية في مادة العلوم</p>",
    unsafe_allow_html=True
)

st.write("")


# =========================================================
# شاشة تسجيل الدخول
# =========================================================

if not st.session_state.logged_in:

    with st.container(border=True):

        st.markdown("## 🌷 مرحبًا بكِ")

        st.write(
            "هذه البيئة التعليمية مخصصة للمشاركات "
            "المصرح لهن في الدراسة."
        )

    st.write("")

    access_code = st.text_input(
        "رمز الدخول الخاص بكِ",
        type="password",
        placeholder="أدخلي رمز الدخول"
    )

    if st.button(
        "دخول إلى نبضة ❤️",
        type="primary"
    ):

        if not access_code.strip():

            st.warning(
                "يرجى إدخال رمز الدخول 🌷"
            )

        else:

            # دخول تجريبي مؤقت
            st.session_state.logged_in = True
            st.rerun()

    st.caption(
        "🔒 لا تكتبي اسمكِ أو أي بيانات شخصية."
    )


# =========================================================
# الصفحة الرئيسية بعد الدخول
# =========================================================

elif not st.session_state.started:

    st.success(
        "🌷 أهلًا بكِ في جلسة اليوم"
    )

    st.write(
        "سنراجع بعض الأفكار العلمية، "
        "وستتغير الأسئلة والمساعدة المقدمة لكِ "
        "وفق إجاباتكِ."
    )

    st.write("")

    with st.container(border=True):

        st.markdown(
            "### 🫀 جهازا الدوران والمناعة"
        )

        st.write(
            "في هذه الجلسة ستجيبين عن مجموعة "
            "من الأسئلة المتنوعة."
        )

        st.write(
            "إذا احتجتِ إلى مساعدة، "
            "ستقدم لكِ نبضة تلميحات تدريجية "
            "تساعدكِ على الوصول إلى الإجابة."
        )

    st.write("")

    st.progress(0)

    st.caption(
        "التقدم في جلسة اليوم: 0%"
    )

    if st.button(
        "ابدئي جلسة اليوم ←",
        type="primary"
    ):

        st.session_state.started = True
        st.session_state.answered = False
        st.rerun()


# =========================================================
# السؤال الأول
# =========================================================

else:

    st.progress(10)

    st.caption(
        "التقدم في جلسة اليوم: 10%"
    )

    with st.container(border=True):

        st.markdown(
            "#### 🌷 السؤال 1"
        )

        st.markdown(
            "### أيُّ مكوّن من مكوّنات الدم "
            "يساعد بصورة أساسية على تجلط الدم "
            "عند حدوث جرح؟"
        )

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

    if st.button(
        "تحققي من إجابتي",
        type="primary"
    ):

        if answer is None:

            st.warning(
                "اختاري إجابة أولًا 🌷"
            )

        elif answer == "الصفائح الدموية":

            st.session_state.answered = True

            st.success(
                "🌟 إجابة صحيحة!"
            )

            st.info(
                "الصفائح الدموية تساعد على "
                "تجلط الدم وإيقاف النزيف."
            )

            st.write(
                "🟢 **مؤشر أولي:** "
                "أظهرتِ فهمًا جيدًا لهذه الفكرة."
            )

        else:

            st.session_state.answered = True

            st.warning(
                "ليست الإجابة الأدق."
            )

            st.info(
                "💡 **تلميح نبضة H1:** "
                "فكري في المكوّن الذي يساعد الجسم "
                "على إيقاف النزيف بعد حدوث الجرح."
            )

    if st.session_state.answered:

        st.divider()

        st.caption(
            "لاحقًا ستختار نبضة السؤال التالي "
            "وفق إجابتكِ ومحاولاتكِ ومستوى إتقانكِ."
        )
