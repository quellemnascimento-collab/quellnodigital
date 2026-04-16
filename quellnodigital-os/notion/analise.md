# 📊 Análise — Métricas

> Aqui você para de criar conteúdo e começa a gerir conteúdo.

---

## Propriedades do Database

| Propriedade | Tipo | Notas |
|-------------|------|-------|
| **Conteúdo** | Relation | Ligado ao database Conteúdo |
| **Data** | Date | Data de postagem |
| **Formato** | Select | Carrossel / Reel / Stories / Texto |
| **Pilar** | Select | IA / Sistema / Bastidor / Prova |
| **Alcance** | Number | |
| **Curtidas** | Number | |
| **Salvamentos** | Number | ← métrica mais importante |
| **Compartilhamentos** | Number | |
| **Comentários** | Number | |
| **CTA converteu** | Select | Sim / Não / Parcial |
| **Score geral** | Formula | (Salvamentos × 3) + Compartilhamentos + Comentários |
| **Status** | Select | Replicar / Adaptar / Descartar |

---

## O que analisar semanalmente

### Por pilar
> Qual pilar gera mais salvamentos?
> Qual gera mais alcance?

### Por formato
> Reel cresce mais que carrossel?
> Stories convertem mais que feed?

### Por hook
> Quais primeiras linhas geraram mais cliques?
> Padrão: tensão, curiosidade ou dado?

---

## Prompt de análise semanal

```
Analise esses conteúdos e identifique:

Dados:
[COLAR TABELA DE MÉTRICAS]

- Padrões de sucesso (o que se repete nos melhores)
- Erros recorrentes (o que os piores têm em comum)
- O que deve ser repetido ou escalado
- O que deve ser descartado

Sugira 3 ajustes práticos para a próxima semana.
```

---

## Ritual de análise — todo domingo

- [ ] Preencher dados de todos os posts da semana
- [ ] Rodar prompt de análise
- [ ] Identificar 1 aprendizado principal
- [ ] Definir ajuste para a semana seguinte
- [ ] Mover status dos posts (Replicar / Adaptar / Descartar)

---

## Métricas por fase do perfil

| Fase | Métrica principal | Meta |
|------|------------------|------|
| 0-1k seguidores | Salvamentos | > 5% do alcance |
| 1k-5k | Compartilhamentos | > 2% do alcance |
| 5k+ | CTA converteu | > 1% do alcance |
