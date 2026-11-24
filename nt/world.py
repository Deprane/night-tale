import math,random,numpy as np,skia
W,H=720,1280
def col(h):h=h.lstrip('#');return np.array([int(h[A:A+2],16)for A in(0,2,4)],float)
def c4(rgb,a=255):A,B,C=(int(A)for A in np.clip(rgb,0,255));return skia.ColorSetARGB(int(a),A,B,C)
def paint(rgb,a=255,stroke=0,cap=True):
 B=stroke;A=skia.Paint(AntiAlias=True,Color=c4(rgb,a))
 if B:
  A.setStyle(skia.Paint.kStroke_Style);A.setStrokeWidth(B)
  if cap:A.setStrokeCap(skia.Paint.kRound_Cap);A.setStrokeJoin(skia.Paint.kRound_Join)
 return A
PAL=dict(sky_top=col('03050f'),sky_hor=col('1d2b63'),fog=col('141e44'),ground_far=col('17263a'),ground_near=col('0b1612'),trunk=col('2a3142'),canopy=col('121a2a'),canopy_lit=col('22304a'),post=col('4a4550'),wire=col('7a84a0'),house=col('2a2f3f'),roof=col('1e2232'),window=col('ffd36b'),pine=col('1f3a30'),grass=[col('203a2c'),col('2f5240'),col('426e56'),col('5d8a70')])
BASE=dict(PAL)
LIGHT=np.array([-.55,.55,-.6])
LIGHT/=np.linalg.norm(LIGHT)
FOG_D=.045
def fog(rgb,z,k=1.):A=1-math.exp(-max(z,0)*PAL.get('fogd',FOG_D)*k);return rgb*(1-A)+PAL['fog']*A
class Cam:
 def __init__(A,pos,yaw,pitch,fov=45,roll=.0):C=pitch;B=yaw;A.p=np.array(pos,float);A.yaw,A.pitch,A.roll=B,C,roll;A.f=H/2/math.tan(math.radians(fov)/2);D,E,F,J=math.cos(B),math.sin(B),math.cos(C),math.sin(C);G=np.array([E*F,J,D*F]);I=np.array([D,0,-E]);K=np.cross(G,I);A.M=np.stack([I,K,G])
 def to_cam(A,P):return(np.asarray(P,float)-A.p)@A.M.T
 def proj(A,C):C=np.atleast_2d(C);B=np.maximum(C[:,2],.001);return np.stack([W/2+A.f*C[:,0]/B,H/2-A.f*C[:,1]/B],1),C[:,2]
 def horizon_y(A):return H/2+A.f*math.tan(A.pitch)
def prism(cx,cz,r,h,n,rot=.0,y0=.0,cap=True):
 D=[rot+2*math.pi*A/n for A in range(n)];B=[np.array([cx+r*math.cos(A),y0,cz+r*math.sin(A)])for A in D];C=[A+[0,h,0]for A in B];A=[[B[A],B[(A+1)%n],C[(A+1)%n],C[A]]for A in range(n)]
 if cap:A.append(C[::-1])
 return A
