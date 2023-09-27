![MVP PUC-Rio - Gustavo Duarte Pedrosa](./assets/sushipuc-banner-repo.jpg)

#

&nbsp;
&nbsp;

# Sobre o MVP

A aplicação consiste no projeto de conclusão de Sprint do MBA em Engenharia de Software pela PUC-Rio.

# Tecnologias

- Python
- Flask
- OpenAPI
- SQLite
- SQLAlchemy
- HTML5
- CSS3
- Bootstrap
- JQuery

# API Externa

- [Google reCAPTCHA](https://www.google.com/recaptcha/about/)

  > Utilizo o reCAPTCHA antes de submeter a finalização da compra.

# Como executar?

A aplicação está dividida em 2 repositórios, sendo:

- Back-end (Este repositório)
- [Front-end](https://github.com/gustavoduartep/pucrio-mvp-front)

```powershell

# Acesse a pasta do da aplicação no terminal
$ cd pucrio-mvp-api

# Instale as dependências
$ pip install -r requirements.txt

# Ative o ambiente virtual (Windows)
$ env/Scripts/Activate.ps1

# Execute a aplicação em modo de desenvolvimento
(env)$ flask run --host 0.0.0.0 --port 5000

# Para desativar o ambiente, utilize:
(env)$ Deactivate

# A aplicação será aberta na porta:5000 - acesse http://localhost:5000
```

# Docker

Para construir a imagem Docker, utilize o comando:

```
docker build -t sushiapi .
```

Para executar o container, esteja em modo Administrador e utilize o comando:

```
docker run -d -p 5000:5000 sushiapi
```

> O argumento **-d** executa o container em segundo plano e o **-p** mapeia as portas.

Em caso de dificuldades, por favor, entre em contato.
