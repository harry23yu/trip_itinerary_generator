from typing import List, Dict, Any
import json

def get_itinerary_schema_prompt() -> str:
    """
    This prompt strictly defines the JSON schema the model must output.
    No markdown, no prose, no extra keys.
    """
    return """
You MUST output valid JSON only.

The JSON MUST follow this exact structure:

{
  "days": [
    {
      "day": <integer starting from 1>,
      "sections": {
        "morning": [<string>, <string>, ...],
        "afternoon": [<string>, <string>, ...],
        "evening": [<string>, <string>, ...]
      }
    }
  ],
  "summary": <string>
}

Rules:
- Do NOT include markdown.
- Do NOT include headings like "Day 1:" outside JSON.
- Do NOT include explanations or notes outside JSON.
- Each activity must be a short, concrete sentence.
- If a section has nothing planned, use an empty list [].
- The number of days MUST match the trip length.
- Output must be parseable by json.loads().

If you violate this format, the response is invalid.
"""

def parse_and_validate_itinerary(raw_output: str) -> Dict[str, Any]:
    """
    Parses model output and ensures it matches the required structure.
    Raises ValueError if invalid.
    """
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError("Model output is not valid JSON") from e

    if "days" not in data or "summary" not in data:
        raise ValueError("Missing required top-level keys")

    if not isinstance(data["days"], list):
        raise ValueError("'days' must be a list")

    for day in data["days"]:
        if "day" not in day or "sections" not in day:
            raise ValueError("Each day must have 'day' and 'sections'")

        sections = day["sections"]
        for key in ["morning", "afternoon", "evening"]:
            if key not in sections or not isinstance(sections[key], list):
                raise ValueError(f"Section '{key}' must be a list")

    return data