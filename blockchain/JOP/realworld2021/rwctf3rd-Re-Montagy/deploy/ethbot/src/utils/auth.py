from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import conf.base as conf
import hashlib
import hmac
import json
import copy


# aes and hmac
def encrypt_then_mac(data, aes_key, hmac_key):
	cipher = AES.new(aes_key, AES.MODE_CBC)
	msg = cipher.iv + cipher.encrypt(pad(data, AES.block_size))
	sig = hmac.new(hmac_key, msg, hashlib.sha256).digest()
	token = b64encode(msg + sig).decode()
	return token


def validate_then_decrypt(token, aes_key, hmac_key):
	s = b64decode(token)
	msg, sig = s[:-32], s[-32:]
	assert sig == hmac.new(hmac_key, msg, hashlib.sha256).digest()
	iv, ct = msg[:16], msg[16:]
	cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
	data = unpad(cipher.decrypt(ct), AES.block_size)
	return data


# game account
def create_game_account(ctx):
	w3 = ctx['web3instance']
	acct = w3.eth.account.create("aHardPassword")
	_ctx = copy.deepcopy(ctx)
	del _ctx["web3instance"]
	_ctx['deployedcontracts'][acct.address] = {}

	string = json.dumps(_ctx)
	with open("db/env_deploy.json", 'w+') as f:
		f.write(string)
	return acct


def validate_game_account(ctx, data):
	w3 = ctx['web3instance']
	addr, priv_key = data[:-32], data[-32:]
	acct = w3.eth.account.from_key(priv_key)
	assert acct.address.encode() == addr
	return acct


def get_acc_nonce(ctx, _acct, ispending=conf.ispending):
	w3 = ctx['web3instance']
	if ispending:
		return [w3.eth.getTransactionCount(_acct.address, 'pending')]  # using list for transifor point
	else:
		return [w3.eth.getTransactionCount(_acct.address)]


def get_cont_addr(ctx, tx_hash):
	w3 = ctx['web3instance']
	tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
	assert tx_receipt != None
	return tx_receipt['contractAddress']


