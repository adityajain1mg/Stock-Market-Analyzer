from dataclasses import dataclass

class Stock: 
    stock: str
    date: str
    close: list(float)
    ma: list(float)
    rsi: list(float)
    max: float
    min: float
    avg: float