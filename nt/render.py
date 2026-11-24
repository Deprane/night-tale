#!/usr/bin/env python3
import json,os,re,sys,math,random,hashlib,argparse,subprocess
from multiprocessing import Pool
import numpy as np,skia
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from world import World,Cam,W,H,vignette,col,paint
import char as C
from char import _p,_q,INK,c4
FPS=30
WPS=2.6
_SRC=hashlib.md5(b''.join(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),A),'rb').read()for A in('world.py','char.py','render.py'))).hexdigest()
FRAMES={'wide':(12,1.8,1.,50),'full':(5.,1.3,.85,45),'medium':(2.7,1.2,1.,40),'close':(1.45,1.3,1.25,38),'xclose':(.95,1.3,1.27,34),'low':(2.2,.35,.95,50),'insert':(1.4,.75,.55,40),'high':(6,5.5,.5,45)}
_WORLDS={}
def world(loc,seed):
 A=loc,seed
 if A not in _WORLDS:_WORLDS[A]=World(loc,seed)
 return _WORLDS[A]
def ease(u):return u*u*(3-2*u)
def dur_of(s):return float(s['dur'])if'dur'in s else max(1.4,len(s.get('say','').split())/WPS+.35)
def kid_state(k,t,d):
 H=np.array(k.get('at',[0,5]),float);M=np.array(k.get('to',H),float);N=min(1,t/d);I=H+(M-H)*N
 if'keys'in k:
  A=k['keys'];I=np.array(A[-1][1:3],float)if t>=A[-1][0]else np.array(A[0][1:3],float)
  for(B,C)in zip(A,A[1:]):
   if B[0]<=t<=C[0]:O=ease((t-B[0])/max(1e-06,C[0]-B[0]));I=np.array(B[1:3],float)+(np.array(C[1:3],float)-np.array(B[1:3],float))*O
 D=k.get('expr','neutral');J=k.get('react')
 if isinstance(D,list):
  E=D[0][1]
  for(F,P)in D:
   if t>=F:E=P;J=F if F>0 else J
  D=E
 G=k.get('view','front')
 if isinstance(G,list):
  E=G[0][1]
  for(F,Q)in G:
   if t>=F:E=Q
  G=E
 K=.0
 if'reach'in k:
  A=k['reach'];K=A[-1][1]if t>=A[-1][0]else A[0][1]
  for(B,C)in zip(A,A[1:]):
   if B[0]<=t<=C[0]:K=B[1]+(C[1]-B[1])*ease((t-B[0])/max(1e-06,C[0]-B[0]))
 def L(name):
  if name not in k:return .0
  A=k[name];D=A[-1][1]if t>=A[-1][0]else A[0][1]
  for(B,C)in zip(A,A[1:]):
   if B[0]<=t<=C[0]:D=B[1]+(C[1]-B[1])*ease((t-B[0])/max(1e-06,C[0]-B[0]))
  return D
 R=dict(glance=L('glance'),htilt=L('htilt'),breath=L('breath')if'breath'in k else 1.,reach=K,lamp=k.get('lamp',False),expr=D,view=G,talk=any(A<=t<B for(A,B)in k['talk'])if isinstance(k.get('talk'),list)else k.get('talk',False),walking=bool(np.any(M!=H))or'keys'in k and k['keys'][0][0]<=t<k['keys'][-1][0],react_t=J,look=k.get('look',0),pose=k.get('pose','down'),seed=k.get('seed',0));return I,R
def camera(s,t,d,target):
 A=s.get('cam',{})if isinstance(s.get('cam'),dict)else{'frame':s.get('cam','medium')};Y=min(1,t/d);E=1-(1-Y)**3 if A.get('ease')=='out'else ease(Y);F=A.get('move','push')
 if'path'in A:
  D=A['path'];B=np.array(D[-1][1:],float)
  for(C,H)in zip(D,D[1:]):
   if C[0]<=t<=H[0]:b=ease((t-C[0])/max(1e-06,H[0]-C[0]));B=np.array(C[1:],float)+(np.array(H[1:],float)-np.array(C[1:],float))*b;break
  if t<D[0][0]:B=np.array(D[0][1:],float)
  L,M,N,G,I,O=B[0],B[1],B[2],math.radians(B[3]),math.radians(B[4]),B[5]
 elif'from'in A:Z,c=np.array(A['from'],float),np.array(A.get('to',A['from']),float);B=Z+(c-Z)*E;L,M,N,G,I,O=B[0],B[1],B[2],math.radians(B[3]),math.radians(B[4]),B[5]if len(B)>5 else 45
 else:
  P,K,U,O=FRAMES[A.get('frame','medium')];P*=A.get('dist',1);K=A.get('height',K);O=A.get('fov',O);J=math.radians(A.get('angle',0));Q=0
  if F=='push':P*=1-.16*E
  elif F=='pull':P*=.84+.16*E
  elif F=='orbit_l':J-=math.radians(14)*(E-.5)
  elif F=='orbit_r':J+=math.radians(14)*(E-.5)
  elif F=='truck_l':Q=-1.2*(E-.5)
  elif F=='truck_r':Q=1.2*(E-.5)
  elif F=='rise':K+=.7*(E-.5)
  elif F=='fall':K-=.7*(E-.5)
  U=A.get('look_h',U);V,W=A.get('target',target);L=V-P*math.sin(J)+Q*math.cos(J);N=W-P*math.cos(J)-Q*math.sin(J);M=K;G=math.atan2(V-L,W-N)+(Q and 0);I=math.atan2(U-K,math.hypot(V-L,W-N))
  if F in('truck_l','truck_r'):G=J
 if'bob_keys'in A:
  R,S=0,6
  for(e,f,g)in A['bob_keys']:
   if t>=e:R,S=f,g
  M+=abs(math.sin(t*S))*R;I+=math.sin(t*S)*R*.12;G+=math.sin(t*S/2)*R*.1
 if A.get('bob'):M+=abs(math.sin(t*A.get('bob_hz',6.5)))*A['bob']
 X=A.get('handheld',.004);a=A.get('shake',0);G+=X*math.sin(t*1.3)+X*.6*math.sin(t*2.9+1);I+=X*.7*math.sin(t*1.7+2)+a*math.sin(t*43)*.5;G+=a*math.sin(t*37)*.5
 if A.get('bob'):I+=math.sin(t*A.get('bob_hz',6.5))*.006
 if'tremor'in A:
  D=A['tremor'];T=.0
  for(C,H)in zip(D,D[1:]):
   if C[0]<=t<=H[0]:T=C[1]+(H[1]-C[1])*(t-C[0])/max(1e-06,H[0]-C[0])
  if t>D[-1][0]:T=D[-1][1]
  G+=T*(math.sin(t*2*math.pi*17)+.6*math.sin(t*2*math.pi*29+1.3)+.4*math.sin(t*2*math.pi*43));I+=T*.25*math.sin(t*2*math.pi*23+.7)
 return Cam((L,M,N),G,I,O)
