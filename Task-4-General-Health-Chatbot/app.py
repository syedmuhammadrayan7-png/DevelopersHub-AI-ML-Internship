import html
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()

APP_NAME = "MediGuide AI 🩺"
MODEL_NAME = "gemini-2.5-flash"
DISCLAIMER = (
    "Disclaimer: This is general health information only and is not a diagnosis "
    "or medical advice. Please consult a qualified healthcare professional for "
    "personal medical concerns."
)
EMERGENCY_RESPONSE = (
    "This sounds like it could be serious. Please seek urgent medical help "
    "immediately or contact local emergency services. I cannot safely handle "
    "emergency medical situations."
)

EMERGENCY_KEYWORDS = [
    "chest pain",
    "heart attack",
    "cannot breathe",
    "can't breathe",
    "difficulty breathing",
    "severe bleeding",
    "unconscious",
    "stroke",
    "seizure",
    "overdose",
    "poison",
    "suicidal",
    "suicide",
    "emergency",
    "fainting",
    "severe allergic reaction",
    "blood vomiting",
]

EXAMPLE_QUESTIONS = [
    "What causes a sore throat?",
    "What are symptoms of dehydration?",
    "How can I improve sleep naturally?",
    "Is paracetamol safe for children?",
    "What can cause headaches?",
    "How can I manage stress?",
]


def build_health_prompt(user_question):
    """Create a safety-focused prompt for Gemini."""
    return f"""
You are MediGuide AI, a friendly general health information assistant.

Safety rules:
- Give simple and safe general health information.
- Do not diagnose the user.
- Do not prescribe medicine.
- Do not provide exact dosage.
- Do not replace a doctor.
- Recommend consulting a qualified doctor for serious, unusual, or persistent symptoms.
- If the user's message sounds dangerous, recommend urgent medical help.
- Keep the answer clear, short, calm, and beginner-friendly.
- Always include this short disclaimer at the end: "{DISCLAIMER}"

User question:
{user_question}
""".strip()


def is_emergency_question(user_question):
    """Return True when the message contains urgent medical warning terms."""
    normalized_question = user_question.lower()
    return any(keyword in normalized_question for keyword in EMERGENCY_KEYWORDS)


def fallback_response(user_question):
    """Provide safe local answers when Gemini is unavailable."""
    question = user_question.lower()

    if "sore throat" in question or "throat" in question:
        answer = (
            "A sore throat can happen with common colds, allergies, dry air, voice strain, "
            "or throat irritation. Rest, fluids, warm drinks, and avoiding smoke may help. "
            "See a doctor if it is severe, lasts several days, comes with high fever, rash, "
            "trouble swallowing, or breathing difficulty."
        )
    elif "dehydration" in question or "dehydrated" in question:
        answer = (
            "Common signs of dehydration include thirst, dry mouth, dark urine, dizziness, "
            "tiredness, headache, and urinating less than usual. Drinking fluids and resting "
            "can help mild dehydration. Seek medical care for confusion, fainting, very little "
            "urine, or dehydration in babies, older adults, or people with serious illness."
        )
    elif "sleep" in question or "insomnia" in question:
        answer = (
            "To support better sleep naturally, keep a regular sleep schedule, reduce caffeine "
            "late in the day, limit screens before bed, keep the room cool and dark, and build "
            "a calming bedtime routine. If sleep problems continue or affect daily life, a "
            "healthcare professional can help find the cause."
        )
    elif "paracetamol" in question or "acetaminophen" in question:
        answer = (
            "Paracetamol, also called acetaminophen, is commonly used for pain or fever, but "
            "children need the correct product and amount based on age and weight. I cannot "
            "give dosing instructions here. Please follow the medicine label and ask a doctor "
            "or pharmacist, especially for infants or if your child has liver problems."
        )
    elif "headache" in question or "headaches" in question:
        answer = (
            "Headaches can be linked to stress, dehydration, poor sleep, eye strain, skipped "
            "meals, sinus issues, or infections. Resting, drinking water, and reducing screen "
            "strain may help mild headaches. Get medical help for a sudden severe headache, "
            "headache after injury, weakness, confusion, vision changes, fever, or repeated "
            "worsening headaches."
        )
    elif "stress" in question or "anxiety" in question:
        answer = (
            "Stress can often be eased with slow breathing, short walks, regular sleep, time "
            "away from screens, journaling, and talking with someone you trust. If stress feels "
            "overwhelming, lasts a long time, or affects work, study, sleep, or relationships, "
            "consider speaking with a mental health professional."
        )
    else:
        answer = (
            "I can share general health information, but I cannot diagnose symptoms or replace "
            "a clinician. For a safe answer, consider the symptom duration, severity, triggers, "
            "and whether it is getting worse. If symptoms are serious, unusual, or persistent, "
            "please contact a qualified healthcare professional."
        )

    return f"{answer}\n\n{DISCLAIMER}"


