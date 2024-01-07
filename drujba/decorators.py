from Style import error_message


def input_error(func):
    def wrapper(*args):
        try:

            return func(*args)
        except IndexError as index_ex_message:
            return error_message(index_ex_message)
        except ValueError as val_ex_message:
            return error_message(val_ex_message)
        except KeyError as key_ex_message:
            return error_message(key_ex_message)
        except TypeError as type_ex_message:
            return error_message(type_ex_message)
        except AttributeError as atr_ex_message:
            return error_message(atr_ex_message)
        except ZeroDivisionError as zero_div_ex_message:
            return error_message(zero_div_ex_message)
        except FileNotFoundError as file_not_found_ex_message:
            return error_message(file_not_found_ex_message)
        except PermissionError as permission_ex_message:
            return error_message(permission_ex_message)

    return wrapper
