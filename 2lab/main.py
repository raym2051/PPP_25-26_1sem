

if __name__ == "__main__":
    print('Возможные операции: +; -; *; /')
    roman_number = input('Введите римсике цифры и операции: ')
    
    roman_data = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    def number(rom):
        if '-' in rom or '+' in rom or '*' in rom or '/' in rom:
            return rom
        else:
            arab_number = 0
            total = 0
            for index in rom[::-1]:
                rec = roman_data[index]
                if rec < total:
                    arab_number -= rec
                else:
                    arab_number += rec
                total = rec
            return arab
    
    def calculation(sting):
        list = sting.split(' ')
        line = ''
        for subject in list:
            line += str(number(subject))
        number_of_end = eval(line)
        if number_of_end <= 0:
            return 'Операция невозможна'
        else:
            return number_of_end
    
    print(f'Результат операции: {calculation(roman_number)}')
