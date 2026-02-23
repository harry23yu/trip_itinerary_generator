// ===============================
// OPTIONAL QUESTIONS CONFIG FILE
// ===============================
//
// Each question object supports:
// - id: string (unique key in formData)
// - type: "mc" | "oe" | "num" | "cata"
// - label: string
// - options: string[] (for mc/cata)
// - showIf: (formData) => boolean (optional conditional rendering)
//
// Optional questions only (per question_design.txt).
// "Other" handling: we add a follow-up OE question with showIf.
//
// NOTE: Option B uses _b suffix on ids to avoid collisions with Option A.
//

export const optionAOptional = [
    {
      id: "money_concern",
      type: "mc",
      label: "19. Is money a concern?",
      options: ["Yes", "No"],
    },
    {
      id: "budget",
      type: "num",
      label:
        "20. How much are you (or your group) willing to spend? If you're not sure, feel free to leave this blank. (1–100000)",
      showIf: (formData) => formData.money_concern === "Yes",
    },
    {
      id: "weather_avoid",
      type: "cata",
      label: "21. What types of weather do you want to avoid or can't tolerate?",
      options: [
        "Extreme heat",
        "Extreme cold",
        "Heavy rain",
        "Snow / icy conditions",
        "High humidity",
        "Low humidity",
        "Strong wind",
        "Hurricane / storm season",
        "None — weather doesn’t matter much",
        "Not sure yet",
      ],
    },
    {
      id: "interests",
      type: "oe",
      label: "22. What types of things interest you?",
    },
    {
      id: "food_interest",
      type: "num",
      label:
        "23. Are you into restaurants and food? Rate on a scale from 1-10 (1 = not at all, 10 = very much).",
    },
    {
      id: "cuisines",
      type: "cata",
      label:
        "24. What types of cuisine do you like? If you aren't really that much into restaurants and food, feel free to skip this question.",
      options: [
        "American",
        "Chinese",
        "French",
        "Greek",
        "Indian",
        "Italian",
        "Japanese",
        "Korean",
        "Mediterranean",
        "Mexican",
        "Middle Eastern",
        "Spanish",
        "Thai",
        "Vietnamese",
        "Other",
      ],
    },
    {
      id: "cuisines_other",
      type: "oe",
      label: "What other cuisines do you like?",
      showIf: (formData) => (formData.cuisines || []).includes("Other"),
    },
    {
      id: "shopping_interest",
      type: "num",
      label:
        "25. Are you into shops, shopping malls, and buying stuff? Rate on a scale from 1-10 (1 = not at all, 10 = very much).",
    },
    {
      id: "shopping_items",
      type: "cata",
      label:
        "26. What types of things are you interested in buying? If you aren't really that much into buying stuff, feel free to skip this question.",
      options: [
        "Antiques",
        "Art",
        "Books",
        "Clothing / fashion",
        "Electronics",
        "Handmade crafts",
        "Jewelry",
        "Local specialty foods",
        "Luxury goods",
        "Outdoor gear",
        "Souvenirs",
        "Street markets",
        "Vintage items",
        "Other",
      ],
    },
    {
      id: "shopping_items_other",
      type: "oe",
      label: "What other types of things are you interested in buying?",
      showIf: (formData) => (formData.shopping_items || []).includes("Other"),
    },
    {
      id: "trip_purpose",
      type: "oe",
      label: "27. What is the main purpose of this trip?",
    },
    {
      id: "schedule_preference",
      type: "mc",
      label: "28. Do you prefer a packed schedule or a relaxed one?",
      options: ["Packed", "Relaxed", "Somewhere in between"],
    },
    {
      id: "must_do",
      type: "oe",
      label: "29. What are some things you definitely want to do?",
    },
    {
      id: "must_avoid",
      type: "oe",
      label: "30. What are some things you definitely want to avoid?",
    },
    {
      id: "physical_activity",
      type: "num",
      label:
        "31. How physically active do you want this trip to be? Rate on a scale from 1-10 (1 = not at all, 10 = very much).",
    },
    {
      id: "public_transport_comfort",
      type: "num",
      label:
        "32. How comfortable are you with using public transportation? Rate on a scale from 1-10 (1 = not at all, 10 = very much).",
    },
    {
      id: "nightlife",
      type: "mc",
      label: "33. Do you want nightlife included?",
      options: ["Yes", "No"],
    },
    {
      id: "photography_importance",
      type: "num",
      label:
        "34. How important is photography or Instagram-style spots? Rate on a scale from 1-10 (1 = not at all, 10 = very much).",
    },
    {
      id: "end_feeling",
      type: "oe",
      label: "35. How do you want to feel at the end of this trip?",
    },
    {
      id: "travel_vs_depth",
      type: "mc",
      label:
        "36. Would you rather spend more time traveling or more time in fewer places?",
      options: [
        "More time traveling",
        "more time in fewer places",
        "Somewhere in between",
      ],
    },
    {
      id: "places_to_avoid",
      type: "oe",
      label:
        "37. Anywhere (cities, districts, important attractions) that you don't want to visit (or don't have time to visit)?",
    },
    {
      id: "start_time",
      type: "mc",
      label: "38. When do you want to start exploring each day (or most days)?",
      options: ["7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "Other"],
    },
    {
      id: "start_time_other",
      type: "oe",
      label: "What time do you want to start exploring?",
      showIf: (formData) => formData.start_time === "Other",
    },
    {
      id: "return_time",
      type: "mc",
      label:
        "39. When do you want to go back to your hotel (or the place you're staying) each day (or most days)?",
      options: [
        "5 PM",
        "6 PM",
        "7 PM",
        "8 PM",
        "9 PM",
        "10 PM",
        "11 PM",
        "12 AM",
        "Other",
      ],
    },
    {
      id: "return_time_other",
      type: "oe",
      label: "What time do you want to go back to your hotel?",
      showIf: (formData) => formData.return_time === "Other",
    },
    {
      id: "anything_else",
      type: "oe",
      label: "40. Anything else that you want to add? The more specific, the better.",
    },
  ];
  
  export const optionBOptional = [
    {
      id: "money_concern_b",
      type: "mc",
      label: "10. Is money a concern?",
      options: ["Yes", "No"],
    },
    {
      id: "budget_b",
      type: "num",
      label:
        "11. How much are you (or your group) willing to spend? If you're not sure, feel free to leave this blank. (1–100000)",
      showIf: (formData) => formData.money_concern_b === "Yes",
    },
    {
      id: "weather_avoid_b",
      type: "cata",
      label: "12. What types of weather do you want to avoid or can't tolerate?",
      options: [
        "Extreme heat",
        "Extreme cold",
        "Heavy rain",
        "Snow / icy conditions",
        "High humidity",
        "Low humidity",
        "Strong wind",
        "Hurricane / storm season",
        "None — weather doesn’t matter much",
        "Not sure yet",
      ],
    },
    {
      id: "interests_b",
      type: "oe",
      label: "13. What types of things interest you?",
    },
    {
      id: "food_interest_b",
      type: "num",
      label:
        "14. Are you into restaurants and food? Rate on a scale from 1-10 (1 = not at all, 10 = very much).",
    },
    {
      id: "cuisines_b",
      type: "cata",
      label:
        "15. What types of cuisine do you like? If you aren't really that much into restaurants and food, feel free to skip this question.",
      options: [
        "American",
        "Chinese",
        "French",
        "Greek",
        "Indian",
        "Italian",
        "Japanese",
        "Korean",
        "Mediterranean",
        "Mexican",
        "Middle Eastern",
        "Spanish",
        "Thai",
        "Vietnamese",
        "Other",
      ],
    },
    {
      id: "cuisines_other_b",
      type: "oe",
      label: "What other cuisines do you like?",
      showIf: (formData) => (formData.cuisines_b || []).includes("Other"),
    },
    {
      id: "shopping_interest_b",
      type: "num",
      label:
        "16. Are you into shops, shopping malls, and buying stuff? Rate on a scale from 1-10 (1 = not at all, 10 = very much).",
    },
    {
      id: "shopping_items_b",
      type: "cata",
      label:
        "17. What types of things are you interested in buying? If you aren't really that much into buying stuff, feel free to skip this question.",
      options: [
        "Antiques",
        "Art",
        "Books",
        "Clothing / fashion",
        "Electronics",
        "Handmade crafts",
        "Jewelry",
        "Local specialty foods",
        "Luxury goods",
        "Outdoor gear",
        "Souvenirs",
        "Street markets",
        "Vintage items",
        "Other",
      ],
    },
    {
      id: "shopping_items_other_b",
      type: "oe",
      label: "What other types of things are you interested in buying?",
      showIf: (formData) => (formData.shopping_items_b || []).includes("Other"),
    },
    {
      id: "trip_purpose_b",
      type: "oe",
      label: "18. What is the main purpose of this trip?",
    },
    {
      id: "schedule_preference_b",
      type: "mc",
      label: "19. Do you prefer a packed schedule or a relaxed one?",
      options: ["Packed", "Relaxed", "Somewhere in between"],
    },
    {
      id: "must_do_b",
      type: "oe",
      label: "20. What are some things you definitely want to do?",
    },
    {
      id: "must_avoid_b",
      type: "oe",
      label: "21. What are some things you definitely want to avoid?",
    },
    {
      id: "physical_activity_b",
      type: "num",
      label:
        "22. How physically active do you want this trip to be? Rate on a scale from 1-10 (1 = not at all, 10 = very much).",
    },
    {
      id: "public_transport_comfort_b",
      type: "num",
      label:
        "23. How comfortable are you with using public transportation? Rate on a scale from 1-10 (1 = not at all, 10 = very much).",
    },
    {
      id: "nightlife_b",
      type: "mc",
      label: "24. Do you want nightlife included?",
      options: ["Yes", "No"],
    },
    {
      id: "photography_importance_b",
      type: "num",
      label:
        "25. How important is photography or Instagram-style spots? Rate on a scale from 1-10 (1 = not at all, 10 = very much).",
    },
    {
      id: "end_feeling_b",
      type: "oe",
      label: "26. What do you want to feel at the end of this trip?",
    },
    {
      id: "travel_vs_depth_b",
      type: "mc",
      label:
        "27. Would you rather spend more time traveling or more time in fewer places?",
      options: [
        "More time traveling",
        "more time in fewer places",
        "Somewhere in between",
      ],
    },
    {
      id: "places_to_avoid_b",
      type: "oe",
      label:
        "28. Anywhere (cities, districts, important attractions) that you don't want to visit (or don't have time to visit)?",
    },
    {
      id: "start_time_b",
      type: "mc",
      label: "29. When do you want to start exploring each day (or most days)?",
      options: ["7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "Other"],
    },
    {
      id: "start_time_other_b",
      type: "oe",
      label: "What time do you want to start exploring?",
      showIf: (formData) => formData.start_time_b === "Other",
    },
    {
      id: "return_time_b",
      type: "mc",
      label:
        "30. When do you want to go back to your hotel (or the place you're staying) each day (or most days)?",
      options: [
        "5 PM",
        "6 PM",
        "7 PM",
        "8 PM",
        "9 PM",
        "10 PM",
        "11 PM",
        "12 AM",
        "Other",
      ],
    },
    {
      id: "return_time_other_b",
      type: "oe",
      label: "What time do you want to go back to your hotel?",
      showIf: (formData) => formData.return_time_b === "Other",
    },
    {
      id: "anything_else_b",
      type: "oe",
      label: "31. Anything else that you want to add? The more specific, the better.",
    },
  ];