class Configuracao:

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)

            cls._instancia.taxa_servico = 0.10
            cls._instancia.frete_base = 5.0
            cls._instancia.frete_gratis_acima = 100.0

        return cls._instancia