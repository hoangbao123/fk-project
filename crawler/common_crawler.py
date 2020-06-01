from newsplease import NewsPlease
article = NewsPlease.from_url('https://news.sky.com/feature/us-election-2016-clinton-v-trump-10606061')
print(article.title)