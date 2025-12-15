import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_topics(profile):
    prompt = f"""
    Generate 3 writing challenge topics for a user with this profile:

    - Country: {profile.country}
    - User Type: {profile.user_type}
    - Writing Level: {profile.writing_level}
    - Tone Preference: {profile.tone_preference}

    Requirements:
    - Topics must be short (max 8–12 words)
    - Must be aligned to user profile & tone
    - Return topics ONLY in this JSON format:

    {{
      "topics": [
        "Topic 1 here",
        "Topic 2 here",
        "Topic 3 here"
      ]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"},
        max_tokens=120
    )

    data = json.loads(response.choices[0].message.content)
    return data.get("topics", [])
