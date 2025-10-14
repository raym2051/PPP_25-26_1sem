

if __name__ == "__main__":
    #Пример таблицы JSON
    dano = {
        'users': [{
            'name': 'Roma',
            'age': 18,
            'city': 'Moscow'
        }, {
            'name': 'Annya',
            'age': 19,
            'city': 'Piter'
        }]
    }
    
    def unbox(dano, history=None, count=0):
        if history is None:
            history = []
    
        if isinstance(dano, dict):
            for key, value in dano.items():
                history.append((count, str(key), value))
                unbox(value, history, count + 1)
    
        elif isinstance(dano, list):
            for i in range(len(dano)):
                history.append((count, str(i), dano[i]))
                unbox(dano[i], history, count + 1)
    
        return history
    
    ans = unbox(dano)
    
    for item in ans:
        print(f'Дальность {item[0]}, Ключ/Индекс "{item[1]}": {item[2]}')
