import os
from typing import Optional, List, Literal, Any, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI
from .itinerary_schema import get_itinerary_schema_prompt, parse_and_validate_itinerary
from .pdf_generator import generate_itinerary_pdf
from datetime import datetime

load_dotenv()

app = FastAPI(title="AI Trip Itinerary Generator")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- Models ----------

from pydantic import BaseModel
from typing import List, Optional

class TripContext(BaseModel):

    # =========================
    # Core mode
    # =========================
    trip_mode: str  # "discover" (Option A) or "known" (Option B)

    # =====================================================
    # ================= OPTION A (DISCOVER) ===============
    # =====================================================

    # Required
    has_discovery_intent: bool  # Q1
    discovery_intent: Optional[str] = None  # Q2 (only if has_discovery_intent=True)

    knows_trip_length: bool  # Q3
    days: Optional[int] = None  # Q4 (required if knows_trip_length=True)

    people: int  # Q5
    transport_mode: str  # Q6
    origin_location: str  # Q7

    international_travel: bool  # Q8
    preferred_countries: Optional[List[str]] = None  # Q9
    distance_preference: Optional[str] = None  # Q10

    has_dates: bool  # Q11
    date_range: Optional[str] = None  # Q12

    has_time_constraints: bool  # Q13
    time_constraints_detail: Optional[str] = None  # Q14

    area_structure: str  # Q15

    special_group_needs: List[str]  # Q16
    accessibility_needs: bool  # Q17
    accessibility_details: Optional[str] = None  # Q18

    # =====================================================
    # ================= OPTION B (KNOWN) ==================
    # =====================================================

    destination: Optional[str] = None  # B1

    knows_trip_length_b: Optional[bool] = None  # B2
    days_b: Optional[int] = None  # B3
    people_b: Optional[int] = None  # B4

    # =====================================================
    # ================= OPTIONAL SHARED ===================
    # =====================================================

    budget_concern: Optional[bool] = None  # Q19 / B10
    budget_amount: Optional[int] = None  # Q20 / B11

    weather_avoidance: Optional[List[str]] = None  # Q21 / B12

    interests: Optional[str] = None  # Q22 / B13

    food_interest_level: Optional[int] = None  # Q23 / B14
    cuisine_preferences: Optional[List[str]] = None  # Q24 / B15
    cuisine_preferences_other_text: Optional[str] = None

    shopping_interest_level: Optional[int] = None  # Q25 / B16
    shopping_preferences: Optional[List[str]] = None  # Q26 / B17
    shopping_preferences_other_text: Optional[str] = None

    trip_purpose: Optional[str] = None  # Q27 / B18
    schedule_style: Optional[str] = None  # Q28 / B19

    must_do: Optional[List[str]] = None  # Q29 / B20
    must_avoid: Optional[List[str]] = None  # Q30 / B21

    physical_activity_level: Optional[int] = None  # Q31 / B22
    public_transit_comfort: Optional[int] = None  # Q32 / B23

    nightlife: Optional[bool] = None  # Q33 / B24
    photography_importance: Optional[int] = None  # Q34 / B25

    desired_feelings: Optional[List[str]] = None  # Q35 / B26

    travel_vs_depth: Optional[str] = None  # Q36 / B27

    excluded_places: Optional[List[str]] = None  # Q37 / B28

    start_time_preference: Optional[str] = None  # Q38 / B29
    start_time_other_text: Optional[str] = None

    end_time_preference: Optional[str] = None  # Q39 / B30
    end_time_other_text: Optional[str] = None

    additional_notes: Optional[str] = None  # Q40 / B31

class TripResponse(BaseModel):
    itinerary: Dict[str, Any]

# ---------- Prompt ----------

