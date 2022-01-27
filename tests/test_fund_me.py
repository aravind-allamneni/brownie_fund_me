from eth_account import Account
from scripts.helpful_scripts import get_account, LOCAL_BLOCK_CHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100

    txn = fund_me.fund({"from": account, "value": entrance_fee})
    txn.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    txn2 = fund_me.withdraw({"from": account})
    txn2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCK_CHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(ValueError):
        fund_me.withdraw({"from": bad_actor})
