# -*- encoding: utf-8 -*-
# written in python 2.7
__author__ = 'garzon'

import pickle
import hashlib, json, rsa, uuid, os
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)
#<hidden>
# this part is hidden from the contestants of the challenge for reducing unnecessary complexity
app.secret_key = 'tklrobjrwobn579g9fdt'
url_prefix = '/<string:prefix>'

valid_url_prefixs = {'6af948d659f0b7c5d3950a': '*ctf{5m@rt_c0n7raCt_0n_s1dechAin_546f93250dacb}'}

def FLAG():
	flag = valid_url_prefixs[request.user_prefix]#+session['genesis_block_hash'][4:8]+request.user_prefix[5:8]+session['genesis_block_hash'][12:16]
	try:
		with open('flag.log', 'ab') as f:
			f.write(request.remote_addr + '\n')
		try:
			with open('blockchain.log', 'ab') as f:
				f.write(json.dumps(session['blocks']) + '\n')
		except:
			with open('blockchain.log', 'ab') as f:
				f.write('FAILED ' + flag + '\n')
	except:
		return 'Something went ERROR, please contact admin of *CTF to get your flag'
	return 'Here is your flag: '+flag
	
original_app_route = app.route
def new_app_route(url_pattern, **kwargs):
	def __dummy(f):
		def _(*args, **kwargs):
			if kwargs['prefix'] not in valid_url_prefixs: return '404 NOT FOUND', 404
			request.user_prefix = kwargs['prefix']
			del kwargs['prefix']
			if len(args) == 0 and len(kwargs) == 0: return f()
			if len(kwargs) == 0: return f(*args)
			if len(args) == 0: return f(**kwargs)
			return f(*args, **kwargs)
		_.__name__ = str(uuid.uuid4())
		return original_app_route(url_pattern, **kwargs)(_)
	return __dummy
app.route = new_app_route
	
'''
#</hidden>
app.secret_key = '*********************'
url_prefix = '{{URL_PREFIX}}'

def FLAG():
	return 'Here is your flag: *ctf{******************}'
#<hidden>
'''
#</hidden>

def hash(x):
	return hashlib.sha256(hashlib.md5(x).digest()).hexdigest()
	
def hash_reducer(x, y):
	return hash(hash(x)+hash(y))
	
def has_attrs(d, attrs):
	if type(d) != type({}): raise Exception("Input should be a dict/JSON")
	for attr in attrs:
		if attr not in d:
			raise Exception("{} should be presented in the input".format(attr))

EMPTY_HASH = '0'*64

def addr_to_pubkey(address):
	return rsa.PublicKey(int(address, 16), 65537)
	
def pubkey_to_address(pubkey):
	assert pubkey.e == 65537
	hexed = hex(pubkey.n)
	if hexed.endswith('L'): hexed = hexed[:-1]
	if hexed.startswith('0x'): hexed = hexed[2:]
	return hexed
	
def gen_addr_key_pair():
	pubkey, privkey = rsa.newkeys(384)
	return pubkey_to_address(pubkey), privkey

#<hidden>
'''
#</hidden>
bank_address, bank_privkey = gen_addr_key_pair()
hacker_address, hacker_privkey = gen_addr_key_pair()
#<hidden>
'''
# this part is also hidden
KEY_FILENAME = 'blockchain.privkey'
if os.path.isfile(KEY_FILENAME):
	with open(KEY_FILENAME, 'rb') as f:
		obj = pickle.loads(f.read())
	bank_address, bank_privkey = obj['bank']
	hacker_address, hacker_privkey = obj['hacker']
else:
	bank_address, bank_privkey = gen_addr_key_pair()
	hacker_address, hacker_privkey = gen_addr_key_pair()
	obj = {'bank': [bank_address, bank_privkey], 'hacker': [hacker_address, hacker_privkey]}
	with open(KEY_FILENAME, 'wb') as f:
		f.write(pickle.dumps(obj))
#</hidden>

def sign_input_utxo(input_utxo_id, privkey):
	return rsa.sign(input_utxo_id, privkey, 'SHA-1').encode('hex')
	
def hash_utxo(utxo):
	return reduce(hash_reducer, [utxo['id'], utxo['addr'], str(utxo['amount'])])
	
def create_output_utxo(addr_to, amount):
	utxo = {'id': str(uuid.uuid4()), 'addr': addr_to, 'amount': amount}
	utxo['hash'] = hash_utxo(utxo)
	return utxo
	
