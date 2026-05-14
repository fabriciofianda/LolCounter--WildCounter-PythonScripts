# Definindo o conteúdo do README.md baseado no que foi discutido
readme_content = """# LoL & Wild Rift Counter Search

Este repositório contém dois scripts independentes em Python para consulta automatizada de *matchups* (counters e sinergias) para League of Legends (PC) e Wild Rift (Mobile). As ferramentas utilizam técnicas de web scraping para extrair dados atualizados diretamente de plataformas de referência.

## 🚀 Funcionalidades

- **LoLCounter.py**: Consulta counters e win rates para League of Legends PC via Mobalytics.
- **WildCounter.py**: Consulta counters e sinergias para Wild Rift via WildRiftFire.
- **Interface Gráfica**: Construída com `customtkinter` para uma experiência moderna e intuitiva.
- **Sincronização Dinâmica**: Lista de campeões atualizada via Riot Data Dragon (API oficial).

## 🛠️ Tecnologias

- **Python 3.x**
- **CustomTkinter**: Interface de usuário (GUI).
- **BeautifulSoup4**: Extração de dados HTML.
- **Requests**: Comunicação HTTP.
- **Pillow (PIL)**: Renderização de ícones dos campeões.

## 📦 Instalação

Clone o repositório e instale as dependências necessárias:

Code output
README.md gerado com sucesso.

```bash
pip install customtkinter requests beautifulsoup4 pillow
