from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, redirect, request, send_from_directory, jsonify
import pdb
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy

from flask_paginate import Pagination
from sqlalchemy.orm.query import Query

from model import Session, Item
from schemas import *
from flask_cors import CORS

import requests

from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'  # Diretório para salvar as imagens
ALLOWED_EXTENSIONS = {'png'}  # Extensões permitidas


info = Info(title="SushiPuc API", version="1.1.0")
app = OpenAPI(__name__, info=info)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.sqlite3'

db = SQLAlchemy(app)

app.static_folder = 'uploads'
app.config['UPLOAD_PATH'] = 'uploads'

# Tags

# home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
item_tag = Tag(name="Catálogo",
               description="Gestão de itens do catálogo")
carrinho_tag = Tag(name="Carrinho de Compras",
                   description="Gestão do carrinho de compras")


@app.get('/')
def home():
    return redirect('/openapi/swagger')


@app.post('/item/cadastrar', tags=[item_tag], responses={"200": ItemViewSchema, "409": ErrorSchema, "400": ErrorSchema, "500": ErrorSchema})
def cadastrar_item():
    """Adicionar um item no catálogo de vendas
    """
    try:
        # Extraia os campos do objeto JSON
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        quantidade = request.form.get('quantidade')
        valor = request.form.get('valor')
        peso = request.form.get('peso')
        status = request.form.get('status')

        if status == "true":
            status = True
        else:
            status = False

        nome_imagem = None  # Inicializa nome_imagem como None

        if 'imagem' in request.files:
            imagem = request.files['imagem']

            print(imagem)

            if imagem.filename != '':
                nome_imagem = salvar_arquivo_unico(
                    UPLOAD_FOLDER, secure_filename(imagem.filename))
                imagem.save(os.path.join(UPLOAD_FOLDER, nome_imagem))

        # Crie o objeto Item com os dados recebidos
        item = Item(
            nome=nome,
            descricao=descricao,
            quantidade=quantidade,
            valor=valor,
            peso=peso,
            status=status,
            imagem=f'/uploads/{nome_imagem}' if nome_imagem else None
        )

        sessao = Session()
        sessao.add(item)
        sessao.commit()

        return {"message": "Item cadastrado com sucesso", "item": apresenta_item(item)}, 200

    except IntegrityError as e:
        mensagem_erro = "Item com o mesmo nome já cadastrado"
        return {"message": mensagem_erro}, 409

    except Exception as e:
        mensagem_erro = "Não foi possível cadastrar um novo item"
        print(f"Erro ao cadastrar item: {str(e)}")
        return {"message": mensagem_erro}, 400

    except TypeError as e:
        mensagem_erro = "Problema interno no servidor da aplicação"
        return {"message": mensagem_erro}, 500


@app.get('/item/listar', tags=[item_tag], responses={"200": ListagemItemSchema, "404": ErrorSchema})
def get_itens():
    try:
        sessao = Session()
        itens_query = sessao.query(Item)
        total_itens = itens_query.count()  # Contar o total de itens

        if not itens_query:
            return {"message": "Nenhum item disponível no catálogo"}, 404
        else:
            return apresenta_itens(itens_query), 200

    except Exception as e:
        mensagem_erro = "Não foi possível listar os itens"
        print(f"Erro ao listar itens: {str(e)}")
        return {"message": mensagem_erro}, 400


@app.get('/item/buscar', tags=[item_tag], responses={"200": ItemViewSchema, "404": ErrorSchema})
def lista_item(query: BuscaItemSchema):
    """Faz a busca de um item específico
    Realiza a consulta do item e retorna uma resposta em JSON. Em caso de sucesso retorna o objeto, em caso de falha retorna um feedback negativo.
    """

    try:
        # Obtenha o item_id da query string
        item_id = request.args.get('id', type=int)

        sessao = Session()
        item = sessao.query(Item).filter(Item.id == item_id).first()

        if not item:
            mensagem_erro = "Item não encontrado"
            return {"message": mensagem_erro}, 404
        else:
            return apresenta_item(item), 200

    except Exception as e:
        mensagem_erro = "Não foi possível buscar o item"
        print(f"Erro ao buscar item: {str(e)}")
        return {"message": mensagem_erro}, 400


