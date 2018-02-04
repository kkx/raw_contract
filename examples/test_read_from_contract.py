from web3 import Web3, HTTPProvider
from contract.contract import Contract
from utils import compile_source_code

private_key = 'PUT YOUR PRIVATE KEY'

web3 = Web3(HTTPProvider('A PUBLIC RINKEBY INFURA ADDRESS'))
contract = Contract(web3, private_key, 4, web3.eth.gasPrice * 5, 6000000)

contract_source_code = open("./test_contract.sol").read()
abi = compile_source_code(contract_source_code)['abi']
// a deployed test contract address
contract.instantiate_contract('0xa4ca0f86fbf552be42c38782d248423385e7a115', abi)
print(contract.contract.call().testValue())
