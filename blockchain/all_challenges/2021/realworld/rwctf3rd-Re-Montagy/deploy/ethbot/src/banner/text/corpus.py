from src.utils.prettyprint.Red import Printer, Formator
_p = Printer()
_f = Formator()
deploy_panic_imp_info = "人们不能预见、不可避免、不能克服的自然、社会现象客观情况。社会及自然现象包括但不限于天灾人祸如地震、战争、市政工程建设、其它政府政策或矿工不给你打包交易"

MENU = '''
Game environment: rinkeby
1. Create a game account
2. Deploy game contract(s)
3. Request for flag
'''


WELCOME = _f.in_column_center(_p.in_fg_color('.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.\r', 40))+\
_f.in_column_center(_p.in_fg_color('.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.\n', 40))+\
_f.in_column_center(_p.in_fg_color('(               Welcome to Re:Montagy!          )\n', 41))+\
_f.in_column_center(_p.in_fg_color(' )              Shall we play a game?          ( \n', 42))+\
_f.in_column_center(_p.in_fg_color('(                       Enjoy it !              )\n', 43))+\
_f.in_column_center(_p.in_fg_color('"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"\n', 44))


SRC_TEXT = '''
https://github.com/PandaTea/NightCity-backup
'''

DEPLOY_SUCCESS_CELEBRATION = "\n\n\n\n\n\n\n\n" + _f.in_column_center(_p.in_fg_color('.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.\r', 40))+\
                             _f.in_column_center(_p.in_fg_color(' .+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.\n', 39))+\
_f.in_column_center(_p.in_fg_color('( ALL CONTRACTS Deployed SUCCESSFUL           )\n',75))+\
_f.in_column_center(_p.in_fg_color(' )Congratulations!!!, You are so lucky!      (\n',111))+\
_f.in_column_center(_p.in_fg_color('( The blessings of the miners are with you!!! )\n',147))+\
_f.in_column_center(_p.in_fg_color(' "+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"\n',183)) + "\n\n\n\n"

PANIC_INFO = '''
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: ^CTraceback (most recent call last):
  File "/usr/local/bin/Top_Secret-underground_financial_network_of_night_city", line 8, in <module>
    sys.exit(main())
  File "/usr/local/lib/python3.8/site-packages/Top_Secret-underground_financial_network_of_night_city/__main__.py", line 28, in main
    result = cli.dispatch(sys.argv[1:])
  File "/usr/local/lib/python3.8/site-packages/Top_Secret-underground_financial_network_of_night_city/cli.py", line 82, in dispatch
    return main(args.args)
  File "/usr/local/lib/python3.8/site-packages/Top_Secret-underground_financial_network_of_night_city/commands/upload.py", line 151, in main
    return upload(upload_settings, parsed_args.dists)
  File "/usr/local/lib/python3.8/site-packages/Top_Secret-underground_financial_network_of_night_city/commands/upload.py", line 89, in upload
    repository = upload_settings.create_repository()
  File "/usr/local/lib/python3.8/site-packages/Top_Secret-underground_financial_network_of_night_city/settings.py", line 321, in create_repository
    self.username,
  File "/usr/local/lib/python3.8/site-packages/Top_Secret-underground_financial_network_of_night_city/settings.py", line 141, in username
    return cast(Optional[str], self.auth.username)
  File "/usr/local/lib/python3.8/site-packages/Top_Secret-underground_financial_network_of_night_city/auth.py", line 35, in username
    return utils.get_userpass_value(
  File "/usr/local/lib/python3.8/site-packages/Top_Secret-underground_financial_network_of_night_city/utils.py", line 241, in get_userpass_value
    return prompt_strategy()
  File "/usr/local/lib/python3.8/site-packages/Top_Secret-underground_financial_network_of_night_city/auth.py", line 76, in username_from_keyring_or_prompt
    return self.get_username_from_keyring() or self.prompt("username", input)
  File "/usr/local/lib/python3.8/site-packages/Top_Secret-underground_financial_network_of_night_city/auth.py", line 84, in prompt
    return how(f"Enter your {what}: ")
'''

SORRY_INFO = '''
Sorry, you do not have access to this confidential content
对不起，你无权访问此机密内容
'''