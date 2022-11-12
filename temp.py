from typing import Callable, Union, Optional

def we_crash_all(name: Union[str, int, bool, None]) -> str:    
    return f'Привет, {str(name)}, мы всё сломали!'


print(we_crash_all('Наташа'))

