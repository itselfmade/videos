import json,os,re,subprocess,sys
import numpy as np
sys.path.insert(0,'/home/user/scripts')
from bl_sfx import SFX,SR,bleep
MUSIC='/tmp/edit/music.wav'; MUSIC_START=20
FPS=25; W='/tmp/bl'; os.makedirs(W+'/seg',exist_ok=True)
FIN='/tmp/final/'; PRO='/tmp/final_pro/'
def vpath(n): return PRO+n+'.mp4' if os.path.exists(PRO+n+'.mp4') else FIN+n+'.mp4'
# ---- words per clip
win=json.load(open('/tmp/bl/win.json')); WORDS={}
for k,v in win.items():
    WORDS.setdefault(v['clip'],[]).extend({'w':w,'s':s,'e':e} for w,s,e in v['words'])
for n,f in [('05_Entrevista','05_Entrevista'),('N1','N1'),('15_Entrevista','15_Entrevista'),('17_Vox-Pop','17_Vox-Pop'),('18_Entrevista','18_Entrevista'),('26_Entrevista_Fernando_FNAJ','26_Entrevista_Fernando_FNAJ'),('22_Entrevista_Carina','22_Entrevista_Carina'),('23_Entrevista_Claudia_take1','23_Entrevista_Claudia_take1'),('25_Entrevista_Fernando_Ingles','25_EN')]:
    WORDS[n]=json.load(open(f'/tmp/tx4/{f}.json'))['words']
WORDS['13_Teste']=[{'w':w,'s':s,'e':e} for w,s,e in [('Olá,',8.0,8.3),('olá!',8.3,8.6),('Muito',8.6,8.9),('bem.',8.9,9.3),('De',9.5,9.7),('novo,',9.7,10.1),('já',12.2,12.5),('a',12.5,12.7),('bateria',13.0,13.3),('foi',13.3,13.5),('abaixo.',13.5,14.0),('Esta',14.8,15.0),('bateria',15.0,15.4),('acabou.',15.4,15.9)]]
FIX={'drek':'direct','tirai':'tira','delexia':'dislexia','testo,':'Teste,','testo.':'Teste.','apreendedor':'empreendedor','viras':'Vira','-te':'-te','câmera':'câmara','shaved':'','manivela?':'manivela?','caralhado.':'caralho.','fernand.':'Fernando.','fernand,':'Fernando,'}
PROF=re.compile(r'^(foda|fod[ai]|fodido|caralh|puta|pariu|merda)',re.I)
def norm(w): return re.sub(r'[^\wçãõáéíóúâêô-]','',w.lower())
# ---- segment definitions: clip, ranges (local clip secs), bw, label, sfx [(abs clip time or 'end', name)], bis (s,e) replay
SEGS=[
 dict(id='A1',clip='22_Entrevista_Carina',ranges=[(0.3,2.0),(3.7,8.0)],label='Teste de som',sfx=[('end','rimshot')]),
 dict(id='A2',clip='25_Entrevista_Fernando_Ingles',ranges=[(5.8,10.3)],label='Fernando… Fernand… Fernand…',sfx=[(7.9,'pop'),(9.0,'pop')]),
 dict(id='A2s',clip='25_Entrevista_Fernando_Ingles',ranges=[(10.3,12.4)],slowmo=4.0,label='Câmara lenta: o microfone',lyrics=[('Era só Jajão',0.15,1.9),('Quando tu dizias para pedir a tua mão',2.0,3.95)],sfx=[]),
 dict(id='A3',clip='23_Entrevista_Claudia_take1',ranges=[(21.3,26.6),(26.6,28.2,{'trig':True}),(28.2,29.6)],bw=True,label='Silêncio constrangedor',sfx=[(25.0,'trombone'),(26.6,'boom'),('end','rimshot')]),
 dict(id='P1',clip='22_Entrevista_Carina',ranges=[(17.1,23.3)],label='"Boa, excelente pergunta" (1)',sfx=[(20.7,'ding')]),
 dict(id='P2',clip='05_Entrevista',ranges=[(26.7,29.4)],label='"É muito boa pergunta" (2)',sfx=[(28.0,'ding')]),
 dict(id='P3',clip='N1',ranges=[(61.4,64.0)],label='"Por acaso boa pergunta" (3)',sfx=[(63.3,'ding'),('end','rimshot')]),
 dict(id='V1',clip='17_Vox-Pop',ranges=[(13.5,16.2)],label='Para de gravar… ou grava-se outra vez?',sfx=[('end','scratch')]),
 dict(id='G1',clip='15_Entrevista',ranges=[(3.0,9.6),(9.6,12.2),(15.9,17.5)],label='À espera da entrevistada…',sfx=[(10.5,'trombone')]),
 dict(id='F1',clip='26_Entrevista_Fernando_FNAJ',ranges=[(2.0,8.4)],label='O Fernando. E, Fernando…',sfx=[(5.8,'pop'),(7.2,'pop'),('end','rimshot')],bis=(5.3,8.0)),
 dict(id='F2',clip='26_Entrevista_Fernando_FNAJ',ranges=[(87.5,91.4)],label='É só isso.',sfx=[('end','rimshot')]),
 dict(id='FA',clip='18_Entrevista',ranges=[(56.3,60.3)],label='Este ficou brutal',sfx=[('end','ding')]),
 dict(id='C2',clip='22_Entrevista_Carina',ranges=[(83.9,87.4)],label='Boa, boa.',sfx=[('end','rimshot')]),
]
def dur(r): return round((r[1]-r[0])*FPS)/FPS
def run(c): subprocess.run(c,check=True)
def extract_audio(path,s,d):
    raw=subprocess.run(['ffmpeg','-nostdin','-v','error','-ss',f'{s:.3f}','-t',f'{d:.3f}','-i',path,'-vn','-ac','1','-ar',str(SR),'-af','highpass=f=80,arnndn=m=/tmp/dn/cb.rnnn:mix=0.7','-f','f32le','-'],capture_output=True,check=True).stdout
    return np.frombuffer(raw,dtype='f4').copy()
