import os
from typing import Optional, List, Literal, Any, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI
from .itinerary_schema import get_itinerary_schema_prompt, parse_and_validate_itinerary

load_dotenv()

app = FastAPI(title="AI Trip Itinerary Generator")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- Models ----------

class TripContext(BaseModel):
    # =========================
    # Core mode
    # =========================
    trip_mode: str  # "discover" (Option A) or "known" (Option B)

    # =========================
    # Option A: destination discovery
    # =========================
    discovery_intent: Optional[str] = None  # Q2
    knows_trip_length: Optional[bool] = None  # Q3
    origin_location: Optional[str] = None  # Q7
    transport_mode: Optional[str] = None  # Q6
    international_travel: Optional[bool] = None  # Q8
    preferred_countries: Optional[List[str]] = None  # Q9
    distance_preference: Optional[str] = None  # Q10
    has_dates: Optional[bool] = None  # Q11
    date_range: Optional[str] = None  # Q12
    area_structure: Optional[str] = None  # Q15

    # =========================
    # Option B: known destination
    # =========================
    destination: Optional[str] = None  # B1

    # =========================
    # Shared / required
    # =========================
    days: Optional[int] = None  # A4 / B2
    people: Optional[int] = None  # A5 / B3

    has_time_constraints: Optional[bool] = None  # A13 / B4
    time_constraints_detail: Optional[str] = None  # A14 / B5

    # =========================
    # Budget
    # =========================
    budget_concern: Optional[bool] = None  # A16 / B6
    budget_amount: Optional[int] = None  # A17 / B7

    # =========================
    # Preferences
    # =========================
    weather_avoidance: Optional[List[str]] = None  # A18 / B9

    food_interest_level: Optional[int] = None  # A19 / B10
    cuisine_preferences: Optional[List[str]] = None  # A20 / B11

    shopping_interest_level: Optional[int] = None  # A21 / B12
    shopping_preferences: Optional[List[str]] = None  # A22 / B13

    trip_purpose: Optional[str] = None  # A23 / B14
    schedule_style: Optional[str] = None  # A24 / B15

    must_do: Optional[List[str]] = None  # A25 / B16
    must_avoid: Optional[List[str]] = None  # A26 / B17

    physical_activity_level: Optional[int] = None  # A27 / B18
    public_transit_comfort: Optional[int] = None  # A28 / B19

    nightlife: Optional[bool] = None  # A29 / B20
    photography_importance: Optional[int] = None  # A30 / B21

    desired_feelings: Optional[List[str]] = None  # A31 / B22
    rest_days: Optional[int] = None  # A32 / B23

    travel_vs_depth: Optional[str] = None  # A33 / B24

    excluded_places: Optional[List[str]] = None  # A34 / B25

    start_time_preference: Optional[str] = None  # A35 / B26
    end_time_preference: Optional[str] = None  # A36 / B27

    special_group_needs: Optional[List[str]] = None  # A37 / B28
    accessibility_needs: Optional[bool] = None  # A38 / B29

    additional_notes: Optional[str] = None  # A39 / B30

class TripResponse(BaseModel):
    itinerary: Dict[str, Any]

# ---------- Prompt ----------