def frame(s,t,d,surf):
 e=world(s.get('loc','fence_forest'),s.get('seed',1));AD=[];z=0,5;e.t=t;e.open=None
 if'open_cell'in s:AE=s['open_cell'];e.open=AE['x'],max(0,min(1,(t-AE.get('start',0))/AE.get('dur',.8)))**2
 AF=list(s.get('chars',[]))+([dict(s['kid'],who='kid')]if'kid'in s else[]);e.door=None;e.swing=None
 if'swing'in s:
  A0=s['swing'];E=A0['keys'];A7=E[-1][1]if t>=E[-1][0]else E[0][1]
  for(D,I)in zip(E,E[1:]):
   if D[0]<=t<=I[0]:A7=D[1]+(I[1]-D[1])*((t-D[0])/max(1e-06,I[0]-D[0]))**2
  e.swing=A0['x'],A0['z0'],A0['z1'],A0['h'],A7
 if'door'in s:Z=s['door'];e.door=Z['x0'],Z['x1'],Z['y1'],Z['z'],max(0,min(1,(t-Z['start'])/Z.get('dur',.5)))
 for(B1,a)in enumerate(AF):
  if'hide_at'in a and t>=a['hide_at']:continue
  if'show'in a and not a['show'][0]<=t<a['show'][1]:continue
  A8,B2=kid_state(a,t,d)
  if B1==0:z=A8[0],A8[1]
  AG={'kid':C.kid,'girl':C.girl,'worker':C.worker,'beto':C.beto,'abuelo':C.abuelo}[a.get('who','kid')](B2,t)
  if'lean'in a:
   E=a['lean'];AH=E[-1][1]if t>=E[-1][0]else E[0][1]
   for(D,I)in zip(E,E[1:]):
    if D[0]<=t<=I[0]:AH=D[1]+(I[1]-D[1])*ease((t-D[0])/max(1e-06,I[0]-D[0]))
   AH+=math.sin(t*7.5)*.8*(1 if t>E[-1][0]else 0)
   def AG(cv,px,py,ppm,_f=AG,_a=AH):A=cv;A.save();A.translate(px,py);A.rotate(_a);A.translate(-px,-py);_f(A,px,py,ppm);A.restore()
  AD.append(dict(pos=[A8[0],0,A8[1]],draw=AG,shadow=.3))
 for G in s.get('props',[]):
  if'show'in G and not G['show'][0]<=t<G['show'][1]:continue
  f,g=G['at']if'at'in G else G['keys'][0][1:]
  if'keys'in G:
   E=G['keys'];f,g=E[-1][1],E[-1][2]
   if t<E[0][0]:f,g=E[0][1],E[0][2]
   for(D,I)in zip(E,E[1:]):
    if D[0]<=t<=I[0]:l=ease((t-D[0])/max(1e-06,I[0]-D[0]));f,g=D[1]+(I[1]-D[1])*l,D[2]+(I[2]-D[2])*l;break
  if'to'in G:AX=min(1,t/d);f,g=f+(G['to'][0]-f)*AX,g+(G['to'][1]-g)*AX
  AI={'sack':lambda:C.sack,'stalker':lambda:C.stalker(t),'antlered':lambda:C.antlered(t),'chupacabras':lambda:C.chupacabras(t,G.get('twist'),G.get('crouch')),'chupa_perch':lambda:C.chupa_perch(t,G.get('part','back'),G.get('climb'),G.get('twist')),'charro':lambda:C.charro(t),'nahual':lambda:C.nahual(t),'nahuala':lambda:C.nahuala(t),'lechuza':lambda:C.lechuza(t),'cadejo':lambda:C.cadejo(t),'red_eyes':lambda:lambda*A:None,'troca':lambda:C.troca(t),'claw_tips':lambda:C.claw_tips(t),'tv':lambda:C.tv(t,G.get('chyron',''),G.get('banner','ÚLTIMA HORA'),G.get('place',''),tuple(G.get('headline',['TITULAR',''])),G.get('inset','')),'llorona':lambda:C.llorona(t,G.get('face',False)),'carved_post':lambda:C.carved_post(G.get('text','WHEN HE|SOUNDS|FAR...').split('|'))}[G['type']]();A9=.0
  if'pose'in G:
   E=G['pose'];A9,AJ=E[-1][1],E[-1][2]
   if t<E[0][0]:A9,AJ=E[0][1],E[0][2]
   for(D,I)in zip(E,E[1:]):
    if D[0]<=t<=I[0]:l=ease((t-D[0])/max(1e-06,I[0]-D[0]));A9,AJ=D[1]+(I[1]-D[1])*l,D[2]+(I[2]-D[2])*l;break
   def AI(cv,px,py,ppm,_f=AI,_r=AJ):A=cv;A.save();A.translate(px,py);A.rotate(_r);A.translate(-px,-py);_f(A,px,py,ppm);A.restore()
  AD.append(dict(pos=[f,A9,g],draw=AI,shadow=G.get('shadow',.4)))
  if not AF:z=f,g
 B=surf.getCanvas();B.clear(skia.ColorBLACK);L=camera(s,t,d,z);e.draw(B,L,AD)
 if s.get('cover'):leaf_cover(B,t)
 if'flashlight'in s:flashlight(B,L,s['flashlight'],t)
 for G in s.get('props',[]):
  if G['type']=='red_eyes':
   N=L.to_cam([G['at'][0],0,G['at'][1]])
   if N[2]>.3:(A1,),m=L.proj(N);C.red_eyes(t,G.get('on'),G.get('h',2.4),G.get('sep',90))(B,A1[0],A1[1],L.f/N[2])
  if G['type']=='chupa_perch'and G.get('part')=='back'and t>=G.get('eyes_from',0):
   N=L.to_cam([G['at'][0],0,G['at'][1]])
   if N[2]>.3:(A1,),m=L.proj(N);C.chupa_perch(t,'eyes',G.get('climb'),G.get('twist'))(B,A1[0],A1[1],L.f/N[2])
 if'lowkey'in s:B3=s.get('lowkey_on')or([z[0],1.1,z[1]]if AF or s.get('props')else s['lowkey']);AY=L.to_cam(B3);B4,B5=L.proj(AY)[0][0]if AY[2]>.1 else(W/2,H/2);B.drawRect(skia.Rect(0,0,W,H),skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(B4,B5),H*.7,[skia.ColorSetARGB(40,0,0,0),skia.ColorSetARGB(140,10,4,0),skia.ColorSetARGB(240,0,0,0)],[0,.42,.9])));B.drawRect(skia.Rect(0,0,W,H),paint(col('ff8a30'),22))
 if'dark'in s:
  AK=s['dark'];E=AK['keys'];F=E[-1][1]if t>=E[-1][0]else E[0][1]
  for(D,I)in zip(E,E[1:]):
   if D[0]<=t<=I[0]:F=D[1]+(I[1]-D[1])*((t-D[0])/max(1e-06,I[0]-D[0]))
  for(B6,B7)in AK.get('flicker',[]):
   if B6<=t<B7:
    AZ=math.sin(int(t*24)*12.9898)*43758.5453%1
    if AZ>.55:F=max(F,.55+.35*AZ)
  B.drawRect(skia.Rect(0,0,W,H),paint(col(AK.get('col','02030a')),int(255*F)))
 for A in s.get('overlays',[]):
  def Q(p):A=L.to_cam(p);return L.proj(A)[0][0]if A[2]>.1 else None
  if A['type']=='gap'and A['on'][0]<=t<A['on'][1]:
   B8=24;Aa=np.linspace(A['z0'],A['z1'],B8+1);AA=None
   for(F,n)in zip(A.get('shadow',[]),A.get('shadow',[])[1:]):
    if F[0]<=t<=n[0]:h=(t-F[0])/max(1e-06,n[0]-F[0]);AA=F[1]+(n[1]-F[1])*h,F[2]+(n[2]-F[2])*h
   for(Ab,Ac)in zip(Aa,Aa[1:]):
    B9=(Ab+Ac)/2
    if AA and abs(B9-AA[0])<AA[1]/2:continue
    V,Ad=Q([A['x'],A['y'],Ab]),Q([A['x'],A['y'],Ac])
    if V is not None and Ad is not None:B.drawLine(*V,*Ad,skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(255,*[int(A)for A in col(A['col'])]),StrokeWidth=A.get('w',5),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,2)))
  if A['type']=='glow':
   E=A['keys'];F=E[-1][1]if t>=E[-1][0]else 0
   for(D,I)in zip(E,E[1:]):
    if D[0]<=t<=I[0]:F=D[1]+(I[1]-D[1])*ease((t-D[0])/max(1e-06,I[0]-D[0]))
   V=Q(A['at'])
   if F>0 and V is not None:
    N=L.to_cam(A['at']);AB=L.f*A['r']/N[2];AC=[int(A)for A in col(A['col'])];B.drawCircle(*V,AB*4,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(*V),AB*4,[skia.ColorSetARGB(int(110*F),*AC),skia.ColorSetARGB(0,*AC)])))
    if A.get('core',True):B.drawCircle(*V,AB,skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(int(255*F),255,255,245),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,max(1,AB*.4))))
  def Ae(K):
   C=K[-1][1]if t>=K[-1][0]else K[0][1]
   for(A,B)in zip(K,K[1:]):
    if A[0]<=t<=B[0]:C=A[1]+(B[1]-A[1])*ease((t-A[0])/max(1e-06,B[0]-A[0]))
   return C
  def Af(pts):
   C=[Q(A)for A in pts]
   if any(A is None for A in C):return False
   A=skia.Path();A.moveTo(*C[0])
   for D in C[1:]:A.lineTo(*D)
   A.close();B.clipPath(A,doAntiAlias=True);return True
  if A['type']=='window_view':
   B.save()
   if Af(A['clip']):
    B.drawRect(skia.Rect(0,0,W,H),paint(col(A.get('sky','0a1020'))));AL=Ae(A['light'])if'light'in A else 0;o=[Q(A)for A in A['hill']]
    if all(A is not None for A in o):
     P=skia.Path();P.moveTo(o[0][0],H*2)
     for p in o:P.lineTo(*p)
     P.lineTo(o[-1][0],H*2);P.close();B.drawPath(P,paint(col(A.get('hill_col','05070c'))))
     if A.get('forest'):
      Ag=sorted(o,key=lambda q:q[0]);BS=[A[0]for A in Ag];BA=[A[1]for A in Ag];B.save();B.clipPath(P,doAntiAlias=True);B.drawRect(skia.Rect(0,0,W,H),skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0,min(BA)),skia.Point(0,H)],[c4(col('5a5d44')),c4(col('6b6447')),c4(col('4a4a38'))],[0,.5,1])));O=random.Random(11);u=[];BB=A['hill'][0][0];AM=[A[2]for A in A['hill']];BC=[A[1]for A in A['hill']]
      for m in range(int(A.get('forest',900))):
       Ah=O.uniform(*A.get('forest_z',(AM[0],AM[-1])));Ai=.3+.7*O.random()**.6;AN=10+(BB-10)*Ai;AO=float(np.interp(Ah,AM,BC))*(Ai-.3)/.7;N=L.to_cam([AN,AO,Ah])
       if N[2]<=.5:continue
       q=L.proj(N)[0][0];BD=L.f*O.uniform(.35,.7)/N[2];u.append((-N[2],q[0],q[1],BD,O.random(),O.choice(['2f3a2a','374430','2a3326','3d4732','334029'])))
      u=[(B,A,C,D,1.,E)for(F,A,B,C,D,E)in sorted(u)];u=[(A,B,C,D,E,F)for(A,B,C,D,E,F)in u]
      for(S,T,U,Aj,BT,Ak)in u:
       if Aj<.5:B.drawPath(_p((T-U*.38,S),(T+U*.38,S),(T,S-U*1.5)),paint(col(Ak)))
       elif Aj<.92:
        B.drawLine(T,S,T,S-U*.5,paint(col('2a241c'),255,max(1,U*.12)))
        for(BE,BF,X)in((-.35,-.7,.42),(.3,-.75,.4),(0,-1.,.45)):B.drawCircle(T+BE*U,S+BF*U,X*U,paint(col(Ak)))
       else:B.drawOval(skia.Rect(T-U*.35,S-U*.25,T+U*.35,S),paint(col('6e6a5c')))
      B.restore()
     O=random.Random(5)
     for(F,n)in zip(o,o[1:]):
      for m in range(6):h=O.random();T,S=F[0]+(n[0]-F[0])*h,F[1]+(n[1]-F[1])*h;b=O.uniform(8,22)*A.get('tree_px',1);B.drawPath(_p((T-b*.35,S+2),(T+b*.35,S+2),(T,S-b)),paint(col(A.get('tree_col','05070c'))))
    if'cave'in A:
     K=Q(A['cave'])
     if K is not None:
      N=L.to_cam(A['cave']);J=L.f*A.get('cave_r',.9)/N[2];A2=skia.Path();A2.moveTo(K[0]-J,K[1]+J*.25)
      for F in range(0,181,15):X=J*(1+.12*math.sin(F*.31));A2.lineTo(K[0]-math.cos(math.radians(F))*X,K[1]+J*.25-math.sin(math.radians(F))*X*.8)
      A2.close();B.drawPath(A2,paint(col('6b6658'),255,J*.35));B.drawPath(A2,paint(col('080a07')))
      for R in range(5):B.drawCircle(K[0]-J*1.2+R*J*.6,K[1]+J*.35,J*.18,paint(col('5e5a4e')))
    if'mist'in A:
     AP=Q(A['mist'])
     if AP is not None:B.drawRect(skia.Rect(0,AP[1]-80,W,H),skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0,AP[1]-80),skia.Point(0,H)],[skia.ColorSetARGB(0,220,226,232),skia.ColorSetARGB(75,210,218,224),skia.ColorSetARGB(25,120,130,110)],[0,.3,1])))
    v=random.Random(21)
    for(R,(BG,BH))in enumerate(A.get('fog',[])):
     Al=Q([A['hill'][len(A['hill'])//2][0],BG,A['hill'][len(A['hill'])//2][2]])
     if Al is None:continue
     for BU in range(int(A.get('fog_n',14))):Am=v.uniform(120,420);An=v.uniform(22,70);F=BH*v.uniform(.2,.8);A3=(v.uniform(-200,W+200)+t*(6+4*R)*v.choice((-1,1)))%(W+600)-300;A4=Al[1]+v.uniform(-90,90);B.drawOval(skia.Rect(A3-Am,A4-An,A3+Am,A4+An),skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(int(255*F),210,216,222),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,38)))
    i=Q(A['pool'])if'pool'in A else None
    if i is not None and AL>0:
     B.drawOval(skia.Rect(i[0]-260,i[1]-40,i[0]+260,i[1]+60),skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(*i),260,[skia.ColorSetARGB(int(120*AL),200,180,140),skia.ColorSetARGB(0,0,0,0)])));O=random.Random(9)
     for m in range(40):BI,BJ=O.uniform(-200,200),O.uniform(-160,20);Z=t*O.uniform(4,12)%30;B.drawCircle(i[0]+BI+Z,i[1]+BJ-Z*.3,O.uniform(.8,2),paint(col('e8dcc0'),int(110*AL)))
   B.restore()
  if A['type']=='glass':
   B.save()
   if Af(A['clip']):
    O=random.Random(3)
    for m in range(7):Ao,Ap=O.uniform(0,W),O.uniform(0,H);Aq=O.uniform(60,220);B.drawLine(Ao,Ap,Ao+Aq*.6,Ap-Aq,skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(int(A.get('a',16)),220,230,255),StrokeWidth=O.uniform(6,18),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,6)))
   B.restore()
   for BK in A.get('bars',[]):
    p=[Q(A)for A in BK]
    if all(A is not None for A in p):
     P=skia.Path();P.moveTo(*p[0])
     for G in p[1:]:P.lineTo(*G)
     P.close();B.drawPath(P,paint(col('22160e')));B.drawPath(P,paint(INK,200,2))
  if A['type']=='runner'and A['t0']<=t<=A['t1']:
   h=(t-A['t0'])/(A['t1']-A['t0']);Ar=[A['from'][B]+(A['to'][B]-A['from'][B])*h for B in range(3)];N=L.to_cam(Ar);V=Q(Ar);As,At=Q(A['from']),Q(A['to'])
   if V is not None and As is not None and At is not None:
    AQ=[Q(A)for A in A['clip']];B.save()
    if all(A is not None for A in AQ):
     P=skia.Path();P.moveTo(*AQ[0])
     for p in AQ[1:]:P.lineTo(*p)
     P.close();B.clipPath(P,doAntiAlias=True)
    AR=L.f*A.get('size',.9)/N[2]/1000;Au=-1 if At[0]<As[0]else 1
    for R in range(6):
     l=max(0,h-R*.05);AS=Q([A['from'][B]+(A['to'][B]-A['from'][B])*l for B in range(3)])
     if AS is not None:B.drawCircle(AS[0],AS[1]+4,(6+R*5)*AR*1000/60,skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(int(70-R*10),190,170,130),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,6)))
    B.translate(*V);B.scale(AR*Au,AR);AT=paint(col('020203'));A5=t*15;BL=-70*abs(math.sin(A5));Av=7*math.sin(A5+.6);B.translate(0,BL);B.rotate(Av)
    def Aw(root,segs,w0):
     E,F=root;A=[root]
     for(G,H)in segs:E+=G*math.cos(math.radians(H));F+=G*math.sin(math.radians(H));A.append((E,F))
     for(J,(K,L))in enumerate(zip(A,A[1:])):B.drawLine(*K,*L,paint(col('020203'),255,w0*(1-J*.28)))
     C,D=A[-1]
     for I in(-1,0,1):B.drawPath(_q((C,D),(C+40,D+10+I*8),(C+70,D+34+I*16)),paint(col('020203'),255,9))
     return A
    for AU in(.5,0):
     c=math.sin(A5-AU);Ax=math.cos(A5-AU);Aw((-300,-120),[(230,70+45*c),(210,135+30*c),(170,60+40*Ax)],70);Aw((240,-150),[(200,100-55*c),(200,70-40*Ax),(90,20-20*c)],52)
     if AU:B.drawRect(skia.Rect(-2000,-2000,2000,2000),paint(col('020203'),0))
    w=skia.Path();w.moveTo(-380,-60);w.cubicTo(-300,-300,150,-340,300,-200);w.cubicTo(330,-120,200,-40,60,-60);w.cubicTo(-120,-20,-300,20,-380,-60);w.close();B.drawPath(w,AT)
    for j in range(12):B.drawPath(_p((-300+j*50,-250-15*math.sin(j*.5)),(-268+j*50,-255),(-320+j*42,-320-30*abs(math.sin(j*1.7)))),AT)
    x=skia.Path();x.moveTo(200,-250);x.quadTo(300,-400,400,-420);x.lineTo(470,-380);x.quadTo(360,-300,300,-170);x.close();B.drawPath(x,AT);B.save();B.translate(450,-440);B.rotate(-Av);B.scale(.55*Au,.55);B.translate(0,850)
    for j in range(15):A7=-70+j*10;BM=260+140*abs(math.sin(j*2.1));B.save();B.translate(0,-820);B.rotate(A7);B.drawPath(_p((-12,0),(12,0),(0,-BM)),paint(col('1a0303')));B.restore()
    BN=skia.Paint(ColorFilter=skia.ColorFilters.Matrix([.22,0,0,0,0,0,.22,0,0,0,0,0,.24,0,0,0,0,0,1,0]));B.saveLayer(None,BN);C._chupa_head(B,t,8);B.restore();B.translate(0,-700);B.rotate(8);B.translate(0,700)
    for AV in(-1,1):B.drawCircle(AV*82,-848,36,skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(255,255,10,10),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,22)));B.drawCircle(AV*82,-848,11,paint(col('ff2a2a')));B.drawCircle(AV*82,-848,4,paint(col('ffd0d0')))
    B.restore();B.drawLine(-380,-60,-560,-120+40*math.sin(A5*.5),paint(col('020203'),255,30));B.restore()
  if A['type']=='cave':
   K=Q(A['at'])
   if K is not None:
    N=L.to_cam(A['at']);J=L.f*A.get('r',2.)/N[2];M=random.Random(4);A6=skia.Path();A6.moveTo(K[0]-J*2.,K[1])
    for R in range(13):F=math.pi*R/12;X=J*(1.75+.25*M.random());A6.lineTo(K[0]-math.cos(F)*X*1.15,K[1]-math.sin(F)*X*1.1)
    A6.lineTo(K[0]+J*2.,K[1]);A6.close();B.drawPath(A6,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeLinear([skia.Point(0,K[1]-J*2),skia.Point(0,K[1])],[c4(col('8a857a')),c4(col('5e5a50'))])))
    for R in range(9):Ay=K[1]-J*(.3+1.5*M.random());Y=K[0]+J*M.uniform(-1.8,1.8);B.drawLine(Y,Ay,Y+J*M.uniform(.2,.6),Ay+J*M.uniform(-.1,.1),paint(col('4a463e'),200,max(1,J*.03)))
    y=skia.Path();y.moveTo(K[0]-J,K[1])
    for R in range(17):F=math.pi*R/16;X=J*(1+.05*math.sin(R*2.3));y.lineTo(K[0]-math.cos(F)*X,K[1]-math.sin(F)*X*1.2)
    y.lineTo(K[0]+J,K[1]);y.close();B.drawPath(y,paint(col('4a463e'),255,J*.12));B.drawPath(y,paint(col('030303')))
    for R in range(7):Y=K[0]+J*M.uniform(-.7,.7);AW=K[1]-J*1.1+abs(Y-K[0])*.5;B.drawPath(_q((Y,AW),(Y+J*.08,AW+J*.3),(Y-J*.03,AW+J*M.uniform(.3,.7))),paint(col('2a241c'),255,max(1,J*.03)))
    for R in range(8):Y=K[0]+J*M.choice((-1,1))*M.uniform(.9,2.);c=J*M.uniform(.12,.25);B.drawOval(skia.Rect(Y-c,K[1]-c*.8,Y+c,K[1]+c*.3),paint(col('6e6a5c')))
  if A['type']=='mist_world':
   M=random.Random(A.get('seed',8))
   for m in range(A.get('n',40)):
    AN=M.uniform(*A['x'])+t*M.uniform(.05,.25);Az=M.uniform(*A['z']);AO=A.get('slope',0)*max(0,Az-A.get('z0',0))+M.uniform(*A['y']);N=L.to_cam([AN,AO,Az])
    if N[2]<1:continue
    q=L.proj(N)[0][0];k=L.f*M.uniform(3,8)/N[2];b=k*M.uniform(.12,.25);B.drawOval(skia.Rect(q[0]-k,q[1]-b,q[0]+k,q[1]+b),skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(int(255*A.get('a',.3)*M.uniform(.4,1)),214,219,224),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,max(4,k*.35))))
  if A['type']=='fogout':
   F=Ae(A['keys'])
   if F>0:
    M=random.Random(6);AC=[int(A)for A in col(A.get('col','d9dde1'))]
    for m in range(26):A3=M.uniform(-.2,1.2)*W+math.sin(t*.6+M.random()*6)*60;A4=H*(1.15-F*M.uniform(.4,1.3));k=W*M.uniform(.35,.8)*(.6+F);b=k*M.uniform(.3,.5);B.drawOval(skia.Rect(A3-k,A4-b,A3+k,A4+b),skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(int(255*min(1,F*1.4)*M.uniform(.5,.9)),*AC),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,90)))
    B.drawRect(skia.Rect(0,0,W,H),paint(col(A.get('col','d9dde1')),int(255*max(0,(F-.45)/.55)**1.5)))
  if A['type']=='wash':
   E=A['keys'];F=E[-1][1]if t>=E[-1][0]else 0
   for(D,I)in zip(E,E[1:]):
    if D[0]<=t<=I[0]:F=D[1]+(I[1]-D[1])*ease((t-D[0])/max(1e-06,I[0]-D[0]))
   if F>0:B.drawRect(skia.Rect(0,0,W,H),paint(col(A['col']),int(60*F)))
 vignette(B,s.get('vignette',.75))
 for A in s.get('overlays',[]):
  if A['type']=='fogout':
   E=A['keys'];F=E[-1][1]if t>=E[-1][0]else 0
   for(D,I)in zip(E,E[1:]):
    if D[0]<=t<=I[0]:F=D[1]+(I[1]-D[1])*ease((t-D[0])/max(1e-06,I[0]-D[0]))
   if F>.6:B.drawRect(skia.Rect(0,0,W,H),paint(col(A.get('col','d9dde1')),int(255*min(1,(F-.6)/.4))))
 if s.get('alarm')and t>=s['alarm']:B.drawRect(skia.Rect(0,0,W,H),skia.Paint(Color=skia.ColorSetARGB(int(70*(.5+.5*math.sin((t-s['alarm'])*9))),255,0,0)))
 if s.get('black'):B.clear(skia.ColorBLACK)
 if'card'in s:B.clear(skia.ColorBLACK);A_=s['card'];BO=int(t*14);B0=skia.Font(skia.Typeface('Inter',skia.FontStyle.Bold()),50);BP=A_[:BO]+('_'if int(t*3)%2==0 else' ');BQ=B0.measureText(A_);B.drawString(BP,W/2-BQ/2,H/2,B0,paint(col('f2f2f2')))
 r=surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
 if'nv'in s:r=nightvision(r,s,t,d)
 for A in s.get('overlays',[]):
  if A['type']=='fogout'and'nv'in s:
   E=A['keys'];F=E[-1][1]if t>=E[-1][0]else E[0][1]
   for(D,I)in zip(E,E[1:]):
    if D[0]<=t<=I[0]:F=D[1]+(I[1]-D[1])*ease((t-D[0])/max(1e-06,I[0]-D[0]))
   if F>0:BR=np.array(col(A.get('col','d9dde1'))[:3],np.float32)*(255 if max(col(A.get('col','d9dde1'))[:3])<=1 else 1);r=r.copy();r[...,:3]=(r[...,:3].astype(np.float32)*(1-F)+BR*F).astype(np.uint8)
 return r
