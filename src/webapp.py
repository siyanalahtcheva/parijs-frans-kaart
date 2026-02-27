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
        "explanation": (
            "De meest neutrale manier om 'ik wil bezoeken' is 'Je veux visiter ...'. "
            "'Je veux voir ...' betekent eerder 'ik wil zien'."
        ),
    },
    {
        "id": "louvre",
        "name": "Musée du Louvre",
        "x": 45,
        "y": 61,
        "question": "Hoe vraag je in het Frans: 'Waar is het Louvre?'",
        "options": [
            "Où est le Louvre ?",
            "Où sont le Louvre ?",
            "Quand est le Louvre ?",
            "Qui est le Louvre ?",
        ],
        "correctIndex": 0,
        "explanation": "Voor 'waar is' gebruik je 'Où est ... ?' (enkelvoud).",
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
        "explanation": "Bij namen van plaatsen/monumenten gebruik je vaak gewoon 'à'.",
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
        "explanation": "'Visiter' + plaats zonder extra voorzetsel: 'visiter Montmartre'.",
    },
    {
        "id": "arc",
        "name": "Arc de Triomphe",
        "x": 12,
        "y": 33,
        "question": "Hoe zeg je: 'Is de Arc de Triomphe dichtbij?'",
        "options": [
            "Est-ce que l’Arc de Triomphe est proche ?",
            "L’Arc de Triomphe est proche est-ce ?",
            "Est-ce que l’Arc de Triomphe proche ?",
            "Arc de Triomphe est proche ?",
        ],
        "correctIndex": 0,
        "explanation": "Een correcte vraagvorm is: 'Est-ce que ... ?' + volledige zin.",
    },
    {
        "id": "orsay",
        "name": "Musée d’Orsay",
        "x": 39,
        "y": 67,
        "question": "Hoe vraag je: 'Hoeveel kost een ticket?'",
        "options": [
            "Combien coûte un billet ?",
            "Combien coûte une billet ?",
            "Combien coûtent un billet ?",
            "Quel coûte un billet ?",
        ],
        "correctIndex": 0,
        "explanation": "'Billet' is mannelijk: 'un billet'. 'Combien coûte ... ?' is correct.",
    },
]
st.set_page_config(page_title="Oefen Frans in Parijs", layout="wide")

if "active_id" not in st.session_state:
    st.session_state.active_id = None

if "answers" not in st.session_state:
    # answers[loc_id] = {"selectedIndex": int, "isCorrect": bool}
    st.session_state.answers = {}

def get_active_location():
    if not st.session_state.active_id:
        return None
    for loc in LOCATIONS:
        if loc["id"] == st.session_state.active_id:
            return loc
    return None


def load_map_as_data_uri(image_path: Path) -> str:
    if not image_path.exists():
        return ""
    raw = image_path.read_bytes()
    b64 = base64.b64encode(raw).decode("utf-8")
    return f"data:image/webp;base64,{b64}"

loc_param = st.query_params.get("loc")
if loc_param:
    st.session_state.active_id = str(loc_param)

st.title("🇫🇷 Oefen Frans in Parijs")
st.caption("Klik op een plek op de kaart (hotspots) of kies een locatie in de sidebar.")

with st.sidebar:
    st.header("Locaties")
    for loc in LOCATIONS:
        state = st.session_state.answers.get(loc["id"])
        label = loc["name"]
        if state:
            label += " ✅" if state["isCorrect"] else " ❌"

        if st.button(label, key=f"side_{loc['id']}"):
            st.session_state.active_id = loc["id"]
            st.query_params["loc"] = loc["id"]
            st.rerun()

    st.markdown("---")
    if st.button("Reset antwoorden"):
        st.session_state.answers = {}
        st.session_state.active_id = None
        st.query_params.clear()
        st.rerun()


left, right = st.columns([1.25, 1])

