T='/tmp/tx4/'; V='/tmp/final_pro/'
def src(n,lowres=False): return {'words':T+n+'.json','video':V+n+'.mp4','lowres':lowres}
def cut(a,b,k='a'): return {'from':a,'to':b,'src':k}
SPECS={
'Agencia_Nacional_Erasmus':dict(name='Reel_Agencia_Nacional_Erasmus',sources={'a':src('15_Entrevista')},lower_third=('Agência Nacional Erasmus+',''),lt_after=['olá','bom','dia'],
 fixes=[(['no','facto'],['de','facto']),(['descobram'],['descubram'])],
 cuts=[cut(['olá','malta'],['ajudar','as','associações']),cut(['olá','bom','dia'],['para','vos','oferecer'])]),
'IPDJ':dict(name='Reel_IPDJ',sources={'a':src('16_Entrevista')},lower_third=('IPDJ','Instituto Português do Desporto e Juventude'),lt_after=['no','meu','entendimento'],
 cuts=[cut(['em','que','é','que','o','associativismo'],['para','o','desporto','e','para','a','juventude']),cut(['no','meu','entendimento'],['essencialmente'])]),
'FAJUB':dict(name='Reel_FAJUB',sources={'a':src('18_Entrevista')},lower_third=('FAJUB',''),lt_after=['uma','federação','distrital'],
 fixes=[(['uma','associação','distrital'],['uma','federação','distrital']),(['federação','juvenil','acaba','distrital','acaba'],['federação','distrital','acaba']),
        (['orações','juvenis'],['associações','juvenis']),(['podam'],['podem']),(['juveniles'],['juvenis'])],
 cuts=[cut(['em','que','é','que','uma','federação'],['em','prol','da','juventude']),cut(['ok','obrigado'],['ok','obrigado'])]),
'Carina':dict(name='Reel_Carina',sources={'a':src('22_Entrevista_Carina')},lower_third=('Carina',''),lt_after=['eu','acho','que'],
 fixes=[(['karina'],['Carina']),(['nos','há','ferramentas'],['nos','dá','ferramentas']),(['enés'],['ENAJ']),(['contrariamente','à','que'],['contrariamente','ao','que']),(['acessativo'],['associativo'])],
 cuts=[cut(['olá','então','estamos','aqui','no'],['karina']),cut(['ok','como','é','que','tu','achas'],['pode','impactar','a','juventude']),
       cut(['eu','acho','que'],['nos','capacita']),cut(['e','nos','permite'],['nesse','sentido']),cut(['além','disso'],['a','nossa','voz'])]),
'Claudia':dict(name='Reel_Claudia',sources={'a':src('24_Entrevista_Claudia')},lower_third=('Cláudia','Youth Dream'),lt_after=['olá','eu','sou','a','cláudia'],
 fixes=[(['enaj22'],['ENAJ','22'])],
 cuts=[cut(['então','estamos'],['youth','dream']),cut(['ok','e','como'],['para','os','jovens']),cut(['obrigado'],['obrigado'])]),
'Fernando_FNAJ_PT':dict(name='Reel_Fernando_FNAJ_PT',sources={'a':src('26_Entrevista_Fernando_FNAJ')},lower_third=('Fernando Vieira','Presidente da FNAJ'),lt_after=['sim','a','fnaj'],
 fixes=[(['do','sítio','juvenil'],['do','associativismo','juvenil']),(['federações','estritais'],['federações','distritais'])],
 cuts=[cut(['olá','estamos','aqui'],['o','fernando']),cut(['e','fernando'],['a','nível','nacional']),cut(['sim','a','fnaj'],['a','nível','local']),
       cut(['o','nosso','trabalho','é','mesmo'],['e','na','federação','nacional']),cut(['em','cooperação'],['voz','de','decisão']),
       cut(['e','no','âmbito'],['mudar','a','vida','de','um','jovem']),cut(['as','associações','tomam'],['no','território']),
       cut(['é','essencial','para','os','jovens'],['do','litoral','e','do','interior']),cut(['ok','obrigado','fernando'],['ok','obrigado','fernando'])]),
'Vox_Pop':dict(name='Reel_Vox_Pop',sources={'a':src('17_Vox-Pop'),'b':src('19_Vox-Pop')},
 cuts=[cut(['olá','malta','estamos'],['vida','deles']),cut(['descrevam','numa','palavra'],['cooperação']),cut(['diversão'],['amizades']),
       cut(['em','que','é','que','o','associativismo'],['numa','palavra'],'b'),cut(['família'],['aprendizagem'],'b')]),
'Solta_1':dict(name='Reel_Entrevista_Solta_1',sources={'a':src('02_Entrevista',True)},
 fixes=[(['federação','nacional','de','ações','juvenis'],['Federação','Nacional','de','Associações','Juvenis.']),(['enas'],['ENAJ'])],
 cuts=[cut(['como','é','que','motivamos'],['federação','nacional','de','ações','juvenis']),cut(['obrigado'],['obrigado'])]),
'Solta_2':dict(name='Reel_Entrevista_Solta_2',sources={'a':src('04_Entrevista',True)},
 cuts=[cut(['achas','que','ser','jovem'],['em','que','se','acredita'])]),
'Solta_3':dict(name='Reel_Entrevista_Solta_3',sources={'a':src('06_Entrevista',True)},
 fixes=[(['vessem','mais'],['houvesse','mais'])],
 cuts=[cut(['o','que','é','que','tu','gostavas'],['e','tudo','mais']),cut(['obrigado'],['obrigado'])]),
}

