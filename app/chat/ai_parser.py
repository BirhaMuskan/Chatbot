from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return {
            "intent": "stock",
            "style": None,
            "colour": None,
            "size": None,
            "distributor": None
        }

    return json.loads(match.group())

def extract_filters(question):
    prompt = f"""
You are an inventory AI parser.

Extract filters and intent from the user question.

Return ONLY JSON. No explanation. No markdown.

Format:
{{
  "intent": "stock",
  "style": null,
  "colour": null,
  "size": null,
  "distributor": null
}}

Possible intents:
- stock (asking about inventory levels, specific products, or stock by distributor/colour/size)
- low_stock (asking about items running low or out of stock)
- sales (asking about sales data)
- overstock (asking about overstocked items)
- dead_stock (asking about dead or slow-moving stock)
- general (anything NOT related to inventory, products, or stock — e.g. general knowledge, greetings, science questions)

IMPORTANT: Only extract style/colour/size/distributor if the question is clearly about inventory.
If the question is general knowledge (e.g. "what is a black hole", "hello", "who are you"), use intent "general" and set all other fields to null.

Examples:

Question: What is stock of JHA001 Jet Black?
Answer:
{{"intent":"stock","style":"JHA001","colour":"JET BLACK","size":null,"distributor":null}}

Question: Show low stock items
Answer:
{{"intent":"low_stock","style":null,"colour":null,"size":null,"distributor":null}}

Question: Which products are running out?
Answer:
{{"intent":"low_stock","style":null,"colour":null,"size":null,"distributor":null}}

Question: Show inventory for Ralawise
Answer:
{{"intent":"stock","style":null,"colour":null,"size":null,"distributor":"RALAWISE"}}

Question: What is a black hole?
Answer:
{{"intent":"general","style":null,"colour":null,"size":null,"distributor":null}}

Question: Hello, how are you?
Answer:
{{"intent":"general","style":null,"colour":null,"size":null,"distributor":null}}

User question:
{question}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text = response.content[0].text.strip()

    print("CLAUDE FILTERS:", text)

    return extract_json(text)