import numpy as np, wave
sr=44100
F=dict(B1=61.74,B2=123.47,C2=65.41,C3=130.81,Fs2=92.50,Ab2=103.83,Bb2=116.54,
 B4=493.88,C5=523.25,E5=659.25,F5=698.46,Fs5=739.99,G5=783.99,Ab5=830.61,A5=880.0,B5=987.77,C6=1046.50,Eb5=622.25)
def seq(l): return [[F[n],d] for n,d in l]
A=[("B4",125),("B5",125),("Fs5",125),("Eb5",125),("B5",125),("F5",250),("E5",125)]
B=[("C5",125),("C6",125),("G5",125),("E5",125),("C6",125),("G5",250),("E5",125)]
C=[("E5",125),("F5",125),("E5",125),("Fs5",125),("G5",125),("Ab5",125),("A5",125),("B5",125)]
rh=seq(A+B+A+C)
def pair(lo,hi): return [(lo,375),(hi,125)]
lh=seq(pair("B1","B2")*2+pair("C2","C3")*2+pair("B1","B2")*2+[("Fs2",250),("Ab2",250),("Bb2",250),("B2",250)])
def render(notes):
    out=[]
    for f,d in notes:
        n=int(sr*d/1000); t=np.arange(n)/sr
        s=np.sin(2*np.pi*f*t); w=0.5*np.sign(s)+0.5*s
        env=np.minimum(1,np.minimum(t/0.005,(d/1000-t)/0.01)).clip(0)
        out.append(w*env*0.2)
    return np.concatenate(out)
a,b=render(rh),render(lh); m=max(len(a),len(b))
x=np.pad(a,(0,m-len(a)))+np.pad(b,(0,m-len(b)))
x=np.concatenate([x,np.zeros(sr//2)])
print(sum(d for _,d in rh),sum(d for _,d in lh))
with wave.open("/tmp/s.wav","wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((x*32767).astype(np.int16).tobytes())
