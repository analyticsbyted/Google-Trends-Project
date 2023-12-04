from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas as pd

pytrends = TrendReq(hl='en-US')

all_keywords = ['Fidget spinner',
                'Food', 'Cycling',
                'Home Alone', 'Delivery',
                'Wine', 'Beer',]

keywords = []

timeframes = ['today 5-y', 'today 12-m', 'today 3-m', 'today 1-m', 'now 7-d', 'now 1-d']
timeframe = timeframes[0]

cat = '0' #all categories. for example, for books, it would be 22
geo= '' #worldwide, 2 letter abbreviation for country
gprop = '' #web searches, image searches, youtube searches, news searches

#Build Payload
def check_trends():
    pytrends.build_payload(keywords, 
                            cat, 
                            timeframe, 
                            geo, 
                            gprop)
    interest_over_time_df = pytrends.interest_over_time()
    mean = round(interest_over_time_df.mean(), 2)
    avg = round(interest_over_time_df[kw][-52:].mean(), 2)
    avg2 = round(interest_over_time_df[kw][:52].mean(), 2)
    # print(kw + ': ' + str(mean[kw]))
    trend = round(((avg/mean[kw])-1)*100, 2)
    trend2 = round(((avg/avg2)-1)*100, 2)
    print('The average 5-year interest of ' + kw + ' is ' + str(mean[kw]) + '.')
    print('The average interest over the last 52 weeks is ' + str(avg) )
    print('The interest has changed by ' + str(trend) + '%.')

    # Define categories
    categories = [
        ("Stable", 75, 5),
        ("Stable and Increasing", 75, 10),
        ("Stable but Decreasing", 75, -10),
        ("Relatively Stable", 60, 10),
        ("Relatively Stable and Increasing", 60, 10),
        ("Relatively Stable but Decreasing", 60, -10),
        ("Cyclical", 20, 15),
        ("Trending", 20, 15),
        ("Significantly Decreasing", 20, -15),
        ("Cyclical", 5, 15),
        ("New and Trending", 0, 15),
    ]

    # Check conditions
    for category, threshold, trend_limit in categories:
        if mean[kw] > threshold and abs(((avg/mean[kw])-1)*100) <= abs(trend_limit):
            print(f'The interest for {kw} is {category} in the last 5 years.')
            print('')
            break  # Stop checking once a category is matched

             
for kw in all_keywords:
    keywords.append(kw)
    check_trends()
    keywords.pop()


