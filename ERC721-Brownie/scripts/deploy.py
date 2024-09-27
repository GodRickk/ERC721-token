import os
import json
from brownie import MyERC721, accounts, web3, network, config


def main():
    owner_account = accounts.load("account_erc721")
    max_supply = 100
    max_per_mint = 3
    max_per_address = 6
    mint_price = web3.to_wei(0.001, 'ether')
    

    '''contract = MyERC721.deploy(
        owner_account,
        {"from": owner_account},
        # {"from": owner_account, 'gas_price': web3.to_wei('20', 'gwei')},
        publish_source=True
    )'''

    contract = MyERC721.deploy(
        owner_account,
        max_supply,
        max_per_mint,
        max_per_address,
        mint_price,
        {"from": owner_account},
        # {"from": owner_account, 'gas_price': web3.to_wei('20', 'gwei')},
        publish_source=True
    )


    base_uri = "https://ipfs.io/ipfs/QmdFTo5chgndkzzsw4fH2GetPNYg6SiTbsAwfGiHfGmexK/"
    contract.setBaseURI(base_uri, {"from": owner_account})

    deployed_address = contract.address
    abi = contract.abi

    contract_data = {
    "address": deployed_address,
    "abi": abi
    }

    parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    file_path = os.path.join(parent_directory, 'deployed_contract.json')

    with open(file_path, 'w') as file:
        json.dump(contract_data, file, indent=4)



