from emulator.assembler.main import Assembler
from emulator.processor.main import Processor


def assemble_and_run(asm_code, expected_value, initial_dmem_values):
    """
    Тест программы ассемблера
    :param expected_value:
    :param asm_code: Список строк с программой на ассемблере
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

    assert processor.registers['A'] == expected_value



def test_sum_of_elements():
    """Сложение всех элементов массива"""
    asm_code = [
        "LDA #0",  # Загружаем адрес первого элемента массива: длину массива
        "STA /B",  # Сохраняем адрес в регистре B (адрес текущего элемента) в регистр в - это адрес длина массива
        "LDA @B",  # Загружаем длину массива (по первому элементу) - должна быть длина массива сейчас в аккумуляторе
        "ADD #1",  # Прибавляем 1, чтобы получить адрес последнего элемента
        "STA /C",  # Сохраняем адрес последнего элемента в регистре C
        "LDA #1",  # Инициализируем сумму в аккумуляторе
        "STA /B",  # Сохраняем сумму в регистре B
        "LDA #0",  # Инициализируем сумму в аккумуляторе
        "STA /A",  # Сохраняем сумму в регистре A

        "LOOP:",  # Метка цикла
        "LDA /B",  # Загружаем адрес текущего элемента # 10
        "LDA @B",  # Загружаем значение текущего элемента
        "ADD /A",  # Добавляем значение к сумме
        "STA /A",  # Сохраняем новую сумму в регистре A # 13
        "LDA /B",  # Загружаем адрес текущего элемента
        "ADD #1",  # Увеличиваем адрес на 1 (переход к следующему элементу) # 15
        "STA /B",  # Сохраняем обновлённый адрес # 16
        "LDA /B",  # Загружаем новый адрес текущего элемента
        "CMP /C",  # Сравниваем текущий адрес с адресом последнего элемента # 16
        "JZ END",  # Переход к концу, если адрес совпал (достигнут конец массива)
        "JMP LOOP",  # Переход к началу цикла

        "END:",  # Метка конца программы
        'HLT #0'  # Выход
    ]

    initial_dmem_values = [5, 20, 30, 40, 50, 60]
    expected_dmem_value = sum(initial_dmem_values[1:])  # Ожидаемая сумма в DMEM[7]

    assemble_and_run(asm_code, expected_dmem_value, initial_dmem_values)