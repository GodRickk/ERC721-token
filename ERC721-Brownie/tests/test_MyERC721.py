import pytest
from brownie import MyERC721, accounts, web3


MAX_SUPPLY = 100
MAX_PER_MINT = 3
MAX_PER_ADDRESS = 6
MINT_PRICE = web3.to_wei(0.001, 'ether')


@pytest.fixture
def nft_contract():
    return MyERC721.deploy(accounts[0], 
                           MAX_SUPPLY, 
                           MAX_PER_MINT, 
                           MAX_PER_ADDRESS, 
                           MINT_PRICE,  
                           {'from': accounts[0]})


def test_mint_allowed_amount(nft_contract):
    initial_balance = accounts[0].balance()
    initial_contract_balance = nft_contract.balance()
    
    nft_contract.mint(3, {'from': accounts[1], 'value': web3.to_wei(0.003, 'ether')})

    assert nft_contract.balanceOf(accounts[1]) == 3
    assert nft_contract.totalSupply() == 3
    assert nft_contract.balance() == initial_contract_balance + web3.to_wei(0.003, 'ether')
    assert accounts[0].balance() == initial_balance


def test_mint_6_tokens(nft_contract):
    initial_contract_balance = nft_contract.balance()

    nft_contract.mint(3, {'from': accounts[1], 'value': web3.to_wei(0.003, 'ether')})
    nft_contract.mint(3, {'from': accounts[1], 'value': web3.to_wei(0.003, 'ether')})

    assert nft_contract.balanceOf(accounts[1]) == 6
    assert nft_contract.totalSupply() == 6
    assert nft_contract.balance() == initial_contract_balance + web3.to_wei(0.006, 'ether')


def test_mint_more_than_allowed(nft_contract):
    with pytest.raises(Exception):
        nft_contract.mint(4, {'from': accounts[1], 'value': web3.to_wei(0.004, 'ether')})


def test_mint_exceeding_max_per_address(nft_contract):
    nft_contract.mint(3, {'from': accounts[1], 'value': web3.to_wei(0.003, 'ether')})
    nft_contract.mint(3, {'from': accounts[1], 'value': web3.to_wei(0.003, 'ether')})
    with pytest.raises(Exception):
        nft_contract.mint(1, {'from': accounts[1], 'value': web3.to_wei(0.001, 'ether')})
    

def test_mint_exceeding_total_supply(nft_contract):
    for i in range(33):
        nft_contract.mint(3, {'from': accounts[i], 'value': web3.to_wei(0.003, 'ether')})

    assert nft_contract.totalSupply() == 99 
    with pytest.raises(Exception):
        nft_contract.mint(2, {'from': accounts[33], 'value': web3.to_wei(0.003, 'ether')})


def test_mint_incorrect_ether_sent(nft_contract):
    with pytest.raises(Exception):
        nft_contract.mint(3, {'from': accounts[1], 'value': web3.to_wei(MINT_PRICE, 'ether')})


def test_withdraw(nft_contract):
    initial_balance = accounts[0].balance()

    nft_contract.mint(1, {'from': accounts[2], 'value': web3.to_wei(0.001, 'ether')})
    nft_contract.withdraw(web3.to_wei(0.001, 'ether'), accounts[0], {'from': accounts[0]})
    
    assert accounts[0].balance() == initial_balance + web3.to_wei(0.001, 'ether')


def test_withdraw_insufficient_balance(nft_contract):
    nft_contract.mint(3, {'from': accounts[1], 'value': web3.to_wei(0.003, 'ether')})
    
    with pytest.raises(Exception):
        nft_contract.withdraw(web3.to_wei(0.004, 'ether'), accounts[0], {'from': accounts[0]})


def test_withdraw_only_owner_have_possibility(nft_contract):
    nft_contract.mint(3, {'from': accounts[1], 'value': web3.to_wei(0.003, 'ether')})
    
    with pytest.raises(Exception):
        nft_contract.withdraw(web3.to_wei(0.003, 'ether'), accounts[0], {'from': accounts[1]})
