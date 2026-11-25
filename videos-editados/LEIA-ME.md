# Vídeos editados

Todos os vídeos estão em 1080×1920 (9:16, Instagram Reels), com legendas gravadas no vídeo (**palavra dita a amarelo**), nome/organização à esquerda, música de fundo baixa (`../musica/`), áudio limpo a −15 LUFS, imagem estabilizada e 0,5 s de silêncio no fim. Cortes de silêncios, hesitações e erros colocados no fim real de cada palavra.

## Estrutura
```
videos-editados/
├─ entrevistas-pt/      01–06, 08–10  (uma pessoa/entidade por vídeo)
├─ montagens/           07, 11, 12    (vários vídeos juntos)
├─ ingles/              13            (entrevista em inglês)
└─ versoes-anteriores/  versões substituídas, só para consulta
```

## entrevistas-pt/
| Ficheiro | Conteúdo | Fonte (`videos-limpos/`) |
|---|---|---|
| 01_Agencia_Nacional_Erasmus | Agência Nacional Erasmus+ | 15 |
| 02_IPDJ | IPDJ | 16 |
| 03_FAJUB | FAJUB (federação distrital) | 18 |
| 04_Carina | Carina (dois takes seguidos juntos) | 22 |
| 05_Claudia | Cláudia, Youth Dream (usada a repetição completa; a 1.ª tentativa ficou de fora) | 24 (e 23) |
| 06_Fernando_FNAJ_PT | Fernando, presidente da FNAJ — ver nota abaixo | 26 |
| 08–10_Entrevista_Solta | Respostas curtas de Tele Alex (480p originais, ampliadas) | 02, 04, 06 de Tele Alex |

Ficaram de fora, por terem a pergunta "qual é a pergunta que nunca te fizeram": Tele Alex 03 e 05.

**06_Fernando_FNAJ_PT:** cartão "Fernando Vieira · Presidente da FNAJ". o apresentador diz só "Olá, estamos aqui com o Presidente da FNAJ" e as perguntas, sem tratar o Fernando pelo nome (aparece só no "Ok, obrigado, Fernando" final). Engasgo em "…um Portugal do litoral e do interior" removido. Na gravação o Fernando não diz "eu sou o presidente". A versão anterior (cortes mais soltos) está em `versoes-anteriores/`.

## montagens/
- **07_Vox_Pop** — "Numa palavra", 2 takes juntos (17 + 19).
- **11_Carina_Claudia_e_Pedro** (1 min 44 s) — "como é que o associativismo impacta os jovens": **Pedro (professor) primeiro**, depois Cláudia e Carina. Níveis de voz igualados, título de abertura, nome de cada pessoa no seu momento. Originais do Pedro em `videos-brutos/`.
- **12_Pergunta_que_nunca_te_fizeram** (2 min 21 s) — cadeia "qual é a pergunta que nunca te fizeram?": a pergunta de cada pessoa é a que a seguinte responde.

| Ordem | Pessoa | O que acontece |
|---|---|---|
| 1 | **Pedro** (professor) — só a pergunta dele | Primeiro (não respondeu a nenhuma pergunta anterior) → "Qual é o papel que tu queres ter na vida dos outros?" |
| 2 | Mulher de cabelo ruivo | Responde "qual deve ser o teu papel na tua comunidade?" |
| 3 | Mesma mulher | → "Como é que nós podemos aproximar os jovens que não conhecem nem participam no movimento associativo?" |
| 4 | Mulher de blazer azul | Responde a essa pergunta |
| 5 | Mesma mulher | → "O que gostaria de ver feito nos próximos 5 anos no movimento associativo?" |
| 6 | Homem de boné verde | Responde à pergunta anterior |
| 7 | Mesmo homem | → "Será que ser jovem vai até aos 30 ou 35?" (só a pergunta) |
| 8 | Mulher de camisola preta | Responde "O que é ser jovem?" (sem silêncios nem hesitações) — **última** |

## ingles/
**13_Fernando_Ingles_Reel** (1 min 07 s) — fonte `25_Entrevista_Fernando_Ingles`. O apresentador diz só "Hello guys, I'm here with the National Federation President" e corta-se para a resposta do Fernando; "Fernando" só no "Thank you, Fernando" final (completo). Perguntas sem o nome, sem "Can you tell us…". Cartão "Fernando Vieira · President of FNAJ". Correções de legenda: Clubs → Associations, Eurodeputies → MEPs. Na gravação o Fernando não diz "I'm the president".

## Melhoria de áudio e imagem (todos os vídeos)
- **Ruído de fundo:** RNNoise (`cb.rnnn`, 90 % do efeito), mantendo o timbre da voz. Vozes de outras pessoas ao fundo não são removidas.
- **Estabilização:** `vidstab` (só translação/rotação, sem deformar), 4 % de zoom.
- **Música:** ≈ −19 dB abaixo da voz, fade in/out.

## Histórico das legendas
As legendas eram a vermelho; passaram a **amarelo** em todos os vídeos (só mudou a cor, o resto da edição é o mesmo).

## Ferramentas
O código que gera estes vídeos está em `../ferramentas/` (`reel_engine.py` motor de edição, `specs.py` cortes de cada vídeo, `refinal.py` repete só a passagem final, `music.py` música).
