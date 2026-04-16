"""
QUELLNODIGITAL OS — Notion Hub Visual
Cria uma página de navegação estilo gallery com cards dark + título branco.

Uso:
  export NOTION_TOKEN="secret_..."
  python scripts/notion_hub.py
"""

import os
import sys
import time
import requests

TOKEN = os.environ.get("NOTION_TOKEN", "")
PARENT_PAGE_ID = "3447c584d596803aa34ae1bc038de21f"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
BASE_URL = "https://api.notion.com/v1"

# ─── SEÇÕES DO HUB ───────────────────────────────────────────────────────────
# Cover: fotos dark via Unsplash direto (sem API key necessária)

SECTIONS = [
    {
        "name": "DASHBOARD",
        "emoji": "🧠",
        "desc": "Painel de controle diário",
        "cover": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&q=80&auto=format&fit=crop",
        "color": "gray",
    },
    {
        "name": "CONTEÚDO",
        "emoji": "📝",
        "desc": "Pipeline de produção",
        "cover": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1200&q=80&auto=format&fit=crop",
        "color": "brown",
    },
    {
        "name": "CALENDÁRIO",
        "emoji": "📅",
        "desc": "Agenda editorial",
        "cover": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=1200&q=80&auto=format&fit=crop",
        "color": "blue",
    },
    {
        "name": "IDEIAS",
        "emoji": "💡",
        "desc": "Backlog de ideias",
        "cover": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&q=80&auto=format&fit=crop",
        "color": "yellow",
    },
    {
        "name": "ANÁLISE",
        "emoji": "📊",
        "desc": "Métricas e resultados",
        "cover": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&q=80&auto=format&fit=crop",
        "color": "green",
    },
    {
        "name": "PROCESSOS",
        "emoji": "⚙️",
        "desc": "SOPs operacionais",
        "cover": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&q=80&auto=format&fit=crop",
        "color": "orange",
    },
    {
        "name": "AGENTES IA",
        "emoji": "🤖",
        "desc": "Prompts e agentes",
        "cover": "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=1200&q=80&auto=format&fit=crop",
        "color": "purple",
    },
    {
        "name": "REFERÊNCIAS",
        "emoji": "📚",
        "desc": "Base estratégica",
        "cover": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1200&q=80&auto=format&fit=crop",
        "color": "red",
    },
    {
        "name": "FLUX",
        "emoji": "⚡",
        "desc": "Sistema e produto",
        "cover": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&q=80&auto=format&fit=crop",
        "color": "pink",
    },
    {
        "name": "CLIENTES",
        "emoji": "🤝",
        "desc": "Gestão de serviço",
        "cover": "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?w=1200&q=80&auto=format&fit=crop",
        "color": "default",
    },
]

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def heading(text, level=2):
    tag = f"heading_{level}"
    return {"object": "block", "type": tag,
            tag: {"rich_text": [{"text": {"content": text},
                                 "annotations": {"bold": True, "color": "default"}}]}}

def paragraph(text):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": text}}]}}

def callout(text, emoji="💡"):
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": [{"text": {"content": text}}],
                        "icon": {"emoji": emoji}}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

# ─── CRIAR HUB DATABASE ──────────────────────────────────────────────────────

def create_hub_database():
    """Cria o database hub com propriedades para gallery view."""
    payload = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"emoji": "🗂️"},
        "title": [{"text": {"content": "QUELLNODIGITAL OS"}}],
        "description": [{"text": {"content": "Sistema operacional da marca — navegar via Gallery view"}}],
        "properties": {
            "Nome": {"title": {}},
            "Descrição": {"rich_text": {}},
            "Categoria": {"select": {"options": [
                {"name": "Conteúdo", "color": "blue"},
                {"name": "Estratégia", "color": "purple"},
                {"name": "Operação", "color": "orange"},
                {"name": "IA", "color": "green"},
                {"name": "Produto", "color": "pink"},
            ]}},
        },
    }
    r = requests.post(f"{BASE_URL}/databases", headers=HEADERS, json=payload)
    if r.status_code not in (200, 201):
        print(f"✗ Erro ao criar hub: {r.status_code} — {r.text[:300]}")
        return None
    db_id = r.json()["id"]
    print(f"✓ Hub database criado: QUELLNODIGITAL OS")
    return db_id


