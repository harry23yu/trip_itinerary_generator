import { useState } from "react";
import QuestionRenderer from "./questions/QuestionRenderer";
import { optionARequired, optionBRequired } from "./questions/required_questions";
import { optionAOptional, optionBOptional } from "./questions/optional_questions";

function App() {
  const [selectedOption, setSelectedOption] = useState(null);
  const [formData, setFormData] = useState({});

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
    setFormData({}); // reset form when switching
  };

  const handleChange = (id, value) => {
    setFormData((prev) => ({
      ...prev,
      [id]: value,
    }));
  };

  const getQuestions = () => {
    if (!selectedOption) return [];

    if (selectedOption === "A") {
      return [...optionARequired, ...optionAOptional];
    }

    if (selectedOption === "B") {
      return [...optionBRequired, ...optionBOptional];
    }

    return [];
  };

  const questions = getQuestions();

  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <h1>AI Trip Itinerary Generator</h1>

      {!selectedOption && (
        <div>
          <h2>Select an Option</h2>
          <button onClick={() => handleOptionSelect("A")}>
            Option A – I don't know where to go
          </button>
          <br />
          <br />
          <button onClick={() => handleOptionSelect("B")}>
            Option B – I already know where I'm going
          </button>
        </div>
      )}

      {selectedOption && (
        <div>
          <h2>
            {selectedOption === "A"
              ? "Option A – Discovery Mode"
              : "Option B – Structured Mode"}
          </h2>

          {questions.map((question) => {
            if (question.showIf && !question.showIf(formData)) {
              return null;
            }

            return (
              <QuestionRenderer
                key={question.id}
                question={question}
                value={formData[question.id]}
                handleChange={handleChange}
              />
            );
          })}
        </div>
      )}
    </div>
  );
}

export default App;