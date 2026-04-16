"""
QUELLNODIGITAL OS — Cria databases para todas as seções
Substitui as páginas simples por databases com estrutura completa.

Uso:
  export NOTION_TOKEN="secret_..."
  python scripts/notion_databases.py
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
COVER_URL = "https://placehold.co/1600x400/8ea690/8ea690.png"

# IDs das páginas existentes (para deletar após criar os databases)
EXISTING_PAGES = {
    "Dashboard":            "3447c584d5968152a103ef8487e5e647",
    "Calendário Editorial": "3447c584d59681a99dc8f06ef277f30b",
    "Processos":            "3447c584d5968178a970c3977b49639c",
    "Referências":          "3447c584d59681a193b7e6289d745a89",
    "Clientes":             "3447c584d59681dda3c2de11ad9e07fa",
}

# IDs dos databases já existentes (só atualizar)
EXISTING_DATABASES = {
    "Conteúdo": "3447c584d596817aaa14f6ebbb789faa",
    "Ideias":   "3447c584d59681e89f28f70491c5ba42",
    "Análise":  "3447c584d59681969c61e60442defc40",
}


def create_database(title, emoji, properties, description=""):
    payload = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"emoji": emoji},
        "cover": {"type": "external", "external": {"url": COVER_URL}},
        "title": [{"text": {"content": title}}],
        "properties": properties,
    }
    if description:
        payload["description"] = [{"text": {"content": description}}]

    r = requests.post(f"{BASE_URL}/databases", headers=HEADERS, json=payload)
    if r.status_code not in (200, 201):
        print(f"  ✗ {title}: {r.status_code} — {r.text[:200]}")
        return None
    db_id = r.json()["id"]
    print(f"  ✓ {emoji} {title} → database criado")
    return db_id


def add_row(db_id, props):
    r = requests.post(f"{BASE_URL}/pages", headers=HEADERS,
                      json={"parent": {"database_id": db_id}, "properties": props})
    time.sleep(0.2)
    return r.status_code in (200, 201)


def archive_page(page_id, name):
    """Arquiva (deleta) a página antiga."""
    r = requests.patch(f"{BASE_URL}/pages/{page_id}", headers=HEADERS,
                       json={"archived": True})
    if r.status_code in (200, 201):
        print(f"  🗑️  Página '{name}' arquivada")
    else:
        print(f"  ⚠️  Não foi possível arquivar '{name}': {r.status_code}")


# ─── DATABASES ───────────────────────────────────────────────────────────────

def db_dashboard():
    props = {
        "Semana": {"title": {}},
        "Data início": {"date": {}},
        "Conteúdos postados": {"number": {"format": "number"}},
        "Alcance total": {"number": {"format": "number"}},
        "Salvamentos": {"number": {"format": "number"}},
        "Leads gerados": {"number": {"format": "number"}},
        "Objetivo da semana": {"select": {"options": [
            {"name": "Alcance", "color": "green"},
            {"name": "Autoridade", "color": "purple"},
            {"name": "Lead", "color": "yellow"},
            {"name": "Conversão", "color": "red"},
        ]}},
        "Status": {"select": {"options": [
            {"name": "Em andamento", "color": "yellow"},
            {"name": "Concluída", "color": "green"},
            {"name": "Planejada", "color": "gray"},
        ]}},
        "Principal aprendizado": {"rich_text": {}},
    }
    db_id = create_database("Dashboard", "🧠", props,
                            "Registro semanal da operação @quellnodigital")
    if db_id:
        add_row(db_id, {
            "Semana": {"title": [{"text": {"content": "Semana 1 — Abril 2026"}}]},
            "Objetivo da semana": {"select": {"name": "Alcance"}},
            "Status": {"select": {"name": "Em andamento"}},
        })
    return db_id


def db_calendario():
    props = {
        "Título": {"title": {}},
        "Data": {"date": {}},
        "Pilar": {"select": {"options": [
            {"name": "IA na prática", "color": "purple"},
            {"name": "Sistema vs improviso", "color": "blue"},
            {"name": "Bastidor", "color": "pink"},
            {"name": "Prova", "color": "green"},
        ]}},
        "Formato": {"select": {"options": [
            {"name": "Carrossel", "color": "orange"},
            {"name": "Reel", "color": "red"},
            {"name": "Stories", "color": "yellow"},
            {"name": "Texto", "color": "gray"},
            {"name": "LinkedIn", "color": "blue"},
        ]}},
        "Status": {"select": {"options": [
            {"name": "Planejado", "color": "gray"},
            {"name": "Em produção", "color": "yellow"},
            {"name": "Agendado", "color": "blue"},
            {"name": "Postado", "color": "green"},
        ]}},
        "Objetivo": {"select": {"options": [
            {"name": "Alcance", "color": "green"},
            {"name": "Autoridade", "color": "purple"},
            {"name": "Lead", "color": "yellow"},
            {"name": "Conversão", "color": "red"},
        ]}},
        "Hook": {"rich_text": {}},
    }
    db_id = create_database("Calendário Editorial", "📅", props,
                            "Planejamento e agendamento de conteúdo — view Calendar por Data")
    if db_id:
        seeds = [
            ("Por que você está ocupado mas não avança", "Sistema vs improviso", "Carrossel", "Lead"),
            ("IA que uso todo dia — sem mágica", "IA na prática", "Reel", "Alcance"),
            ("Bastidor da semana", "Bastidor", "Stories", "Autoridade"),
        ]
        for titulo, pilar, fmt, obj in seeds:
            add_row(db_id, {
                "Título": {"title": [{"text": {"content": titulo}}]},
                "Pilar": {"select": {"name": pilar}},
                "Formato": {"select": {"name": fmt}},
                "Objetivo": {"select": {"name": obj}},
                "Status": {"select": {"name": "Planejado"}},
            })
    return db_id


def db_processos():
    props = {
        "Processo": {"title": {}},
        "Categoria": {"select": {"options": [
            {"name": "Criação", "color": "blue"},
            {"name": "Distribuição", "color": "green"},
            {"name": "Análise", "color": "purple"},
            {"name": "Produto", "color": "orange"},
            {"name": "Cliente", "color": "pink"},
        ]}},
        "Frequência": {"select": {"options": [
            {"name": "Diário", "color": "red"},
            {"name": "Semanal", "color": "yellow"},
            {"name": "Mensal", "color": "gray"},
            {"name": "Por demanda", "color": "blue"},
        ]}},
        "Status": {"select": {"options": [
            {"name": "Ativo", "color": "green"},
            {"name": "Em revisão", "color": "yellow"},
            {"name": "Inativo", "color": "gray"},
        ]}},
        "Tempo estimado": {"rich_text": {}},
        "Responsável": {"rich_text": {}},
    }
    db_id = create_database("Processos", "⚙️", props,
                            "SOPs operacionais — o que transforma você em gestora, não executora")
    if db_id:
        sops = [
            ("Criação de conteúdo", "Criação", "Por demanda", "30-60 min"),
            ("Roteirização", "Criação", "Por demanda", "20-40 min"),
            ("Postagem", "Distribuição", "Por demanda", "15 min"),
            ("Reaproveitamento", "Distribuição", "Semanal", "30 min"),
            ("Análise semanal", "Análise", "Semanal", "30 min"),
        ]
        for nome, cat, freq, tempo in sops:
            add_row(db_id, {
                "Processo": {"title": [{"text": {"content": nome}}]},
                "Categoria": {"select": {"name": cat}},
                "Frequência": {"select": {"name": freq}},
                "Status": {"select": {"name": "Ativo"}},
                "Tempo estimado": {"rich_text": [{"text": {"content": tempo}}]},
            })
        print(f"    → 5 SOPs adicionados")
    return db_id


def db_referencias():
    props = {
        "Título": {"title": {}},
        "Tipo": {"select": {"options": [
            {"name": "Livro", "color": "blue"},
            {"name": "Perfil", "color": "pink"},
            {"name": "Frase", "color": "yellow"},
            {"name": "Insight", "color": "purple"},
            {"name": "Trend", "color": "orange"},
            {"name": "Ferramenta", "color": "green"},
        ]}},
        "Aplicação": {"rich_text": {}},
        "Tags": {"multi_select": {"options": [
            {"name": "decisão", "color": "blue"},
            {"name": "gestão", "color": "green"},
            {"name": "conteúdo", "color": "orange"},
            {"name": "IA", "color": "purple"},
            {"name": "copy", "color": "pink"},
        ]}},
        "Usado em conteúdo": {"checkbox": {}},
    }
    db_id = create_database("Referências", "📚", props,
                            "Base estratégica — livros, perfis, frases e insights")
    if db_id:
        refs = [
            ("Rápido e Devagar — Kahneman", "Livro", "Diagnóstico de comportamento e vieses de decisão"),
            ("A Única Coisa — Keller", "Livro", "Framework de prioridade, foco extremo"),
            ("Ego é seu inimigo — Holiday", "Livro", "Controle emocional, consistência sem vaidade"),
            ("Como fazer amigos — Carnegie", "Livro", "Comunicação que gera conexão"),
            ("Diário do CEO", "Livro", "Construção de autoridade, rotina pública"),
            ("@millenanbg", "Perfil", "Referência de storytelling — Quellem = sistema"),
            ("Conteúdo não é criatividade. É sistema.", "Frase", "Posicionamento central da marca"),
            ("Você não está sem tempo. Você está sem critério.", "Frase", "Gancho de alto potencial"),
            ("Ocupado é um estado. Avançando é uma escolha.", "Frase", "Insight de gestão aplicada"),
        ]
        for titulo, tipo, aplicacao in refs:
            add_row(db_id, {
                "Título": {"title": [{"text": {"content": titulo}}]},
                "Tipo": {"select": {"name": tipo}},
                "Aplicação": {"rich_text": [{"text": {"content": aplicacao}}]},
            })
        print(f"    → 9 referências adicionadas")
    return db_id


def db_clientes():
    props = {
        "Cliente": {"title": {}},
        "Nicho": {"rich_text": {}},
        "Status": {"select": {"options": [
            {"name": "Prospect", "color": "gray"},
            {"name": "Proposta enviada", "color": "yellow"},
            {"name": "Ativo", "color": "green"},
            {"name": "Pausado", "color": "orange"},
            {"name": "Encerrado", "color": "red"},
        ]}},
        "Plano": {"select": {"options": [
            {"name": "Básico", "color": "gray"},
            {"name": "Padrão", "color": "blue"},
            {"name": "Premium", "color": "purple"},
        ]}},
        "Início": {"date": {}},
        "Próxima entrega": {"date": {}},
        "Valor mensal": {"number": {"format": "real"}},
        "Contato": {"rich_text": {}},
    }
    db_id = create_database("Clientes", "🤝", props,
                            "Gestão de serviço — quando @quellnodigital virar produto")
    return db_id


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    if not TOKEN:
        print("\n❌ NOTION_TOKEN não encontrado.")
        sys.exit(1)

    print("\n🗂️  QUELLNODIGITAL OS — Criando databases...\n")

    databases = [
        ("Dashboard",            db_dashboard),
        ("Calendário Editorial", db_calendario),
        ("Processos",            db_processos),
        ("Referências",          db_referencias),
        ("Clientes",             db_clientes),
    ]

    created = []
    for name, fn in databases:
        print(f"\n📦 {name}:")
        db_id = fn()
        if db_id:
            created.append(name)
        time.sleep(0.5)

    print(f"\n{'─'*50}")
    print(f"✅ {len(created)}/5 databases criados\n")

    print("🗑️  Arquivando páginas antigas...\n")
    for name, page_id in EXISTING_PAGES.items():
        if name in created:
            archive_page(page_id, name)
            time.sleep(0.3)

    print(f"\n{'─'*50}")
    print("✅ Concluído!\n")
    print("📌 PRÓXIMO PASSO:")
    print("   Calendário Editorial → Add view → Calendar → Data")
    print("   Dashboard → Add view → Table ou Board\n")


if __name__ == "__main__":
    main()