def leaf_cover(cv,t):
 A=cv;I=skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(255,4,7,5),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,9));D=np.random.default_rng(11)
 for(B,C,J,K)in((-40,60,14,260),(W+30,120,10,220),(-30,H-60,12,260),(W+40,H-30,12,240),(W*.45,-60,8,260)):
  E=math.sin(t*1.3+B*.01)*10;A.drawLine(B,C,B+(W/2-B)*.35+E,C+(H/2-C)*.2,skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(255,4,7,5),StrokeWidth=22,Style=skia.Paint.kStroke_Style,MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,9)))
  for N in range(J):F=D.uniform(0,2*math.pi);G=D.uniform(0,K);L,M=B+math.cos(F)*G*.9+E,C+math.sin(F)*G*.7;A.save();A.translate(L,M);A.rotate(D.uniform(0,180)+E);A.drawOval(skia.Rect(-70,-26,70,26),I);A.restore()
def flashlight(cv,cam,fl,t):
 A=fl
 if any(A<=t<B for(A,B)in A.get('off',[])):cv.drawRect(skia.Rect(0,0,W,H),paint(col('000000'),252));return
 L,M=A.get('spot',[.5,.6])
 def E(K,n):
  if t<=K[0][0]:return K[0][1:1+n]
  for(A,B)in zip(K,K[1:]):
   if A[0]<=t<=B[0]:D=ease((t-A[0])/max(1e-06,B[0]-A[0]));return[A[C]+(B[C]-A[C])*D for C in range(1,1+n)]
  return K[-1][1:1+n]
 if'aim'in A:L,M=E(A['aim'],2)
 N=E(A['wander'],1)[0]if'wander'in A else .3;O=E(A['jolt'],1)[0]if'jolt'in A else 0;B=W*L+(math.sin(t*.71)*70+math.sin(t*1.93+1)*28)*N+(math.sin(t*9.5)*55+math.sin(t*14.3+2)*35)*O+math.sin(t*13)*3,H*M+(math.sin(t*.93+2)*55+math.sin(t*2.3)*20)*N+(abs(math.sin(t*9.5))*90-45+math.sin(t*17.1)*30)*O+math.sin(t*11)*3
 if'walk'in A:P,F=E(A['walk'],2);G=P/.07;B=B[0]+math.sin(t*F/2)*75*G+math.sin(t*F)*18*G,B[1]+(abs(math.sin(t*F))-.5)*80*G+math.sin(t*F/2+1)*20*G
 D=A.get('px',240);cv.drawRect(skia.Rect(0,0,W,H),skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(*B),D*1.45,[skia.ColorSetARGB(0,0,0,0),skia.ColorSetARGB(195,0,0,0),skia.ColorSetARGB(252,0,0,0)],[0,.45,1])));I=W*.86,H*1.05;K=np.array(B)-np.array(I);Q=np.hypot(*K)or 1;J=np.array([-K[1],K[0]])/Q;C=skia.Path();C.moveTo(*np.array(I)+J*20);C.lineTo(*np.array(B)+J*D*.85);C.lineTo(*np.array(B)-J*D*.85);C.lineTo(*np.array(I)-J*20);C.close();cv.drawPath(C,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeLinear([skia.Point(*I),skia.Point(*B)],[skia.ColorSetARGB(26,255,240,200),skia.ColorSetARGB(4,255,240,200)])));cv.drawCircle(*B,D*.85,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(*B),D*.85,[skia.ColorSetARGB(110,255,235,190),skia.ColorSetARGB(0,255,235,190)])))
