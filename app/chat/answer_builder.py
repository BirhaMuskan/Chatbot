from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def build_general_answer(question):
    prompt = f"""Answer the following question clearly and helpfully.

Return clean HTML only. No markdown. No triple backticks.

Use <h3> for headings, <p> for paragraphs, <ul><li> for bullet points, <b> for bold.
Wrap everything in a single <div>.

Question: {question}
"""
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=700,
        temperature=0.7,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text

def build_answer(question, data):
    if not data:
        return "No matching inventory records found."

    prompt = f"""
You are an inventory assistant.

Answer using only this database data.

Question:
{question}

Database Data:
{json.dumps(data, indent=2)}

Return clean HTML only.

Use this format:
<div>
  <h3>Stock Summary</h3>
  <p><b>Total Available Quantity:</b> value units</p>
  <table border="1" cellpadding="6" cellspacing="0">
    <tr>
      <th>Size</th>
      <th>Available</th>
      <th>Committed</th>
      <th>In Transit</th>
      <th>Distributor</th>
    </tr>
  </table>
</div>

Rules:
- No markdown
- No ```html
- No explanation
- Do not invent data
- Keep it professional
"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=700,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text