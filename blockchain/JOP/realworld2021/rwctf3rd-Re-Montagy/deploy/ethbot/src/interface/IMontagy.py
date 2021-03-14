from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r
from conf.base import chainId, gasPriceOfMontagyDeploy, gasLimitOfMontagyDeploy

# mint
def registerCode1(ctx, _contract, _p1bytes, _from, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['montagy']['abi'])
	construct_tx = store_var_contract.functions.registerCode('0x00').buildTransaction(
		{'chainId': chainId,
		'from': _from.address,
		'nonce': _acc_nonce[0],
		'gasPrice': gasPriceOfMontagyDeploy,
		'gas': gasLimitOfMontagyDeploy
		#'value': w3.toWei(value, 'ether'),
		})
	construct_tx['data']= '0x81d838e5'+_p1bytes
	try:
		signed_tx = _from.signTransaction(construct_tx)
		tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
		_acc_nonce[0] += 1
	except Exception as err:
		return err, None
	return None, tx_hash


def register1(ctx, _contract, _bytecode, _acct, _acc_nonce):
	#p.ppln("[*] calling registerCode1...")
	err, txhash = registerCode1(ctx, _contract, _bytecode, _acct, _acc_nonce)
	if err:
		p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
		exit(0)
	else:
		return None, txhash.hex()


def register1_review(ctx, _acct, _txhash):
	w3 = ctx['web3instance']
	#p.ppln("[*] Checking for registerCode1 status... ")
	try:
		tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
	except Exception as err:
		p.ppln(str(err))
		exit(0)
	addr = tx_receipt['transactionHash'].hex()

	if not addr:
		p.pln(p.in_fg_color("[!] registerCode1 Broken down", r.red5))
	else:
		p.ppln("[+] registerCode1 " + p.in_fg_color("success", r.green1) + " transaction hash: " + p.in_fg_color(addr, r.blue1))

# mint
def registerCode2(ctx, _contract, _p2bytes, _from, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['montagy']['abi'])
	construct_tx = store_var_contract.functions.registerCode('0x00').buildTransaction(
		{'chainId': chainId,
		'from': _from.address,
		'nonce': _acc_nonce[0],
		'gasPrice': gasPriceOfMontagyDeploy,
		'gas': gasLimitOfMontagyDeploy
		#'value': w3.toWei(value, 'ether'),
		})
	construct_tx['data']= '0x81d838e5'+_p2bytes
	try:
		signed_tx = _from.signTransaction(construct_tx)
		tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
		_acc_nonce[0] += 1
	except Exception as err:
		return err, None
	return None, tx_hash


def register2(ctx, _contract, _bytecode, _acct, _acc_nonce):
	#p.ppln("[*] calling registerCode2...")
	err, txhash = registerCode2(ctx, _contract, _bytecode, _acct, _acc_nonce)
	if err:
		p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
		exit(0)
	else:
		return None, txhash.hex()


def register2_review(ctx, _acct, _txhash):
	w3 = ctx['web3instance']
	#p.ppln("[*] Checking for registerCode2 status... ")
	try:
		tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
	except Exception as err:
		p.ppln(str(err))
		exit(0)
	addr = tx_receipt['transactionHash'].hex()

	if not addr:
		p.pln(p.in_fg_color("[!] registerCode Broken down", r.red5))
	else:
		p.ppln("[+] registerCode " + p.in_fg_color("success", r.green1) + ", transaction hash: " + p.in_fg_color(addr, r.blue1))


# mint
def setNewPuzzle1(ctx, _contract, _p1bytes, _from, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['montagy']['abi'])
	construct_tx = store_var_contract.functions.newPuzzle('0x00').buildTransaction(
		{'chainId': chainId,
		'from': _from.address,
		'nonce': _acc_nonce[0],
		'gasPrice': gasPriceOfMontagyDeploy,
		'gas': gasLimitOfMontagyDeploy
		#'value': w3.toWei(value, 'ether'),
		})
	construct_tx['data']= '0xe6744e8d'+_p1bytes
	try:
		signed_tx = _from.signTransaction(construct_tx)
		tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
		_acc_nonce[0] += 1
	except Exception as err:
		return err, None
	return None, tx_hash


def newPuzzle1(ctx, _contract, _p1bytes, _acct, _acc_nonce):
	p.ppln("[*] calling newPuzzle1...")
	err, txhash = setNewPuzzle1(ctx, _contract, _p1bytes, _acct, _acc_nonce)
	if err:
		p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
		exit(0)
	else:
		return None, txhash.hex()


def newPuzzle1_review(ctx, _acct, _txhash):
	w3 = ctx['web3instance']
	p.ppln("[*] Checking for newPuzzle1 status... ")
	try:
		tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
	except Exception as err:
		p.ppln(str(err))
		exit(0)
	addr = tx_receipt['transactionHash'].hex()

	if not addr:
		p.pln(p.in_fg_color("[!] newPuzzle1 Broken down", r.red5))
	else:
		p.ppln("[+] newPuzzle1 " + p.in_fg_color("success", r.green1) + " transaction hash: " + p.in_fg_color(addr, r.blue1))


# mint
def setNewPuzzle2(ctx, _contract, _p2bytes, _from, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['montagy']['abi'])
	construct_tx = store_var_contract.functions.newPuzzle('0x00').buildTransaction(
		{'chainId': chainId,
		'from': _from.address,
		'nonce': _acc_nonce[0],
		'gasPrice': gasPriceOfMontagyDeploy,
		'gas': gasLimitOfMontagyDeploy
		#'value': w3.toWei(value, 'ether'),
		})
	construct_tx['data']= '0xe6744e8d'+_p2bytes
	try:
		signed_tx = _from.signTransaction(construct_tx)
		tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
		_acc_nonce[0] += 1
	except Exception as err:
		return err, None
	return None, tx_hash


def newPuzzle2(ctx, _contract, _p2bytes, _acct, _acc_nonce):
	#p.ppln("[*] calling newPuzzle2...")
	err, txhash = setNewPuzzle2(ctx, _contract, _p2bytes, _acct, _acc_nonce)
	if err:
		p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
		exit(0)
	else:
		return None, txhash.hex()


def newPuzzle2_review(ctx, _acct, _txhash):
	w3 = ctx['web3instance']
	#p.ppln("[*] Checking for newPuzzle2 status... ")
	try:
		tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
	except Exception as err:
		p.ppln(str(err))
		exit(0)
	addr = tx_receipt['transactionHash'].hex()

	if not addr:
		p.pln(p.in_fg_color("[!] newPuzzle Broken down", r.red5))
	else:
		p.ppln("[+] newPuzzle " + p.in_fg_color("success", r.green1) + ", transaction hash: " + p.in_fg_color(addr, r.blue1))


def getPAddress(ctx, _contract, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['montagy']['abi'])

	try:
		lastchildaddr = store_var_contract.functions.lastchildaddr().call()
		return lastchildaddr
	except Exception as err:
		return err, None