def build_prompt(ctx: TripContext) -> str:
    if ctx.trip_mode == "discover":
        # =========================
        # Option A: destination discovery
        # =========================
        if ctx.international_travel is True:
            travel_scope = f"""
International travel: Yes
Preferred countries: {ctx.preferred_countries or "Not specified"}
"""
        elif ctx.international_travel is False:
            travel_scope = f"""
International travel: No
Preferred distance from origin: {ctx.distance_preference or "Not specified"}
"""
        else:
            travel_scope = """
International travel: Not specified
"""

        destination_block = f"""
Trip mode: Destination discovery (Option A)

User intent / desired experiences: {ctx.discovery_intent}
Current location (city, country): {ctx.origin_location}
Transportation mode to destination: {ctx.transport_mode or "Not specified"}
{travel_scope}
Has specific dates: {ctx.has_dates}
Date range (if known): {ctx.date_range or "Not specified"}

Planned trip structure (one area vs multiple areas): {ctx.area_structure or "Not specified"}
"""
    else:
        # =========================
        # Option B: known destination
        # =========================
        destination_block = f"""
Trip mode: Known destination (Option B)

Destination details (including dates if provided): {ctx.destination}
"""

    return f"""
You are an expert travel planner.

Create a realistic, practical, and well-paced itinerary using the information below.
All fields reflect explicit user answers. If a value is "Not specified",
make conservative assumptions and avoid over-optimizing.

{destination_block}

Trip length (days): {ctx.days or "Not specified"}
Number of people: {ctx.people}

Has strict time constraints: {ctx.has_time_constraints}
Time constraint details: {ctx.time_constraints_detail or "None"}

Budget sensitivity: {ctx.budget_concern}
Budget amount: {ctx.budget_amount or "Not specified"}

Weather conditions to avoid: {ctx.weather_avoidance or "Not specified"}

Food interest level (1–10): {ctx.food_interest_level or "Not specified"}
Cuisine preferences: {ctx.cuisine_preferences or "Not specified"}

Shopping interest level (1–10): {ctx.shopping_interest_level or "Not specified"}
Shopping preferences: {ctx.shopping_preferences or "Not specified"}

Main purpose of trip: {ctx.trip_purpose or "Not specified"}
Schedule style: {ctx.schedule_style or "Not specified"}

Must-do activities: {ctx.must_do or "None"}
Things to avoid: {ctx.must_avoid or "None"}

Physical activity level (1–10): {ctx.physical_activity_level or "Not specified"}

Public transportation comfort (1–10): {ctx.public_transit_comfort or "Not specified"}

Nightlife included: {ctx.nightlife}

Photography importance (1–10): {ctx.photography_importance or "Not specified"}

Desired feelings at end of trip: {ctx.desired_feelings or "Not specified"}

Number of rest days desired: {ctx.rest_days or "Not specified"}

Travel vs depth preference: {ctx.travel_vs_depth or "Not specified"}

Excluded places or attractions: {ctx.excluded_places or "None"}

Preferred daily start time: {ctx.start_time_preference or "Not specified"}
Preferred daily end time: {ctx.end_time_preference or "Not specified"}

Special group considerations: {ctx.special_group_needs or "None"}
Accessibility or mobility needs: {ctx.accessibility_needs}

Additional notes from user: {ctx.additional_notes or "None"}

Constraints and interpretation rules:

0) Contradictions and resolution policy (apply before planning)
- Treat user answers as constraints and preferences that can conflict.
- Never silently violate a hard constraint.
- If two hard constraints conflict, choose the safest, most conservative interpretation and explain it in 1–3 bullets under “Assumptions & conflict resolutions”.
- When a hard constraint conflicts with a soft preference, satisfy the hard constraint.
- When two soft preferences conflict, satisfy the higher-priority preference.

Conflict classes
A) Hard constraints
- Safety, accessibility, mobility limitations
- Strict time constraints
- Explicit exclusions and must-avoid lists
- Feasibility constraints: trip length, dates, distance, international feasibility, transportation feasibility

B) Strong preferences
- Numeric ratings 7–10

C) Moderate preferences
- Numeric ratings 4–6
- Schedule style (packed vs relaxed)

D) Weak preferences
- Numeric ratings 1–3 (minimize unless unavoidable)

1) Automatic contradiction detection rules

1.1 International vs domestic travel
- If international_travel = true, select destinations only from preferred_countries.
- If international_travel = false, select destinations only within distance_preference.
- If required information is missing, make conservative assumptions and note them.

1.2 Transport mode vs distance feasibility
- If transport_mode = driving and distance is very large, prefer closer destinations unless a road trip is explicitly implied.
- If multiple_areas is selected, longer driving distances may be interpreted as a road trip.

1.3 Dates vs trip length
- If both days and date_range are provided but conflict:
  - Treat date_range as authoritative.
  - Adjust planned days accordingly and note the adjustment.

1.4 Time constraints vs daily start/end preferences
- Always satisfy strict time constraints.
- Adjust daily structure and pacing as needed.

1.5 Nightlife vs daily timing
- If nightlife = true but late nights are constrained:
  - Interpret nightlife as early-evening social activity.
  - Mark late-night options as optional.

1.6 Rest days vs packed schedule
- If rest_days is high relative to trip length:
  - Treat rest_days as a hard constraint.
  - Pack only non-rest days.

1.7 Physical activity vs accessibility
- Accessibility always overrides physical activity level.
- Offer accessible alternatives when needed.

1.8 Budget vs must-do
- Must-do items take priority.
- Offset cost elsewhere when budget is constrained.

1.9 Weather avoidance vs dates
- Treat dates as authoritative.
- Choose destinations and activities that minimize exposure to avoided weather.

2) General structure
- Break each day into Morning, Afternoon, Evening.
- Keep pacing realistic.
- Avoid places the user explicitly wants to avoid.
- Make conservative assumptions when information is missing.

3) Preference priority order
1. Safety, accessibility, strict time constraints
2. Explicit exclusions and feasibility constraints
3. Must-do items
4. Strong numeric preferences (7–10)
5. Moderate numeric preferences (4–6) and schedule style
6. Logistics (meals, transit, rest)
7. Weak numeric preferences (1–3)

4) Numeric preference interpretation
- 1–3: minimize
- 4–6: include selectively
- 7–10: central theme

Apply numeric interpretation for:
- food interest
- shopping interest
- physical activity
- photography

Note:
- Nightlife is boolean; treat as moderate when true.

5) Food and dining
- Low interest: meals are logistical.
- Moderate/high interest: include proportionally.

6) Transportation
- Match activity density to physical activity level.
- Favor walkable clusters when possible.

7) Accuracy and realism
- Only suggest real, publicly accessible places.
- Never invent venue names.
- Keep descriptions practical.

8) Output requirements
- Include “Assumptions & conflict resolutions” only if needed.
- Use 1–3 concise bullets.

Format:
Day 1:
Morning:
Afternoon:
Evening:
""".strip()

