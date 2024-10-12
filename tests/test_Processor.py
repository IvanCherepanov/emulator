from emulator.processor.instruction import Instruction, Program
from emulator.processor.main import Processor
from emulator.processor.value_object import Opcode, AddressingMode


def test_sum_array():
    processor = Processor(mem_size=32)

    processor.DMEM = [5, 20, 30, 40, 50, 60]

    instructions = [
        Instruction(Opcode.LDA, AddressingMode.IMMEDIATE, 0),  # LDA 0 (Прямая адресация)
        Instruction(Opcode.STA, AddressingMode.REGISTER, 2),  # ADD 1 (Прямая адресация)
        Instruction(Opcode.LDA, AddressingMode.INDIRECT_REGISTER, 2),  # ADD 2 (Прямая адресация)
        Instruction(Opcode.ADD, AddressingMode.IMMEDIATE, 1),  # ADD 3 (Прямая адресация)
        Instruction(Opcode.STA, AddressingMode.REGISTER, 3),  # ADD 4 (Прямая адресация)
        Instruction(Opcode.LDA, AddressingMode.IMMEDIATE, 1),  # ADD 5 (Прямая адресация)

        Instruction(Opcode.STA, AddressingMode.REGISTER, 2),  # ADD 6 (Прямая адресация)
        Instruction(Opcode.LDA, AddressingMode.IMMEDIATE, 0),  # ADD 7 (Прямая адресация)
        Instruction(Opcode.STA, AddressingMode.REGISTER, 1),  # ADD 8 (Прямая адресация)
        Instruction(Opcode.LDA, AddressingMode.REGISTER, 2),  # ADD 5 (Прямая адресация)
        Instruction(Opcode.LDA, AddressingMode.INDIRECT_REGISTER, 2),  # ADD 6 (Прямая адресация)

        Instruction(Opcode.ADD, AddressingMode.REGISTER, 1),  # ADD 7 (Прямая адресация)
        Instruction(Opcode.STA, AddressingMode.REGISTER, 1),  # ADD 8 (Прямая адресация)
        Instruction(Opcode.LDA, AddressingMode.REGISTER, 2),  # ADD 5 (Прямая адресация)
        Instruction(Opcode.ADD, AddressingMode.IMMEDIATE, 1),  # ADD 6 (Прямая адресация)
        Instruction(Opcode.STA, AddressingMode.REGISTER, 2),  # ADD 7 (Прямая адресация)
        Instruction(Opcode.LDA, AddressingMode.REGISTER, 2),  # ADD 8 (Прямая адресация)
        Instruction(Opcode.CMP, AddressingMode.REGISTER, 3),  # ADD 5 (Прямая адресация)
        Instruction(Opcode.JZ, AddressingMode.IMMEDIATE, 20),  # ADD 6 (Прямая адресация)
        Instruction(Opcode.JMP, AddressingMode.IMMEDIATE, 9),  # ADD 7 (Прямая адресация)
        Instruction(Opcode.HLT, AddressingMode.IMMEDIATE, 0),  # ADD 8 (Прямая адресация)

    ]

    program = Program()
    # Загружаем инструкции в память процессора
    for i, instr in enumerate(instructions):
        program.add_instruction(instruction=instr)

    processor.load_program(program=program)
    processor.run()

    # Проверяем результат
    assert processor.registers['A'] == sum(processor.DMEM[1:]), f"Expected {sum(processor.DMEM)}, got {processor.AC}"