_RNG=np.random.default_rng(3)
_VIG=None
def nightvision(arr,s,t,d):
 global _VIG;D=s['nv']if isinstance(s['nv'],dict)else{};L=arr[...,:3].astype(np.float32)/255
 if D.get('day'):
  l=(L[...,0]*.3+L[...,1]*.59+L[...,2]*.11)[...,None];E=L*.55+l*.45;E=E*.95+.04+_RNG.normal(0,.035,E[...,:1].shape).astype(np.float32)
  if _VIG is None:Z,a=np.mgrid[0:H,0:W];_VIG=np.clip(1.25-(((a-W/2)/(W*.62))**2+((Z-H/2)/(H*.62))**2),0,1).astype(np.float32)
  E=E*(.55+.45*_VIG[...,None]);Q=D.get('hud_at',0)
  if Q and Q-.6<=t<=Q+.35 or any(A<=t<=B for(A,B)in D.get('glitch',[])):
   for u in range(7):F=int(_RNG.integers(0,H-40));f=int(_RNG.integers(8,70));m=int(_RNG.integers(-90,90));E[F:F+f]=np.roll(E[F:F+f],m,axis=1)*_RNG.uniform(.7,1.3)
   if _RNG.random()<.35:E=E*.5+_RNG.random(E.shape[:2])[...,None].astype(np.float32)*.5
  R=D.get('static_end',0)
  if R and t>d-R:n=_RNG.random(E.shape[:2]).astype(np.float32)*.9;E=np.repeat(n[...,None],3,-1)
  K=np.concatenate([np.clip(E,0,1),np.ones_like(E[...,:1])],-1);K=(K*255).astype(np.uint8);b=skia.Image.fromarray(K,colorType=skia.kRGBA_8888_ColorType);O=skia.Surface(W,H);B=O.getCanvas();B.drawImage(b,0,0)
  if Q and t<Q:return O.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
  C=col('f2f2f2');M=skia.Font(skia.Typeface('Inter',skia.FontStyle.Bold()),30)
  for(G,F,I,J)in((40,150,1,1),(W-40,150,-1,1),(40,H-120,1,-1),(W-40,H-120,-1,-1)):B.drawLine(G,F,G+I*60,F,paint(C,230,4));B.drawLine(G,F,G,F+J*60,paint(C,230,4))
  if int(t*2)%2==0:B.drawCircle(70,200,11,paint(col('ff3030')))
  B.drawString('REC',92,211,M,paint(C));N=D.get('clock','07:31:02').split(':');S=int(N[2])+int(t);B.drawString(f"{N[0]}:{int(N[1])+S//60:02d}:{S%60:02d}",W-210,211,M,paint(C));P=D.get('zoom_keys');c=1.
  if P:
   c=P[-1][1]if t>=P[-1][0]else P[0][1]
   for(T,e)in zip(P,P[1:]):
    if T[0]<=t<=e[0]:c=T[1]+(e[1]-T[1])*ease((t-T[0])/(e[0]-T[0]))
  B.drawString(f"{D.get("cam","CAM 03")}   x{c:.1f}",60,H-140,M,paint(C));U,V=W/2,H/2
  for(I,J)in((1,0),(-1,0),(0,1),(0,-1)):B.drawLine(U+I*18,V+J*18,U+I*46,V+J*46,paint(C,160,3))
  return O.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
 A=L[...,0]*.3+L[...,1]*.59+L[...,2]*.11;A=np.clip(A*1.9,0,1)**1.15;A=A+_RNG.normal(0,.07,A.shape).astype(np.float32);A[::3]*=.82
 if _VIG is None:Z,a=np.mgrid[0:H,0:W];_VIG=np.clip(1.25-(((a-W/2)/(W*.62))**2+((Z-H/2)/(H*.62))**2),0,1).astype(np.float32)
 A=np.clip(A*_VIG,0,1);g=1.
 if D.get('on'):
  X=t/.9
  if X<1:h=max(2,int(H*max(0,(X-.25)/.75)**2));i=np.zeros_like(A);j=H//2-h//2;i[j:j+h]=1;A=np.where(i>0,np.clip(A*(.4+.6*X)+_RNG.random(A.shape)*(1-X)*.9,0,1),0);g=X
 R=D.get('static_end',0)
 if R and t>d-R:A=_RNG.random(A.shape).astype(np.float32)*.9;o=(np.arange(H)[:,None]+int(t*900))%260<40;A=np.where(o,A*.35,A)
 K=np.stack([A*.22+A**3*.45,A*.92,A*.26+A**3*.4,np.ones_like(A)],-1);K=(np.clip(K,0,1)*255).astype(np.uint8)
 if g<.5:return K
 b=skia.Image.fromarray(K,colorType=skia.kRGBA_8888_ColorType);O=skia.Surface(W,H);B=O.getCanvas();B.drawImage(b,0,0);C=col('d8ffd8');M=skia.Font(skia.Typeface('Inter',skia.FontStyle.Bold()),30);p=skia.Font(skia.Typeface('Inter',skia.FontStyle.Bold()),38)
 for(G,F,I,J)in((40,150,1,1),(W-40,150,-1,1),(40,H-120,1,-1),(W-40,H-120,-1,-1)):B.drawLine(G,F,G+I*60,F,paint(C,230,4));B.drawLine(G,F,G,F+J*60,paint(C,230,4))
 if int(t*2)%2==0:B.drawCircle(70,200,11,paint(col('ff3030')))
 B.drawString('REC',92,211,M,paint(C));N=D.get('clock','02:14:07').split(':');S=int(N[2])+int(t+s.get('_t0',0));B.drawString(f"{N[0]}:{int(N[1])+S//60:02d}:{S%60:02d}",W-210,211,M,paint(C));B.drawString('NV  x4.0',60,H-140,M,paint(C));B.drawRect(skia.Rect(W-150,H-168,W-72,H-138),paint(C,230,3));B.drawRect(skia.Rect(W-146,H-164,W-96,H-142),paint(C));B.drawRect(skia.Rect(W-72,H-160,W-66,H-146),paint(C));U,V=W/2,H/2
 for(I,J)in((1,0),(-1,0),(0,1),(0,-1)):B.drawLine(U+I*18,V+J*18,U+I*46,V+J*46,paint(C,160,3))
 if D.get('label')and t>=D.get('label_at',0):
  q=int((t-D.get('label_at',0))*28)
  for(Y,k)in enumerate(D['label'].split('|')):r=k[:max(0,q-sum(len(A)for A in D['label'].split('|')[:Y]))];B.drawRect(skia.Rect(40,265+Y*58,40+22*len(k)+30,312+Y*58),paint(col('000000'),150));B.drawString(r,55,302+Y*58,p,paint(col('ffffff')))
 return O.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
