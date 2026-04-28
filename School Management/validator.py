class InputValidator:

    @staticmethod
    def int_input(prompt, allow_empty=False, default=None):
        while True:
            value = input(prompt).strip()

            if allow_empty and value == "":
                return default

            try:
                return int(value)
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
