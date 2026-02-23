// ===============================
// REQUIRED QUESTIONS CONFIG FILE
// ===============================

export const optionARequired = [
    {
      id: "has_discovery_intent",
      type: "mc",
      label: "1. Do you have any idea what you want to do or what types of places you want to go?",
      options: ["Yes", "No"]
    },
    {
      id: "discovery_intent",
      type: "oe",
      label: "2. Describe the type(s) of places you want to go.",
      showIf: (formData) => formData.has_discovery_intent === "Yes"
    },
    {
      id: "knows_trip_length",
      type: "mc",
      label: "3. Do you know how long you want your trip to be?",
      options: ["Yes", "No"]
    },
    {
      id: "days",
      type: "num",
      label: "4. How long is your trip (in days)?",
      showIf: (formData) => formData.knows_trip_length === "Yes"
    },
    {
      id: "people",
      type: "mc",
      label: "5. How many people are planning to go?",
      options: ["1", "2", "3-4", "5-6", "7-9", "10-14", "15 or more"]
    },
    {
      id: "transport_mode",
      type: "mc",
      label: "6. How are you planning on getting to your destination?",
      options: ["Driving", "Flying", "Train", "Bus", "Cruise or ferry", "Not sure yet"]
    },
    {
      id: "origin_location",
      type: "oe",
      label: "7. Where are you currently? (City and country)"
    },
    {
      id: "international_travel",
      type: "mc",
      label: "8. Do you want to travel to a different country? Note: If you don't have a valid passport that allows international travel, answer 'no' to this question.",
      options: ["Yes", "No"]
    },
    {
      id: "preferred_countries",
      type: "oe",
      label: "9. What country (or countries) do you prefer?",
      showIf: (formData) => formData.international_travel === "Yes"
    },
    {
      id: "distance_preference",
      type: "mc",
      label: "10. How far do you want your destination to be?",
      options: [
        "<10 miles",
        "10-20 miles",
        "20-50 miles",
        "50-100 miles",
        "100-200 miles",
        "200-500 miles",
        ">500 miles"
      ],
      showIf: (formData) => formData.international_travel === "No"
    },
    {
      id: "has_dates",
      type: "mc",
      label: "11. Do you know the dates of your trip?",
      options: ["Yes", "No"]
    },
    {
      id: "date_range",
      type: "oe",
      label: "12. To make the AI understand the dates as clear as possible, enter the dates here in this format: [Month] [Day] to [Month] [Day].",
      showIf: (formData) => formData.has_dates === "Yes"
    },
    {
      id: "13. has_time_constraints",
      type: "mc",
      label: "Are there any strict time constraints?",
      options: ["Yes", "No"]
    },
    {
      id: "14. time_constraints_detail",
      type: "oe",
      label: "To make the AI understand the dates and times as clear as possible, enter the day(s) and time(s) you have time constraints in this format: [Month] [Day] from [hh:mm] [AM/PM] to [hh:mm] [AM/PM]. To enter more than one date or time, use commas to separate them.",
      showIf: (formData) => formData.has_time_constraints === "Yes"
    },
    {
      id: "area_structure",
      type: "mc",
      label: "15. Are you planning to visit one area (like one city, even if it is very big) or multiple areas (an example would be a trip across the entire Oregon Coast, since it contains multiple cities)?",
      options: ["Yes", "No"]
    },
    {
      id: "special_group_needs",
      type: "cata",
      label: "16. Are you traveling with children, disabled people, or elderly people?",
      options: ["Children", "Disabled People", "Elderly People", "None"]
    },
    {
      id: "accessibility_needs",
      type: "mc",
      label: "17. Do you have mobility limitations or accessibility needs?",
      options: ["Yes", "No"]
    },
    {
      id: "accessibility_details",
      type: "oe",
      label: "18. Explain the mobility limitations or accessibility needs.",
      showIf: (formData) => formData.accessibility_needs === "Yes"
    }
  ];
  
  
  export const optionBRequired = [
    {
      id: "destination",
      type: "oe",
      label: "1. Where is your trip? Include dates if possible."
    },
    {
      id: "knows_trip_length_b",
      type: "mc",
      label: "2. Do you know how long your trip is?",
      options: ["Yes", "No"]
    },
    {
      id: "days_b",
      type: "num",
      label: "3. How long is your trip (in days)?",
      showIf: (formData) => formData.knows_trip_length_b === "Yes"
    },
    {
      id: "people_b",
      type: "mc",
      label: "4. How many people are planning to go?",
      options: ["1", "2", "3-4", "5-6", "7-9", "10-14", "15 or more"]
    },
    {
      id: "has_time_constraints",
      type: "mc",
      label: "5. Are there any strict time constraints?",
      options: ["Yes", "No"]
    },
    {
      id: "time_constraints_detail",
      type: "oe",
      label: "6. To make the AI understand the dates and times as clear as possible, enter the day(s) and time(s) you have time constraints in this format: [Month] [Day] from [hh:mm] [AM/PM] to [hh:mm] [AM/PM]. To enter more than one date or time, use commas to separate them.",
      showIf: (formData) => formData.has_time_constraints === "Yes"
    },
    {
      id: "special_group_needs",
      type: "cata",
      label: "7. Are you traveling with children, disabled people, or elderly people?",
      options: ["Children", "Disabled People", "Elderly People", "None"]
    },
    {
      id: "accessibility_needs",
      type: "mc",
      label: "8. Do you have mobility limitations or accessibility needs?",
      options: ["Yes", "No"]
    },
    {
      id: "accessibility_details",
      type: "oe",
      label: "9. Explain the mobility limitations or accessibility needs.",
      showIf: (formData) => formData.accessibility_needs === "Yes"
    }
  ];  