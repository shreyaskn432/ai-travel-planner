import requests

# ✅ Known valid places (basic filter)
VALID_PLACES = [
    "Baga Beach", "Calangute Beach", "Anjuna Beach",
    "Vagator Beach", "Palolem Beach", "Colva Beach",
    "Fort Aguada", "Dona Paula", "Panaji", "Old Goa"
]

def clean_output(text):
    if "Day 1" in text:
        text = text.split("Day 1")[1]
        text = "Day 1" + text

    lines = []
    seen = set()

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        # 🔥 Remove fake places
        if "Places:" in line:
            valid = [p for p in VALID_PLACES if p in line]
            if valid:
                line = "- Places: " + ", ".join(valid)
            else:
                continue

        # remove duplicates
        if line not in seen:
            seen.add(line)
            lines.append(line)

    return "\n".join(lines).strip()


def generate_itinerary(destination, days, budget, interests):
    url = "http://localhost:11434/api/generate"

    prompt = f"""
Create a {days}-day travel plan for {destination}.

Format:

Day 1:
- Places:
- Activities:
- Food:

Day 2:
- Places:
- Activities:
- Food:

Day 3:
- Places:
- Activities:
- Food:

Rules:
- Use real places in {destination}
- Max 3 places per day
- Short bullet points only
"""

    data = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)
    result = response.json()["response"]

    return clean_output(result)