def gable_house(cx,cz,w,d,h,rh):G=rh;F=cz;B,C,D,E=cx-w/2,cx+w/2,F-d/2,F+d/2;A=lambda x,y,z:np.array([x,y,z],float);H=[[A(B,0,D),A(C,0,D),A(C,h,D),A(B,h,D)],[A(C,0,E),A(B,0,E),A(B,h,E),A(C,h,E)],[A(B,0,E),A(B,0,D),A(B,h,D),A(B,h,E)],[A(C,0,D),A(C,0,E),A(C,h,E),A(C,h,D)],[A(B,h,D),A(C,h,D),A(C,h+G,F),A(B,h+G,F)],[A(C,h,E),A(B,h,E),A(B,h+G,F),A(C,h+G,F)],[A(B,h,D),A(B,h+G,F),A(B,h,E)],[A(C,h,E),A(C,h+G,F),A(C,h,D)]];return H
class World:
 def __init__(A,loc='fence_forest',seed=1):B=random.Random(seed);A.r=B;A.solids=[];A.blobs=[];A.wires=[];A.glows=[];A.windows=[];A.moon=None;A.stars=[(B.random(),B.random(),B.uniform(.7,1.9),B.uniform(.35,1))for A in range(110)];A.grass_rects=[];A.decals=[];A.wins2=[];A.glass=[];A.open=None;A.sprites=[];A.door=None;A.swing=None;A.snow=False;A.t=.0;PAL.clear();PAL.update(BASE);getattr(A,'loc_'+loc)(B);A.pal=dict(PAL);A._grass(B)
 def tree(A,x,z,r):
  C=r.uniform(.18,.4);B=r.uniform(9,14);A.solids.append((prism(x,z,C,B,6,r.random()),PAL['trunk']*r.uniform(.75,1.1)))
  for F in range(r.randint(3,5)):D=r.uniform(1.6,3.);E=[r.uniform(.78,1.05)for A in range(9)];A.blobs.append((x+r.uniform(-1.6,1.6),B*r.uniform(.55,.95),z+r.uniform(-1,1),D,E))
 def forest(A,r,x0,x1,z0,z1,n):
  for B in range(n):A.tree(r.uniform(x0,x1),r.uniform(z0,z1),r)
 def fence(B,r,x0,z0,x1,z1,step=2.6):
  H=math.hypot(x1-x0,z1-z0);C=int(H/step);A=[]
  for I in range(C+1):D=I/C;E=x0+(x1-x0)*D+r.uniform(-.05,.05);F=z0+(z1-z0)*D;J=r.uniform(1.05,1.3);B.solids.append((prism(E,F,.11,J,4,math.pi/4+r.uniform(-.2,.2)),PAL['post']*r.uniform(.85,1.1)));A.append((E,F))
  for G in(.55,.95):
   for((K,L),(M,N))in zip(A,A[1:]):B.wires.append((np.array([K,G,L]),np.array([M,G+r.uniform(-.05,.05),N])))
 def house(B,x,z,lit=True):
  B.solids.append((gable_house(x,z,7,5,3.2,2.2),PAL['house']))
  if lit:A=z-2.5-.02;B.windows.append([np.array(A,float)for A in((x+.8,1.3,A),(x+1.8,1.3,A),(x+1.8,2.3,A),(x+.8,2.3,A))]);B.glows.append((x+1.3,1.8,A-.1,2.2,PAL['window']))
 def pine(E,x,z,r):
  E.solids.append((prism(x,z,.2,1.2,6,r.random()),PAL['trunk']));B=r.uniform(6,10);C=B*.32;D=.8
  for I in range(3):A=7;F=r.random();G=[np.array([x+C*math.cos(F+2*math.pi*B/A),D,z+C*math.sin(F+2*math.pi*B/A)])for B in range(A)];H=np.array([x,D+B*.5,z]);E.solids.append(([[G[B],H,G[(B+1)%A]]for B in range(A)],PAL['pine']*r.uniform(.85,1.15)));D+=B*.25;C*=.7
 def cabin(B,x,z,glow=1.,roof=None):
  C=gable_house(x,z,6,5,3.,2.)
  if roof is None:B.solids.append((C,PAL['house']))
  else:
   B.solids.append((C[:4]+C[6:],PAL['house']));E=[[A+np.array([0,.05,0])for A in A]for A in C[4:6]]
   for D in E:F=np.mean(D,0);D[:]=[F+(A-F)*1.12 for A in D]
   B.solids.append((E,roof))
  A=z-2.5-.02;B.windows.append([np.array(A,float)for A in((x-.6,0,A),(x+.4,0,A),(x+.4,2.,A),(x-.6,2.,A))]);B.windows.append([np.array(A,float)for A in((x+1.3,1.2,A),(x+2.3,1.2,A),(x+2.3,2.1,A),(x+1.3,2.1,A))]);B.glows+=[(x-.1,1.,A-.1,3.*glow,PAL['window']),(x+1.8,1.6,A-.1,1.8*glow,PAL['window'])]
 def box(H,x0,x1,y0,y1,z0,z1,colr):G=y0;F=z1;E=z0;D=x1;C=x0;B=y1;A=lambda x,y,z:np.array([x,y,z],float);H.solids.append(([[A(C,G,E),A(D,G,E),A(D,B,E),A(C,B,E)],[A(D,G,F),A(C,G,F),A(C,B,F),A(D,B,F)],[A(C,G,F),A(C,G,E),A(C,B,E),A(C,B,F)],[A(D,G,E),A(D,G,F),A(D,B,F),A(D,B,E)],[A(C,B,E),A(D,B,E),A(D,B,F),A(C,B,F)]],colr))
 def streetlamp(B,x,z,side,flicker=False):B.solids.append((prism(x,z,.07,5.2,6),col('3a3a42')));A=x-side*1.1;B.box(min(x,A),max(x,A),5.1,5.2,z-.05,z+.05,col('3a3a42'));B.box(A-.25,A+.25,4.95,5.12,z-.15,z+.15,col('ffcf86'));B.glows.append((A,4.9,z,1.5,col('ff9a3c'),flicker));B.decals.append((A,z,1.3,1.3,0,col('2a221e')))
 def vocho(A,x,z,c):A.box(x-.8,x+.8,.25,.9,z-1.9,z+1.9,c);A.box(x-.65,x+.65,.9,1.4,z-.9,z+.7,c*.9);A.box(x-.82,x+.82,.0,.28,z-1.5,z+1.5,col('111114'))
 def loc_cdmx_street(B,r):
  PAL.update(sky_top=col('07060f'),sky_hor=col('3d2a45'),fog=col('2a2236'),ground_far=col('2c2a36'),ground_near=col('17161c'),window=col('ffc66b'));L=[col(A)for A in('b5543c','d09a3a','3f7f7a','b0607a','6a6fa8','c8b89a','8a4a3a')]
  for C in(-1,1):
   B.box(C*3. if C>0 else-5.6,5.6 if C>0 else-3.,0,.18,-10,120,col('3b3a42'));A=-10
   while A<110:
    H=r.uniform(5,11);I=r.uniform(5,13);D=C*5.6;M=r.choice(L)*r.uniform(.45,.6);B.box(min(D,D+C*8),max(D,D+C*8),0,I,A,A+H-.2,M);E=D+C*-.02
    for F in np.arange(1.2,I-1,2.6):
     for G in np.arange(A+.9,A+H-1,2.):N=r.random()<.3;O=col('ffc66b')*r.uniform(.8,1.05)if N else col('15141c');B.wins2.append(([np.array(A,float)for A in((E,F,G),(E,F,G+1.),(E,F+1.4,G+1.),(E,F+1.4,G))],O))
    A+=H
  for A in np.arange(4,100,14):B.streetlamp(-3.3,A,-1,flicker=abs(A-32)<3);B.streetlamp(3.3,A+7,1)
  for J in range(30):A=r.uniform(0,90);K=r.uniform(5.5,7.5);B.wires.append((np.array([-5.6,K,A]),np.array([5.6,K+r.uniform(-.6,.6),A+r.uniform(-4,4)])))
  B.vocho(2.1,20,col('2f8a4a'));B.vocho(-2.1,41,col('d8d2c0'));B.vocho(2.1,52,col('c43c2c'))
  for J in range(60):B.decals.append((0,J*3.,.08,.7,0,col('6a6550')))
 def loc_lab(A,r):
  PAL.update(sky_top=col('06070b'),sky_hor=col('0c0d12'),fog=col('0b0c11'),ground_far=col('15171e'),ground_near=col('08090c'));A.box(-20,40,0,9,8.5,9,col('16181f'))
  for I in range(-3,9):
   B=I*3.2;C,D=B-1.45,B+1.45;A.box(C,D,0,.35,4.5,8.4,col('23262e'));A.box(C-.15,C,0,3.6,4.4,8.4,col('3a3d48'));A.box(D,D+.15,0,3.6,4.4,8.4,col('3a3d48'));A.box(C-.15,D+.15,3.4,3.8,4.4,8.4,col('34373f'));A.box(C,D,3.,3.4,8.,8.4,col('1a1c22'));A.box(B-.9,B+.9,3.32,3.38,6.,6.4,col('e8eeff'));A.glows.append((B,3.1,6.2,1.1,col('c8d8ff')));A.decals.append((B,6.2,.9,.7,0,col('3a4050')))
   for E in range(8):A.decals.append((C+.2+E*.36,4.1,.1,.22,.6,col('d8a91c')if E%2==0 else col('15151a')))
   for H in(C-.07,D+.07):A.glows.append((H,3.55,4.35,.7,col('ff2a2a'),r.random()<.5));A.box(H-.06,H+.06,3.5,3.62,4.3,4.4,col('ff3b3b'))
   for F in(C-.15,D):
    for E in range(6):G=.4+E*.5;A.wins2.append(([np.array(A,float)for A in((F,G,4.39),(F+.15,G,4.39),(F+.15,G+.25,4.39),(F,G+.25,4.39))],col('d8a91c')))
   A.wins2.append(([np.array(A,float)for A in((B-.5,3.5,4.38),(B+.5,3.5,4.38),(B+.5,3.7,4.38),(B-.5,3.7,4.38))],col('9a1c1c')));A.glass.append(([np.array(A,float)for A in((C,.35,4.5),(D,.35,4.5),(D,3.4,4.5),(C,3.4,4.5))],col('8fb6d8'),22))
 def tree_at(B,x,z,r,y0=.0,rad=None,h=None):
  A=rad;A=A or r.uniform(.2,.4);h=h or r.uniform(8,13);B.solids.append((prism(x,z,A,h,6,r.random(),y0=y0),PAL['trunk']*r.uniform(.8,1.1)))
  for D in range(r.randint(4,6)):C=r.uniform(1.8,3.);B.blobs.append((x+r.uniform(-1.8,1.8),y0+h*r.uniform(.6,1.),z+r.uniform(-1,1),C,[r.uniform(.75,1.05)for A in range(9)]))
 def quad_in(B,pts,colr,inside):
  A=[np.array(A,float)for A in pts];C=np.cross(A[1]-A[0],A[2]-A[0])
  if np.dot(C,np.array(inside,float)-np.mean(A,0))<0:A=A[::-1]
  B.solids.append(([A],colr))
 def loc_casa_int(A,r):
  PAL.update(sky_top=col('0d0a08'),sky_hor=col('1a1410'),fog=col('140f0b'),ground_far=col('4a382a'),ground_near=col('3a2c20'),fogd=.01);B=0,1.5,2;I,C=col('8a6644'),col('6e5036');A.quad_in([(-3,0,6),(3,0,6),(3,3,6),(-3,3,6)],I,B);A.quad_in([(-3,0,-2),(-3,0,6),(-3,3,6),(-3,3,-2)],C,B);A.quad_in([(3,0,-2),(3,0,6),(3,3,6),(3,3,-2)],C,B);A.quad_in([(-3,3,-2),(3,3,-2),(3,3,6),(-3,3,6)],col('3a2a1e'),B)
  for D in range(6):A.box(-3,3,2.9,3.,-1.5+D*1.4,-1.3+D*1.4,col('4a3424'))
  A.wins2.append(([np.array(A,float)for A in((-1,1,5.97),(.6,1,5.97),(.6,2.1,5.97),(-1,2.1,5.97))],col('0c1426')))
  for(E,F,G,H)in((-1.08,.95,.68,1.),(-1.08,2.1,.68,2.15),(-1.08,.95,-1.,2.15),(.6,.95,.68,2.15),(-.24,1,-.16,2.1),(-1,1.52,.6,1.58)):A.wins2.append(([np.array(A,float)for A in((E,F,5.95),(G,F,5.95),(G,H,5.95),(E,H,5.95))],col('3a2818')))
  A.wins2.append(([np.array(A,float)for A in((2.97,0,2),(2.97,0,3),(2.97,2.1,3),(2.97,2.1,2))],col('4e3622')));A.wins2.append(([np.array(A,float)for A in((2.95,.95,2.15),(2.95,.95,2.25),(2.95,1.05,2.25),(2.95,1.05,2.15))],col('c9b27a')));A.box(-2.9,-2.4,0,1.8,2.5,4.5,col('6e5236'));A.box(-2.95,-2.4,.9,.95,2.5,4.5,col('4a3424'));A.box(-2.95,-2.4,1.4,1.45,2.5,4.5,col('4a3424'));A.glows.append((0,2.6,2.2,2.2,col('ff8a2a'),True));A.glows.append((-.2,1.5,5.8,1.6,col('6f8fd0')));A.box(-.06,.06,2.5,2.7,2.14,2.26,col('fff0c8'));A.decals.append((-.2,3.6,1.6,1.1,0,col('7a3a2a')));A.stars=[];A.aged_wall(r,'z',5.97,(-3,3),(0,3),col('8a6644'));A.aged_wall(r,'x',-2.97,(-2,6),(0,3),col('6e5036'));A.aged_wall(r,'x',2.97,(3.2,6),(0,3),col('6e5036'));A.aged_wall(r,'x',2.97,(-2,1.8),(0,3),col('6e5036'));A.old_door(r,2.97,2.,3.,2.1);A.wins2.append(([np.array(A,float)for A in((2.955,1.,3.55),(2.955,1.,4.85),(2.955,2.1,4.85),(2.955,2.1,3.55))],col('3a2818')));A.wins2.append(([np.array(A,float)for A in((2.95,1.06,3.62),(2.95,1.06,4.78),(2.95,2.04,4.78),(2.95,2.04,3.62))],col('0e1830')));A.wins2.append(([np.array(A,float)for A in((2.945,1.06,4.175),(2.945,1.06,4.225),(2.945,2.04,4.225),(2.945,2.04,4.175))],col('3a2818')));A.wins2.append(([np.array(A,float)for A in((2.945,1.53,3.62),(2.945,1.53,4.78),(2.945,1.57,4.78),(2.945,1.57,3.62))],col('3a2818')))
 def _wq(B,ax,c,pts2,colr,eps=.0):
  if ax=='z':A=[np.array([A,B,c-eps],float)for(A,B)in pts2]
  else:A=[np.array([c-math.copysign(eps,c),B,A],float)for(A,B)in pts2]
  B.wins2.append((A,colr))
 def aged_wall(H,r,ax,c,ur,vr,base):
  (B,C),(N,O)=ur,vr
  for K in range(int((C-B)*1.6)):D,E=r.uniform(B+.3,C-.3),r.choice([r.uniform(N+.1,.6),r.uniform(2.1,O-.1),r.uniform(.6,2.1)]);P=r.uniform(.15,.45);A=[(D+math.cos(A)*P*r.uniform(.6,1.2),E+math.sin(A)*P*r.uniform(.5,1.1))for A in np.linspace(0,2*math.pi,10)[:-1]];H._wq(ax,c,A,base*r.uniform(.45,.62),.004)
  for K in range(int((C-B)*.5)):
   D,E=r.uniform(B+.4,C-.4),r.uniform(.3,2.4);Q,R=r.uniform(.25,.45),r.uniform(.18,.32);A=[(D+math.cos(A)*Q*r.uniform(.75,1.1),E+math.sin(A)*R*r.uniform(.75,1.1))for A in np.linspace(0,2*math.pi,11)[:-1]];H._wq(ax,c,A,col('5a3e2a'),.008)
   for S in range(-2,3):
    for T in range(-2,3):
     F,G=D+T*.2+(.1 if S%2 else 0),E+S*.1
     if abs(F-D)<Q*.75 and abs(G-E)<R*.7:H._wq(ax,c,[(F-.085,G-.04),(F+.085,G-.04),(F+.085,G+.04),(F-.085,G+.04)],col('7a5236')*r.uniform(.9,1.1),.012)
  for K in range(int((C-B)*1.3)):
   L,M=r.uniform(B+.2,C-.2),r.uniform(N+.2,O-.3);A=[(L,M)]
   for K in range(r.randint(4,8)):L+=r.uniform(-.12,.12);M+=r.uniform(-.22,-.06);A.append((L,M))
   for(I,J)in zip(A,A[1:]):H._wq(ax,c,[(I[0]-.013,I[1]),(I[0]+.013,I[1]),(J[0]+.013,J[1]),(J[0]-.013,J[1])],col('1a0e06'),.015)
 def old_door(E,r,x,z0,z1,h):
  C=z1;A=z0;I=5;J=(C-A)/I
  for F in range(I):
   K,L=A+F*J+.01,A+(F+1)*J-.01;E._wq('x',x,[(K,0),(L,0),(L,h-r.uniform(0,.05)),(K,h)],col('5a3e26')*r.uniform(.8,1.15),.006)
   for M in range(3):D=r.uniform(K+.02,L-.02);G=r.uniform(.1,1.5);E._wq('x',x,[(D,G),(D+.006,G),(D+.006+r.uniform(-.02,.02),G+r.uniform(.2,.5)),(D,G+.3)],col('3a2614'),.01)
  for F in range(1,I):D=A+F*J;E._wq('x',x,[(D-.008,0),(D+.008,0),(D+.008,h),(D-.008,h)],col('0e0805'),.011)
  for B in(.35,1.7):E._wq('x',x,[(A+.03,B),(C-.03,B),(C-.03,B+.12),(A+.03,B+.12)],col('4a321c'),.014)
  E._wq('x',x,[(A+.05,.47),(C-.08,1.62),(C-.08,1.72),(A+.05,.57)],col('4a321c'),.016)
  for B in(.33,1.68):
   E._wq('x',x,[(A-.02,B),(A+.32,B+.02),(A+.32,B+.14),(A-.02,B+.16)],col('3a2a22'),.02)
   for H in range(3):E._wq('x',x,[(A+.05+H*.1,B+.06),(A+.08+H*.1,B+.06),(A+.08+H*.1,B+.09),(A+.05+H*.1,B+.09)],col('6a5a4a'),.022)
  E._wq('x',x,[(C-.2,.95),(C-.1,.95),(C-.1,1.08),(C-.2,1.08)],col('7a6a50'),.022)
 def loc_rancho(A,r):
  import char as X;PAL.update(sky_top=col('05070f'),sky_hor=col('1a2140'),fog=col('121830'),ground_far=col('2a2a2e'),ground_near=col('15130f'),house=col('7e6a56'),window=col('b8894a'),trunk=col('2a241f'),canopy=col('0c100d'),canopy_lit=col('1e2a20'),fogd=.012);A.moon=math.radians(25),math.radians(30);I=lambda z:max(.0,(z-24)*.5)
  for J in range(14):M,N=24+J*4,28+J*4;A.solids.append(([[np.array([-70,I(N),N]),np.array([70,I(N),N]),np.array([70,I(M),M]),np.array([-70,I(M),M])]],col('1a1d16')))
  for Y in range(280):B=r.uniform(23,78);C=r.uniform(-50,50);A.tree_at(C,B,r,y0=I(B)-.2)
  for Y in range(260):B=r.uniform(23,70);C=r.uniform(-45,45);A.blobs.append((C,I(B)+r.uniform(.4,1.),B,r.uniform(.8,1.6),[r.uniform(.7,1.05)for A in range(9)]))
  for(e,f)in((2e1,-.4),(21.,-2.8),(19.6,1.8),(21.8,.9),(19.,-4.2),(23.5,-5.),(24.5,1.5),(22.5,-8.),(17.5,-6.5),(25.5,-2.5)):A.tree_at(e,f,r)
  for Y in range(20):C=r.choice([-1,1])*r.uniform(9,30);B=r.uniform(8,24);A.tree_at(C,B,r)
  A.cabin(.4,20,glow=.35,roof=col('c07a52'));D=17.495
  for J in range(9):O=.25+J*.32;A.wins2.append(([np.array(A,float)for A in((-2.6,O,D),(3.4,O,D),(3.4,O+.035,D),(-2.6,O+.035,D))],col('6a5644')))
  A.wins2.append(([np.array(A,float)for A in((-2.6,2.65,D),(3.4,2.65,D),(3.4,3.,D),(-2.6,3.,D))],col('4a3a2e')));A.wins2.append(([np.array(A,float)for A in((-2.6,0,D),(3.4,0,D),(3.4,.35,D),(-2.6,.35,D))],col('5a4634')))
  for(K,Z)in((-15,12),(14,15)):A.solids.append((gable_house(K,Z,5,4,2.6,1.6),PAL['house']*.8));D=Z-2.02;A.wins2.append(([np.array(A,float)for A in((K+.5,1,D),(K+1.3,1,D),(K+1.3,1.8,D),(K+.5,1.8,D))],col('ffc46a')));A.glows.append((K+.9,1.4,D-.1,1.2,col('ffc46a')))
  for J in range(60):P=J/59;C=.4-12*P**1.3;B=17-13*P;A.decals.append((C,B,1.4,.9,.5*P,col('5a4a38')))
  for(g,h,i)in((1.55,-2.1,.32),(-3.9,-1.,.3)):A.solids.append((prism(g,h,i,14,7,r.random()),PAL['trunk']*.8))
  for(C,B,Q,L)in((17.,-1.,'nopal',2.6),(18.3,.2,'nopal',1.5),(16.,-2.2,'maguey',1.3),(18.6,-1.9,'nopal',1.6),(3,14,'nopal',1.1),(-3.5,15,'maguey',1.),(4.5,19,'nopal',1.2),(-5.5,20,'nopal',1.3),(-8,9,'maguey',1.2)):A.sprites.append(dict(pos=[C,0,B],draw=getattr(X,Q)(L,r.random()),shadow=.4*L))
  F,G=.737,-.676;a=math.hypot(F,G);F,G=F/a,G/a;b,c=-G,F;R=math.atan2(F,G)
  for S in range(30):
   d=.11 if S%2 else-.11;T,U=2.6+F*S*.6+b*d,12.+G*S*.6+c*d;A.decals.append((T,U,.06,.08,R,col('060403')));A.decals.append((T+F*.15,U+G*.15,.085,.07,R,col('060403')))
   for V in(-1,0,1):A.decals.append((T+F*.29+b*V*.06,U+G*.29+c*V*.06,.018,.1,R+V*.3,col('030202')))
  import random as j;E=j.Random(77)
  def W(x,z):C,D,F,G=.3,16.9,13.8,2.;A,B=F-C,G-D;E=max(0,min(1,((x-C)*A+(z-D)*B)/(A*A+B*B)));return math.hypot(x-C-A*E,z-D-B*E)>2.2 and math.hypot(x-17,z+1)>3.2 and not(-4<x<5 and z>15)
  H=0
  while H<70:
   C,B=E.uniform(-26,34),E.uniform(-30,15)
   if W(C,B)and math.hypot(C-7,B-9)>6:A.tree_at(C,B,r);H+=1
  H=0
  while H<90:
   C,B=E.uniform(-18,30),E.uniform(-20,16)
   if W(C,B):A.blobs.append((C,E.uniform(.3,.7),B,E.uniform(.5,1.2),[E.uniform(.7,1.05)for A in range(9)]));H+=1
  H=0
  while H<45:
   C,B=E.uniform(-16,28),E.uniform(-16,16)
   if W(C,B):Q=E.choice(['nopal','nopal','maguey']);L=E.uniform(.9,1.8);A.sprites.append(dict(pos=[C,0,B],draw=getattr(X,Q)(L,E.random()),shadow=.4*L));H+=1
  A.grass_rects=[(-26,34,-30,17.2,.12),(-15,-3.2,17.2,24,.12),(4.,15,17.2,24,.12)]
 def loc_fence_forest(A,r):A.forest(r,-30,-3.5,-5,90,150);A.forest(r,8,40,45,90,50);A.fence(r,-2.2,-6,-2.2,80);A.grass_rects=[(-3.5,25,-6,70,1.)]
 def loc_deep_forest(A,r):A.forest(r,-30,30,-6,70,260);A.solids=[A for A in A.solids if abs(A[0][0][0][0])>1.8];A.blobs=[A for A in A.blobs if abs(A[0])>1. or A[1]>7];A.grass_rects=[(-12,12,-6,40,.6)]
 def loc_snow_woods(C,r):
  PAL.update(sky_top=col('070b1c'),sky_hor=col('34466f'),fog=col('3e4f75'),ground_far=col('6c7ea6'),ground_near=col('aebcd8'),trunk=col('3a2e2a'),pine=col('22403f'),house=col('4a3a32'),window=col('ffc35c'))
  for E in range(170):
   D=r.uniform(-30,30);A=r.uniform(-5,80)
   if abs(D)>2.6 and not(abs(D-.5)<6 and 28<A<40):C.pine(D,A,r)
  C.cabin(.5,34)
  for B in range(90):A=-3+B*.35;C.decals.append((-.35+(.09 if B%2 else-.09),A,.06,.12,0,col('7d8db0')))
  for B in range(24):A=-2+B*1.35;C.decals.append((.55+(.18 if B%2 else-.18),A,.13,.3,.15*(-1)**B,col('5d6c90')))
  C.snow=True
 def loc_cerro_dia(C,r):
  PAL.update(sky_top=col('7f8992'),sky_hor=col('b9c0c6'),fog=col('aeb6bd'),ground_far=col('5a5c48'),ground_near=col('4b4a3a'),trunk=col('3a3328'),canopy=col('34402f'),canopy_lit=col('4d5a44'),pine=col('2f3b2b'),grass=[col('4a5038'),col('586046'),col('666b4e'),col('73775a')],fogd=.007);C.moon=None;C.stars=[];D=lambda z:max(.0,(z-8)*.55)
  for G in range(16):H,I=8+G*4,12+G*4;C.solids.append(([[np.array([-70,D(I),I]),np.array([70,D(I),I]),np.array([70,D(H),H]),np.array([-70,D(H),H])]],col(('545642','5a5a44','4f5240','57563f')[G%4])))
  F,E=.0,28.;P=D(E)
  for J in range(420):
   A=r.uniform(6,70);B=r.uniform(-45,45)
   if abs(B-F)<4.2 and abs(A-E)<3.2:continue
   if abs(B)<2.2+A*.12 and A<E:continue
   if A<9 and abs(B)<9:continue
   C.tree_at(B,A,r,y0=D(A)-.2,h=r.uniform(6,11))
  for J in range(300):
   A=r.uniform(5,60);B=r.uniform(-40,40)
   if abs(B-F)<3.5 and abs(A-E)<3 or abs(B)<1.5+A*.1 and A<E:continue
   C.blobs.append((B,D(A)+r.uniform(.3,.8),A,r.uniform(.6,1.3),[r.uniform(.7,1.05)for A in range(9)]))
  for J in range(520):
   A=r.uniform(4,34);B=r.uniform(-18,18)
   if abs(B-F)<2.6 and abs(A-E)<1.5:continue
   C.blobs.append((B,D(A)+r.uniform(.05,.3),A,r.uniform(.18,.55),[r.uniform(.6,1.)for A in range(9)]))
  for J in range(70):
   A=r.uniform(5,40);B=r.uniform(-16,16)
   if abs(B-F)<2.6 and abs(A-E)<1.5:continue
   C.solids.append((prism(B,A,r.uniform(.25,.7),r.uniform(.2,.6),r.randint(4,6),r.random(),y0=D(A)-.1),col('6c695c')*r.uniform(.85,1.1)))
  for(L,M)in((-3.2,1.5),(3.6,2.2)):C.tree_at(L,M,r,rad=.3,h=12)
  K=E-.6;N=D(K)
  for G in range(10):O=r.choice((-1,1))*r.uniform(2.2,3.6);C.blobs.append((F+O,N+.15,K-r.uniform(.1,1.),r.uniform(.18,.38),[r.uniform(.8,1.)for A in range(9)]))
  C.grass_rects=[(-20,20,-8,8,.5)]
 def loc_field(A,r):A.forest(r,-60,60,55,95,120);A.moon=math.radians(-8),math.radians(22);A.grass_rects=[(-20,20,-6,60,1.)]
 def loc_farmhouse(A,r):A.forest(r,-60,60,60,95,90);A.house(4,40);A.fence(r,-14,10,14,10,3.);A.grass_rects=[(-15,15,-6,55,1.)]
 def _grass(A,r):
  D,E,F,G=[],[],[],[]
  for(H,I,J,O,P)in A.grass_rects:
   for B in np.arange(J,O,2.):
    K=B+1-J;Q=P*(14 if K<12 else 7 if K<25 else 3);R=int(Q*(I-H)*2.)
    for T in range(R):L,M=r.uniform(H,I),r.uniform(B,B+2);C=r.uniform(.22,.7)*(1. if r.random()>.15 else 1.5);N=r.uniform(-1.,1.);S=r.uniform(.035,.07);D.append((L,M,math.cos(N),math.sin(N)));E.append((L+r.uniform(-.3,.3)*C,C,M+r.uniform(-.2,.2)*C));F.append(S);G.append(r.randrange(4))
  A.gb=np.array(D);A.gt=np.array(E);A.gw=np.array(F);A.gc=np.array(G)
 def draw(B,cv,cam,billboards=()):
  I=cv;A=cam;PAL.clear();PAL.update(B.pal);Q=A.horizon_y();AG=skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0,0),skia.Point(0,max(Q,1))],[c4(PAL['sky_top']),c4(PAL['sky_hor'])]));I.drawRect(skia.Rect(0,0,W,H),AG)
  for(U,j,AH,AI)in B.stars:
   V=(U*W*3-A.yaw*A.f)%(W*3)-W;k=j*(Q-80)if Q>80 else-10
   if 0<=V<W:I.drawCircle(V,k,AH,paint(col('ffffff'),255*AI))
  if B.moon:
   u,l=B.moon;L=np.array([math.sin(u)*math.cos(l),math.sin(l),math.cos(u)*math.cos(l)]);v=A.to_cam(A.p+L*1000)
   if v[2]>0:m=A.proj(v)[0][0];n=skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(*m),260,[skia.ColorSetARGB(120,200,212,255),skia.ColorSetARGB(0,200,212,255)]));I.drawCircle(*m,260,n);I.drawCircle(*m,11,paint(col('f4f6ff')))
  n=skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0,Q),skia.Point(0,H)],[c4(PAL['ground_far']),c4(PAL['ground_near'])]));I.drawRect(skia.Rect(0,Q,W,H),n)
  for(AJ,D,N,w,R,o)in B.decals:
   x,y=math.cos(R),math.sin(R);AK=[[AJ+N*math.cos(A)*x+w*math.sin(A)*y,.01,D-N*math.cos(A)*y+w*math.sin(A)*x]for A in np.linspace(0,2*math.pi,9)[:-1]];X=A.to_cam(AK)
   if(X[:,2]<.1).any()or X[:,2].mean()>60:continue
   z,_=A.proj(X);Y=skia.Path();Y.moveTo(*z[0])
   for C in z[1:]:Y.lineTo(*C)
   Y.close();I.drawPath(Y,paint(fog(o,X[:,2].mean())))
  E=[]
  for(A0,o)in B.solids:
   AL=np.mean([np.mean(A,0)for A in A0],0);D=A.to_cam(AL)[2]
   if D>-3:E.append((D,'solid',(A0,o)))
  for A1 in B.blobs:
   D=A.to_cam(A1[:3])[2]
   if D>.5:E.append((D,'blob',A1))
  for N in B.wires:
   D=A.to_cam((N[0]+N[1])/2)[2]
   if D>.2:E.append((D,'wire',N))
  for C in B.windows:E.append((A.to_cam(np.mean(C,0))[2]-.3,'window',C))
  for(C,S)in B.wins2:
   D=A.to_cam(np.mean(C,0))[2]-.05
   if D>.2:E.append((D,'win2',(C,S)))
  for(C,S,AM)in B.glass:
   D=A.to_cam(np.mean(C,0))[2]-.02
   if D>.2:E.append((D,'glass',(C,S,AM)))
  if B.door:
   O,A2,A3,Z,p=B.door
   if p>0:C=[np.array(A,float)for A in((O,0,Z-.03),(O+(A2-O)*p,0,Z-.03),(O+(A2-O)*p,A3,Z-.03),(O,A3,Z-.03))];E.append((A.to_cam(np.mean(C,0))[2]-.45,'win2',(C,col('3a2a1e'))))
  if B.swing:
   AN,G,T,a,R=B.swing
   if R>.5:
    F=AN-.03;C=[np.array(A,float)for A in((F,0,G),(F,0,T),(F,a,T),(F,a,G))];E.append((A.to_cam(np.mean(C,0))[2]-.1,'win2',(C,col('16213d'))))
    for(AO,(A4,A5,S))in enumerate(((0,.55,'0c1424'),(.55,.62,'22304e'))):C=[np.array(A,float)for A in((F+.001,A4,G),(F+.001,A4,T),(F+.001,A5,T),(F+.001,A5,G))];E.append((A.to_cam(np.mean(C,0))[2]-.11-AO*.001,'win2',(C,col(S))))
    J=T-G;K=math.radians(R)
    for q in range(5):A6,A7=q/5,(q+1)/5-.012;M=F-J*A6*math.sin(K),G+J*A6*math.cos(K);b=F-J*A7*math.sin(K),G+J*A7*math.cos(K);C=[np.array(A,float)for A in((M[0],0,M[1]),(b[0],0,b[1]),(b[0],a,b[1]),(M[0],a,M[1]))];E.append((A.to_cam(np.mean(C,0))[2]-.05,'win2',(C,col(('4e3622','563c25','4a3320','523924','4c3421')[q]))))
    for c in(.35,1.7):d=F-J*.97*math.sin(K),G+J*.97*math.cos(K);e=F-J*.03*math.sin(K),G+J*.03*math.cos(K);C=[np.array(A,float)for A in((e[0],c,e[1]),(d[0],c,d[1]),(d[0],c+.12,d[1]),(e[0],c+.12,e[1]))];E.append((A.to_cam(np.mean(C,0))[2]-.06,'win2',(C,col('3a2616'))))
  for A8 in B.glows:E.append((A.to_cam(A8[:3])[2]-.1,'glow',A8))
  for A9 in list(billboards)+B.sprites:
   D=A.to_cam(A9['pos'])[2]
   if D>.15:E.append((D,'bb',A9))
  if len(B.gb):
   M=np.stack([B.gb[:,0],np.zeros(len(B.gb)),B.gb[:,1]],1);AA=np.stack([B.gb[:,2],np.zeros(len(B.gb)),B.gb[:,3]],1)*B.gw[:,None];AB,AC,AD=A.to_cam(M-AA),A.to_cam(M+AA),A.to_cam(B.gt);r=AB[:,2];s=(r>.25)&(AC[:,2]>.25)&(AD[:,2]>.25)&(r<70);f,g,h=A.proj(AB)[0],A.proj(AC)[0],A.proj(AD)[0];s&=(np.maximum(np.maximum(f[:,0],g[:,0]),h[:,0])>-20)&(np.minimum(np.minimum(f[:,0],g[:,0]),h[:,0])<W+20);s&=np.minimum(np.minimum(f[:,1],g[:,1]),h[:,1])<H+10;AE=np.nonzero(s)[0];P=[0,1,2,3,4.5,6,8,11,15,20,27,36,48,70];AF=np.digitize(r[AE],P)
   for i in np.unique(AF):AP=AE[AF==i];E.append((P[min(i,len(P)-1)],'grass',(AP,f,g,h,(P[i-1]+P[min(i,len(P)-1)])/2)))
  E.sort(key=lambda it:-it[0])
  for(D,AQ,AR)in E:getattr(B,'_d_'+AQ)(I,A,D,AR)
  if B.snow:
   t=random.Random(7)
   for _ in range(260):U,j,L=t.random(),t.random(),t.uniform(1,9);V=(U*W*1.4-A.yaw*A.f*2/L+math.sin(B.t*1.3+U*20)*12)%(W*1.4)-W*.2;k=(j*H*1.2+B.t*(40+260/L)+A.pitch*A.f*2/L)%(H*1.2)-H*.1;I.drawCircle(V,k,.8+3.2/L,paint(col('eef3ff'),120+120/L))
 def _d_solid(O,cv,cam,z,pl):
  D=cam;I,J=pl
  for K in I:
   A=np.array(K);B=np.cross(A[1]-A[0],A[2]-A[0]);F=np.linalg.norm(B)
   if F<1e-09:continue
   B/=F;L=A.mean(0)
   if np.dot(B,D.p-L)<=0:continue
   E=D.to_cam(A)
   if(E[:,2]<.08).any():continue
   G,P=D.proj(E);M=.38+.9*max(0,float(np.dot(B,LIGHT)))+(.12 if B[1]>.5 else 0);C=skia.Path();C.moveTo(*G[0])
   for N in G[1:]:C.lineTo(*N)
   C.close();H=fog(J*M,E[:,2].mean());cv.drawPath(C,paint(H));cv.drawPath(C,paint(H,255,.8))
 def _d_blob(S,cv,cam,z,b):
  D=cam;M,N,O,P,E=b;Q=D.to_cam([M,N,O]);(B,),T=D.proj(Q);A=D.f*P/z
  if B[0]+A<0 or B[0]-A>W or B[1]+A<0 or B[1]-A>H:return
  for(F,R)in(((-.12,-.14),PAL['canopy_lit']),((.06,.07),PAL['canopy'])):
   C=skia.Path()
   for(G,I)in enumerate(E):J=2*math.pi*G/len(E);K,L=B[0]+F[0]*A+math.cos(J)*A*I,B[1]+F[1]*A+math.sin(J)*A*I;C.moveTo(K,L)if G==0 else C.lineTo(K,L)
   C.close();cv.drawPath(C,paint(fog(R,z)))
 def _d_wire(D,cv,cam,z,w):
  A=cam;B=A.to_cam(np.array(w));C,E=A.proj(B)
  if(B[:,2]<.1).any():return
  cv.drawLine(*C[0],*C[1],paint(fog(PAL['wire'],z),200,max(.7,A.f*.012/z)))
 def _d_window(E,cv,cam,z,q):
  B=cam.to_cam(np.array(q))
  if(B[:,2]<.1).any():return
  C,F=cam.proj(B);A=skia.Path();A.moveTo(*C[0])
  for D in C[1:]:A.lineTo(*D)
  A.close();cv.drawPath(A,paint(PAL['window']))
 def _d_win2(G,cv,cam,z,pl):
  D,E=pl;B=cam.to_cam(np.array(D))
  if(B[:,2]<.1).any():return
  C,H=cam.proj(B);A=skia.Path();A.moveTo(*C[0])
  for F in C[1:]:A.lineTo(*F)
  A.close();cv.drawPath(A,paint(fog(E,z,.6)))
 def _d_glass(D,cv,cam,z,pl):
  E=cam;A,G,H=pl;A=np.array(A)
  if D.open and abs(A[:,0].mean()-D.open[0])<1:A=A+[0,3.2*D.open[1],0]
  F=E.to_cam(A)
  if(F[:,2]<.1).any():return
  C,J=E.proj(F);B=skia.Path();B.moveTo(*C[0])
  for I in C[1:]:B.lineTo(*I)
  B.close();cv.drawPath(B,paint(G,H));cv.drawPath(B,paint(col('cfe8ff'),120,2));cv.drawLine(*C[0],*C[2],paint(col('ffffff'),25,max(2,E.f*.08/z)))
 def _d_glow(A,cv,cam,z,gl):
  B=cam;H,I,J,K,L=gl[:5]
  if z<.3:return
  if len(gl)>5 and gl[5]and math.sin(A.t*23)+math.sin(A.t*7.7+1)+math.sin(A.t*3.1)<-1.1:return
  (C,),M=B.proj(B.to_cam([H,I,J]));D=B.f*K/z;E,F,G=(int(A)for A in L);cv.drawCircle(*C,D,skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(*C),D,[skia.ColorSetARGB(140,E,F,G),skia.ColorSetARGB(0,E,F,G)])))
 def _d_grass(F,cv,cam,z,pl):
  A,G,H,I,J=pl;D=[skia.Path()for A in range(4)];K=F.gc[A];L,M,N=G[A].tolist(),H[A].tolist(),I[A].tolist()
  for B in range(len(A)):C=D[K[B]];C.moveTo(*L[B]);C.lineTo(*N[B]);C.lineTo(*M[B]);C.close()
  for E in range(4):cv.drawPath(D[E],paint(fog(PAL['grass'][E],J,1.3)))
 def _d_bb(G,cv,cam,z,bb):C=cam;E=C.to_cam(bb['pos']);(A,),H=C.proj(E);D=C.f/z;F=skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(110,0,0,0),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,max(.5,D*.05)));B=bb.get('shadow',.35)*D;cv.drawOval(skia.Rect(A[0]-B,A[1]-B*.22,A[0]+B,A[1]+B*.22),F);bb['draw'](cv,A[0],A[1],D)
def vignette(cv,k=.8):cv.drawRect(skia.Rect(0,0,W,H),skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W/2,H/2),H*.72,[skia.ColorSetARGB(0,0,0,0),skia.ColorSetARGB(int(255*k),0,0,0)],[.45,1.])))
