# -*- encoding: utf-8 -*-
# written in python 2.7
__author__ = 'garzon'

import hashlib, json, rsa, uuid, os
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)
app.secret_key = '*********************'
url_prefix = '/b942f830cf97e'

def FLAG():
    return 'Here is your flag: DDCTF{******************}'

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

bank_address, bank_privkey = gen_addr_key_pair()
hacker_address, hacker_privkey = gen_addr_key_pair()
shop_address, shop_privkey = gen_addr_key_pair()
shop_wallet_address, shop_wallet_privkey = gen_addr_key_pair()

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
    if type(prev_block_hash) != type(''): raise Exception('prev_block_hash should be hex-encoded hash value')
    nonce = str(nonce_str)
    if len(nonce) > 128: raise Exception('the nonce is too long')
    block = {'prev': prev_block_hash, 'nonce': nonce, 'transactions': transactions}
    block['hash'] = hash_block(block)
    return block
    
def find_blockchain_tail():
    return max(session['blocks'].values(), key=lambda block: block['height'])
    
def calculate_utxo(blockchain_tail):
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
    return utxos
        
def calculate_balance(utxos):
    balance = {bank_address: 0, hacker_address: 0, shop_address: 0}
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
    if block['prev'] not in session['blocks']: raise Exception("unknown parent block")
    tail = session['blocks'][block['prev']]
    utxos = calculate_utxo(tail)
    
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
            if utxo['amount'] <= 0: raise Exception("invalid amount of output utxo")
            if type(utxo['addr']) != type(''): raise Exception("unknown type of address of output utxo")
            try:
                addr_to_pubkey(utxo['addr'])
            except:
                raise Exception("invalid type of address({})".format(utxo['addr']))
            utxo['hash'] = hash_utxo(utxo)
        tot_output = sum([utxo['amount'] for utxo in tx['output']])
        
        if type(tx['input']) != type([]): raise Exception("type of input utxo ids in tx should be array")
        if type(tx['signature']) != type([]): raise Exception("type of input utxo signatures in tx should be array")
        if len(tx['input']) != len(tx['signature']): raise Exception("lengths of arrays of ids and signatures of input utxos should be the same")
        tot_input = 0
        tx['input'] = [str(i) if type(i) == type(u'') else i for i in tx['input']]
        tx['signature'] = [str(i) if type(i) == type(u'') else i for i in tx['signature']]
        for utxo_id, signature in zip(tx['input'], tx['signature']):
            if type(utxo_id) != type(''): raise Exception("unknown type of id of input utxo")
            if utxo_id not in utxos: raise Exception("invalid id of input utxo. Input utxo({}) does not exist or it has been consumed.".format(utxo_id))
            utxo = utxos[utxo_id]
            if type(signature) != type(''): raise Exception("unknown type of signature of input utxo")
            if not verify_utxo_signature(utxo['addr'], utxo_id, signature):
                raise Exception("Signature of input utxo is not valid. You are not the owner of this input utxo({})!".format(utxo_id))
            tot_input += utxo['amount']
            del utxos[utxo_id]
        if tot_output > tot_input:
            raise Exception("You don't have enough amount of DDCoins in the input utxo! {}/{}".format(tot_input, tot_output))
        tx['hash'] = hash_tx(tx)
    
    block = create_block(block['prev'], block['nonce'], block['transactions'])
    print block['prev'], block['nonce'], block['transactions']
    print 'blockhash',block['hash']
    block_hash = int(block['hash'], 16)
    print 'blockhash',block_hash
    if block_hash > difficulty: raise Exception('Please provide a valid Proof-of-Work')
    block['height'] = tail['height']+1
    if len(session['blocks']) > 50: raise Exception('The blockchain is too long. Use ./reset to reset the blockchain')
    if block['hash'] in session['blocks']: raise Exception('A same block is already in the blockchain')
    session['blocks'][block['hash']] = block
    print 'append success!', block['hash']
    session.modified = True
    
def init():
    if 'blocks' not in session:
        session['blocks'] = {}
        session['your_diamonds'] = 0
    
        # First, the bank issued some DDCoins ...
        total_currency_issued = create_output_utxo(bank_address, 1000000)
        genesis_transaction = create_tx([], [total_currency_issued]) # create DDCoins from nothing
        genesis_block = create_block(EMPTY_HASH, 'The Times 03/Jan/2009 Chancellor on brink of second bailout for bank', [genesis_transaction])
        session['genesis_block_hash'] = genesis_block['hash']
        genesis_block['height'] = 0
        session['blocks'][genesis_block['hash']] = genesis_block
        
        # Then, the bank was hacked by the hacker ...
        handout = create_output_utxo(hacker_address, 999999)
        reserved = create_output_utxo(bank_address, 1)
        transferred = create_tx([total_currency_issued['id']], [handout, reserved], bank_privkey)
        second_block = create_block(genesis_block['hash'], 'HAHA, I AM THE BANK NOW!', [transferred])
        append_block(second_block)
        
        # Can you buy 2 diamonds using all DDCoins?
        third_block = create_block(second_block['hash'], 'a empty block', [])
        append_block(third_block)
        
