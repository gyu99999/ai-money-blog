import os
import datetime
import argparse
import re

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Required: pip install google-genai")
    exit(1)

API_KEY = os.environ.get("GEMINI_API_KEY", "")

def generate_seo_article(topic, affiliate_link):
    if not API_KEY:
        print("[ERROR] GEMINI_API_KEY is not set.")
        return None

    prompt = f\"\"\"
You are an elite affiliate marketing blogger who specializes in High-Intent, transactional SEO content. 
Your goal is to write a highly persuasive blog post about "{topic}" that targets readers who are in the decision-making phase and ready to buy.

CRITICAL RULES:
1. Do NOT write generic, informational fluff (e.g., "What is AI?"). Focus entirely on buyer intent (Reviews, Pricing, Vs comparisons, ROI).
2. Push the reader towards making a purchasing decision by highlighting value and resolving doubts.
3. Use the following affiliate link strategically and naturally as a strong Call-To-Action (CTA): {affiliate_link}
4. Output ONLY valid Markdown text. Use ## for sections. Do NOT output a main # title.
5. Include highly converting formatting: "Pros & Cons" bullet points, a "Pricing Breakdown" section, and a clear "Final Verdict".
6. Write in a persuasive, authoritative, yet conversational tone in English.
\"\"\"
    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7)
        )
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] API Error: {e}")
        return None

def build_jekyll_post(topic, affiliate_link):
    markdown_text = generate_seo_article(topic, affiliate_link)
    if not markdown_text:
        print("Failed to generate content.")
        return

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%Y-%m-%d %H:%M:%S +0900")
    
    safe_title = re.sub(r'[^a-zA-Z0-9\s-]', '', topic).strip().replace(' ', '-')
    safe_title = re.sub(r'-+', '-', safe_title)[:50].lower()
    filename = f"{date_str}-{safe_title}.md"
    
    os.makedirs(os.path.join("docs", "_posts"), exist_ok=True)
    filepath = os.path.join("docs", "_posts", filename)

    front_matter = f"---\nlayout: post\ntitle: \"{topic}\"\ndate: {time_str}\ncategories: ai\n---\n\n"
    
    if markdown_text.startswith("# "):
        lines = markdown_text.split("\n")
        markdown_text = "\n".join(lines[1:]).strip()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(front_matter + markdown_text)
    print(f"Generated {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--link", required=True)
    args = parser.parse_args()
    build_jekyll_post(args.topic, args.link)
