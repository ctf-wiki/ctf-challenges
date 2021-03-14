import json
import copy
from conf.base import providerOfNetwork
import random
import string


def dumps_env(_ctx):
	ctx = copy.deepcopy(_ctx)
	del ctx["web3instance"]
	string = json.dumps(ctx)
	with open("db/env_deploy.json", 'w+') as f:
		f.write(string)


def loads_env():
	# connect to node
	from web3 import Web3
	from web3.middleware import geth_poa_middleware

	w3 = Web3(Web3.HTTPProvider(providerOfNetwork))
	w3.middleware_onion.inject(geth_poa_middleware, layer=0)

	with open("db/env_deploy.json", 'r+') as f:
		ctx = json.loads(f.read())
	ctx['web3instance'] = w3
	return ctx

def randhex(length):
	return ''.join([random.choice(string.hexdigits) for i in range(length)]).lower()