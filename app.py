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
# إعداد حالة الجلسة
# =========================================================

defaults = {
    "logged_in": False,
    "started": False,
    "question_index": 0,
    "attempt": 0,
    "score": 0,
    "feedback": "",
    "hint_level": 0,
    "completed": False,
    "mastery": {
        "مكونات الدم": 0,
        "خلايا الدم الحمراء": 0,
        "الدورة الدموية": 0
    }
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# بنك الأسئلة التجريبي
# =========================================================

questions = [

    {
        "id": "C02-Q01",
        "concept": "مكونات الدم",

        "question":
            "أيُّ مكوّن من مكوّنات الدم يساعد بصورة أساسية "
            "على تجلط الدم عند حدوث جرح؟",

        "options": [
            "خلايا الدم الحمراء",
            "خلايا الدم البيضاء",
            "الصفائح الدموية",
            "البلازما"
        ],

        "answer": "الصفائح الدموية",

        "hint1":
            "فكري في المكوّن الذي يساعد الجسم على إيقاف "
            "النزيف بعد حدوث الجرح.",

        "hint2":
            "خلايا الدم البيضاء ترتبط بالدفاع عن الجسم، "
            "أما المطلوب هنا فهو مكوّن يشارك في تكوين الخثرة.",

        "lesson":
            "عند حدوث جرح، تشارك الصفائح الدموية في عملية "
            "تجلط الدم، مما يساعد على تقليل فقدان الدم.",

        "equivalent":
            "تعرضت طالبة لجرح صغير في يدها، فما مكوّن الدم "
            "الذي يؤدي دورًا مهمًا في إيقاف النزيف؟"
    },

    {
        "id": "C03-Q01",
        "concept": "خلايا الدم الحمراء",

        "question":
            "ما الوظيفة الأساسية لخلايا الدم الحمراء؟",

        "options": [
            "الدفاع عن الجسم",
            "المساعدة على تجلط الدم",
            "نقل الأكسجين",
            "إنتاج الأجسام المضادة"
        ],

        "answer": "نقل الأكسجين",

        "hint1":
            "فكري في المادة التي تحتاج إليها خلايا الجسم "
            "لإطلاق الطاقة.",

        "hint2":
            "تحتوي خلايا الدم الحمراء على الهيموجلوبين، "
            "وهو يرتبط بأحد الغازات المهمة للجسم.",

        "lesson":
            "تحتوي خلايا الدم الحمراء على الهيموجلوبين، "
            "وتؤدي دورًا أساسيًا في نقل الأكسجين.",

        "equivalent":
            "أي مكوّن من مكونات الدم ينقل الأكسجين "
            "إلى خلايا الجسم؟"
    },

    {
        "id": "C08-Q01",
        "concept": "الدورة الدموية",

        "question":
            "أي دورة دموية ينتقل فيها الدم من القلب "
            "إلى الرئتين ثم يعود إلى القلب؟",

        "options": [
            "الدورة الجسمية",
            "الدورة الرئوية",
            "الدورة القلبية",
            "الدورة اللمفية"
        ],

        "answer": "الدورة الرئوية",

        "hint1":
            "ركزي على العضو الذي ينتقل إليه الدم "
            "في السؤال.",

        "hint2":
            "اسم هذه الدورة مرتبط بالرئتين مباشرة.",

        "lesson":
            "في الدورة الرئوية ينتقل الدم من القلب إلى "
            "الرئتين، حيث يحدث تبادل الغازات، ثم يعود إلى القلب.",

        "equivalent":
            "ما اسم الدورة التي يذهب فيها الدم إلى الرئتين "
            "للتخلص من ثاني أكسيد الكربون والحصول على الأكسجين؟"
    }
]


# =========================================================
# التنسيق
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        direction: rtl;
        background: linear-gradient(
            135deg,
            #fff8fa 0%,
            #f7f9ff 100%
        );
    }

    .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4, p, label {
        direction: rtl;
        text-align: right;
    }

    div.stButton > button {
        width: 100%;
        min-height: 52px;
        border-radius: 14px;
        font-size: 17px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# الشعار
# =========================================================

st.markdown(
    "<h1 style='text-align:center;color:#d94b68;'>❤️ نبضة AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center;
    color:#64748b;
    font-size:18px;'>
    مساعدتك الذكية التكيفية في مادة العلوم
    </p>
    """,
    unsafe_allow_html=True
)

st.write("")


# =========================================================
# شاشة الدخول
# =========================================================

if not st.session_state.logged_in:

    with st.container(border=True):

        st.markdown("## 🌷 مرحبًا بكِ")

        st.write(
            "هذه البيئة التعليمية مخصصة للمشاركات "
            "المصرح لهن في الدراسة."
        )

    access_code = st.text_input(
        "رمز الدخول الخاص بكِ",
        type="password",
        placeholder="أدخلي رمز الدخول"
    )

    if st.button(
        "دخول إلى نبضة ❤️",
        type="primary"
    ):

        if access_code.strip():

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.warning(
                "يرجى إدخال رمز الدخول."
            )

    st.caption(
        "🔒 لا تكتبي اسمكِ أو أي بيانات شخصية."
    )


# =========================================================
# شاشة البداية
# =========================================================

elif not st.session_state.started:

    st.success(
        "🌷 أهلًا بكِ في جلسة اليوم"
    )

    st.write(
        "ستقدم لكِ نبضة أسئلة تتغير المساعدة فيها "
        "وفق إجاباتكِ ومحاولاتكِ."
    )

    with st.container(border=True):

        st.markdown(
            "### 🫀 جهازا الدوران والمناعة"
        )

        st.write(
            "اقرئي كل سؤال جيدًا ثم اختاري الإجابة."
        )

        st.write(
            "إذا كانت الإجابة غير صحيحة، "
            "ستساعدكِ نبضة تدريجيًا دون إعطائكِ "
            "الإجابة مباشرة."
        )

    st.progress(0)

    st.caption(
        "التقدم في جلسة اليوم: 0%"
    )

    if st.button(
        "ابدئي جلسة اليوم ←",
        type="primary"
    ):

        st.session_state.started = True
        st.rerun()


# =========================================================
# انتهاء الجلسة
# =========================================================

elif st.session_state.completed:

    st.balloons()

    st.success(
        "🌟 أحسنتِ! أنهيتِ جلسة نبضة."
    )

    st.markdown(
        "### 📊 خريطة تعلمكِ الأولية"
    )

    for concept, level in st.session_state.mastery.items():

        if level >= 2:

            symbol = "🟢"
            text = "أداء جيد"

        elif level == 1:

            symbol = "🟡"
            text = "يحتاج إلى تعزيز"

        else:

            symbol = "🔴"
            text = "يحتاج إلى دعم"

        st.write(
            f"{symbol} **{concept}:** {text}"
        )

    st.info(
        "هذه الخريطة لا تمثل درجة نهائية، "
        "وإنما تساعد نبضة على اختيار ما تحتاجين "
        "إلى مراجعته لاحقًا."
    )

    if st.button(
        "إنهاء الجلسة ❤️"
    ):

        st.session_state.started = False
        st.session_state.completed = False
        st.session_state.question_index = 0
        st.session_state.attempt = 0
        st.session_state.hint_level = 0

        st.rerun()


# =========================================================
# الأسئلة
# =========================================================

else:

    index = st.session_state.question_index

    question = questions[index]

    progress = int(
        ((index + 1) / len(questions)) * 100
    )

    st.progress(
        (index + 1) / len(questions)
    )

    st.caption(
        f"التقدم في جلسة اليوم: {progress}%"
    )

    with st.container(border=True):

        st.markdown(
            f"#### 🌷 السؤال {index + 1}"
        )

        st.markdown(
            f"### {question['question']}"
        )

    # -----------------------------------------------------
    # الاختيارات
    # -----------------------------------------------------

    answer = st.radio(
        "اختاري إجابة واحدة:",
        question["options"],
        index=None,
        key=f"answer_{index}_{st.session_state.attempt}"
    )

    # -----------------------------------------------------
    # زر التحقق
    # -----------------------------------------------------

    if st.button(
        "تحققي من إجابتي",
        type="primary",
        key=f"check_{index}_{st.session_state.attempt}"
    ):

        if answer is None:

            st.warning(
                "اختاري إجابة أولًا 🌷"
            )

        elif answer == question["answer"]:

            st.success(
                "🌟 إجابة صحيحة!"
            )

            # تحديث مستوى المفهوم
            concept = question["concept"]

            st.session_state.mastery[concept] += 1

            st.session_state.feedback = "correct"

        else:

            st.session_state.attempt += 1

            if st.session_state.attempt == 1:

                st.session_state.hint_level = 1

            elif st.session_state.attempt == 2:

                st.session_state.hint_level = 2

            else:

                st.session_state.hint_level = 3

            st.session_state.feedback = "wrong"

        st.rerun()


    # =====================================================
    # إذا كانت الإجابة صحيحة
    # =====================================================

    if st.session_state.feedback == "correct":

        st.success(
            "🌟 أحسنتِ، إجابتكِ صحيحة."
        )

        st.info(
            "نبضة سجلت هذه الإجابة كدليل "
            "أولي على فهمكِ للمفهوم."
        )

        if st.button(
            "السؤال التالي ←",
            key=f"next_{index}"
        ):

            st.session_state.question_index += 1

            st.session_state.attempt = 0
            st.session_state.hint_level = 0
            st.session_state.feedback = ""

            if (
                st.session_state.question_index
                >= len(questions)
            ):

                st.session_state.completed = True

            st.rerun()


    # =====================================================
    # التلميح الأول
    # =====================================================

    elif st.session_state.hint_level == 1:

        st.warning(
            "ليست الإجابة الأدق بعد."
        )

        st.info(
            "💡 تلميح نبضة H1:\n\n"
            + question["hint1"]
        )

        st.caption(
            "حاولي مرة أخرى اعتمادًا على التلميح."
        )


    # =====================================================
    # التلميح الثاني
    # =====================================================

    elif st.session_state.hint_level == 2:

        st.warning(
            "ما زلنا نحتاج إلى التفكير قليلًا."
        )

        st.info(
            "💡 تلميح نبضة H2:\n\n"
            + question["hint2"]
        )

        st.caption(
            "قارني بين وظيفة كل اختيار ثم حاولي مجددًا."
        )


    # =====================================================
    # الشرح المصغر
    # =====================================================

    elif st.session_state.hint_level >= 3:

        st.warning(
            "سأشرح لكِ الفكرة باختصار 🌷"
        )

        st.info(
            "📘 شرح نبضة:\n\n"
            + question["lesson"]
        )

        st.markdown(
            "### 🔄 والآن سؤال مشابه"
        )

        st.write(
            question["equivalent"]
        )

        equivalent_answer = st.radio(
            "اختاري الإجابة:",
            question["options"],
            index=None,
            key=f"equivalent_{index}"
        )

        if st.button(
            "تحققي من السؤال المشابه",
            key=f"equivalent_check_{index}"
        ):

            if equivalent_answer is None:

                st.warning(
                    "اختاري إجابة أولًا."
                )

            elif (
                equivalent_answer
                == question["answer"]
            ):

                st.success(
                    "🌟 ممتاز! وصلتِ إلى الفكرة."
                )

                concept = question["concept"]

                st.session_state.mastery[concept] += 1

                st.session_state.feedback = "correct"

                st.rerun()

            else:

                st.error(
                    "هذه الفكرة ما زالت تحتاج إلى دعم، "
                    "وسنعود إليها مرة أخرى في الجلسة."
                )
