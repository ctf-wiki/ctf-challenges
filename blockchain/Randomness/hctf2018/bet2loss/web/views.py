import sha3
import binascii
import traceback
import base64
import time
from web3 import Web3, HTTPProvider

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from core.function import random_num, random_str, send_email
from core.bet2loss_abi import Bet2lossABI
from bet2loss.settings import contractAddress, ez2winAddress
from bet2loss.settings import my_account_address, private_key
from bet2loss.settings import rpcurl
from bet2loss.settings import flag1, flag2
from web.models import HashTable

w3 = Web3(Web3.HTTPProvider(rpcurl, request_kwargs={'timeout': 60}))


def index(req):
    return render(req, 'index.html')


def random(req):
    # {"secret":{"commit":"0xfa5a729f8f60da43c15f15a319abc0324e401a79d6ed4b27a06a16f44592becc","commitLastBlock":6606891,"signature":{"r":"0xe515251a397bdbad17ae3916b73821f07b50158d9bc984f5d880582349fd9ee6","s":"0xff03b8851ec72b3406b03d2910bffb6923e3745d5ae66e8efd90d551db61873e"}},"gasPrice":"12000000000","contractAddress":"0xD1CEeeeee83F8bCF3BEDad437202b6154E9F5405"}
    # account = '0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C'
    result = {'address': contractAddress, 'gasPrice': 12000000000}

    # 随机数
    reveal = random_num()
    result['commit'] = "0x"+sha3.keccak_256(bytes.fromhex(binascii.hexlify(reveal.to_bytes(32, 'big')).decode('utf-8'))).hexdigest()

    # web3获取当前blocknumber
    result['commitLastBlock'] = w3.eth.blockNumber + 250

    h = HashTable(reveal=reveal, commit=result['commit'], commitlastblock=result['commitLastBlock'])
    h.save()

    message = binascii.hexlify(result['commitLastBlock'].to_bytes(32,'big')).decode('utf-8')+result['commit'][2:]
    message_hash = '0x'+sha3.keccak_256(bytes.fromhex(message)).hexdigest()

    signhash = w3.eth.account.signHash(message_hash, private_key=private_key)

    result['signature'] = {}
    result['signature']['r'] = '0x' + binascii.hexlify((signhash['r']).to_bytes(32,'big')).decode('utf-8')
    result['signature']['s'] = '0x' + binascii.hexlify((signhash['s']).to_bytes(32,'big')).decode('utf-8')

    result['signature']['v'] = signhash['v']

    return JsonResponse(result)


@csrf_exempt
def settlebet(req):

    if 'commit' in req.POST:
        commit = req.POST['commit']

        w3 = Web3(HTTPProvider(rpcurl))
        bet2loss = w3.eth.contract(abi=Bet2lossABI)
        bet2loss = bet2loss(address=Web3.toChecksumAddress(contractAddress))

        h = HashTable.objects.filter(commit=commit, is_settle=0)

        if len(h) == 0:
            return HttpResponse('bad guys!')

        h = h[0]
        reveal = h.reveal
        nonce = w3.eth.getTransactionCount(my_account_address)

        try:
            transaction = bet2loss.functions.settleBet(int(reveal)).buildTransaction(
                {'chainId': 3, 'gas': 70000, 'nonce': nonce, 'gasPrice': w3.toWei('1', 'gwei')})

            signed = w3.eth.account.signTransaction(transaction, private_key)

            result = w3.eth.sendRawTransaction(signed.rawTransaction)

        except:
            print(traceback.print_exc())
            return HttpResponse("bad netword, please contact LoRexxar")

        h.is_settle = 1
        h.save()

        return HttpResponse('Success, please wait txns unpack...')

    else:
        return HttpResponse('Welcome to hctf ;>')


def sendflag1():
    w3 = Web3(HTTPProvider(rpcurl))

    flag_logs = w3.eth.getLogs({"address": Web3.toChecksumAddress(contractAddress), "topic0": "0xdb476abde9678304917d1d7094570a616c0d8a4ee4956de1b2ade393ddcdfaa9"})

    if flag_logs is not []:
        for flag_log in flag_logs:
            data = flag_log["data"][2:]

            length = int(data[64*2:64*3].replace('00', ''),16)
            data = data[64*3:][:length*2]
            
            email = binascii.unhexlify(data).decode('utf-8')

            try:
                send_email(base64.b64decode(email).decode('utf-8'), flag1)

            except:
                print('send mail gg? flag1 for {}'.format(email))

    return True


def sendflag2():
    w3 = Web3(HTTPProvider(rpcurl))

    flag_logs = w3.eth.getLogs({"address": Web3.toChecksumAddress(ez2winAddress),
                                "topic0": "0xdb476abde9678304917d1d7094570a616c0d8a4ee4956de1b2ade393ddcdfaa9"})

    if flag_logs is not []:
        for flag_log in flag_logs:
            data = flag_log["data"][2:]

            length = int(data[64 * 2:64 * 3].replace('00', ''), 16)
            data = data[64 * 3:][:length * 2]

            email = binascii.unhexlify(data).decode('utf-8')

            try:
                send_email(base64.b64decode(email).decode('utf-8'), flag2)

            except:
                print('send mail gg? flag2 for {}'.format(email))

    return True


def cron_sendflag():
    for i in range(10):
        sendflag1()
        sendflag2()
        time.sleep(5)
