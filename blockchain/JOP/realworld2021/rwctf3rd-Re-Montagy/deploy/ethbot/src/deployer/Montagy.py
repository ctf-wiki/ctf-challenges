
import conf.base as conf
from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r
from src.utils.utils import randhex
import re


def montagy(w3, _abi, _bin, _acct, _acc_nonce):
    instance = w3.eth.contract(
        abi=_abi,
        bytecode=_bin
    )
    construct_tx = instance.constructor().buildTransaction(
        {'chainId': conf.chainId,
         'from': _acct.address,
         'nonce': _acc_nonce[0],
         'gasPrice': conf.gasPriceOfMontagyDeploy,
         'gas': conf.gasLimitOfMontagyDeploy,
         'value': w3.toWei(conf.TOPIC_VALUE, 'ether')
         })
    try:
        signed_tx = _acct.signTransaction(construct_tx)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        _acc_nonce[0] += 1
    except Exception as err:
        return err, None
    return None, tx_hash.hex()


def deploy(ctx, _acct, _acc_nonce):
    #p.ppln("[*] trying to deploy montagy contracts...")
    abi = ctx['compiledcontracts']['montagy']['abi']
    bin = ctx['compiledcontracts']['montagy']['bin']
    w3 = ctx['web3instance']

    bin = re.sub('a265627a7a72315820.{64}64736f6c634300050b0032', 'a265627a7a72315820'+randhex(64)+'64736f6c634300050b0032', bin)
    #bin.repalce("627a7a72315820f044b77d8376499313d5239e6881baadb3dec8e7f36eca97638fed329186930964736f6c634300050b0032","627a7a" + ''.join(random.sample(string.hexdigits, 10)).lower()*9 + "0032")
    err, txhash = montagy(w3, abi, bin, _acct, _acc_nonce)
    if err:
        p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
        exit(0)
    else:
        return None, txhash


def review(ctx, _acct, _txhash):
    w3 = ctx['web3instance']
    #p.ppln("[*] checking deployment statue... ")
    try:
        tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
    except Exception as err:
        p.p(str(err))
        exit(0)
    addr = tx_receipt['contractAddress']

    if not addr:
        p.pln(p.in_fg_color("[!] contract montagy deploy Broken down", r.red5))
        exit(0)
    else:
        p.ppln("[+] contract Montagy deploy " + p.in_fg_color("success", r.green1) + ", address: " + p.in_fg_color(addr, r.blue1))
        return addr