SUBS={}
def ass_for(text,dur,path,title='',start=.0):
 J=start;I=title;C=dur;Q=text.split();D,A=[],[]
 for K in Q:
  A.append(K)
  if len(' '.join(A))>18 or re.search('[.,!?…]\\**$',K):D.append(A);A=[]
 if A:D.append(A)
 R=sum(len(' '.join(A))for A in D)or 1;S=C;C=max(.5,C-J);F,E=J,[];B=lambda x:f"0:{int(x//60):02d}:{x%60:05.2f}"
 for L in D:M=C*len(' '.join(L))/R;T=re.sub('\\*([^*]+)\\*','{\\\\c&H2A1DE1&}\\1{\\\\c&HFFFFFF&}',' '.join(L).upper());E.append(f"Dialogue: 0,{B(F)},{B(F+M)},Cap,,0,0,0,,{{\\fad(40,0)}}{T}");F+=M
 for G in SUBS.get(path,[]):
  U,V,N=G[:3];O=G[3]if len(G)>3 else'Cap'
  if O=='Small':P=re.sub('\\*([^*]+)\\*','\\1',N)
  else:P=re.sub('\\*([^*]+)\\*','{\\\\c&H2A1DE1&}\\1{\\\\c&HFFFFFF&}',N.upper())
  E.append(f"Dialogue: 0,{B(U)},{B(V)},{O},,0,0,0,,{{\\fad(60,60)}}{P}")
 if I:X=re.sub('\\*([^*]+)\\*','{\\\\c&H2A1DE1&}\\1{\\\\c&HFFFFFF&}',I.upper());E.append(f"Dialogue: 1,{B(0)},{B(S)},Top,,0,0,0,,{X}")
 open(path,'w').write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter ExtraBold,46,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,3,2,2,40,40,280,1
