import React from "react";

const QuestionRenderer = ({ question, value, formData, handleChange }) => {
  if (!question) return null;

  const otherTextValue = question.otherTextId ? (formData?.[question.otherTextId] ?? "") : "";

  const renderInput = () => {
    switch (question.type) {
      case "mc":
        return (
          <div>
            <select value={value || ""} onChange={(e) => handleChange(question.id, e.target.value)}>
              <option value="">Select an option</option>
              {question.options.map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>

            {question.otherTextId && value === "Other" && (
              <div style={{ marginTop: "0.5rem" }}>
                <input
                  type="text"
                  value={otherTextValue}
                  placeholder={question.otherPlaceholder || "Enter other..."}
                  onChange={(e) => handleChange(question.otherTextId, e.target.value)}
                />
              </div>
            )}
          </div>
        );

      case "oe":
        return (
          <textarea value={value || ""} onChange={(e) => handleChange(question.id, e.target.value)} rows={3} />
        );

      case "num":
        return <input type="number" value={value || ""} onChange={(e) => handleChange(question.id, e.target.value)} />;

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
                      if (e.target.checked) newVals.push(opt);
                      else newVals = newVals.filter((v) => v !== opt);
                      handleChange(question.id, newVals);
                    }}
                  />
                  {opt}
                </label>
              );
            })}

            {question.otherTextId && Array.isArray(value) && value.includes("Other") && (
              <div style={{ marginTop: "0.5rem" }}>
                <input
                  type="text"
                  value={otherTextValue}
                  placeholder={question.otherPlaceholder || "Enter other..."}
                  onChange={(e) => handleChange(question.otherTextId, e.target.value)}
                />
              </div>
            )}
          </div>
        );

      default:
        return null;
    }
  };

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