def rms_gain(x,target=-20.0):
    act=x[np.abs(x)>10**(-45/20)]
    if len(act)<100: return 1.0
    r=20*np.log10(np.sqrt((act**2).mean())+1e-9); return 10**((target-r)/20)
def render_video(path,s,d,out,bw=False,slow=1.0,interp=False):
    n=int(round(d*FPS)); vf='scale=1080:1920:flags=lanczos,setsar=1,fps=25'
    if bw: vf+=',hue=s=0,eq=contrast=1.22:brightness=-0.03,noise=alls=5:allf=t,vignette=PI/5'
    if slow!=1.0: vf+=f',setpts={slow}*PTS'+(',minterpolate=fps=25:mi_mode=mci:mc_mode=aobmc:vsbmc=1' if interp else ',fps=25')
    run(['ffmpeg','-nostdin','-v','error','-y','-ss',f'{s:.3f}','-t',f'{d:.3f}','-i',path,'-an','-vf',vf,'-frames:v',str(int(round(n*slow))),'-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',out])
def render_trig(path,s,d,out):
    n=int(round(d*FPS))
    vf=("scale=2160:3840,setsar=1,fps=25,zoompan=z='1+0.9*min(1,on/9)':x='1080-iw/zoom/2+(random(1)-0.5)*40':y='1740-ih/zoom/2+(random(1)-0.5)*40':d=1:s=1080x1920:fps=25,"
        "colorbalance=rs=0.5:gs=-0.2:bs=-0.2:enable='lt(mod(n,6),3)',eq=contrast=1.18:saturation=1.35")
    run(['ffmpeg','-nostdin','-v','error','-y','-ss',f'{s:.3f}','-t',f'{d:.3f}','-i',path,'-an','-vf',vf,'-frames:v',str(n),'-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',out])