Style: CapHi,Inter ExtraBold,46,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,3,2,8,40,40,170,1
Style: Small,Inter SemiBold,30,&H00E6E6E6,&H00FFFFFF,&H00000000,&H96000000,0,-1,0,0,100,100,0,0,1,2,1,2,60,60,230,1
Style: Top,Inter ExtraBold,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,2,0,1,4,3,8,30,30,70,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""+'\n'.join(E)+'\n')
def render_shot(args):
 D,A,I=args;C=dur_of(A);K=hashlib.md5((json.dumps(A,sort_keys=True)+_SRC).encode()).hexdigest()[:10];B=f"{I}/shot{D:03d}_{K}.mp4"
 if os.path.exists(B):return B
 E=f"{I}/s{D:03d}.ass";SUBS[E]=A.get('subs',[]);ass_for(A.get('say',''),C,E,A.get('title',''),A.get('say_start',0));F=f"ass={E}:fontsdir=/usr/share/fonts/opentype/inter"
 if A.get('fade_in'):F+=f",fade=in:d={A["fade_in"]}"
 if A.get('fade_out'):F+=f",fade=out:st={C-A["fade_out"]}:d={A["fade_out"]}"
 J=B[:-4]+'.tmp.mp4';G=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgba','-s',f"{W}x{H}",'-r',str(FPS),'-i','-','-vf',F,'-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',J],stdin=subprocess.PIPE);L=skia.Surface(W,H)
 for M in range(int(round(C*FPS))):G.stdin.write(frame(A,M/FPS,C,L).tobytes())
 G.stdin.close()
 if G.wait():sys.exit(f"ffmpeg failed on shot {D}")
 os.replace(J,B);return B
