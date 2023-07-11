import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd
from openpyxl import Workbook
# requesting hmtml information
res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')

# parsing  into html object
#by this we can access different parts/tags
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

#using css selectors to target class and href 

links = soup.select('.titleline > a') 
subtext = soup.select('.subtext')
links2 = soup2.select('.titleline > a') 
subtext2 = soup2.select('.subtext')

# merging the two different lists into 1
mega_links = links + links2
mega_subtext = subtext + subtext2

#defining the return function
def sort_stories_by_votes(hnlist):
  return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

#defining the function to separate out required articles from request html document obtained 
def create_custom_hn(links, subtext):
  hn = []
  for idx, item in enumerate(links): # enumerating here to also get index for the link so we can find the same subtext to target votes later
    title = item.getText()
    href = item.get('href', None)
    vote = subtext[idx].select('.score')
    if len(vote):
      points = int(vote[0].getText().replace(' points', ''))
      if points > 150:
        hn.append({'title': title, 'link': href, 'votes': points})
  return sort_stories_by_votes(hn)
 
pprint.pprint(create_custom_hn(mega_links, mega_subtext))

converting = create_custom_hn(mega_links, mega_subtext)
# convert into dataframe

df = pd.DataFrame(data=converting)

#convert into excel
df.to_csv("mydaily_hackernews.csv")
# print("Dictionary converted into excel")