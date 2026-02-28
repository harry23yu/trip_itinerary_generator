import { useMemo, useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import QuestionRenderer from "./questions/QuestionRenderer";
import { optionARequired, optionBRequired } from "./questions/required_questions";
import { optionAOptional, optionBOptional } from "./questions/optional_questions";

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: "2rem", maxWidth: "700px", margin: "0 auto" }}>
      <h1>AI Trip Itinerary Generator</h1>
      <h2>Select an Option</h2>

      <button onClick={() => navigate("/option-a")} style={{ marginRight: "1rem" }}>
        Option A – I don't know where to go
      </button>

      <button onClick={() => navigate("/option-b")}>
        Option B – I already know where I'm going
      </button>
    </div>
  );
}

// Renders the validated itinerary JSON inline on the page
function ItineraryDisplay({ itinerary }) {
  if (!itinerary) return null;

  const { days, summary } = itinerary;

  const sectionStyle = {
    marginBottom: "0.5rem",
  };

  const sectionHeadingStyle = {
    fontWeight: "bold",
    marginBottom: "0.25rem",
    textTransform: "capitalize",
  };

  const activityStyle = {
    marginLeft: "1.25rem",
    marginBottom: "0.2rem",
  };

  return (
    <div style={{ marginTop: "2rem", borderTop: "1px solid #ccc", paddingTop: "1.5rem" }}>
      <h2>Your Itinerary</h2>

      {days && days.map((dayData) => (
        <div key={dayData.day} style={{ marginBottom: "1.5rem" }}>
          <h3>Day {dayData.day}</h3>

          {["morning", "afternoon", "evening"].map((section) => {
            const activities = dayData.sections?.[section] || [];
            if (activities.length === 0) return null;

            return (
              <div key={section} style={sectionStyle}>
                <div style={sectionHeadingStyle}>{section}</div>
                {activities.map((activity, i) => (
                  <div key={i} style={activityStyle}>• {activity}</div>
                ))}
              </div>
            );
          })}
        </div>
      ))}

      {summary && (
        <div style={{ marginTop: "1rem", borderTop: "1px solid #eee", paddingTop: "1rem" }}>
          <h3>Summary</h3>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

function QuestionPage({ requiredQs, optionalQs, title }) {
  const [formData, setFormData] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [itinerary, setItinerary] = useState(null);

  const handleChange = (id, value) => {
    setFormData((prev) => ({ ...prev, [id]: value }));
  };

  const questions = useMemo(() => [...requiredQs, ...optionalQs], [requiredQs, optionalQs]);
  const isVisible = (q) => !q.showIf || q.showIf(formData);

  // Required only when visible.
  // Exception: budget follow-up (id "budget" / "budget_b") is optional even when visible.
  const optionalEvenWhenVisible = new Set(["budget", "budget_b"]);

  // Helper: returns false if a question with otherTextId has "Other" selected but text is empty.
  // Applies to ALL questions (required and optional) since the backend enforces this too.
  const otherTextFilled = (q) => {
    if (!q.otherTextId || !isVisible(q)) return true;
    const value = formData[q.id];
    const otherSelected =
      (q.type === "mc" && value === "Other") ||
      (q.type === "cata" && Array.isArray(value) && value.includes("Other"));
    if (!otherSelected) return true;
    const otherText = formData[q.otherTextId];
    return !!(otherText && String(otherText).trim() !== "");
  };

  const hasRequiredAnswers =
    requiredQs.every((q) => {
      if (!isVisible(q)) return true;
      if (optionalEvenWhenVisible.has(q.id)) return true;

      const value = formData[q.id];
      if (value === undefined || value === null) return false;
      if (typeof value === "string" && value.trim() === "") return false;
      if (Array.isArray(value) && value.length === 0) return false;

      return otherTextFilled(q);
    }) &&
    // Also block if any optional question has "Other" selected but text is empty
    optionalQs.every((q) => otherTextFilled(q));

  const toBool = (v) => v === true || v === "Yes";

  const toIntOrNull = (v) => {
    if (v === undefined || v === null || String(v).trim() === "") return null;
    const n = parseInt(v, 10);
    return Number.isFinite(n) ? n : null;
  };

  const toListOrNull = (v) => {
    if (v === undefined || v === null) return null;
    if (Array.isArray(v)) return v.length ? v : null;
    if (typeof v !== "string") return null;

    const parts = v
      .split(/\n|,/)
      .map((s) => s.trim())
      .filter(Boolean);

    return parts.length ? parts : null;
  };

  const buildTripContext = () => {
    const isOptionA = title.startsWith("Option A");
    const trip_mode = isOptionA ? "discover" : "known";

    const ctx = {
      trip_mode,

      // --- Option A required ---
      has_discovery_intent: toBool(formData.has_discovery_intent),
      discovery_intent: formData.discovery_intent || null,

      knows_trip_length: toBool(formData.knows_trip_length),
      days: toIntOrNull(formData.days),

      // people is a string like "1", "3-4", "15 or more" — sent as-is; backend accepts Any
      people: formData.people ?? null,

      transport_mode: formData.transport_mode || "Not specified",
      origin_location: formData.origin_location || "Not specified",

      international_travel: toBool(formData.international_travel),
      preferred_countries: formData.preferred_countries || null,
      distance_preference: formData.distance_preference || null,

      has_dates: toBool(formData.has_dates),
      date_range: formData.date_range || null,

      has_time_constraints: toBool(formData.has_time_constraints),
      time_constraints_detail: formData.time_constraints_detail || null,

      area_structure: formData.area_structure || "Not specified",

      special_group_needs: Array.isArray(formData.special_group_needs)
        ? formData.special_group_needs
        : ["None"],

      accessibility_needs: toBool(formData.accessibility_needs),
      accessibility_details: formData.accessibility_details || null,

      // --- Option B required ---
      destination: formData.destination || null,

      knows_trip_length_b: formData.knows_trip_length_b
        ? toBool(formData.knows_trip_length_b)
        : null,
      days_b: toIntOrNull(formData.days_b),
      // people_b is a string like "1", "3-4" — same pattern as people
      people_b: formData.people_b ?? null,

      // --- Optional shared ---
      // Option A uses money_concern / budget; Option B uses money_concern_b / budget_b
      budget_concern: isOptionA
        ? formData.money_concern === "Yes"
          ? true
          : formData.money_concern === "No"
          ? false
          : null
        : formData.money_concern_b === "Yes"
        ? true
        : formData.money_concern_b === "No"
        ? false
        : null,

      budget_amount: isOptionA
        ? toIntOrNull(formData.budget)
        : toIntOrNull(formData.budget_b),

      weather_avoidance: isOptionA
        ? toListOrNull(formData.weather_avoid)
        : toListOrNull(formData.weather_avoid_b),

      interests: isOptionA
        ? formData.interests || null
        : formData.interests_b || null,

      food_interest_level: isOptionA
        ? toIntOrNull(formData.food_interest)
        : toIntOrNull(formData.food_interest_b),

      cuisine_preferences: isOptionA
        ? toListOrNull(formData.cuisines)
        : toListOrNull(formData.cuisines_b),

      cuisine_preferences_other_text: isOptionA
        ? formData.cuisines_other || null
        : formData.cuisines_other_b || null,

      shopping_interest_level: isOptionA
        ? toIntOrNull(formData.shopping_interest)
        : toIntOrNull(formData.shopping_interest_b),

      shopping_preferences: isOptionA
        ? toListOrNull(formData.shopping_items)
        : toListOrNull(formData.shopping_items_b),

      shopping_preferences_other_text: isOptionA
        ? formData.shopping_items_other || null
        : formData.shopping_items_other_b || null,

      trip_purpose: isOptionA
        ? formData.trip_purpose || null
        : formData.trip_purpose_b || null,

      schedule_style: isOptionA
        ? formData.schedule_preference || null
        : formData.schedule_preference_b || null,

      must_do: isOptionA
        ? toListOrNull(formData.must_do)
        : toListOrNull(formData.must_do_b),

      must_avoid: isOptionA
        ? toListOrNull(formData.must_avoid)
        : toListOrNull(formData.must_avoid_b),

      physical_activity_level: isOptionA
        ? toIntOrNull(formData.physical_activity)
        : toIntOrNull(formData.physical_activity_b),

      public_transit_comfort: isOptionA
        ? toIntOrNull(formData.public_transport_comfort)
        : toIntOrNull(formData.public_transport_comfort_b),

      nightlife: isOptionA
        ? formData.nightlife === "Yes"
          ? true
          : formData.nightlife === "No"
          ? false
          : null
        : formData.nightlife_b === "Yes"
        ? true
        : formData.nightlife_b === "No"
        ? false
        : null,

      photography_importance: isOptionA
        ? toIntOrNull(formData.photography_importance)
        : toIntOrNull(formData.photography_importance_b),

      desired_feelings: isOptionA
        ? toListOrNull(formData.end_feeling)
        : toListOrNull(formData.end_feeling_b),

      travel_vs_depth: isOptionA
        ? formData.travel_vs_depth || null
        : formData.travel_vs_depth_b || null,

      excluded_places: isOptionA
        ? toListOrNull(formData.places_to_avoid)
        : toListOrNull(formData.places_to_avoid_b),

      start_time_preference: isOptionA
        ? formData.start_time || null
        : formData.start_time_b || null,

      start_time_other_text: isOptionA
        ? formData.start_time_other || null
        : formData.start_time_other_b || null,

      end_time_preference: isOptionA
        ? formData.return_time || null
        : formData.return_time_b || null,

      end_time_other_text: isOptionA
        ? formData.return_time_other || null
        : formData.return_time_other_b || null,

      additional_notes: isOptionA
        ? formData.anything_else || null
        : formData.anything_else_b || null,
    };

    // Backend mutual-exclusion rules for discover mode
    if (trip_mode === "discover") {
      if (ctx.international_travel) ctx.distance_preference = null;
      if (!ctx.international_travel) ctx.preferred_countries = null;
    }

    return ctx;
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);
    setItinerary(null);

    try {
      const payload = buildTripContext();

      const response = await fetch("http://127.0.0.1:8000/generate-itinerary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const maybeText = await response.text();
        throw new Error(`Backend returned status ${response.status}: ${maybeText}`);
      }

      // Backend returns JSON: { itinerary: { days: [...], summary: "..." }, pdf_path: "..." }
      const data = await response.json();
      setItinerary(data.itinerary);

      // If the backend also generated a PDF, trigger a download automatically
      if (data.pdf_path) {
        const pdfUrl = `http://127.0.0.1:8000/download-itinerary/${encodeURIComponent(data.pdf_path)}`;
        const link = document.createElement("a");
        link.href = pdfUrl;
        link.download = "itinerary.pdf";
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    } catch (e) {
      console.error(e);
      setError("Generation failed. Check the backend logs and try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <h1>{title}</h1>

      {questions.map((question) => {
        if (!isVisible(question)) return null;

        return (
          <QuestionRenderer
            key={question.id}
            question={question}
            value={formData[question.id]}
            formData={formData}
            handleChange={handleChange}
          />
        );
      })}

      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

      <button
        onClick={handleSubmit}
        disabled={isSubmitting || !hasRequiredAnswers}
        style={{ marginTop: "2rem" }}
      >
        {isSubmitting ? "Generating..." : "Generate itinerary"}
      </button>

      {/* Inline itinerary display, rendered below the button after generation */}
      <ItineraryDisplay itinerary={itinerary} />
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