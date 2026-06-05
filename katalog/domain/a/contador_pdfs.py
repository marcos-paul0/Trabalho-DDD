import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entry_caminho.delete(0, tk.END)
        entry_caminho.insert(0, pasta)


def contar_pdfs():
    caminho_principal = entry_caminho.get().strip()

    if not os.path.isdir(caminho_principal):
        messagebox.showerror("Erro", "Selecione uma pasta válida.")
        return

    txt_log.delete(1.0, tk.END)

    arquivo_saida = os.path.join(
        caminho_principal,
        "contagem_pdfs.txt"
    )

    total_geral = 0
    resultado = []

    try:
        pastas = sorted(os.listdir(caminho_principal))

        for pasta in pastas:
            caminho_pasta = os.path.join(caminho_principal, pasta)

            if not os.path.isdir(caminho_pasta):
                continue

            contador = 0

            for raiz, _, arquivos in os.walk(caminho_pasta):
                contador += sum(
                    1 for arquivo in arquivos
                    if arquivo.lower().endswith(".pdf")
                )

            total_geral += contador

            linha = f"{pasta}: {contador} PDFs"
            resultado.append(linha)

            txt_log.insert(tk.END, linha + "\n")
            txt_log.see(tk.END)
            janela.update()

        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("RELATÓRIO DE CONTAGEM DE PDFs\n")
            f.write("=" * 50 + "\n\n")

            for linha in resultado:
                f.write(linha + "\n")

            f.write("\n" + "=" * 50 + "\n")
            f.write(f"TOTAL GERAL: {total_geral} PDFs\n")
            f.write("=" * 50 + "\n")

        txt_log.insert(
            tk.END,
            f"\n\nRelatório salvo em:\n{arquivo_saida}"
        )

        messagebox.showinfo(
            "Concluído",
            f"Contagem finalizada!\n\nTotal de PDFs: {total_geral}"
        )

    except Exception as e:
        messagebox.showerror("Erro", str(e))


# Interface
janela = tk.Tk()
janela.title("Contador de PDFs")
janela.geometry("700x500")
janela.resizable(True, True)

frame_topo = tk.Frame(janela)
frame_topo.pack(fill="x", padx=10, pady=10)

tk.Label(
    frame_topo,
    text="Caminho da pasta:"
).pack(anchor="w")

entry_caminho = tk.Entry(frame_topo)
entry_caminho.pack(side="left", fill="x", expand=True, padx=(0, 5))

btn_buscar = tk.Button(
    frame_topo,
    text="Procurar",
    command=selecionar_pasta
)
btn_buscar.pack(side="left")

btn_contar = tk.Button(
    janela,
    text="Contar PDFs",
    command=contar_pdfs,
    height=2
)
btn_contar.pack(fill="x", padx=10)

txt_log = scrolledtext.ScrolledText(
    janela,
    wrap=tk.WORD
)
txt_log.pack(fill="both", expand=True, padx=10, pady=10)

janela.mainloop()