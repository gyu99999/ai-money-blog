import os
import datetime
import argparse
import markdown
import urllib.parse
import urllib.request

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("패키지가 없습니다. 설치해주세요: pip install google-genai")
    exit(1)

# API 키 설정 (환경 변수에서 가져오기)
API_KEY = os.environ.get("GEMINI_API_KEY", "")

# --- HTML 템플릿 (블로그 디자인) ---
POST_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 2rem; color: #333; background-color: #fcfcfc; }}
        h1 {{ color: #2c3e50; font-size: 2.5rem; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2, h3 {{ color: #34495e; margin-top: 2rem; }}
        a {{ color: #e74c3c; text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
        .thumbnail-img {{ width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 20px 0; }}
        img {{ max-width: 100%; border-radius: 8px; margin: 20px 0; }}
        .header-nav {{ margin-bottom: 30px; }}
        .header-nav a {{ color: #3498db; font-weight: normal; }}
        blockquote {{ border-left: 4px solid #3498db; margin: 0; padding-left: 20px; color: #555; background: #f0f8ff; padding: 15px; border-radius: 4px; }}
        .date {{ color: #888; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="header-nav">
        <a href="../index.html">← Back to Home</a>
    </div>
    <div class="date">Published on {date}</div>
    {content}
</body>
</html>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Tech & Finance Insights</title>
    <meta name="google-site-verification" content="O1gyxK0pEZyAVfYwqclCwf3urV1wGBM2_0rD3SKeVy4" />
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 2rem; color: #333; background-color: #fcfcfc; }}
        h1 {{ color: #2c3e50; font-size: 3rem; text-align: center; margin-bottom: 10px; }}
        p.subtitle {{ text-align: center; color: #7f8c8d; margin-bottom: 40px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ background: white; margin-bottom: 15px; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        li a {{ color: #3498db; text-decoration: none; font-size: 1.2rem; font-weight: bold; }}
        li a:hover {{ text-decoration: underline; }}
        .date {{ color: #95a5a6; font-size: 0.9rem; margin-top: 5px; }}
    </style>
</head>
<body>
    <h1>AI Tech & Finance Insights</h1>
    <p class="subtitle">Latest reviews, tutorials, and trends in AI and Business.</p>
    <ul>
        {links}
    </ul>
</body>
</html>
"""

def generate_seo_article(topic, affiliate_link):
    print(f"[{datetime.datetime.now()}] '{topic}' 주제로 SEO 영문 아티클 생성을 시작합니다...")

    system_instruction = """
    You are a world-class SEO expert and tech blogger.
    Write a highly engaging, SEO-optimized English blog post about the given topic.
    Requirements:
    1. Write at least 800 - 1,200 words.
    2. Use Markdown formatting: H1, H2, H3, bullet points.
    3. The first line MUST be an H1 heading (e.g., # Your Title).
    4. Naturally weave in the provided 'Affiliate Link' at least 2-3 times.
    5. CRITICAL: DO NOT use 4-space indentations or tabs at the start of paragraphs. Use blockquotes (>) for highlights instead of indents.
    """
    prompt = f"Topic: {topic}\nAffiliate Link: {affiliate_link}\n\nPlease generate."

    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            )
        )
        return response.text
    except Exception as e:
        print(f"\n[ERROR] API 오류: {e}")
        return None

def update_index_page(docs_dir, post_filename, post_title, date_str):
    index_path = os.path.join(docs_dir, "index.html")
    
    # 새로운 포스트 링크 HTML 생성
    new_link_html = f'<li><a href="posts/{post_filename}">{post_title}</a><div class="date">{date_str}</div></li>\n'
    
    existing_links = ""
    # 기존 index.html이 있으면 링크 부분만 추출 (간단한 파싱)
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "<ul>" in content and "</ul>" in content:
                existing_links = content.split("<ul>")[1].split("</ul>")[0].strip()
    
    # 새 링크를 맨 위에 추가
    combined_links = new_link_html + existing_links
    
    # [제한 규칙] 최신 글 100개까지만 유지
    link_list = [link for link in combined_links.split("</li>") if link.strip()]
    if len(link_list) > 100:
        link_list = link_list[:100]
    combined_links = "</li>".join(link_list) + "</li>"

    
    # 템플릿에 합쳐서 저장
    final_index = INDEX_TEMPLATE.format(links=combined_links)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(final_index)
    print(f"[SUCCESS] 메인 페이지(index.html)가 업데이트 되었습니다.")

def generate_thumbnail(topic, safe_title, docs_dir):
    images_dir = os.path.join(docs_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    image_filename = f"{safe_title}.jpg"
    image_path = os.path.join(images_dir, image_filename)
    
    prompt = f"Professional high quality blog thumbnail illustration about {topic}, modern digital art, clean, aesthetic"
    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=400&nologo=true"
    
    print(f"[{datetime.datetime.now()}] AI 썸네일 이미지를 무료 생성기로부터 받아옵니다...")
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(image_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"[SUCCESS] 썸네일 이미지가 저장되었습니다: {image_path}")
        return f"../images/{image_filename}"
    except Exception as e:
        print(f"[ERROR] 이미지 생성 실패: {e}")
        return ""


def update_sitemap(docs_dir):
    sitemap_path = os.path.join(docs_dir, "sitemap.xml")
    posts_dir = os.path.join(docs_dir, "posts")
    base_url = "https://gyu99999.github.io/ai-money-blog/posts/"
    
    urls = []
    if os.path.exists(posts_dir):
        for f in os.listdir(posts_dir):
            if f.endswith(".html"):
                from urllib.parse import quote
                safe_url = base_url + quote(f)
                urls.append(f"    <url><loc>{safe_url}</loc></url>\n")
                
    sitemap_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    sitemap_content += "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
    sitemap_content += "".join(urls)
    sitemap_content += "</urlset>"
    
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"[SUCCESS] sitemap.xml ?성 ?료")

def build_static_blog(topic, affiliate_link):
    # 폴더 구조 생성 (GitHub Pages 호스팅을 위해 docs/ 폴더 사용)
    base_dir = "github_blog"
    docs_dir = os.path.join(base_dir, "docs")
    posts_dir = os.path.join(docs_dir, "posts")
    
    os.makedirs(posts_dir, exist_ok=True)
    
    # 1. AI 글 작성
    markdown_text = generate_seo_article(topic, affiliate_link)
    if not markdown_text:
        return

    # 2. 마크다운 파싱하여 제목 추출
    lines = markdown_text.split("\n")
    title = topic # 기본 제목
    for line in lines:
        if line.startswith("# "):
            title = line.replace("# ", "").strip()
            break
            
    # 3. 마크다운을 HTML로 변환
    html_content = markdown.markdown(markdown_text, extensions=['extra'])
    
    # 4. 개별 포스트 HTML 생성
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    safe_title = title.replace(" ", "-").replace("?", "").replace("!", "").replace(":", "").lower()[:50]
    post_filename = f"{date_str}-{safe_title}.html"
    
    final_post_html = POST_TEMPLATE.format(
        title=title,
        date=date_str,
        content=html_content
    )
    
    post_path = os.path.join(posts_dir, post_filename)
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(final_post_html)
    print(f"[SUCCESS] 포스트가 생성되었습니다: {post_path}")
    
    # 5. 메인 페이지(index.html) 업데이트
    update_index_page(docs_dir, post_filename, title, date_str)
    update_sitemap(docs_dir)
    
    print("\n[DONE] 모든 작업이 완료되었습니다!")
    print(f"[INFO] 브라우저에서 '{os.path.abspath(docs_dir)}/index.html'을 열어서 블로그를 확인하세요.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Pages Auto Blogger")
    parser.add_argument("--topic", type=str, default="Top 5 Best AI Website Builders in 2026", help="블로그 주제")
    parser.add_argument("--link", type=str, default="https://your-affiliate-link.com/?ref=your_id", help="제휴 마케팅 링크")
    args = parser.parse_args()

    if API_KEY == "여기에_API_키를_입력하세요" or not API_KEY:
        print("⚠️ GEMINI_API_KEY가 설정되지 않았습니다. 코드를 열어 API_KEY를 직접 입력해주세요.")
    else:
        build_static_blog(args.topic, args.link)