@app.get('/item/catalogo', tags=[item_tag], responses={"200": ItemCatalogoSchema, "404": ErrorSchema})
def get_itens_habilitados():
    """Lista os itens disponíveis para compra
    Retorna apenas os itens habilitados pelo Gerenciar Catálogo.
    """
    try:
        sessao = Session()

        # Consulta apenas os itens habilitados
        itens_habilitados = sessao.query(
            Item).filter(Item.status == True).all()

        if not itens_habilitados:
            return {"message": "Nenhum item disponível no catálogo"}, 404
        else:
            return {"itens": [apresenta_item(item) for item in itens_habilitados]}, 200

    except Exception as e:
        mensagem_erro = "Não foi possível listar os itens"
        print(f"Erro ao listar itens: {str(e)}")
        return {"message": mensagem_erro}, 400


@app.delete('/item/deletar', tags=[item_tag], responses={"200": ItemDelSchema, "404": ErrorSchema})
def del_produto():
    """Deleta um Item a partir do id informado

    Remove o item da base de dados. Em caso de sucesso retorna uma mensagem de confirmação da remoção, em caso de falha retorna um feedback negativo.
    """
    try:
        # Obtenha o valor do item_id a partir da query string
        item_id = request.args.get('item_id', type=int)
        if item_id is None:
            return {"message": "Parâmetro 'item_id' ausente ou inválido"}, 400

        sessao = Session()

        # Buscar o item pelo ID
        item = sessao.query(Item).filter(Item.id == item_id).first()

        if item:
            if item.imagem:
                # Verifique se há uma imagem associada ao item
                # Se houver, exclua a pasta ou o arquivo de imagem
                if os.path.exists(item.imagem):
                    os.remove(item.imagem)

            # Continue com a exclusão do item no banco de dados
            sessao.delete(item)
            sessao.commit()

            return {"message": "Item removido do catálogo", "id": item_id}
        else:
            # Se o item não foi encontrado
            return {"message": "Item não encontrado"}, 404
    except Exception as e:
        sessao.rollback()
        mensagem_erro = "Erro ao excluir o item"
        print(f"Erro ao excluir item: {str(e)}")
        return {"message": mensagem_erro}, 500


