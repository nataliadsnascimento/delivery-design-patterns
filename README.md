# Sistema de Delivery de Restaurante

Projeto da disciplina de **Padroes de Projeto**. Sistema de pedidos de delivery em Python com banco SQLite, usando 7 padroes GoF.

> README inicial. A versao completa (com diagramas e exemplos) e a issue #25.

## Padroes utilizados

| Padrao | Onde |
|---|---|
| Singleton | `config/`, `database/conexao.py` |
| Factory Method | `factories/` |
| Decorator | `adicionais/` |
| Strategy | `strategies/` |
| State | `states/` |
| Observer | `observers/` |
| Facade | `facade/` |

O acesso ao banco usa Repository (`repositories/`), que e um complemento e nao conta entre os 7.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m database.seed          # cria o banco com dados iniciais (apos a issue #6)
python main.py                   # roda a demonstracao
pytest                           # roda os testes
```

## Equipe

| Integrante | Responsabilidade |
|---|---|
| Pessoa 1 | Singleton, Factory Method, base do projeto, banco e integracao |
| Pessoa 2 | Strategy, Decorator, Facade e ProdutoRepository |
| Pessoa 3 | State, PedidoRepository e itens concretos |
| Pessoa 4 | Observer, diagramas, README e apresentacao |

## Como contribuir

1. `git checkout develop && git pull`
2. `git checkout -b feature/nome-da-tarefa`
3. Commits pequenos, ex.: `feat(strategy): adiciona frete por distancia`
4. `git push -u origin feature/nome-da-tarefa` e abra um Pull Request para **develop**
5. Peca revisao a pelo menos uma pessoa. Use `Closes #N` na descricao do PR.

Nao e permitido dar push direto em `main` nem em `develop`.
