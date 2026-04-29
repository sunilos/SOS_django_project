 
class DropdownListBean:
    """
    Bean class representing a key-value pair for dropdown list items.
    Equivalent to in.co.sunrays.proj4.bean.DropdownListBean
    """
 
    def __init__(self, key: str, value: str):
        self._key = key
        self._value = value
 
    def get_key(self) -> str:
        return self._key
 
    def get_value(self) -> str:
        return self._value
 
    def __lt__(self, other: "DropdownListBean") -> bool:
        """Enable sorting by value (mirrors Collections.sort behavior on DropdownListBean)."""
        return self._value < other._value
 
    def __repr__(self) -> str:
        return f"DropdownListBean(key={self._key!r}, value={self._value!r})"