SPECS['Carina_Claudia']=dict(name='Reel_Carina_Claudia_e_Pedro',sources={'a':src('24_Entrevista_Claudia'),'b':src('22_Entrevista_Carina'),'c':src('Pedro',True)},
 match_levels=True,target_lufs=-20,
 hook='Como é que o associativismo\\Nimpacta os jovens?',
 lower_thirds=[(['olá','eu','sou','a','cláudia'],'Cláudia','Youth Dream'),(['eu','acho','que'],'Carina',''),(['eu','acho','que','a','coisa'],'Pedro','Professor',1.0)],
 fixes=[(['associativas','e','hoje'],['associativas','e','hoje']),(['contato'],['contacto']),(['ansinhos'],['ancinhos,']),(['enaj22'],['ENAJ','22']),(['acessativo'],['associativo']),(['karina'],['Carina']),(['nos','há','ferramentas'],['nos','dá','ferramentas'])],
 cuts=[cut(['então','estamos'],['youth','dream'],'a'),cut(['ok','e','como'],['para','os','jovens'],'a'),
       cut(['estou','aqui','com','a'],['karina'],'b'),cut(['eu','acho','que'],['nos','capacita'],'b'),cut(['e','nos','permite'],['e','nos','permite'],'b'),
       cut(['garantir','aqui','uma','comunidade'],['das','nossas','comunidades'],'b'),{**cut(['o','movimento','acessativo','está','vivo'],['a','nossa','voz'],'b'),'cap':True},cut(['então','no','que','é','que'],['isso','é','importante'],'c')])

SPECS['Cadeia']=dict(name='Reel_Pergunta_que_nunca_te_fizeram',
 sources={'a':src('02_Entrevista',True),'b':src('03_Entrevista',True),'c':src('05_Entrevista',True),'d':src('06_Entrevista',True),'e':src('04_Entrevista',True)},
 match_levels=True,target_lufs=-20,hook='A pergunta que\\Nnunca te fizeram',
 fixes=[(['federação','nacional','de','ações','juvenis'],['Federação','Nacional','de','Associações','Juvenis.']),(['enas'],['ENAJ']),
        (['que','acho','super'],['que','achas','super']),(['ver','feitos'],['ver','feito']),(['vessem','mais'],['houvesse','mais']),
        (['por','que','não','alargar'],['Porque','não','alargar']),(['alargado','como','é','a'],['alargado,','como','a'])],
 cuts=[cut(['como','é','que','motivamos'],['federação','nacional','de','ações','juvenis'],'a'),
       cut(['e','qual','é','que','é','aquela'],['português'],'b'),
       cut(['o','que','é','que','tu','gostavas'],['e','tudo','mais'],'d'),
       cut(['qual','é','que','achas'],['e','tudo','mais'],'c'),cut(['é','muito','boa','pergunta'],['é','muito','boa','pergunta'],'c'),
       cut(['achas','que','ser','jovem'],['em','que','se','acredita'],'e')])

