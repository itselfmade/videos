# Vídeos editados

## 25_Fernando_Ingles_Reel.mp4 (1 min 17 s, 1080×1920, Instagram Reels)
Fonte: `videos-limpos/25_Entrevista_Fernando_Ingles.mp4` (2 min 20 s).

- **Cortes:** 10 segmentos; o último deixa o Fernando acabar a frase ("…voice in Europe all the days") e termina em "Obrigado, Fernando", com imagem parada nele no último segundo e **0,5 s de silêncio** no fim (música já apagada); tirei hesitações, repetições, o "Okay, not to take your time…" e o "Last question". Mantém intro, as 3 perguntas e as respostas principais.
- **Zoom:** alternância 100 % / 112 % nos segmentos do Fernando para esconder os cortes secos.
- **Legendas (inglês):** gravadas no vídeo, 2–4 palavras por cartão, brancas com contorno; a palavra que está a ser dita fica a vermelho. Dentro da zona central (fora da interface do Reels). Correções: Fernand→Fernando, Clubs→Associations, euro deputies→MEPs.
- **Nome (inglês, à esquerda):** "Fernando · President of FNAJ" no 1.º aparecimento.
- **Música:** `musica/ambiente_calma_original.m4a`, ~21 dB abaixo da voz, com fade in/out.
- **Áudio:** filtro de graves, compressão suave, −15 LUFS.

---

## Entrevistas ENAJ 22 (português) — 01 a 10
Mesmo estilo do reel do Fernando em inglês: cortes sem hesitações nem erros, zoom alternado, legendas na zona central com a palavra dita a vermelho, nome/organização à esquerda, música de fundo baixa (`musica/`), áudio a −15 LUFS e 0,5 s de silêncio no fim.

| Ficheiro | Conteúdo | Fonte (videos-limpos) |
|---|---|---|
| 01_Agencia_Nacional_Erasmus | Agência Nacional Erasmus+ | 15 |
| 02_IPDJ | IPDJ | 16 |
| 03_FAJUB | FAJUB (federação distrital) | 18 |
| 04_Carina | Carina (dois takes seguidos juntos) | 22 |
| 05_Claudia | Cláudia, Youth Dream (usada a repetição completa; a 1.ª tentativa, incompleta, ficou de fora) | 24 (e 23) |
| 06_Fernando_FNAJ_PT | Fernando, presidente da FNAJ | 26 |
| 07_Vox_Pop | "Numa palavra" — 2 takes juntos | 17 + 19 |
| 08–10_Entrevista_Solta | Respostas curtas de Tele Alex (480p originais, ampliadas) | 02, 04, 06 de Tele Alex |

Ficaram de fora, por terem a pergunta "qual é a pergunta que nunca te fizeram": Tele Alex 03 e 05.

---

## Melhoria de áudio e imagem (aplicada a todos os vídeos acima)
- **Ruído de fundo:** filtro RNNoise (modelo `cb.rnnn`, 90 % do efeito) sobre o áudio original. Mede-se cerca de −9 dB de ruído e a relação voz/ruído sobe ~5 dB, mantendo o timbre da voz (centro tonal 2262 → 2283 Hz). Vozes de outras pessoas ao fundo não são removidas.
- **Estabilização:** `vidstab` (só translação e rotação, sem deformar), suavizado de 15 fotogramas, 4 % de zoom. O solavanco entre fotogramas desce ~60 %.
- **Música:** ligeiramente mais presente (≈ −19 dB abaixo da voz), com fade in/out.

---

## 11_Carina_Claudia_e_Pedro.mp4 (1 min 44 s)
Junta as entrevistas sobre "como é que o associativismo impacta os jovens" num só vídeo: título de abertura, pergunta, resposta da Cláudia (pessoal e cívico), da Carina (visão mais ampla) e do **Pedro, professor** (capacidades práticas e ligação ao meio rural), no fim. Níveis de voz igualados, nome de cada pessoa no seu momento, mesma música e estilo. Cortei o trecho ininteligível da Carina e o final cortado do Pedro. Os vídeos `04_Carina` e `05_Claudia` mantêm-se separados. Original do Pedro em `videos-brutos/`.

---

## 12_Pergunta_que_nunca_te_fizeram.mp4 (1 min 52 s)
Cadeia "qual é a pergunta que nunca te fizeram?" — a pergunta de cada pessoa é a pergunta que a seguinte responde. Fontes: os 5 vídeos de Tele Alex (02 a 06), reordenados pela cadeia:

| Ordem | Fonte | Quem | O que acontece |
|---|---|---|---|
| 1 | Tele Alex 02 | Pessoa 1 (blazer azul) | Pergunta de abertura: "Como é que motivamos jovens…?" (não responde a nenhuma pergunta anterior → **primeira**) |
| 2 | Tele Alex 03 | Pessoa 1 | "Qual é a pergunta que nunca te fizeram?" → pergunta: "O que gostaria de ver feito nos próximos 5 anos no movimento associativo juvenil?" |
| 3 | Tele Alex 06 | Pessoa 2 (boné verde) | Responde à pergunta da Pessoa 1 |
| 4 | Tele Alex 05 | Pessoa 2 | "Qual é a pergunta que nunca te fizeram?" → pergunta: "Será que ser jovem vai até aos 30 ou 35?" |
| 5 | Tele Alex 04 | Pessoa 3 (preto) | Responde "O que é ser jovem?" (não lhe voltam a perguntar a pergunta → **última**) |

Mesmo estilo: legendas com a palavra dita a vermelho, áudio limpo (RNNoise) e imagem estabilizada, música baixa, níveis de voz igualados.
