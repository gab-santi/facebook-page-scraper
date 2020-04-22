# facebook-page-scraper
Scraping tool for public Facebook pages without the use of an API key. A Facebook account is required. Extended from @kevinzg's facebook-scraper. Used Selenium for scraping comments. All code is written in Python.

## How to use
1. Clone repository
2. Install requirements 

```bash
pip install -r requirements.txt
```
3. Download chromedriver for Selenium and put it in the project folder
4. Open main.py file and edit the following variables:

```python
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
```

5. Run in the command line (make sure you are in the project directorys)
```bash
python main.py
```

