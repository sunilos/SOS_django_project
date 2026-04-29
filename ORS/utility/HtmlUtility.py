from service.models import DropdownItem

class HtmlUtility:
    """Utility class for generating HTML form elements such as dropdown SELECT lists."""

    @staticmethod
    def get_list_from_map(name: str, selected_val: int, map_data: dict[int, str]) -> str:
        """
        Generate an HTML SELECT element from a dictionary.

        Args:
            name:         The name attribute of the <select> element.
            selected_val: The integer key of the option to pre-select.
            map_data:     A dict of {int key: str label} pairs for the options.

        Returns:
            An HTML <select> string with a default --Select-- option.
        """
        sb = [f"<select class='form-control' name='{name}'>"]
        sb.append("<option value='0'>--Select--</option>")

        for key, val in map_data.items():
            if key == selected_val:
                sb.append(f"<option selected value='{key}'>{val}</option>")
            else:
                sb.append(f"<option value='{key}'>{val}</option>")

        sb.append("</select>")
        return "".join(sb)

    @staticmethod
    def get_list_from_list(name: str, selected_val: int, list_data: list[str]) -> str:
        """
        Generate an HTML SELECT element from a list.

        Args:
            name:         The name attribute of the <select> element.
            selected_val: The integer key of the option to pre-select.
            list_data:    A list of strings for the options.

        Returns:
            An HTML <select> string with a default --Select-- option.
        """
        sb = [f"<select class='form-control' name='{name}'>"]
        sb.append("<option value='0'>--Select--</option>")

        for key, val in enumerate(list_data):
            if key == selected_val:
                sb.append(f"<option selected value='{val}'>{val}</option>")
            else:
                sb.append(f"<option value='{val}'>{val}</option>")

        sb.append("</select>")
        return "".join(sb)

    @staticmethod
    def get_list_from_beans(name: str, selected_val: int, bean_list: list[DropdownItem]) -> str:
        """
        Generate an HTML SELECT element from a list of DropdownItem objects.

        Args:
            name:         The name attribute of the <select> element.
            selected_val: The integer key of the option to pre-select.
            bean_list:    A list of DropdownItem objects, sorted automatically by key.

        Returns:
            An HTML <select> string with a default --Select-- option.
        """
        sorted_list = sorted(bean_list, key=lambda o: o.get_key())

        sb = [f"<select class='form-control' name='{name}'>"]
        sb.append("<option value=''>--Select--</option>")

        for obj in sorted_list:
            key = obj.get_key()
            val = obj.get_value()

            if key == selected_val:
                sb.append(f"<option selected value='{key}'>{val}</option>")
            else:
                sb.append(f"<option value='{key}'>{val}</option>")

        sb.append("</select>")
        return "".join(sb)
