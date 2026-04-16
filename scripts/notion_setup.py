"""
QUELLNODIGITAL OS — Notion Setup
Cria toda a estrutura de páginas e databases na workspace do Notion.

Uso:
  export NOTION_TOKEN="secret_..."
  python scripts/notion_setup.py
"""

import os
import sys
import json
import time
import requests

# ─── CONFIG ───────────────────────────────────────────────────────────────────

TOKEN = os.environ.get("NOTION_TOKEN", "")
PARENT_PAGE_ID = "3447c584d596803aa34ae1bc038de21f"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

BASE_URL = "https://api.notion.com/v1"

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def heading(text, level=2):
    tag = f"heading_{level}"
    return {"object": "block", "type": tag, tag: {"rich_text": [{"text": {"content": text}}]}}

def paragraph(text, bold=False):
    rt = {"text": {"content": text}}
    if bold:
        rt["annotations"] = {"bold": True}
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [rt]}}

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"text": {"content": text}}]}}

def todo(text, checked=False):
    return {"object": "block", "type": "to_do",
            "to_do": {"rich_text": [{"text": {"content": text}}], "checked": checked}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def callout(text, emoji="💡"):
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": [{"text": {"content": text}}], "icon": {"emoji": emoji}}}

def code_block(text, language="plain text"):
    return {"object": "block", "type": "code",
            "code": {"rich_text": [{"text": {"content": text}}], "language": language}}

def quote(text):
    return {"object": "block", "type": "quote",
            "quote": {"rich_text": [{"text": {"content": text}}]}}

def create_page(parent_id, title, emoji, children, is_database_parent=False):
    parent_key = "database_id" if is_database_parent else "page_id"
    payload = {
        "parent": {parent_key: parent_id},
        "icon": {"emoji": emoji},
        "properties": {
            "title": {"title": [{"text": {"content": title}}]}
        },
        "children": children[:100],  # Notion limit per request
    }
    r = requests.post(f"{BASE_URL}/pages", headers=HEADERS, json=payload)
    if r.status_code not in (200, 201):
        print(f"  ✗ Erro ao criar '{title}': {r.status_code} — {r.text[:200]}")
        return None
    page_id = r.json()["id"]
    print(f"  ✓ Página criada: {title}")
    # Append remaining blocks if > 100
    if len(children) > 100:
        append_blocks(page_id, children[100:])
    return page_id

def append_blocks(page_id, blocks):
    for i in range(0, len(blocks), 100):
        chunk = blocks[i:i+100]
        r = requests.patch(
            f"{BASE_URL}/blocks/{page_id}/children",
            headers=HEADERS,
            json={"children": chunk}
        )
        time.sleep(0.3)

def create_database(parent_id, title, emoji, properties, description=""):
    payload = {
        "parent": {"page_id": parent_id},
        "icon": {"emoji": emoji},
        "title": [{"text": {"content": title}}],
        "properties": properties,
    }
    if description:
        payload["description"] = [{"text": {"content": description}}]
    r = requests.post(f"{BASE_URL}/databases", headers=HEADERS, json=payload)
    if r.status_code not in (200, 201):
        print(f"  ✗ Erro ao criar database '{title}': {r.status_code} — {r.text[:200]}")
        return None
    db_id = r.json()["id"]
    print(f"  ✓ Database criado: {title}")
    return db_id

def add_database_row(db_id, props):
    payload = {"parent": {"database_id": db_id}, "properties": props}
    r = requests.post(f"{BASE_URL}/pages", headers=HEADERS, json=payload)
    time.sleep(0.2)
    return r.status_code in (200, 201)

# ─── PAGES ────────────────────────────────────────────────────────────────────

def create_dashboard(parent_id):
    blocks = [
        callout("Conteúdo não é criatividade. É sistema.", "🧠"),
        divider(),

        heading("🔥 Conteúdos da Semana", 2),
        paragraph("→ Ver database Conteúdo filtrado por esta semana"),
        divider(),

        heading("⚙️ Produção em Andamento", 2),
        paragraph("→ Ver Kanban do database Conteúdo (Status ≠ Postado)"),
        divider(),

        heading("📊 Últimos Resultados", 2),
        paragraph("→ Ver database Análise ordenado por Data desc"),
        divider(),

        heading("💡 Ideias Novas", 2),
        todo("Preencher com ideias da semana"),
        todo("Validar com Agente Ideator"),
        todo("Mover aprovadas para database Ideias"),
        divider(),

        heading("🔄 Fluxo Operacional", 2),
        code_block("IDEIA → ROTEIRO → PRODUÇÃO → POSTADO → ANÁLISE → REAPROVEITAMENTO"),
        divider(),

        heading("🚨 Regras da Operação", 2),
        bullet("Nenhum conteúdo é usado apenas uma vez"),
        bullet("Todo post tem objetivo definido antes de ser criado"),
        bullet("Análise semanal toda domingo"),
        bullet("1 conteúdo → 1 reel + 3 stories + 1 post LinkedIn"),
        divider(),

        heading("📌 Checklist Semanal", 2),
        todo("Segunda: rodar Agente Ideator + selecionar 3 ideias"),
        todo("Terça/Quarta: roteiro + refinamento"),
        todo("Quinta: produção no Canva + aprovação"),
        todo("Sexta/Sáb: publicação"),
        todo("Domingo: análise de métricas + planejamento"),
    ]
    return create_page(parent_id, "Dashboard", "🧠", blocks)


def create_conteudo_database(parent_id):
    props = {
        "Título": {"title": {}},
        "Status": {"select": {"options": [
            {"name": "Ideia", "color": "gray"},
            {"name": "Roteiro", "color": "yellow"},
            {"name": "Produção", "color": "orange"},
            {"name": "Postado", "color": "green"},
            {"name": "Reaproveitado", "color": "blue"},
        ]}},
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
        "Objetivo": {"select": {"options": [
            {"name": "Alcance", "color": "green"},
            {"name": "Autoridade", "color": "purple"},
            {"name": "Lead", "color": "yellow"},
            {"name": "Conversão", "color": "red"},
        ]}},
        "Data de postagem": {"date": {}},
        "Hook": {"rich_text": {}},
        "CTA": {"rich_text": {}},
        "Score Analista": {"number": {"format": "number"}},
        "Salvamentos": {"number": {"format": "number"}},
        "Alcance": {"number": {"format": "number"}},
    }
    return create_database(
        parent_id, "Conteúdo", "📝", props,
        "Database principal — cada linha é um conteúdo com ciclo completo"
    )


def create_calendario(parent_id):
    blocks = [
        callout("Não é só agenda — é controle de consistência.", "📅"),
        divider(),
        heading("Cadência Semanal Padrão", 2),
        bullet("Segunda → Carrossel | Sistema vs improviso | Lead / Autoridade"),
        bullet("Quarta → Reel | IA na prática | Alcance"),
        bullet("Quinta → Carrossel | Qualquer pilar | Autoridade"),
        bullet("Sexta → Texto ou Stories | Bastidor / Prova | Conexão"),
        bullet("Sábado → Reel | Alcance | Novos seguidores"),
        bullet("Domingo → Stories | Engajamento | Retenção"),
        divider(),
        heading("Blocos Mensais", 2),
        bullet("Semana 1 → Dor: nomear o problema, sem oferta"),
        bullet("Semana 2 → Solução: mostrar o caminho, sem oferta"),
        bullet("Semana 3 → Prova: resultado real + bastidor"),
        bullet("Semana 4 → Oferta: direto, com CTA claro"),
        divider(),
        heading("Regras", 2),
        bullet("Nunca publicar sem objetivo definido"),
        bullet("Alternar formatos — nunca dois carrosseis seguidos"),
        bullet("Manter equilíbrio entre os 4 pilares na semana"),
        bullet("Stories diários, mesmo que simples"),
        divider(),
        callout("Criar view Calendar no database Conteúdo → campo: Data de postagem", "⚙️"),
    ]
    return create_page(parent_id, "Calendário Editorial", "📅", blocks)


def create_ideias_database(parent_id):
    props = {
        "Ideia": {"title": {}},
        "Dor central": {"rich_text": {}},
        "Pilar": {"select": {"options": [
            {"name": "IA na prática", "color": "purple"},
            {"name": "Sistema vs improviso", "color": "blue"},
            {"name": "Bastidor", "color": "pink"},
            {"name": "Prova", "color": "green"},
        ]}},
        "Potencial": {"select": {"options": [
            {"name": "Alto", "color": "green"},
            {"name": "Médio", "color": "yellow"},
            {"name": "Baixo", "color": "gray"},
        ]}},
        "Formato sugerido": {"select": {"options": [
            {"name": "Carrossel", "color": "orange"},
            {"name": "Reel", "color": "red"},
            {"name": "Stories", "color": "yellow"},
            {"name": "Texto", "color": "gray"},
        ]}},
        "Origem": {"select": {"options": [
            {"name": "Insight", "color": "purple"},
            {"name": "Comentário", "color": "blue"},
            {"name": "Trend", "color": "orange"},
            {"name": "Concorrente", "color": "gray"},
            {"name": "IA", "color": "green"},
        ]}},
        "Status": {"select": {"options": [
            {"name": "Não usada", "color": "gray"},
            {"name": "Em produção", "color": "yellow"},
            {"name": "Usada", "color": "green"},
        ]}},
        "Gancho": {"rich_text": {}},
    }
    db_id = create_database(
        parent_id, "Ideias", "💡", props,
        "Backlog de ideias — registrar tudo, filtrar depois"
    )
    if not db_id:
        return None

    # Seed com ideias iniciais
    ideias = [
        ("Por que você posta e não converte", "Falta de sistema", "Sistema vs improviso", "Alto", "Carrossel", "Conteúdo bom que não converte tem um problema. Não é o conteúdo."),
        ("O erro de quem depende de motivação", "Inconsistência", "Sistema vs improviso", "Alto", "Texto", "Motivação acabou. Sistema continua."),
        ("Conteúdo não é criatividade", "Bloqueio criativo", "Sistema vs improviso", "Alto", "Reel", "Conteúdo não é criatividade. É sistema. E sistema se aprende."),
        ("O que aprendi como gestora sobre conteúdo", "Transição de carreira", "Bastidor", "Alto", "Carrossel", "Eu não vim do marketing para a gestão. Vim da gestão para o marketing."),
        ("IA que uso todo dia (sem mágica)", "Medo de IA", "IA na prática", "Alto", "Reel", "Parei de perguntar o que a IA pode fazer. Comecei a perguntar o que faço sem ela."),
        ("Por que você sabe muito e aparece pouco", "Insegurança no digital", "Sistema vs improviso", "Alto", "Carrossel", "Competência sem comunicação é currículo guardado na gaveta."),
        ("Bastidor da criação com sistema", "Curiosidade de processo", "Bastidor", "Médio", "Stories", "Como foi meu processo de criação essa semana (com IA, sem mágica)"),
        ("Decisão que mudou o perfil", "Resultado real", "Prova", "Alto", "Texto", "Uma decisão. Resultado em 30 dias."),
        ("Inteligência emocional não é calma, é precisão", "Reatividade", "Sistema vs improviso", "Médio", "Carrossel", "Parar de reagir não é fraqueza. É a habilidade mais cara do mercado."),
        ("Por que social media estratégico é diferente de criativo", "Posicionamento", "IA na prática", "Alto", "Carrossel", "Tem diferença entre criar conteúdo e gerir conteúdo."),
    ]
    print("  → Adicionando ideias iniciais...")
    for ideia, dor, pilar, potencial, formato, gancho in ideias:
        add_database_row(db_id, {
            "Ideia": {"title": [{"text": {"content": ideia}}]},
            "Dor central": {"rich_text": [{"text": {"content": dor}}]},
            "Pilar": {"select": {"name": pilar}},
            "Potencial": {"select": {"name": potencial}},
            "Formato sugerido": {"select": {"name": formato}},
            "Origem": {"select": {"name": "Insight"}},
            "Status": {"select": {"name": "Não usada"}},
            "Gancho": {"rich_text": [{"text": {"content": gancho}}]},
        })
    print(f"  ✓ {len(ideias)} ideias adicionadas")
    return db_id


def create_analise_database(parent_id):
    props = {
        "Conteúdo": {"title": {}},
        "Data": {"date": {}},
        "Formato": {"select": {"options": [
            {"name": "Carrossel", "color": "orange"},
            {"name": "Reel", "color": "red"},
            {"name": "Stories", "color": "yellow"},
            {"name": "Texto", "color": "gray"},
        ]}},
        "Pilar": {"select": {"options": [
            {"name": "IA na prática", "color": "purple"},
            {"name": "Sistema vs improviso", "color": "blue"},
            {"name": "Bastidor", "color": "pink"},
            {"name": "Prova", "color": "green"},
        ]}},
        "Alcance": {"number": {"format": "number"}},
        "Curtidas": {"number": {"format": "number"}},
        "Salvamentos": {"number": {"format": "number"}},
        "Compartilhamentos": {"number": {"format": "number"}},
        "Comentários": {"number": {"format": "number"}},
        "CTA converteu": {"select": {"options": [
            {"name": "Sim", "color": "green"},
            {"name": "Parcial", "color": "yellow"},
            {"name": "Não", "color": "red"},
        ]}},
        "Status": {"select": {"options": [
            {"name": "Replicar", "color": "green"},
            {"name": "Adaptar", "color": "yellow"},
            {"name": "Descartar", "color": "red"},
        ]}},
    }
    return create_database(
        parent_id, "Análise", "📊", props,
        "Métricas pós-postagem — análise semanal toda domingo"
    )


def create_processos(parent_id):
    blocks = [
        callout("Isso é o que transforma você em gestora da operação, não executora.", "⚙️"),
        divider(),
        heading("SOPs disponíveis", 2),
        bullet("Criação de Conteúdo — 6 passos"),
        bullet("Roteirização — do briefing ao roteiro aprovado"),
        bullet("Postagem — do Canva ao Instagram"),
        bullet("Reaproveitamento — critério e processo"),
        bullet("Análise Semanal — ritual de domingo"),
        divider(),
        heading("SOP: Criação de Conteúdo", 2),
        todo("1. Definir pilar"),
        todo("2. Identificar a dor específica do público"),
        todo("3. Definir o resultado que o post deve gerar"),
        todo("4. Criar o hook (primeira linha que para o scroll)"),
        todo("5. Estruturar o conteúdo slide a slide"),
        todo("6. Definir CTA coerente com o objetivo"),
        divider(),
        heading("SOP: Roteirização", 2),
        todo("Abrir template de conteúdo no Notion"),
        todo("Preencher: Objetivo / Dor / Estrutura"),
        todo("Escrever slide a slide ou por segundos (reel)"),
        todo("Rodar Agente Analista para refinamento"),
        todo("Ajustar gancho se score < 8"),
        todo("Aprovar → mover status para Produção"),
        divider(),
        heading("SOP: Postagem", 2),
        todo("Arte pronta no Canva (exportar alta resolução)"),
        todo("Copiar legenda do Notion"),
        todo("Selecionar hashtags (3 amplas + 3 médias + 3 nicho)"),
        todo("Postar no horário definido no Calendário"),
        todo("Primeiras 2h: responder todos os comentários"),
        todo("Compartilhar nos stories"),
        todo("Mover status → Postado"),
        divider(),
        heading("SOP: Reaproveitamento", 2),
        paragraph("Trigger: Salvamentos > 5% do alcance ou status = Replicar"),
        todo("Identificar conteúdo elegível no database Análise"),
        todo("Escolher novo formato (reel / stories / LinkedIn)"),
        todo("Rodar Agente de Repurpose"),
        todo("Produzir com intervalo mínimo de 30 dias do original"),
        todo("Registrar no database com tag Reaproveitado"),
        divider(),
        heading("SOP: Análise Semanal — todo domingo", 2),
        todo("Preencher métricas de todos os posts no database Análise"),
        todo("Rodar prompt de análise semanal com IA"),
        todo("Registrar 1 aprendizado principal"),
        todo("Definir ajuste para a semana seguinte"),
        todo("Planejar ideias da próxima semana"),
        todo("Atualizar Calendário Editorial"),
        divider(),
        heading("Convenção de commits (Git)", 2),
        code_block("feat: novo conteúdo criado\nrefactor: melhoria em conteúdo existente\nrepurpose: adaptação de formato\nfix: correção de erro\nchore: atualização de backlog"),
    ]
    return create_page(parent_id, "Processos", "⚙️", blocks)


def create_referencias(parent_id):
    blocks = [
        heading("Base Bibliográfica", 2),
        bullet("Rápido e Devagar (Kahneman) → diagnóstico de comportamento, vieses de decisão"),
        bullet("A Única Coisa (Keller) → framework de prioridade, foco extremo"),
        bullet("Ego é seu inimigo (Holiday) → controle emocional, consistência sem vaidade"),
        bullet("Como fazer amigos (Carnegie) → comunicação que gera conexão"),
        bullet("Diário do CEO → construção de autoridade, rotina pública"),
        divider(),
        heading("Perfis de Referência", 2),
        bullet("@millenanbg → storytelling | diferença: Quellem = sistema"),
        divider(),
        heading("Banco de Frases Isoláveis", 2),
        quote("Conteúdo não é criatividade. É sistema."),
        quote("Você não está sem tempo. Você está sem critério."),
        quote("Ocupado é um estado. Avançando é uma escolha."),
        quote("Clareza > criatividade."),
        quote("Resultado antes do processo."),
        quote("Eu não vim do marketing para a gestão. Vim da gestão para o marketing."),
        quote("O problema do conteúdo não é falta de ideia. É falta de método."),
        divider(),
        heading("Insights Acumulados", 2),
        paragraph("→ Registrar aqui após cada análise semanal"),
        divider(),
        heading("Prompt de Análise Semanal", 2),
        code_block(
            "Analise esses conteúdos e identifique:\n\n"
            "- Padrões de sucesso (o que se repete nos melhores)\n"
            "- Erros recorrentes (o que os piores têm em comum)\n"
            "- O que deve ser repetido ou escalado\n"
            "- O que deve ser descartado\n\n"
            "Sugira 3 ajustes práticos para a próxima semana."
        ),
    ]
    return create_page(parent_id, "Referências", "📚", blocks)


def create_clientes(parent_id):
    blocks = [
        callout("Para quando o @quellnodigital virar serviço para terceiros.", "🤝"),
        divider(),
        heading("Entregas Semanais Padrão", 2),
        bullet("3 posts prontos (arte + legenda) — prazo: quinta-feira"),
        bullet("3 roteiros de reels — prazo: quarta-feira"),
        bullet("10 ideias validadas — prazo: segunda-feira"),
        bullet("1 relatório de resultados — prazo: domingo"),
        divider(),
        heading("Fluxo de Aprovação", 2),
        code_block("Criação → Revisão cliente → Ajuste → Aprovado → Produção → Entrega"),
        paragraph("Prazo de aprovação: 24h após envio"),
        paragraph("Rodadas de ajuste incluídas: 2 por peça"),
        divider(),
        heading("Checklist de Onboarding", 2),
        todo("Briefing preenchido"),
        todo("Acesso ao Instagram (via Meta Business)"),
        todo("Referências de estilo aprovadas"),
        todo("Calendário do primeiro mês definido"),
        todo("Primeira entrega agendada"),
        divider(),
        heading("Template por Cliente", 2),
        paragraph("Criar sub-página para cada cliente com: Estratégia / Público / Tom de voz / Conteúdos aprovados / Resultados"),
    ]
    return create_page(parent_id, "Clientes", "🤝", blocks)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    if not TOKEN:
        print("\n❌ NOTION_TOKEN não encontrado.")
        print("   Execute: export NOTION_TOKEN='secret_...'")
        print("   Crie sua integração em: https://www.notion.so/my-integrations\n")
        sys.exit(1)

    print("\n🚀 QUELLNODIGITAL OS — Configurando Notion...")
    print(f"   Parent page: {PARENT_PAGE_ID}\n")

    pages = [
        ("Dashboard",          create_dashboard),
        ("Conteúdo DB",        create_conteudo_database),
        ("Calendário",         create_calendario),
        ("Ideias DB",          create_ideias_database),
        ("Análise DB",         create_analise_database),
        ("Processos",          create_processos),
        ("Referências",        create_referencias),
        ("Clientes",           create_clientes),
    ]

    results = {}
    for name, fn in pages:
        print(f"\n📄 Criando: {name}")
        page_id = fn(PARENT_PAGE_ID)
        results[name] = page_id
        time.sleep(0.5)

    print("\n" + "─" * 50)
    print("✅ CONCLUÍDO\n")
    created = sum(1 for v in results.values() if v)
    print(f"   {created}/{len(pages)} páginas criadas com sucesso")

    if created < len(pages):
        failed = [k for k, v in results.items() if not v]
        print(f"\n   ⚠️  Falhas: {', '.join(failed)}")
        print("   Verifique se a integração tem acesso à página pai.")
    print()


if __name__ == "__main__":
    main()
