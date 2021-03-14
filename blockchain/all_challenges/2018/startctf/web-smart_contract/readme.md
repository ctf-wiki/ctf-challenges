## Smart? Contract
http://47.75.9.127:10012/6af948d659f0b7c5d3950a/
Yet another blockchain challenge with tokens in the smart contract. Be careful that the blockchain is stored in the cookie and a browser might ignore set-cookie header if it is too long, which prevents the blockchain being updated. So send the requests using scripts.

## Flag
*ctf{5m@rt_c0n7raCt_0n_s1dechAin_546f93250dacb}

## 依赖

`pip install rsa gunicorn`

## 部署

python serve.py 同时生成privkey

### 多worker - 正式CTF模式

启动：gunicorn -w 4 -b 0.0.0.0:10012 serve:app --log-level=warning --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Real-IP}i)s"' --access-logfile gunicorn.log --error-logfile gunicorn_error.log -D

杀进程：pkill -9 -f gunicorn
