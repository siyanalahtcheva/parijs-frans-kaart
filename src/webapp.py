import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


LOCATIONS = [
    {
        "id": "eiffel",
        "name": "Tour Eiffel",
        "x": 14,
        "y": 70,
        "question": "Hoe zeg je in het Frans: 'Ik wil de Eiffeltoren bezoeken'?",
        "options": [
            "Je veux visiter la tour Eiffel",
            "Je veux voir la tour Eiffel",
            "Je vais aller à la tour Eiffel",
            "Je visite la tour Eiffel hier",
        ],
        "correctIndex": 0,
        "explanation": "‘Visiter’ gebruik je voor het bezoeken van plaatsen.",
    },
    {
        "id": "louvre",
        "name": "Musée du Louvre",
        "x": 45,
        "y": 61,
        "question": "Hoe vraag je: 'Waar is het Louvre?'",
        "options": [
            "Où est le Louvre ?",
            "Où sont le Louvre ?",
            "Quand est le Louvre ?",
            "Qui est le Louvre ?",
        ],
        "correctIndex": 0,
        "explanation": "‘Où est … ?’ gebruik je voor plaatsbepaling.",
    },
    {
        "id": "notredame",
        "name": "Notre-Dame",
        "x": 58,
        "y": 73,
        "question": "Hoe zeg je: 'Ik ga naar de Notre-Dame'?",
        "options": [
            "Je vais à Notre-Dame",
            "Je vais au Notre-Dame",
            "Je vais de Notre-Dame",
            "Je vais chez Notre-Dame",
        ],
        "correctIndex": 0,
        "explanation": "Bij monumenten gebruik je meestal gewoon ‘à’.",
    },
    {
        "id": "sacrecoeur",
        "name": "Sacré-Cœur",
        "x": 55,
        "y": 24,
        "question": "Hoe zeg je: 'Ik wil Montmartre bezoeken'?",
        "options": [
            "Je veux visiter Montmartre",
            "Je veux visiter le Montmartre",
            "Je veux visiter à Montmartre",
            "Je veux visité Montmartre",
        ],
        "correctIndex": 0,
        "explanation": "‘Visiter’ krijgt geen voorzetsel.",
    },
]


st.set_page_config(page_title="Oefen Frans in Parijs", layout="wide")

if "active_id" not in st.session_state:
    st.session_state.active_id = None

if "answers" not in st.session_state:
    st.session_state.answers = {}


def get_active_location():
    for loc in LOCATIONS:
        if loc["id"] == st.session_state.active_id:
            return loc
    return None


def load_image(path: Path):
    raw = path.read_bytes()
    encoded = base64.b64encode(raw).decode()
    return f"data:image/jpeg;base64,{encoded}"


loc_param = st.query_params.get("loc")
if loc_param:
    st.session_state.active_id = loc_param


st.title("🇫🇷 Oefen Frans in Parijs")
st.caption("Klik op een plek op de kaart of kies een locatie.")

with st.sidebar:
    st.header("Locaties")
    for loc in LOCATIONS:
        if st.button(loc["name"]):
            st.session_state.active_id = loc["id"]
            st.query_params["loc"] = loc["id"]
            st.rerun()


left, right = st.columns([1.3, 1])


with left:
    img_path = Path(__file__).parent / "paris city map.jpg"
    img_data = load_image(img_path)

    css = """
    <style>
      .mapwrap { position: relative; max-width: 1000px; margin: auto; }
      .mapwrap img { width: 100%; border-radius: 12px; }

      .hotspot {
        position: absolute;
        transform: translate(-50%, -50%);
        padding: 7px 10px;
        background: rgba(0,0,0,0.7);
        color: white;
        border-radius: 999px;
        font-size: 12px;
        text-decoration: none;
        cursor: pointer;
        transition: transform 0.15s;
      }

      .hotspot:hover {
        transform: translate(-50%, -50%) scale(1.08);
        background: rgba(30,90,200,0.9);
      }

      .hotspot.active {
        background: rgba(0,150,90,0.9);
      }
    </style>
    """

    hotspots = ""
    for loc in LOCATIONS:
        active = "active" if loc["id"] == st.session_state.active_id else ""
        hotspots += f"""
        <a class="hotspot {active}"
           style="left:{loc['x']}%; top:{loc['y']}%;"
           onclick="window.parent.location.replace('?loc={loc['id']}'); return false;">
           {loc['name']}
        </a>
        """

    html = f"""
    {css}
    <div class="mapwrap">
        <img src="{img_data}">
        {hotspots}
    </div>
    """

    components.html(html, height=580, scrolling=False)


with right:
    loc = get_active_location()

    if not loc:
        st.info("Kies een locatie op de kaart.")
    else:
        st.subheader(loc["name"])
        st.write(loc["question"])

        choice = st.radio("Antwoorden", loc["options"], index=None)

        if st.button("Controleer"):
            if choice is None:
                st.warning("Kies een antwoord.")
            else:
                correct = loc["options"][loc["correctIndex"]]
                if choice == correct:
                    st.success("✔ Goed!")
                else:
                    st.error("✘ Niet goed.")
                st.write("Uitleg:", loc["explanation"])
