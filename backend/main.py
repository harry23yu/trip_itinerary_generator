from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TripRequest(BaseModel):
    destination: str
    days: int
    interests: list[str]

@app.post("/generate-itinerary")
def generate_itinerary(req: TripRequest):
    return {
        "itinerary": f"""
        Trip to {req.destination}
        Duration: {req.days} days
        Interests: {', '.join(req.interests)}

        Day 1: Explore the city
        Day 2: Local food and culture
        """
    }