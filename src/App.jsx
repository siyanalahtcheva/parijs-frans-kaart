import { useState } from "react";

const LOCATIONS = [
  {
    id: "eiffel",
    name: "Tour Eiffel",
    x: "55%",
    y: "60%",
    question: "Hoe zeg je in het Frans: 'Ik wil de Eiffeltoren bezoeken'?",
    options: [
      "Je veux visiter la tour Eiffel",
      "Je veux voir la tour Eiffel",
      "Je vais aller à la tour Eiffel",
      "Je visite la tour Eiffel hier"
    ],
    correctIndex: 0,
    explanation:
      "De meest neutrale manier om 'ik wil bezoeken' te zeggen is 'je veux visiter'. 'Je veux voir' betekent 'ik wil zien', wat ook kan, maar de oefenzin focust op 'bezoeken'."
  },
  {
    id: "louvre",
    name: "Le Louvre",
    x: "45%",
    y: "55%",
    question:
      "Welke vraag kun je stellen om te vragen waar de ingang van het Louvre is?",
    options: [
      "Où est l'entrée du Louvre ?",
      "Où est Louvre ?",
      "Où sont les Louvre ?",
      "Où est la porte Louvre ?"
    ],
    correctIndex: 0,
    explanation:
      "Je vraagt naar de ingang: 'l'entrée du Louvre'. Let op het lidwoord en het gebruik van 'du' (de + le)."
  },
  {
    id: "notre-dame",
    name: "Notre-Dame",
    x: "52%",
    y: "52%",
    question:
      "Hoe zeg je in het Frans: 'We nemen de metro naar Notre-Dame'?",
    options: [
      "On prend le métro pour Notre-Dame",
      "On va en métro Notre-Dame",
      "Nous prenons la métro à Notre-Dame",
      "On prend métro vers Notre-Dame"
    ],
    correctIndex: 0,
    explanation:
      "'Prendre le métro' = de metro nemen. In spreektaal gebruik je vaak 'on' in plaats van 'nous'."
  }
];

function App() {
  const [activeId, setActiveId] = useState(null);
  const [answers, setAnswers] = useState({});

  const activeLocation =
    LOCATIONS.find((loc) => loc.id === activeId) || null;

  const handleMarkerClick = (id) => {
    setActiveId(id);
  };

  const handleAnswer = (index) => {
    if (!activeLocation) return;
    setAnswers((prev) => ({
      ...prev,
      [activeLocation.id]: {
        selectedIndex: index,
        isCorrect: index === activeLocation.correctIndex
      }
    }));
  };

  return (
    <div className="app">
      {/* Linker panel: kaart */}
      <div className="panel">
        <h1>Oefen Frans in Parijs</h1>
        <p className="subtitle">
          Klik op een plek in Parijs en beantwoord de bijbehorende vraag.
        </p>

        <div className="map-wrapper">
          <div className="map-image">
            {LOCATIONS.map((loc) => {
              const state = answers[loc.id];
              return (
                <button
                  key={loc.id}
                  type="button"
                  className="map-marker"
                  style={{ left: loc.x, top: loc.y }}
                  onClick={() => handleMarkerClick(loc.id)}
                >
                  <div className="marker-dot" />
                  <div className={`marker-label ${state?.isCorrect === true ? 'marker-label-correct' : state?.isCorrect === false ? 'marker-label-wrong' : ''}`}>
                    {loc.name}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Rechter panel: vragen */}
      <div className="panel">
        {!activeLocation ? (
          <div>
            <p className="question-placeholder">
              Kies eerst een locatie op de kaart om een vraag te krijgen.
            </p>
            <ul className="small-list">
              <li>Oefen zinnen die je écht in Parijs zou gebruiken.</li>
              <li>Lees na je antwoord de uitleg om te leren waarom.</li>
              <li>
                Je kunt later zelf nieuwe plekken en vragen toevoegen in
                de code.
              </li>
            </ul>
          </div>
        ) : (
          <div>
            <h2 className="question-title">{activeLocation.name}</h2>
            <p className="question-text">{activeLocation.question}</p>

            <div className="options">
              {activeLocation.options.map((opt, index) => {
                const state = answers[activeLocation.id];
                const isSelected = state?.selectedIndex === index;
                const isCorrect =
                  index === activeLocation.correctIndex;

                let extraClass = "";
                if (state && state.selectedIndex !== null) {
                  if (isCorrect) extraClass = "option-correct";
                  if (isSelected && !isCorrect)
                    extraClass = "option-wrong";
                }

                return (
                  <button
                    key={index}
                    className={`option-button ${extraClass}`}
                    type="button"
                    onClick={() => handleAnswer(index)}
                  >
                    <strong>{String.fromCharCode(65 + index)}. </strong>
                    {opt}
                  </button>
                );
              })}
            </div>

            {answers[activeLocation.id]?.isCorrect !== undefined && (
              <div className="feedback">
                {answers[activeLocation.id]?.isCorrect ? (
                  <div className="feedback-good">✔ Goed gedaan!</div>
                ) : (
                  <div className="feedback-bad">
                    ✖ Niet helemaal juist.
                  </div>
                )}
                <div className="explanation">
                  {activeLocation.explanation}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
