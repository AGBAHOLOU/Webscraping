# Scrapy settings for Projet project

BOT_NAME = "price"

SPIDER_MODULES = ["price.spiders"]
NEWSPIDER_MODULE = "price.spiders"

# User Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Disable robots.txt
ROBOTSTXT_OBEY = False
DUPEFILTER_DEBUG = True

# Configure request delays and concurrency
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Configure pipelines
ITEM_PIPELINES = {
    "price.pipelines.MySQLPipeline": 300,  
}

# AutoThrottle configuration
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# HTTP Cache configuration
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [500, 503, 504, 400, 403, 404]
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]

# Logging
LOG_LEVEL = "INFO"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
