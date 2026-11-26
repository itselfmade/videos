import numpy as np
SR=48000
def _t(d): return np.arange(int(d*SR))/SR
def _env(n,a=0.005,r=0.05):
    e=np.ones(n); na=int(a*SR); nr=int(r*SR)
    if na>0: e[:na]=np.linspace(0,1,na)
    if nr>0: e[-nr:]*=np.linspace(1,0,nr)
    return e
def lp(x,a): # one-pole lowpass
    y=np.empty_like(x); s=0.0
    for i,v in enumerate(x): s+=a*(v-s); y[i]=s
    return y
def bleep(d): t=_t(d); return 0.45*np.sin(2*np.pi*1000*t)*_env(len(t),0.004,0.01)
def boing():
    t=_t(0.9); f=140+520*np.exp(-t*5)*(1+0.5*np.sin(2*np.pi*14*t)); ph=2*np.pi*np.cumsum(f)/SR
    return 0.7*(np.sin(ph)+0.4*np.sin(2*ph))*np.exp(-t*3.2)*_env(len(t),0.003,0.05)
def trombone():
    notes=[(311,.42),(294,.42),(277,.42),(262,1.2)]; out=[]
    for k,(f0,d) in enumerate(notes):
        t=_t(d); vib=(0.02*np.sin(2*np.pi*6*t) if k==3 else 0)
        f=f0*(1+vib)*(1-0.04*(t/d) if k==3 else 1); ph=2*np.pi*np.cumsum(f)/SR
        x=sum(np.sin(h*ph)/h for h in range(1,9)); x=lp(x,0.12)
        out.append(0.5*x*_env(len(t),0.03,0.08))
    return np.concatenate(out)
def snare(d=0.18,gain=1.0):
    t=_t(d); n=np.random.RandomState(3).randn(len(t)); return gain*(0.5*n*np.exp(-t*28)+0.5*np.sin(2*np.pi*190*t)*np.exp(-t*30))
def rimshot():
    out=np.zeros(int(1.4*SR))
    for off,g in [(0.0,0.9),(0.17,0.9)]:
        s=snare(0.18,g); i=int(off*SR); out[i:i+len(s)]+=s
    t=_t(0.9); n=np.random.RandomState(5).randn(len(t)); c=n-lp(n,0.35)
    i=int(0.42*SR); out[i:i+len(t)]+=0.5*c*np.exp(-t*5)
    return out*0.8
def boom():
    t=_t(1.0); f=60*np.exp(-t*1.2)+30; ph=2*np.pi*np.cumsum(f)/SR
    x=np.tanh(2.2*np.sin(ph))*np.exp(-t*3.2); n=np.random.RandomState(7).randn(len(t))*np.exp(-t*40)*0.5
    return 0.8*(x+n)*_env(len(t),0.002,0.1)
def scratch():
    t=_t(0.45); n=np.random.RandomState(9).randn(len(t)); f=2200*np.exp(-t*4.5)+250
    ph=2*np.pi*np.cumsum(f)/SR; saw=((ph/(2*np.pi))%1)*2-1
    x=(0.6*n-lp(n,0.05)*0.6)*0.5+0.5*saw; return 0.7*x*_env(len(t),0.004,0.06)*np.where(t<0.4,1,0.3)
def pop():
    t=_t(0.12); f=900*np.exp(-t*25)+180; ph=2*np.pi*np.cumsum(f)/SR; return 0.7*np.sin(ph)*np.exp(-t*30)*_env(len(t),0.001,0.01)
def whoosh(d=0.35):
    t=_t(d); n=np.random.RandomState(11).randn(len(t)); x=lp(n,0.08)-lp(n,0.01)
    e=np.sin(np.pi*t/d)**2; return 0.55*x*e*3
def ring():
    t=_t(0.42); x=(np.sin(2*np.pi*440*t)+np.sin(2*np.pi*480*t))*(0.6+0.4*np.sign(np.sin(2*np.pi*20*t)))*0.3*_env(len(t),0.01,0.02)
    gap=np.zeros(int(0.18*SR)); return np.concatenate([x,gap,x,np.zeros(int(0.25*SR)),x,gap,x])
def ding():
    t=_t(0.9); return 0.5*(np.sin(2*np.pi*1568*t)+0.4*np.sin(2*np.pi*3136*t))*np.exp(-t*5)*_env(len(t),0.001,0.05)
def clapper():
    t=_t(0.2); n=np.random.RandomState(13).randn(len(t)); return 0.8*(n-lp(n,0.2))*np.exp(-t*45)
SFX={'boing':boing,'trombone':trombone,'rimshot':rimshot,'boom':boom,'scratch':scratch,'pop':pop,'whoosh':whoosh,'ring':ring,'ding':ding,'clapper':clapper}
if __name__=='__main__':
    import wave,sys
    for k,f in SFX.items():
        x=f(); print(k,round(len(x)/SR,2),round(float(np.abs(x).max()),2))
