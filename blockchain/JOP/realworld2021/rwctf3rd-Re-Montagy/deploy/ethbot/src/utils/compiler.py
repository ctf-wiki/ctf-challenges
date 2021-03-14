import json
from solcx import compile_source
from src.utils.utils import dumps_env


# solc
def compile_from_src(source):
	compiled_sol = compile_source(source, output_values=["abi", "bin"], solc_version="0.5.11")
	return compiled_sol

# web3
def get_deploy_est_gas(ctx, cont_if):
	w3 = ctx['web3instance']
	instance = w3.eth.contract(
		abi=cont_if['abi'],
		bytecode=cont_if['bin']
	)
	return instance.constructor().estimateGas()


def prepare_contract_source_without_cache():
	confs = {}

	with open("contracts/Montagy.sol", 'r+') as fi:
		source1 = fi.read()
		conf_all = compile_from_src(source1)
		confs['montagy'] = conf_all['<stdin>:Montagy']


	return confs


def comp(ctx):
	if not ctx['compiledcontracts']:
		compiler_result = prepare_contract_source_without_cache()
		ctx['compiledcontracts'] = compiler_result
		dumps_env(ctx)
		return ctx
	else:
		return ctx
