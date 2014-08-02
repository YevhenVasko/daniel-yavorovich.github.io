#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Даниэль Яворович'
SITENAME = u'Сон наяву'
SITEURL = 'http://yavorovych.com'

TIMEZONE = 'Europe/Kiev'

DEFAULT_LANG = u'ru'

# Feed generation is usually not desired when developing

FEED_ALL_ATOM = "feeds/all.atom.xml"
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Hosting for Django', 'https://hosting4django.net/'),
	 )

# Social widget
SOCIAL = (('github', 'https://github.com/daniel-yavorovich'),
	 )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
THEME = "theme"

DISQUS_SITENAME = "danielyavorovichblog"
GITHUB_URL = "https://github.com/daniel-yavorovich"

STATIC_PATHS = ['images', 'extra/CNAME', 'extra/README']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'}, 'extra/README': {'path': 'README'}}
