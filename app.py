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
# تصميم الواجهة
# =========================================================

st.markdown(
    """
    <style>

    /* اتجاه الصفحة */
    .stApp {
        direction: rtl;
        text-align: right;
        background: linear-gradient(
            135deg,
            #fff8fa 0%,
            #f7f9ff 100%
        );
    }

    /* عرض الصفحة */
    .block-container {
        max-width: 720px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* عنوان نبضة */
    .nabda-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #d94b68;
        margin-bottom: 5px;
    }

    /* العنوان الفرعي */
    .nabda-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 18px;
        margin-bottom: 28px;
    }

    /* البطاقة البيضاء */
    .nabda-card {
        background-color: #ffffff;
        padding: 26px;
        border-radius: 22px;
        border: 1px solid #f0d9df;
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
        margin-top: 15px;
        margin-bottom: 22px;
    }

    /* بطاقة الطالبة */
    .student-card {
        background-color: #fff0f4;
        padding: 18px 22px;
        border-radius: 18px;
        margin-top: 15px;
        margin-bottom: 20px;
        color: #374151;
        font-size: 17px;
    }

    /* رقم السؤال */
    .question-number {
        color: #d94b68;
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 10px;
    }

    /* نص السؤال */
    .question-text {
        color: #26364a;
        font-weight: 700;
        font-size: 21px;
        line-height: 1.8;
    }

    /* النص الصغير */
    .small-text {
        color: #64748b;
        font-size: 14px;
        text-align: center;
        margin-top: 18px;
    }

    /* الأزرار */
    div.stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 14px;
        font-size: 17px;
        font-weight: 700;
        border: 1px solid #ead5dc;
    }

    div.stButton > button:hover {
        border-color: #d94b68;
        color: #d94b68;
    }

    /* حقل الإدخال */
    div[data-baseweb="input"] {
        border-radius: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# رأس الصفحة
# =========================================================

st.markdown(
    '<div class="nabda-title">❤️ نبضة AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="nabda-subtitle">مساعدتك الذكية التكيفية في مادة العلوم</div>',
    unsafe_allow_html=True
)


# =========================================================
# الشاشة الأولى: تسجيل الدخول
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="nabda-card">
            <h2 style="
                text-align:center;
                color:#26364a;
                margin-bottom:12px;
            ">
                🌷 مرحبًا بكِ
            </h2>

            <p style="
                text-align:center;
                color:#64748b;
                font-size:17px;
                line-height:1.8;
                margin:0;
            ">
                هذه البيئة التعليمية مخصصة للمشاركات
                المصرح لهن في الدراسة.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    access_code = st.text_input(
        "رمز الدخول الخاص بكِ",
        type="password",
        placeholder="أدخلي رمز الدخول"
    )

    if st.button("دخول إلى نبضة ❤️"):

        if access_code.strip() == "":
            st.warning("يرجى إدخال رمز الدخول 🌷")

        else:
            # مؤقت للتجربة فقط
            # سنربطه لاحقًا برموز الدخول الآمنة
            st.session_state.logged_in = True
            st.rerun()

    st.markdown(
        """
        <div class="small-text">
            🔒 لا تكتبي اسمكِ أو أي بيانات شخصية.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# الشاشة الثانية: الصفحة الرئيسية للطالبة
# =========================================================

elif not st.session_state.started:

    st.markdown(
        """
        <div class="student-card">
            🌷 <strong>أهلًا بكِ في جلسة اليوم</strong>
            <br><br>
            سنراجع بعض الأفكار العلمية،
            وستتغير الأسئلة والمساعدة المقدمة لكِ
            حسب إجاباتكِ.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="nabda-card">

            <h3 style="
                color:#26364a;
                margin-top:0;
            ">
                🫀 جهازا الدوران والمناعة
            </h3>

            <p style="
                color:#64748b;
                font-size:16px;
                line-height:1.9;
            ">
                في هذه الجلسة ستجيبين عن مجموعة
                من الأسئلة المتنوعة.
                وإذا احتجتِ إلى مساعدة،
                ستقدم لكِ نبضة تلميحات تدريجية
                تساعدكِ على الوصول إلى الإجابة.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(0)

    st.caption("التقدم في جلسة اليوم: 0%")

    if st.button("ابدئي جلسة اليوم ←"):
        st.session_state.started = True
        st.session_state.answered = False
        st.rerun()


# =========================================================
# الشاشة الثالثة: السؤال الأول
# =========================================================

else:

    st.progress(10)

    st.caption("التقدم في جلسة اليوم: 10%")

    st.markdown(
        """
        <div class="nabda-card">

            <div class="question-number">
                السؤال 1
            </div>

            <div class="question-text">
                أيُّ مكوّن من مكوّنات الدم
                يساعد بصورة أساسية على تجلط الدم
                عند حدوث جرح؟
            </div>

        </div>
        """,
        unsafe_allow_html=True
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

    if st.button("تحققي من إجابتي"):

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

            st.markdown(
                "🟢 **مؤشر أولي:** "
                "أظهرتِ فهمًا جيدًا لهذه الفكرة."
            )

        else:

            st.session_state.answered = True

            st.warning(
                "ليست الإجابة الأدق. "
                "حاولي التفكير مرة أخرى."
            )

            st.info(
                "💡 تلميح نبضة H1: "
                "فكري في المكوّن الذي يساعد الجسم "
                "على إيقاف النزيف بعد حدوث الجرح."
            )


    # =====================================================
    # بعد الإجابة
    # =====================================================

    if st.session_state.answered:

        st.markdown("---")

        st.caption(
            "هذه نسخة تجريبية أولية. "
            "لاحقًا ستختار نبضة السؤال التالي "
            "وفق إجابتكِ ومحاولاتكِ ومستوى إتقانكِ."
        )


# =========================================================
# نهاية التطبيق
# =========================================================
