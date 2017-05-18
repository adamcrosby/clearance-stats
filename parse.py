#!/usr/bin/env python

from bs4 import BeautifulSoup
from collections import Counter
import urllib2
import pprint

START_YEAR = 1996
END_YEAR = 2017
class DOHACase(object):
	date = ""
	disposition = ""
	keywords = []
	digest = ""

keyword_data = {}

def parse_file(soup):
	soup = soup.find_all('div', class_='case')
	cases = []
	favorable = ["clearance is granted",
		"adverse decision remanded",
		"adverse decision reversed",
		"adverse decision is unsupported",
		"adverse decision is unsupportable",
		"clearance continued",
		"is granted",
		"clearance granted",
		"public trust postition granted",
		'favorable decision affirmed']

	unfavorable = ['clearance is denied',
		'clearance denied',
		'clearance is revoked',
		'information is revoked',
		'adverse decision is supported',
		'adverse decision is supportable',
		'adverse decision affirmed',
		'favorable decision reversed',
		'favorable decision remanded',
		'clearance revoked',
		'is denied',
		'fails to mitigate',
		'are not mitigated',
		'did not mitigate',
		'position denied']

	indeterminate = ['case remanded with instruction', 'unfavorable decision is vacated']

	for case in soup:
		dohacase = DOHACase()
		dohacase.date = case.find('p', class_='date').get_text().strip()
		kw = case.find('div', class_='keywords').get_text()
		kw = kw.replace(';', '|').replace(':', '|').lower()
		dohacase.keywords = [x.strip() for x in kw.split('|')]
		dohacase.digest = case.find('p', class_='digest')

		try:
			dohacase.disposition = "Unknown"
			for item in favorable:
				if dohacase.digest.get_text().lower().replace('\n', ' ').find(item) > 0:
					dohacase.disposition = "Favorable"
			for item in unfavorable:
				if dohacase.digest.get_text().lower().replace('\n', ' ').find(item) > 0:
					dohacase.disposition = "Unfavorable"
			for item in indeterminate:
				if dohacase.digest.get_text().lower().replace('\n', ' ').find(item) > 0:
					dohacase.disposition = "Indeterminate"
		except AttributeError, e:
			pass
		cases.append(dohacase)
		
	return cases

def get_year(x):
	url = "http://ogc.osd.mil/doha/industrial/%s.html"
	opener = urllib2.build_opener()
	# OGC DOHA website is now filtering by useragent....which is silly.
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open(url % x)
	page = response.read()
	soup = BeautifulSoup(page)
	cases = parse_file(soup)
	return cases

overall_favorable = Counter()
overall_unfavorable = Counter()
overall_indeterminate = Counter()
years = {}
for x in xrange(START_YEAR, END_YEAR+1):
	year_favorable = Counter()
	year_unfavorable = Counter()
	year_indeterminate = Counter()
	
	cases = get_year(x)	
	for case in cases:
		if case.disposition == "Favorable":
			for k in case.keywords:
				if k in year_favorable.keys():
					year_favorable[k] = year_favorable[k] + 1
				else:
					year_favorable[k] = 1
		elif case.disposition == "Unfavorable":
			for k in case.keywords:
				if k in year_unfavorable.keys():
					year_unfavorable[k] = year_unfavorable[k] + 1
				else:
					year_unfavorable[k] = 1
		elif case.disposition == "Indeterminate":
			for k in case.keywords:
				if k in year_indeterminate.keys():
					year_indeterminate[k] = year_indeterminate[k] + 1
				else:
					year_indeterminate[k] = 1
	overall_indeterminate = overall_indeterminate + year_indeterminate
	overall_unfavorable = overall_unfavorable + year_unfavorable
	overall_favorable = overall_favorable + year_favorable
	print x, year_favorable, year_unfavorable
	years[x] = (year_favorable, year_unfavorable, year_indeterminate)
pp = pprint.PrettyPrinter(indent=4)

print "For years %s - %s:" % (START_YEAR, END_YEAR)
print "Cases found Favorable for Applicant:"
for k in sorted(overall_favorable, key=overall_favorable.get):
	print "\t%s\t%s" % (overall_favorable[k], k)
print "Cases found Unfavorable for Applicant:"
for i in sorted(overall_unfavorable, key=overall_unfavorable.get):
	print "\t%s\t%s" % (overall_unfavorable[i], i)
