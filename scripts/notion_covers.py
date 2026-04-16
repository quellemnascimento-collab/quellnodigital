"""
QUELLNODIGITAL OS — Atualiza capas com cor #8ea690
Aplica cover de cor sólida em todas as páginas do workspace.

Uso:
  export NOTION_TOKEN="secret_..."
  python scripts/notion_covers.py
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

# Cor sólida #8ea690 como imagem via placehold.co
COVER_URL = "https://placehold.co/1600x400/8ea690/8ea690.png"


def set_cover(page_id, name=""):
    """Aplica cover de cor sólida em uma página."""
    r = requests.patch(
        f"{BASE_URL}/pages/{page_id}",
        headers=HEADERS,
        json={"cover": {"type": "external", "external": {"url": COVER_URL}}}
    )
    if r.status_code in (200, 201):
        print(f"  ✓ {name or page_id}")
        return True
    else:
        print(f"  ✗ {name or page_id}: {r.status_code} — {r.text[:120]}")
        return False


def get_child_pages(page_id):
    """Retorna todas as sub-páginas e databases filhos de uma página."""
    children = []
    cursor = None

    while True:
        params = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor

        r = requests.get(
            f"{BASE_URL}/blocks/{page_id}/children",
            headers=HEADERS,
            params=params
        )
        if r.status_code != 200:
            break

        data = r.json()
        for block in data.get("results", []):
            btype = block.get("type")
            if btype == "child_page":
                title = block.get("child_page", {}).get("title", "")
                children.append({"id": block["id"], "name": title, "type": "page"})
            elif btype == "child_database":
                title = block.get("child_database", {}).get("title", "")
                children.append({"id": block["id"], "name": title, "type": "database"})

        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")

    return children


def main():
    if not TOKEN:
        print("\n❌ NOTION_TOKEN não encontrado.")
        sys.exit(1)

    print("\n🎨 Aplicando cor #8ea690 em todas as páginas...\n")

    # 1. Página principal
    print("📄 Página principal:")
    set_cover(PARENT_PAGE_ID, "Quellnodigital")
    time.sleep(0.3)

    # 2. Sub-páginas diretas
    print("\n📁 Sub-páginas:")
    children = get_child_pages(PARENT_PAGE_ID)

    if not children:
        print("  Nenhuma sub-página encontrada.")
    else:
        for child in children:
            set_cover(child["id"], child["name"])
            time.sleep(0.3)

            # 3. Sub-páginas dos databases (QUELLNODIGITAL OS hub)
            if child["type"] == "database":
                sub = get_database_pages(child["id"])
                for page in sub:
                    set_cover(page["id"], f"  └─ {page['name']}")
                    time.sleep(0.3)

    print(f"\n✅ Concluído — todas as páginas com capa #8ea690\n")


def get_database_pages(db_id):
    """Retorna todas as páginas dentro de um database."""
    r = requests.post(
        f"{BASE_URL}/databases/{db_id}/query",
        headers=HEADERS,
        json={"page_size": 100}
    )
    if r.status_code != 200:
        return []

    pages = []
    for result in r.json().get("results", []):
        props = result.get("properties", {})
        title = ""
        for prop in props.values():
            if prop.get("type") == "title":
                parts = prop.get("title", [])
                if parts:
                    title = parts[0].get("text", {}).get("content", "")
                break
        pages.append({"id": result["id"], "name": title})
    return pages


if __name__ == "__main__":
    main()
