from typing import List

from emulator.processor.main import AddressingMode, Opcode, Instruction


class Assembler:
    def __init__(self):
        self.instructions = []

    def assemble(self, asm_code) -> List[int]:
        """
        Переводит текст программы в машинные коды.
        :param asm_code: список строк ассемблерных команд
        :return: список 16-битных машинных кодов
        """
        for line in asm_code:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            opcode_str = parts[0]
            addr_mode_str = parts[1]
            operand_str = parts[2]

            opcode = self.parse_opcode(opcode_str)
            addr_mode = self.parse_addressing_mode(addr_mode_str)
            operand = int(operand_str)

            instruction = Instruction(opcode, addr_mode, operand)
            self.instructions.append(instruction.encode())

        return self.instructions

    def parse_opcode(self, opcode_str):
        """
        Парсинг строковой команды в соответствующий Opcode.
        """
        try:
            return Opcode[opcode_str.upper()]
        except KeyError:
            raise ValueError(f"Неизвестная команда: {opcode_str}")

    def parse_addressing_mode(self, addr_mode_str: str):
        """
        Парсинг строки с типом адресации в соответствующий AddressingMode.
        """
        if addr_mode_str == "?":
            return AddressingMode.DIRECT
        elif addr_mode_str == "#":
            return AddressingMode.IMMEDIATE
        elif addr_mode_str == "/":
            return AddressingMode.REGISTER
        elif addr_mode_str == "@":
            return AddressingMode.INDIRECT_REGISTER
        else:
            raise ValueError(f"Неизвестный тип адресации: {addr_mode_str}")
