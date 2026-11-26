import subprocess,json,sys,numpy as np
from faster_whisper import WhisperModel
D={'07':79.656,'08':247.008,'09':466.976,'10':294.848,'11':330.208,'12':139.36}
names={'07':'07_Estudio','08':'08_Estudio','09':'09_Estudio','10':'10_Estudio','11':'11_Estudio','12':'12_Estudio'}
starts={};c=0
for k in ['07','08','09','10','11','12']: starts[k]=c; c+=D[k]
def loc(t):
    for k in ['12','11','10','09','08','07']:
        if t>=starts[k]-1e-6: return names[k],t-starts[k]
W={ # id: (abs start, abs end) in AVCHD seconds
 's01':(0,9),'s02':(100,118),'s03':(312,332),'s04':(634,668),'s05':(684,698),'s06':(768,790),'s07':(842,874),
 's08':(944,990),'s09a':(1025,1033),'s09b':(1051,1088),'s10':(1244,1274),'s11':(1281,1332),'s12':(1334,1346),
 's13':(1404,1414),'s14':(1450,1462),'s15':(1548,1560)}
m=WhisperModel('large-v3-turbo',device='cpu',compute_type='int8')
res={}
for id_,(a,b) in W.items():
    # window may span clip boundary; handle by splitting at clip start
    clip,off=loc(a+0.01)
    if loc(b-0.01)[0]!=clip: print('SPAN',id_,clip,loc(b-0.01)[0]); b=starts[[k for k in names if names[k]==clip][0]]+D[[k for k in names if names[k]==clip][0]]
    p=f'/tmp/final/{clip}.mp4'
    raw=subprocess.run(['ffmpeg','-nostdin','-v','error','-ss',f'{off:.2f}','-t',f'{b-a:.2f}','-i',p,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    arr=np.frombuffer(raw,dtype='f4')
    seg,_=m.transcribe(arr,language='pt',word_timestamps=True,beam_size=5,condition_on_previous_text=False,vad_filter=False)
    ws=[(w.word.strip(),round(w.start+off,2),round(w.end+off,2)) for s in seg for w in s.words]
    res[id_]={'clip':clip,'off':off,'dur':b-a,'words':ws}
    print(id_,clip,round(off,1),' '.join(f"{w}[{s}]" for w,s,e in ws),flush=True)
json.dump(res,open('/tmp/bl/win.json','w'),ensure_ascii=False)
