# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

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

from scrapy.item import Item, Field

class RawSpell(Item):
    name = Field()
    short_desc = Field()
    source = Field()
    level = Field()
    description = Field()
    school = Field()
    incanting = Field()
    components = Field()
    range = Field()
    effect = Field()
    target = Field()
    area = Field()
    target_or_effect_or_area = Field()
    target_or_area = Field()
    target_or_effect = Field()
    duration = Field()
    save = Field()
    spell_resistance = Field()
