
from conf.base import AES_KEY, HMAC_KEY, sz_col, sz_row
from src.utils.auth import validate_then_decrypt, validate_game_account
from src.checker.flagchecker import check_if_has_topic, getflag
from colorfulpanda.mov.PanicWhiteRed import main as mov2
from src.banner.text.corpus import PANIC_INFO, SORRY_INFO
from src.utils.prettyprint.Red import Printer as p
from src.utils.prettyprint.Red import red1, white1
import sys


def run(ctx):
	new_token = input("[-]input your new token: ")
	new_token = new_token.strip()
	try:
		data = validate_then_decrypt(new_token, AES_KEY, HMAC_KEY)
	except Exception as err:
		print("[!]bad token")
		sys.exit(0)

	if len(data) != 114:
		print("[!]wrong token")
		sys.exit(0)

	data, msg = data[:-40], data[-40:]
	acct = validate_game_account(ctx, data)
	res = check_if_has_topic(ctx, acct, "0x"+msg.decode())
	if res:
		flag = getflag()
		p.ppln(p.in_fg_color("[+] Congratulation! Here's the flag:", white1))
		p.ppln(p.in_fg_color(flag, red1))
	else:
		p.ppln(p.in_fg_color("[!] It seems that you didn't solve the puzzle.", white1))
		p.ppln(p.in_fg_color("[!] Note that it may take time for ethereum to update, so please try 1 min latter if you feel necessary.", white1))

		#mov2(PANIC_INFO, SORRY_INFO, sz_col, sz_row)