LOCS=['cerro_dia','casa_int','rancho','lab','field','fence_forest','deep_forest','farmhouse','snow_woods','cdmx_street']
WHO=['kid','girl','worker','beto','abuelo']
PROPS=['nahuala','sack','stalker','antlered','llorona','carved_post','chupacabras','charro','nahual','lechuza','cadejo','red_eyes','troca','chupa_perch','claw_tips','tv']
def validate(shots):
 A=[]
 for(B,D)in enumerate(shots):
  if D.get('loc','fence_forest')not in LOCS:A.append(f"shot {B}: loc '{D.get("loc")}' not in {LOCS}")
  for F in D.get('chars',[]):
   if F.get('who','kid')not in WHO:A.append(f"shot {B}: who '{F.get("who")}' not in {WHO}")
   G=F.get('expr','neutral');K=[A for(B,A)in G]if isinstance(G,list)else[G]
   for H in K:
    if H not in C.EXPR:A.append(f"shot {B}: expr '{H}' not in {list(C.EXPR)}")
  for I in D.get('props',[]):
   if I.get('type')not in PROPS:A.append(f"shot {B}: prop '{I.get("type")}' not in {PROPS}")
  E=D.get('cam',{})
  if isinstance(E,dict)and'from'not in E and E.get('frame','medium')not in FRAMES:A.append(f"shot {B}: frame '{E.get("frame")}' not in {list(FRAMES)}")
  for J in re.split('(?<=[.,!?…])\\s+',D.get('say','')):
   if J.count('*')%2:A.append(f"shot {B}: *red* markup must open and close inside one phrase: '{J}'")
 if A:sys.exit('INVALID shots.json:\n  '+'\n  '.join(A))