def generate_gemini_response(user_question, api_key):
    """Ask Gemini for a safe answer using the official google-genai package."""
    client = genai.Client(api_key=api_key)
    prompt = build_health_prompt(user_question)
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return response.text.strip()


def get_bot_response(user_question):
    """Run emergency filtering first, then Gemini, then local fallback."""
    if is_emergency_question(user_question):
        return EMERGENCY_RESPONSE

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return fallback_response(user_question)

    try:
        return generate_gemini_response(user_question, api_key)
    except Exception:
        return fallback_response(user_question)


def is_gemini_mode():
    """Check only whether an API key is configured without revealing it."""
    return bool(os.getenv("GEMINI_API_KEY"))


def inject_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --ink: #102033;
            --muted: #526173;
            --brand: #116466;
            --brand-2: #15a3a6;
            --accent: #ffb703;
            --surface: rgba(255, 255, 255, 0.78);
            --line: rgba(255, 255, 255, 0.42);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 20%, rgba(255, 183, 3, 0.26), transparent 25%),
                radial-gradient(circle at 88% 8%, rgba(21, 163, 166, 0.26), transparent 30%),
                linear-gradient(135deg, #e8f7f6 0%, #f8fbff 42%, #fff6e2 100%);
            color: var(--ink);
        }

        .block-container {
            max-width: 1120px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(16, 32, 51, 0.95), rgba(17, 100, 102, 0.94));
        }

        [data-testid="stSidebar"] * {
            color: #f8fbff;
        }

        .hero {
            padding: 2rem;
            border: 1px solid var(--line);
            border-radius: 24px;
            background: var(--surface);
            box-shadow: 0 24px 70px rgba(17, 100, 102, 0.16);
            backdrop-filter: blur(18px);
            margin-bottom: 1.25rem;
        }

        .hero h1 {
            font-size: clamp(2.15rem, 5vw, 4.2rem);
            line-height: 1.02;
            margin: 0 0 0.75rem 0;
            letter-spacing: 0;
            color: var(--ink);
        }

        .hero p {
            max-width: 780px;
            color: var(--muted);
            font-size: 1.08rem;
            line-height: 1.65;
            margin: 0;
        }

        .disclaimer {
            padding: 1rem 1.1rem;
            border-radius: 18px;
            background: rgba(255, 247, 219, 0.86);
            border: 1px solid rgba(255, 183, 3, 0.45);
            color: #614700;
            font-weight: 600;
            margin: 1rem 0;
        }

        .chat-shell {
            padding: 1.2rem;
            border-radius: 22px;
            background: rgba(255, 255, 255, 0.62);
            border: 1px solid rgba(255, 255, 255, 0.55);
            box-shadow: 0 18px 50px rgba(16, 32, 51, 0.1);
            backdrop-filter: blur(16px);
            margin-top: 1rem;
        }

        .bubble-row {
            display: flex;
            margin: 0.75rem 0;
        }

        .bubble-row.user {
            justify-content: flex-end;
        }

        .bubble-row.bot {
            justify-content: flex-start;
        }

        .chat-bubble {
            max-width: min(760px, 88%);
            padding: 0.9rem 1rem;
            border-radius: 20px;
            line-height: 1.55;
            font-size: 0.98rem;
            box-shadow: 0 10px 28px rgba(16, 32, 51, 0.09);
            overflow-wrap: anywhere;
            white-space: pre-wrap;
        }

        .bubble-row.user .chat-bubble {
            background: linear-gradient(135deg, #116466, #15a3a6);
            color: white;
            border-bottom-right-radius: 8px;
        }

        .bubble-row.bot .chat-bubble {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(17, 100, 102, 0.13);
            color: var(--ink);
            border-bottom-left-radius: 8px;
        }

        .section-label {
            color: var(--ink);
            font-size: 0.95rem;
            font-weight: 800;
            margin: 0.5rem 0 0.3rem 0;
        }

        div.stButton > button {
            width: 100%;
            border-radius: 999px;
            border: 1px solid rgba(17, 100, 102, 0.18);
            background: rgba(255, 255, 255, 0.74);
            color: var(--ink);
            font-weight: 700;
            min-height: 2.8rem;
            box-shadow: 0 10px 24px rgba(16, 32, 51, 0.08);
            transition: all 160ms ease;
        }

        div.stButton > button:hover {
            border-color: rgba(17, 100, 102, 0.5);
            background: rgba(255, 255, 255, 0.95);
            transform: translateY(-1px);
        }

        [data-testid="stChatInput"] {
            border-radius: 18px;
        }

        .mode-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.55rem 0.75rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.22);
            font-weight: 800;
        }

        .sidebar-note {
            color: rgba(248, 251, 255, 0.82);
            line-height: 1.55;
            font-size: 0.94rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})


