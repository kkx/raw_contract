from web3 import Web3, HTTPProvider
from contract.contract import Contract

private_key = 'PUT YOUR PRIVATE KEY'

web3 = Web3(HTTPProvider('A PUBLIC RINKEBY INFURA ADDRESS'))
contract = Contract(web3, private_key, 4, web3.eth.gasPrice * 5, 6000000)
contract_source_code = open("./test_contract.sol").read()
print(contract.new_contract(contract_source_code, [3]))