def hash_tx(tx):
	return reduce(hash_reducer, [
		reduce(hash_reducer, tx['input'], EMPTY_HASH),
		reduce(hash_reducer, [utxo['hash'] for utxo in tx['output']], EMPTY_HASH)
	])
	
def create_tx(input_utxo_ids, output_utxo, privkey_from=None):
	tx = {'input': input_utxo_ids, 'signature': [sign_input_utxo(id, privkey_from) for id in input_utxo_ids], 'output': output_utxo}
	tx['hash'] = hash_tx(tx)
	return tx
	
def hash_block(block):
	return reduce(hash_reducer, [block['prev'], block['nonce'], reduce(hash_reducer, [tx['hash'] for tx in block['transactions']], EMPTY_HASH)])
	
def create_block(prev_block_hash, nonce_str, transactions):
	if type(prev_block_hash) == type(u''): prev_block_hash = str(prev_block_hash)
	if type(prev_block_hash) != type(''): raise Exception('prev_block_hash should be hex-encoded hash value')
	nonce = str(nonce_str)
	if len(nonce) > 128: raise Exception('the nonce is too long')
	block = {'prev': prev_block_hash, 'nonce': nonce, 'transactions': transactions}
	block['hash'] = hash_block(block)
	return block
	
def find_blockchain_tail(blocks=None):
	if blocks is None: blocks = session['blocks']
	return max(blocks.values(), key=lambda block: block['height'])
	
class SRC20SmartContract:
	def __init__(self, addr, privkey):
		self.starTokenNum = 0
		self.balanceOfAddr = {addr: 999999999}
		self.addr = addr
		self.privkey = privkey
		self.owned_token_utxos = {}
		
	def onCall_withdraw(self, tx):
		# by calling this you can convert your StarTokens into StarCoins!
		if len(tx['input']) == 1 and len(tx['output']) == 1 and len(tx['signature']) == 0 and tx['input'][0] in self.owned_token_utxos:
			# which means that you would like to redeem StarCoins in the input utxo using your StarTokens
			recv_addr = tx['output'][0]['addr']
			amount_to_redeem = self.owned_token_utxos[tx['input'][0]]['amount']
			self.sendTokenAtTx(tx, recv_addr, self.addr, amount_to_redeem)
			tx['signature'].append(sign_input_utxo(tx['input'][0], self.privkey))
		
	def onCall_buyTokens(self, utxos, tx):
		# by calling this you can buy some StarTokens using StarCoins!
		if len(tx['input']) == 1 and len(tx['output']) == 1 and tx['output'][0]['addr'] == self.addr:
			self.sendTokenAtTx(tx, self.addr, utxos[tx['input'][0]]['addr'], tx['output'][0]['amount'])
		
	def getTokenBalance(self, addr):
		if addr not in self.balanceOfAddr: return 0
		return self.balanceOfAddr[addr]
		
	def sendTokenAtTx(self, tx, from_addr, to_addr, amount):
		if self.getTokenBalance(from_addr) < amount: raise Exception("no enough StarToken at " + from_addr)
		if to_addr == self.addr:
			from_addr, to_addr = to_addr, from_addr
			amount = -amount
		utxo_used_to_record_SRCToken = create_output_utxo(to_addr, 0)
		obj = {'utxo_id': utxo_used_to_record_SRCToken['id'], 'tokenNum': amount}
		payload = json.dumps(obj)
		signature = self.signSRCTokenUtxoPayload(payload)
		info = signature + '$$$' + payload
		utxo_used_to_record_SRCToken['extra'] = info
		tx['output'].append(utxo_used_to_record_SRCToken)
		
	def signSRCTokenUtxoPayload(self, payload):
		return rsa.sign(payload, self.privkey, 'SHA-1').encode('hex')
		
	def verifySRCTokenUtxoPayload(self, payload, signature):
		try:
			return rsa.verify(payload, signature.decode('hex'), addr_to_pubkey(self.addr))
		except:
			return False
		
	def extractInfoFromUtxos(self, utxos):
		for utxo_id, utxo in utxos.items():
			if 'extra' in utxo:
				info = utxo['extra']
				if type(info) == type(u''): info = str(info)
				if type(info) != type(''): raise Exception("unknown type of 'extra' in utxo")
				if '$$$' not in info: raise Exception("signature of SRC20 token is not found")
				signature = info[:info.index('$$$')]
				payload = info[info.index('$$$')+3:]
				if not self.verifySRCTokenUtxoPayload(payload, signature): raise Exception("this SRC20 token is fake")
				obj = json.loads(payload)
				if obj['utxo_id'] != utxo['id']: raise Exception("the id of utxo does not match the one on the token")
				if utxo['addr'] not in self.balanceOfAddr: self.balanceOfAddr[utxo['addr']] = 0
				self.balanceOfAddr[utxo['addr']] += obj['tokenNum']
			if utxo['addr'] == self.addr: self.owned_token_utxos[utxo['id']] = utxo
		
	
