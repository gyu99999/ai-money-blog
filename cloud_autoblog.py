import os
import subprocess
import shutil
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
    
    import shutil
    os.makedirs("github_blog/docs", exist_ok=True)
    if os.path.exists("docs/index.html"):
        shutil.copy("docs/index.html", "github_blog/docs/index.html")
    subprocess.run(["python", "auto_github_blog.py" , "--topic", topic, "--link", AFFILIATE_LINK])
    
    # 깃허브 액션 환경에서는 github_blog/docs 안에 생성되므로, 진짜 docs/ 폴더로 복사/이동
    if os.path.exists("github_blog/docs"):
        # Copy posts
        for f in os.listdir("github_blog/docs/posts"):
            if f.endswith(".html"):
                shutil.copy(os.path.join("github_blog/docs/posts", f), os.path.join("docs/posts", f))
        # Copy index
        shutil.copy("github_blog/docs/index.html", "docs/index.html")
        print("Moved files to root docs/ folder")