with left:
    img_path = Path(__file__).parent / "Paris.webp"
    data_uri = load_map_as_data_uri(img_path)

    if not data_uri:
        st.error("Ik kan Paris.webp niet vinden. Zet 'Paris.webp' in dezelfde map als webapp.py (de src-map).")
    else:
        active_id = st.session_state.active_id or ""

        css = """
        <style>
          .mapwrap{
            position: relative;
            width: 100%;
            max-width: 1000px;
            margin: 0 auto;
            border-radius: 14px;
            overflow: hidden;
          }
          .mapwrap img{
            width: 100%;
            height: auto;
            display:block;
          }

          .hotspot{
            position:absolute;
            transform: translate(-50%, -50%);
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 11px;
            border-radius: 999px;
            text-decoration: none;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            font-size: 12px;
            line-height: 1;
            background: rgba(0,0,0,0.70);
            color: white;
            border: 1px solid rgba(255,255,255,0.22);
            box-shadow: 0 10px 26px rgba(0,0,0,0.35);
            backdrop-filter: blur(6px);
            transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease, background 120ms ease;
            user-select: none;
            -webkit-user-select: none;
            cursor: pointer;
          }

          /* 🔵 hover highlight */
          .hotspot:hover{
            transform: translate(-50%, -50%) scale(1.06);
            box-shadow: 0 14px 34px rgba(0,0,0,0.45);
            border-color: rgba(255,255,255,0.45);
            background: rgba(10, 70, 190, 0.85);
          }

          .dot{
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: rgba(255,255,255,0.95);
            box-shadow: 0 0 0 3px rgba(255,255,255,0.20);
            flex: 0 0 auto;
          }

          /* 📍 active marker */
          .hotspot.active{
            background: rgba(0, 150, 90, 0.88);
            border-color: rgba(255,255,255,0.65);
            box-shadow: 0 16px 40px rgba(0,0,0,0.50);
            transform: translate(-50%, -50%) scale(1.08);
          }
          .hotspot.active .dot{
            background: rgba(255,255,255,0.98);
            box-shadow: 0 0 0 4px rgba(255,255,255,0.28);
          }
          .hotspot.active::after{
            content: "";
            position: absolute;
            inset: -10px;
            border-radius: 999px;
            border: 2px solid rgba(0, 255, 170, 0.55);
            animation: pulse 1.2s ease-in-out infinite;
          }
          @keyframes pulse{
            0%   { transform: scale(0.96); opacity: 0.10; }
            50%  { transform: scale(1.05); opacity: 0.55; }
            100% { transform: scale(0.96); opacity: 0.10; }
          }

          .legend{
            position:absolute;
            right: 12px;
            bottom: 12px;
            background: rgba(0,0,0,0.55);
            color: white;
            padding: 8px 10px;
            border-radius: 12px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            font-size: 12px;
            border: 1px solid rgba(255,255,255,0.18);
            backdrop-filter: blur(6px);
          }
          .legend b{ font-weight: 650; }
        </style>
        """

        hotspots_html = ""
        for loc in LOCATIONS:
            cls = "hotspot"
            if loc["id"] == active_id:
                cls += " active"

            hotspots_html += f"""
              <a class="{cls}" href="#"
                 onclick="window.parent.location.replace('?loc={loc['id']}'); return false;"
                 style="left:{loc['x']}%; top:{loc['y']}%;"
                 title="Open vraag: {loc['name']}">
                 <span class="dot"></span>
                 <span>{loc['name']}</span>
              </a>
            """

        html = f"""
        {css}
        <div class="mapwrap">
          <img src="{data_uri}" alt="Kaart van Parijs" />
          {hotspots_html}
          <div class="legend"><b>Tip:</b> hover = highlight • groen = actief</div>
        </div>
        """

        components.html(html, height=590, scrolling=False)

    st.markdown(
        "<div style='opacity:0.8; font-size: 13px;'>Klik op een label op de kaart om een vraag te openen.</div>",
        unsafe_allow_html=True,
    )

with right:
    active = get_active_location()

    if not active:
        st.info("Kies eerst een locatie op de kaart.")
    else:
        st.subheader(active["name"])
        st.markdown(f"**Vraag:** {active['question']}")

        prev = st.session_state.answers.get(active["id"])
        default_index = prev["selectedIndex"] if prev else None

        placeholder = "— Kies een antwoord —"
        radio_options = [placeholder] + active["options"]

        if default_index is None:
            selected = st.radio("Antwoorden", radio_options, index=0, key=f"radio_{active['id']}")
            selected_index = None if selected == placeholder else radio_options.index(selected) - 1
        else:
            selected = st.radio("Antwoorden", radio_options, index=default_index + 1, key=f"radio_{active['id']}")
            selected_index = radio_options.index(selected) - 1

        col_a, col_b = st.columns([1, 1])

        with col_a:
            if st.button("Controleer", type="primary"):
                if selected_index is None:
                    st.warning("Kies eerst een antwoord.")
                else:
                    is_correct = selected_index == active["correctIndex"]
                    st.session_state.answers[active["id"]] = {
                        "selectedIndex": selected_index,
                        "isCorrect": is_correct,
                    }
                    st.rerun()

        with col_b:
            if st.button("Volgende locatie"):
                ids = [l["id"] for l in LOCATIONS]
                current_i = ids.index(active["id"])
                next_id = ids[(current_i + 1) % len(ids)]
                st.session_state.active_id = next_id
                st.query_params["loc"] = next_id
                st.rerun()

        answer = st.session_state.answers.get(active["id"])
        if answer:
            if answer["isCorrect"]:
                st.success("✔ Goed gedaan!")
            else:
                st.error("✖ Niet helemaal juist.")

            st.markdown("**Uitleg:**")
            st.write(active["explanation"])