def categoria(name):
    cats = {
        "DASHBOARD": "Estratégia",
        "CONTEÚDO": "Conteúdo",
        "CALENDÁRIO": "Conteúdo",
        "IDEIAS": "Conteúdo",
        "ANÁLISE": "Operação",
        "PROCESSOS": "Operação",
        "AGENTES IA": "IA",
        "REFERÊNCIAS": "Estratégia",
        "FLUX": "Produto",
        "CLIENTES": "Produto",
    }
    return cats.get(name, "Operação")


def conteudo_da_secao(name):
    """Retorna blocos de conteúdo específico por seção."""
    base = {
        "DASHBOARD": [
            callout("Centro de comando diário da operação @quellnodigital", "🧠"),
            divider(),
            heading("Conteúdos da Semana"),
            paragraph("→ Ver database Conteúdo filtrado por esta semana"),
            divider(),
            heading("Fluxo Operacional"),
            {"object": "block", "type": "code", "code": {
                "rich_text": [{"text": {"content":
                    "IDEIA → ROTEIRO → PRODUÇÃO → POSTADO → ANÁLISE → REAPROVEITAMENTO"
                }}], "language": "plain text"
            }},
        ],
        "CONTEÚDO": [
            callout("Aqui acontece tudo. Cada linha é um conteúdo com ciclo completo.", "📝"),
            divider(),
            heading("Propriedades"),
            paragraph("Status / Pilar / Formato / Objetivo / Data / Hook / CTA / Score"),
            divider(),
            heading("Regra"),
            paragraph("Nenhum conteúdo é usado apenas uma vez."),
            paragraph("1 post → 1 reel + 3 stories + 1 LinkedIn"),
        ],
        "CALENDÁRIO": [
            callout("Não é só agenda — é controle de consistência.", "📅"),
            divider(),
            heading("Cadência Semanal"),
            paragraph("Segunda → Carrossel | Sistema vs improviso"),
            paragraph("Quarta → Reel | IA na prática"),
            paragraph("Quinta → Carrossel | Autoridade"),
            paragraph("Sexta → Stories | Bastidor"),
            paragraph("Sábado → Reel | Alcance"),
        ],
        "IDEIAS": [
            callout("Registrar tudo. Filtrar depois. Nenhuma ideia boa morre no WhatsApp.", "💡"),
            divider(),
            heading("Prompt para abastecer com IA"),
            {"object": "block", "type": "code", "code": {
                "rich_text": [{"text": {"content":
                    "Crie 10 ideias de conteúdo com base em dores reais do meu público.\n\n"
                    "Para cada ideia:\n- Tema\n- Dor central\n- Pilar\n- Potencial de viralização"
                }}], "language": "plain text"
            }},
        ],
        "ANÁLISE": [
            callout("Aqui você para de criar conteúdo e começa a gerir conteúdo.", "📊"),
            divider(),
            heading("O que analisar semanalmente"),
            paragraph("• Qual pilar gera mais salvamentos?"),
            paragraph("• Qual formato cresce mais?"),
            paragraph("• Quais hooks funcionam?"),
            divider(),
            heading("Ritual — todo domingo"),
            paragraph("Preencher métricas → Rodar prompt → Registrar aprendizado → Planejar semana"),
        ],
        "PROCESSOS": [
            callout("Isso transforma você em gestora da operação, não executora.", "⚙️"),
            divider(),
            heading("SOPs disponíveis"),
            paragraph("1. Criação de conteúdo — 6 passos"),
            paragraph("2. Roteirização"),
            paragraph("3. Postagem"),
            paragraph("4. Reaproveitamento"),
            paragraph("5. Análise semanal"),
        ],
        "AGENTES IA": [
            callout("Você NÃO usa IA solta. Você usa agentes com função definida.", "🤖"),
            divider(),
            heading("Agentes disponíveis"),
            paragraph("• Ideator — gera ideias"),
            paragraph("• Copywriter — transforma em post"),
            paragraph("• Analista — melhora e pontua"),
            paragraph("• Estrategista — decide o que postar"),
            divider(),
            heading("Como usar"),
            paragraph("Abrir o prompt da pasta /agents + colar no Claude ou ChatGPT"),
        ],
        "REFERÊNCIAS": [
            callout("Base estratégica — o que alimenta o sistema.", "📚"),
            divider(),
            heading("Base bibliográfica"),
            paragraph("Rápido e Devagar · A Única Coisa · Ego é seu inimigo · Carnegie · Diário do CEO"),
            divider(),
            heading("Frase central"),
            {"object": "block", "type": "quote", "quote": {
                "rich_text": [{"text": {"content": "Conteúdo não é criatividade. É sistema."}}]
            }},
        ],
        "FLUX": [
            callout("Sistema de conteúdo baseado em estratégia, IA e processos.", "⚡"),
            divider(),
            heading("Objetivo"),
            paragraph("Gerar resultado sem depender de criatividade constante."),
            divider(),
            heading("Fluxo"),
            {"object": "block", "type": "code", "code": {
                "rich_text": [{"text": {"content":
                    "IDEIA → ROTEIRO → PRODUÇÃO → POST → REAPROVEITAMENTO"
                }}], "language": "plain text"
            }},
        ],
        "CLIENTES": [
            callout("Para quando o @quellnodigital virar serviço para terceiros.", "🤝"),
            divider(),
            heading("Entregas semanais"),
            paragraph("3 posts prontos · 3 roteiros de reels · 10 ideias · 1 relatório"),
            divider(),
            heading("Fluxo de aprovação"),
            {"object": "block", "type": "code", "code": {
                "rich_text": [{"text": {"content":
                    "Criação → Revisão → Ajuste → Aprovado → Produção → Entrega"
                }}], "language": "plain text"
            }},
        ],
    }
    return base.get(name, [paragraph(f"Seção: {name}")])