# ---------- Endpoint ----------

@app.post("/generate-itinerary", response_model=TripResponse)
def generate_itinerary(ctx: TripContext):
    # =========================
    # Trip mode validation
    # =========================
    if ctx.trip_mode not in {"discover", "known"}:
        raise HTTPException(400, "trip_mode must be 'discover' or 'known'")

    # =========================
    # Option B: known destination
    # =========================
    if ctx.trip_mode == "known":
        if not ctx.destination:
            raise HTTPException(400, "destination is required for trip_mode='known'")
        if ctx.days is None:
            raise HTTPException(400, "days is required for trip_mode='known'")
        if ctx.people is None:
            raise HTTPException(400, "people is required for trip_mode='known'")

    # =========================
    # Option A: discovery
    # =========================
    if ctx.trip_mode == "discover":
        if not ctx.discovery_intent:
            raise HTTPException(400, "discovery_intent is required for trip_mode='discover'")
        if not ctx.origin_location:
            raise HTTPException(400, "origin_location is required for trip_mode='discover'")
        if ctx.people is None:
            raise HTTPException(400, "people is required for trip_mode='discover'")

        # Trip length logic
        if ctx.knows_trip_length:
            if ctx.days is None:
                raise HTTPException(400, "days is required when knows_trip_length is true")
        else:
            if not (ctx.has_dates and ctx.date_range):
                raise HTTPException(
                    400,
                    "Either days or a valid date_range must be provided"
                )

        # International vs distance (mutually exclusive)
        if ctx.international_travel is None:
            raise HTTPException(400, "international_travel is required")

        if ctx.international_travel:
            if not ctx.preferred_countries:
                raise HTTPException(
                    400,
                    "preferred_countries is required when international_travel is true"
                )
            if ctx.distance_preference is not None:
                raise HTTPException(
                    400,
                    "distance_preference must not be provided when international_travel is true"
                )
        else:
            if ctx.distance_preference is None:
                raise HTTPException(
                    400,
                    "distance_preference is required when international_travel is false"
                )
            if ctx.preferred_countries:
                raise HTTPException(
                    400,
                    "preferred_countries must not be provided when international_travel is false"
                )

    # =========================
    # Time constraints (shared)
    # =========================
    if ctx.has_time_constraints and not ctx.time_constraints_detail:
        raise HTTPException(
            400,
            "time_constraints_detail is required when has_time_constraints is true"
        )

    # =========================
    # Budget dependency
    # =========================
    if ctx.budget_amount is not None and not ctx.budget_concern:
        raise HTTPException(
            400,
            "budget_amount should not be provided when budget_concern is false"
        )

    # =========================
    # Prompt + model call
    # =========================
    prompt = build_prompt(ctx) + "\n\n" + get_itinerary_schema_prompt()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate realistic, practical travel itineraries."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=1200,
    )

    raw_output = completion.choices[0].message.content

    validated_itinerary = parse_and_validate_itinerary(raw_output)

    return TripResponse(itinerary=validated_itinerary)