def build_prompt(ctx: TripContext) -> str:

    # ==========================================
    # Handle "Other" fields cleanly
    # ==========================================

    cuisine_display = ctx.cuisine_preferences or "Not specified"
    if ctx.cuisine_preferences and "Other" in ctx.cuisine_preferences:
        cuisine_display = [
            c for c in ctx.cuisine_preferences if c != "Other"
        ]
        if ctx.cuisine_preferences_other_text:
            cuisine_display.append(f"Other: {ctx.cuisine_preferences_other_text}")

    shopping_display = ctx.shopping_preferences or "Not specified"
    if ctx.shopping_preferences and "Other" in ctx.shopping_preferences:
        shopping_display = [
            s for s in ctx.shopping_preferences if s != "Other"
        ]
        if ctx.shopping_preferences_other_text:
            shopping_display.append(f"Other: {ctx.shopping_preferences_other_text}")

    start_time_display = ctx.start_time_preference
    if ctx.start_time_preference == "Other" and ctx.start_time_other_text:
        start_time_display = ctx.start_time_other_text

    end_time_display = ctx.end_time_preference
    if ctx.end_time_preference == "Other" and ctx.end_time_other_text:
        end_time_display = ctx.end_time_other_text

    # ==========================================
    # Destination Block
    # ==========================================

    if ctx.trip_mode == "discover":

        if ctx.international_travel is True:
            travel_scope = f"""
International travel: Yes
Preferred countries: {ctx.preferred_countries or "Not specified"}
"""
        else:
            travel_scope = f"""
International travel: No
Preferred distance from origin: {ctx.distance_preference or "Not specified"}
"""

        destination_block = f"""
Trip mode: Destination discovery (Option A)

User has specific intent: {ctx.has_discovery_intent}
User intent / desired experiences: {ctx.discovery_intent or "Not specified"}

Current location (city, country): {ctx.origin_location}
Transportation mode to destination: {ctx.transport_mode}

{travel_scope}

Has specific dates: {ctx.has_dates}
Date range (if known): {ctx.date_range or "Not specified"}

Planned trip structure (one area vs multiple areas): {ctx.area_structure}
"""

    else:
        destination_block = f"""
Trip mode: Known destination (Option B)

Destination details (including dates if provided): {ctx.destination}
"""

    # ==========================================
    # Main Prompt Body
    # ==========================================

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

Special group considerations: {ctx.special_group_needs}
Accessibility needs: {ctx.accessibility_needs}
Accessibility details: {ctx.accessibility_details or "None"}

Budget sensitivity: {ctx.budget_concern}
Budget amount: {ctx.budget_amount or "Not specified"}

Weather conditions to avoid: {ctx.weather_avoidance or "Not specified"}

General interests: {ctx.interests or "Not specified"}

Food interest level (1–10): {ctx.food_interest_level or "Not specified"}
Cuisine preferences: {cuisine_display}

Shopping interest level (1–10): {ctx.shopping_interest_level or "Not specified"}
Shopping preferences: {shopping_display}

Main purpose of trip: {ctx.trip_purpose or "Not specified"}
Schedule style: {ctx.schedule_style or "Not specified"}

Must-do activities: {ctx.must_do or "None"}
Things to avoid: {ctx.must_avoid or "None"}

Physical activity level (1–10): {ctx.physical_activity_level or "Not specified"}

Public transportation comfort (1–10): {ctx.public_transit_comfort or "Not specified"}

Nightlife included: {ctx.nightlife}

Photography importance (1–10): {ctx.photography_importance or "Not specified"}

Desired feelings at end of trip: {ctx.desired_feelings or "Not specified"}

Travel vs depth preference: {ctx.travel_vs_depth or "Not specified"}

Excluded places or attractions: {ctx.excluded_places or "None"}

Preferred daily start time: {start_time_display or "Not specified"}
Preferred daily end time: {end_time_display or "Not specified"}

Additional notes from user: {ctx.additional_notes or "None"}

Constraints and interpretation rules:

0) Core Planning Philosophy
- Treat user inputs as structured signals with varying strength.
- Convert all inputs into operational planning constraints before generating the itinerary.
- Do not improvise beyond user tolerance levels.
- Do not optimize aggressively when information is incomplete.
- When in doubt, choose the more conservative, feasible, and lower-risk option.

------------------------------------------------------------
1) Conflict Resolution Framework (Apply BEFORE planning)
------------------------------------------------------------

1.1 Classification of input signals

A) Hard constraints (never violate)
- Safety concerns
- Accessibility and mobility limitations
- Strict time constraints
- Explicit exclusions / must-avoid
- Trip length (days)
- Date range
- Transportation feasibility
- International feasibility (passport/distance restrictions)

B) Strong preferences
- Numeric ratings 7–10
- Explicit must-do items
- Schedule style when explicitly chosen

C) Moderate preferences
- Numeric ratings 4–6
- Travel vs depth preference
- Public transit comfort

D) Weak preferences
- Numeric ratings 1–3
- Secondary optional interests

1.2 Conflict resolution rules

- Never silently violate a hard constraint.
- If two hard constraints conflict, choose the safest and most conservative interpretation and explain in 1–3 bullets under:
  "Assumptions & conflict resolutions".
- When a hard constraint conflicts with a preference, satisfy the hard constraint.
- When two preferences conflict:
  - Satisfy the stronger signal (based on classification above).
  - If equal strength, choose the option that improves feasibility and reduces risk.
- Do not exaggerate fulfillment of low-priority signals.