def censor(t): return t[0]+'***' if len(t)>1 else '***'
def cards_for(words,rs,re_,off):
    """words: list of (text,s,e,flag) absolute clip secs; returns ASS Dialogue lines on timeline offset"""
    ws=[w for w in words if w[1]>=rs-0.05 and w[1]<re_-0.02]
    out=[];i=0
    while i<len(ws):
        grp=[ws[i]];j=i+1
        while j<len(ws) and len(grp)<4 and ws[j][1]-grp[-1][2]<0.5 and not grp[-1][0].endswith(('.','?','!')): grp.append(ws[j]);j+=1
        i=j
        txt=[(g[3] and censor(g[0].rstrip('.,?!…')) + (g[0][-1] if g[0][-1] in '.,?!…' else '') or g[0]) for g in grp]
        for k,g in enumerate(grp):
            st=max(g[1],rs)-rs+off
            en=(grp[k+1][1] if k+1<len(grp) else min(g[2]+0.25,re_))
            en=min(en,g[1]+1.3,re_)-rs+off
            if en<=st: en=st+0.1
            parts=[]
            for q,t in enumerate(txt):
                parts.append('{\\c&H00D7FF&}'+t+'{\\c&HFFFFFF&}' if q==k else t)
            lines=[' '.join(parts[:2]),' '.join(parts[2:])] if len(parts)>2 else [' '.join(parts)]
            out.append((st,en,'\\N'.join([l for l in lines if l])))
    out.sort(key=lambda x:x[0])
    for q in range(len(out)-1):
        if out[q][1]>out[q+1][0]: out[q]=(out[q][0],max(out[q+1][0],out[q][0]+0.05),out[q][2])
    # drop events fully overlapped
    out=[o for q,o in enumerate(out) if q==len(out)-1 or o[0]<out[q+1][0]-0.01]
    return out
