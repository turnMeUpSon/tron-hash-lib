class Subscription:
    VALID_SUBSCRIPTIONS_USDT = set([19, 150, 400, 600, 1000])


    @classmethod
    def is_subscriber(cls, amount_usdt: int) -> bool:
        if amount_usdt in cls.VALID_SUBSCRIPTIONS_USDT or amount_usdt > max(cls.VALID_SUBSCRIPTIONS_USDT):
            return True
        else:
            return False