def process_question(question):
    add_message("user", question)
    add_message("bot", get_bot_response(question))


def render_chat_history():
    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown(
            """
            <div class="bubble-row bot">
                <div class="chat-bubble">
                    Hi, I am MediGuide AI. Ask me a general health question and I will keep the answer safe, clear, and beginner-friendly.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for message in st.session_state.chat_history:
        role = "user" if message["role"] == "user" else "bot"
        content = html.escape(message["content"])
        st.markdown(
            f"""
            <div class="bubble-row {role}">
                <div class="chat-bubble">{content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.title(APP_NAME)
        st.markdown(
            '<p class="sidebar-note">A safe general health information chatbot built with Streamlit, prompt engineering, Gemini, and local fallback responses.</p>',
            unsafe_allow_html=True,
        )

        mode_text = "Gemini API mode" if is_gemini_mode() else "Local fallback mode"
        st.markdown(f'<div class="mode-pill">{mode_text}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Safety Approach")
        st.markdown(
            """
            - Emergency keywords are filtered before any AI call.
            - Answers avoid diagnosis, prescriptions, and exact dosages.
            - Serious or persistent symptoms are directed to qualified care.
            """
        )

        if st.button("Reset chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


def render_example_buttons():
    st.markdown('<p class="section-label">Try an example question</p>', unsafe_allow_html=True)
    cols = st.columns(2)
    for index, question in enumerate(EXAMPLE_QUESTIONS):
        with cols[index % 2]:
            if st.button(question, key=f"example_{index}"):
                process_question(question)
                st.rerun()


def main():
    st.set_page_config(page_title=APP_NAME, page_icon="🩺", layout="wide")
    inject_styles()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    render_sidebar()

    st.markdown(
        f"""
        <section class="hero">
            <h1>{APP_NAME}</h1>
            <p>
                A calm, safety-first chatbot for general health questions. It can explain common symptoms,
                healthy habits, and when to seek professional care without diagnosing or replacing a doctor.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="disclaimer">{DISCLAIMER}</div>', unsafe_allow_html=True)
    render_example_buttons()
    render_chat_history()

    user_question = st.chat_input("Ask a general health question...")
    if user_question:
        process_question(user_question)
        st.rerun()


if __name__ == "__main__":
    main()
