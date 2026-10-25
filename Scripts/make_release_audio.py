import math, wave, struct, os
root=r"D:\UnrealProjects\TinyCourse\Resources\Audio"
os.makedirs(root,exist_ok=True)
def tone(name, notes, dur=.18):
    rate=22050; data=[]
    for freq,seconds in notes:
        n=int(rate*seconds)
        for i in range(n):
            env=min(1,i/(rate*.015),(n-i)/(rate*.03))
            data.append(int(10000*env*math.sin(2*math.pi*freq*i/rate)))
    with wave.open(os.path.join(root,name),'wb') as w:
        w.setparams((1,2,rate,len(data),'NONE','not compressed'))
        w.writeframes(b''.join(struct.pack('<h',v) for v in data))
tone('S_CoreCollect.wav',[(660,.10),(880,.16)])
tone('S_EntranceUnlock.wav',[(523,.10),(659,.10),(784,.16)])
tone('S_HazardWarning.wav',[(440,.12),(0,.05),(440,.12)])
tone('S_GateOpen.wav',[(160,.25),(120,.35)])
tone('S_Victory.wav',[(523,.14),(659,.14),(784,.28)])
