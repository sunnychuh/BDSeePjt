# -*- coding: utf-8 -*-

# Scrapy settings for BDSeePjt project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'BDSeePjt'

SPIDER_MODULES = ['BDSeePjt.spiders']
NEWSPIDER_MODULE = 'BDSeePjt.spiders'

IPPOOL=[
	{"ipaddr":"113.200.214.164:9999"},
	{"ipaddr":"118.81.70.132:9797"},
	{"ipaddr":"163.125.253.245:9000"}
]

UAPOOL=[
	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Chrome/64.0"
]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'BDSeePjt (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'BDSeePjt.middlewares.BdseepjtSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'BDSeePjt.middlewares.BdseepjtDownloaderMiddleware': 543,
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':123,
    #'BDSeePjt.middlewares.httpProxyMiddleware':125,
    
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware':2,
    'BDSeePjt.middlewares.userAgentMiddleware':1
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'BDSeePjt.pipelines.BdseepjtPipeline': 300,
}

MONGODB_HOST = '127.0.0.1'
# 端口号，默认27017
MONGODB_PORT = 27017
# 设置数据库名称
MONGODB_DBNAME = 'BDSeeDB'
# 存放本数据的表名称
MONGODB_DOCNAME = 'tb_movielist'
# 存放本数据的表名称
MONGODB_DOCNAME_MOVIE_DETAIL = 'tb_movie_detail'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
