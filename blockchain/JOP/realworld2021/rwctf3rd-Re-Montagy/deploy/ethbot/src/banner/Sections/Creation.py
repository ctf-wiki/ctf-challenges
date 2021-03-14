from src.utils.auth import encrypt_then_mac, create_game_account
from conf.base import AES_KEY, HMAC_KEY, est_gas

def run(ctx):
	# create game account
	acct = create_game_account(ctx)
	print("[+]Your game account:{}".format(acct.address))

	# generate token
	data = acct.address.encode() + acct.key
	token = encrypt_then_mac(data, AES_KEY, HMAC_KEY)
	print("[+]Token: {}".format(token))

	print("[+]Please transfer at least {} ETH to your game account before Deploy".format(est_gas/10**18))
	#print("[+]Make sure that you have enough ether to deploy!!!!!!")