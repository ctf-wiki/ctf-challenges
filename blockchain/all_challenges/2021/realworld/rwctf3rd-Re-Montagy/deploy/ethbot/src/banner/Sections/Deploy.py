

from conf.base import AES_KEY, HMAC_KEY, est_gas
from src.utils.auth import validate_then_decrypt, validate_game_account, encrypt_then_mac
import src.deployer.main as deployer
import sys
from src.utils.prettyprint.Red import Printer
import src.utils.prettyprint.Red as r
from src.checker.deployerchecker import balancecheck



def run(ctx):
	token = input("[-]input your token: ")
	token = token.strip()
	try:
		data = validate_then_decrypt(token, AES_KEY, HMAC_KEY)
	except Exception as err:
		print("[!]bad token")
		sys.exit(0)
	if len(data) != 74:
		#print(Printer.in_fg_color("[-]wrong token", r.red4))
		print("[!]wrong token")
		sys.exit(0)
	acct = validate_game_account(ctx, data)

	if not balancecheck(ctx, acct):
		print("[!]game account balance not enough, should >={} ETH, please send more...".format(est_gas/10**18))
		sys.exit(0)

	montagy_address = deployer.run(ctx, acct) 

	# generate new token
	data = acct.address.encode() + acct.key + montagy_address.encode()
	new_token = encrypt_then_mac(data, AES_KEY, HMAC_KEY)
	Printer.ppln(Printer.in_fg_color("[+]new token: {}".format(new_token), r.white1))
	Printer.ppln("[+]Your goal is to empty the Montagy contract's ETH balance.")