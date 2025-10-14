

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
    
    def rom_number(rom):
        if '-' in rom or '+' in rom or '*' in rom or '/' in rom:
            return rom
        else:
            arab = 0
            total = 0
            for index in rom[::-1]:
                rec = roman_data[index]
                if rec < total:
                    arab -= rec
                else:
                    arab += rec
                total = rec
            return arab
    
    def arab_number(arab):
        line = ''
        while arab > 0:
    
            if arab - roman_data['M'] > 0:
                line += 'M'
                arab -= roman_data['M']
    
            elif arab - roman_data['D'] > 0:
                line += 'D'
                arab -= roman_data['D']
    
            elif arab - roman_data['C'] > 0:
                line += 'C'
                arab -= roman_data['C']
    
            elif arab - roman_data['L'] > 0:
                line += 'L'
                arab -= roman_data['L']
    
            elif arab - roman_data['X'] > 0:
                line += 'X'
                arab -= roman_data['X']
    
            elif arab - roman_data['V'] > 0:
                line += 'V'
                arab -= roman_data['V']
    
            else:
                line += 'I'
                arab -= roman_data['I']
    
        return line
    
    def calculation(sting):
        list = sting.split(' ')
        line = ''
        for subject in list:
            line += str(rom_number(subject))
    
        number = eval(line)
        if number <= 0:
            return 'Операция невозможна'
        else:
            return arab_number(number)
    
    print(f'Результат операции: {calculation(roman_number)}')
