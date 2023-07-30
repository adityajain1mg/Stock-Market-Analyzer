from dataclasses import dataclass

@dataclass
class Stock: 
    symbol: str
    date: str
    close: list(float)
    ma: list(float)
    rsi: list(float)
    max: float
    min: float
    avg: float
