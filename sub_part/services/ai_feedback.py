import json, os
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are an expert writing coach focused on helping people think more clearly through writing. Your feedback should:
1) Evaluate THINKING quality, not just mechanics
2) Identify depth vs surface arguments
3) Point out logical gaps or unsupported claims
4) Recognize originality vs cliché
5) Be encouraging but honest
6) Give specific, actionable suggestions
Avoid generic praise. Focus on substance and thought process."""

def generate_feedback(submission_text: str, challenge_prompt: str):
    user_prompt = f"""Challenge: {challenge_prompt}

Writer's Response:
{submission_text}

Provide feedback in this exact JSON format:
{{
  "clarity_score": 0-100,
  "depth_score": 0-100,
  "structure_score": 0-100,
  "originality_score": 0-100,
  "overall_score": 0-100,
  "strengths": "2-3 specific things done well",
  "improvements": "2-3 areas needing work",
  "specific_suggestions": "Concrete next steps to improve"
}}

Focus on:
- Clarity
- Depth
- Structure
- Originality
Be specific with examples from their writing."""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":user_prompt}
        ],
        temperature=0.7,
        max_tokens=800,
        response_format={"type":"json_object"}
    )

    content = resp.choices[0].message.content
    feedback_json = json.loads(content)

    usage = resp.usage or None
    tokens_used = (usage.total_tokens if usage else None)
    # rough cost calc — adjust with current pricing if you want exactness
    input_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0
    output_tokens = getattr(usage, "completion_tokens", 0) if usage else 0
    cost = input_tokens * 0.00000015 + output_tokens * 0.0000006

    return {"feedback": feedback_json, "tokens_used": tokens_used, "cost": cost}
