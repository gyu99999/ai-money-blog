import os
import subprocess
import random

AFFILIATE_LINK = "https://partnerstack.com/"

# HIGH-INTENT BUYER KEYWORDS (Reviews, Vs, Pricing, Best)
TOPICS = [
    "Jasper AI vs Copy.ai: Which is the Best AI Copywriter for High Conversions in 2026?",
    "Midjourney vs DALL-E 3: Which AI Art Generator is Worth the Subscription?",
    "Top 5 AI Voice Generators with Commercial Licenses in 2026 (Pricing & Reviews)",
    "Best AI Video Editors for YouTube Shorts: In-Depth Review and Pricing",
    "Notion AI vs ChatGPT Plus: Which Productivity Tool is Worth Your Money?",
    "Is ElevenLabs the Best AI Voice Generator? Honest Review & Pricing Guide",
    "Best AI Website Builders for E-commerce: Honest Review and ROI Analysis"
]

def main():
    print("Starting Daily AI Autoblog (High-Intent SEO Version)...")
    chosen_topic = "PartnerStack Test: Is Jasper AI Still Worth It in 2026?"
    subprocess.run(["python", "auto_github_blog.py", "--topic", chosen_topic, "--link", AFFILIATE_LINK])
    print("Done!")

if __name__ == "__main__":
    main()
