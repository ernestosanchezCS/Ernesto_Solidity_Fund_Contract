from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


# testing that only owner can withdraw
def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    # line below gives us a random account which
    # we will try to withdraw contract from
    bad_actor = accounts.add()
    # this test below says we want the line
    # fund_me.withdraw({"from": bad_actor}) to return VirtualMachineError
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
