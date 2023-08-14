class InputVerificationUtils:

    @staticmethod
    def isinteger(value) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def isfloat(value) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False
