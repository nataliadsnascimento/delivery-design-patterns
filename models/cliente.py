from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    nome: str
    telefone: str
    endereco: Optional[str] = None
    primeira_compra: bool = True
    id: Optional[int] = None  