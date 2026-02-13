"""
PDF generator for travel itineraries.
Uses reportlab for simple, reliable PDF generation.
"""

from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_itinerary_pdf(itinerary: dict, output_path: str) -> None:
    """
    Generate a PDF from a validated itinerary JSON.

    Args:
        itinerary: Dictionary with structure:
            {
                "days": [
                    {
                        "day": 1,
                        "sections": {
                            "morning": ["activity1", "activity2"],
                            "afternoon": ["activity3"],
                            "evening": ["activity4"]
                        }
                    }
                ],
                "summary": "string"
            }
        output_path: Path where the PDF should be saved (e.g., "output.pdf")

    Returns:
        None (writes PDF to output_path)
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#1a5490',
        spaceAfter=30,
        alignment=TA_CENTER,
    )

    day_heading_style = ParagraphStyle(
        'DayHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#2a5490',
        spaceAfter=12,
        spaceBefore=20,
    )

    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading3'],
        fontSize=13,
        textColor='#4a5490',
        spaceAfter=8,
        spaceBefore=12,
        leftIndent=20,
    )

    activity_style = ParagraphStyle(
        'Activity',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=40,
        spaceAfter=6,
        bulletIndent=30,
    )

    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        spaceBefore=20,
        leftIndent=20,
        rightIndent=20,
    )

    # Title
    story.append(Paragraph("Travel Itinerary", title_style))
    story.append(Spacer(1, 0.3 * inch))

    # Days
    days = itinerary.get("days", [])

    for day_data in days:
        day_num = day_data.get("day", 0)
        sections = day_data.get("sections", {})

        # Day heading
        story.append(Paragraph(f"Day {day_num}", day_heading_style))

        # Morning section
        morning_activities = sections.get("morning", [])
        if morning_activities:
            story.append(Paragraph("Morning", section_heading_style))
            for activity in morning_activities:
                bullet_text = f"• {activity}"
                story.append(Paragraph(bullet_text, activity_style))

        # Afternoon section
        afternoon_activities = sections.get("afternoon", [])
        if afternoon_activities:
            story.append(Paragraph("Afternoon", section_heading_style))
            for activity in afternoon_activities:
                bullet_text = f"• {activity}"
                story.append(Paragraph(bullet_text, activity_style))

        # Evening section
        evening_activities = sections.get("evening", [])
        if evening_activities:
            story.append(Paragraph("Evening", section_heading_style))
            for activity in evening_activities:
                bullet_text = f"• {activity}"
                story.append(Paragraph(bullet_text, activity_style))

        # Add space between days
        story.append(Spacer(1, 0.3 * inch))

    # Summary section
    summary = itinerary.get("summary", "")
    if summary:
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("Summary", day_heading_style))
        story.append(Paragraph(summary, summary_style))

    # Build PDF
    doc.build(story)
    print(f"PDF successfully generated at: {output_path}")

# Local test runner for PDF generation; not used by FastAPI
if __name__ == "__main__":
    # Example usage
    sample_itinerary = {
        "days": [
            {
                "day": 1,
                "sections": {
                    "morning": [
                        "Arrive in Cannon Beach",
                        "Check into your accommodation"
                    ],
                    "afternoon": [
                        "Visit Cannon Beach and Haystack Rock",
                        "Explore local shops and galleries"
                    ],
                    "evening": [
                        "Have dinner at a seafood restaurant",
                        "Watch the sunset over the ocean"
                    ]
                }
            },
            {
                "day": 2,
                "sections": {
                    "morning": [
                        "Drive to Ecola State Park for scenic views",
                        "Hike along the trails to see the coastline"
                    ],
                    "afternoon": [
                        "Enjoy a picnic lunch at the park",
                        "Drive to Newport along the scenic highway"
                    ],
                    "evening": [
                        "Check into your Newport accommodation",
                        "Dine at a local seafood restaurant"
                    ]
                }
            }
        ],
        "summary": "This 2-day itinerary offers a relaxed coastal road trip along the Oregon Coast."
    }

    generate_itinerary_pdf(sample_itinerary, "sample_itinerary.pdf")
