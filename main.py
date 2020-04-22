from facebook_scraper import get_posts
import csv
from classes.selenium_scraper import SeleniumScraper
import pandas as pd

# name of page, can be found in url. ex: nintendo
page = ''
filename_posts = page + '_posts.csv'
filename_comments = page + '_comments.csv'

# path to chromedriver.exe (in chromedriver folder)
chromedriver_path = ''

# your fb email
email = ''
# your fb password
password = ''

links = []

# scrape posts (using facebook_scraper)
with open(filename_posts, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['post_id', 'text', 'time', 'image', 'likes', 'comments', 'shares', 'post_url', 'link'])

    print('Scraping {}...'.format(page))

    for post in get_posts(page, extra_info=True):
        print(post)
        writer.writerow([post['post_id'], post['text'], post['time'], post['image'], post['likes'], post['comments'], post['shares'], post['post_url'], post['link']])

        # get post comments
        if (post['post_url'] != None):
            links.append([post['post_id'], post['post_url']])

# scrape comments (using Selenium since facebook_scraper can't scrape comments)
#with open(filename_comments, 'w', encoding='utf-8', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerow(['post_id', 'comment_id', 'commenter_name', 'commenter_profile_link', 'text', 'time', 'reactions_count'])
scraper = SeleniumScraper(chromedriver_path, email, password)

# df containing all comments; init
comments_master_df = pd.DataFrame(columns=['post_id', 'comment_id', 'commenter_name', 'commenter_profile_link', 'text', 'time', 'reactions_count'], index=None)

for link in links:
    #put comments in rows
    post_id = print(link[0])

    # scrape comments
    comments_df = scraper.scrapeFacebookComments(post_id, link[1])

    # append to master df
    comments_master_df = pd.concat([comments_master_df, comments_df], ignore_index=True)
    print('current master comments:')
    print(comments_master_df)

# write df to csv
print('writing file to csv..')
comments_master_df.to_csv(filename_comments, index=False)
print('done')

print('done scraping', page)
scraper.closeDriver()

