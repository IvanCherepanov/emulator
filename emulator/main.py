from emulator.assembler.main import Assembler
from emulator.common.utils import load_asm_from_file, save_machine_code
from emulator.processor.instruction import Program, Instruction
from emulator.processor.main import Processor
from emulator.processor.value_object import Opcode, AddressingMode


def processor_start():
    """Пример использования: создание программы и выполнение на процессоре"""
    machine_code = [
        5120,
        18434,
        7170,
        9217,
        18435,
        5121,
        18434,
        5120,
        18433,
        6146,
        7170,
        10241,
        18433,
        6146,
        9217,
        18434,
        6146,
        30723,
        25620,
        21513,
        62464
    ]

    # Инициализируем процессор и загружаем программу
    processor = Processor()
    processor.DMEM[0] = 5  # размер массива
    processor.DMEM[1] = 20
    processor.DMEM[2] = 30
    processor.DMEM[3] = 40
    processor.DMEM[4] = 50
    processor.DMEM[5] = 60
    processor.load_machine_code_program(machine_code)

    # Запускаем процессор
    # print(processor.CMEM)
    # print('\n\n')
    # for i in range(21):
    #     print(processor.CMEM[i], Instruction.decode(processor.CMEM[i]))
    #
    # print('\n\n')
    processor.run()
    # print(processor.registers['A'])


def assembler_start():
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
    # print(processor.CMEM)
    # print('\n\n')
    # for i in range(21):
    #     print(processor.CMEM[i], Instruction.decode(processor.CMEM[i]))
    #
    # print('\n\n')
    processor.run()
    # print(processor.registers['A'])

def new_start():
    assembler = Assembler()

    asm_code_2 = [
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
        'HLT #0' # Выход
    ]

    # Чтение программы на ассемблере из файла
    asm_code = load_asm_from_file('program.asm')
    print("Equal: ", asm_code_2 == asm_code, asm_code)
    # Ассемблируем программу
    machine_code = assembler.assemble(asm_code)

    # Сохраняем машинный код в файл
    save_machine_code(machine_code, 'machine_code_2.txt')

    # Инициализируем процессор и загружаем программу
    processor = Processor()
    processor.DMEM[0] = 5  # размер массива
    processor.DMEM[1] = 20
    processor.DMEM[2] = 30
    processor.DMEM[3] = 40
    processor.DMEM[4] = 50
    processor.DMEM[5] = 60
    processor.load_machine_code_program(machine_code)

    # Запускаем процессор
    print(processor.CMEM)
    print('\n\n')
    for i in range(21):
        print(processor.CMEM[i], Instruction.decode(processor.CMEM[i]))

    print('\n\n')
    processor.run()
    print(processor.registers['A'])


if __name__ == "__main__":
    processor_start()
    # assembler_start()
    # new_start()
