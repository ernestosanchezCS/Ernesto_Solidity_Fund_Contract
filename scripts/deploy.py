from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # if we are on a persistant network like rinkeby we
    #     need to pass it the pricefeed address
    # else we want to setup on ganache mock network
    #     thus we address how the contract gets it pricefeed source
    # we can check what network we on using brownie network shown below
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    # we need to pass the pricefeed address to teh fund me contract.
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # again whenever we make a state change we need
    # to provide account! using this format ({"from":account})
    # publish_source=True this part says yes we want to publish our source code
    # if publish_source then brownie uses the etherscan token in .env automatically
    print(f"Contrat Deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
