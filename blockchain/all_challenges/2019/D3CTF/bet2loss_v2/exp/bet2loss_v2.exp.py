# -*- coding: UTF-8 -*-
from web3 import Web3, HTTPProvider
import sha3
import binascii
from random import Random
from requests import request

true = True
false = False
config = {
    "abi":[
    {
        "constant": true,
        "inputs": [],
        "name": "count",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "reveal",
                "type": "uint256"
            }
        ],
        "name": "settleBet",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "name": "balances",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "INITIAL_SUPPLY",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "_totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "_airdropAmount",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "betnumber",
                "type": "uint8"
            },
            {
                "name": "modulo",
                "type": "uint8"
            },
            {
                "name": "wager",
                "type": "uint40"
            },
            {
                "name": "commitLastBlock",
                "type": "uint40"
            },
            {
                "name": "commit",
                "type": "uint256"
            },
            {
                "name": "r",
                "type": "bytes32"
            },
            {
                "name": "s",
                "type": "bytes32"
            },
            {
                "name": "v",
                "type": "uint8"
            }
        ],
        "name": "placeBet",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "croupier",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [],
        "name": "PayForFlag",
        "outputs": [
            {
                "name": "success",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "lockedInBets",
        "outputs": [
            {
                "name": "",
                "type": "uint128"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "newCroupier",
                "type": "address"
            }
        ],
        "name": "setCroupier",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "beneficiary",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "FailedPayment",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "beneficiary",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "Payment",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "name": "commit",
                "type": "uint256"
            }
        ],
        "name": "Commit",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "name": "message",
                "type": "string"
            }
        ],
        "name": "GetFlag",
        "type": "event"
    }
    ],
    "address": Web3.toChecksumAddress("0x66d30937C5b98000c2e9f77acbf51915A1AacbC9")
}

w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/2daa76d148c341c0aabf5b5de0f5d175"))
contract_instance = w3.eth.contract(address=config['address'], abi=config['abi'])

public_key = 0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C
private_key = b'o\x08\xd7A\x949\x90t#\x81\xe1"4FU:c\xb3\x8a:\xa8k\xee\xf1\xe9\xfc_\xcfa\xe6m\x12'

public1 = "0x75e65F3C1BB334ab927168Bd49F5C44fbB4D480f"
private1 = "92B562F4DCB430F547401F31B5D1074E6791EC37786F449497C4F9563ABEF3FB"

public2 = "0x88D3052D12527F1FbE3a6E1444EA72c4DdB396c2"
private2 = "D732A601291E11277EF479C0F2D567AC813FB7A2404F3528CA213CAA37B1EFCB"

public3 = "0x52cC2403764380CCa583633d2523999FE5077113"
private3 = "F35BD686FE298C6B1F1F50D4DB33F0E65CEF843573E0E52303EF22219A9FE95C"

public4 = "0x0063b03366DA8063D6B92Bf141D923709Fb69824"
private4 = "AF1C4FFADB3B6CB466568229763E3409626A70F258DCB12C86351EDC73E4B43B"

public5 = "0xabb09dE7bAEC859E62B8516087419bCDa3D1e14C"
private5 = "991267F2F83286C121511589C93AABBF8B501CB77A9BA034039FE2B50A43F014"

def random_num(start=2**20, end=2**30):
    random = Random()
    return random.randint(start,end)

def random():
    # {"secret":{"commit":"0xfa5a729f8f60da43c15f15a319abc0324e401a79d6ed4b27a06a16f44592becc","commitLastBlock":6606891,"signature":{"r":"0xe515251a397bdbad17ae3916b73821f07b50158d9bc984f5d880582349fd9ee6","s":"0xff03b8851ec72b3406b03d2910bffb6923e3745d5ae66e8efd90d551db61873e"}},"gasPrice":"12000000000","contractAddress":"0xD1CEeeeee83F8bCF3BEDad437202b6154E9F5405"}
    # account = '0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C'
    result = {'address': config['address'], 'gasPrice': 12000000000}

    # 随机数
    reveal = random_num()
    #reveal = 0x36bb455d

    result['commit'] = "0x"+sha3.keccak_256(bytes.fromhex(binascii.hexlify(reveal.to_bytes(32, 'big')).decode('utf-8'))).hexdigest()

    # web3获取当前blocknumber
    result['commitLastBlock'] = w3.eth.blockNumber + 250
    #result['commitLastBlock'] = 0x68507e

    message = binascii.hexlify(result['commitLastBlock'].to_bytes(5,'big')).decode('utf-8')+result['commit'][2:]
    message_hash = '0x'+sha3.keccak_256(bytes.fromhex(message)).hexdigest()
    #message_hash = '0x4fb4c41d0f7cabc65f6427377ef3939f7e31da769a3528a2f1d1d2d1688db172'

    signhash = w3.eth.account.signHash(message_hash, private_key=private_key)

    result['signature'] = {}
    result['signature']['r'] = '0x' + binascii.hexlify((signhash['r']).to_bytes(32,'big')).decode('utf-8')
    result['signature']['s'] = '0x' + binascii.hexlify((signhash['s']).to_bytes(32,'big')).decode('utf-8')

    result['signature']['v'] = signhash['v']

    for key,value in result.items():
        print('{key}:{value}'.format(key = key, value = value))
    return result,reveal,w3.eth.blockNumber

