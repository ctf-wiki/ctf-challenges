from conf.base import flag, TOPIC, ONEHUNDRED
from src.utils.auth import get_acc_nonce
from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r

def getflag():
	return flag


def balanceofflagtoken(ctx, _contract, _to_address, _acc_nonce):
	w3 = ctx['web3instance']

	try:
		balance = w3.eth.getBalance(_contract)
	except Exception as err:
		print(err) # xhyu
		return err, None
	return None, balance


def check_if_has_topic(ctx, _acct, montagy_addr):
	acc_nonce = get_acc_nonce(ctx, _acct)
	err, balance = balanceofflagtoken(ctx, montagy_addr, _acct, acc_nonce)

	if err:
		p.pln(p.in_fg_color(str(err), r.red4))

	if balance == TOPIC:
		return True
	else:
		return False
