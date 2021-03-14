
from conf.base import est_gas
from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r



def balancecheck(ctx, _acct):
    w3 = ctx['web3instance']
    try:
        balance = w3.eth.getBalance(_acct.address)
    except:
        return False

    if balance < est_gas:
        return False
    return True