def get_balance_of_all():
    init()
    tail = find_blockchain_tail()
    utxos = calculate_utxo(tail)
    return calculate_balance(utxos), utxos, tail
    
@app.route(url_prefix+'/')
def homepage():
    announcement = 'Announcement: The server has been restarted at 21:45 04/17. All blockchain have been reset. '
    balance, utxos, _ = get_balance_of_all()
    genesis_block_info = 'hash of genesis block: ' + session['genesis_block_hash']
    addr_info = 'the bank\'s addr: ' + bank_address + ', the hacker\'s addr: ' + hacker_address + ', the shop\'s addr: ' + shop_address
    balance_info = 'Balance of all addresses: ' + json.dumps(balance)
    utxo_info = 'All utxos: ' + json.dumps(utxos)
    blockchain_info = 'Blockchain Explorer: ' + json.dumps(session['blocks'])
    view_source_code_link = "<a href='source_code'>View source code</a>"
    print 'balance_info:', balance_info
    return announcement+('<br /><br />\r\n\r\n'.join([view_source_code_link, genesis_block_info, addr_info, balance_info, utxo_info, blockchain_info]))
    
    
@app.route(url_prefix+'/flag')
def getFlag():
    init()
    print 'diamonds:', session['your_diamonds']
    if session['your_diamonds'] >= 2: return FLAG()
    return 'To get the flag, you should buy 2 diamonds from the shop. You have {} diamonds now. To buy a diamond, transfer 1000000 DDCoins to '.format(session['your_diamonds']) + shop_address
    
def find_enough_utxos(utxos, addr_from, amount):
    collected = []
    for utxo in utxos.values():
        if utxo['addr'] == addr_from:
            amount -= utxo['amount']
            collected.append(utxo['id'])
        if amount <= 0: return collected, -amount
    raise Exception('no enough DDCoins in ' + addr_from)
    
def transfer(utxos, addr_from, addr_to, amount, privkey):
    input_utxo_ids, the_change = find_enough_utxos(utxos, addr_from, amount)
    outputs = [create_output_utxo(addr_to, amount)]
    if the_change != 0:
        outputs.append(create_output_utxo(addr_from, the_change))
    return create_tx(input_utxo_ids, outputs, privkey)
    
@app.route(url_prefix+'/5ecr3t_free_D1diCoin_b@ckD00r/<string:address>')
def free_ddcoin(address):
    print '!!!!!!!',address
    balance, utxos, tail = get_balance_of_all()
    if balance[bank_address] == 0: return 'The bank has no money now.'
    try:
        address = str(address)
        addr_to_pubkey(address) # to check if it is a valid address
        transferred = transfer(utxos, bank_address, address, balance[bank_address], bank_privkey)
        new_block = create_block(tail['hash'], 'b@cKd00R tr1993ReD', [transferred])
        append_block(new_block)
        return str(balance[bank_address]) + ' DDCoins are successfully sent to ' + address
    except Exception, e:
        return 'ERROR: ' + str(e)

#DIFFICULTY = int('00000' + 'f' * 59, 16)
DIFFICULTY = int('0' + 'f' * 63, 16)
@app.route(url_prefix+'/create_transaction', methods=['POST'])
def create_tx_and_check_shop_balance():
    init()
    try:
        block = json.loads(request.data)
        append_block(block, DIFFICULTY)
        msg = 'transaction finished.'
    except Exception, e:
        return str(e)
        
    balance, utxos, tail = get_balance_of_all()
    print 'last balance:', balance
    if balance[shop_address] == 1000000:
        # when 1000000 DDCoins are received, the shop will give you a diamond
        session['your_diamonds'] += 1
        # and immediately the shop will store the money somewhere safe.
        transferred = transfer(utxos, shop_address, shop_wallet_address, balance[shop_address], shop_privkey)
        new_block = create_block(tail['hash'], 'save the DDCoins in a cold wallet', [transferred])
        append_block(new_block)
        msg += ' You receive a diamond.'
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
    for line in source:
        html += line.replace('&','&amp;').replace('\t', '&nbsp;'*4).replace(' ','&nbsp;').replace('<', '&lt;').replace('>','&gt;').replace('\n', '<br />')
    source.close()
    return html
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