------------------------------------------------------------
2) Automatic Feasibility & Consistency Checks
------------------------------------------------------------

2.1 International vs domestic logic
- If international_travel = true:
  - Select only destinations from preferred_countries.
  - Do not assume visa feasibility beyond user indication.
- If international_travel = false:
  - Select only destinations within stated distance_preference.
- If origin_location is provided:
  - Ensure travel feasibility given transport_mode.

2.2 Transport mode vs geography
- Driving:
  - Avoid unrealistic long-distance drives unless multi-area road trip implied.
- Flying:
  - Allow larger distance but cluster activities geographically within each destination.
- Train / bus:
  - Prefer urban corridors with strong public transit.
- Cruise/ferry:
  - Anchor itinerary around port-based exploration.

2.3 Dates vs trip length
- If both days and date_range exist and conflict:
  - Treat date_range as authoritative.
  - Adjust effective day count.
  - Note adjustment briefly.
- Do not compress unrealistic number of cities into short duration.

2.4 Time constraints vs daily structure
- Strict time constraints override all scheduling preferences.
- Build the day around fixed events.
- Adjust activity density accordingly.
- Do not stack unrealistic activities near fixed windows.

2.5 Nightlife vs timing
- If nightlife = true:
  - Include evening social experiences.
- If early end_time_preference conflicts:
  - Interpret nightlife as early-evening (dinner, wine bar, performance).
- Never force late-night if timing constraints contradict.

2.6 Physical activity vs accessibility
- Accessibility always overrides activity intensity.
- If physical_activity_level is high but accessibility_needs = true:
  - Provide accessible alternatives with similar experience.
- Do not include steep hikes, long walking loops, or high exertion unless physically feasible.

2.7 Budget vs must-do
- Must-do items take priority.
- If budget_concern = true:
  - Reduce cost in lodging, dining, or secondary activities.
  - Avoid premium-only experiences unless essential.
- Do not fabricate unrealistic “budget luxury.”

2.8 Weather avoidance vs dates
- Dates are authoritative.
- Choose locations and indoor/outdoor mix to minimize exposure to avoided weather types.
- Do not contradict explicit weather avoidance.

2.9 Travel vs depth
- “More time traveling”:
  - Increase geographic diversity.
  - Accept higher transit time.
- “More time in fewer places”:
  - Deepen neighborhood-level exploration.
  - Reduce intercity transfers.
- “Somewhere in between”:
  - Moderate balance.

------------------------------------------------------------
3) Pacing & Density Algorithm
------------------------------------------------------------

3.1 Schedule style interpretation

If schedule_style = Packed:
- 3–4 substantial activities per day.
- Short transitions.
- Limited downtime.

If schedule_style = Relaxed:
- 1–2 anchor activities per day.
- Built-in buffer periods.
- Flexible afternoons.

If “Somewhere in between”:
- 2–3 structured activities per day.

3.2 Physical activity scaling
- 1–3: Mostly seated, scenic, or transit-based activities.
- 4–6: Moderate walking, short exploration blocks.
- 7–10: Active exploration, longer walks, outdoor components.

3.3 Public transportation comfort
- 1–3: Minimize transfers; prioritize compact geography.
- 4–6: Moderate transit usage.
- 7–10: Multi-stop public transit acceptable.

3.4 Activity clustering
- Minimize backtracking.
- Group geographically adjacent attractions.
- Avoid unrealistic commute assumptions.

------------------------------------------------------------
4) Numeric Preference Interpretation
------------------------------------------------------------

For:
- food_interest_level
- shopping_interest_level
- physical_activity_level
- photography_importance

Interpret as:

1–3:
- Include minimally.
- Do not make central theme.

4–6:
- Integrate selectively.
- Secondary but visible.

7–10:
- Make central to itinerary design.
- Allocate prime time blocks.

------------------------------------------------------------
5) Food & Dining Logic
------------------------------------------------------------

Low food interest:
- Meals serve logistical function.
- No long tasting menus.

Moderate:
- Include 1 notable dining experience.

High:
- Include destination-appropriate restaurants.
- Balance cost with budget sensitivity.
- Avoid unrealistic reservation difficulty unless noted.

------------------------------------------------------------
6) Accuracy & Realism Requirements
------------------------------------------------------------

- Only suggest real, publicly accessible locations.
- Never invent venues.
- Do not fabricate obscure attractions.
- Avoid private or restricted-access locations.
- Avoid over-precise logistics (no fake addresses or times).
- Avoid assuming impossible ticket availability.

------------------------------------------------------------
7) Output Structure Rules
------------------------------------------------------------

- Break each day into:
  Morning
  Afternoon
  Evening

