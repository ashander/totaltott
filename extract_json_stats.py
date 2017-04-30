import fileinput
import re
import json
from collections import OrderedDict

redict  = [
	('applications',
	 r"(?P<{}>[0-9]+) [aA]pp"),
	('interviews',
	 r"(?P<{}>[0-9]+) [iI]nt"),
	('visits',
	 r"(?P<{}>[0-9]+) (.?.?.?[cC]ampus )?[vV]is"),
	('offers',
	 r"(?P<{}>[0-9]+) [oO]ff"),  # NOTE replacing encolsing "" with a ( )?" will expand coverage to non-complete cases
]
restr = r".+".join([e.format(n) for n, e in redict])
reost = re.compile(restr)

renost = re.compile(r"(?P<applications>[0-9]{1,3}), (?P<interviews>[0-9]{1,2}), (?P<visits>[0-9]{1,2}), (?P<offers>[0-9]{1,2})")
year = re.compile(r"(19(8|9)[0-9]|20(0|1)[0-9]),")

url = re.compile(r"[0-9]{8,9}[0-9]*")

class Processor(object):
	def __init__(self):
		self.data = OrderedDict()
		self.data['url'] = None
		self

	@property
	def url(self):
		return self.data['url']

	@url.setter
	def url(self, value):
		self.data['url'] = value
		
	def clearid(self):
		self.data['url'] = None

	def find_url(self, line):
		m = url.search(line)
		if m:
			self.url = m.group(0)

	def write_with_url(self):
		self.data['url']  = 'https://twitter.com/-/status/' + self.url  # actual username don't matter
		self.convert() # write int
		self.write()
		self.clearid()

	def convert(self):
		tmp = self.data.pop('url')
		for k, v in self.data.items():
			try:
				self.data[k] = int(v)
			except:
				self.data[k] = v
		self.data['url'] = tmp

	def write(self):
		print(json.dumps(self.data, sort_keys=True))

	def __call__(self, line):
		if not self.url:
			self.find_url(line)
			return
		
		y = year.search(line)
		if y:
			yr = y.group(1)
			line  = line.replace(yr, "ZZZZZZZZZ")
			self.data['year'] = yr

		m = reost.search(line)
		ms = renost.search(line)
		if m:
			self.data.update(m.groupdict(default=""))
		elif ms:
			self.data.update(ms.groupdict(default=""))
		else:
			# TODO with urls uncoment
			self.clearid()
			return
		self.write_with_url()



if __name__ == '__main__':
        # cat tenure_* |grep -v "RT @"| jq ".id_str, .text" | python THISFILE
	p = Processor()
	for line in fileinput.input():
		p(line)
