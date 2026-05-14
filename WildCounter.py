import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

class WildRiftAssistant(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WildRiftFire Helper - WR Edition")
        self.geometry("1000x350")

        # 1. Obtém a lista filtrada apenas com campeões do Wild Rift
        self.todos_campeoes = self.obter_lista_wild_rift()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Cabeçalho
        self.header = ctk.CTkFrame(self)
        self.header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(self.header, text="Campeão do Wild Rift:").pack(side="left", padx=5)

        # ComboBox com a lista filtrada
        self.combo_champ = ctk.CTkComboBox(self.header, values=self.todos_campeoes, width=250)
        self.combo_champ.pack(side="left", padx=10, pady=10)
        self.combo_champ.set("Norra") 
        
        self.btn = ctk.CTkButton(self.header, text="Analisar", command=self.executar_busca)
        self.btn.pack(side="left", padx=10)

        # Container de Resultados
        self.result_container = ctk.CTkFrame(self, fg_color="transparent")
        self.result_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.result_container.grid_columnconfigure((0, 1), weight=1)

        self.frame_counters = ctk.CTkScrollableFrame(self.result_container, label_text="Counters", label_fg_color="#7a1a1a")
        self.frame_counters.grid(row=0, column=0, sticky="nsew", padx=5)

        self.frame_synergies = ctk.CTkScrollableFrame(self.result_container, label_text="Sinergias", label_fg_color="#1a5f3a")
        self.frame_synergies.grid(row=0, column=1, sticky="nsew", padx=5)

    def obter_lista_wild_rift(self):
        """Puxa do DDragon e filtra para o Wild Rift."""
        try:
            # Puxa a lista global da Riot
            url = "https://ddragon.leagueoflegends.com/cdn/14.10.1/data/pt_BR/champion.json"
            res = requests.get(url, timeout=10).json()
            lista_pc = res['data'].keys()

            # Lista de exclusão: Campeões que estão no PC mas NÃO estão no Wild Rift (Exemplos)
            # Você pode atualizar essa lista conforme novos campeões saem no mobile
            nao_estao_no_wr = {
                "Anivia", "Azir", "BelVeth", "Bard", "ChoGath", "Hecarim", "Illaoi", 
                "Ivern", "Karthus", "Kassadin", "Kled", "KogMaw", "Leblanc", "Lissandra", 
                "Malzahar", "Mordekaiser", "Nidalee", "Nocturne", "Quinn", "Reksai", 
                "Rumble", "Ryze", "Skarner", "TahmKench", "Taliyah", "Taric", "Trundle", 
                "Udyr", "VelKoz", "Victor", "Viego", "Xerath", "Yorick", "Zac"
            }

            # Filtra apenas quem está no WR
            lista_filtrada = [c for c in lista_pc if c not in nao_estao_no_wr]
            return sorted(lista_filtrada)
        except:
            return ["Ashe", "Garen", "Jinx", "Lux", "Vi"]

    def executar_busca(self):
        for f in [self.frame_counters, self.frame_synergies]:
            for w in f.winfo_children(): w.destroy()
            
        nome_selecionado = self.combo_champ.get().strip()
        # Tratativa para URL: remove apóstrofos e troca espaços por hífens
        nome_url = nome_selecionado.lower().replace("'", "").replace(" ", "-")
        url = f"https://www.wildriftfire.com/guide/{nome_url}"
        
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            def processar(classe, frame, cor):
                container = soup.find("div", class_=classe)
                if container:
                    for item in container.find_all("div", class_="ico-holder"):
                        nome = item.find("span").text if item.find("span") else "???"
                        # Ignora a imagem da função e pega a do campeão
                        img_tag = item.find("img", class_="champion")
                        if img_tag:
                            img_url = img_tag.get("src")
                            if img_url.startswith("/"):
                                img_url = "https://www.wildriftfire.com" + img_url
                            self.renderizar_card(frame, nome, img_url, cor)

            processar("data-mod counters-mod counters", self.frame_counters, "#e74c3c")
            processar("data-mod counters-mod synergies", self.frame_synergies, "#2ecc71")
                
        except Exception as e:
            print(f"Erro: {e}")

    def renderizar_card(self, pai, nome, url_img, cor):
        card = ctk.CTkFrame(pai, border_width=1, border_color=cor)
        card.pack(fill="x", pady=3, padx=5)
        try:
            img_data = requests.get(url_img, timeout=5).content
            img = Image.open(BytesIO(img_data))
            photo = ctk.CTkImage(img, size=(45, 45))
            ctk.CTkLabel(card, image=photo, text="").pack(side="left", padx=10, pady=5)
        except: pass
        ctk.CTkLabel(card, text=nome, font=("Arial", 12, "bold")).pack(side="left")

if __name__ == "__main__":
    app = WildRiftAssistant()
    app.mainloop()