def ts(t): h=int(t//3600);m=int(t%3600//60);s=t%60; return f'{h}:{m:02d}:{s:05.2f}'
def main():
    segs_v=[];audio=[];ass=[];t=0.0;marks=[]
    items=[]  # timeline items: (video file, audio array, dur, label, sfx list (rel times), captions)
    # title
    td=2.0
    run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',f'color=c=0x101010:s=1080x1920:r=25:d={td}','-c:v','libx264','-pix_fmt','yuv420p','-crf','18',W+'/seg/title.mp4'])
    items.append(dict(v=W+'/seg/title.mp4',a=np.zeros(int(td*SR),dtype='f4'),d=td,kind='title',sfx=[(0.1,'boing')],caps=[]))
    for sg in SEGS:
        path=vpath(sg['clip']); wl=WORDS[sg['clip']]
        if sg.get('slowmo'):
            r=sg['ranges'][0]; D=sg['slowmo']; f=f"{W}/seg/{sg['id']}.mp4"
            render_video(path,r[0],r[1]-r[0],f,slow=D/(r[1]-r[0]),interp=True)
            mraw=subprocess.run(['ffmpeg','-nostdin','-v','error','-ss',str(MUSIC_START),'-t',str(D),'-i',MUSIC,'-vn','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout
            xa=np.frombuffer(mraw,dtype='f4').copy(); xa=np.pad(xa,(0,max(0,int(D*SR)-len(xa))))[:int(D*SR)]
            xa*=0.9/max(1e-9,np.abs(xa).max())*0.5; xa[:int(0.2*SR)]*=np.linspace(0,1,int(0.2*SR)); xa[-int(0.3*SR):]*=np.linspace(1,0,int(0.3*SR))
            caps=[]
            for txt,a0,b0 in sg['lyrics']:
                wsx=txt.split(); n=len(wsx); step=(b0-a0)/n
                for k in range(n):
                    parts=['{\\c&H00D7FF&}'+w_+'{\\c&HFFFFFF&}' if q==k else w_ for q,w_ in enumerate(wsx)]
                    lines=[' '.join(parts[:4]),' '.join(parts[4:])] if n>4 else [' '.join(parts)]
                    caps.append((a0+k*step,a0+(k+1)*step,'\\N'.join([l for l in lines if l])))
            items.append(dict(v=f,a=xa,d=D,kind='seg',label=sg['label'],sfx=[],caps=caps,bw=False))
            continue
        # word tuples
        wt=[]
        k=0
        while k<len(wl):
            w=wl[k]; tx=FIX.get(w['w'].lower(),w['w']); flag=bool(PROF.match(norm(tx)))
            if k+1<len(wl) and wl[k+1]['w'].startswith('-'):
                nxt=wl[k+1]; tx=tx+nxt['w']; w=dict(w,e=nxt['e']); k+=1
            if tx=='' : k+=1; continue
            wt.append([tx,w['s'],w['e'],flag]); k+=1
        for q in range(len(wt)-2):  # filho da puta
            if norm(wt[q][0])=='filho' and norm(wt[q+2][0]).startswith('puta'): wt[q][3]=wt[q+1][3]=True
        if sg.get('words_override'): wt=[[a,b,c,False] for a,b,c in sg['words_override']]
        offs=0.0;va=[];caps=[];bleeps=[]
        part_files=[]
        for ri,r in enumerate(sg['ranges']):
            d=dur(r); f=f"{W}/seg/{sg['id']}_{ri}.mp4"
            opts=r[2] if len(r)>2 else {}
            if opts.get('trig'): render_trig(path,r[0],d,f)
            else: render_video(path,r[0],d,f,bw=sg.get('bw',False))
            part_files.append(f)
            x=extract_audio(path,r[0],d); x=x[:int(d*SR)]
            if len(x)<int(d*SR): x=np.pad(x,(0,int(d*SR)-len(x)))
            x*=rms_gain(x); va.append(x)
            if opts.get('trig'):
                rr=np.random.RandomState(4)
                for k in range(int(round(d*FPS))):
                    a0=offs+k/FPS; col,bc=(('0000FF','FFFFFF'),('FFFFFF','0000FF'))[k%2]
                    caps.append((a0,a0+1/FPS,'RAW:{\\an5\\pos(%d,%d)\\fs250\\b1\\c&H%s&\\3c&H%s&\\bord12\\shad0}NOVAS'%(540+rr.randint(-16,17),1340+rr.randint(-16,17),col,bc)))
                    caps.append((a0,a0+1/FPS,'RAW:{\\an5\\pos(%d,1530)\\fs84\\b1\\c&HFFFFFF&\\3c&H0000FF&\\bord8}TRIGGERED'%(540+rr.randint(-8,9))))
            else: caps+=[(a,b,c) for a,b,c in cards_for(wt,r[0],r[1],offs)]
            for w in wt:
                if w[3] and w[1]>=r[0]-0.05 and w[1]<r[1]: bleeps.append((max(w[1],r[0])-r[0]+offs-0.02,min(w[2],r[1])-r[0]+offs+0.06))
            for (a,b) in sg.get('bleeps',[]):
                if a<r[1] and b>r[0]: bleeps.append((max(a,r[0])-r[0]+offs,min(b,r[1])-r[0]+offs))
            offs+=d
        # concat parts video
        cl=f"{W}/seg/{sg['id']}.txt"; open(cl,'w').write(''.join(f"file '{p}'\n" for p in part_files))
        vf=f"{W}/seg/{sg['id']}.mp4"; run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i',cl,'-c','copy',vf])
        a=np.concatenate(va)
        # sfx times relative to timeline offs: map abs clip time -> rel
        sfx=[]
        for tm,nm in sg['sfx']:
            if tm=='end': sfx.append((offs-0.05,nm)); continue
            o=0.0;found=None
            for r in sg['ranges']:
                if r[0]<=tm<=r[1]: found=o+tm-r[0];break
                o+=dur(r)
            if found is not None: sfx.append((found,nm))
        # bleeps -> audio
        for (a0,b0) in bleeps:
            i0=max(int(a0*SR),0);i1=min(int(b0*SR),len(a))
            if i1>i0: a[i0:i1]=np.resize(bleep((i1-i0)/SR),i1-i0)*0.6
        items.append(dict(v=vf,a=a,d=offs,kind='seg',label=sg['label'],sfx=sfx,caps=caps,bw=sg.get('bw',False)))
        if sg.get('bis'):
            bs,be=sg['bis']; d=dur((bs,be)); slow=1.6; f=f"{W}/seg/{sg['id']}_bis.mp4"
            render_video(path,bs,d,f,bw=True,slow=slow)
            x=extract_audio(path,bs,d); x=x[:int(d*SR)]; x*=rms_gain(x)
            # slow audio by resampling to 1/slow speed (pitch drops: comic)
            n=int(len(x)*slow); xs=np.interp(np.linspace(0,len(x)-1,n),np.arange(len(x)),x).astype('f4')
            cb=[]
            for (a0,b0,c0) in cards_for(wt,bs,be,0.0): cb.append((a0*slow,b0*slow,c0))
            for w in wt:
                pass
            items.append(dict(v=f,a=xs,d=n/SR,kind='bis',label='BIS!',sfx=[(0.0,'scratch')],caps=cb,bw=True))
    # end card
    ed=2.0
    run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',f'color=c=0x101010:s=1080x1920:r=25:d={ed}','-c:v','libx264','-pix_fmt','yuv420p','-crf','18',W+'/seg/end.mp4'])
    items.append(dict(v=W+'/seg/end.mp4',a=np.zeros(int(ed*SR),dtype='f4'),d=ed,kind='end',sfx=[(0.1,'clapper')],caps=[]))
    # TV static + 'piii' between scenes
    sd=0.3
    run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',f'nullsrc=s=1080x1920:r=25:d={sd}',"-vf","geq=lum='random(1)*255':cb=128:cr=128,eq=contrast=1.15","-c:v",'libx264','-pix_fmt','yuv420p','-crf','24',W+'/seg/static.mp4'])
    rs=np.random.RandomState(21); noise=(rs.randn(int(sd*SR))*0.12).astype('f4'); tt=np.arange(int(sd*SR))/SR
    beep=(0.30*np.sin(2*np.pi*1000*tt)*np.minimum(1,np.minimum(tt/0.005,(sd-tt)/0.02))).astype('f4')
    st=dict(v=W+'/seg/static.mp4',a=noise+beep,d=sd,kind='static',sfx=[],caps=[])
    new_items=[]
    for k,it in enumerate(items):
        new_items.append(it)
        if k<len(items)-1: new_items.append(dict(st))
    items=new_items
    for it in items:
        vd=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',it['v']],capture_output=True,text=True).stdout)
        it['d']=round(vd*FPS)/FPS
    # ---- timeline
    total=sum(round(it['d']*FPS)/FPS for it in items)
    buf=np.zeros(int((total+0.5)*SR)+SR,dtype='f4')
    A=[]; t=0.0; concat=[]
    for it in items:
        d=round(it['d']*FPS)/FPS; i0=int(t*SR); x=it['a'][:int(d*SR)]; buf[i0:i0+len(x)]+=x
        for tm,nm in it['sfx']:
            s=SFX[nm](); s=s/max(1e-9,np.abs(s).max())*0.55 if nm not in('whoosh',) else s/np.abs(s).max()*0.25
            j=i0+int(max(tm,0)*SR); buf[j:j+len(s)]+=s[:max(0,len(buf)-j)]
        # ass
        if it['kind']=='title':
            A.append((t+0.05,t+d,'{\\an5\\fs170\\b1\\c&H00D7FF&\\bord8\\3c&H000000&\\fad(150,200)\\t(0,350,\\fscx115\\fscy115)}BLOOPERS'))
            A.append((t+0.4,t+d,'{\\an5\\pos(540,1130)\\fs54\\c&HFFFFFF&\\bord4\\fad(300,200)}ENAJ 22 · Selfmade'))
        elif it['kind']=='end':
            A.append((t+0.05,t+d-0.5,'{\\an5\\fs190\\b1\\c&H00D7FF&\\bord8\\3c&H000000&\\fad(100,200)}CORTA!'))
        else:
            if it['kind']=='bis': A.append((t+0.1,t+d,'{\\an8\\pos(540,230)\\fs150\\b1\\c&H00D7FF&\\bord8\\3c&H000000&\\frz-6\\fad(80,150)}BIS!'))
            elif it.get('label'): A.append((t+0.15,t+min(d,3.2),'{\\an8\\pos(540,200)\\fs58\\b1\\c&HFFFFFF&\\bord6\\3c&H000000&\\fad(120,200)}'+it['label']))
            for a0,b0,c0 in it['caps']: A.append((t+a0,t+b0,c0[4:] if c0.startswith('RAW:') else '{\\an2\\fs66\\b1\\c&HFFFFFF&\\bord5\\3c&H000000&\\shad2\\q1\\pos(540,1450)}'+c0))
        concat.append(it['v']); t+=d
    open(W+'/all.txt','w').write(''.join(f"file '{p}'\n" for p in concat))
    run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i',W+'/all.txt','-c','copy',W+'/video_all.mp4'])
    # master audio: loudness
    mx=np.clip(buf[:int((total+0.5)*SR)],-1,1)
    np.save(W+'/mix.npy',mx)
    import wave
    w=wave.open(W+'/mix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mx*32767).astype('<i2').tobytes()); w.close()
    hdr=open('/tmp/edit/r_Reel_FAJUB/cap.ass',encoding='utf-8').read().split('[Events]')[0]
    ev='[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'+''.join(f'Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{c}\n' for a,b,c in sorted(A))
    open(W+'/bl.ass','w',encoding='utf-8').write(hdr+ev)
    print('TOTAL',round(total+0.5,1),'s',len(items),'items')
main()