@app.put('/item/editar', tags=[item_tag], responses={"200": ItemViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def editar_item(form: EditarItemSchema):
    """Edita um item existente

        Edita um item da base de dados. Em caso de sucesso retorna uma mensagem de confirmação da edição.
    """
    try:
        # Obtenha o item_id do formulário
        print(form.item_id)
        item_id = form.item_id
        sessao = Session()
        item = sessao.query(Item).filter(Item.id == item_id).first()

        if not item:
            mensagem_erro = "Item não encontrado"
            return {"message": mensagem_erro}, 404
        else:
            # Atualize os campos do item com os valores fornecidos no formulário
            item.nome = form.nome
            item.descricao = form.descricao
            item.quantidade = form.quantidade
            item.valor = form.valor
            item.peso = form.peso
            item.status = form.status

            print(form.status)

            if 'imagem' in request.files:
                imagem = request.files['imagem']

                if imagem.filename != '':
                    item.imagem = salvar_arquivo_unico(
                        UPLOAD_FOLDER, secure_filename(imagem.filename))
                    imagem.save(os.path.join(UPLOAD_FOLDER, item.imagem))

            sessao.commit()
            return apresenta_item(item), 200
    except Exception as e:
        sessao.rollback()
        mensagem_erro = "Não foi possível editar o item"
        print(f"Erro ao editar item: {str(e)}")
        return {"message": mensagem_erro}, 400


@app.route('/uploads/<path:filename>')
def serve_static(filename):
    return send_from_directory('uploads', filename)


def extensao_permitida(arquivo):
    return '.' in arquivo and arquivo.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def salvar_arquivo_unico(upload_folder, arquivo):
    # Verifique se o arquivo já existe no diretório de upload
    if not os.path.exists(os.path.join(upload_folder, arquivo)):
        return arquivo  # O arquivo não existe, portanto, é único

    # Separe o nome do arquivo e a extensão
    nome, extensao = os.path.splitext(arquivo)

    contar = 1

    # Gere um nome de arquivo único com um sufixo numérico
    while True:
        arquivo_unico = f"{nome}_{contar}{extensao}"
        caminho_arquivo = os.path.join(upload_folder, arquivo_unico)

        if not os.path.exists(caminho_arquivo):
            return arquivo_unico  # Nome único encontrado

        contar += 1

# Rotas para o Carrinho de Compras


carrinho = []

catalogo_itens = []


@app.post('/carrinho/adicionar', tags=[carrinho_tag], responses={"200": SuccessSchema, "400": ErrorSchema})
def adicionar_item_ao_carrinho():
    try:
        data = request.get_json()
        if 'item_id' not in data or 'quantidade' not in data:
            return {"message": "Campos 'item_id' e 'quantidade' são obrigatórios"}, 400

        item_id = data['item_id']
        quantidade = data['quantidade']

        if not verificar_disponibilidade_item(item_id, quantidade):
            return {"message": "Item não disponível ou quantidade insuficiente"}, 400

        item_no_carrinho = {
            "item_id": item_id,
            "quantidade": quantidade
        }

        carrinho.append(item_no_carrinho)

        return {"message": "Item adicionado ao carrinho com sucesso"}, 200

    except Exception as e:
        mensagem_erro = "Não foi possível adicionar o item ao carrinho"
        print(f"Erro ao adicionar item ao carrinho: {str(e)}")
        return {"message": mensagem_erro}, 400


def verificar_disponibilidade_item(item_id, quantidade_desejada):
    try:

        sessao = Session()
        item = sessao.query(Item).filter(Item.id == item_id).first()

        if not item:
            return False

        if quantidade_desejada > 0 and quantidade_desejada <= item.quantidade:
            return True

        return False

    except Exception as e:
        print(f"Erro ao verificar disponibilidade do item: {str(e)}")
        return False


@app.delete('/carrinho/remover/<int:item_id>', tags=[carrinho_tag], responses={"200": SuccessSchema, "404": ErrorSchema})
def remover_item_do_carrinho():
    """Remover um item do carrinho de compras pelo ID."""
    try:
        data = request.get_json()
        item_id = data.get('item_id')

        if item_id is None:
            return jsonify({"message": "Parâmetro 'item_id' ausente no corpo da solicitação"}), 400

        # Verifique se o item existe no carrinho
        item_removido = None
        for item in carrinho:
            if item.get('id') == item_id:
                item_removido = item
                carrinho.remove(item)
                break

        if item_removido:
            return jsonify({"message": "Item removido do carrinho com sucesso"}), 200
        else:
            return jsonify({"message": "Item não encontrado no carrinho"}), 404

    except Exception as e:
        mensagem_erro = "Não foi possível remover o item do carrinho"
        print(f"Erro ao remover item do carrinho: {str(e)}")
        return jsonify({"message": mensagem_erro}), 500


@app.get('/carrinho/listar', tags=[carrinho_tag], responses={"200": ListagemCarrinhoSchema})
def listar_itens_do_carrinho():
    """Listar os itens no carrinho de compras."""
    try:
        carrinho_com_nomes = []

        for item_no_carrinho in carrinho:
            item_id = item_no_carrinho["item_id"]
            quantidade = item_no_carrinho["quantidade"]

            sessao = Session()
            item = sessao.query(Item).filter(
                Item.id == item_id).first()

            if item:
                # Adicione o nome do item ao objeto no carrinho
                item_no_carrinho_com_nome = {
                    "item_id": item.id,
                    "nome": item.nome,
                    "valor": item.valor,
                    "quantidade": quantidade
                }
                carrinho_com_nomes.append(item_no_carrinho_com_nome)

        return jsonify(carrinho_com_nomes), 200

    except Exception as e:
        mensagem_erro = "Não foi possível listar os itens no carrinho"
        print(f"Erro ao listar itens no carrinho: {str(e)}")
        return jsonify({"message": mensagem_erro}), 500


def verificar_recaptcha(secret_key, response):
    base_url = "https://www.google.com/recaptcha/api/siteverify"
    url = f"{base_url}?secret={secret_key}&response={response}"

    response = requests.post(url)
    result = response.json()

    return result.get("success", False)


@app.route('/carrinho/validacao', methods=['POST'])
def processar_formulario():
    recaptcha_secret_key = "6Lf3xVMoAAAAAE5qbMfhftjpzr4a0Q9PoELxAGfL"
    recaptcha_response = request.form.get('recaptchaResponse')

    if verificar_recaptcha(recaptcha_secret_key, recaptcha_response):
        return jsonify({"success": True, "message": "Formulário enviado com sucesso!"}), 200
    else:
        return jsonify({"success": False, "message": "Erro: reCAPTCHA não verificado."}), 400
