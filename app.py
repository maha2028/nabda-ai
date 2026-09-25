import streamlit as st
from questions import QUESTIONS, CONCEPTS
import random

# =========================================================
# إعداد ScAI
# =========================================================
st.set_page_config(
    page_title="ScAI",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# تنسيق عربي
# =========================================================
st.markdown("""
<style>
.stApp {
    direction: rtl;
    text-align: right;
    background: linear-gradient(180deg,#fffafd 0%,#f7f9ff 100%);
}

h1,h2,h3,p,div,label {
    direction: rtl;
    text-align: right;
}

.main-title {
    text-align:center;
    font-size:52px;
    font-weight:800;
    color:#d94b70;
    margin-bottom:0;
}

.subtitle {
    text-align:center;
    color:#596275;
    font-size:19px;
    margin-bottom:28px;
}

.question-box {
    padding:24px;
    border:1px solid #eadce3;
    border-radius:18px;
    background:white;
    margin:15px 0;
    font-size:22px;
    font-weight:700;
}

.status-box {
    padding:12px;
    border-radius:12px;
    background:#ffffff;
    border:1px solid #ececec;
    margin-bottom:8px;
}

.small-note {
    color:#777;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# الحالة
# =========================================================
defaults = {
    "logged_in": False,
    "started": False,
    "phase": "diagnostic",
    "current_q": None,
    "attempt": 0,
    "hint_level": 0,
    "show_lesson": False,
    "equivalent_mode": False,
    "feedback": "",
    "answered": False,
    "score": 0,
    "total_answered": 0,
    "mastery": {},
    "seen": [],
    "diagnostic_done": [],
    "target_concept": None,
    "completed": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# إنشاء/إصلاح سجل كل مفهوم
for cid, cname in CONCEPTS.items():
    old = st.session_state.mastery.get(cid, {})

    if not isinstance(old, dict):
        old = {}

    st.session_state.mastery[cid] = {
        "name": cname,
        "correct": old.get("correct", 0),
        "wrong": old.get("wrong", 0),
        "status": old.get("status", "⚪ لم يُقَيَّم")
    }
# =========================================================
# وظائف
# =========================================================
def update_mastery(cid, correct):
    data = st.session_state.mastery[cid]

    if correct:
        data["correct"] += 1
    else:
        data["wrong"] += 1

    c = data["correct"]
    w = data["wrong"]

    if c >= 2 and c > w:
        data["status"] = "🟢 متقن"
    elif c >= 1:
        data["status"] = "🟡 في طور الإتقان"
    elif w >= 1:
        data["status"] = "🔴 يحتاج دعمًا"
    else:
        data["status"] = "⚪ لم يُقَيَّم"


def reset_question():
    st.session_state.attempt = 0
    st.session_state.hint_level = 0
    st.session_state.show_lesson = False
    st.session_state.equivalent_mode = False
    st.session_state.feedback = ""
    st.session_state.answered = False


def questions_for_concept(cid):
    return [q for q in QUESTIONS if q["concept_id"] == cid]


def choose_unseen_for_concept(cid):
    pool = questions_for_concept(cid)
    unseen = [q for q in pool if q["id"] not in st.session_state.seen]

    if unseen:
        return random.choice(unseen)

    if pool:
        return random.choice(pool)

    return None


def choose_diagnostic_question():
    # سؤال واحد مبدئي من كل مفهوم لم يُشخّص بعد
    remaining = [
        cid for cid in CONCEPTS
        if cid not in st.session_state.diagnostic_done
    ]

    if not remaining:
        return None

    cid = remaining[0]
    return choose_unseen_for_concept(cid)


def weakest_concept():
    candidates = []

    for cid, data in st.session_state.mastery.items():
        if data["status"] == "🔴 يحتاج دعمًا":
            candidates.append((0, data["correct"] - data["wrong"], cid))
        elif data["status"] == "🟡 في طور الإتقان":
            candidates.append((1, data["correct"] - data["wrong"], cid))
        elif data["status"] == "⚪ لم يُقَيَّم":
            candidates.append((2, 0, cid))

    if not candidates:
        return None

    candidates.sort()
    return candidates[0][2]


def select_next_question():
    # المرحلة الأولى: تشخيص جميع المفاهيم
    if st.session_state.phase == "diagnostic":
        q = choose_diagnostic_question()

        if q:
            return q

        st.session_state.phase = "adaptive"

    # المرحلة الثانية: التركيز على الأضعف
    cid = weakest_concept()

    if cid:
        st.session_state.target_concept = cid
        return choose_unseen_for_concept(cid)

    st.session_state.completed = True
    return None


def move_next():
    reset_question()
    st.session_state.current_q = select_next_question()


def restart():
    for key in list(defaults.keys()):
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


# =========================================================
# العنوان
# =========================================================
st.markdown('<div class="main-title">🔬 ScAI</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">مساعدكِ الذكي التكيفي لتعلُّم العلوم</div>',
    unsafe_allow_html=True
)

# =========================================================
# تسجيل الدخول
# =========================================================
if not st.session_state.logged_in:

    st.info(
        "مرحبًا بكِ في ScAI. هذه البيئة مخصصة للمشاركات المصرح لهن في الدراسة."
    )

    access_code = st.text_input(
        "أدخلي رمز الدخول البحثي",
        type="password",
        placeholder="رمز الدخول"
    )

    st.caption("لا تكتبي اسمكِ أو أي بيانات شخصية.")

    if st.button("دخول إلى ScAI", use_container_width=True):
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

    st.markdown("""
### كيف يعمل ScAI؟

سيبدأ ScAI بتشخيص فهمكِ لمفاهيم الفصل، ثم يحدد المفاهيم التي تحتاج إلى مراجعة.

إذا واجهتِ صعوبة، سيقدم لكِ تلميحات تدريجية ثم مراجعة قصيرة، وبعدها سؤالًا للتحقق من الفهم.
""")

    if st.button("🚀 ابدئي جلسة التعلّم", use_container_width=True):
        st.session_state.started = True
        st.session_state.current_q = select_next_question()
        st.rerun()

    st.stop()

# =========================================================
# خريطة الإتقان
# =========================================================
with st.expander("🧠 خريطة إتقاني"):
    for cid, data in st.session_state.mastery.items():
        st.markdown(
            f"**{data['name']}** — {data['status']}"
        )

# =========================================================
# النهاية
# =========================================================
if st.session_state.completed:
    st.success("🎉 أحسنتِ! اكتملت جلسة ScAI.")

    st.write(
        f"عدد الإجابات الصحيحة: **{st.session_state.score}**"
    )

    st.write(
        f"عدد الاستجابات المسجلة: **{st.session_state.total_answered}**"
    )

    st.subheader("🧠 خريطة الإتقان النهائية")

    for cid, data in st.session_state.mastery.items():
        st.markdown(
            f"**{data['name']}** — {data['status']}"
        )

    if st.button("بدء جلسة جديدة"):
        restart()

    st.stop()

# =========================================================
# السؤال الحالي
# =========================================================
if st.session_state.current_q is None:
    st.session_state.current_q = select_next_question()

question = st.session_state.current_q

if question is None:
    st.session_state.completed = True
    st.rerun()

cid = question["concept_id"]
concept_name = CONCEPTS[cid]

# =========================================================
# معلومات التقدم
# =========================================================
if st.session_state.phase == "diagnostic":
    st.caption("🔎 المرحلة الحالية: التشخيص الذكي")
else:
    st.caption("🎯 المرحلة الحالية: التعلّم التكيفي")

st.caption(
    f"المفهوم الحالي: {concept_name} | "
    f"{st.session_state.mastery[cid]['status']}"
)

# =========================================================
# السؤال
# =========================================================
st.markdown(
    f"""
    <div class="question-box">
    🌷 {question["question"]}
    </div>
    """,
    unsafe_allow_html=True
)

# صورة مستقبلية إن وجدت
if question.get("image"):
    try:
        st.image(question["image"], use_container_width=True)
    except Exception:
        pass

# =========================================================
# الوضع العادي
# =========================================================






   if not st.session_state.equivalent_mode:

    # تحديد نوع السؤال
    question_type = question.get("type", "mcq")

    # عرض صورة السؤال إن وجدت
    if question.get("image"):
        try:
            st.image(
                question["image"],
                use_container_width=True
            )
        except Exception:
            pass
    # -----------------------------------------
    # التلميح الأول
    # -----------------------------------------
    if st.session_state.hint_level >= 1:
        st.info(
            "💡 **التلميح الأول:**\n\n"
            + question["hint1"]
        )

    # -----------------------------------------
    # التلميح الثاني
    # -----------------------------------------
    if st.session_state.hint_level >= 2:
        st.info(
            "💡 **التلميح الثاني:**\n\n"
            + question["hint2"]
        )

    # -----------------------------------------
    # مراجعة مصغرة
    # -----------------------------------------
    if st.session_state.show_lesson:

        st.warning(
            "سنراجع الفكرة سريعًا ثم نجرب سؤالًا مكافئًا."
        )

        st.markdown("### 📘 مراجعة سريعة")
        st.info(question["micro_lesson"])

        if st.button(
            "فهمت، اختبريني بسؤال آخر",
            use_container_width=True
        ):
            st.session_state.equivalent_mode = True
            st.rerun()

# =========================================================
# بعد الإجابة الصحيحة
# =========================================================
if st.session_state.feedback == "correct":

    st.success("✅ أحسنتِ! إجابتك صحيحة.")

    if st.button(
        "السؤال التالي ➜",
        use_container_width=True
    ):
        move_next()
        st.rerun()

# =========================================================
# السؤال المكافئ بعد المراجعة
# =========================================================
if st.session_state.equivalent_mode:

    st.markdown("### 🧪 تحققي من فهمك")

    st.markdown(
        f"""
        <div class="question-box">
        {question["equivalent"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    equivalent_answer = st.radio(
        "اختاري الإجابة:",
        question["options"],
        index=None,
        key=f"equiv_{question['id']}"
    )

    if st.button(
        "تحققي من السؤال المكافئ",
        use_container_width=True
    ):

        if equivalent_answer is None:
            st.warning("اختاري إجابة أولًا.")

        elif equivalent_answer == question["answer"]:

            update_mastery(cid, True)

            if question["id"] not in st.session_state.seen:
                st.session_state.seen.append(question["id"])

            if (
                st.session_state.phase == "diagnostic"
                and cid not in st.session_state.diagnostic_done
            ):
                st.session_state.diagnostic_done.append(cid)

            st.success(
                "🌟 ممتاز! يبدو أن الفكرة أصبحت أوضح."
            )

            st.session_state.answered = True
            st.session_state.feedback = "equivalent_correct"
            st.rerun()

        else:
            update_mastery(cid, False)
            st.error(
                "ما زالت الفكرة تحتاج إلى دعم. سيعيد ScAI هذا المفهوم لاحقًا."
            )

            if (
                st.session_state.phase == "diagnostic"
                and cid not in st.session_state.diagnostic_done
            ):
                st.session_state.diagnostic_done.append(cid)

            st.session_state.feedback = "equivalent_wrong"
            st.rerun()

# =========================================================
# الانتقال بعد السؤال المكافئ
# =========================================================
if st.session_state.feedback in [
    "equivalent_correct",
    "equivalent_wrong"
]:

    if st.button(
        "متابعة التعلّم ➜",
        use_container_width=True,
        key="continue_after_equiv"
    ):
        move_next()
        st.rerun()
