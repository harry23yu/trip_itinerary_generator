import os
from typing import Optional, List, Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from .itinerary_schema import get_itinerary_schema_prompt, parse_and_validate_itinerary
from .pdf_generator import generate_itinerary_pdf
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="AI Trip Itinerary Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- Models ----------

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

    # NOTE: people is a string because the frontend sends values like "3-4",
    # "15 or more", "Not sure yet". Do not type as int.
    people: Optional[Any] = None  # Q5
    transport_mode: str  # Q6
    origin_location: str  # Q7

    international_travel: bool  # Q8
    preferred_countries: Optional[str] = None  # Q9
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
    # Same as people: string values like "3-4", "Not sure yet"
    people_b: Optional[Any] = None  # B4

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
    pdf_path: Optional[str] = None

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

    # Resolve people and days for both modes
    people_display = ctx.people if ctx.trip_mode == "discover" else (ctx.people_b or ctx.people)
    days_display = ctx.days if ctx.trip_mode == "discover" else (ctx.days_b or ctx.days)

    # ==========================================
    # Main Prompt Body
    # ==========================================

    return f"""
You are an expert travel planner.

Create a realistic, practical, and well-paced itinerary using the information below.
All fields reflect explicit user answers. If a value is "Not specified",
make conservative assumptions and avoid over-optimizing.

{destination_block}

Trip length (days): {days_display or "Not specified"}
Number of people: {people_display or "Not specified"}

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

Trip purpose: {ctx.trip_purpose or "Not specified"}
Schedule style (packed/relaxed): {ctx.schedule_style or "Not specified"}

Must-do activities: {ctx.must_do or "Not specified"}
Must-avoid activities: {ctx.must_avoid or "Not specified"}

Physical activity level (1–10): {ctx.physical_activity_level or "Not specified"}
Public transit comfort (1–10): {ctx.public_transit_comfort or "Not specified"}

Nightlife desired: {ctx.nightlife}
Photography importance (1–10): {ctx.photography_importance or "Not specified"}

Desired feelings at end of trip: {ctx.desired_feelings or "Not specified"}

Travel vs depth preference: {ctx.travel_vs_depth or "Not specified"}
Excluded places: {ctx.excluded_places or "None"}

Preferred daily start time: {start_time_display or "Not specified"}
Preferred daily end time: {end_time_display or "Not specified"}

Additional notes: {ctx.additional_notes or "None"}

------------------------------------------------------------
PLANNING RULES:

1. Trip Length Inference
If days is "Not specified" but a date range is given, calculate the number of days from it. For example, 6/22-6/27 includes 6/22, 6/23, 6/24, 6/25, 6/26, and 6/27, which is equal to 6 days.
If neither is available, default to 5 days.

2. Group Size Adaptation
- "1": solo traveler — prioritize safety, flexibility, social opportunities
- "2": couple or pair — balance shared and individual interests
- "3-4": small group — coordinate logistics, allow for some splitting
- "5-6" or more: larger group — prioritize accessible, high-capacity venues
- "Not sure yet": plan for 2 as a safe default

3. Budget Handling
If budget_concern is True and budget_amount is given, keep recommendations within budget.
If budget_concern is True but no amount, lean toward mid-range options.
If budget_concern is False or null, do not restrict choices by cost.

4. Time Constraints
If has_time_constraints is True, anchor those windows in the correct day blocks.
Leave buffer before and after constraint windows.

5. Accessibility
If accessibility_needs is True, avoid activities with significant physical barriers.
Prioritize wheelchair-accessible, low-mobility-friendly, and transport-accessible options.

6. Weather Avoidance
If weather_avoidance is provided, avoid recommending outdoor activities in those conditions.
Suggest indoor alternatives where relevant.

7. Schedule Pacing
- "Packed": 4–6 activities per day across sections
- "Relaxed": 2–3 activities per day, include rest/leisure
- "Somewhere in between": 3–4 activities per day

8. Nightlife
If nightlife is True, include at least one evening activity involving bars, music, or entertainment per day where appropriate.
If False, keep evenings restaurant/leisure-focused only.

9. Start/End Times
Respect preferred daily start and end times. Do not schedule activities before start or after end.

9.1 Dominant Theme Rule
If the user provided interests, must_do items, or trip_purpose, those should be the dominant theme of at least 60% of activities across the itinerary. Do not dilute the itinerary with generic tourist activities if the user has clear preferences.

9.2 Budget Sensitivity Enforcement
If budget_concern is True:
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

# ---------- Endpoints ----------

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
    people_value = ctx.people if ctx.trip_mode == "discover" else ctx.people_b
    if people_value is None:
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

        if ctx.knows_trip_length_b and ctx.days_b is None:
            raise HTTPException(
                400,
                "days_b is required when knows_trip_length_b is true"
            )

    # =====================================================
    # 4) Option A: destination discovery
    # =====================================================
    if ctx.trip_mode == "discover":

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
    validate_range(ctx.days_b, 1, 30, "days_b")
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
    pdf_filename = f"itinerary_{timestamp}.pdf"
    pdf_path = f"generated_pdfs/{pdf_filename}"

    generate_itinerary_pdf(
        validated_itinerary,
        pdf_path
    )

    return TripResponse(itinerary=validated_itinerary, pdf_path=pdf_filename)


@app.get("/download-itinerary/{filename}")
def download_itinerary(filename: str):
    """Download a previously generated itinerary PDF by filename."""
    # Sanitize: reject any path traversal attempts
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(400, "Invalid filename")

    pdf_path = f"generated_pdfs/{filename}"

    if not os.path.exists(pdf_path):
        raise HTTPException(404, "PDF not found")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename="itinerary.pdf",
    )