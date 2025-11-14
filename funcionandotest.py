# ================================================================
#  AcadIA – Sistema Acadêmico Completo com IA + Dashboard
#  Arquivo único, interface + IA + SQLite
#  Login padrão: admin / 123
# ================================================================

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor

# ================================================================
# BANCO DE DADOS
# ================================================================

def conectar():
    return sqlite3.connect("acadIA.db")


def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            senha TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            turma TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER,
            n1 REAL,
            n2 REAL,
            n3 REAL,
            media REAL,
            FOREIGN KEY(aluno_id) REFERENCES alunos(id)
        );
    """)

    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", ("admin", "123"))
    except:
        pass

    conn.commit()
    conn.close()

# ================================================================
# FUNÇÕES DO BANCO
# ================================================================

def validar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
    dados = cursor.fetchone()
    conn.close()
    return dados is not None


def cadastrar_aluno(nome, turma):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alunos (nome, turma) VALUES (?, ?)", (nome, turma))
    conn.commit()
    conn.close()


def listar_alunos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos")
    lista = cursor.fetchall()
    conn.close()
    return lista


def salvar_notas(aluno_id, n1, n2, n3, media):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notas (aluno_id, n1, n2, n3, media) VALUES (?, ?, ?, ?, ?)",
        (aluno_id, n1, n2, n3, media)
    )
    conn.commit()
    conn.close()


def listar_notas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT alunos.nome, notas.n1, notas.n2, notas.n3, notas.media
        FROM notas
        JOIN alunos ON alunos.id = notas.aluno_id
    """)
    lista = cursor.fetchall()
    conn.close()
    return lista

# ================================================================
# IA – REGRESSÃO + REDE NEURAL
# ================================================================

def treinar_ia():
    X = np.array([
        [5,6,7],[7,8,9],[3,4,5],[9,9,10],
        [6,6,7],[8,7,6],[4,5,6],[2,3,4]
    ])
    y = np.array([6.0,8.0,4.0,9.3,6.3,7.0,5.0,3.0])

    reg = LinearRegression()
    reg.fit(X, y)

    nn = MLPRegressor(hidden_layer_sizes=(10,10), max_iter=1000)
    nn.fit(X, y)

    return reg, nn


regressor, rede_neural = treinar_ia()


def prever_media(n1, n2, n3):
    entrada = np.array([[n1, n2, n3]])
    p1 = regressor.predict(entrada)[0]
    p2 = rede_neural.predict(entrada)[0]
    return (p1 + p2) / 2

# ================================================================
# INTERFACE TKINTER
# ================================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ------------------------------- LOGIN ---------------------------

def abrir_login():

    def entrar():
        usuario = entry_user.get()
        senha = entry_senha.get()

        if validar_login(usuario, senha):
            login.destroy()
            abrir_home()
        else:
            messagebox.showerror("Erro", "Login inválido!")

    login = ctk.CTk()
    login.title("AcadIA - Login")
    login.geometry("380x350")

    ctk.CTkLabel(login, text="AcadIA - Login",
                 font=("Arial", 18, "bold")).pack(pady=20)

    entry_user = ctk.CTkEntry(login, placeholder_text="Usuário")
    entry_user.pack(pady=10)

    entry_senha = ctk.CTkEntry(login, placeholder_text="Senha", show="•")
    entry_senha.pack(pady=10)

    ctk.CTkButton(login, text="Entrar", command=entrar).pack(pady=15)

    login.mainloop()

# ------------------------------- HOME ----------------------------

def abrir_home():

    def tela_cadastro():
        home.destroy()
        abrir_tela_cadastro()

    def tela_notas():
        home.destroy()
        abrir_tela_notas()

    def tela_dash():
        home.destroy()
        abrir_dashboard()

    home = ctk.CTk()
    home.title("AcadIA - Home")
    home.geometry("450x450")

    ctk.CTkLabel(home, text="AcadIA - Início",
                 font=("Arial", 22, "bold")).pack(pady=30)

    ctk.CTkButton(home, text="Cadastrar Aluno", width=250,
                  command=tela_cadastro).pack(pady=15)

    ctk.CTkButton(home, text="Lançar Notas + IA", width=250,
                  command=tela_notas).pack(pady=15)

    ctk.CTkButton(home, text="Dashboard", width=250,
                  command=tela_dash).pack(pady=15)

    home.mainloop()

# ---------------------- TELA CADASTRO ALUNO ---------------------