def ambience(dur,path):A=dur;subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i',f"anoisesrc=color=brown:amplitude=0.35:d={A},lowpass=f=300",'-f','lavfi','-i',f"sine=f=55:d={A},volume=0.25,tremolo=f=0.3:d=0.6",'-filter_complex',f"[0][1]amix=2,afade=in:d=1,afade=out:st={max(0,A-1)}:d=1,volume=1.4[a]",'-map','[a]',path],check=True)
def main():
 B=argparse.ArgumentParser();B.add_argument('shots');B.add_argument('out');B.add_argument('--audio');B.add_argument('--preview',action='store_true');B.add_argument('--silent',action='store_true');B.add_argument('--amb',action='store_true');B.add_argument('--jobs',type=int,default=os.cpu_count());A=B.parse_args();E=json.load(open(A.shots));D=E['shots']if isinstance(E,dict)else E;validate(D);C=os.path.splitext(A.out)[0]+'_work';os.makedirs(C,exist_ok=True)
 if A.preview:
  O=skia.Surface(W,H)
  for(P,G)in enumerate(D):I=dur_of(G);Q=frame(G,I*.6,I,O);skia.Image.fromarray(Q,colorType=skia.kRGBA_8888_ColorType).save(f"{C}/prev{P:03d}.png")
  J=min(6,len(D));R=-(-len(D)//J);subprocess.run(['ffmpeg','-y','-v','error','-framerate','1','-i',f"{C}/prev%03d.png",'-vf',f"scale=200:-1,tile={J}x{R}",'-frames:v','1',A.out],check=True);print(A.out);return
 with Pool(A.jobs)as S:T=S.map(render_shot,[(A,B,C)for(A,B)in enumerate(D)],chunksize=1)
 K=f"{C}/list.txt";open(K,'w').write(''.join(f"file '{os.path.abspath(A)}'\n"for A in T));F=sum(dur_of(A)for A in D)
 if not A.audio and A.amb:A.audio=f"{C}/amb.m4a";ambience(F,A.audio)
 L=A.out if not A.audio else f"{C}/silent.mp4";subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',K,'-c','copy',L],check=True)
 if A.audio:subprocess.run(['ffmpeg','-y','-v','error','-i',L,'-i',A.audio,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-shortest',A.out],check=True)
 M=os.path.splitext(A.out)[0]+'_sheet.jpg';N=max(1,int(F*1.5));subprocess.run(['ffmpeg','-y','-v','error','-i',A.out,'-vf',f"fps=1.5,scale=150:-1,tile={min(10,N)}x{-(-N//10)}",'-frames:v','1',M],check=True);print(A.out,f"{F:.1f}s",'check:',M)
if __name__=='__main__':main()
