# Vídeos editados

## 25_Fernando_Ingles_Reel.mp4 (1 min 07 s, 1080×1920, Instagram Reels)
Fonte: `videos-limpos/25_Entrevista_Fernando_Ingles.mp4` (2 min 20 s), com áudio limpo e imagem estabilizada.

- **Abertura (sem a pergunta "Can you tell us what you do?"):** o apresentador diz só "Hello guys, I'm here with the National Federation President." e corta-se para a resposta do Fernando (começa em "the National Federation…", sem "Yes"). O cartão "Fernando · President of FNAJ" aparece quando ele fala. (Na gravação o Fernando não diz "I'm the president".)
- **v10:** "…we have also here in Portugal." deixa de ser cortado e termina a palavra "Portugal".
- **v9:** a introdução acaba em "President" (sem "of the Youth") e a segunda frase do Fernando vai até ao fim ("among all the country").
- **v8:** os cortes no fim de cada frase do Fernando passaram a ser colocados no fim real da palavra (sem cortar a última sílaba) e o final mantém o "Thank you, Fernando." completo, seguido de 0,5 s de silêncio. A versão alternativa 25b foi removida.
- **Nome nas perguntas:** cortado de todas ("Fernando, can you tell us…" passa a "Can you tell us…"). O final fica em "Thank you" sem "Fernando".
- **Erros e hesitações cortados:** o engasgo "in all, among all the country", pausas e hesitações na resposta sobre desinformação, "Um" do entrevistador, silêncios (pausas > 0,3 s) e as frases confusas ("that's why we make that sense…", "we do and we developed…").
- **Legendas:** gravadas no vídeo, palavra dita a vermelho, na zona central. Correções: Clubs → Associations, Eurodeputies → MEPs.
- **Música** baixa, áudio a −15 LUFS, **0,5 s de silêncio no fim** (imagem do Fernando parada no último segundo).

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

## 12_Pergunta_que_nunca_te_fizeram_completo.mp4 (2 min 21 s)
Cadeia completa "qual é a pergunta que nunca te fizeram?" — a pergunta de cada pessoa é a que a seguinte responde. 8 vídeos, ordenados pelas perguntas:

| Ordem | Pessoa | O que acontece |
|---|---|---|
| 1 | **Pedro** (professor) — só a pergunta dele, cortei o resto do que diz | Perguntam-lhe a "pergunta que nunca te fizeram" sem ter respondido a nenhuma pergunta anterior (**primeiro**) → pergunta: "Qual é o papel que tu queres ter na vida dos outros?" |
| 2 | Mulher de cabelo ruivo | Responde "qual deve ser o teu papel na tua comunidade?" |
| 3 | Mesma mulher | "Qual é a pergunta que nunca te fizeram?" → "Como é que nós podemos aproximar os jovens que não conhecem nem participam no movimento associativo?" |
| 4 | Mulher de blazer azul | Responde a essa pergunta ("como motivamos jovens…") |
| 5 | Mesma mulher | Pergunta que nunca lhe fizeram → "O que gostaria de ver feito nos próximos 5 anos no movimento associativo?" |
| 6 | Homem de boné verde | Responde à pergunta anterior |
| 7 | Mesmo homem | Pergunta que nunca lhe fizeram → "Será que ser jovem vai até aos 30 ou 35?" (fica só a pergunta, o resto que ele diz foi cortado) |
| 8 | Mulher de camisola preta | Responde "O que é ser jovem?" (sem silêncios nem hesitações) (não lhe voltam a perguntar a pergunta → **última**) |

Mesmo estilo: legendas com a palavra dita a vermelho, áudio limpo (RNNoise), imagem estabilizada, música baixa, níveis de voz igualados. Originais dos 3 vídeos novos em `videos-brutos/`.