def abrir_tela_cadastro():

    def salvar():
        nome = entry_nome.get()
        turma = entry_turma.get()

        if nome == "" or turma == "":
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        cadastrar_aluno(nome, turma)
        messagebox.showinfo("OK", "Aluno cadastrado!")
        entry_nome.delete(0, tk.END)
        entry_turma.delete(0, tk.END)

    tela = ctk.CTk()
    tela.title("Cadastro de Alunos")
    tela.geometry("420x380")

    ctk.CTkLabel(tela, text="Cadastrar Aluno",
                 font=("Arial", 22, "bold")).pack(pady=20)

    entry_nome = ctk.CTkEntry(tela, placeholder_text="Nome")
    entry_nome.pack(pady=10)

    entry_turma = ctk.CTkEntry(tela, placeholder_text="Turma")
    entry_turma.pack(pady=10)

    ctk.CTkButton(tela, text="Salvar", command=salvar).pack(pady=20)

    tela.mainloop()

# ---------------------- TELA DE NOTAS + IA ----------------------

def abrir_tela_notas():

    alunos = listar_alunos()

    def salvar_dados():
        try:
            aluno = combo.get()
            aluno_id = aluno.split(" - ")[0]

            n1 = float(entry1.get())
            n2 = float(entry2.get())
            n3 = float(entry3.get())

            media = prever_media(n1, n2, n3)

            salvar_notas(aluno_id, n1, n2, media)

            messagebox.showinfo(
                "OK",
                f"Notas salvas!\nMédia prevista pela IA: {media:.2f}"
            )

        except:
            messagebox.showerror("Erro", "Verifique os dados!")

    tela = ctk.CTk()
    tela.title("Lançamento de Notas")
    tela.geometry("450x420")

    lista_formatada = [f"{a[0]} - {a[1]}" for a in alunos]

    ctk.CTkLabel(tela, text="Lançar Notas",
                 font=("Arial", 22, "bold")).pack(pady=15)

    combo = ctk.CTkComboBox(tela, values=lista_formatada, width=280)
    combo.pack(pady=10)

    entry1 = ctk.CTkEntry(tela, placeholder_text="Nota 1")
    entry1.pack(pady=8)

    entry2 = ctk.CTkEntry(tela, placeholder_text="Nota 2")
    entry2.pack(pady=8)

    entry3 = ctk.CTkEntry(tela, placeholder_text="Nota 3")
    entry3.pack(pady=8)

    ctk.CTkButton(tela, text="Salvar + Calcular IA",
                  command=salvar_dados).pack(pady=15)

    tela.mainloop()

# ------------------------- DASHBOARD ----------------------------

def abrir_dashboard():

    notas = listar_notas()
    if len(notas) == 0:
        messagebox.showerror("Erro", "Nenhum dado encontrado!")
        return

    nomes = [i[0] for i in notas]
    medias = [i[4] for i in notas]

    aprovados = sum(1 for m in medias if m >= 6)
    reprovados = len(medias) - aprovados

    melhor = max(medias)
    pior = min(medias)

    dash = ctk.CTk()
    dash.title("Dashboard AcadIA")
    dash.geometry("600x550")

    ctk.CTkLabel(dash, text="Dashboard Acadêmico",
                 font=("Arial", 22, "bold")).pack(pady=15)

    frame = ctk.CTkFrame(dash)
    frame.pack(pady=15)

    ctk.CTkLabel(frame, text=f"Aprovados: {aprovados}",
                 font=("Arial", 17)).grid(row=0, column=0, padx=15)
    ctk.CTkLabel(frame, text=f"Reprovados: {reprovados}",
                 font=("Arial", 17)).grid(row=0, column=1, padx=15)
    ctk.CTkLabel(frame, text=f"Maior Média: {melhor:.2f}",
                 font=("Arial", 17)).grid(row=1, column=0, pady=10)
    ctk.CTkLabel(frame, text=f"Menor Média: {pior:.2f}",
                 font=("Arial", 17)).grid(row=1, column=1, pady=10)

    def grafico_barras():
        plt.figure(figsize=(8,4))
        plt.bar(nomes, medias)
        plt.title("Média por aluno")
        plt.xlabel("Aluno")
        plt.ylabel("Média")
        plt.show()

    def grafico_pizza():
        plt.figure(figsize=(6,6))
        plt.pie([aprovados, reprovados],
                labels=["Aprovados", "Reprovados"],
                autopct="%1.1f%%")
        plt.show()

    def grafico_linha():
        plt.plot(medias, marker="o")
        plt.title("Evolução das médias")
        plt.xlabel("Aluno")
        plt.ylabel("Média")
        plt.grid()
        plt.show()

    ctk.CTkButton(dash, text="Gráfico de Barras",
                  command=grafico_barras).pack(pady=10)
    ctk.CTkButton(dash, text="Gráfico de Pizza",
                  command=grafico_pizza).pack(pady=10)
    ctk.CTkButton(dash, text="Gráfico de Linha",
                  command=grafico_linha).pack(pady=10)

    dash.mainloop()

# ================================================================
# INICIAR SISTEMA
# ================================================================

inicializar_banco()
abrir_login()
