# -*- encoding: utf-8 -*-
# written in python 2.7
__author__ = 'garzon'

import requests, json, hashlib, rsa, pickle, uuid

from serve import *

# do some modifications to the original one to remove 'session' variable and privkey
def calculate_utxo(blocks, bankAddr, blockchain_tail):
	starToken_contract = SRC20SmartContract(bankAddr, 0)
	curr_block = blockchain_tail
	blockchain = [curr_block]
	while curr_block['height'] != 0:
		curr_block = blocks[curr_block['prev']]
		blockchain.append(curr_block)
	blockchain = blockchain[::-1]
	utxos = {}
	for block in blockchain:
		for tx in block['transactions']:
			for input_utxo_id in tx['input']:
				del utxos[input_utxo_id]
			for utxo in tx['output']:
				utxos[utxo['id']] = utxo
	starToken_contract.extractInfoFromUtxos(utxos)
	return utxos, starToken_contract

# ==============

def create_output_utxo(addr_to, amount):
	utxo = {'id': str(uuid.uuid4()), 'addr': addr_to, 'amount': amount}
	utxo['hash'] = hash_utxo(utxo)
	return utxo

def find_inner_str(haystack, st, ed=None):
	haystack = haystack[haystack.index(st)+len(st):]
	if ed is None: return haystack
	return haystack[:haystack.index(ed)]
	
def append_block(block):
	print '[APPEND]', s.post(url_prefix+'/create_block', data=json.dumps(block)).text
	
is_first_time = True
def show_blockchain():
	global is_first_time
	ret = s.get(url_prefix+'/').text
	#print ret.replace('<br />','')
	tokens = json.loads(find_inner_str(ret, 'StarTokens balance of all addresses: ', '.'))
	balance = json.loads(find_inner_str(ret, 'StarCoins balance of all addresses: ', '.'))
	if not is_first_time:
		print '[tokens = {}, balance = {}]'.format(tokens.get(my_address, 0), balance[my_address])
	is_first_time = False
	return ret, json.loads(find_inner_str(ret, 'Blockchain Explorer: '))
	
def redeem(bank_owned_utxo_id, tail, amount, nonce):
	output_to_get_starcoins = create_output_utxo(my_address, amount)
	tx = create_tx([bank_owned_utxo_id], [output_to_get_starcoins], my_privkey) # my_privkey is dummy, the signature will be overwritten
	tx['signature'] = [] # remains the field to be filled by smart contract
	tx['call_smart_contract'] = 'withdraw'
	block = create_block(tail['hash'], nonce, [tx])
	append_block(block)
	return output_to_get_starcoins
	
def buyTokens(utxoIdPaid, tail, amount, contractAddr, nonce):
	output_to_get_tokens = create_output_utxo(contractAddr, amount)
	tx = create_tx([utxoIdPaid], [output_to_get_tokens], my_privkey)
	tx['call_smart_contract'] = 'buyTokens'
	block = create_block(tail['hash'], nonce, [tx])
	append_block(block)
	return output_to_get_tokens

url_prefix = 'http://47.75.9.127:10012/6af948d659f0b7c5d3950a'
s = requests.session()

# 100 starcoins
resp, blocks = show_blockchain()
my_address, my_privkey = find_inner_str(resp, 'your addr: ', ','), pickle.loads(find_inner_str(resp, 'your privkey: ', '.').decode('hex'))
bankAddr = find_inner_str(resp, 'the bank\'s addr: ', ',')

tail = find_blockchain_tail(blocks)
utxos, contract = calculate_utxo(blocks, bankAddr, tail)
for utxo in utxos.values():
	if utxo['addr'] == my_address: my_utxo = utxo # find the utxo of 100 starcoins 
	if utxo['addr'] == bankAddr: coinsIssued = utxo
first100TokenBankOwned = buyTokens(my_utxo['id'], tail, 100, contract.addr, 'step1')

# 100 tokens
resp, blocks = show_blockchain()
tail = find_blockchain_tail(blocks)
utxos, contract = calculate_utxo(blocks, bankAddr, tail)
for utxo in utxos.values():
	if utxo['addr'] == my_address:
		break
my_first_100_tokens_utxo_id = utxo['id']
my_100_starcoins = redeem(first100TokenBankOwned['id'], tail, 100, 'step2')

# 100 starcoins, 100 - 100 tokens
resp, blocks = show_blockchain()
tail = find_blockchain_tail(blocks)
utxos, contract = calculate_utxo(blocks, bankAddr, tail)
for utxo in utxos.values():
	if utxo['addr'] == my_address and utxo['id'] != my_first_100_tokens_utxo_id and utxo['amount'] == 0:
		break # find the utxo of -100 tokens
output_to_send_minus_100_token = create_output_utxo(bankAddr, 0)
tx = create_tx([utxo['id']], [output_to_send_minus_100_token], my_privkey)
block = create_block(tail['hash'], 'step3', [tx])
append_block(block)

# 100 starcoins, 100 tokens, but the bank now just own a utxo of 200 starcoins, we need 200 tokens to redeem that utxo
resp, blocks = show_blockchain()
tail = find_blockchain_tail(blocks)
buyTokens(my_100_starcoins['id'], tail, 100, contract.addr, 'step4')

# 200 tokens to exchange the utxo of 200 starcoins owned by the bank initially
resp, blocks = show_blockchain()
tail = find_blockchain_tail(blocks)
redeem(coinsIssued['id'], tail, 200, 'step5')