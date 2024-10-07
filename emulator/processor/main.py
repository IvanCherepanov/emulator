from emulator.processor.instruction import Program, Instruction
from emulator.processor.value_object import Opcode, AddressingMode


class Processor:
    """Процессор для выполнения программы"""
    def __init__(self, mem_size=4096):
        self.AC = 0             # Аккумулятор
        self.IR = 0             # Регистр команд
        self.PC = 0             # Программный счетчик
        self.FLAGS = 0          # Регистр флагов
        self.REG_A = 0          # Дополнительный регистр A

        self.CMEM = [0] * mem_size   # Память для команд
        self.DMEM = [0] * mem_size   # Память для данных

    def load_machine_code_program(self, machine_code):
        """
        Загружает скомпилированную программу в память.
        :param machine_code: список 16-битных машинных кодов
        """
        for i, instruction in enumerate(machine_code):
            self.CMEM[i] = instruction

    def load_program(self, program: Program):
        """
        Загружает программу в память процессора.
        :param program: Объект класса Program
        """
        instructions = program.get_instructions()
        self.load_machine_code_program(machine_code=instructions)
        # for i, instruction in enumerate(instructions):
        #     self.CMEM[i] = instruction

    def run(self):
        while True:
            # Чтение команды
            self.IR = self.CMEM[self.PC]
            self.PC += 1

            # Декодирование команды
            opcode, addr_type, operand = Instruction.decode(self.IR)

            # Выполнение команды
            if opcode == Opcode.LDA:
                self.lda(operand, addr_type)
            elif opcode == Opcode.ADD:
                self.add(operand, addr_type)
            elif opcode == Opcode.SUB:
                self.sub(operand, addr_type)
            elif opcode == Opcode.STA:
                self.sta(operand, addr_type)
            elif opcode == Opcode.JMP:
                self.jmp(operand)
            elif opcode == Opcode.HLT:
                break  # Остановка процессора
            else:
                raise Exception(f"Неизвестная команда: {opcode}")

            # Вывод текущего состояния процессора
            self.print_state(opcode, addr_type, operand)

    # Определение команд процессора
    def lda(self, operand, addr_type):
        if addr_type == AddressingMode.DIRECT:  # Прямая адресация
            self.AC = self.DMEM[operand]
        elif addr_type == AddressingMode.IMMEDIATE:  # Непосредственная адресация
            self.AC = operand
        elif addr_type == AddressingMode.REGISTER:  # Регистровая адресация
            self.AC = self.REG_A
        elif addr_type == AddressingMode.INDIRECT_REGISTER:  # Косвенно-регистровая адресация
            indirect_address = self.DMEM[operand]
            if 0 <= indirect_address < len(self.DMEM):
                self.AC = self.DMEM[indirect_address]
            else:
                raise IndexError(f"Неверный косвенный адрес: {indirect_address}")

    def add(self, operand, addr_type):
        if addr_type == AddressingMode.DIRECT:  # Прямая адресация
            self.AC += self.DMEM[operand]
        elif addr_type == AddressingMode.IMMEDIATE:  # Непосредственная адресация
            self.AC += operand
        elif addr_type == AddressingMode.REGISTER:  # Регистровая адресация
            self.AC += self.REG_A
        elif addr_type == AddressingMode.INDIRECT_REGISTER:  # Косвенно-регистровая адресация
            indirect_address = self.DMEM[operand]
            print("operand: ", operand,
                  "indirect_address: ", indirect_address,
                  "self.DMEM[indirect_address]: ", self.DMEM[indirect_address])
            if 0 <= indirect_address < len(self.DMEM):
                self.AC += self.DMEM[indirect_address]
            else:
                raise IndexError(f"Неверный косвенный адрес: {indirect_address}")

    def sub(self, operand, addr_type):
        if addr_type == AddressingMode.DIRECT:  # Прямая адресация
            self.AC -= self.DMEM[operand]
        elif addr_type == AddressingMode.IMMEDIATE:  # Непосредственная адресация
            self.AC -= operand
        elif addr_type == AddressingMode.REGISTER:  # Регистровая адресация
            self.AC -= self.REG_A
        elif addr_type == AddressingMode.INDIRECT_REGISTER:  # Косвенно-регистровая адресация
            indirect_address = self.DMEM[operand]
            if 0 <= indirect_address < len(self.DMEM):
                self.AC -= self.DMEM[indirect_address]
            else:
                raise IndexError(f"Неверный косвенный адрес: {indirect_address}")

    def sta(self, operand, addr_type):
        if addr_type == AddressingMode.DIRECT:  # Прямая адресация
            self.DMEM[operand] = self.AC
        elif addr_type == AddressingMode.REGISTER:  # Регистровая адресация
            self.REG_A = self.AC
        elif addr_type == AddressingMode.INDIRECT_REGISTER:  # Косвенно-регистровая адресация
            indirect_address = self.DMEM[operand]
            if 0 <= indirect_address < len(self.DMEM):
                self.DMEM[indirect_address] = self.AC
            else:
                raise IndexError(f"Неверный косвенный адрес: {indirect_address}")

    def jmp(self, operand):
        self.PC = operand

    def print_state(self, opcode, addr_type, operand):
        """
        Выводит текущее состояние процессора, включая декодированные поля инструкции.
        """
        print(f"PC: {self.PC}, IR: {self.IR}, AC: {self.AC}, FLAGS: {self.FLAGS}, REG_A: {self.REG_A}")
        print(f"Текущая команда: {opcode.name}, Тип адресации: {addr_type.name}, Операнд: {operand}")
        print(f"Машинный код команды: {format(self.IR, '016b')}. "
              f"Код команды: {format(self.IR >> 12, '04b')} "
              f"Тип адресации: {format((self.IR >> 10) & 0x3, '02b')} "
              f"Адрес: {format(self.IR & 0x3FF, '010b')}")
        print(f"DMEM: {self.DMEM[:10]} \n")  # Вывод первых 10 элементов памяти
