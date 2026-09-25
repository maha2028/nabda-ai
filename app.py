import streamlit as st
import random
from questions import QUESTIONS, CONCEPTS

# =========================================================
# ScAI V3
# مساعد ذكي تكيفي لتعلم العلوم
# =========================================================

st.set_page_config(
    page_title="ScAI | تعلم العلوم",
    page_icon="🔬",
    layout="centered"
)

# =========================================================
# التصميم
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
}

.stApp {
    background: linear-gradient(
        180deg,
        #fffafd 0%,
        #f7f9ff 100%
    );
}

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.logo {
    text-align:center;
    font-size:58px;
    font-weight:800;
    color:#e34b70;
    margin-bottom:0;
}

.subtitle {
    text-align:center;
    font-size:25px;
    color:#5c6477;
    margin-top:-8px;
    margin-bottom:35px;
}

.question-box {
    background:white;
    border:1px solid #ece7eb;
    border-radius:22px;
    padding:28px;
    margin-top:20px;
    margin-bottom:20px;
    box-shadow:0 4px 15px rgba(0,0,0,.03);
}

.concept-card {
    background:#f4f7ff;
    border-radius:15px;
    padding:15px;
    margin-bottom:15px;
}

.correct-box {
    background:#e9f8ef;
    color:#167a3c;
    border-radius:15px;
    padding:18px;
    font-size:18px;
}

.hint-box {
    background:#eef5ff;
    color:#155da7;
    border-radius:15px;
    padding:18px;
}

