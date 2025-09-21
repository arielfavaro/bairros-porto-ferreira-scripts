# Mapa de Bairros de Porto Ferreira - Script de processamento

Este repositório contêm o script responsável por gerar a clusterização de bairros a partir dos dados do [IBGE CNEFE](https://www.ibge.gov.br/estatisticas/sociais/populacao/38734-cadastro-nacional-de-enderecos-para-fins-estatisticos.html) para o município de Porto Ferreira.

Para visualizar os dados gerado na pasta `out` utilize um software GIS (SIG), como o QGIS.

Acesse o resultado do processamento na versão web [aqui](https://bairros.ariel.dev.br).

Repositório da versão web [aqui](https://github.com/arielfavaro/bairros-porto-ferreira).

## Execução do script
```sh
# Criar env
python -m venv env

# Windows
env\Scripts\activate

# Linux
source env/bin/activate

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Executar script
python main.py

# Desativar env
deactivate
```