# AI Trip Itinerary Generator

An AI-powered travel itinerary generator that creates **realistic, preference-aware itineraries** by asking users structured, constraint-first questions.

Unlike generic AI travel planners, this project is designed to reduce hallucinations, avoid rushed schedules, and respect uncertainty by explicitly separating **hard constraints** from **soft preferences**.

---

## Project Status

**In active development.**

- Backend logic is partially implemented and functional
- Both trip modes (discover + known destination) work end-to-end
- Generated itineraries are realistic, paced, and preference-aware
- Frontend has not been implemented yet
- Output structure and validation are still evolving

The current focus is **backend correctness, question design, and itinerary quality**, not UI polish.

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
├── backend/        # Backend logic (in progress)
├── frontend/       # Frontend (not implemented yet)
├── .env            # Environment variables (ignored)
├── .gitignore
└── README.md
```

---

## Current Capabilities

- Two fully defined trip modes (discover + known)
- Structured constraint and preference capture
- Preference-aware itinerary generation
- Support for:
  - Time constraints
  - Rest days
  - Activity level
  - Accessibility considerations
  - Early/late schedule preferences
- Outputs realistic, named locations and coherent daily flow

---

## Sample JSON Request (Discover Mode)

```text
{
  "trip_mode": "discover",

  "discovery_intent": "I want a relaxing trip with nature, scenic views, and some light walking. I want to feel refreshed, not rushed.",
  "knows_trip_length": true,
  "days": 4,

  "people": 2,

  "origin_location": "San Francisco, United States",
  "transport_mode": "driving",

  "international_travel": false,
  "distance_preference": "50–100 miles",
  "preferred_countries": null,

  "has_dates": false,
  "date_range": null,

  "area_structure": "multiple_areas",

  "has_time_constraints": false,
  "time_constraints_detail": null,

  "budget_concern": true,
  "budget_amount": 1500,

  "weather_avoidance": ["heavy rain", "extreme heat"],

  "food_interest_level": 6,
  "cuisine_preferences": ["seafood", "local cuisine"],

  "shopping_interest_level": 2,
  "shopping_preferences": null,

  "trip_purpose": "Rest, recharge, and enjoy beautiful surroundings",
  "schedule_style": "relaxed",

  "must_do": ["Spend time near the coast", "Watch sunsets"],
  "must_avoid": ["Crowded nightlife areas", "Overly touristy attractions"],

  "physical_activity_level": 4,
  "public_transit_comfort": 3,

  "nightlife": false,

  "photography_importance": 5,

  "desired_feelings": ["relaxed", "refreshed"],

  "rest_days": 1,

  "travel_vs_depth": "fewer_places",

  "excluded_places": ["Las Vegas"],

  "start_time_preference": "midday",
  "end_time_preference": "early",

  "special_group_needs": [],
  "accessibility_needs": false,

  "additional_notes": "Please keep the pace flexible and avoid long drives between locations."
}
```

---

## Sample Output (Generated Itinerary)

```text
{
  "itinerary": "### Itinerary for a Relaxing Nature-Focused Trip from San Francisco\n\n**Trip Length:** 4 days  \n**Travel Mode:** Driving  \n**Budget:** $1500  \n**Number of People:** 2\n\n---\n\n### Day 1: Arrival in Monterey\n\n**Morning:**  \n- Depart from San Francisco around midday.  \n- Drive to Monterey (approximately 2 hours).  \n- Check into a cozy hotel or Airbnb with ocean views (suggested area: Cannery Row).\n\n**Afternoon:**  \n- Lunch at a local seafood restaurant on Cannery Row (e.g., Cannery Row Brewing Company).  \n- Explore the Monterey Bay Aquarium (entry fee approximately $50 per person).  \n- Stroll along Cannery Row and enjoy the scenic coastal views.\n\n**Evening:**  \n- Dinner at a seafood restaurant (e.g., The Fish Hopper) with views of the sunset over the ocean.  \n- Enjoy the sunset at Lovers Point Park.\n\n---\n\n### Day 2: Scenic Drive and Coastal Relaxation\n\n**Morning:**  \n- Breakfast at a local café (e.g., First Awakenings).  \n- Drive along the scenic 17-Mile Drive, stopping at iconic viewpoints (e.g., The Lone Cypress, Spanish Bay).\n\n**Afternoon:**  \n- Picnic lunch at one of the scenic stops along the drive or at Pebble Beach.  \n- Light walking at Point Lobos State Natural Reserve; enjoy the coastal trails and beautiful ocean views (entry fee around $10 per vehicle).\n\n**Evening:**  \n- Dinner at a local restaurant in Carmel-by-the-Sea (e.g., La Bicyclette).  \n- Relax at the beach and watch the sunset.\n\n---\n\n### Day 3: Day Trip to Big Sur\n\n**Morning:**  \n- Breakfast at your accommodation or a local café.  \n- Depart for Big Sur (about a 30-minute drive).  \n- Visit McWay Falls in Julia Pfeiffer Burns State Park (entry fee included in state park fee).\n\n**Afternoon:**  \n- Light walking along the trails with stunning ocean views.  \n- Lunch at a roadside café (e.g., Big Sur River Inn).  \n- Visit Pfeiffer Beach; enjoy the unique purple sand and striking rock formations.\n\n**Evening:**  \n- Return to Monterey or Carmel for dinner (suggested: The Wharf Marketplace for casual dining).  \n- Enjoy a leisurely evening stroll along the coastline.\n\n---\n\n### Day 4: Relaxation and Departure\n\n**Morning:**  \n- Breakfast at a local bakery (e.g., Parker-Lusseau Pastries).  \n- Visit the nearby Carmel Mission or enjoy a final walk on Carmel Beach.\n\n**Afternoon:**  \n- Light lunch in Carmel-by-the-Sea.  \n- Depart back to San Francisco, stopping at scenic viewpoints along the way.\n\n**Evening:**  \n- Arrive back in San Francisco by early evening, concluding your relaxing trip.\n\n---\n\n### Key Notes:\n- **Weather Consideration:** With a focus on avoiding heavy rain and extreme heat, the coastal areas are generally mild, but check forecasts before departure.\n- **Budget Management:** Opt for moderate dining options and consider picnics to maintain budget while still enjoying local cuisine. \n- **Relaxed Pace:** Each day allows for leisurely exploration without rushing, fitting your desire for a restful getaway."
}
```

---

## Planned Improvements

- Finalize backend constraint normalization
- Improve output structure consistency
- Add **PDF itinerary export (backend)**
- Build minimal frontend (question flow + itinerary view)
- Add export and sharing options

---

## Important Note

Frontend work will begin after backend behavior stabilizes.