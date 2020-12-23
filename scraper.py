import praw
import sys
import post_handler
import text_analytics
import json

sys.stdin.reconfigure(encoding='utf-16')
sys.stdout.reconfigure(encoding='utf-16')

limit = 3

print(text_analytics.get_ooh("OOOOOOOOOOOOOOOOO"))
posts = None
if len(sys.argv) > 1 and sys.argv[1] == "test":
    with open("data.json") as json_file:
        posts = json.load(json_file)
else:
    posts = post_handler.get_text_appearances(limit)
    with open("data.json", "w") as file:
        json.dump(posts, file, indent=4)


ooh = text_analytics.OohAnalyzer(posts)
ooh.calculate_stats()

print("-------------------------------------------------")
ooh.print_stats()
ooh.plots()