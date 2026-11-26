from config.configuracao import Configuracao

def test_instancia_unica():
    config1 = Configuracao()
    config2 = Configuracao()

    assert config1 is config2


def test_valores_configuracao():
    config = Configuracao()

    assert config.taxa_servico == 0.10
    assert config.frete_base == 5.0
    assert config.frete_gratis_acima == 100.0