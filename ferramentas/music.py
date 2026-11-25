import numpy as np, wave
sr=44100; dur=82.0; n=int(sr*dur); t=np.arange(n)/sr
L=np.zeros(n); R=np.zeros(n)
chords=[[110,164.81,261.63,392.0,493.88],[87.31,130.81,220.0,329.63,440.0],[130.81,196.0,246.94,329.63,392.0],[98.0,146.83,246.94,329.63,392.0]]
step=8.0
def env(x,a,r):  # smooth attack/release on array x in seconds
    return np.clip(x/a,0,1)**2*(3-2*np.clip(x/a,0,1))*np.clip((r-x)/ (r*0.35),0,1)
for i in range(int(dur//step)+2):
    t0=i*step; ch=chords[i%4]
    m=(t>=t0)&(t<t0+step+3); x=t[m]-t0
    e=np.clip(x/2.5,0,1); e=e*e*(3-2*e); e*=np.clip((step+3-x)/3.0,0,1)
    for k,f in enumerate(ch):
        for det,pan in ((-0.35,0.35),(0.35,0.65)):
            s=np.sin(2*np.pi*(f+det)*x+k)*0.55+np.sin(2*np.pi*2*(f+det)*x)*0.12
            amp=(0.30 if k==0 else 0.16)*e*s
            L[m]+=amp*(1-pan); R[m]+=amp*pan
    # sparse soft plucks
    arp=[ch[1]*2,ch[2]*2,ch[3]*2,ch[2]*2,ch[4]*2,ch[3]*2,ch[2]*2,ch[1]*4]
    for j,f in enumerate(arp):
        s0=t0+j*1.0+ (0.5 if j%2 else 0)
        if s0>=dur: continue
        mm=(t>=s0)&(t<s0+4); x=t[mm]-s0
        env_=np.exp(-x*1.6)*np.clip(x/0.01,0,1)
        v=(np.sin(2*np.pi*f*x)+0.35*np.sin(2*np.pi*2*f*x)*np.exp(-x*3))*env_*0.07
        p=0.3+0.4*((j*37)%10)/10
        L[mm]+=v*(1-p); R[mm]+=v*p
mx=max(abs(L).max(),abs(R).max()); L/=mx; R/=mx
w=wave.open('/tmp/edit/music_raw.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((np.stack([L,R],1)*0.8*32767).astype(np.int16).tobytes()); w.close()
