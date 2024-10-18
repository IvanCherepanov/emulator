from emulator.assembler.main import Assembler
from emulator.common.utils import load_asm_from_file, save_machine_code
from emulator.processor.main import Processor


def test_assemble_and_run():
    """Тест программы ассемблера"""
    assembler = Assembler()

    # Чтение программы на ассемблере из файла
    asm_code = load_asm_from_file('program.asm')
    # Перевод команд в машинные коды
    machine_code = assembler.assemble(asm_code)

    # Сохраняем машинный код в файл
    save_machine_code(machine_code, 'machine_code_2.txt')

    # Инициализируем процессор и загружаем программу
    processor = Processor()
    # Загружаем секцию данных в память процессора
    for i, value in enumerate(assembler.data_section):
        processor.DMEM[i] = value

    processor.load_machine_code_program(machine_code)

    # Запускаем процессор
    processor.run()

    assert processor.registers['A'] == sum(processor.DMEM[1:])
