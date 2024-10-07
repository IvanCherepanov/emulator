from emulator import processor
from emulator.assembler.main import Assembler
from emulator.common.utils import load_asm_from_file
from emulator.processor.instruction import Instruction, Program
from emulator.processor.main import Processor


def test_output_machine_code():
    machine_code = load_asm_from_file('../emulator/machine_code.txt')
    instructions = []
    for machine_code_string in machine_code:
        instructions.append(Instruction.from_machine_code(machine_code_str=machine_code_string))
    print(instructions)

    program = Program()
    # Загружаем инструкции в память процессора
    for i, instr in enumerate(instructions):
        program.add_instruction(instruction=instr)

    processor = Processor()
    processor.DMEM[0] = 10  # Пример данных
    processor.DMEM[1] = 20
    processor.DMEM[2] = 30
    processor.load_machine_code_program(machine_code)
    processor.load_program(program=program)
    processor.run()

    # Проверяем результат
    # todo: убрать привязку к результату, вызывать напрямую метод. Т.к. при изменении данных генерации придется менять теста
    assert processor.AC == 125, f"Expected {sum(processor.DMEM)}, got {processor.AC}"
