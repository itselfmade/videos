import json, re, subprocess, os, shutil, sys
FONTDIR='/usr/share/fonts/truetype/dejavu'
RED='&H00D7FF&'; WHITE='&HFFFFFF&'
def norm(x): return re.sub(r'[^\w]','',x.lower())
def load_words(path):
    out=[]
    for x in json.load(open(path))['words']:
        w=x['w']
        if out and (w.startswith('-') or norm(w)==''): out[-1]['w']+=w; out[-1]['e']=x['e']; continue
        out.append({'w':w,'s':x['s'],'e':x['e']})
    for o in out: o['t']=norm(o['w'])
    return out
def find(ws,seq,start=0):
    n=len(seq)
    for i in range(start,len(ws)-n+1):
        if [ws[i+k]['t'] for k in range(n)]==seq: return i
    raise SystemExit(f'sequencia nao encontrada: {seq} (a partir de {start})')
def apply_fixes(seg,fixes):
    for old,new in fixes:
        old=[norm(o) for o in old]; n=len(old); i=0
        while i<=len(seg)-n:
            if [seg[i+k]['t'] for k in range(n)]==old:
                s0=seg[i]['s']; e0=seg[i+n-1]['e']; m=len(new)
                rep=[{'w':new[k],'s':s0+(e0-s0)*k/max(m,1),'e':s0+(e0-s0)*(k+1)/max(m,1),'t':norm(new[k])} for k in range(m)]
                seg[i:i+n]=rep; i+=max(m,1)
            else: i+=1
_EN={}
def energy(video):
    if video in _EN: return _EN[video]
    import numpy as np, wave
    wp='/tmp/edit/_en_%d.wav'%(abs(hash(video))%10**8)
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',video,'-map','0:a:0','-ac','1','-ar','16000',wp],check=True)
    w=wave.open(wp); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768; w.close()
    hop=160; n=len(a)//hop
    db=np.array([20*np.log10(np.sqrt((a[i*hop:(i+1)*hop]**2).mean())+1e-9) for i in range(n)])
    db=np.convolve(db,np.ones(3)/3,mode='same'); _EN[video]=db; return db
def dips(video,lo,hi,depth=6.0):
    import numpy as np
    db=energy(video); out=[]
    for i in range(max(3,int(lo*100)),min(len(db)-12,int(hi*100)+1)):
        if db[i]<=db[i-3:i+4].min() and (db[max(0,i-10):i+11].max()-db[i])>=depth: out.append(i*0.01)
    return out
def snap_end(video,e_nom,hi_limit=None,fallback=None):
    c=[t for t in dips(video,e_nom-0.05,e_nom+0.45) if (hi_limit is None or t<=hi_limit)]
    return (c[0]+0.005) if c else fallback
def snap_start(video,s_nom,fallback=None):
    c=dips(video,s_nom-0.30,s_nom+0.04)
    return c[-1] if c else fallback
