import streamlit as st  # Adicionando a importação do streamlit
import pandas as pd
from datetime import datetime
import logging
import os

# Configuração do Log
logging.basicConfig(filename="empresa_log.txt", level=logging.INFO, 
                    format="%(asctime)s - %(message)s")

# Função para registrar eventos no log
def registrar_log(mensagem):
    logging.info(mensagem)

# Função para criar o arquivo Excel vazio se ele não existir
def criar_arquivo_vazio():
    # Definir as colunas padrão
    colunas = ["Cliente", "Endereço de Coleta", "Data de Coleta", "Status", "Empresa"]
    # Criar um DataFrame vazio com essas colunas
    df_vazio = pd.DataFrame(columns=colunas)
    # Salvar o DataFrame vazio no arquivo Excel
    df_vazio.to_excel("dados_coletas.xlsx", index=False)

# Verificar se o arquivo Excel existe, se não, criar um
if not os.path.exists("dados_coletas.xlsx"):
    criar_arquivo_vazio()

# Configuração do Tema Dark
st.set_page_config(page_title="Sistema de Coletas", page_icon=":truck:", layout="centered", initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho do App
st.title("Sistema de Coletas")

# Tentar carregar a imagem do logo
try:
    logo_path = "image.png"  # Defina o caminho correto do logo
    st.image(logo_path, width=200)
except FileNotFoundError:
    st.error("O arquivo de logo não foi encontrado. Você pode carregar o logo manualmente.")
    logo_file = st.file_uploader("Escolha o logo da empresa", type=["png", "jpg", "jpeg"])
    if logo_file is not None:
        st.image(logo_file, width=200)

# Exibição do log atual
st.header("")
try:
    with open("empresa_log.txt", "r") as file:
        log_data = file.read()
    st.text_area("Eventos Registrados", value=log_data, height=300, max_chars=None)
except FileNotFoundError:
    st.text("O arquivo de log ainda não foi criado.")

# Seleção da empresa (Jadlog ou Terceirizada)
st.header("Cadastro de Coleta")
empresa_selecionada = st.selectbox("Escolha a Empresa", ["Jadlog", "Empresa Terceirizada"])

# Cadastro de Motorista
st.header("Cadastro de Motorista")
motorista_nome = st.text_input("Nome do Motorista")
motorista_placa = st.text_input("Placa do Veículo")
motorista_modelo = st.selectbox(
    "Modelo do Veículo",
    ["Fiorino", "Truck", "Toco", "Carreta", "Van", "Delivery", "3/4", "HR"]
)
motorista_contato = st.text_input("Contato")
motorista_rg = st.text_input("RG do Motorista")
motorista_cpf = st.text_input("CPF do Motorista")

# Cadastro de Ajudante
st.header("Cadastro de Ajudante")
ajudante_nome = st.text_input("Nome do Ajudante")
ajudante_contato = st.text_input("Contato do Ajudante")
ajudante_rg = st.text_input("RG do Ajudante")
ajudante_cpf = st.text_input("CPF do Ajudante")

# Função para excluir motorista
def excluir_motorista(nome, placa):
    try:
        df = pd.read_excel("dados_coletas.xlsx")
        df = df[df["Motorista"] != nome]  # Exclui a linha com o nome do motorista
        df = df[df["Placa"] != placa]    # Exclui a linha com a placa do motorista
        df.to_excel("dados_coletas.xlsx", index=False)
        st.success(f"Motorista {nome} com a placa {placa} excluído com sucesso!")
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado.")

# Ação para verificar se o motorista já existe e excluir
if st.button("Excluir Motorista"):
    if motorista_nome and motorista_placa:
        excluir_motorista(motorista_nome, motorista_placa)

# Ação de salvar motorista
if st.button("Salvar Motorista"):
    if motorista_nome and motorista_placa and motorista_modelo and motorista_contato and motorista_rg and motorista_cpf:
        # Registrar no log
        registrar_log(f"Motorista {motorista_nome} ({motorista_placa}) cadastrado na empresa {empresa_selecionada}. Modelo: {motorista_modelo}")
        st.success(f"Motorista {motorista_nome} cadastrado com sucesso!")
        
        # Adicionar dados ao arquivo Excel
        dados_motorista = {
            "Motorista": [motorista_nome],
            "Placa": [motorista_placa],
            "Modelo": [motorista_modelo],
            "Contato": [motorista_contato],
            "RG": [motorista_rg],
            "CPF": [motorista_cpf],
            "Empresa": [empresa_selecionada]
        }
        df_motorista = pd.DataFrame(dados_motorista)
        
        # Salvar os dados no Excel, criando ou atualizando o arquivo
        try:
            df_existente = pd.read_excel("dados_coletas.xlsx")
            df_atualizado = pd.concat([df_existente, df_motorista], ignore_index=True)
            df_atualizado.to_excel("dados_coletas.xlsx", index=False)
        except FileNotFoundError:
            df_motorista.to_excel("dados_coletas.xlsx", index=False)

# Ação de salvar ajudante
if st.button("Salvar Ajudante"):
    if ajudante_nome and ajudante_contato and ajudante_rg and ajudante_cpf:
        # Registrar no log
        registrar_log(f"Ajudante {ajudante_nome} cadastrado com sucesso para a empresa {empresa_selecionada}.")
        st.success(f"Ajudante {ajudante_nome} cadastrado com sucesso!")
        
        # Adicionar dados ao arquivo Excel
        dados_ajudante = {
            "Ajudante": [ajudante_nome],
            "Contato do Ajudante": [ajudante_contato],
            "RG": [ajudante_rg],
            "CPF": [ajudante_cpf],
            "Empresa": [empresa_selecionada]
        }
        df_ajudante = pd.DataFrame(dados_ajudante)
        
        # Salvar os dados no Excel, criando ou atualizando o arquivo
        try:
            df_existente = pd.read_excel("dados_coletas.xlsx")
            df_atualizado = pd.concat([df_existente, df_ajudante], ignore_index=True)
            df_atualizado.to_excel("dados_coletas.xlsx", index=False)
        except FileNotFoundError:
            df_ajudante.to_excel("dados_coletas.xlsx", index=False)

# Cadastro de Coleta
cliente_nome = st.text_input("Nome do Cliente")
endereco_coleta = st.text_input("Endereço de Coleta")
data_coleta = st.date_input("Data da Coleta", min_value=datetime.today())
status_coleta = st.selectbox("Status da Coleta", ["Pendente", "Andamento", "Concluída", "Improdutiva"])

# Ação de salvar coleta
if st.button("Salvar Coleta"):
    if cliente_nome and endereco_coleta and data_coleta and status_coleta:
        # Registrar no log
        registrar_log(f"Coleta para o cliente {cliente_nome} cadastrada em {endereco_coleta} para o dia {data_coleta} com status {status_coleta} pela empresa {empresa_selecionada}.")
        st.success(f"Coleta para o cliente {cliente_nome} cadastrada com sucesso!")
        
        # Adicionar dados ao arquivo Excel
        dados_coleta = {
            "Cliente": [cliente_nome],
            "Endereço de Coleta": [endereco_coleta],
            "Data de Coleta": [data_coleta],
            "Status": [status_coleta],
            "Empresa": [empresa_selecionada]
        }
        df_coleta = pd.DataFrame(dados_coleta)
        
        # Salvar os dados no Excel, criando ou atualizando o arquivo
        try:
            df_existente = pd.read_excel("dados_coletas.xlsx")
            df_atualizado = pd.concat([df_existente, df_coleta], ignore_index=True)
            df_atualizado.to_excel("dados_coletas.xlsx", index=False)
        except FileNotFoundError:
            df_coleta.to_excel("dados_coletas.xlsx", index=False)

# Gerar relatório Excel
if st.button("Gerar Relatório Excel"):
    try:
        df = pd.read_excel("dados_coletas.xlsx")
        st.write(df)
        st.download_button(
            label="Baixar Relatório Excel",
            data=open("dados_coletas.xlsx", "rb").read(),
            file_name="dados_coletas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except FileNotFoundError:
        st.error("Nenhum dado foi salvo ainda.")