def calculate_utxo(blockchain_tail):
	starToken_contract = SRC20SmartContract(bank_address, bank_privkey)
	curr_block = blockchain_tail
	blockchain = [curr_block]
	while curr_block['hash'] != session['genesis_block_hash']:
		curr_block = session['blocks'][curr_block['prev']]
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
		
def calculate_balance(utxos):
	balance = {bank_address: 0, hacker_address: 0}
	for utxo in utxos.values():
		if utxo['addr'] not in balance:
			balance[utxo['addr']] = 0
		balance[utxo['addr']] += utxo['amount']
	return balance

def verify_utxo_signature(address, utxo_id, signature):
	try:
		return rsa.verify(utxo_id, signature.decode('hex'), addr_to_pubkey(address))
	except:
		return False
	

def append_block(block, difficulty=int('f'*64, 16)):
	has_attrs(block, ['prev', 'nonce', 'transactions'])
	
	if type(block['prev']) == type(u''): block['prev'] = str(block['prev'])
	if type(block['nonce']) == type(u''): block['nonce'] = str(block['nonce'])
	if block['prev'] != find_blockchain_tail()['hash']: raise Exception("You do not have the dominant mining power so you can only submit tx to the last block.")
	tail = session['blocks'][block['prev']]
	utxos, contract = calculate_utxo(tail)
	
	if type(block['transactions']) != type([]): raise Exception('Please put a transaction array in the block')
	new_utxo_ids = set()
	for tx in block['transactions']:
		has_attrs(tx, ['input', 'output', 'signature'])
		
		for utxo in tx['output']:
			has_attrs(utxo, ['amount', 'addr', 'id'])
			if type(utxo['id']) == type(u''): utxo['id'] = str(utxo['id'])
			if type(utxo['addr']) == type(u''): utxo['addr'] = str(utxo['addr'])
			if type(utxo['id']) != type(''): raise Exception("unknown type of id of output utxo")
			if utxo['id'] in new_utxo_ids: raise Exception("output utxo of same id({}) already exists.".format(utxo['id']))
			new_utxo_ids.add(utxo['id'])
			if type(utxo['amount']) != type(1): raise Exception("unknown type of amount of output utxo")
			if utxo['amount'] < 0: raise Exception("invalid amount of output utxo")
			if type(utxo['addr']) != type(''): raise Exception("unknown type of address of output utxo")
			try:
				addr_to_pubkey(utxo['addr'])
			except:
				raise Exception("invalid type of address({})".format(utxo['addr']))
			utxo['hash'] = hash_utxo(utxo)
		
		for new_id in new_utxo_ids:
			if new_id in utxos:
				raise Exception("invalid id of output utxo. utxo id({}) exists".format(utxo_id))
				
		if type(tx['input']) != type([]): raise Exception("type of input utxo ids in tx should be array")
		if type(tx['signature']) != type([]): raise Exception("type of input utxo signatures in tx should be array")
		
		tx['input'] = [str(i) if type(i) == type(u'') else i for i in tx['input']]
		for utxo_id in tx['input']:
			if type(utxo_id) != type(''): raise Exception("unknown type of id of input utxo")
			if utxo_id not in utxos: raise Exception("invalid id of input utxo. Input utxo({}) does not exist or it has been consumed.".format(utxo_id))
				
		if contract is not None:
			if 'call_smart_contract' in tx:
				if tx['call_smart_contract'] == 'buyTokens': contract.onCall_buyTokens(utxos, tx)
				if tx['call_smart_contract'] == 'withdraw': contract.onCall_withdraw(tx)
		
		tot_input = 0
		if len(tx['input']) != len(tx['signature']): raise Exception("lengths of arrays of ids and signatures of input utxos should be the same")
		tx['signature'] = [str(i) if type(i) == type(u'') else i for i in tx['signature']]
		for utxo_id, signature in zip(tx['input'], tx['signature']):
			utxo = utxos[utxo_id]
			if type(signature) != type(''): raise Exception("unknown type of signature of input utxo")
			if not verify_utxo_signature(utxo['addr'], utxo_id, signature):
				raise Exception("Signature of input utxo is not valid. You are not the owner of this input utxo({})!".format(utxo_id))
			tot_input += utxo['amount']
			del utxos[utxo_id]
			
		tot_output = sum([utxo['amount'] for utxo in tx['output']])
		if tot_output > tot_input:
			raise Exception("You don't have enough amount of StarCoins in the input utxo! {}/{}".format(tot_input, tot_output))
		tx['hash'] = hash_tx(tx)
	
	block = create_block(block['prev'], block['nonce'], block['transactions'])
	block_hash = int(block['hash'], 16)
	#We are users in this challenge, so leave the Proof-of-Work thing to the non-existent miners
	#if block_hash > difficulty: raise Exception('Please provide a valid Proof-of-Work')
	block['height'] = tail['height']+1
	if len(session['blocks']) > 10: raise Exception('The blockchain is too long. Use ./reset to reset the blockchain')
	if block['hash'] in session['blocks']: raise Exception('A same block is already in the blockchain')
	session['blocks'][block['hash']] = block
	session.modified = True
	
