import os
import subprocess
from google import genai

AFFILIATE_LINK = "https://partnerstack.com/"

def get_trending_topic():
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    try:
        client = genai.Client(api_key=gemini_key)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents="Provide exactly ONE highly clickable, SEO-optimized blog post title about AI tools or AI making money in 2026. Do NOT include quotes, hashtags, or any other text. Just the title."
        )
        return response.text.strip().replace("\"", "")
    except Exception as e:
        print(f"Error: {e}")
        return "Best AI Tools for Business Automation"

if __name__ == "__main__":
    topic = get_trending_topic()
    print(f"Topic: {topic}")
    subprocess.run(["python", "auto_github_blog.py", "--topic", topic, "--link", AFFILIATE_LINK])