SPECS['Cadeia3']=dict(name='Reel_Pergunta_que_nunca_te_fizeram_v3',
 sources={'x':src('N1',True),'y':src('N2',True),'z':src('N3',True),'a':src('02_Entrevista',True),'b':src('03_Entrevista',True),'c':src('05_Entrevista',True),'d':src('06_Entrevista',True),'e':src('04_Entrevista',True)},
 match_levels=True,target_lufs=-20,hook='A pergunta que\\Nnunca te fizeram',
 lower_thirds=[(['qual','é','que','é','o','papel'],'Pedro','Professor')],
 fixes=[(['federação','nacional','de','ações','juvenis'],['Federação','Nacional','de','Associações','Juvenis.']),(['enas'],['ENAJ']),
        (['que','acho','super'],['que','achas','super']),(['ver','feitos'],['ver','feito']),(['vessem','mais'],['houvesse','mais']),
        (['por','que','não','alargar'],['Porque','não','alargar']),(['alargado','como','é','a'],['alargado,','como','a']),(['junil'],['juvenil'])],
 cuts=[cut(['qual','é','que','achas'],['toda','a','gente','soubesse'],'x'),cut(['qual','é','que','é','o','papel'],['na','vida','dos','outros'],'x'),
       cut(['qual','é','que','achas','que','deve'],['na','tua','comunidade'],'y'),cut(['eu','acho','que','o','meu','papel'],['ideia','ou','não'],'y'),
       cut(['e','qual','é','que','achas'],['devia','ser','respondida'],'z'),cut(['como','é','que','nós','podemos'],['fazeremno'],'z'),
       cut(['como','é','que','motivamos'],['federação','nacional','de','ações','juvenis'],'a'),
       cut(['e','qual','é','que','é','aquela'],['português'],'b'),
       cut(['o','que','é','que','tu','gostavas'],['e','tudo','mais'],'d'),
       cut(['qual','é','que','achas'],['e','tudo','mais'],'c'),cut(['é','muito','boa','pergunta'],['é','muito','boa','pergunta'],'c'),
       cut(['achas','que','ser','jovem'],['em','que','se','acredita'],'e')])

SPECS['FernandoEN']=dict(name='Reel_Fernando_Ingles_v6',sources={'a':{'words':'/tmp/tx4/25_EN.json','video':'/tmp/final_pro/25_Entrevista_Fernando_Ingles.mp4','lowres':False}},
 pause=0.3,tail_pad=0.03,
 lower_third=('Fernando Vieira','President of FNAJ'),lt_after=['yes','the','national'],
 fixes=[(['clubs'],['Associations']),(['eurodeputies'],['MEPs,'])],
 cuts=[cut(['hello','guys'],['here','with']),cut(['can','you','tell','us'],['in','the','organization']),
       cut(['yes','the','national'],['associativism']),cut(['among','all','the','country'],['among','all','the','country']),
       cut(['we','can','promote'],['decisionmakers']),
       cut(['how','can','young','people'],['respond','to','it']),cut(['basically'],['they','dont','know']),
       cut(['we','know','that'],['get','involved']),cut(['how','can','the','youngsters'],['change','europe']),
       cut(['with','the','youth','forum'],['national','level']),cut(['with','our','voice'],['all','the','days']),
       {**cut(['thank','you'],['thank','you']),'freeze_after':138.40}])

_base=dict(sources={'a':{'words':'/tmp/tx4/25_EN.json','video':'/tmp/final_pro/25_Entrevista_Fernando_Ingles.mp4','lowres':False}},
 pause=0.3,tail_pad=0.03,lower_third=('Fernando Vieira','President of FNAJ'),lt_after=['of','youth','associations','of'],
 fixes=[(['clubs'],['Associations']),(['eurodeputies'],['MEPs,'])])
