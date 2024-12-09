# Início

Projeto de disciplina de Engenharia de Software I - INE5417, para desenvolvimento de um jogo de cartas chamado Rei nos Cantos, utilizando linguagem de programação Python.

# Autores

Yano de Melo Cavalcante, Marina Benvenuti, Jéssica dos Santos.

# Build

<em> Obs: Esse tutorial considera a utilização de um sistema operacional baseado em Linux</em><br>
Para executar o programa é recomendado o uso de um ambiente virtual para isolar as dependências necessárias para sua execução do resto do sistema do usuário. Para isso, execute o seguinte comando:
```bash
python -m venv {venv_name}
```

<em>venv_name</em> sendo o nome do ambiente virtual de sua escolha.
Para ativá-lo e desativá-lo, respectivamente:
```bash
source venv/bin/activate
deactivate
```
Com o ambiente virtual criado e ativado, agora é preciso instalar os pacotes e bibliotecas que o jogo utiliza para funcionar normalmente. Para isso, execute o seguinte comando:
```bash
pip install -r requirements.txt
```

# Run

Com os pacotes instalados, já podemos executar o programa e começar a jogar! Para isso, vá até a pasta 'src/' execute o arquivo 'player_interface.py' a partir do Python:
```bash
$ cd src/
$ python3 player_interface.py
```

# Play

Para entender o funcionamento do Jogo e suas regras, leia a especificação de requisitos em PDF presente na raiz do projeto.

# Troubleshooting
```bash
ModuleNotFoundError: No module named 'tkinter'
```
É possível que, caso você tente iniciar o jogo usando uma distribuição Linux, o sistema aponte para a inexistência do módulo Tkinter.<br> <br>Este é um problema conhecido que pode afetar diversos projetos que dependem de componentes do Tkinter, principalmente porque algumas instalações de Linux podem deliberadamente retirar alguns pacotes/componentes do Python, sendo um deles o TK.<br>
Caso isso aconteça com você, sugerimos, seguir as instruções presentes em: <br>
<a href="https://stackoverflow.com/a/76105219">Stackoveflow - Why does tkinter seems to be missing</a><br>
Tutorial de Instalação Oficial:<br>
<a href="https://tkdocs.com/tutorial/install.html">TkDocs - Installing Tk</a>