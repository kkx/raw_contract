from web3 import Web3
from ethereum.utils import privtoaddr
from utils import encode_constructor_data, encode_transaction, compile_source_code
from eth_utils import decode_hex


class Contract():
    def __init__(self, web3, private_key, network_id, gas_price, gas_limit):
        self.web3 = web3
        self.private_key = private_key
        self.public_address = Web3.toHex(privtoaddr(private_key))
        self.network_id = network_id
        self.gas_price = gas_price
        self.gas_limit = gas_limit
        self.contract = None
        
    def new_contract(self, contract_source_code, constructor_args_list):
        compiled_sol = compile_source_code(contract_source_code)
        constructor_encoded_data = decode_hex(self.construct_contract_constructor_data(compiled_sol, constructor_args_list))
        nonce = self.web3.eth.getTransactionCount(self.public_address)
        raw_tx_hex = encode_transaction(nonce, self.gas_price, self.gas_limit, '',  0, constructor_encoded_data, self.private_key, self.network_id)
        transaction_hash = self.web3.eth.sendRawTransaction(raw_tx_hex)
        return transaction_hash 

    def construct_contract_constructor_data(self, compiled_sol, args):
        myContract = self.web3.eth.contract(
            abi = compiled_sol['abi'],
            bytecode = compiled_sol['bin'],   
            bytecode_runtime = compiled_sol['bin-runtime'],  
        ) 
        return encode_constructor_data(myContract, args)

    def instantiate_contract(self, address, abi):
        self.contract = self.web3.eth.contract(address=address, abi=abi)
        self.abi = abi

    def encode_contract_transaction(self, function_name, args):
        if not self.contract or not self.abi:
            print('contract not instantiated')
            return 
        return self.contract.encodeABI(function_name, args)
        
    def send_contract_transaction(self, function_name, function_args, eth_value=0):
        transaction_encoded_data = decode_hex(self.encode_contract_transaction(function_name, function_args))
        nonce = self.web3.eth.getTransactionCount(self.public_address)
        raw_tx_hex = encode_transaction(nonce, self.gas_price, self.gas_limit, self.contract.address, eth_value, transaction_encoded_data, self.private_key, self.network_id)
        transaction_hash = self.web3.eth.sendRawTransaction(raw_tx_hex)
        return transaction_hash 