result,reveal,blocknumber = random()
print("reveal=",reveal)

def placeBet1():
    modulo = 100
    wager = 1000
    blocknumber = w3.eth.blockNumber+2
    print("blocknumber=",blocknumber)
    tmp = binascii.hexlify(reveal.to_bytes(32,'big')).decode('utf-8')+binascii.hexlify(blocknumber.to_bytes(32,'big')).decode('utf-8')
    tmp_hash = '0x'+sha3.keccak_256(bytes.fromhex(tmp)).hexdigest()
    print("tmp_hash16=",int(tmp_hash, 16))

    betnumber = int(tmp_hash, 16) % modulo
    print("betnumber=",betnumber)

    commitLastBlock = result['commitLastBlock']
    commit = result['commit']
    r = result['signature']['r']
    s = result['signature']['s']
    v = result['signature']['v']
    txn = contract_instance.functions.placeBet(betnumber, modulo, wager, commitLastBlock, int(commit,16), r, s, int(v)).buildTransaction(
        {
            'chainId':3,
            'nonce':w3.eth.getTransactionCount(Web3.toChecksumAddress(public1)),
            'gas':7600000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice':w3.eth.gasPrice,
        }
    )
    signed_txn = w3.eth.account.signTransaction(txn,private_key=private1)
    res = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = w3.eth.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt

print(placeBet1())

def settleBet1():
    txn = contract_instance.functions.settleBet(reveal).buildTransaction(
        {
            'chainId':3,
            'nonce':w3.eth.getTransactionCount(Web3.toChecksumAddress(public_key)),
            'gas':7600000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice':w3.eth.gasPrice,
        }
    )
    signed_txn = w3.eth.account.signTransaction(txn,private_key=private_key)
    res  = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = w3.eth.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt

print(settleBet1())


print("-----------------")
result,reveal,blocknumber = random()
print("reveal=",reveal)

def placeBet2():
    modulo = 100
    wager = 1000
    blocknumber = w3.eth.blockNumber+3
    print("blocknumber=",blocknumber)
    tmp = binascii.hexlify(reveal.to_bytes(32,'big')).decode('utf-8')+binascii.hexlify(blocknumber.to_bytes(32,'big')).decode('utf-8')
    tmp_hash = '0x'+sha3.keccak_256(bytes.fromhex(tmp)).hexdigest()
    print("tmp_hash16=",int(tmp_hash, 16))

    betnumber = int(tmp_hash, 16) % modulo
    print("betnumber=",betnumber)

    commitLastBlock = result['commitLastBlock']
    commit = result['commit']
    r = result['signature']['r']
    s = result['signature']['s']
    v = result['signature']['v']
    txn = contract_instance.functions.placeBet(betnumber, modulo, wager, commitLastBlock, int(commit,16), r, s, int(v)).buildTransaction(
        {
            'chainId':3,
            'nonce':w3.eth.getTransactionCount(Web3.toChecksumAddress(public2)),
            'gas':7600000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice':w3.eth.gasPrice,
        }
    )
    signed_txn = w3.eth.account.signTransaction(txn,private_key=private2)
    res = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = w3.eth.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt

print(placeBet2())

def settleBet2():
    txn = contract_instance.functions.settleBet(reveal).buildTransaction(
        {
            'chainId':3,
            'nonce':w3.eth.getTransactionCount(Web3.toChecksumAddress(public_key)),
            'gas':7600000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice':w3.eth.gasPrice,
        }
    )
    signed_txn = w3.eth.account.signTransaction(txn,private_key=private_key)
    res  = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = w3.eth.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt

print(settleBet2())


print("-----------------")
result,reveal,blocknumber = random()
print("reveal=",reveal)

def placeBet3():
    modulo = 100
    wager = 1000
    blocknumber = w3.eth.blockNumber+4
    print("blocknumber=",blocknumber)
    tmp = binascii.hexlify(reveal.to_bytes(32,'big')).decode('utf-8')+binascii.hexlify(blocknumber.to_bytes(32,'big')).decode('utf-8')
    tmp_hash = '0x'+sha3.keccak_256(bytes.fromhex(tmp)).hexdigest()
    print("tmp_hash16=",int(tmp_hash, 16))

    betnumber = int(tmp_hash, 16) % modulo
    print("betnumber=",betnumber)

    commitLastBlock = result['commitLastBlock']
    commit = result['commit']
    r = result['signature']['r']
    s = result['signature']['s']
    v = result['signature']['v']
    txn = contract_instance.functions.placeBet(betnumber, modulo, wager, commitLastBlock, int(commit,16), r, s, int(v)).buildTransaction(
        {
            'chainId':3,
            'nonce':w3.eth.getTransactionCount(Web3.toChecksumAddress(public3)),
            'gas':7600000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice':w3.eth.gasPrice,
        }
    )
    signed_txn = w3.eth.account.signTransaction(txn,private_key=private3)
    res = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = w3.eth.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt

print(placeBet3())

def settleBet3():
    txn = contract_instance.functions.settleBet(reveal).buildTransaction(
        {
            'chainId':3,
            'nonce':w3.eth.getTransactionCount(Web3.toChecksumAddress(public_key)),
            'gas':7600000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice':w3.eth.gasPrice,
        }
    )
    signed_txn = w3.eth.account.signTransaction(txn,private_key=private_key)
    res  = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = w3.eth.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt

print(settleBet3())




print("-----------------")
result,reveal,blocknumber = random()
print("reveal=",reveal)

def placeBet4():
    modulo = 100
    wager = 1000
    blocknumber = w3.eth.blockNumber+5
    print("blocknumber=",blocknumber)
    tmp = binascii.hexlify(reveal.to_bytes(32,'big')).decode('utf-8')+binascii.hexlify(blocknumber.to_bytes(32,'big')).decode('utf-8')
    tmp_hash = '0x'+sha3.keccak_256(bytes.fromhex(tmp)).hexdigest()
    print("tmp_hash16=",int(tmp_hash, 16))

    betnumber = int(tmp_hash, 16) % modulo
    print("betnumber=",betnumber)

    commitLastBlock = result['commitLastBlock']
    commit = result['commit']
    r = result['signature']['r']
    s = result['signature']['s']
    v = result['signature']['v']
    txn = contract_instance.functions.placeBet(betnumber, modulo, wager, commitLastBlock, int(commit,16), r, s, int(v)).buildTransaction(
        {
            'chainId':3,
            'nonce':w3.eth.getTransactionCount(Web3.toChecksumAddress(public4)),
            'gas':7600000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice':w3.eth.gasPrice,
        }
    )
    signed_txn = w3.eth.account.signTransaction(txn,private_key=private4)
    res = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = w3.eth.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt

print(placeBet4())

def settleBet4():
    txn = contract_instance.functions.settleBet(reveal).buildTransaction(
        {
            'chainId':3,
            'nonce':w3.eth.getTransactionCount(Web3.toChecksumAddress(public_key)),
            'gas':7600000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice':w3.eth.gasPrice,
        }
    )
    signed_txn = w3.eth.account.signTransaction(txn,private_key=private_key)
    res  = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = w3.eth.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt

print(settleBet4())


print("-----------------")
result,reveal,blocknumber = random()
print("reveal=",reveal)

def placeBet5():
    modulo = 100
    wager = 1000
    blocknumber = w3.eth.blockNumber+6
    print("blocknumber=",blocknumber)
    tmp = binascii.hexlify(reveal.to_bytes(32,'big')).decode('utf-8')+binascii.hexlify(blocknumber.to_bytes(32,'big')).decode('utf-8')
    tmp_hash = '0x'+sha3.keccak_256(bytes.fromhex(tmp)).hexdigest()
    print("tmp_hash16=",int(tmp_hash, 16))

    betnumber = int(tmp_hash, 16) % modulo
    print("betnumber=",betnumber)

    commitLastBlock = result['commitLastBlock']
    commit = result['commit']
    r = result['signature']['r']
    s = result['signature']['s']
    v = result['signature']['v']
    txn = contract_instance.functions.placeBet(betnumber, modulo, wager, commitLastBlock, int(commit,16), r, s, int(v)).buildTransaction(
        {
            'chainId':3,
            'nonce':w3.eth.getTransactionCount(Web3.toChecksumAddress(public5)),
            'gas':7600000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice':w3.eth.gasPrice,
        }
    )
    signed_txn = w3.eth.account.signTransaction(txn,private_key=private5)
    res = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = w3.eth.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt

print(placeBet5())

def settleBet5():
    txn = contract_instance.functions.settleBet(reveal).buildTransaction(
        {
            'chainId':3,
            'nonce':w3.eth.getTransactionCount(Web3.toChecksumAddress(public_key)),
            'gas':7600000,
            'value':Web3.toWei(0,'ether'),
            'gasPrice':w3.eth.gasPrice,
        }
    )
    signed_txn = w3.eth.account.signTransaction(txn,private_key=private_key)
    res  = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    txn_receipt = w3.eth.waitForTransactionReceipt(res)
    print(res)
    return txn_receipt

print(settleBet5())
