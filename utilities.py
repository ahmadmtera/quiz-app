class InputVerificationUtils:

    @staticmethod
    def isinteger(value) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False
