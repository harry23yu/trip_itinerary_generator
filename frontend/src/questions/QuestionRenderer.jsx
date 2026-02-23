import React from "react";

const QuestionRenderer = ({ question, value, handleChange }) => {
  if (!question) return null;

  const renderInput = () => {
    switch (question.type) {
      case "mc":
        return (
          <select
            value={value || ""}
            onChange={(e) => handleChange(question.id, e.target.value)}
          >
            <option value="">Select an option</option>
            {question.options.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        );

      case "oe":
        return (
          <textarea
            value={value || ""}
            onChange={(e) => handleChange(question.id, e.target.value)}
            rows={3}
          />
        );

      case "num":
        return (
          <input
            type="number"
            value={value || ""}
            onChange={(e) => handleChange(question.id, e.target.value)}
          />
        );

      case "cata":
        return (
          <div>
            {question.options.map((opt) => {
              const selected = Array.isArray(value) && value.includes(opt);

              return (
                <label key={opt} style={{ display: "block" }}>
                  <input
                    type="checkbox"
                    checked={selected}
                    onChange={(e) => {
                      let newVals = Array.isArray(value) ? [...value] : [];
                      if (e.target.checked) {
                        newVals.push(opt);
                      } else {
                        newVals = newVals.filter((v) => v !== opt);
                      }
                      handleChange(question.id, newVals);
                    }}
                  />
                  {opt}
                </label>
              );
            })}
          </div>
        );

      default:
        return null;
    }
  };

  // FINAL RETURN (your file was missing this!)
  return (
    <div style={{ marginBottom: "1.5rem" }}>
      <label>
        <strong>{question.label}</strong>
      </label>
      <div>{renderInput()}</div>
    </div>
  );
};

export default QuestionRenderer;