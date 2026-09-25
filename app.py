import streamlit as st
from questions import QUESTIONS, CONCEPTS

# =========================================================
# ScAI - المساعد الذكي التكيفي لتعلم العلوم
# =========================================================

st.set_page_config(
    page_title="ScAI",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# تنسيق الواجهة
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
        background: linear-gradient(180deg, #fffafd 0%, #f7f9ff 100%);
    }

    h1, h2, h3, p, div, label {
        direction: rtl;
        text-align: right;
    }

    .main-title {
        text-align: center;
        font-size: 54px;
        font-weight: 800;
        color: #d94b70;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #596275;
        font-size: 20px;
        margin-bottom: 25px;
    }

    .question-box {
        padding: 22px;
        border: 1px solid #e4dce3;
        border-radius: 15px;
        background: white;
        margin: 15px 0;
        font-size: 22px;
        font-weight: 700;
    }

    .info-box {
        padding: 16px;
        border-radius: 14px;
        background: #eaf3ff;
        color: #075fae;
        margin: 12px 0;
    }

    .mastery-box {
        padding: 12px;
        border-radius: 12px;
        background: white;
        border: 1px solid #ececec;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# رأس الصفحة
# =========================================================

st.markdown('<div class="main-title">ScAI 🔬</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">مساعدكِ الذكي التكيفي لتعلُّم العلوم</div>',
    unsafe_allow_html=True
)

# =========================================================
# حالة الجلسة
# =========================================================

defaults = {
    "logged_in": False,
    "student_code": "",
    "started": False,

    "question_index": 0,
    "attempt": 0,
    "score": 0,
    "total_answered": 0,

    "feedback": "",
    "hint_level": 0,
    "show_lesson": False,
    "equivalent_mode": False,
    "answered": False,

    "completed": False,

    "phase": "diagnostic",
    "diagnostic_done": [],

    "seen": [],

    "mastery": {}
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# إنشاء خريطة إتقان لجميع المفاهيم
for concept_id, concept_name in CONCEPTS.items():
    if concept_id not in st.session_state.mastery:
        st.session_state.mastery[concept_id] = {
            "name": concept_name,
            "correct": 0,
            "wrong": 0,
            "status": "⚪ لم يُقيَّم"
        }

# =========================================================
# وظائف مساعدة
# =========================================================

def reset_question_state():
    st.session_state.attempt = 0
    st.session_state.feedback = ""
    st.session_state.hint_level = 0
    st.session_state.show_lesson = False
    st.session_state.equivalent_mode = False
    st.session_state.answered = False


def update_mastery(concept_id, correct):
    if concept_id not in st.session_state.mastery:
        st.session_state.mastery[concept_id] = {
            "name": CONCEPTS.get(concept_id, concept_id),
            "correct": 0,
            "wrong": 0,
            "status": "⚪ لم يُقيَّم"
        }

    data = st.session_state.mastery[concept_id]

    if correct:
        data["correct"] += 1
    else:
        data["wrong"] += 1

    c = data["correct"]
    w = data["wrong"]

    if c >= 2 and w == 0:
        data["status"] = "🟢 متقن"
    elif c >= 1 and c >= w:
        data["status"] = "🟡 في طور الإتقان"
    elif w >= 1:
        data["status"] = "🔴 يحتاج دعمًا"
    else:
        data["status"] = "⚪ لم يُقيَّم"


def move_next():
    st.session_state.question_index += 1
    reset_question_state()

    if st.session_state.question_index >= len(QUESTIONS):
        st.session_state.completed = True
        st.session_state.question_index = max(len(QUESTIONS) - 1, 0)


def restart():
    keys_to_reset = [
        "started",
        "question_index",
        "attempt",
        "score",
        "total_answered",
        "feedback",
        "hint_level",
        "show_lesson",
        "equivalent_mode",
        "answered",
        "completed",
        "phase",
        "diagnostic_done",
        "seen"
    ]

    for key in keys_to_reset:
        if key in defaults:
            st.session_state[key] = defaults[key]

    st.session_state.mastery = {}

    for concept_id, concept_name in CONCEPTS.items():
        st.session_state.mastery[concept_id] = {
            "name": concept_name,
            "correct": 0,
            "wrong": 0,
            "status": "⚪ لم يُقيَّم"
        }


def normalize_text(text):
    if text is None:
        return ""

    text = str(text).strip().lower()

    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ة": "ه",
        "ى": "ي"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return " ".join(text.split())


def is_correct_answer(question, answer):
    if answer is None:
        return False

    expected = question.get("answer", "")

    if question.get("type", "mcq") == "short_answer":
        user_answer = normalize_text(answer)

        accepted = question.get("accepted_answers", [])

        if not accepted:
            accepted = [expected]

        accepted = [normalize_text(x) for x in accepted]

        return user_answer in accepted

    return str(answer).strip() == str(expected).strip()


def show_mastery_map():
    with st.expander("🧠 خريطة إتقاني", expanded=False):

        for concept_id, data in st.session_state.mastery.items():
            st.markdown(
                f"""
                <div class="mastery-box">
                <b>{data['name']}</b><br>
                {data['status']}<br>
                صحيحة: {data['correct']} |
                تحتاج مراجعة: {data['wrong']}
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# تسجيل الدخول
# =========================================================

if not st.session_state.logged_in:

    st.info(
        "مرحبًا بكِ في ScAI. هذه البيئة مخصصة للمشاركات المصرح لهن في الدراسة."
    )

    code = st.text_input(
        "أدخلي رمز الدخول البحثي",
        type="password",
        placeholder="رمز الدخول"
    )

    st.caption("لا تكتبي اسمكِ أو أي بيانات شخصية.")

    if st.button("دخول إلى ScAI", use_container_width=True):

        # مؤقت أثناء التطوير:
        # أي رمز غير فارغ يسمح بالدخول.
        # لاحقًا ستُنقل الرموز الحقيقية إلى Streamlit Secrets.

        if code.strip():
            st.session_state.logged_in = True
            st.session_state.student_code = code.strip()
            st.rerun()
        else:
            st.warning("أدخلي رمز الدخول أولًا.")

    st.stop()

# =========================================================
# الصفحة الترحيبية
# =========================================================

if not st.session_state.started:

    st.success("تم الدخول بنجاح 🌷")

    st.markdown(
        """
        ### كيف سيعمل ScAI معكِ؟

        سيبدأ بأسئلة قصيرة للتعرّف إلى المفاهيم التي تتقنينها
        والمفاهيم التي تحتاج إلى دعم.

        إذا كانت الإجابة غير صحيحة فلن يعطيكِ الحل مباشرة؛
        بل سيقدّم تلميحًا، ثم تلميحًا أقوى، ثم مراجعة قصيرة،
        وبعدها سؤالًا مكافئًا للتأكد من الفهم.
        """
    )

    if st.button("ابدئي رحلة التعلم 🚀", use_container_width=True):
        st.session_state.started = True
        st.rerun()

    show_mastery_map()
    st.stop()

# =========================================================
# إذا لم توجد أسئلة
# =========================================================

if not QUESTIONS:
    st.error("لا توجد أسئلة في questions.py.")
    st.stop()

# =========================================================
# انتهاء الرحلة
# =========================================================

if st.session_state.completed:

    st.success("🎉 أحسنتِ! اكتملت هذه الجولة التعليمية.")

    st.metric(
        "عدد الإجابات الصحيحة",
        st.session_state.score
    )

    st.metric(
        "عدد الأسئلة التي تمت معالجتها",
        st.session_state.total_answered
    )

    st.markdown("### 🧠 خريطة الإتقان النهائية")

    for concept_id, data in st.session_state.mastery.items():
        st.markdown(
            f"""
            <div class="mastery-box">
            <b>{data['name']}</b><br>
            {data['status']}<br>
            صحيحة: {data['correct']} |
            تحتاج مراجعة: {data['wrong']}
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button("بدء جولة جديدة 🔄", use_container_width=True):
        restart()
        st.rerun()

    st.stop()

# =========================================================
# السؤال الحالي
# =========================================================

question = QUESTIONS[st.session_state.question_index]

cid = question.get("concept_id", "")
concept_name = CONCEPTS.get(
    cid,
    question.get("concept", "مفهوم علمي")
)

# =========================================================
# شريط التقدم
# =========================================================

progress = (st.session_state.question_index + 1) / len(QUESTIONS)

st.progress(min(progress, 1.0))

st.caption(
    f"التقدم في جلسة اليوم: "
    f"{st.session_state.question_index + 1} من {len(QUESTIONS)}"
)

status = st.session_state.mastery.get(
    cid,
    {"status": "⚪ لم يُقيَّم"}
)["status"]

st.caption(
    f"المفهوم الحالي: {concept_name} | {status}"
)

# =========================================================
# صندوق السؤال
# =========================================================

st.markdown(
    f"""
    <div class="question-box">
    🌷 السؤال {st.session_state.question_index + 1}
    <br><br>
    {question.get('question', '')}
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# صورة السؤال إن وجدت
# =========================================================

if question.get("image"):
    try:
        st.image(
            question["image"],
            use_container_width=True
        )
    except Exception:
        st.warning("تعذر عرض صورة هذا السؤال.")

# =========================================================
# الوضع العادي للسؤال
# =========================================================

if not st.session_state.equivalent_mode:

    question_type = question.get("type", "mcq")

    # -------------------------
    # اختيار من متعدد
    # -------------------------

    if question_type in ["mcq", "image_mcq"]:

        answer = st.radio(
            "اختاري إجابة واحدة:",
            question.get("options", []),
            index=None,
            key=f"main_{question['id']}_{st.session_state.attempt}"
        )

    # -------------------------
    # صح أو خطأ
    # -------------------------

    elif question_type == "true_false":

        answer = st.radio(
            "حددي صحة العبارة:",
            ["صح", "خطأ"],
            index=None,
            horizontal=True,
            key=f"tf_{question['id']}_{st.session_state.attempt}"
        )

    # -------------------------
    # إجابة قصيرة
    # -------------------------

    elif question_type == "short_answer":

        answer = st.text_input(
            "اكتبي إجابتك:",
            key=f"short_{question['id']}_{st.session_state.attempt}"
        )

    # -------------------------
    # ترتيب
    # -------------------------

    elif question_type == "sequence":

        st.caption("اختاري الترتيب الصحيح:")

        answer = st.radio(
            "الترتيب:",
            question.get("options", []),
            index=None,
            key=f"sequence_{question['id']}_{st.session_state.attempt}"
        )

    # -------------------------
    # افتراضي
    # -------------------------

    else:

        answer = st.radio(
            "اختاري إجابة واحدة:",
            question.get("options", []),
            index=None,
            key=f"default_{question['id']}_{st.session_state.attempt}"
        )

    # =====================================================
    # زر التحقق
    # =====================================================

    if st.button(
        "تحققي من إجابتي",
        use_container_width=True,
        key=f"check_{question['id']}_{st.session_state.attempt}"
    ):

        if answer is None or str(answer).strip() == "":
            st.warning("اختاري أو اكتبي إجابة أولًا.")

        elif is_correct_answer(question, answer):

            st.session_state.feedback = "correct"
            st.session_state.score += 1
            st.session_state.total_answered += 1

            update_mastery(cid, True)

            if question["id"] not in st.session_state.seen:
                st.session_state.seen.append(question["id"])

            if (
                st.session_state.phase == "diagnostic"
                and cid not in st.session_state.diagnostic_done
            ):
                st.session_state.diagnostic_done.append(cid)

            st.session_state.answered = True
            st.rerun()

        else:

            st.session_state.attempt += 1

            if st.session_state.attempt == 1:
                st.session_state.total_answered += 1
                update_mastery(cid, False)
                st.session_state.hint_level = 1

            elif st.session_state.attempt == 2:
                st.session_state.hint_level = 2

            else:
                st.session_state.show_lesson = True

            st.rerun()

# =========================================================
# تغذية راجعة للإجابة الصحيحة
# =========================================================

if (
    st.session_state.feedback == "correct"
    and not st.session_state.equivalent_mode
):

    st.success("🌟 إجابة صحيحة، أحسنتِ!")

    if st.button(
        "السؤال التالي ➜",
        use_container_width=True,
        key="next_after_correct"
    ):
        move_next()
        st.rerun()

# =========================================================
# التلميح الأول
# =========================================================

if (
    st.session_state.hint_level >= 1
    and not st.session_state.answered
    and not st.session_state.equivalent_mode
):

    hint1 = question.get("hint1", "")

    if hint1:
        st.info(
            "💡 **التلميح الأول:**\n\n"
            + hint1
        )

# =========================================================
# التلميح الثاني
# =========================================================

if (
    st.session_state.hint_level >= 2
    and not st.session_state.answered
    and not st.session_state.equivalent_mode
):

    hint2 = question.get("hint2", "")

    if hint2:
        st.info(
            "💡 **التلميح الثاني:**\n\n"
            + hint2
        )

# =========================================================
# المراجعة المصغرة
# =========================================================

if (
    st.session_state.show_lesson
    and not st.session_state.equivalent_mode
):

    st.warning(
        "سنراجع الفكرة سريعًا ثم نجرب سؤالًا مكافئًا."
    )

    st.markdown("## 📘 مراجعة سريعة")

    lesson = question.get(
        "micro_lesson",
        question.get("lesson", "")
    )

    if lesson:
        st.info(lesson)

    if st.button(
        "فهمت، اختبريني بسؤال آخر",
        use_container_width=True,
        key=f"equiv_start_{question['id']}"
    ):
        st.session_state.equivalent_mode = True
        st.session_state.feedback = ""
        st.rerun()

# =========================================================
# السؤال المكافئ
# =========================================================

if st.session_state.equivalent_mode:

    st.markdown("### 🔄 سؤال للتأكد من الفهم")

    equivalent = question.get(
        "equivalent",
        question.get("question", "")
    )

    st.markdown(
        f"""
        <div class="question-box">
        {equivalent}
        </div>
        """,
        unsafe_allow_html=True
    )

    # إذا كان لدينا خيارات مكافئة مستقلة نستخدمها،
    # وإلا نستخدم خيارات السؤال الأصلي.

    equivalent_options = question.get(
        "equivalent_options",
        question.get("options", [])
    )

    equivalent_answer = question.get(
        "equivalent_answer",
        question.get("answer", "")
    )

    question_type = question.get("type", "mcq")

    if question_type == "short_answer":

        eq_answer = st.text_input(
            "اكتبي إجابتك:",
            key=f"equiv_short_{question['id']}"
        )

    elif question_type == "true_false":

        eq_answer = st.radio(
            "حددي صحة العبارة:",
            ["صح", "خطأ"],
            index=None,
            horizontal=True,
            key=f"equiv_tf_{question['id']}"
        )

    else:

        eq_answer = st.radio(
            "اختاري إجابة واحدة:",
            equivalent_options,
            index=None,
            key=f"equiv_{question['id']}"
        )

    if st.button(
        "تحققي من السؤال المكافئ",
        use_container_width=True,
        key=f"check_equiv_{question['id']}"
    ):

        if eq_answer is None or str(eq_answer).strip() == "":
            st.warning("أجيبي أولًا.")

        else:

            if question_type == "short_answer":

                temp_question = dict(question)
                temp_question["answer"] = equivalent_answer

                if question.get("equivalent_accepted_answers"):
                    temp_question["accepted_answers"] = (
                        question["equivalent_accepted_answers"]
                    )

                correct_equivalent = is_correct_answer(
                    temp_question,
                    eq_answer
                )

            else:
                correct_equivalent = (
                    str(eq_answer).strip()
                    == str(equivalent_answer).strip()
                )

            if correct_equivalent:

                update_mastery(cid, True)

                st.session_state.feedback = "equivalent_correct"
                st.session_state.answered = True
                st.rerun()

            else:

                update_mastery(cid, False)

                st.session_state.feedback = "equivalent_wrong"
                st.rerun()

# =========================================================
# نتيجة السؤال المكافئ
# =========================================================

if st.session_state.feedback == "equivalent_correct":

    st.success(
        "🌟 ممتاز! الآن أظهرتِ فهمًا أفضل للمفهوم."
    )

    if st.button(
        "متابعة التعلم ➜",
        use_container_width=True,
        key="continue_after_equiv_correct"
    ):
        move_next()
        st.rerun()


elif st.session_state.feedback == "equivalent_wrong":

    st.error(
        "هذا المفهوم ما زال يحتاج إلى دعم. "
        "سنعود إليه مرة أخرى أثناء التعلم."
    )

    if st.button(
        "متابعة التعلم ➜",
        use_container_width=True,
        key="continue_after_equiv_wrong"
    ):
        move_next()
        st.rerun()

# =========================================================
# خريطة الإتقان
# =========================================================

show_mastery_map()

# =========================================================
# تنبيه منهجي
# =========================================================

st.caption(
    "ScAI يستخدم المحتوى التعليمي المعتمد للدراسة، "
    "وتُستخدم الاستجابات لتكييف مسار التعلم دون الحاجة "
    "إلى إدخال الاسم أو البيانات الشخصية."
)
