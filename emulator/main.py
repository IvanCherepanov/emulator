from emulator.assembler.main import Assembler
from emulator.common.utils import load_asm_from_file, save_machine_code
from emulator.processor.instruction import Program, Instruction
from emulator.processor.main import Processor
from emulator.processor.value_object import Opcode, AddressingMode


def processor_start():
    """Пример использования: создание программы и выполнение на процессоре"""
    program = Program()

    # Добавляем инструкции в программу
    program.add_instruction(Instruction(Opcode.LDA, AddressingMode.DIRECT, 0))  # LDA 0
    program.add_instruction(Instruction(Opcode.ADD, AddressingMode.DIRECT, 1))  # ADD 1
    program.add_instruction(Instruction(Opcode.SUB, AddressingMode.DIRECT, 2))  # SUB 2
    program.add_instruction(Instruction(Opcode.ADD, AddressingMode.DIRECT, 3))  # ADD 3
    program.add_instruction(Instruction(Opcode.ADD, AddressingMode.DIRECT, 4))  # ADD 4
    program.add_instruction(Instruction(Opcode.ADD, AddressingMode.DIRECT, 5))  # ADD 5
    program.add_instruction(Instruction(Opcode.ADD, AddressingMode.DIRECT, 6))  # ADD 6
    program.add_instruction(Instruction(Opcode.STA, AddressingMode.DIRECT, 7))  # STA 7
    program.add_instruction(Instruction(Opcode.HLT, AddressingMode.DIRECT, 0))  # HLT

    # Инициализируем процессор и загружаем программу
    processor = Processor()
    processor.DMEM[0] = 10
    processor.DMEM[1] = 20
    processor.DMEM[2] = 30
    processor.DMEM[3] = 40
    processor.DMEM[4] = 50
    processor.DMEM[5] = 60
    processor.DMEM[6] = 70
    processor.load_program(program)

    processor.run()


def assembler_start():
    assembler = Assembler()

    # Чтение программы на ассемблере из файла
    asm_code = load_asm_from_file('program.asm')

    # Ассемблируем программу
    machine_code = assembler.assemble(asm_code)

    # Сохраняем машинный код в файл
    save_machine_code(machine_code, 'machine_code.txt')

    # Инициализируем процессор и загружаем программу
    processor = Processor()
    processor.DMEM[0] = 10  # Пример данных
    processor.DMEM[1] = 20
    processor.DMEM[2] = 30
    processor.load_machine_code_program(machine_code)

    # Запускаем процессор
    processor.run()


if __name__ == "__main__":
    processor_start()
    # assembler_start()
