# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

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
