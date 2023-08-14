from datetime import datetime


class InputVerificationUtils:

    @staticmethod
    def isinteger(value) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False


class DateAndTime:

    @staticmethod
    def get_date_and_time() -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
