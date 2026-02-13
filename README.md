# AI Trip Itinerary Generator

An AI-powered travel itinerary generator that creates **realistic, preference-aware itineraries** by asking users structured, constraint-first questions.

Unlike generic AI travel planners, this project is designed to reduce hallucinations, avoid rushed schedules, and respect uncertainty by explicitly separating **hard constraints** from **soft preferences**.

---

## Project Status

**In active development. Backend is done, frontend in progress.**

- Backend pipeline is functional end-to-end
- Both trip modes (discover + known destination) work
- Structured itinerary JSON validation implemented
- PDF itinerary export implemented
- Prompt and itinerary refinement ongoing

---

## Trip Modes

### Option A: Discover a Destination
For users who **don’t know where they want to go yet**.

The system:
- Interprets high-level intent (e.g. “relaxing,” “nature,” “not rushed”)
- Applies distance, transport, budget, and pacing constraints
- Suggests a coherent trip with specific destinations

### Option B: Known Destination
For users who **already know where they’re going**.

The system:
- Builds a day-by-day itinerary for a fixed location
- Respects time constraints, rest days, accessibility, and schedule style
- Avoids overloading days or repeating similar activities

---

## Core Design Principles

- **Constraint-first questioning**  
  Required constraints (dates, duration, mobility, transport, time limits) are collected before preferences.

- **Explicit uncertainty handling**  
  Optional or unanswered questions are treated as unknown rather than guessed.

- **Preference-weighted, not preference-dominated**  
  Interests like food, shopping, nightlife, and photography influence decisions proportionally.

- **Realistic pacing**  
  Supports relaxed schedules, early evenings, rest days, and partial days.

- **Avoids generic or unverifiable attractions**  
  Prioritizes well-known, accessible locations and realistic travel flow.

---

## How It Works (High Level)

1. User selects a trip mode (discover or known destination)
2. System asks structured questions to gather:
   - Constraints (required)
   - Preferences (optional)
3. Inputs normalize into a single itinerary context
4. The model generates a day-by-day itinerary that:
   - Respects constraints and exclusions
   - Accounts for uncertainty
   - Balances activity, rest, and travel time

---

## Repository Structure

```text
AI_TRIP_ITINERARY_GENERATOR/
├── backend/
  ├── itinerary_schema.py
  ├── main.py
  ├── pdf_generator.py
├── frontend/
├── generated_pdfs/             # Ignored
├── venv/                       # Ignored
├── .env                        # Ignored
├── .gitignore
├── question_design.txt
├── README.md
├── requirements.txt
```

---

## Current Capabilities

- Two fully defined trip modes (discover + known)
- Structured constraint and preference capture
- Preference-aware itinerary generation
- Support for:
  - Time constraints
  - Activity level
  - Accessibility considerations
  - Early/late schedule preferences
- Outputs realistic, named locations and coherent daily flow
- Automatic PDF itinerary generation with timestamped filenames

---

## Sample JSON Request (Option A, Discover a Destination)

```text
{
  "trip_mode": "discover",

  "has_discovery_intent": true,
  "discovery_intent": "I want a destination with a lot of museums and amusement parks.",

  "knows_trip_length": true,
  "days": 5,

  "people": 2,

  "transport_mode": "Driving",
  "origin_location": "Phoenix, AZ",

  "international_travel": false,
  "preferred_countries": null,
  "distance_preference": "200-500 miles",

  "has_dates": true,
  "date_range": "July 10 to July 14",

  "has_time_constraints": true,
  "time_constraints_detail": "July 12 from 2:00 PM to 5:00 PM",

  "area_structure": "Yes",

  "special_group_needs": ["None"],
  "accessibility_needs": false,
  "accessibility_details": null,

  "destination": null,
  "knows_trip_length_b": null,
  "days_b": null,
  "people_b": null,

  "budget_concern": true,
  "budget_amount": 2500,

  "weather_avoidance": ["Extreme heat", "High humidity"],

  "interests": "Museums, family fun centers, and amusement parks.",

  "food_interest_level": 8,
  "cuisine_preferences": ["Italian", "Other"],
  "cuisine_preferences_other_text": "Peruvian",

  "shopping_interest_level": 5,
  "shopping_preferences": ["Local specialty foods", "Other"],
  "shopping_preferences_other_text": "Independent bookstores",

  "trip_purpose": "Relaxing anniversary getaway",
  "schedule_style": "Packed",

  "must_do": ["Watch a sunset over the ocean", "Visit a lighthouse"],
  "must_avoid": ["None"],

  "physical_activity_level": 6,
  "public_transit_comfort": 3,

  "nightlife": false,
  "photography_importance": 9,

  "desired_feelings": ["Inspired", "Connected"],

  "travel_vs_depth": "More time traveling",

  "excluded_places": ["Charlotte"],

  "start_time_preference": "Other",
  "start_time_other_text": "8:30 AM",

  "end_time_preference": "9 PM",
  "end_time_other_text": null,

  "additional_notes": "Prefer boutique hotels over large resorts."
}
```

