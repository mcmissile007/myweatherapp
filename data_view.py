'''
comments
'''

from dataclasses import dataclass,field


@dataclass
class DataView():
    ''''
    comments
    '''
    date : str =  field(init=False)
    text: str = field(init=False)
    temperature: str = field(init=False)
    units: str = field(init=False)

    def show_console(self):
        '''
        show in console
        '''
        print(f"{self.date}")
        print(f">{self.text}")
        print(f">{self.temperature} {self.units}")
        print("\n")
