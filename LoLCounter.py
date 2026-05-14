import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# --- Configurações de Tema ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LoLCounterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LoLCounter - Powered by Mobalytics")
        self.geometry("900x450") # Aumentei um pouco a altura para caber mais champs

        # Dados Iniciais
        self.todos_campeoes = self.obter_lista_campeoes()
        
        # --- Layout Principal ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Barra Lateral (Seleção e Busca)
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_busca = ctk.CTkLabel(self.sidebar, text="Buscar Campeão:", font=("Arial", 16, "bold"))
        self.lbl_busca.pack(pady=(20, 5), padx=10)

        self.entry_busca = ctk.CTkEntry(self.sidebar, placeholder_text="Ex: Elise...")
        self.entry_busca.pack(pady=5, padx=10, fill="x")
        self.entry_busca.bind("<KeyRelease>", self.filtrar_campeoes)

        self.listbox_champs = ctk.CTkOptionMenu(self.sidebar, values=self.todos_campeoes)
        self.listbox_champs.pack(pady=10, padx=10, fill="x")
        self.listbox_champs.set("Ashe")

        self.btn_analisar = ctk.CTkButton(self.sidebar, text="Analisar Matchups", command=self.atualizar_interface)
        self.btn_analisar.pack(pady=20, padx=10, fill="x")

        # Painel de Conteúdo (Direita)
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.lbl_status = ctk.CTkLabel(self.content_frame, text="Selecione um campeão e clique em Analisar", font=("Arial", 14))
        self.lbl_status.pack(pady=10)

        # Containers de Matchups (Lado a Lado)
        self.matchup_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.matchup_container.pack(fill="both", expand=True)

        self.frame_best = ctk.CTkScrollableFrame(self.matchup_container, label_text="Fortes Contra (Best Picks)", label_fg_color="#1a5f7a")
        self.frame_best.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.frame_worst = ctk.CTkScrollableFrame(self.matchup_container, label_text="Fracos Contra (Worst Picks)", label_fg_color="#7a1a1a")
        self.frame_worst.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    def obter_lista_campeoes(self):
        """Puxa a lista oficial da Riot."""
        try:
            url = "https://ddragon.leagueoflegends.com/cdn/14.9.1/data/pt_BR/champion.json"
            res = requests.get(url).json()
            return sorted(list(res['data'].keys()))
        except:
            return ["Aatrox", "Ahri", "Elise", "Garen", "Lux", "Zac"]

    def filtrar_campeoes(self, event):
        termo = self.entry_busca.get().lower()
        filtrados = [c for c in self.todos_campeoes if termo in c.lower()]
        if filtrados:
            self.listbox_champs.configure(values=filtrados)
            self.listbox_champs.set(filtrados[0])

    def buscar_no_mobalytics(self, campeao):
        nome_url = campeao.lower().replace(" ", "").replace("'", "").replace(".", "")
        headers = {"User-Agent": "Mozilla/5.0"}
    
        def scrap_completo(url_alvo):
            try:
                res = requests.get(url_alvo, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                # Busca todos os links de confronto
                links = soup.find_all('a', href=lambda x: x and '/vs-' in x)
                
                dados = []
                for link in links:
                    img = link.find('img')
                    wr = link.find('span', style=lambda s: s and 'color' in s)
                    
                    if img and wr:
                        nome = img.get('alt')
                        if nome not in [d['nome'] for d in dados]:
                            dados.append({
                                "nome": nome,
                                "wr": wr.text,
                                "img_url": img.get('src')
                            })
                return dados
            except: 
                return []

        url_base = f"https://mobalytics.gg/lol/champions/{nome_url}/counters"
        # Agora busca as listas completas de ambos os lados
        return scrap_completo(url_base), scrap_completo(url_base + "?wp=t")

    def criar_card(self, pai, info, cor_texto):
        card = ctk.CTkFrame(pai)
        card.pack(fill="x", pady=5, padx=5)

        try:
            img_res = requests.get(info['img_url'])
            img_data = Image.open(BytesIO(img_res.content))
            ctk_img = ctk.CTkImage(img_data, size=(40, 40))
            ctk.CTkLabel(card, image=ctk_img, text="").pack(side="left", padx=10)
        except: pass

        label_nome = ctk.CTkLabel(card, text=info['nome'], font=("Arial", 12, "bold"))
        label_nome.pack(side="left", padx=5)

        label_wr = ctk.CTkLabel(card, text=info['wr'], font=("Arial", 12), text_color=cor_texto)
        label_wr.pack(side="right", padx=15)

    def atualizar_interface(self):
        target = self.listbox_champs.get()
        self.lbl_status.configure(text=f"Analisando {target} no Mobalytics...")
        
        for f in [self.frame_best, self.frame_worst]:
            for w in f.winfo_children(): w.destroy()
        
        self.update()
        best, worst = self.buscar_no_mobalytics(target)

        if best:
            for b in best: self.criar_card(self.frame_best, b, "#3498db")
        if worst:
            for w in worst: self.criar_card(self.frame_worst, w, "#e74c3c")

        self.lbl_status.configure(text=f"Resultados para {target}")

if __name__ == "__main__":
    app = LoLCounterApp()
    app.mainloop()