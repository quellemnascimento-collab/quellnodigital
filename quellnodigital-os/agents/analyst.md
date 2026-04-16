# Agente Analista

Função: melhorar conteúdo e analisar resultado

## Prompt base — refinamento

```
Analise esse conteúdo como estrategista de marketing do perfil @quellnodigital:

[COLAR CONTEÚDO]

Avalie:
- Clareza de dor (1-10)
- Força do gancho (1-10)
- Potencial de salvamento (1-10)
- Conexão com posicionamento (1-10)

Sugira melhorias objetivas (não subjetivas).
Entregue versão refinada do gancho se abaixo de 8.
```

## Prompt base — métrica

```
Dados da publicação:
- Alcance: [INPUT]
- Salvamentos: [INPUT]
- Compartilhamentos: [INPUT]
- Comentários: [INPUT]
- CTA converteu: [sim / não / parcialmente]

Diagnostique:
1. O que funcionou (seja específico)
2. O que não funcionou (causa provável)
3. Ajuste para o próximo conteúdo do mesmo pilar

Status: Replicar / Adaptar / Descartar
```

## Entrada
- Roteiro (refinamento) ou dados do Instagram (métrica)

## Saída
- Score + melhorias + versão ajustada