- Keep daily blocks realistic.
- Do not overfill.
- Respect start_time_preference and end_time_preference.
- Respect time constraints first.

Include “Assumptions & conflict resolutions” ONLY if:
- You adjusted for conflicting constraints.
- You made conservative assumptions due to missing data.


------------------------------------------------------------
8) Itinerary Quality & Polish Rules
------------------------------------------------------------

8.1 Structural completeness
- Every day must include Morning, Afternoon, and Evening.
- No section may be empty.
- If returning home mid-day:
  - Include a meaningful closing experience (e.g., farewell meal, scenic stop, relaxed wind-down).
- The final day should feel intentional, not truncated.

8.2 Thematic consistency
- Identify the dominant trip theme based on strongest preferences:
  - Photography ≥ 7 → scenic framing & golden-hour moments
  - Food ≥ 7 → curated dining moments
  - Relaxed schedule → breathing space
  - Anniversary / romantic purpose → elevated tone
- Each day must visibly reflect the dominant theme.

8.3 Personalization reinforcement
- If trip_purpose is specified:
  - Reinforce it subtly each day.
- Anniversary:
  - Include at least one elevated romantic moment.
- Family:
  - Include balance and recovery pacing.
- Solo:
  - Allow flexibility and exploration.

8.4 Experience progression
- Days should feel like a narrative arc:
  - Day 1: Orientation & arrival ease
  - Middle days: Peak experiences
  - Final day: Closure & reflection
- Avoid repetitive daily structure.

8.5 Geographic intelligence
- Minimize backtracking.
- Cluster nearby activities.
- Avoid unrealistic transfer assumptions.
- Avoid unnecessary long drives for short stops.

8.6 Activity density refinement
- Do not exceed:
  - 4 major activities per day (packed)
  - 3 moderate activities (balanced)
  - 2 anchor activities (relaxed)
- Avoid stacking high-energy activities back-to-back.

8.7 Highlighted moments
- Include at least one “memorable highlight” per 2 days.
- Highlights may include:
  - Scenic overlook
  - Unique dining experience
  - Cultural immersion
  - Landmark moment

8.8 Budget realism
If budget_concern = true:
- Avoid premium-only venues.
- Balance one premium activity with lower-cost options.
- Avoid unrealistic luxury density.

8.9 Time-window enforcement
- Respect start_time_preference and end_time_preference.
- Do not schedule evening activity past end_time_preference.
- Honor strict time constraints explicitly.

8.10 Tone control
- Avoid generic phrasing.
- Keep descriptions concise but purposeful.
- Avoid filler language like “enjoy some time” without context.

------------------------------------------------------------
9) Elite Refinement & Coherence Layer (Apply Before Output)
------------------------------------------------------------

9.1 Dominant Theme Reinforcement

Identify the dominant theme based on strongest signals:
- trip_purpose (e.g., anniversary, family, solo exploration)
- Highest numeric preference ≥ 8
- Explicit emotional goals in desired_feelings

Rules:
- The dominant theme must visibly influence at least one major block per day.
- Do not let the itinerary feel generic.
- If anniversary or romantic purpose:
  - Include at least one elevated or intimate moment.
  - Include at least one sunset or scenic framing moment.
  - Include at least one thoughtfully chosen dinner.
- If photography importance ≥ 8:
  - Explicitly schedule golden-hour or scenic vantage points.
- If food interest ≥ 8:
  - Include at least one curated or destination-defining dining experience.

9.2 Budget Visibility Enforcement

If budget_concern = true:
- Demonstrate visible cost balancing.
- At most one premium-style experience every 2 days.
- Balance higher-cost dinners with casual lunches.
- Avoid unrealistic luxury density.
- Do not assume unlimited ticket access or premium tours.

The itinerary must subtly reflect cost awareness.

9.3 Travel vs Depth Enforcement

If travel_vs_depth = "More time in fewer places":
- Limit lodging changes.
- Base in 1–2 primary towns maximum.
- Use short day trips instead of full relocations.

If travel_vs_depth = "More time traveling":
- Allow multi-city flow.
- Accept higher transit frequency.

If "Somewhere in between":
- Moderate transitions.

9.4 Hard Constraint Anchoring

If strict time constraints exist:
- Explicitly anchor them in the correct day block.
- Show buffer time before and after.
- Do not bury them implicitly.

9.5 Final Day Integrity Rule

The final day must:
- Feel intentional and complete.
- Include a closing or reflective moment.
- Not feel abruptly truncated.

If returning home early:
- Include a light but meaningful closing activity.

9.6 Structural Self-Check (Internal)

