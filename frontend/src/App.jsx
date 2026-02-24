import { useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import QuestionRenderer from "./questions/QuestionRenderer";
import { optionARequired, optionBRequired } from "./questions/required_questions";
import { optionAOptional, optionBOptional } from "./questions/optional_questions";

// Landing Page
function LandingPage() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: "2rem", maxWidth: "700px", margin: "0 auto" }}>
      <h1>AI Trip Itinerary Generator</h1>
      <h2>Select an Option</h2>

      <button
        onClick={() => navigate("/option-a")}
        style={{ marginRight: "1rem" }}
      >
        Option A – I don't know where to go
      </button>

      <button onClick={() => navigate("/option-b")}>
        Option B – I already know where I'm going
      </button>
    </div>
  );
}

// Shared Question Page Component
function QuestionPage({ requiredQs, optionalQs, title }) {
  const [formData, setFormData] = useState({});

  const handleChange = (id, value) => {
    setFormData((prev) => ({ ...prev, [id]: value }));
  };

  const questions = [...requiredQs, ...optionalQs];

  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <h1>{title}</h1>

      {questions.map((question) => {
        if (question.showIf && !question.showIf(formData)) return null;

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
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />

      <Route
        path="/option-a"
        element={
          <QuestionPage
            title="Option A – Discovery Mode"
            requiredQs={optionARequired}
            optionalQs={optionAOptional}
          />
        }
      />

      <Route
        path="/option-b"
        element={
          <QuestionPage
            title="Option B – Structured Mode"
            requiredQs={optionBRequired}
            optionalQs={optionBOptional}
          />
        }
      />
    </Routes>
  );
}