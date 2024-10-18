from emulator.processor.instruction import Instruction, Program
from emulator.processor.main import Processor
from emulator.processor.value_object import Opcode, AddressingMode


def test_sum_array():
    processor = Processor(mem_size=32)

    processor.DMEM = [5, 20, 30, 40, 50, 60]

    instructions = [
        Instruction(Opcode.LDA, AddressingMode.IMMEDIATE, 0),
        Instruction(Opcode.STA, AddressingMode.REGISTER, 2),
        Instruction(Opcode.LDA, AddressingMode.INDIRECT_REGISTER, 2),
        Instruction(Opcode.ADD, AddressingMode.IMMEDIATE, 1),
        Instruction(Opcode.STA, AddressingMode.REGISTER, 3),
        Instruction(Opcode.LDA, AddressingMode.IMMEDIATE, 1),

        Instruction(Opcode.STA, AddressingMode.REGISTER, 2),
        Instruction(Opcode.LDA, AddressingMode.IMMEDIATE, 0),
        Instruction(Opcode.STA, AddressingMode.REGISTER, 1),
        Instruction(Opcode.LDA, AddressingMode.REGISTER, 2),
        Instruction(Opcode.LDA, AddressingMode.INDIRECT_REGISTER, 2),

        Instruction(Opcode.ADD, AddressingMode.REGISTER, 1),
        Instruction(Opcode.STA, AddressingMode.REGISTER, 1),
        Instruction(Opcode.LDA, AddressingMode.REGISTER, 2),
        Instruction(Opcode.ADD, AddressingMode.IMMEDIATE, 1),
        Instruction(Opcode.STA, AddressingMode.REGISTER, 2),
        Instruction(Opcode.LDA, AddressingMode.REGISTER, 2),
        Instruction(Opcode.CMP, AddressingMode.REGISTER, 3),
        Instruction(Opcode.JZ, AddressingMode.IMMEDIATE, 20),
        Instruction(Opcode.JMP, AddressingMode.IMMEDIATE, 9),
        Instruction(Opcode.HLT, AddressingMode.IMMEDIATE, 0),

    ]

    program = Program()
    # Загружаем инструкции в память процессора
    for i, instr in enumerate(instructions):
        program.add_instruction(instruction=instr)

    processor.load_program(program=program)
    processor.run()

    # Проверяем результат
    assert processor.registers['A'] == sum(processor.DMEM[1:]), f"Expected {sum(processor.DMEM)}, got {processor.AC}"
