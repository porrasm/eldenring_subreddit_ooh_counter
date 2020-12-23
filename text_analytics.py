import re
import numpy as np
from collections import Counter
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class OohAnalyzer:

    posts = None

    # general stats
    start_time = float('inf')

    post_count = 0
    comment_count = 0

    ooh_count = 0
    ooh_post_count = 0
    ooh_comment_count = 0

    o_count = 0
    h_count = 0

    total_score_of_all_oohs = 0

    # top lists
    all_users = {}

    all_oohs = {}
    all_ooh_counter = {}
    list_most_common_oohs = None

    different_ooh_users = {}

    user_amount = 0

    day_ooh_count = {}
    avg_oohs_per_day = 0

    unique_ooh_appearances = 0
    avg_upvotes_per_ooh = 0

    avg_ooh_per_active_user = 0
    avg_ooh_per_ooh_user = 0

    ooh_chance_in_any_text = 0

    score_69_count = 0

    # awards
    longest_ooh = (None, 0)
    most_upvoted_ooh = (None, -100000000)
    most_oohs_by_user = (None, 0)
    most_upvotes_from_oohs = (None, 0)
    post_with_most_oohs = (None, 0)

    most_common_ooh = (None, 0)
    ooh_user_participate_percentage = 0

    def __init__(self, posts):
        self.posts = posts


    def calculate_stats(self):
        for post in self.posts:

            if post[0]["created_utc"] < self.start_time:
                self.start_time = post[0]["created_utc"]

            post_ooh_count = self.process_text_appearance(post[0])
            for comment in post[1]:
                post_ooh_count += self.process_text_appearance(comment)

            if post_ooh_count > self.post_with_most_oohs[1]:
                self.post_with_most_oohs = (post[0], post_ooh_count)
        
        self.most_common_oohs()
        self.set_most_ooh_user()
        self.set_avg_ooh_per_day()
        self.avg_upvotes_per_ooh = self.avg_upvotes_per_ooh / self.unique_ooh_appearances
        self.ooh_chance_in_any_text = self.unique_ooh_appearances / (self.post_count + self.comment_count)
        self.ooh_user_participate_percentage = len(self.different_ooh_users) / len(self.all_users)
        self.set_most_upvotes_from_oohs()
        self.set_most_common_ooh()

        self.avg_ooh_per_active_user = self.ooh_count / len(self.all_users)
        self.avg_ooh_per_ooh_user = self.ooh_count / len(self.different_ooh_users)

        self.user_amount = len(self.different_ooh_users)

    def most_common_oohs(self):
        self.list_most_common_oohs = dict(Counter(self.all_ooh_counter).most_common(5))

    def set_most_ooh_user(self):
        for key in self.different_ooh_users:
            amount = self.different_ooh_users[key]
            if amount > self.most_oohs_by_user[1]:
                self.most_oohs_by_user = (key, amount) 
    def set_avg_ooh_per_day(self):
        count = 0
        for k in self.day_ooh_count:
            count += self.day_ooh_count[k]
        self.avg_oohs_per_day = count / len(self.day_ooh_count)

    def set_most_upvotes_from_oohs(self):
        for k in self.all_users:
            if self.all_users[k] > self.most_upvotes_from_oohs[1]:
                self.most_upvotes_from_oohs = (k, self.all_users[k])

    def set_most_common_ooh(self):
        for k in self.all_oohs:
            amount = self.all_oohs[k]
            if amount > self.most_common_ooh[1]:
                self.most_common_ooh = (k, amount)



    def process_text_appearance(self, text):
        if text["is_post"]:
            self.post_count += 1
        else:
            self.comment_count += 1

        if text["score"] == 69:
            self.score_69_count += 1

        if text["author"] not in self.all_users:
            self.all_users[text["author"]] = 0

        local_ooh_count = 0

        # Individual ooh
        for word in re.split('\s+', text["text"]):
            ooh = get_ooh(word)

            if not ooh:
                continue
            local_ooh_count += 1
            self.all_users[text["author"]] += text["score"]

            date = datetime.datetime.fromtimestamp(text["created_utc"])
            if date.date() in self.day_ooh_count:
                self.day_ooh_count[date.date()] += 1
            else:
                self.day_ooh_count[date.date()] = 1

            if word in self.all_oohs:
                self.all_oohs[word] += 1
            else:
                self.all_oohs[word] = 1

            oohkey = (ooh[0], ooh[1])
            if oohkey in self.all_ooh_counter:
                self.all_ooh_counter[oohkey] += 1
            else:
                self.all_ooh_counter[oohkey] = 1

            if text["author"] in self.different_ooh_users:
                self.different_ooh_users[text["author"]] += 1
            else:
                self.different_ooh_users[text["author"]] = 1

            self.ooh_count += 1
            self.o_count += ooh[0]
            self.h_count += ooh[1]

            if text["is_post"]:
                self.ooh_post_count += 1
                # most upvoted ooh post

            else:
                self.ooh_comment_count += 1

            # longest ooh
            ooh_len = ooh[0] + ooh[1]
            if ooh_len > self.longest_ooh[1]:
                self.longest_ooh = (text, ooh_len, ooh)
        
        # Text ooh
        if local_ooh_count == 0:
            return 0

        self.total_score_of_all_oohs += text["score"]
        self.avg_upvotes_per_ooh += text["score"]
        self.unique_ooh_appearances += 1

        if text["score"] > self.most_upvoted_ooh[1]:
            self.most_upvoted_ooh = (text, text["score"])
        
        return local_ooh_count

    def print_stats(self):

        print("\n----------------------------------------------------------\n")
        print(f"Start time: {(self.start_time, datetime.datetime.fromtimestamp(self.start_time))}\n")

        # General
        print(f"- Post count: {self.post_count}")
        print(f"- Comment count: {self.comment_count}")
        print(f"- Ooh count: {self.ooh_count}")
        print(f"- Ooh post count: {self.ooh_post_count}")
        print(f"- Ooh comment count: {self.ooh_comment_count}")
        print(f"- Letter O count: {self.o_count}")
        print(f"- Letter H count: {self.h_count}")
        print(f"- O / H ratio: {self.o_count / self.h_count}")
        print(f"- Total upvotes on OOHs: {self.total_score_of_all_oohs}")
        print(f"- Unique ooh count: {len(self.all_oohs)}")
        print(f"- Active user count {len(self.all_users)}")
        print(f"- Total OOH user count: {self.user_amount}")
        print(f"- AVG oohs per day: {self.avg_oohs_per_day}")
        print(f"- AVG upvotes per ooh: {self.avg_upvotes_per_ooh}")
        print(f"- AVG oohs per active user: {self.avg_ooh_per_active_user}")
        print(f"- AVG oohs per OOH user: {self.avg_ooh_per_ooh_user}")

        # Awards
        print("\nAwards\n")

        print(f"- Longest OOH {self.longest_ooh}")
        print(f"- Most upvoted OOH {self.most_upvoted_ooh}")
        print(f"- Most OOHs by user {self.most_oohs_by_user}")
        print(f"- Most Upvotes from OOhs {self.most_upvotes_from_oohs}")
        print(f"- Post with most OOhs {self.post_with_most_oohs}")

        print("\nOther\n")
        
        print(f"- Most common ooh {self.most_common_ooh}")
        print(f"- Ooh chance in text appearance {self.ooh_chance_in_any_text}")
        print(f"- Active user ooh participate rate {self.ooh_user_participate_percentage}")
        print(f"- Score 69 count {self.score_69_count}")



    def plots(self):
        print("\nOohs per day plot", flush=True)
        # frequency plot
        x = list()
        y = list()

        for k in self.day_ooh_count:
            x.append(datetime.datetime(k.year, k.month, k.day))
            y.append(self.day_ooh_count[k])
        
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        plt.plot(x, y, 'r--')
        plt.gcf().autofmt_xdate()
        plt.show()

            


def get_ooh(text):
        
    l = len(text)
    if l < 3:
        return False

    lw = text.lower()

    upperCount = 0
    lowerCount = 0
    startOs = 0
    endHs = 0
    endLetters = 0

    if lw[0] != 'o':
        return None

    # Start Os
    i = 0
    while i < l:
        if lw[i] == 'o':
            startOs += 1
            if text[i].isupper():
                upperCount += 1
            else:
                lowerCount += 1
        else:
            break
        i += 1
    
    # End Hs
    while i < l:
        if lw[i] == 'h':
            endHs += 1
            if text[i].isupper():
                upperCount += 1
            else:
                lowerCount += 1
        elif lw[i] == 'o':
            if text[i].isupper():
                upperCount += 1
            else:
                lowerCount += 1
        else:
            break
        i += 1

    if i == l and upperCount > lowerCount:
        return (startOs, endHs, lowerCount, upperCount)
    
    while i < l:
        if text[i].isalpha():
            endLetters += 1
        else:
            break
        i += 1
    
    if endHs == 0 or endLetters > 0:
        return None

    if upperCount > lowerCount:
        return (startOs, endHs, lowerCount, upperCount)
    else:
        return None
