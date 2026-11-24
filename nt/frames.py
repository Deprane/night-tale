import json,sys,os; sys.path.insert(0,os.path.dirname(__file__))
import render as R, skia
S=json.load(open(sys.argv[1]))['shots']; out=sys.argv[2]; surf=skia.Surface(720,1280); names=[]
for k,a in enumerate(sys.argv[3:]):
    i,t=a.split(':'); sh=S[int(i)]; x=R.frame(sh,float(t),R.dur_of(sh),surf)
    n=f'/tmp/_f{k}.png'; skia.Image.fromarray(x,colorType=skia.kRGBA_8888_ColorType).save(n); names.append(n)
os.system('ffmpeg -v error -y '+' '.join(f'-i {n}' for n in names)+f' -filter_complex "hstack={len(names)},scale=1080:-1" {out}')
