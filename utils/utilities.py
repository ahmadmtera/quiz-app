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


class Converter:

    @staticmethod
    def convert_list_to_dict(convert_me):
        resultant_dict = {}
        for i in range(0, len(convert_me)):
            resultant_dict[convert_me[i]["auth_cred"]["name"]] = convert_me[i]
