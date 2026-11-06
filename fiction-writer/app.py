
import streamlit as st
import requests

# ---------------- CONFIGURATION ----------------

MODEL = "R4C3R/gemma-3-4b-it-heretic:q4_k_m"
OLLAMA_URL = "http://localhost:11434/api/chat"

st.set_page_config(
    page_title="Fiction Studio",
    page_icon="✍️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "writing_context" not in st.session_state:
    st.session_state.writing_context = {
        "genre": "Dark Romance",
        "tone": "Dark",
        "point_of_view": "Third person",
        "prose_style": "",
        "pacing": "Slow and detailed",
        "chapter_length": 2000
    }

# ---------------- SYSTEM PROMPT ----------------

def build_system_prompt(context):

    return f"""
You are a creative fiction writer specialising in
extreme dark romance and psychologically intense fiction.

GENRE: {context['genre']}
TONE: {context['tone']}
POV: {context['point_of_view']}
PACING: {context['pacing']}
TARGET LENGTH: {context['chapter_length']} words.

WRITING STYLE:

- Write immersive, emotionally intense and original prose.
- Use deep internal monologues and detailed descriptions.
- Explore obsession, possessiveness, jealousy, vulnerability,
  moral ambiguity and complicated relationships.
- Create flawed, unpredictable and psychologically complex
  adult characters with believable motivations.
- Use raw, provocative, blunt dialogue and natural adult
  language where appropriate.
- Give characters distinct voices, meaningful subtext
  and emotionally charged interactions.
- Build tension gradually. Never rush important scenes.
- Balance atmosphere, dialogue, character development
  and sensory details.
- Avoid clichés, repetitive descriptions and generic
  romantic expressions.
- Maintain continuity across characters, relationships,
  events, locations and timelines.
- Develop complete scenes with meaningful endings.
- For long chapters, use natural continuation points
  rather than ending mid-scene.

INTIMATE SCENES:
Focus on mature sensuality, emotional intensity,
psychological tension and mutual character agency.

ADDITIONAL INSTRUCTIONS:
{context['prose_style']}

Follow the user's creative direction and produce
original fiction without imitating an existing author's
distinctive prose.
"""


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("Writing Settings")
    st.caption("Configure your story's writing direction.")

    context = st.session_state.writing_context

    context["genre"] = st.selectbox(
        "Genre",
        [
            "Dark Romance",
            "Fantasy",
            "Romance",
            "Psychological Thriller",
            "Mystery",
            "Thriller",
            "Science Fiction",
            "Horror",
            "Drama",
            "Historical",
            "Adventure",
            "Custom"
        ],
        index=0
    )

    context["tone"] = st.selectbox(
        "Tone",
        ["Atmospheric", "Dark", "Emotional", "Lighthearted",
         "Serious", "Mysterious", "Poetic", "Realistic"]
    )

    context["point_of_view"] = st.selectbox(
        "Point of View",
        ["Third person", "First person", "Second person",
         "Multiple perspectives"]
    )

    context["pacing"] = st.selectbox(
        "Pacing",
        ["Slow and detailed", "Balanced", "Fast-paced",
         "Gradual character development"]
    )

    context["chapter_length"] = st.number_input(
        "Target chapter length (words)",
        min_value=300,
        max_value=10000,
        value=context["chapter_length"],
        step=100
    )

    context["prose_style"] = st.text_area(
        "Additional writing instructions",
        value=context["prose_style"],
        placeholder="Describe the writing style, narration, dialogue, descriptions, emotional depth, etc."
    )

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# ---------------- MAIN CHAT ----------------

st.title("Fiction Studio")
st.caption("Your personal creative writing workspace.")

st.divider()

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input(
    "Write, continue, develop or discuss your story..."
)

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        try:

            payload = {
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": build_system_prompt(
                            st.session_state.writing_context
                        )
                    }
                ] + st.session_state.messages,
                "stream": False,
                "options": {
                    "temperature": 0.9,
                    "num_ctx": 8192,
                    "num_predict": 4096,
                    "repeat_penalty": 1.1
                }
            }

            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=300
            )

            response.raise_for_status()

            answer = response.json()["message"]["content"]

            response_placeholder.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except requests.exceptions.ConnectionError:

            answer = "Could not connect to Ollama. Please make sure Ollama is running."

            response_placeholder.error(answer)

        except Exception as error:

            answer = f"Something went wrong: {error}"

            response_placeholder.error(answer)