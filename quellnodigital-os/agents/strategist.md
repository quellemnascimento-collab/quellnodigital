# Agente Estrategista

Função: decidir o que postar e quando

## Prompt base

```
Com base no pipeline e nos pilares do perfil @quellnodigital:

Pilares: IA na prática | Sistema vs improviso | Bastidor | Prova

Defina os próximos 7 dias de conteúdo com:
- formato (carrossel / reels / texto / stories)
- objetivo (alcance / lead / conversão)
- prioridade (alta / média / baixa)

Considere:
- Equilíbrio entre pilares
- Alternância de formatos
- Progressão: autoridade → engajamento → conversão

Contexto atual: [INPUT — o que foi postado na semana anterior]
Objetivo da semana: [INPUT]
```

## Também usado para: seleção de ideias

```
Recebeu as seguintes ideias do Ideator:
[COLAR OUTPUT]

Selecione a de maior potencial com base em:
1. Conexão com posicionamento
2. Potencial de salvamento
3. Alinhamento com objetivo da semana
4. Tensão genuína

Entregue:
- Ideia selecionada
- Justificativa em 3 linhas
- CTA sugerido
```

## Entrada
- Output do Ideator ou backlog atual
- Objetivo da semana

## Saída
- Plano de 7 dias ou ideia selecionada
