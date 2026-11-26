"""Estados e transições do pedido usando o padrão State (#14)."""

from abc import ABC, abstractmethod


class TransicaoInvalidaError(ValueError):
    """Lançada quando uma transição de estado não é permitida."""


class EstadoPedido(ABC):
    """Interface base para os estados do ciclo de vida de um pedido."""

    @property
    @abstractmethod
    def nome(self) -> str:
        """Identificador textual do estado."""

    @abstractmethod
    def avancar(self) -> "EstadoPedido":
        """Avança o pedido para o próximo estado válido."""

    @abstractmethod
    def cancelar(self) -> "EstadoPedido":
        """Cancela o pedido, se o estado atual permitir."""

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EstadoPedido):
            return self.nome == other.nome
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Recebido(EstadoPedido):
    @property
    def nome(self) -> str:
        return "recebido"

    def avancar(self) -> EstadoPedido:
        return Preparando()

    def cancelar(self) -> EstadoPedido:
        return Cancelado()


class Preparando(EstadoPedido):
    @property
    def nome(self) -> str:
        return "preparando"

    def avancar(self) -> EstadoPedido:
        return ACaminho()

    def cancelar(self) -> EstadoPedido:
        return Cancelado()


class ACaminho(EstadoPedido):
    @property
    def nome(self) -> str:
        return "a_caminho"

    def avancar(self) -> EstadoPedido:
        return Entregue()

    def cancelar(self) -> EstadoPedido:
        raise TransicaoInvalidaError("Não é possível cancelar um pedido que já saiu para entrega.")


class Entregue(EstadoPedido):
    @property
    def nome(self) -> str:
        return "entregue"

    def avancar(self) -> EstadoPedido:
        raise TransicaoInvalidaError("Pedido já foi entregue e não pode avançar.")

    def cancelar(self) -> EstadoPedido:
        raise TransicaoInvalidaError("Não é possível cancelar um pedido já entregue.")


class Cancelado(EstadoPedido):
    @property
    def nome(self) -> str:
        return "cancelado"

    def avancar(self) -> EstadoPedido:
        raise TransicaoInvalidaError("Pedido cancelado não pode avançar.")

    def cancelar(self) -> EstadoPedido:
        raise TransicaoInvalidaError("Pedido já está cancelado.")


ESTADOS: dict[str, type[EstadoPedido]] = {
    "recebido": Recebido,
    "preparando": Preparando,
    "a_caminho": ACaminho,
    "entregue": Entregue,
    "cancelado": Cancelado,
}