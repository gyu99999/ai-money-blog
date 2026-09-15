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

    prompt = f"""
You are an elite affiliate marketing blogger whose sole purpose is to write High-Intent, transactional SEO content that gets instantly approved by top-tier affiliate networks like PartnerStack.
Your goal is to write a highly persuasive blog post about "{topic}".

CRITICAL STRUCTURAL RULES (YOU MUST FOLLOW THIS EXACT MARKDOWN FORMAT):

<div style="background-color: #f8fafc; padding: 1.25rem; border-left: 4px solid #3b82f6; margin-bottom: 2.5rem; font-size: 0.95rem; color: #475569; border-radius: 4px;">
<em><strong>Affiliate Disclosure:</strong> This post contains affiliate links. If you purchase through our links, we may earn a commission at no extra cost to you. We only recommend tools we have strictly vetted to ensure maximum ROI for your business.</em>
</div>

## ⏱️ Quick Verdict (TL;DR)
[Write a punchy 2-3 sentence summary. Give a rating out of 5 stars (e.g., ⭐️⭐️⭐️⭐️ 4.5/5). Explicitly state if they should buy it or skip it. Make it sound like an expert review.]

## ✅ Pros & ❌ Cons
[Use Markdown lists. You MUST use ✅ for Pros and ❌ for Cons. Give exactly 3 Pros and 2 Cons.]

## 🎯 Who is this for?
[Identify EXACTLY which types of businesses, marketers, or creators need this tool and why. Be specific.]

## 💰 Pricing Analysis: Which plan is worth it?
[Do NOT just list the prices blindly. Analyze them like an expert. E.g., "The Basic plan is enough for solo creators, but agencies MUST get the Pro plan for API access."]

## 🏆 Final Conclusion & Recommendation
[Wrap up the review with a strong closing statement. Then provide a clear call-to-action text encouraging them to click your affiliate link.]

[Insert this link strategically as a Call to Action: {affiliate_link}]

Important rules:
1. Output ONLY valid Markdown text. 
2. Do NOT output a main # title at the very beginning (start directly with the div).
3. Write in a persuasive, authoritative, and analytical tone in English.
"""
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
