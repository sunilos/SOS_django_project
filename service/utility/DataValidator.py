class DataValidator:

    # add comment to explain that this class provides static methods for validating different types of data, such as checking for null values, validating email format, etc.

    @classmethod
    def isNotNull(self, val):
        if val == None or val == "":
            return False
        else:
            return True

    @classmethod
    def isNull(self, val):
        if val == None or val == "":
            return True
        else:
            return False

    # add isInteger method to validate if a value is an integer
    @classmethod
    def isInteger(self, val):
        try:
            int(val)
            return True
        except ValueError:
            return False

    # add isEmail method to validate if a value is a valid email address
    @classmethod
    def isEmail(self, val):
        if val == None or val == "":
            return False
        if "@" not in val:
            return False
        if "." not in val:
            return False
        return True

    # add isDate method to validate if a value is a valid date in YYYY-MM-DD format
    @classmethod
    def isDate(self, val):
        if val == None or val == "":
            return False
        try:
            year, month, day = map(int, val.split("-"))
            if year < 1900 or year > 2100:
                return False
            if month < 1 or month > 12:
                return False
            if day < 1 or day > 31:
                return False
            return True
        except ValueError:
            return False

    # add isMobileNumber method to validate if a value is a valid mobile number (10 digits)
    @classmethod
    def isMobileNumber(self, val):
        if val == None or val == "":
            return False
        if len(val) != 10:
            return False
        if not val.isdigit():
            return False
        return True
       
    @classmethod
    def isUrl(self, val):
        if val == None or val == "":
            return False
        if not (val.startswith("http://") or val.startswith("https://")):
            return False
        if "." not in val:
            return False
        return True