def create_section_page(db_id, section):
    """Cria uma página dentro do hub database com cover dark."""
    name = section["name"]
    payload = {
        "parent": {"database_id": db_id},
        "icon": {"emoji": section["emoji"]},
        "cover": {
            "type": "external",
            "external": {"url": section["cover"]}
        },
        "properties": {
            "Nome": {"title": [{"text": {"content": name}}]},
            "Descrição": {"rich_text": [{"text": {"content": section["desc"]}}]},
            "Categoria": {"select": {"name": categoria(name)}},
        },
        "children": conteudo_da_secao(name),
    }
    r = requests.post(f"{BASE_URL}/pages", headers=HEADERS, json=payload)
    if r.status_code not in (200, 201):
        print(f"  ✗ {name}: {r.status_code} — {r.text[:150]}")
        return False
    print(f"  ✓ {section['emoji']} {name}")
    return True


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    if not TOKEN:
        print("\n❌ NOTION_TOKEN não encontrado.")
        print("   export NOTION_TOKEN='secret_...'\n")
        sys.exit(1)

    print("\n🎨 QUELLNODIGITAL OS — Criando Hub Visual...\n")

    db_id = create_hub_database()
    if not db_id:
        sys.exit(1)

    print(f"\n📄 Criando {len(SECTIONS)} seções...\n")
    ok = 0
    for section in SECTIONS:
        if create_section_page(db_id, section):
            ok += 1
        time.sleep(0.4)

    print(f"\n{'─'*50}")
    print(f"✅ {ok}/{len(SECTIONS)} seções criadas\n")
    print("📌 PRÓXIMO PASSO NO NOTION:")
    print("   1. Abrir 'QUELLNODIGITAL OS'")
    print("   2. Clicar em '+ Add a view' → Gallery")
    print("   3. Card preview → Page cover")
    print("   4. Card size → Large")
    print("   5. Propriedades → desativar tudo exceto 'Nome'\n")


if __name__ == "__main__":
    main()