def ts(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
def make(spec,music='/tmp/edit/music.wav',work='/tmp/edit/r'):
    name=spec['name']; wd=f'{work}_{name}'; shutil.rmtree(wd,ignore_errors=True); os.makedirs(wd)
    S={k:{'ws':load_words(v['words']),'video':v['video'],'lowres':v.get('lowres',False)} for k,v in spec['sources'].items()}
    cursor={k:0 for k in S}; segs=[]
    for c in spec['cuts']:
        k=c.get('src',list(S)[0]); ws=S[k]['ws']
        if 'raw' in c:
            segs.append((k,None,None,c,None)); continue
        i0=find(ws,c['from'],cursor[k]); i1=find(ws,c['to'],i0)+len(c['to'])-1; cursor[k]=i1+1
        segs.append((k,i0,i1,c.get('cap',False),c.get('freeze_after')))
    chunks=[]; lt_anchor=spec.get('lt_after'); prev_end_punct=True
    for si,(k,i0,i1,capf,frz) in enumerate(segs):
        if i0 is None:
            rngs=capf['raw']; ws=S[k]['ws']; lo=min(r[0] for r in rngs); hi=max(r[1] for r in rngs)
            seg=[dict(x) for x in ws if lo-0.05<=x['s']<hi]
            apply_fixes(seg,spec.get('fixes',[]))
            for q in range(len(seg)):
                starts=(q==0 and (si==0 or prev_end_punct)) or (q>0 and re.search(r'[.?!]$',seg[q-1]['w']))
                if starts and seg[q]['w'][:1].islower(): seg[q]['w']=seg[q]['w'][0].upper()+seg[q]['w'][1:]
            prev_end_punct=bool(re.search(r'[.?!]$',seg[-1]['w']))
            base=len(chunks)
            for ri,(rs,re_) in enumerate(rngs):
                chunks.append({'k':k,'s':max(0,rs),'e':re_,'ws':[],'newseg':ri==0,'first':si==0 and ri==0,'raw':True})
            for x in seg:
                idx=len(rngs)-1
                for ri,(rs,re_) in enumerate(rngs):
                    if x['s']<re_: idx=ri; break
                chunks[base+idx]['ws'].append(x)
            continue
        ws=S[k]['ws']; seg=[dict(x) for x in ws[i0:i1+1]]
        prev_e=ws[i0-1]['e'] if i0>0 else 0; next_s=ws[i1+1]['s'] if i1+1<len(ws) else 1e9
        orig=[(x['t'],x['s']) for x in seg]
        apply_fixes(seg,spec.get('fixes',[]))
        for q in range(len(seg)):
            starts = (q==0 and (si==0 or prev_end_punct or capf)) or (q>0 and re.search(r'[.?!]$',seg[q-1]['w']))
            if starts and seg[q]['w'][:1].islower(): seg[q]['w']=seg[q]['w'][0].upper()+seg[q]['w'][1:]
        prev_end_punct=bool(re.search(r'[.?!]$',seg[-1]['w']))
        # split on long pauses
        groups=[[seg[0]]]
        for a,b in zip(seg,seg[1:]):
            if b['s']-a['e']>=spec.get('pause',0.6): groups.append([b])
            else: groups[-1].append(b)
        for gi,g in enumerate(groups):
            st=g[0]['s']-0.08; en=g[-1]['e']+0.16
            if gi==0: st=max(st,prev_e+0.03)
            else: st=max(st,groups[gi-1][-1]['e']+0.2)
            if gi==len(groups)-1: en=min(en,next_s-0.03)
            else: en=min(en,groups[gi+1][0]['s']-0.2)
            if spec.get('tail_pad') and si==len(segs)-1 and gi==len(groups)-1: en=min(g[-1]['e']+spec['tail_pad'],next_s-0.02)
            if spec.get('snap_end'):
                lim=(None if gi==len(groups)-1 else groups[gi+1][0]['s']-0.05)
                fb=en
                if spec.get('tail_pad') and si==len(segs)-1 and gi==len(groups)-1: fb=g[-1]['e']+spec['tail_pad']
                e_=snap_end(S[k]['video'],g[-1]['e'],lim,fb); en=max(e_ if e_ else fb,g[-1]['s']+0.10)
                if gi==len(groups)-1 and spec['cuts'][si].get('end_at'): en=spec['cuts'][si]['end_at']
                for _k,_v in (spec.get('end_fix') or {}).items():
                    if abs(g[-1]['e']-_k)<0.12: en=_v
                st_=snap_start(S[k]['video'],g[0]['s'],st)
                if st_ is not None and (gi>0 or True): st=min(st_,g[0]['s']-0.02)
                for _k,_v in (spec.get('start_fix') or {}).items():
                    if abs(g[0]['s']-_k)<0.06: st=_v
            chunks.append({'k':k,'s':max(0,st),'e':en,'ws':g,'newseg':gi==0,'first':si==0 and gi==0})
        if frz is not None and chunks and chunks[-1]['k']==k:
            lc=chunks[-1]
            if lc['s']<frz<lc['e']:
                B={'k':k,'s':frz,'e':lc['e'],'ws':[w for w in lc['ws'] if w['s']>=frz-0.02],'newseg':False,'first':False,'freeze':frz}
                lc['ws']=[w for w in lc['ws'] if w['s']<frz-0.02]; lc['e']=frz; chunks.append(B)
            elif frz<=lc['s']: lc['freeze']=frz
    if os.environ.get('REEL_DEBUG'):
        for ci_,c_ in enumerate(chunks): print('chunk',ci_,round(c_['s'],2),round(c_['e'],2),'freeze' if c_.get('freeze') else '',len(c_['ws']))
    # zoom assignment + timeline
    z=0; last_t=-99; t=0.0; allcap=[]; lt_time=None
    for ci,c in enumerate(chunks):
        if not c['first']:
            if (c['newseg'] or t-last_t>=5.0) and not c.get('freeze'): z=1-z; last_t=t
        c['z']=z; c['t0']=t; d=c['e']-c['s']
        if c.get('raw'):
            prev=t
            for w in c['ws']:
                s0=max(prev,t+max(0,w['s']-c['s'])); s1=max(s0+0.08,t+max(0,min(w['e']-c['s'],d))); w['ot']=(s0,s1); prev=s0+0.05
        else:
            for w in c['ws']: w['ot']=(t+w['s']-c['s'],t+w['e']-c['s'])
        t+=d
    TOTAL=t
    # lower third anchor (original token of first answer word)
    if lt_anchor:
        a=[norm(x) for x in lt_anchor]
        flat=[w for c in chunks for w in c['ws']]
        for i in range(len(flat)-len(a)+1):
            if [flat[i+k]['t'] for k in range(len(a))]==a: lt_time=flat[i]['ot'][0]; break
    # cards
    cards=[]
    for c in chunks:
        cur=[]
        def flush():
            global_cards=cards
            if cur: global_cards.append(list(cur)); cur.clear()
        for w in c['ws']:
            cur.append(w); txt=' '.join(y['w'] for y in cur)
            if (len(cur)>=3 and re.search(r'[.?,!;:]$',w['w'])) or re.search(r'[.?!]$',w['w']) or len(cur)>=4 or len(txt)>=22: flush()
        flush()
    A=["[Script Info]","ScriptType: v4.00+","PlayResX: 1080","PlayResY: 1920","WrapStyle: 0","ScaledBorderAndShadow: yes","",
    "[V4+ Styles]","Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: Cap,DejaVu Sans,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,2,2,90,90,470,1",
    "Style: Name,DejaVu Sans,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,4,2,1,0,0,0,1",
    "Style: Role,DejaVu Sans,38,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,1,0,1,3,2,1,0,0,0,1",
    "Style: Hook,DejaVu Sans,56,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,2,8,100,100,330,1","",
    "[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for ci,cd in enumerate(cards):
        words=[re.sub(r'[,.;:]+$','',x['w']) if i==len(cd)-1 else x['w'] for i,x in enumerate(cd)]
        full=' '.join(words); brk=None
        if len(full)>15:
            acc=0;best=1e9
            for i in range(len(words)-1):
                acc+=len(words[i])+(1 if i else 0); dd=abs(acc-len(full)/2)
                if dd<best: best=dd;brk=i
        cs=cd[0]['ot'][0]; ce=cd[-1]['ot'][1]+0.12
        nxt=cards[ci+1][0]['ot'][0] if ci+1<len(cards) else 1e9
        ce=min(ce,nxt-0.02) if nxt>cs else ce
        for k,x in enumerate(cd):
            st=x['ot'][0] if k else cs; en=(cd[k+1]['ot'][0] if k+1<len(cd) else ce)
            if en<=st: continue
            parts=[]
            for i,wrd in enumerate(words):
                parts.append(('{\\c'+RED+'}'+wrd+'{\\c'+WHITE+'}') if i==k else wrd)
                if i<len(words)-1: parts.append('\\N' if i==brk else ' ')
            A.append(f"Dialogue: 0,{ts(st)},{ts(en)},Cap,,0,0,0,,{''.join(parts)}")
    def anchor_time(anchor):
        an=[norm(x) for x in anchor]; flat=[w for c in chunks for w in c['ws']]
        for i in range(len(flat)-len(an)+1):
            if [flat[i+k]['t'] for k in range(len(an))]==an: return flat[i]['ot'][0]
        return None
    lts=list(spec.get('lower_thirds') or [])
    if spec.get('lower_third'): lts.append((lt_anchor,)+tuple(spec['lower_third']))
    for anchor,nm,role,dly in [(x[0],x[1],(x[2] if len(x)>2 else ''),(x[3] if len(x)>3 else 0.0)) for x in lts]:
        tt=anchor_time(anchor) if anchor else None
        t0=(tt if tt is not None else 0.3)+0.2+dly
        A.append(f"Dialogue: 1,{ts(t0)},{ts(t0+4.2)},Name,,0,0,0,,{{\\pos(80,1130)\\fad(300,400)}}{nm}")
        if role: A.append(f"Dialogue: 1,{ts(t0)},{ts(t0+4.2)},Role,,0,0,0,,{{\\pos(82,1190)\\fad(300,400)}}{role}")
    if spec.get('hook'):
        A.append(f"Dialogue: 2,{ts(0.3)},{ts(4.6)},Hook,,0,0,0,,{{\\fad(400,500)}}{spec['hook']}")
    assf=f'{wd}/cap.ass'; open(assf,'w',encoding='utf-8').write('\n'.join(A)+'\n')
    # render chunks
    gains={}
    if spec.get('match_levels'):
        for k_,v_ in S.items():
            o=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-i',v_['video'],'-af','ebur128','-vn','-f','null','-'],capture_output=True,text=True).stderr
            li=[l for l in o.split('\n') if re.match(r'\s+I:\s',l)]
            gains[k_]=spec.get('target_lufs',-20)-float(li[-1].split()[1]) if li else 0.0
        print('ganhos (dB):',{k:round(v,1) for k,v in gains.items()},flush=True)
    files=[]
    for ci,c in enumerate(chunks):
        S_=S[c['k']]; pre='scale=1080:1920:flags=lanczos,' if S_['lowres'] else ''
        zoom=',crop=947:1684:67:40,scale=1080:1920:flags=lanczos' if c['z'] else ''
        out=f'{wd}/c{ci}.mp4'; files.append(out); d=c['e']-c['s']
        if c.get('freeze'):
            png=f'{wd}/f{ci}.png'
            subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',f"{c['freeze']:.3f}",'-i',S_['video'],'-frames:v','1','-vf',f'{pre}setsar=1{zoom}',png],check=True)
            subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-loop','1','-framerate','25','-i',png,'-ss',f"{c['s']:.3f}",'-t',f'{d:.3f}','-i',S_['video'],'-map','0:v:0','-map','1:a:0','-vf','setsar=1,fps=25',
              '-af',(f"volume={gains[c['k']]:.2f}dB," if gains else '')+f'afade=t=in:d=0.015,afade=t=out:st={max(d-0.03,0):.3f}:d=0.03','-c:v','libx264','-preset','fast','-crf','14','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar','48000','-t',f'{d:.3f}',out],check=True)
            continue
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',f"{c['s']:.3f}",'-i',S_['video'],'-t',f'{d:.3f}','-map','0:v:0','-map','0:a:0','-vf',f'{pre}setsar=1{zoom},fps=25',
          '-af',(f"volume={gains[c['k']]:.2f}dB," if gains else '')+f'afade=t=in:d=0.015,afade=t=out:st={max(d-0.03,0):.3f}:d=0.03','-c:v','libx264','-preset','fast','-crf','14','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar','48000',out],check=True)
    open(f'{wd}/list.txt','w').write(''.join(f"file '{p}'\n" for p in files))
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i',f'{wd}/list.txt','-c','copy',f'{wd}/cat.mp4'],check=True)
    fc=[f"[0:v]tpad=stop_mode=clone:stop_duration=0.5,ass={assf}:fontsdir={FONTDIR}[vo]",
        "[0:a]highpass=f=90,acompressor=threshold=0.1:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-16:TP=-2:LRA=7,apad=pad_dur=0.5[voice]",
        f"[1:a]atrim=0:{TOTAL+0.5:.2f},asetpts=PTS-STARTPTS,volume=-8.5dB,afade=t=in:d=2.5,afade=t=out:st={max(TOTAL-2.6,0):.2f}:d=2.6[mus]",
        "[voice][mus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[ao]"]
    outp=f'/tmp/edit/out/{name}.mp4'; os.makedirs('/tmp/edit/out',exist_ok=True)
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',f'{wd}/cat.mp4','-i',music,'-filter_complex',';'.join(fc),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-movflags','+faststart',outp],check=True)
    print(name,'OK',round(TOTAL+0.5,1),'s',len(chunks),'chunks',flush=True)
    for cd in cards: print('   ',' '.join(x['w'] for x in cd))
