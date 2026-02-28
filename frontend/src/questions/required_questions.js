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
    label: "2. Describe the type(s) of places you want to go. The more specific, the better. For example, you could say \"I want to go to a place (or places) where there are lots of hiking trails and beaches.\"",
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
    label: "4. How long is your trip? Enter the number of days. (1–30)",
    showIf: (formData) => formData.knows_trip_length === "Yes"
  },
  {
    id: "people",
    type: "mc",
    label: "5. How many people are planning to go on your trip, including yourself?",
    options: ["1", "2", "3-4", "5-6", "7-9", "10-14", "15 or more", "Not sure yet"]
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
    label: "7. Where are you currently? If possible, include the city and country."
  },
  {
    id: "international_travel",
    type: "mc",
    label: "8. Do you want to travel to a different country? Note: If you don't have a valid passport that allows international travel, answer \"No\" to this question.",
    options: ["Yes", "No"]
  },
  {
    id: "preferred_countries",
    type: "oe",
    label: "9. What country (or countries) do you prefer? Only list countries where your passport is valid for travel.",
    showIf: (formData) => formData.international_travel === "Yes"
  },
  {
    id: "distance_preference",
    type: "mc",
    label: "10. How far do you want your destination to be away from your current location?",
    options: [
      "<10 miles",
      "10-20 miles",
      "20-50 miles",
      "50-100 miles",
      "100-200 miles",
      "200-500 miles",
      ">500 miles",
      "Don't care"
    ],
    showIf: (formData) => formData.international_travel === "No"
  },
  {
    id: "has_dates",
    type: "mc",
    label: "11. Do you know the dates that you want your trip to be?",
    options: ["Yes", "No"]
  },
  {
    id: "date_range",
    type: "oe",
    label: "12. Enter the dates here in this format: [Month] [Day] to [Month] [Day].",
    showIf: (formData) => formData.has_dates === "Yes"
  },
  {
    id: "has_time_constraints",
    type: "mc",
    label: "13. Are there any strict time constraints on specific days?",
    options: ["Yes", "No"]
  },
  {
    id: "time_constraints_detail",
    type: "oe",
    label: "14. Enter the day(s) and time(s) you have time constraints in this format: [Month] [Day] from [hh:mm] [AM/PM] to [hh:mm] [AM/PM]. To enter more than one, use commas to separate them.",
    showIf: (formData) => formData.has_time_constraints === "Yes"
  },
  {
    id: "area_structure",
    type: "mc",
    label: "15. Are you planning to visit one area (like one city, even if it is very big) or multiple areas (an example would be a trip across the entire Oregon Coast, since it contains multiple cities)?",
    options: ["One area", "Multiple areas"]
  },
  {
    id: "special_group_needs",
    type: "cata",
    label: "16. Are you traveling with children, disabled people, and/or elderly people? Check all that apply.",
    options: ["Children", "Disabled People", "Elderly People", "None"]
  },
  {
    id: "accessibility_needs",
    type: "mc",
    label: "17. Do you (or anyone in your group) have any mobility limitations and/or accessibility needs?",
    options: ["Yes", "No"]
  },
  {
    id: "accessibility_details",
    type: "oe",
    label: "18. Explain the mobility limitations and/or accessibility needs here.",
    showIf: (formData) => formData.accessibility_needs === "Yes"
  }
];


export const optionBRequired = [
  {
    id: "destination",
    type: "oe",
    label: "1. Where is your trip? Enter the city or area you are staying. If possible, give the dates. If you are staying in multiple places, be as detailed as possible (for example, \"New York City, 6/24-6/27, Boston, 6/28-6/30, Miami, 7/1-7/4\")."
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
    label: "3. How long is your trip? Enter the number of days. (1–30)",
    showIf: (formData) => formData.knows_trip_length_b === "Yes"
  },
  {
    id: "people_b",
    type: "mc",
    label: "4. How many people are planning to go on your trip, including yourself?",
    options: ["1", "2", "3-4", "5-6", "7-9", "10-14", "15 or more", "Not sure yet"]
  },
  {
    id: "has_time_constraints",
    type: "mc",
    label: "5. Are there any strict time constraints on specific days?",
    options: ["Yes", "No"]
  },
  {
    id: "time_constraints_detail",
    type: "oe",
    label: "6. Enter the day(s) and time(s) you have time constraints in this format: [Month] [Day] from [hh:mm] [AM/PM] to [hh:mm] [AM/PM]. To enter more than one, use commas to separate them.",
    showIf: (formData) => formData.has_time_constraints === "Yes"
  },
  {
    id: "special_group_needs",
    type: "cata",
    label: "7. Are you traveling with children, disabled people, and/or elderly people? Check all that apply.",
    options: ["Children", "Disabled People", "Elderly People", "None"]
  },
  {
    id: "accessibility_needs",
    type: "mc",
    label: "8. Do you (or anyone in your group) have any mobility limitations or accessibility needs?",
    options: ["Yes", "No"]
  },
  {
    id: "accessibility_details",
    type: "oe",
    label: "9. Explain the mobility limitations and/or accessibility needs here.",
    showIf: (formData) => formData.accessibility_needs === "Yes"
  }
];