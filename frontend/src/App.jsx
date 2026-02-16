import { useState } from "react";

function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateTestItinerary = async () => {
    setLoading(true);

    const testPayload = {
      trip_mode: "discover",
      has_discovery_intent: false,
      discovery_intent: null,
      knows_trip_length: true,
      days: 2,
      people: 1,
      transport_mode: "Driving",
      origin_location: "Phoenix, AZ",
      international_travel: false,
      preferred_countries: null,
      distance_preference: "100-200 miles",
      has_dates: false,
      date_range: null,
      has_time_constraints: false,
      time_constraints_detail: null,
      area_structure: "Yes",
      special_group_needs: ["None"],
      accessibility_needs: false,
      accessibility_details: null,
      destination: null,
      knows_trip_length_b: null,
      days_b: null,
      people_b: null,
      budget_concern: false,
      budget_amount: null,
      weather_avoidance: [],
      interests: null,
      food_interest_level: 5,
      cuisine_preferences: [],
      cuisine_preferences_other_text: null,
      shopping_interest_level: 3,
      shopping_preferences: [],
      shopping_preferences_other_text: null,
      trip_purpose: null,
      schedule_style: "Relaxed",
      must_do: [],
      must_avoid: [],
      physical_activity_level: 5,
      public_transit_comfort: 5,
      nightlife: false,
      photography_importance: 5,
      desired_feelings: [],
      travel_vs_depth: "More time traveling",
      excluded_places: [],
      start_time_preference: "9 AM",
      start_time_other_text: null,
      end_time_preference: "6 PM",
      end_time_other_text: null,
      additional_notes: null
    };

    const res = await fetch("http://127.0.0.1:8000/generate-itinerary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(testPayload)
    });

    const data = await res.json();
    setResponse(data);
    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h1>AI Trip Itinerary Generator</h1>

      <button onClick={generateTestItinerary}>
        Generate Test Itinerary
      </button>

      {loading && <p>Generating itinerary...</p>}

      {response && (
        <pre style={{ marginTop: "20px" }}>
          {JSON.stringify(response, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default App;