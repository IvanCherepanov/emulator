from emulator.assembler.main import Assembler
from emulator.processor.main import Processor


def assemble_and_run(asm_code, expected_dmem_values, initial_dmem_values):
    """
    Тест программы ассемблера
    :param asm_code: Список строк с программой на ассемблере
    :param expected_dmem_values: Ожидаемые значения в памяти данных после выполнения программы
    :param initial_dmem_values: Исходные значения в памяти данных (массив)
    """
    assembler = Assembler()

    machine_code = assembler.assemble(asm_code)

    # Инициализируем процессор и загружаем программу
    processor = Processor()
    processor.DMEM[:len(initial_dmem_values)] = initial_dmem_values  # Задаем начальные значения
    processor.load_machine_code_program(machine_code)

    # Запускаем процессор
    processor.run()

    # Проверяем значения в памяти данных после выполнения программы
    for address, expected_value in expected_dmem_values.items():
        assert processor.DMEM[
                   address] == expected_value, f"Ошибка в DMEM[{address}]: ожидается {expected_value}, получено {processor.DMEM[address]}"

    print("Тест пройден успешно")


def test_sum_of_elements():
    """Сложение всех элементов массива"""
    asm_code = [
        "LDA ? 0",
        "ADD ? 1",
        "ADD ? 2",
        "ADD ? 3",
        "ADD ? 4",
        "ADD ? 5",
        "ADD ? 6",
        "STA ? 7",
        "HLT ? 0"
    ]

    initial_dmem_values = [10, 20, 30, 40, 50, 60, 70]
    expected_dmem_values = {7: 280}  # Ожидаемая сумма в DMEM[7]

    assemble_and_run(asm_code, expected_dmem_values, initial_dmem_values)


def test_add_and_subtract_elements():
    """Сложение и вычитание элементов массива"""
    asm_code = [
        "LDA ? 0",
        "ADD ? 1",
        "SUB ? 2",
        "ADD ? 3",
        "SUB ? 4",
        "ADD ? 5",
        "STA ? 7",
        "HLT ? 0"
    ]

    initial_dmem_values = [100, 50, 30, 20, 10, 60]
    expected_dmem_values = {7: 190}  # Ожидаемый результат в DMEM[7]

    assemble_and_run(asm_code, expected_dmem_values, initial_dmem_values)


def test_difference_between_groups():
    """Разница между двумя группами элементов"""
    asm_code = [
        "LDA ? 0",
        "ADD ? 1",
        "ADD ? 2",
        "STA ? 7",
        "LDA ? 3",
        "ADD ? 4",
        "ADD ? 5",
        "SUB ? 7",
        "STA ? 8",
        "HLT ? 0"
    ]

    initial_dmem_values = [10, 20, 30, 100, 50, 25]
    expected_dmem_values = {7: 60, 8: 115}  # Ожидаемые результаты в DMEM[7] и DMEM[8]

    assemble_and_run(asm_code, expected_dmem_values, initial_dmem_values)


def test_different_memory():
    """Разница между двумя группами элементов"""
    asm_code = [
        "LDA ? 0",
        "ADD ? 1",
        "ADD ? 2",
        "STA / 3",
        "ADD # 50",
        "ADD / 0",
        "ADD @ 2",
        "ADD ? 7",
        "ADD ? 8",
        "STA ? 31",
        "HLT ? 0"
    ]

    initial_dmem_values = [1, 2, 30, 4, 5, 6, 7, 8, 9, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 10000]
    expected_dmem_values = {0: 1, 1: 2, 30: 10000, 31:10133}  # Ожидаемые результаты в DMEM[7] и DMEM[8]

    assemble_and_run(asm_code, expected_dmem_values, initial_dmem_values)