Before finalizing:
- Check that no Morning/Afternoon/Evening section is empty.
- Check for geographic inefficiency.
- Check for hard constraint violations.
- Check that dominant theme appears visibly.
- Revise internally if needed before output.

------------------------------------------------------------
FORMAT:

Day 1:
Morning:
Afternoon:
Evening:
""".strip()

# ---------- Endpoint ----------

@app.post("/generate-itinerary", response_model=TripResponse)
def generate_itinerary(ctx: TripContext):

    # =====================================================
    # 1) Trip mode validation
    # =====================================================
    if ctx.trip_mode not in {"discover", "known"}:
        raise HTTPException(400, "trip_mode must be 'discover' or 'known'")

    # =====================================================
    # 2) Shared required fields (both modes)
    # =====================================================
    if ctx.people is None:
        raise HTTPException(400, "people is required")

    if ctx.has_time_constraints and not ctx.time_constraints_detail:
        raise HTTPException(
            400,
            "time_constraints_detail is required when has_time_constraints is true"
        )

    if ctx.accessibility_needs and not ctx.accessibility_details:
        raise HTTPException(
            400,
            "accessibility_details is required when accessibility_needs is true"
        )

    if ctx.budget_amount is not None and not ctx.budget_concern:
        raise HTTPException(
            400,
            "budget_amount must not be provided when budget_concern is false"
        )

    # =====================================================
    # 3) Option B: known destination
    # =====================================================
    if ctx.trip_mode == "known":

        if not ctx.destination:
            raise HTTPException(400, "destination is required for trip_mode='known'")

        if ctx.days is None:
            raise HTTPException(400, "days is required for trip_mode='known'")

    # =====================================================
    # 4) Option A: destination discovery
    # =====================================================
    if ctx.trip_mode == "discover":

        # Required discovery logic
        if ctx.has_discovery_intent and not ctx.discovery_intent:
            raise HTTPException(
                400,
                "discovery_intent is required when has_discovery_intent is true"
            )

        if not ctx.origin_location:
            raise HTTPException(400, "origin_location is required")

        if ctx.knows_trip_length:
            if ctx.days is None:
                raise HTTPException(
                    400,
                    "days is required when knows_trip_length is true"
                )
        else:
            if not (ctx.has_dates and ctx.date_range):
                raise HTTPException(
                    400,
                    "Either days or a valid date_range must be provided"
                )

        # International vs domestic logic
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

    # =====================================================
    # 5) "Other" field enforcement
    # =====================================================
    if ctx.cuisine_preferences and "Other" in ctx.cuisine_preferences:
        if not ctx.cuisine_preferences_other_text:
            raise HTTPException(
                400,
                "cuisine_preferences_other_text is required when 'Other' is selected"
            )

    if ctx.shopping_preferences and "Other" in ctx.shopping_preferences:
        if not ctx.shopping_preferences_other_text:
            raise HTTPException(
                400,
                "shopping_preferences_other_text is required when 'Other' is selected"
            )

    if ctx.start_time_preference == "Other" and not ctx.start_time_other_text:
        raise HTTPException(
            400,
            "start_time_other_text is required when start_time_preference is 'Other'"
        )

    if ctx.end_time_preference == "Other" and not ctx.end_time_other_text:
        raise HTTPException(
            400,
            "end_time_other_text is required when end_time_preference is 'Other'"
        )

    # =====================================================
    # 6) Numeric range validation
    # =====================================================
    def validate_range(value, min_val, max_val, field_name):
        if value is None:
            return
        if not (min_val <= value <= max_val):
            raise HTTPException(
                400,
                f"{field_name} must be between {min_val} and {max_val}"
            )

    validate_range(ctx.days, 1, 30, "days")
    validate_range(ctx.food_interest_level, 1, 10, "food_interest_level")
    validate_range(ctx.shopping_interest_level, 1, 10, "shopping_interest_level")
    validate_range(ctx.physical_activity_level, 1, 10, "physical_activity_level")
    validate_range(ctx.public_transit_comfort, 1, 10, "public_transit_comfort")
    validate_range(ctx.photography_importance, 1, 10, "photography_importance")

    # =====================================================
    # 7) Prompt + Model Call
    # =====================================================
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

    # -----------------------------------------------------
    # PDF generation layer
    # -----------------------------------------------------
    os.makedirs("generated_pdfs", exist_ok=True)

    timestamp = datetime.now().strftime("%m_%d_%Y_%H%M%S")
    pdf_path = f"generated_pdfs/itinerary_{timestamp}.pdf"

    generate_itinerary_pdf(
        validated_itinerary,
        pdf_path
    )

    return TripResponse(itinerary=validated_itinerary)