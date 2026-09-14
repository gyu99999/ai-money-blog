import os
import subprocess
import random

AFFILIATE_LINK = "https://partnerstack.com/"

TOPICS = [
    "10 Best AI Tools to Make Money Online in 2026",
    "How to Use AI for Passive Income: A Beginner's Guide",
    "Top 5 AI Website Builders to Start a Business Fast",
    "Make $10k/Month with These Secret AI Automation Tools",
    "Best AI Voice Generators for Faceless YouTube Channels",
    "7 Underrated AI Tools That Can Make You $10,000 a Month in 2026",
    "Top AI Copywriting Tools to Dominate SEO in 2026"
]

def main():
    print("Starting Daily AI Autoblog (Jekyll CMS Version)...")
    chosen_topic = random.choice(TOPICS)
    
    subprocess.run(["python", "auto_github_blog.py", "--topic", chosen_topic, "--link", AFFILIATE_LINK])
    print("Done!")

if __name__ == "__main__":
    main()
