from web3 import Web3
from solc import compile_source
import rlp
from ethereum.transactions import Transaction
from web3.utils.abi import (
    get_constructor_abi,
    merge_args_and_kwargs,
)

from eth_utils import (
    add_0x_prefix,
    decode_hex,
    coerce_return_to_text,
)

def encode_transaction(nonce, gasprice, startgas, to, value, data, private_key, network_id):
    tx = Transaction(
        nonce=nonce,
        gasprice=gasprice,
        startgas=startgas,
        to=to,
        value=value,
        data=data,
    )
    tx.sign(private_key, network_id)
    raw_tx = rlp.encode(tx)
    raw_tx_hex = Web3.toHex(raw_tx)
    return raw_tx_hex 


@coerce_return_to_text
def encode_constructor_data(contract, args=None, kwargs=None):
    constructor_abi = get_constructor_abi(contract.abi)

    if constructor_abi:
        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = {}

        arguments = merge_args_and_kwargs(constructor_abi, args, kwargs)
        deploy_data = add_0x_prefix(
            contract._encode_abi(constructor_abi, arguments, data=contract.bytecode)
        )
    else:
        deploy_data = add_0x_prefix(contract.bytecode)

    return deploy_data


def compile_source_code(contract_source_code):
    compiled_sol = compile_source(contract_source_code)
    # get first contract
    compiled_sol = compiled_sol[list(compiled_sol.keys())[0]]
    return compiled_sol

