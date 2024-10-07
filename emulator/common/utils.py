from typing import List


def load_asm_from_file(filename) -> List[str]:
    """
    Чтение программы на ассемблере из файла.
    """
    with open(filename, 'r') as file:
        return file.readlines()


def save_machine_code(machine_code, filename) -> None:
    """
    Сохранение машинного кода в файл.
    """
    with open(filename, 'w') as file:
        for code in machine_code:
            file.write(f"{format(code, '016b')}\n")
