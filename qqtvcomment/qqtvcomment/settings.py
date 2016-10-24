# -*- coding: utf-8 -*-

BOT_NAME = 'qqtvcomment'

SPIDER_MODULES = ['qqtvcomment.spiders']
NEWSPIDER_MODULE = 'qqtvcomment.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

#DOWNLOAD_DELAY = 3

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

ITEM_PIPELINES = {
   'qqtvcomment.pipelines.QqtvcommentPipeline': 300,
}

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'data'
MONGODB_DOCNAME = 'qqtv'
