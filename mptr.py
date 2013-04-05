#!/usr/bin/env python

from __future__ import print_function, unicode_literals
from lxml import etree
from urlparse import urljoin
from operator import attrgetter
from datetime import datetime
from itertools import imap, ifilter
from collections import namedtuple
import requests

TRACK_ENTRY = namedtuple('TrackEntry', ('timestamp', 'place', 'info'))
HTML_PARSER = etree.HTMLParser()
STATIC_VALUES = """javax.faces.source:nyomkoveto:pushBtnActionList
javax.faces.partial.event:click
javax.faces.partial.execute:@all
javax.faces.partial.render:@all
ice.focus:nyomkoveto:pushBtnActionList_span-button
ice.event.target:
ice.event.captured:nyomkoveto:pushBtnActionList
ice.event.type:onclick
ice.event.alt:false
ice.event.ctrl:false
ice.event.shift:false
ice.event.meta:false
ice.event.x:864
ice.event.y:1558
ice.event.left:true
ice.event.right:false
ice.submit.type:ice.s
ice.submit.serialization:form
javax.faces.partial.ajax:true"""

def main():
	from sys import argv, stderr
	try:
		number = argv[1]
	except IndexError:
		print('Usage: {0} <tracking number>'.format(argv[0]), file=stderr)
		raise SystemExit(1)
	else:
		for entry in track_item_iter(number):
			print('\t'.join((entry.timestamp.isoformat(), entry.place, entry.info)))


def track_item(number):
	return list(track_item_iter(number))


def track_item_iter(number):
	session = requests.session()
	resp = session.get('http://posta.hu/ugyfelszolgalat/nyomkovetes')
	tree = etree.fromstring(resp.content, HTML_PARSER)
	(form,) = tree.xpath('//form[@name="nyomkoveto"]')

	data = {a['name']: a.get('value', '') for a in
			imap(attrgetter('attrib'), form.xpath('.//input'))}

	for row in STATIC_VALUES.split('\n'):
		key, value = row.strip().split(':', 1)
		data[key] = value

	data['nyomkoveto:documentnumber:input'] = number

	resp = session.post(urljoin(resp.url, form.attrib['action']),
			data=data, headers={'Referer': resp.url})
	tree = etree.fromstring(resp.content, HTML_PARSER)

	for row in tree.xpath('//table')[0].xpath('tbody/tr'):
		timestamp = datetime.strptime(''.join(ifilter(None, imap(unicode.strip, imap(unicode,
			row.xpath('td[@class="date"]//text()'))))), '%Y.%m.%d%H:%M')
		(place_td,) = row.xpath('td[@class="place"]')
		(place,) = place_td.xpath('span/text()')
		info = ''.join(ifilter(None, imap(unicode.strip, imap(unicode, place_td.xpath('p//text()')))))
		yield TRACK_ENTRY(timestamp=timestamp, place=place, info=info)


if __name__ == '__main__':
	main()
