"""Ponto de entrada: roda a demonstracao completa do sistema de delivery.

Cada funcao abaixo corresponde a uma etapa do roteiro de demonstracao
(secao 9 do PDF do projeto). Elas serao preenchidas conforme as issues
forem concluidas. A versao final e a issue #22.
"""


def preparar_banco():
    # TODO (#5, #6): criar o banco a partir de database/schema.sql e rodar o seed
    print("[1] Banco de dados: pendente")


def demonstrar_singleton():
    # TODO (#4, #5): mostrar que duas chamadas de Configuracao() devolvem o mesmo objeto
    print("[2] Singleton: pendente")


def demonstrar_factory():
    # TODO (#7): criar um pedido de entrega pela fabrica
    print("[3] Factory Method: pendente")


def demonstrar_decorator():
    # TODO (#13): montar pizza com borda recheada e queijo extra
    print("[4] Decorator: pendente")


def demonstrar_strategy():
    # TODO (#11, #12): calcular total com frete e cupom, depois trocar para frete gratis
    print("[5] Strategy: pendente")


def demonstrar_observer():
    # TODO (#16, #17, #18): registrar cliente, cozinha e log como observadores
    print("[6] Observer: pendente")


def demonstrar_state():
    # TODO (#14, #15, #19): avancar o pedido ate Entregue e tentar cancelar depois
    print("[7] State: pendente")


def demonstrar_repository():
    # TODO (#20): recarregar o pedido do banco e imprimir itens, total e historico
    print("[8] Repository: pendente")


def demonstrar_facade():
    # TODO (#21): repetir o fluxo usando apenas a PedidoFacade
    print("[9] Facade: pendente")


def main():
    print("=== Sistema de Delivery ===")
    preparar_banco()
    demonstrar_singleton()
    demonstrar_factory()
    demonstrar_decorator()
    demonstrar_strategy()
    demonstrar_observer()
    demonstrar_state()
    demonstrar_repository()
    demonstrar_facade()


if __name__ == "__main__":
    main()