def init():
	if 'blocks' not in session:
		session['blocks'] = {}
	
		# At first, the bank issued some StarCoins, and give you 100
		currency_issued = create_output_utxo(bank_address, 200)
		airdrop = create_output_utxo(hacker_address, 100)
		genesis_transaction = create_tx([], [currency_issued, airdrop]) # create StarCoins from nothing
		genesis_block = create_block(EMPTY_HASH, 'The Times 03/Jan/2009 Chancellor on brink of second bailout for bank', [genesis_transaction])
		
		session['genesis_block_hash'] = genesis_block['hash']
		genesis_block['height'] = 0
		session['blocks'][genesis_block['hash']] = genesis_block
		
		
def get_balance_of_all():
	init()
	tail = find_blockchain_tail()
	utxos, contract = calculate_utxo(tail)
	return calculate_balance(utxos), utxos, tail, contract
	
@app.route(url_prefix+'/')
def homepage():
	announcement = ''
	balance, utxos, _, contract = get_balance_of_all()
	genesis_block_info = 'hash of genesis block: ' + session['genesis_block_hash']
	addr_info = 'the bank\'s addr: ' + bank_address + ', your addr: ' + hacker_address + ', your privkey: ' + pickle.dumps(hacker_privkey).encode('hex')
	balance_info = 'StarCoins balance of all addresses: ' + json.dumps(balance)
	starcoins_utxo_info = 'All utxos: ' + json.dumps(utxos)
	startokens_info = 'StarTokens balance of all addresses: ' + json.dumps(contract.balanceOfAddr)
	blockchain_info = 'Blockchain Explorer: ' + json.dumps(session['blocks'])
	view_source_code_link = "<a href='source_code'>View source code</a>"
	return announcement+('.<br /><br />\r\n\r\n'.join([view_source_code_link, genesis_block_info, addr_info, balance_info, starcoins_utxo_info, startokens_info, blockchain_info]))
	

DIFFICULTY = int('00000' + 'f' * 59, 16)
@app.route(url_prefix+'/create_block', methods=['POST'])
def create_block_api():
	init()
	try:
		block = json.loads(request.data)
		append_block(block, DIFFICULTY)
		msg = 'transaction finished.'
	except Exception, e:
		return str(e)
		
	balance, utxos, tail, contract = get_balance_of_all()
	
	if balance[hacker_address] == 200:
		msg += ' Congratulations~ ' + FLAG()
	return msg
	
		
# if you mess up the blockchain, use this to reset the blockchain.
@app.route(url_prefix+'/reset')
def reset_blockchain():
	if 'blocks' in session: del session['blocks']
	if 'genesis_block_hash' in session: del session['genesis_block_hash']
	return 'reset.'
	
@app.route(url_prefix+'/source_code')
def show_source_code():
	source = open('serve.py', 'r')
	html = ''
	#<hidden>
	is_hidden = False
	#</hidden>
	for line in source:
		line = line.decode('utf8', 'ignore')
		#<hidden>
		if line.strip() == '#</hidden>':
			is_hidden = False
			continue
		if line.strip() == '#<hidden>':
			is_hidden = True
		if is_hidden: continue
		line = line.replace('{{URL_PREFIX}}', '/'+request.user_prefix)
		#</hidden>
		html += line.replace('&','&amp;').replace('\t', '&nbsp;'*4).replace(' ','&nbsp;').replace('<', '&lt;').replace('>','&gt;').replace('\n', '<br />')
	source.close()
	return html
	
if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=10012)