_rest=[cut(['the','national','federation','of','youth'],['associativism']),cut(['among','all','the','country'],['among','all','the','country']),
       cut(['we','can','promote'],['decisionmakers']),
       cut(['how','can','young','people'],['respond','to','it']),cut(['basically'],['they','dont','know']),
       cut(['we','know','that'],['get','involved']),cut(['how','can','the','youngsters'],['change','europe']),
       cut(['with','the','youth','forum'],['national','level']),cut(['with','our','voice'],['all','the','days']),
       {**cut(['thank','you'],['thank','you']),'freeze_after':138.40}]
SPECS['FernandoEN_A']=dict(_base,name='Reel_Fernando_Ingles_v7',cuts=[cut(['hello','guys'],['of','the','youth'])]+_rest)
SPECS['FernandoEN_B']=dict(_base,name='Reel_Fernando_Ingles_v7_alt',cuts=[cut(['hello','guys'],['here','with'])]+_rest)

SPECS['FernandoEN_C']=dict(_base,name='Reel_Fernando_Ingles_v8',snap_end=True,tail_pad=0.10,end_fix={63.38:63.52},
 fixes=[(['clubs'],['Associations']),(['eurodeputies'],['MEPs,']),(['fernand'],['Fernando.'])],
 cuts=[{**cut(['hello','guys'],['president']),'end_at':4.62}]+[_rest[0],{**_rest[1],'end_at':21.98}]+_rest[2:-1]+[{**cut(['thank','you'],['fernand']),'freeze_after':138.40}])

SPECS['Fernando_FNAJ_PT_v2']=dict(name='Reel_Fernando_FNAJ_PT_v2',sources={'a':src('26_Entrevista_Fernando_FNAJ')},
 pause=0.3,tail_pad=0.10,snap_end=True,end_fix={5.36:5.47,88.98:89.12},lower_third=('Fernando Vieira','Presidente da FNAJ'),lt_after=['a','fnaj'],
 fixes=[(['do','sítio','juvenil'],['do','associativismo','juvenil']),(['federações','estritais'],['federações','distritais']),(['conseguiasme'],['Conseguias-me']),(['em','cooperação'],['Em','cooperação'])],
 cuts=[cut(['olá','estamos','aqui'],['presidente','da','fnaj']),cut(['conseguiasme'],['a','nível','nacional']),cut(['a','fnaj'],['a','nível','local']),
       cut(['o','nosso','trabalho','é','mesmo'],['e','na','federação','nacional']),cut(['em','cooperação'],['voz','de','decisão']),
       cut(['e','no','âmbito'],['mudar','a','vida','de','um','jovem']),cut(['as','associações','tomam'],['no','território']),
       cut(['é','essencial','para','os','jovens'],['do','litoral','e','do','interior']),cut(['ok','obrigado','fernando'],['ok','obrigado','fernando'])])

SPECS['Fernando_FNAJ_PT_v3']=dict(SPECS['Fernando_FNAJ_PT_v2'],name='Reel_Fernando_FNAJ_PT_v3',
 sources={'a':{'words':T+'26_Entrevista_Fernando_FNAJ_b.json','video':V+'26_Entrevista_Fernando_FNAJ.mp4','lowres':False}},
 start_fix={86.4:86.37},end_fix={5.36:5.47,88.98:89.12,85.38:85.40},
 cuts=SPECS['Fernando_FNAJ_PT_v2']['cuts'][:7]+[cut(['é','essencial','para','os','jovens'],['portugal','do','litoral']),cut(['e','do','interior'],['e','do','interior']),SPECS['Fernando_FNAJ_PT_v2']['cuts'][8]])

_cc=SPECS['Carina_Claudia']
SPECS['Carina_Claudia_Pedro_primeiro']=dict(_cc,name='Reel_Carina_Claudia_e_Pedro_v2',
 lower_thirds=[(['eu','acho','que','a','coisa'],'Pedro','Professor',1.0),(['olá','eu','sou','a','cláudia'],'Cláudia','Youth Dream'),(['eu','acho','que','o','associativismo'],'Carina','')],
 cuts=[_cc['cuts'][-1]]+_cc['cuts'][:-1])
