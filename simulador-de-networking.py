from playwright.sync_api import sync_playwright
import random

# Lista de usuários de teste
usuarios = ["Carlos", "Ana", "João"]

# Templates de mensagens simuladas
templates = [
    "Olá {}, prazer em te conhecer!",
    "Oi {}, tudo bem? Prazer em falar contigo!",
    "Olá {}, espero que esteja tendo um ótimo dia!"
]

def gerar_mensagem(nome):
    """Gera mensagem simulada para portfólio"""
    return random.choice(templates).format(nome)

def padronizar_id(nome):
    """Remove acentos e transforma em minúsculas para usar como ID"""
    return nome.lower().replace("ã", "a").replace("á", "a") \
               .replace("é", "e").replace("ó", "o") \
               .replace("ô", "o").replace("ç", "c")

with sync_playwright() as pw:
    navegador = pw.chromium.launch(headless=False)  # navegador visível
    context = navegador.new_context()  # sem login real
    page = context.new_page()
    
    # Abrir página de teste
    page.goto("http://127.0.0.1:5500/teste.html")

    for usuario in usuarios:
        # Padroniza o nome do usuário para bater com o ID do HTML
        usuario_id = padronizar_id(usuario)

        # Gera a mensagem simulada
        msg = gerar_mensagem(usuario)
        print(f"Mensagem para {usuario}: {msg}")

        # Espera até o campo existir
        page.wait_for_selector(f"#mensagem-{usuario_id}", timeout=5000)
        
        # Preenche campo e clica no botão
        page.fill(f"#mensagem-{usuario_id}", msg)
        page.click(f"#enviar-{usuario_id}")

    # Fecha o navegador ao final
    navegador.close()
