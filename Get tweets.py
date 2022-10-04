import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# install this once :
#driver = webdriver.Chrome(ChromeDriverManager().install())

# download chrome driver
xpath='D:\Tweets\chromedriver.exe'
driver = Chrome(xpath)
driver.get('https://twitter.com/login')
# login to your twitter account


search_input=driver.find_element(By.XPATH,'//input[@aria-label="Search query"]')
# search whatever you like for instance boson
search_input.send_keys('#boson')
search_input.send_keys(Keys.RETURN)
driver.find_element(By.LINK_TEXT,'Latest').click()


# get tweets
cards=driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')
card=cards[0]



# twitter handle
card.find_element(By.XPATH,'.//span[contains(text(),"@")]').text
# postdate
card.find_element(By.XPATH,'.//time').get_attribute('datetime')
# context of tweet
comment = card.find_element(By.XPATH,'.//div[contains(text())]').text
text = card.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
print(text)
# by how hour ago
date = card.find_element(By.XPATH, './/time').text
print(date)
# replay
reply = card.find_element(By.XPATH, './/div[@data-testid="reply"]').text
# retweet
retweet = card.find_element(By.XPATH, './/div[@data-testid="retweet"]').text
#likes
likes = card.find_element(By.XPATH, './/div[@data-testid="like"]').text




def get_tweet_data(card):
    username = card.find_element(By.XPATH,'.//span').text
    handle = card.find_element(By.XPATH,'.//span[contains(text(),"@")]').text
    try :
        postdate = card.find_element(By.XPATH, './/time').get_attribute('datetime')
    except NoSuchElementException:
        return
    tweettext = card.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
    reply = card.find_element(By.XPATH, './/div[@data-testid="reply"]').text
    retweet = card.find_element(By.XPATH, './/div[@data-testid="retweet"]').text
    likes = card.find_element(By.XPATH, './/div[@data-testid="like"]').text

    tweet = (username,handle,postdate,tweettext,reply,retweet,likes)
    return tweet


get_tweet_data(card)
tweet_data=[]
for card in cards:
    data = get_tweet_data(card)
    if data:
        tweet_data.append(data)
print(len(data))
tweet_data[0]


# different way of scrolling
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
driver.execute_script('window.scrollByPages(5);')
driver.execute_script('window.scrollBy(0, 5*window.innerHeight);')
driver.execute_script("window.scrollBy(-1000,document.body.scrollHeight || -document.documentElement.scrollHeight)", "")
driver.execute_script('window.scrollTo(-16, document.body.scrollHeight);')
driver.execute_script('window.scrollTo({top: 4000, left: 10, behavior: "smooth" });')
driver.execute_script("window.scrollTo(0, 5500)")





# get all tweets on the page
data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    page_cards = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')
    for card in page_cards[:]:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
                if len(data)==100 :
                    break


    scroll_attempt = 0
    while True:
        # check scroll position
        driver.execute_script('window.scrollBy(0, 5*window.innerHeight);')
        sleep(3)
        if len(data) == 100:
            break
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1

            # end of scroll region
            if scroll_attempt >= 10:
                scrolling = False
                break
            else:
                sleep(3)  # attempt another scroll
        else:
            last_position = curr_position
            break

# close the web driver
driver.close()


with open('bosongood_tweets.csv', 'w', newline='', encoding='utf-8') as f:
    header = ['username', 'handle', 'postdate', 'tweettext', 'reply', 'likes', 'retweet']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)


