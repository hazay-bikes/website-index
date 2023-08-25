import requests
import re
import html

# locale
LANG_PL = '/pl/'
LANG_EN = '/en/'

ROOT_SITEMAP_URL = 'https://hazaybikes.com/pl/sitemap_index.xml'

r = requests.get(ROOT_SITEMAP_URL)
sitemap = r.text
sitemap_links = re.findall('<loc>(.*?)</loc>', sitemap, re.IGNORECASE)

page_links = []


for sitemap_link in sitemap_links:
    r = requests.get(sitemap_link)
    sitemap = r.text
    page_links.extend(re.findall('<loc>(.*?)</loc>', sitemap, re.IGNORECASE))

links = []

for page_link in page_links:
    r = requests.get(page_link)
    content = r.text
    title = re.findall('<title>(.*?)</title>', content, re.IGNORECASE)
    page_title = html.unescape(title[0])
    links.append((page_title, page_link))


polish_links = filter(lambda link: LANG_PL in link[1], links)
english_links = filter(lambda link: LANG_EN in link[1], links)

markdown = '# [hazaybikes.com](https://hazaybikes.com/)\n'
markdown += 'Hazay is an electric cargo bike made in Poland. Eco-friendly and economical solution to urban commuting that will change your life! Discover our cargo bikes and accessories.\n\n'
markdown += '![Hazay Bikes](/assets/logo.png)\n\n'
markdown += '### Content (PL)\n'
markdown += '\n'.join(['* [%s](%s)' % link for link in polish_links])
markdown += '\n---\n'
markdown += '### Content (EN)\n'
markdown += '\n'.join(['* [%s](%s)' % link for link in english_links])
markdown += '\n'

with open('README.md', 'w') as f:
    f.write(markdown)