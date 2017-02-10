# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from pfwiki.items import RawSpell
from scrapy.log import CRITICAL, WARNING

registres = [
    u'acide', u'air', u'bien', u'chaos', u'langage', u'douleur',
    u'eau', u'mental', u'électricité', u'émotion', u'feu', u'force',
    u'froid', u'loi', u'lumière', u'mal', u'maladie', u'malédiction', u'mort',
    u'ombre', u'peur', u'poison', u'sonore', u'ténèbres', u'terre',
    # Unsure
    u'terreur', u'obscurité', u'son',
]

branches = {
    u'Abjuration': [],
    u'Divination': [u'scrutation'],
    u'Enchantement': [u'charme', u'coercition'],
    u'Évocation': [],
    u'Illusion': [u'chimère', u'fantasme', u'hallucination', u'mirage', u'ombre'],
    u'Invocation': [u'appel', u'convocation', u'création', u'guérison', u'téléportation'],
    u'Nécromancie': [],
    u'Transmutation': [u'métamorphose']
}

class PathfinderFRSpellsSpider(BaseSpider):
    name = "pathfinder-fr-spells"
    allowed_domains = ["pathfinder-fr.org"]
    start_urls = [
        "http://www.pathfinder-fr.org/Wiki/Pathfinder-RPG.Liste%20des%20sorts.ashx",
        "http://www.pathfinder-fr.org/Wiki/Pathfinder-RPG.Liste%20des%20sorts%20(suite).ashx",
        "http://www.pathfinder-fr.org/Wiki/Pathfinder-RPG.Liste%20des%20sorts%20(fin).ashx",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        spells = hxs.select('//li/b/i/a')
        base = '/'.join(response.url.split('/')[:-1]) + '/'
        for spell in spells:
            link = ''.join(spell.select('@href').extract()).strip()
            desc = ''.join(spell.select('../../..//text()').re('\)\.(.*)')).strip()
            request = Request(base + link, callback=self.parse_spell)
            request.meta['short_desc'] = desc
            yield request

    def parse_spell(self, response):
        hxs = HtmlXPathSelector(response)
        content = hxs.select('id("PageContentDiv")')
        res = RawSpell(
            short_desc=response.meta['short_desc'],
            name=''.join(hxs.select(
                '//h1[@class="pagetitle"]//text()'
            ).extract()).strip()
        )
        src = ''.join(''.join(''.join(content.select(
            './/img[@class="opachover"]/@src'
        ).extract()).upper().split('/')[-1:]).split('.')[:-1])
        if 'APG' in src:
            res['source'] = 'APG'
        elif 'UM' in src:
            res['source'] = 'UM'
        elif 'UC' in src:
            res['source'] = 'UC'
        elif src == '':
            res['source'] = 'CRB'
        else:
            self.log('Unknown source (%s).' % response.url, level=WARNING)
        fields = content.select(
            'b[not(preceding-sibling::br[following-sibling::*[1][self::br]])]' +
            '/text()'
        ).extract()
        for field in fields:
            value = ''.join(content.select((
                u'b[text()="%s"]/following-sibling::*[self::b or self::br][1]/' +
                u'preceding-sibling::node()[preceding-sibling::b[text()="%s"]]' +
                u'/descendant-or-self::text()'
            ) % (field, field)).extract()).strip().strip(';').strip()
            field = field.replace(u'’', '\'').strip()
            if u'École' == field:
                res['school'] = value
                # school = value.split(' ', 1)
                # res['school'] = school[0]
                # after = []
                # if len(school) > 1:
                #     after = re.findall('[[(][^])]+[])]', school[1])
                # descriptors = []
                # subschool = None
                # if len(after) == 1:
                #     after = after[0].strip()
                #     if after[0] == '[' and after[-1] == ']':
                #         descriptors = after[1:-1].split(',')
                #     elif after[0] == '(' and after[-1] == ')':
                #         subschool = after[1:-1]
                # elif len(after) == 2:
                #     subschool = after[0][1:-1]
                #     descriptors = after[1][1:-1].split(',')
                # elif len(after) > 2:
                #     self.log(
                #         'Too many subschools/descriptors (%s).' % response.url,
                #         level=WARNING
                #     )
                # res['subschool'] = subschool
                # res['descriptors'] = descriptors
            elif u'Niveau' == field:
                res['level'] = {}
                for info in value.strip().split(','):
                    cls, lvl = info.split()
                    res['level'][cls.strip().capitalize()] = int(lvl)
            elif u'Temps d\'incantation' == field:
                res['incanting'] = value
            elif u'Effet' == field:
                res['effect'] = value
            elif field in [u'Zone d\'effet', u'Zone']:
                res['area'] = value
            elif field in [u'Cible, effet ou zone d\'effet']:
                res['target_or_effect_or_area'] = value
            elif field in [u'Cible ou zone d\'effet', u'Zone d\'effet ou cible']:
                res['target_or_area'] = value
            elif field in [u'Cibles ou effet']:
                res['target_or_effect'] = value
            elif field == u'Cible et zone d\'effet':
                both = value.split(' et ')
                res['target'] = both[0].strip()
                res['area'] = both[1].strip()
            elif u'Composantes' == field:
                res['components'] = value
            elif u'Portée' == field:
                res['range'] = value
            elif field in [u'Cible', u'Cibles']:
                res['target'] = value
            elif u'Durée' == field:
                res['duration'] = value
            elif u'Jet de sauvegarde' == field:
                res['save'] = value.lower()
            elif u'Résistance à la magie' == field:
                res['spell_resistance'] = value.lower()
            else:
                self.log(
                    'Unknown field %s @ %s' % (field, response.url),
                    level=WARNING
                )
        # TODO: box "similaire à ..."
        res['description'] = ''.join(content.select(
            'br[preceding-sibling::*[1][self::br]][1]/' +
            'following-sibling::node()'
        ).extract()).strip()
        return res
