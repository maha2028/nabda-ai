import streamlit as st
from questions import QUESTIONS, CONCEPTS

# =========================================================
# ScAI - مساعد التعلم الذكي التكيفي للعلوم
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

st.markdown("""
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

    .mastery-box {
        padding: 12px;
        border-radius: 12px;
        background: white;
        border: 1px solid #ececec;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# حالة الجلسة
# =========================================================

defaults = {
    "logged_in": False,
    "started": False,
    "question_index": 0,
    "attempt": 0,
    "score": 0,
    "feedback": "",
    "hint_level": 0,
    "show_lesson": False,
    "equivalent_mode": False,
    "completed": False,
    "mastery": {},
    "answered": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# إنشاء خريطة إتقان لكل المفاهيم
for concept_id, concept_name in CONCEPTS.items():
    if concept_name not in st.session_state.mastery:
        st.session_state.mastery[concept_name] = {
            "correct": 0,
            "wrong": 0,
            "status": "⚪ لم يُقَيَّم"
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


def update_mastery(concept, correct):
    data = st.session_state.mastery[concept]

    if correct:
        data["correct"] += 1
    else:
        data["wrong"] += 1

    c = data["correct"]
    w = data["wrong"]

    if c >= 2 and w == 0:
        data["status"] = "🟢 متقن"
    elif c >= 1:
        data["status"] = "🟡 في طور الإتقان"
    else:
        data["status"] = "🔴 يحتاج دعمًا"


def next_question():
    st.session_state.question_index += 1
    reset_question_state()

    if st.session_state.question_index >= len(QUESTIONS):
        st.session_state.completed = True


def restart_session():
    st.session_state.started = False
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.completed = False
    reset_question_state()


# =========================================================
# رأس التطبيق
# =========================================================

st.markdown('<div class="main-title">ScAI 🔬</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">مساعدكِ الذكي التكيفي لتعلّم العلوم</div>',
    unsafe_allow_html=True
)

# =========================================================
# تسجيل الدخول
# =========================================================

if not st.session_state.logged_in:

    st.info(
        "مرحبًا بكِ في ScAI. هذه البيئة مخصصة للمشاركات "
        "المصرح لهن في الدراسة."
    )

    code = st.text_input(
        "أدخلي رمز الدخول البحثي",
        type="password",
        placeholder="رمز الدخول"
    )

    st.caption("لا تكتبي اسمكِ أو أي بيانات شخصية.")

    if st.button("دخول إلى ScAI", use_container_width=True):
        # مؤقت للاختبار فقط - سنستبدله لاحقًا برموز آمنة
        if code.strip():
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("يرجى إدخال رمز الدخول.")

    st.stop()

# =========================================================
# شاشة البداية
# =========================================================

if not st.session_state.started:

    st.success("تم تسجيل الدخول بنجاح 🌷")

    st.markdown("""
    ### كيف يعمل ScAI؟

    سيقدم لكِ ScAI مجموعة من الأسئلة في العلوم.

    إذا كانت إجابتكِ صحيحة فسيتقدم بكِ في التعلم.

    وإذا احتجتِ إلى مساعدة، سيقدم لكِ تلميحات تدريجية
    وشرحًا قصيرًا ثم يتحقق من فهمكِ مرة أخرى.
    """)

    if st.button("ابدئي جلسة التعلّم 🚀", use_container_width=True):
        st.session_state.started = True
        st.rerun()

    st.stop()

# =========================================================
# نهاية الجلسة
# =========================================================

if st.session_state.completed:

    st.balloons()

    st.success("أحسنتِ 🌟 لقد أكملتِ جلسة ScAI.")

    st.metric(
        "عدد الإجابات الصحيحة",
        f"{st.session_state.score} من {len(QUESTIONS)}"
    )

    st.subheader("🧠 خريطة تعلّمكِ")

    for concept_id, concept_name in CONCEPTS.items():
        data = st.session_state.mastery[concept_name]

        st.markdown(
            f"""
            <div class="mastery-box">
            <b>{concept_name}</b><br>
            {data["status"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button("بدء جلسة جديدة"):
        restart_session()
        st.rerun()

    st.stop()

# =========================================================
# السؤال الحالي
# =========================================================

index = st.session_state.question_index
question = QUESTIONS[index]
concept = question["concept"]

progress = index / len(QUESTIONS)

st.progress(progress)

st.caption(
    f"التقدم في جلسة اليوم: "
    f"{index + 1} من {len(QUESTIONS)}"
)

st.caption(
    f"المفهوم الحالي: {concept} | "
    f"{st.session_state.mastery[concept]['status']}"
)

# صورة السؤال إذا أضيفت لاحقًا
if question.get("image"):
    try:
        st.image(question["image"], use_container_width=True)
    except Exception:
        pass

# =========================================================
# السؤال الأساسي
# =========================================================

if not st.session_state.equivalent_mode:

    st.markdown(
        f"""
        <div class="question-box">
        🌷 السؤال {index + 1}<br><br>
        {question["question"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    answer = st.radio(
        "اختاري إجابة واحدة:",
        question["options"],
        index=None,
        key=f"main_{question['id']}_{st.session_state.attempt}"
    )

    if st.button(
        "تحققي من إجابتي",
        use_container_width=True,
        key=f"check_{question['id']}"
    ):

        if answer is None:
            st.warning("اختاري إجابة أولًا.")

        elif answer == question["answer"]:

            st.session_state.score += 1
            update_mastery(concept, True)

            st.session_state.feedback = (
                "✅ ممتاز! إجابتكِ صحيحة."
            )

            st.session_state.answered = True
            st.rerun()

        else:

            update_mastery(concept, False)
            st.session_state.attempt += 1

            if st.session_state.attempt == 1:
                st.session_state.hint_level = 1
                st.session_state.feedback = (
                    "ليست الإجابة الصحيحة بعد. "
                    "استخدمي التلميح الأول ثم حاولي مرة أخرى."
                )

            elif st.session_state.attempt == 2:
                st.session_state.hint_level = 2
                st.session_state.feedback = (
                    "محاولة جيدة. إليكِ تلميحًا أكثر تحديدًا."
                )

            else:
                st.session_state.show_lesson = True
                st.session_state.feedback = (
                    "سنراجع الفكرة سريعًا ثم نجرب سؤالًا مكافئًا."
                )

            st.rerun()

# =========================================================
# التغذية الراجعة
# =========================================================

if st.session_state.feedback:
    if st.session_state.answered:
        st.success(st.session_state.feedback)
    else:
        st.warning(st.session_state.feedback)

# =========================================================
# إذا كانت الإجابة صحيحة
# =========================================================

if st.session_state.answered:

    st.info(
        f"حالة المفهوم الآن: "
        f"{st.session_state.mastery[concept]['status']}"
    )

    if st.button(
        "السؤال التالي ➜",
        use_container_width=True,
        key=f"next_{question['id']}"
    ):
        next_question()
        st.rerun()

    st.stop()

# =========================================================
# التلميحات
# =========================================================

if (
    st.session_state.hint_level >= 1
    and not st.session_state.show_lesson
):

    st.info(
        f"💡 التلميح الأول:\n\n"
        f"{question['hint1']}"
    )

if (
    st.session_state.hint_level >= 2
    and not st.session_state.show_lesson
):

    st.info(
        f"💡 التلميح الثاني:\n\n"
        f"{question['hint2']}"
    )

# =========================================================
# الشرح المصغر
# =========================================================

if st.session_state.show_lesson:

    lesson_text = question.get(
        "micro_lesson",
        question.get("lesson", "")
    )

    st.markdown("### 📘 مراجعة سريعة")

    st.info(lesson_text)

    if st.button(
        "فهمتُ، اختبريني بسؤال آخر",
        use_container_width=True,
        key=f"equiv_start_{question['id']}"
    ):
        st.session_state.equivalent_mode = True
        st.session_state.show_lesson = False
        st.session_state.feedback = ""
        st.rerun()

# =========================================================
# السؤال المكافئ
# =========================================================

if st.session_state.equivalent_mode:

    equivalent_text = question.get(
        "equivalent",
        question["question"]
    )

    st.markdown(
        f"""
        <div class="question-box">
        🔄 سؤال للتحقق من الفهم<br><br>
        {equivalent_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    equivalent_answer = st.radio(
        "اختاري إجابتكِ:",
        question["options"],
        index=None,
        key=f"equivalent_{question['id']}"
    )

    if st.button(
        "تحققي من فهمي",
        use_container_width=True,
        key=f"equiv_check_{question['id']}"
    ):

        if equivalent_answer is None:
            st.warning("اختاري إجابة أولًا.")

        elif equivalent_answer == question["answer"]:

            update_mastery(concept, True)

            st.success(
                "✅ رائع! الآن أظهرتِ فهمًا أفضل للمفهوم."
            )

            st.session_state.answered = True
            st.session_state.equivalent_mode = False
            st.session_state.feedback = (
                "تم تسجيل تقدمكِ في هذا المفهوم."
            )

            st.rerun()

        else:

            update_mastery(concept, False)

            st.error(
                "ما زال هذا المفهوم يحتاج إلى بعض الدعم. "
                "لا بأس، سيعود ScAI إليه في جلسات المراجعة."
            )

            st.session_state.answered = True
            st.session_state.equivalent_mode = False
            st.session_state.feedback = (
                "سنسجل هذا المفهوم ضمن الموضوعات التي تحتاج إلى مراجعة."
            )

            st.rerun()

# =========================================================
# خريطة الإتقان الجانبية
# =========================================================

with st.expander("🧠 خريطة إتقاني"):

    for concept_id, concept_name in CONCEPTS.items():

        data = st.session_state.mastery[concept_name]

        st.write(
            f"{concept_id} — "
            f"{concept_name}: "
            f"{data['status']}"
        )
