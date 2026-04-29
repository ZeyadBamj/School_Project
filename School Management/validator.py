from datetime import datetime


class InputValidator:

    @staticmethod
    def int_input(prompt, allow_empty=False, default=None):
        while True:
            value = int(input(prompt))

            if allow_empty and value == "":
                return default

            try:
                if value > 0:
                    return int(value)
                else:
                    print("❌ Your Enter must be > 0")
            except ValueError:
                print("❌ Please enter a valid number (int).")

    @staticmethod
    def str_input(prompt, allow_empty=False, default=None):
        while True:
            value = input(prompt).strip()

            if allow_empty and value == "":
                return default

            if value:
                return value

            print("❌ This field cannot be empty.")

    @staticmethod
    def date_input(prompt, allow_empty=False, default=None):
        while True:
            value = input(prompt).strip()

            if allow_empty and value == "":
                return default

            try:
                date = datetime.strptime(value, "%d-%m-%Y")

                if date > datetime.now():
                    print("❌ Date Can't be in the Future.")
                    continue

                return date.strftime("%d-%m-%Y")

            except ValueError:
                print("❌ Invalid date, Use format DD-MM-YYYY (e.g.: 30-1-2025)")

    @staticmethod
    def gui_date_input(value):
        if not value.strip():
            raise ValueError(f"❌ is Empty")

        try:
            gui_date = datetime.strptime(value.strip(), "%d-%m-%Y")
            if gui_date > datetime.now():
                raise Exception("❌ Date Can't be in the Future.")
            return gui_date.strftime("%d-%m-%Y")
        except ValueError:
            raise ValueError(f"❌ must be Enter format DD-MM-YYYY (e.g.: 30-1-2025)")