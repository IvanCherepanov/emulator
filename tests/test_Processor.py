from emulator.processor.instruction import Instruction, Program
from emulator.processor.main import Processor
from emulator.processor.value_object import Opcode, AddressingMode


def test_sum_array():
    processor = Processor(mem_size=16)

    processor.DMEM = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    instructions = [
        Instruction(Opcode.LDA, AddressingMode.DIRECT, 0),  # LDA 0 (Прямая адресация)
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 1),  # ADD 1 (Прямая адресация)
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 2),  # ADD 2 (Прямая адресация)
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 3),  # ADD 3 (Прямая адресация)
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 4),  # ADD 4 (Прямая адресация)
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 5),  # ADD 5 (Прямая адресация)
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 6),  # ADD 6 (Прямая адресация)
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 7),  # ADD 7 (Прямая адресация)
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 8),  # ADD 8 (Прямая адресация)
        Instruction(Opcode.HLT, AddressingMode.DIRECT, 0)   # HLT
    ]

    program = Program()
    # Загружаем инструкции в память процессора
    for i, instr in enumerate(instructions):
        program.add_instruction(instruction=instr)

    processor.load_program(program=program)
    processor.run()

    # Проверяем результат
    assert processor.AC == sum(processor.DMEM), f"Expected {sum(processor.DMEM)}, got {processor.AC}"


def test_sum_array_different_memory():
    processor = Processor(mem_size=1024)

    processor.DMEM = [1, 2, 30, 4, 5, 6, 7, 8, 9, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 10000]

    instructions = [
        Instruction(Opcode.LDA, AddressingMode.DIRECT, 0), #LDA ? 0 (Прямая адресация) : AC=1
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 1),  # ADD ? 1 (Прямая адресация) : AC=3
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 2),  # ADD ? 2 (Прямая адресация) : AC=33
        Instruction(Opcode.STA, AddressingMode.REGISTER, 3),  # STA / 3 (Прямая адресация) : REG_A=33
        Instruction(Opcode.ADD, AddressingMode.IMMEDIATE, 50),  # ADD # 50 (Непосредственная адресация) : AC=83
        Instruction(Opcode.ADD, AddressingMode.REGISTER, 0),  # ADD / 0 (Регистровая адресация) : AC=116
        Instruction(Opcode.ADD, AddressingMode.INDIRECT_REGISTER, 2),  # ADD @ 2 (Косвенно-регистровая адресация)
                                                                               # : 2->30. dmem[30]=10000. AC=10116
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 7),  # ADD ? 7 (Прямая адресация) : AC=10124
        Instruction(Opcode.ADD, AddressingMode.DIRECT, 8),  # ADD ? 8 (Прямая адресация) : AC=10133
        Instruction(Opcode.HLT, AddressingMode.DIRECT, 0)   # HLT : выход
    ]

    program = Program()
    # Загружаем инструкции в память процессора
    for i, instr in enumerate(instructions):
        program.add_instruction(instruction=instr)

    processor.load_program(program=program)
    processor.run()

    # Проверяем результат
    assert processor.AC == 10133, f"Expected {sum(processor.DMEM)}, got {processor.AC}"