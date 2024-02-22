class TRC20Converter:

    
    @classmethod
    def convert_string_to_trc20(cls, amount_str: str, decimals: int) -> int:
        return int(int(amount_str) / (10 ** decimals))
