

if __name__ == "__main__":
    print('Возможные операции: +; -; *; //')
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
        if '-' in rom or '+' in rom or '*' in rom or '//' in rom:
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
    
            if arab - 1000 > 0:
                line += 'M'
                arab -= 1000
    
            elif arab - 500 > 0:
                line += 'D'
                arab -= 500
    
            elif arab - 100 > 0:
                line += 'C'
                arab -= 100
    
            elif arab - 50 > 0:
                line += 'L'
                arab -= 50
    
            elif arab - 10 > 0:
                line += 'X'
                arab -= 10
    
            elif arab - 5 > 0:
                line += 'V'
                arab -= 5
    
            else:
                line += 'I'
                arab -= 1
                
        line = line.replace('VIIII','IX').replace('IIII','IV')\
        .replace('LXXXX','XC').replace('XXXX','XL')\
    .replace('DCCCC','CM').replace('CCCC','CD')
        
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
