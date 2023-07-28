from dataclasses import dataclass

@dataclass
class Stock:
    stock:str
    open:dict
    close:dict
    avg:float
    max:float
    min:float
    ma:dict
    rsi:dict

    
