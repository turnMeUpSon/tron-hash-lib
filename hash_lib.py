import requests
import os
from subsciption import Subscription
from dotenv import load_dotenv
load_dotenv()


class TronConnector:
    API_ENDPOINT = os.environ.get('API_ENDPOINT')
    API_KEY = os.environ.get('API_KEY')
    STAS_TRC20_WALLET_ADDRESS = os.environ.get('STAS_TRC20_WALLET_ADDRESS')


    @staticmethod
    def convert_string_to_trc20(amount_str: str, decimals: int) -> int:
        return int(int(amount_str) / (10 ** decimals))


    @classmethod
    def is_tx_hash_valid(cls, tx_hash: str) -> bool:
        url = f'{cls.API_ENDPOINT}={tx_hash}'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'TRON-PRO-API-KEY': f'{cls.API_KEY}'
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                valid_data = response.json()
                for transfer_info in valid_data["trc20TransferInfo"]:
                    if transfer_info["to_address"] != cls.STAS_TRC20_WALLET_ADDRESS:
                        print(f"Stanislav Ivankin {cls.STAS_TRC20_WALLET_ADDRESS} didn't get your USDT!")
                        return False
                    else:
                        amount_usdt = cls.convert_string_to_trc20(
                            transfer_info["amount_str"],
                            transfer_info["decimals"]
                        )
                        is_subscriber = Subscription.is_subscriber(amount_usdt)
                        if is_subscriber:
                            result = {
                                "tx_hash": tx_hash,
                                "to_address": transfer_info["to_address"],
                                "amount_usdt": amount_usdt,
                                "is_subscriber": is_subscriber
                            }
                            print(result)
                            return True
                        else:
                            return False
            else:
                print(f"Error: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
    

# Valid test case
tx = TronConnector.is_tx_hash_valid("357648462a7b472c7ac1123550023a0674aca4849fc385bd67e3a51aeb492564")
print(f"{tx}\n")


# Unvalid test case where to address isn't Stas's wallet address
tx = TronConnector.is_tx_hash_valid("bea676853563a236e355aae05622aae5f28a03f071280ac4b907cc9147667b41")
print(f"{tx}\n")


# Unvalid test case where there is no USDT token
tx = TronConnector.is_tx_hash_valid("b55cc2b0103ca8933e72bdd7e42269220b1b7e1b1a27448571aa03cb3c7875ea")
print(f"{tx}\n")