from typing import List

from emulator.common.settings import logger
from emulator.processor.main import AddressingMode, Opcode, Instruction
from emulator.processor.value_object import GeneralProposeRegisters


class Assembler:
    def __init__(self):
        self.instructions = []
        self.label_map = {}
        self.label_counter = 0
        self.data_section = []
        self.is_data_section = False

    def assemble(self, asm_code) -> List[int]:
        """
        Переводит текст программы в машинные коды.
        :param asm_code: список строк ассемблерных команд
        :return: список 16-битных машинных кодов
        """

        # Первый проход для определения меток и данных
        for line in asm_code:
            line = line.strip()
            # Проверка на секции данных и команд
            if line == ".data":
                self.in_data_section = True
                continue
            elif line == ".code":
                self.in_data_section = False
                continue

            if self.in_data_section:
                if line.startswith("num"):
                    self.data_section.append(int(line.split()[1]))
            else:
                if line.endswith(":"):
                    self.label_map[line[:-1]] = self.label_counter
                    # self.label_counter += 1 ## добавлять не нужно, т.к в кодах программы это будет ошибкой
                else:
                    self.label_counter += 1
        logger.debug(f"self.label_map: {self.label_map}")

        for line in asm_code:
            if not line.endswith(":") and not line.startswith('.') and not line.startswith('num'):
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                opcode_str = parts[0]
                addr_mode_str = parts[1][0]
                operand_str = parts[1][1:]
                logger.debug(f"parts: {parts}, "
                             f"opcode_str: {opcode_str}, "
                             f"addr_mode_str: {addr_mode_str}, "
                             f"operand_str: {operand_str}")

                opcode = self._parse_opcode(opcode_str)

                if opcode in [Opcode.JZ, Opcode.JMP]:
                    label = parts[1]
                    addr_label = self.label_map.get(label)
                    logger.debug(f"label:, {label}, addr_label:, {addr_label}")

                    instruction = Instruction(opcode, AddressingMode.IMMEDIATE, addr_label)
                else:
                    addr_mode = self._parse_addressing_mode(addr_mode_str)
                    operand = self._parse_operand_str(operand_str)
                    logger.debug(f"opcode: {opcode}, addr_mode: {addr_mode}, operand:{operand}")

                    instruction = Instruction(opcode, addr_mode, operand)
                self.instructions.append(instruction.encode())
        logger.debug(f"len(self.instructions): {len(self.instructions)}")
        return self.instructions

    def _parse_operand_str(self, operand_str):
        if GeneralProposeRegisters.has_member(operand_str):
            return int(GeneralProposeRegisters[operand_str].value)
        logger.debug(f"operand_str: {operand_str}, "
                     f"GeneralProposeRegisters.has_member(operand_str):{GeneralProposeRegisters.has_member(operand_str)}")

        return int(operand_str)

    def _parse_opcode(self, opcode_str):
        """
        Парсинг строковой команды в соответствующий Opcode.
        """
        try:
            return Opcode[opcode_str.upper()]
        except KeyError:
            raise ValueError(f"Неизвестная команда: {opcode_str}")

    def _parse_addressing_mode(self, addr_mode_str: str):
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