---

## Sample Output (Generated Itinerary)

```text
{
  "itinerary": {
    "days": [
      {
        "day": 1,
        "sections": {
          "morning": [
            "Depart from Phoenix, AZ at 8:30 AM.",
            "Drive to San Diego, CA (approx. 5 hours).",
            "Check into a boutique hotel in the Gaslamp Quarter."
          ],
          "afternoon": [
            "Visit the San Diego Museum of Art.",
            "Explore Balboa Park, taking photos of the gardens."
          ],
          "evening": [
            "Dinner at an Italian restaurant in Little Italy.",
            "Watch the sunset at Sunset Cliffs."
          ]
        }
      },
      {
        "day": 2,
        "sections": {
          "morning": [
            "Visit the USS Midway Museum.",
            "Grab brunch at a local café."
          ],
          "afternoon": [
            "Spend the afternoon at SeaWorld San Diego.",
            "Enjoy various shows and attractions."
          ],
          "evening": [
            "Dinner at a Peruvian restaurant in Hillcrest.",
            "Stroll along the Embarcadero."
          ]
        }
      },
      {
        "day": 3,
        "sections": {
          "morning": [
            "Drive to Los Angeles (about 2 hours).",
            "Visit the Getty Center."
          ],
          "afternoon": [
            "Explore the Los Angeles County Museum of Art (LACMA).",
            "Take photos at the Urban Light installation."
          ],
          "evening": [
            "Dinner at a local Italian eatery.",
            "Relax at a scenic viewpoint overlooking the city."
          ]
        }
      },
      {
        "day": 4,
        "sections": {
          "morning": [
            "Spend the morning at Disneyland Park.",
            "Enjoy iconic rides and attractions."
          ],
          "afternoon": [
            "Lunch at the park.",
            "Continue exploring Disneyland."
          ],
          "evening": [
            "Dinner at a restaurant in Downtown Disney.",
            "Return to hotel for rest."
          ]
        }
      },
      {
        "day": 5,
        "sections": {
          "morning": [
            "Check out of the hotel.",
            "Visit the Ocean Institute in Dana Point."
          ],
          "afternoon": [
            "Drive back to Phoenix, AZ.",
            "Stop for lunch along the way."
          ],
          "evening": [
            "Arrive back in Phoenix around 7 PM.",
            "Celebrate the anniversary with a cozy dinner at home."
          ]
        }
      }
    ],
    "summary": "A packed 5-day itinerary exploring museums and amusement parks, featuring scenic views, delicious dining, and a romantic sunset, all while celebrating an anniversary."
  }
}
```

---

## Planned Improvements

- Improve itinerary accuracy and constraint handling
- Build frontend (question flow + itinerary view)
- Add PDF download from frontend
- Add sharing/export options

---

##  Running the Backend Locally

Do these commands in the terminal of your text editor:

```text
git clone https://github.com/yourusername/ai_trip_itinerary_generator.git
cd ai_trip_itinerary_generator

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a .env file with:

```text
OPENAI_API_KEY=your_api_key_here
```

**Important:** You need to have a working OpenAI API key to run the backend. To get an OpenAI API key, follow these four steps:

1. Log in or create an [OpenAI](https://auth.openai.com/log-in) account.
2. In order to have a working OpenAI API key, you need OpenAI credits. Go to the [billing page](https://platform.openai.com/settings/organization/billing/overview) to pay for credits. Calling OpenAI's API for the backend is very cheap; you can make several calls with just 1 cent! If you don't have any credits, I recommend you add $5, the minimum required amount on OpenAI.
3. Once you have the money, you can start making API calls. Add an API key on [this page](https://platform.openai.com/api-keys). Make sure to keep your key secret!
4. Copy and paste your secret key in the .env file (see above).

Start the server by using this command:

```text
uvicorn backend.main:app --reload
```

The app will be available at:

```text
http://127.0.0.1:8000/docs
```

Once you are at the URL above, follow these steps:

1. Click POST /generate-itinerary
2. Click Try it out
3. Paste a JSON request body (see example in this README)
4. Click Execute
5. Wait for the itinerary to appear!

Generated PDFs with the itinerary will appear in:

```text
generated_pdfs/
```