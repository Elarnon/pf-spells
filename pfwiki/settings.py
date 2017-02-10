# Scrapy settings for pfwiki project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

'''
    
    Copyright (C) 2016 Basile Clement <basile-licensing@clement.pm>
    
    pf-spells is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    pf-spells is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

BOT_NAME = 'pfwiki'

SPIDER_MODULES = ['pfwiki.spiders']
NEWSPIDER_MODULE = 'pfwiki.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pfwiki (+http://www.yourdomain.com)'
