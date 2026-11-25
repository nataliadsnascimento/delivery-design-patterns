"""Teste minimo: garante que todas as pastas do projeto sao importaveis."""


def test_pacotes_importaveis():
    import config, database, models, factories, adicionais  # noqa: F401
    import strategies, states, observers, repositories, facade  # noqa: F401
