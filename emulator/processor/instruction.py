from emulator.common.settings import logger
from emulator.processor.value_object import Opcode, AddressingMode


class Instruction:
    """Сущность для инструкции"""
    def __init__(self, opcode: Opcode, addr_type: AddressingMode, operand: int):
        self.opcode = opcode
        self.addr_type = addr_type
        self.operand = operand

    def encode(self):
        """
        Кодирует команду в 16-битное число для хранения в памяти.
        Формат: [4 бита - команда | 2 бита - адресация | 10 бит - адрес].
        """
        logger.debug(self.__dict__)
        return (self.opcode.value << 12) | (self.addr_type.value << 10) | (self.operand & 0x3FF)

    @staticmethod
    def decode(encoded_instruction):
        """
        Декодирует 16-битное число обратно в поля инструкции.
        :param encoded_instruction: 16-битное число
        :return: кортеж (opcode, addr_type, operand)
        """
        opcode = Opcode((encoded_instruction >> 12) & 0xF)
        addr_type = AddressingMode((encoded_instruction >> 10) & 0x3)
        operand = encoded_instruction & 0x3FF

        return opcode, addr_type, operand

    @staticmethod
    def from_machine_code(machine_code_str: str):
        """
        Преобразует строку машинного кода в объект Instruction.
        :param machine_code_str: строка с 16-битным машинным кодом (например, "0001000000000000")
        :return: экземпляр Instruction
        """
        # Преобразуем строку в 16-битное целое число
        encoded_instruction = int(machine_code_str, 2)

        # Декодируем инструкцию
        opcode, addr_type, operand = Instruction.decode(encoded_instruction)

        # Возвращаем экземпляр Instruction
        return Instruction(opcode, addr_type, operand)


class Program:
    """Класс для программы"""
    def __init__(self):
        self.instructions = []

    def add_instruction(self, instruction: Instruction):
        """
        Добавляет инструкцию в программу.
        :param instruction: Объект класса Instruction
        """
        self.instructions.append(instruction.encode())

    def get_instructions(self):
        """
        Возвращает закодированные инструкции программы.
        :return: Список закодированных инструкций
        """
        return self.instructions