.lesson-box {
    background:#fff8dc;
    color:#795d00;
    border-radius:15px;
    padding:20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# شعار
# =========================================================

st.markdown('<div class="logo">🔬 ScAI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">مساعدكِ الذكي التكيفي لتعلّم العلوم</div>',
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "logged_in": False,
    "started": False,
    "phase": "diagnostic",
    "current_question": None,
    "attempt": 0,
    "hint_level": 0,
    "show_lesson": False,
    "equivalent_mode": False,
    "feedback": "",
    "answered": False,
    "score": 0,
    "total_answered": 0,
    "seen": [],
    "diagnostic_done": [],
    "session_questions": 0,
    "max_session_questions": 12,
    "mastery": {},
    "history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# إنشاء خريطة الإتقان

for cid, name in CONCEPTS.items():

    if cid not in st.session_state.mastery:

        st.session_state.mastery[cid] = {
            "name": name,
            "correct": 0,
            "wrong": 0,
            "status": "⚪ لم يُقيّم"
        }


# =========================================================
# دوال مساعدة
# =========================================================

def reset_question_state():

    st.session_state.attempt = 0
    st.session_state.hint_level = 0
    st.session_state.show_lesson = False
    st.session_state.equivalent_mode = False
    st.session_state.feedback = ""
    st.session_state.answered = False


def update_mastery(cid, correct):

    data = st.session_state.mastery[cid]

    if correct:
        data["correct"] += 1
    else:
        data["wrong"] += 1

    c = data["correct"]
    w = data["wrong"]

    if c >= 2 and w == 0:
        data["status"] = "🟢 متقن"

    elif c >= 2 and c > w:
        data["status"] = "🟡 في طور الإتقان"

    elif w >= 1:
        data["status"] = "🔴 يحتاج دعماً"

    else:
        data["status"] = "⚪ لم يُقيّم"


def weak_concepts():

    weak = []

    for cid, data in st.session_state.mastery.items():

        if data["wrong"] > 0 or data["status"] == "🔴 يحتاج دعماً":
            weak.append(cid)

    return weak


def questions_for_concept(cid):

    return [
        q for q in QUESTIONS
        if q["concept_id"] == cid
    ]


def unseen_questions(pool):

    return [
        q for q in pool
        if q["id"] not in st.session_state.seen
    ]


# =========================================================
# اختيار السؤال تكيفياً
# =========================================================

def choose_next_question():

    # ------------------------------
    # المرحلة الأولى: التشخيص
    # ------------------------------

    if st.session_state.phase == "diagnostic":

        remaining_concepts = [
            cid for cid in CONCEPTS
            if cid not in st.session_state.diagnostic_done
        ]

        if remaining_concepts:

            cid = remaining_concepts[0]

            pool = questions_for_concept(cid)
            pool = unseen_questions(pool)

            if not pool:
                pool = questions_for_concept(cid)

            if pool:
                return random.choice(pool)

        st.session_state.phase = "adaptive"


    # ------------------------------
    # المرحلة التكيفية
    # ------------------------------

    weak = weak_concepts()

    if weak:

        random.shuffle(weak)

        for cid in weak:

            pool = unseen_questions(
                questions_for_concept(cid)
            )

            if pool:
                return random.choice(pool)


    # ------------------------------
    # إذا لم توجد نقاط ضعف
    # ------------------------------

    pool = unseen_questions(QUESTIONS)

    if pool:
        return random.choice(pool)

    return random.choice(QUESTIONS)


def load_next_question():

    reset_question_state()

    st.session_state.current_question = choose_next_question()


# =========================================================
# تسجيل الاستجابة
# =========================================================

def log_response(question, answer, correct):

    st.session_state.history.append({

        "question_id": question["id"],
        "concept_id": question["concept_id"],
        "answer": str(answer),
        "correct": correct,
        "attempt": st.session_state.attempt,
        "hint_level": st.session_state.hint_level

    })


# =========================================================
# تسجيل الدخول
# =========================================================

if not st.session_state.logged_in:

    st.info(
        "مرحباً بكِ في ScAI. "
        "هذه البيئة مخصصة للمشاركات المصرح لهن في الدراسة."
    )

    access_code = st.text_input(
        "أدخلي رمز الدخول البحثي",
        type="password",
        placeholder="رمز الدخول"
    )

    st.caption(
        "لا تكتبي اسمكِ أو أي بيانات شخصية."
    )

    if st.button(
        "دخول إلى ScAI",
        use_container_width=True
    ):

        # مؤقت للاختبار فقط
        if access_code.strip():

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.warning("أدخلي رمز الدخول.")

    st.stop()


# =========================================================
# شاشة البداية
# =========================================================

if not st.session_state.started:

    st.success("تم الدخول بنجاح 🌷")

    st.markdown("## كيف سيعمل ScAI معكِ؟")

    st.write(
        "سيبدأ بأسئلة تشخيصية قصيرة، ثم يحدد المفاهيم "
        "التي أتقنتِها والمفاهيم التي تحتاج إلى دعم."
    )

    st.write(
        "إذا كانت الإجابة غير صحيحة فلن يعطيكِ الحل مباشرة؛ "
        "سيقدم تلميحاً، ثم تلميحاً أقوى، ثم مراجعة قصيرة "
        "وسؤالاً مكافئاً."
    )

    st.write(
        "لن تحلي جميع أسئلة البنك. سيختار ScAI الأسئلة "
        "وفق أدائكِ."
    )

    if st.button(
        "ابدئي رحلة التعلم 🚀",
        use_container_width=True
    ):

        st.session_state.started = True
        load_next_question()
        st.rerun()

    st.stop()


# =========================================================
# نهاية الجلسة
# =========================================================

if (
    st.session_state.session_questions
    >= st.session_state.max_session_questions
):

    st.success("🌷 أحسنتِ! انتهت جلسة التعلم الحالية.")

    st.markdown("## 🧠 خريطة إتقانكِ")

    for cid, data in st.session_state.mastery.items():

        if (
            data["correct"] > 0
            or data["wrong"] > 0
        ):

            st.write(
                f"**{data['name']}** — "
                f"{data['status']}"
            )

    if st.session_state.total_answered > 0:

        percentage = round(
            (
                st.session_state.score
                / st.session_state.total_answered
            ) * 100
        )

        st.metric(
            "نسبة الإجابات الصحيحة",
            f"{percentage}%"
        )

    st.info(
        "ستُستخدم هذه الخريطة لتحديد المفاهيم "
        "التي تحتاج إلى مراجعة في الجلسة التالية."
    )

    if st.button(
        "بدء جلسة جديدة 🔄",
        use_container_width=True
    ):

        st.session_state.session_questions = 0
        st.session_state.phase = "adaptive"
        load_next_question()
        st.rerun()

    st.stop()


# =========================================================
# تحميل سؤال إذا لم يوجد
# =========================================================

if st.session_state.current_question is None:

    load_next_question()


question = st.session_state.current_question
cid = question["concept_id"]

concept_name = CONCEPTS[cid]


# =========================================================
# شريط التقدم
# =========================================================

progress = (
    st.session_state.session_questions
    / st.session_state.max_session_questions
)

st.progress(min(progress, 1.0))

st.caption(
    f"التقدم في جلسة اليوم: "
    f"{st.session_state.session_questions + 1} "
    f"من {st.session_state.max_session_questions}"
)


# =========================================================
# المفهوم الحالي
# =========================================================

status = st.session_state.mastery[cid]["status"]

st.markdown(
    f"""
    <div class="concept-card">
    <b>المفهوم الحالي:</b>
    {concept_name}
    &nbsp; | &nbsp;
    {status}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# السؤال
# =========================================================

st.markdown(
    f"""
    <div class="question-box">
    <h3>🌷 السؤال</h3>
    <h2>{question["question"]}</h2>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# الصورة
# =========================================================

if question.get("image"):

    try:

        st.image(
            question["image"],
            use_container_width=True
        )

    except Exception:

        st.caption(
            "تعذر عرض الصورة المرتبطة بهذا السؤال."
        )


# =========================================================
# تحديد نوع السؤال
# =========================================================

question_type = question.get("type", "mcq")

answer = None


# =========================================================
# اختيار من متعدد
# =========================================================

if question_type in ["mcq", "image_mcq"]:

    answer = st.radio(
        "اختاري إجابة واحدة:",
        question.get("options", []),
        index=None,
        key=f"answer_{question['id']}_{st.session_state.attempt}"
    )


# =========================================================
# صح / خطأ
# =========================================================

elif question_type == "true_false":

    answer = st.radio(
        "حددي صحة العبارة:",
        ["صح", "خطأ"],
        index=None,
        horizontal=True,
        key=f"tf_{question['id']}_{st.session_state.attempt}"
    )


# =========================================================
# إجابة قصيرة
# =========================================================

elif question_type == "short_answer":

    answer = st.text_input(
        "اكتبي إجابتكِ:",
        key=f"short_{question['id']}_{st.session_state.attempt}"
    )


# =========================================================
# ترتيب
# =========================================================

elif question_type == "sequence":

    st.caption(
        "اختاري الترتيب الصحيح للخطوات:"
    )

    answer = st.radio(
        "الترتيب:",
        question.get("options", []),
        index=None,
        key=f"sequence_{question['id']}_{st.session_state.attempt}"
    )


# =========================================================
# تحليل رسم / موقف
# =========================================================

elif question_type in ["diagram", "application"]:

    answer = st.radio(
        "اختاري الإجابة الأنسب:",
        question.get("options", []),
        index=None,
        key=f"diagram_{question['id']}_{st.session_state.attempt}"
    )


# =========================================================
# نوع احتياطي
# =========================================================

else:

    answer = st.radio(
        "اختاري إجابة واحدة:",
        question.get("options", []),
        index=None,
        key=f"default_{question['id']}_{st.session_state.attempt}"
    )


# =========================================================
# فحص الإجابة
# =========================================================

if not st.session_state.answered:

    if st.button(
        "تحققي من إجابتي",
        use_container_width=True,
        key=f"check_{question['id']}_{st.session_state.attempt}"
    ):

        if answer is None or str(answer).strip() == "":

            st.warning("اختاري أو اكتبي إجابة أولاً.")

        else:

            # ---------------------------------------------
            # مقارنة الإجابة
            # ---------------------------------------------

            correct_answer = str(
                question["answer"]
            ).strip()

            student_answer = str(answer).strip()

            correct = (
                student_answer.lower()
                == correct_answer.lower()
            )


            # ---------------------------------------------
            # صحيحة
            # ---------------------------------------------

            if correct:

                st.session_state.feedback = "correct"

                st.session_state.score += 1
                st.session_state.total_answered += 1

                update_mastery(cid, True)

                log_response(
                    question,
                    answer,
                    True
                )

                if question["id"] not in st.session_state.seen:
                    st.session_state.seen.append(
                        question["id"]
                    )

                if (
                    st.session_state.phase == "diagnostic"
                    and cid not in st.session_state.diagnostic_done
                ):

                    st.session_state.diagnostic_done.append(
                        cid
                    )

                st.session_state.answered = True

                st.rerun()


            # ---------------------------------------------
            # غير صحيحة
            # ---------------------------------------------

            else:

                st.session_state.attempt += 1

                # نسجل الخطأ مرة واحدة فقط
                if st.session_state.attempt == 1:

                    st.session_state.total_answered += 1

                    update_mastery(
                        cid,
                        False
                    )

                    log_response(
                        question,
                        answer,
                        False
                    )

                # التلميح الأول
                if st.session_state.attempt == 1:

                    st.session_state.hint_level = 1

                # التلميح الثاني
                elif st.session_state.attempt == 2:

                    st.session_state.hint_level = 2

                # بعد المحاولتين تظهر المراجعة
                else:

                    st.session_state.show_lesson = True

                st.rerun()


# =========================================================
# التغذية الراجعة الصحيحة
# =========================================================

if st.session_state.feedback == "correct":

    st.markdown(
        """
        <div class="correct-box">
        🌟 إجابة صحيحة. أحسنتِ!
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "السؤال التالي ➜",
        use_container_width=True
    ):

        st.session_state.session_questions += 1

        load_next_question()

        st.rerun()


# =========================================================
# التلميح الأول
# =========================================================

if (
    st.session_state.hint_level >= 1
    and not st.session_state.show_lesson
):

    st.markdown(
        f"""
        <div class="hint-box">
        💡 <b>التلميح الأول:</b><br><br>
        {question.get("hint1", "")}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# التلميح الثاني
# =========================================================

if (
    st.session_state.hint_level >= 2
    and not st.session_state.show_lesson
):

    st.markdown(
        f"""
        <div class="hint-box">
        💡 <b>التلميح الثاني:</b><br><br>
        {question.get("hint2", "")}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# المراجعة العلاجية
# =========================================================

if st.session_state.show_lesson:

    lesson = question.get(
        "micro_lesson",
        question.get("lesson", "")
    )

    st.markdown(
        f"""
        <div class="lesson-box">
        📘 <b>مراجعة سريعة</b>
        <br><br>
        {lesson}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "بعد المراجعة سيختبر ScAI الفكرة مرة أخرى."
    )

    if st.button(
        "فهمتُ، اختبريني بسؤال مكافئ 🧠",
        use_container_width=True
    ):

        st.session_state.equivalent_mode = True
        st.session_state.show_lesson = False
        st.rerun()


# =========================================================
# السؤال المكافئ
# =========================================================

if st.session_state.equivalent_mode:

    st.markdown("---")

    st.markdown("### 🧠 سؤال مكافئ")

    equivalent_question = question.get(
        "equivalent",
        question["question"]
    )

    st.write(equivalent_question)

    # يستخدم نفس الاختيارات مؤقتاً
    equivalent_answer = st.radio(
        "اختاري إجابتكِ:",
        question.get("options", []),
        index=None,
        key=f"equiv_{question['id']}"
    )

    if st.button(
        "تحققي من السؤال المكافئ",
        use_container_width=True,
        key=f"check_equiv_{question['id']}"
    ):

        if equivalent_answer is None:

            st.warning("اختاري إجابة أولاً.")

        elif (
            str(equivalent_answer).strip().lower()
            ==
            str(question["answer"]).strip().lower()
        ):

            update_mastery(
                cid,
                True
            )

            st.session_state.feedback = "equivalent_correct"

            st.session_state.answered = True

            st.rerun()

        else:

            update_mastery(
                cid,
                False
            )

            st.session_state.feedback = "equivalent_wrong"

            st.session_state.answered = True

            st.rerun()


# =========================================================
# نتيجة السؤال المكافئ
# =========================================================

if st.session_state.feedback == "equivalent_correct":

    st.success(
        "🌟 ممتاز! يبدو أنكِ فهمتِ الفكرة الآن."
    )

    if st.button(
        "متابعة التعلم ➜",
        use_container_width=True,
        key="continue_equiv_correct"
    ):

        st.session_state.session_questions += 1

        load_next_question()

        st.rerun()


elif st.session_state.feedback == "equivalent_wrong":

    st.warning(
        "لا بأس. سيعيد ScAI هذا المفهوم لاحقاً "
        "بطريقة مختلفة."
    )

    if st.button(
        "متابعة التعلم ➜",
        use_container_width=True,
        key="continue_equiv_wrong"
    ):

        st.session_state.session_questions += 1

        load_next_question()

        st.rerun()


# =========================================================
# خريطة الإتقان
# =========================================================

with st.expander("🧠 خريطة إتقاني"):

    for cid, data in st.session_state.mastery.items():

        st.write(
            f"**{data['name']}** — "
            f"{data['status']}"
        )
