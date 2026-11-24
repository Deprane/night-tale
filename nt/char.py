import math,skia
from world import col,c4,paint
INK=col('0a0a12')
EXPR={'neutral':(None,'flat',1.,False),'worried':('worried','frown',1.,True),'scared':('worried_hi','o',1.25,True),'shocked':('up','open',1.3,True),'nervous':('worried','grimace',1.,True),'relieved':(None,'smile',1.,False),'determined':('angry','flat',.95,False),'blank':(None,'flat',.85,True),'happy':(None,'smile_open',1.,False)}
def _p(*B,close=True):
 A=skia.Path();A.moveTo(*B[0])
 for C in B[1:]:A.lineTo(*C)
 if close:A.close()
 return A
def _lin(x0,y0,x1,y1,a,b):return skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeLinear([skia.Point(x0,y0),skia.Point(x1,y1)],[c4(col(a)),c4(col(b))]))
def kid(st,t):
 D=st;J=D.get('expr','neutral');K=D.get('view','front');L=D.get('seed',0)
 def A(cv,x,y,ppm):
  A=cv;M=ppm*1.45/1000;A.save();A.translate(x,y);A.scale(M,M);E=D.get('walking');N=t*8.5;O=-abs(math.sin(N))*22 if E else math.sin(t*2.3+L)*3;P=1.;I=D.get('react_t')
  if I is not None and 0<=t-I<.35:Q=(t-I)/.35;P=1+.12*math.sin(Q*math.pi)*(1-Q)
  F=math.sin(N)*38 if E else 0
  for(R,W)in((-42,F),(42,-F)):A.drawLine(R,-300+O,R+W,0,paint(INK,255,26))
  A.translate(0,O);A.scale(1,P);S=D.get('pose')=='up'
  for B in(-1,1):T=B*112,-610;U=(B*125,-760)if S else(B*(150+(abs(F)*.3 if E else 0)),-335+(B*F*.4 if E else 0));X=B*175,(T[1]+U[1])/2;G=skia.Path();G.moveTo(*T);G.quadTo(*X,*U);A.drawPath(G,paint(INK,255,74));A.drawPath(G,paint(col('8ea7ea'),255,52));A.drawPath(G,paint(col('c5d3fb'),255,8))
  C=skia.Path();C.moveTo(-108,-640);C.lineTo(108,-640);C.quadTo(132,-470,138,-300);C.lineTo(-138,-300);C.quadTo(-132,-470,-108,-640);C.close();A.drawPath(C,paint(col('8ea7ea')));A.save();A.clipPath(C,doAntiAlias=True)
  for H in range(-6,7):A.drawLine(H*24,-660,H*27,-290,paint(col('c5d3fb'),255,8,cap=False))
  A.drawRect(skia.Rect(-150,-660,150,-290),skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(-140,0),skia.Point(140,0)],[skia.ColorSetARGB(0,0,0,0),skia.ColorSetARGB(0,0,0,0),skia.ColorSetARGB(85,10,15,50)],[0,.45,1])));A.restore();A.drawPath(C,paint(INK,255,14))
  for B in(-1,1):A.drawCircle(B*150,-330+(B*F*.4 if E else 0),30,paint(INK))if not S else A.drawCircle(B*125,-760,30,paint(INK))
  if K=='front':
   A.drawPath(_p((-58,-642),(58,-642),(0,-548)),paint(col('f4f6ff')));A.drawPath(_p((-58,-642),(0,-548),(58,-642),close=False),paint(INK,255,10))
   for H in range(3):A.drawCircle(0,-500+H*62,11,paint(col('2a3b8f')));A.drawCircle(0,-500+H*62,11,paint(INK,255,5))
  Y={'worried':-4,'scared':3,'nervous':-3}.get(J,0)+math.sin(t*1.7+L)*1.2;A.save();A.translate(0,-650);A.rotate(Y);A.translate(0,650);Z=skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-55,-850),260,[c4(col('ffffff')),c4(col('e4e9f8')),c4(col('aeb9de'))],[0,.55,1]));A.drawCircle(0,-790,152,Z);A.drawCircle(0,-790,152,paint(INK,255,14));V=skia.RRect.MakeRectXY(skia.Rect(-168,-985,168,-862),62,62);A.drawRRect(V,_lin(0,-985,0,-862,'3b4fc4','141c6e'));A.drawRRect(V,paint(INK,255,14));A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-118,-968,118,-948),10,10),paint(col('ffffff'),85))
  if K=='front':_face(A,J,D,t)
  A.restore();A.restore()
 return A
def _lively_eyes(cv,st,t,look,bl,es):
 C=es;A=cv;L=col(st.get('lid','c99a72'));M=st.get('look',0);G=1. if bl else st.get('lid_level',.16)
 for N in(-1,1):D,E=N*56+look,-800;F,B=30*C,27*C;A.save();H=skia.Rect(D-F,E-B,D+F,E+B);A.drawOval(H,paint(col('f6f3ea')));K=skia.Path();K.addOval(H);A.clipPath(K,doAntiAlias=True);I=D+M*13*C;J=E+3;A.drawCircle(I,J,18*C,paint(col('22140c')));A.drawCircle(I,J,9*C,paint(INK));A.drawCircle(I-6*C,J-7*C,5*C,paint(col('ffffff'),230));A.drawRect(skia.Rect(D-F-2,E-B-2,D+F+2,E-B+2*B*G),paint(L));A.restore();A.drawOval(H,paint(INK,255,6));A.drawLine(D-F*.95,E-B+2*B*G,D+F*.95,E-B+2*B*G,paint(INK,255,7))
def _face(cv,expr,st,t):
 F=st;D=cv;I,Q,G,T=EXPR.get(expr,EXPR['neutral']);E=F.get('look',0)*14;R=F.get('seed',0);N=(t+R*.7)%3.3<.12 and not expr in('shocked',)
 if F.get('eyes')=='lively':
  E=F.get('look',0)*22;_lively_eyes(D,F,t,E,N,G*1.3)
  if not I:
   for A in(-1,1):D.drawPath(_q((A*28+E,-846),(A*60+E,-858),(A*92+E,-846)),paint(INK,255,9))
 for A in(-1,1):
  if F.get('eyes')=='lively':
   if I:J,K={'worried':((A*92,-848),(A*30,-866)),'worried_hi':((A*92,-860),(A*30,-884)),'up':((A*88,-876),(A*28,-880)),'angry':((A*92,-868),(A*28,-842))}[I];D.drawLine(J[0]+E,J[1],K[0]+E,K[1],paint(INK,255,10))
   continue
  O,P=A*55+E,-795;S=3 if N else 25*G;D.drawOval(skia.Rect(O-16*G,P-S,O+16*G,P+S),paint(INK))
  if not N:D.drawCircle(O-5*G,P-9*G,5*G,paint(col('ffffff'),200))
  if I:J,K={'worried':((A*92,-838),(A*30,-858)),'worried_hi':((A*92,-852),(A*30,-876)),'up':((A*88,-868),(A*28,-872)),'angry':((A*92,-862),(A*28,-836))}[I];D.drawLine(J[0]+E,J[1],K[0]+E,K[1],paint(INK,255,10))
 if F.get('talk')and int(t*9+math.sin(t*23)*1.4)%2==0:Q='open_s'
 B,C=E*.6,-712;U={'flat':lambda:D.drawLine(B-30,C,B+30,C,paint(INK,255,10)),'frown':lambda:D.drawPath(_q((B-34,C+10),(B,C-16),(B+34,C+10)),paint(INK,255,10)),'smile':lambda:D.drawPath(_q((B-36,C-6),(B,C+22),(B+36,C-6)),paint(INK,255,10)),'o':lambda:D.drawOval(skia.Rect(B-13,C-16,B+13,C+18),paint(INK)),'open':lambda:D.drawOval(skia.Rect(B-22,C-22,B+22,C+30),paint(INK)),'open_s':lambda:_open(D,B,C,28,20),'smile_open':lambda:_open(D,B,C,36,30,smile=True),'grimace':lambda:(D.drawRRect(skia.RRect.MakeRectXY(skia.Rect(B-38,C-14,B+38,C+14),10,10),paint(col('ffffff'))),D.drawLine(B-36,C,B+36,C,paint(INK,255,5)),D.drawRRect(skia.RRect.MakeRectXY(skia.Rect(B-38,C-14,B+38,C+14),10,10),paint(INK,255,8)))}[Q];U()
 if T:V=(t*.6+R)%1;L,M=112,-880+V*40;H=skia.Path();H.moveTo(L,M-22);H.quadTo(L+16,M+4,L,M+12);H.quadTo(L-16,M+4,L,M-22);H.close();D.drawPath(H,paint(col('a8d8ff')));D.drawPath(H,paint(INK,255,5))
def _q(a,c,b):A=skia.Path();A.moveTo(*a);A.quadTo(*c,*b);return A
def _open(cv,mx,my,w,h,smile=False):
 D=cv;B=my;A=mx;C=skia.Path();C.moveTo(A-w,B-h*.35);C.lineTo(A+w,B-h*.35);C.quadTo(A+w*.9,B+h*.75,A,B+h*.8);C.quadTo(A-w*.9,B+h*.75,A-w,B-h*.35);C.close();D.drawPath(C,paint(INK));D.save();D.clipPath(C,doAntiAlias=True);D.drawRect(skia.Rect(A-w*.7,B-h*.35,A+w*.7,B-h*.05),paint(col('ffffff')))
 if smile:D.drawOval(skia.Rect(A-w*.5,B+h*.3,A+w*.5,B+h*1.),paint(col('d0505a')))
 D.restore()
def sack(cv,x,y,ppm):
 A=cv;D=ppm*1./1000;A.save();A.translate(x,y);A.scale(D,D)
 for(E,F)in((-80,-14),(0,-4),(70,10)):A.save();A.translate(E,-520);A.rotate(F);A.drawLine(0,0,0,-330,paint(col('d8cdb0'),255,34));A.drawCircle(-14,-335,22,paint(col('e6dcc0')));A.drawCircle(14,-335,22,paint(col('e6dcc0')));A.restore()
 B=skia.Path();B.moveTo(-230,-500);B.quadTo(0,-560,230,-500);B.quadTo(290,-150,210,0);B.lineTo(-210,0);B.quadTo(-290,-150,-230,-500);B.close();A.drawPath(B,_lin(-250,0,250,0,'7a5a3c','3e2c1e'))
 for C in(-360,-200):A.drawPath(_q((-250,C),(0,C+30),(250,C)),paint(col('2c1f14'),200,8))
 A.drawPath(B,paint(INK,255,12));A.restore()
def stalker(t=.0):
 def A(cv,x,y,ppm):
  A=cv;E=ppm*3.2/1000;A.save();A.translate(x,y);A.scale(E,E);B=math.sin(t*1.1)*6;C=col('120f12');H=col('3b3550')
  for F in(-40,40):A.drawLine(F,-470,F*1.2,0,paint(C,255,26))
  G=_p((-75,-820),(75,-820),(60,-460),(-60,-460));A.drawPath(G,paint(C));A.drawPath(G,paint(H,255,4))
  for D in(-1,1):
   A.drawLine(D*70,-800,D*95+B,-330,paint(C,255,18))
   for I in(-1,0,1):A.drawLine(D*95+B,-330,D*95+B+I*14,-290,paint(col('cfc7b0'),255,6))
  A.drawCircle(B*.3,-860,52,paint(C));A.drawOval(skia.Rect(-190+B*.3,-930,190+B*.3,-880),paint(col('8a7650')));A.drawPath(_p((-80,-905),(80,-905),(55,-990),(-55,-990)),paint(col('8a7650')));A.restore()
 return A
def carved_post(lines):
 def A(cv,x,y,ppm):
  A=cv;C=ppm*1.3/1000;A.save();A.translate(x,y);A.scale(C,C);A.drawRect(skia.Rect(-160,-1000,160,0),_lin(-160,0,160,0,'8a7458','4a3b2c'))
  for B in range(14):A.drawLine(-150+B*22,-1000,-146+B*22,0,paint(col('3b2f22'),90,3,cap=False))
  D=skia.Font(skia.Typeface('Permanent Marker')or skia.Typeface('Inter'),70)
  for(B,E)in enumerate(lines):A.save();A.translate(0,-800+B*95);A.rotate(B*37%7-3);F=D.measureText(E);A.drawString(E,-F/2,0,D,paint(col('1e150e')));A.restore()
  A.restore()
 return A
def girl(st,t):
 C=st;N=C.get('expr','neutral');O=C.get('view','front');P=C.get('seed',3);Q,R,J=col('d9483b'),col('a8302a'),col('2fa39a')
 def A(cv,x,y,ppm):
  A=cv;S=ppm*1.4/1000;A.save();A.translate(x,y);A.scale(S,S);T=C.get('walking');U=t*8.5;V=-abs(math.sin(U))*22 if T else math.sin(t*2.3+P)*3;W=1.;K=C.get('react_t')
  if K is not None and 0<=t-K<.35:X=(t-K)/.35;W=1+.12*math.sin(X*math.pi)*(1-X)
  F=math.sin(U)*38 if T else 0
  for(G,L)in((-48,F),(48,-F)):A.drawLine(G,-300+V,G+L,-30,paint(col('1c2340'),255,40));A.drawOval(skia.Rect(G+L-38,-50,G+L+34,6),paint(INK))
  A.translate(0,V);A.scale(1,W);c=C.get('pose')=='up'
  for D in(-1,1):Y=D*125,-610;H=(D*125,-770)if c else(D*(168+abs(F)*.3),-340+D*F*.4);I=skia.Path();I.moveTo(*Y);I.quadTo(D*195,(Y[1]+H[1])/2,*H);A.drawPath(I,paint(INK,255,92));A.drawPath(I,paint(Q,255,70));A.drawCircle(*H,34,paint(J));A.drawCircle(*H,34,paint(INK,255,10))
  B=skia.Path();B.moveTo(-122,-650);B.lineTo(122,-650);B.quadTo(160,-480,160,-290);B.lineTo(-160,-290);B.quadTo(-160,-480,-122,-650);B.close();A.drawPath(B,paint(Q));A.save();A.clipPath(B,doAntiAlias=True)
  for M in(-560,-470,-380):A.drawPath(_q((-170,M),(0,M+22),(170,M)),paint(R,255,8))
  A.drawRect(skia.Rect(-170,-660,170,-280),skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(-160,0),skia.Point(160,0)],[skia.ColorSetARGB(60,255,255,255),skia.ColorSetARGB(0,0,0,0),skia.ColorSetARGB(90,30,0,10)],[0,.45,1])))
  if O=='front':A.drawLine(0,-640,0,-290,paint(R,255,7,cap=False))
  A.restore();A.drawPath(B,paint(INK,255,14));Z=col('5a3522');A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-178,-900,178,-655),70,70),paint(Z));A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-178,-900,178,-655),70,70),paint(INK,255,12));d={'worried':-4,'scared':3,'nervous':-3}.get(N,0)+math.sin(t*1.7+P)*1.2+(C.get('htilt',0)or 0);A.save();A.translate(0,-650);A.rotate(d);A.translate(0,650)
  if O=='front':
   e=skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-55,-850),260,[c4(col('fff6ee')),c4(col('f3e1d4')),c4(col('cdb3a6'))],[0,.55,1]));A.drawCircle(0,-790,150,e);A.drawCircle(0,-790,150,paint(INK,255,14))
   for D in(-1,1):A.drawOval(skia.Rect(D*95-22,-748,D*95+22,-728),paint(col('f28b8b'),120))
   _face(A,N,C,t)
  else:A.drawCircle(0,-790,152,paint(Z));A.drawCircle(0,-790,152,paint(INK,255,14))
  A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-120,-670,120,-615),26,26),paint(J));A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-120,-670,120,-615),26,26),paint(INK,255,10));a=skia.RRect.MakeRectXY(skia.Rect(40,-640,92,-500+math.sin(t*3)*8),18,18);A.drawRRect(a,paint(J));A.drawRRect(a,paint(INK,255,10));E=skia.Path();E.moveTo(-162,-860);E.cubicTo(-160,-1010,160,-1010,162,-860);E.close();A.drawPath(E,_lin(0,-990,0,-860,'f0c050','c98d22'));A.drawPath(E,paint(INK,255,14));b=skia.RRect.MakeRectXY(skia.Rect(-170,-895,170,-840),24,24);A.drawRRect(b,paint(col('e9b445')));A.drawRRect(b,paint(INK,255,12));A.drawCircle(0,-1000,42,paint(col('fff4dc')));A.drawCircle(0,-1000,42,paint(INK,255,12));A.restore();A.restore()
 return A
def antlered(t=.0):
 def A(cv,x,y,ppm):
  A=cv;G=ppm*3./1000;A.save();A.translate(x,y);A.scale(G,G);D=math.sin(t*.9)*5;E=col('16121a');H=col('d9d2c0');I=col('3a2c22')
  for J in(-35,35):A.drawLine(J,-450,J*1.3,0,paint(E,255,22))
  L=_p((-70,-760),(70,-760),(45,-440),(-45,-440));A.drawPath(L,paint(E))
  for K in range(4):A.drawLine(-40,-690+K*50,40,-690+K*50,paint(col('2c2630'),255,6))
  for B in(-1,1):
   A.drawLine(B*65,-740,B*110+D,-260,paint(E,255,16))
   for M in(-1,0,1):A.drawLine(B*110+D,-260,B*110+D+M*16,-200,paint(H,255,5))
  A.save();A.translate(D*.4,0)
  for B in(-1,1):
   for(N,F)in((B*30,260),(B*70,160)):A.save();A.translate(B*30,-860);A.rotate(N);A.drawLine(0,0,0,-F,paint(I,255,14));A.drawLine(0,-F*.5,B*50,-F*.8,paint(I,255,10));A.restore()
  C=skia.Path();C.moveTo(-50,-880);C.quadTo(0,-910,50,-880);C.lineTo(30,-780);C.quadTo(0,-760,-30,-780);C.close();A.drawPath(C,paint(H));A.drawPath(C,paint(INK,255,5))
  for B in(-1,1):A.drawOval(skia.Rect(B*22-12,-860,B*22+12,-830),paint(INK));A.drawCircle(B*22,-845,3.5,paint(col('ffffff')))
  A.restore();A.restore()
 return A
def worker(st,t):
 E=st;O=E.get('expr','neutral');H=E.get('view','front');P=E.get('seed',5);L,Q,Z,a=col('3f5a4a'),col('2c4034'),col('34507e'),col('2a2a33')
 def A(cv,x,y,ppm):
  A=cv;R=ppm*1.55/1000;A.save();A.translate(x,y);A.scale(R,R);S=E.get('walking');T=t*8.5;M=-abs(math.sin(T))*22 if S else math.sin(t*2.3+P)*3;U=1.;N=E.get('react_t')
  if N is not None and 0<=t-N<.35:V=(t-N)/.35;U=1+.12*math.sin(V*math.pi)*(1-V)
  I=math.sin(T)*40 if S else 0
  for(F,G)in((-46,I),(46,-I)):A.drawLine(F,-300+M,F+G,-30,paint(Z,255,44));A.drawLine(F,-300+M,F+G,-30,paint(INK,255,4));A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(F+G-40,-48,F+G+40,4),20,20),paint(col('e8e8ee')));A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(F+G-40,-48,F+G+40,4),20,20),paint(INK,255,8))
  A.translate(0,M);A.scale(1,U)
  if H=='back':W=skia.RRect.MakeRectXY(skia.Rect(-120,-640,120,-340),50,50)
  b=E.get('pose')=='up'
  for B in(-1,1):X=B*122,-615;J=(B*125,-770)if b else(B*(160+abs(I)*.3),-335+B*I*.4);K=skia.Path();K.moveTo(*X);K.quadTo(B*190,(X[1]+J[1])/2,*J);A.drawPath(K,paint(INK,255,84));A.drawPath(K,paint(L,255,62));A.drawCircle(*J,30,paint(col('d9a77e')));A.drawCircle(*J,30,paint(INK,255,9))
  D=skia.Path();D.moveTo(-118,-650);D.lineTo(118,-650);D.quadTo(148,-480,148,-300);D.lineTo(-148,-300);D.quadTo(-148,-480,-118,-650);D.close();A.drawPath(D,paint(L));A.save();A.clipPath(D,doAntiAlias=True);A.drawRect(skia.Rect(-160,-360,160,-290),paint(Q))
  if H=='front':
   A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-80,-470,80,-380),20,20),paint(Q))
   for B in(-1,1):A.drawLine(B*95,-650,B*105,-330,paint(a,255,26))
   for B in(-1,1):A.drawLine(B*22,-640,B*26,-560,paint(col('e8e8ee'),255,6))
  A.drawRect(skia.Rect(-160,-660,160,-290),skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(-150,0),skia.Point(150,0)],[skia.ColorSetARGB(50,255,255,255),skia.ColorSetARGB(0,0,0,0),skia.ColorSetARGB(95,10,0,20)],[0,.45,1])));A.restore();A.drawPath(D,paint(INK,255,14))
  if H=='back':A.drawRRect(W,_lin(0,-640,0,-340,'3a3a46','1e1e26'));A.drawRRect(W,paint(INK,255,12));A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-80,-470,80,-380),20,20),paint(INK,255,8))
  A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-135,-690,135,-625),30,30),paint(L));A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-135,-690,135,-625),30,30),paint(INK,255,11));c={'worried':-4,'scared':3,'nervous':-3}.get(O,0)+math.sin(t*1.7+P)*1.2+(E.get('htilt',0)or 0);A.save();A.translate(0,-650);A.rotate(c);A.translate(0,650);Y=col('17141a')
  if H=='front':d=skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-55,-850),260,[c4(col('f3d2b0')),c4(col('dcb18a')),c4(col('a87a58'))],[0,.55,1]));A.drawCircle(0,-790,150,d);A.drawCircle(0,-790,150,paint(INK,255,14));C=skia.Path();C.moveTo(-152,-800);C.cubicTo(-160,-985,160,-985,152,-800);C.lineTo(120,-850);C.lineTo(70,-830);C.lineTo(30,-868);C.lineTo(-20,-838);C.lineTo(-70,-866);C.lineTo(-120,-836);C.close();A.drawPath(C,paint(Y));A.drawPath(C,paint(INK,255,12));A.drawPath(_q((-70,-905),(0,-928),(70,-905)),paint(col('4a4560'),255,8));_face(A,O,E,t)
  else:A.drawCircle(0,-790,152,paint(Y));A.drawCircle(0,-790,152,paint(INK,255,14));A.drawPath(_q((-70,-880),(0,-905),(70,-880)),paint(col('4a4560'),255,8))
  A.restore();A.restore()
 return A
def llorona(t=.0,face=False):
 H=face
 def A(cv,x,y,ppm):
  A=cv;L=ppm*1.75/1000;A.save();A.translate(x,y);A.scale(L,L);A.translate(0,-90+math.sin(t*2.)*18);C=math.sin(t*1.6)*14;M=skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(70,200,215,255),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,60));A.drawOval(skia.Rect(-260,-1020,260,40),M);F=skia.Path();F.moveTo(-105,-740);F.lineTo(105,-740);F.quadTo(200+C,-380,250+C,-20)
  for G in range(10,-1,-1):N=-250+G*50+C*(G/10);F.lineTo(N,-20+(30 if G%2 else-10)+math.sin(t*4+G)*12)
  F.quadTo(-200+C*.3,-380,-105,-740);F.close();O=skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeLinear([skia.Point(0,-740),skia.Point(0,0)],[skia.ColorSetARGB(240,246,248,255),skia.ColorSetARGB(200,170,182,215),skia.ColorSetARGB(40,140,155,200)],[0,.6,1]));A.drawPath(F,O)
  for I in(-60,20,90):A.drawPath(_q((I*.6,-700),(I+C*.5,-380),(I*1.6+C,-60)),paint(col('8e9ac0'),120,6))
  for B in(-1,1):
   J=skia.Path();J.moveTo(B*95,-720);J.quadTo(B*190,-560,B*165+C*.3,-400);A.drawPath(J,paint(col('e6eaf8'),230,60));A.drawCircle(B*165+C*.3,-385,22,paint(col('c8d0e2')))
   for P in(-1,0,1):A.drawLine(B*165+C*.3,-385,B*165+C*.3+P*10,-345,paint(col('c8d0e2'),255,6))
  A.drawCircle(0,-850,108,paint(col('c9d0e2')))
  if H:
   for B in(-1,1):A.drawOval(skia.Rect(B*42-24,-885,B*42+24,-830),paint(INK));A.drawCircle(B*42,-858,4,paint(col('ffffff')));K=skia.Path();K.moveTo(B*42,-835);K.quadTo(B*48,-780,B*40,-700);A.drawPath(K,paint(INK,230,7))
   A.drawOval(skia.Rect(-26,-812,26,-745),paint(INK))
  D=skia.Path()
  if H:
   for B in(-1,1):D.moveTo(B*40,-955);D.quadTo(B*140,-940,B*130,-820);D.lineTo(B*(150+C*.2),-450);D.lineTo(B*95,-470);D.quadTo(B*105,-800,B*40,-955);D.close()
  else:
   D.moveTo(-120,-900);D.quadTo(0,-990,120,-900);D.lineTo(140+C*.3,-470)
   for G in range(7):D.lineTo(140-(G+1)*40+C*.3,-470+(25 if G%2 else-15))
   D.close()
  A.drawPath(D,paint(col('0a080c')))
  if not H:A.drawLine(-6,-900,-2,-620,paint(col('2a2630'),255,5));A.drawCircle(-2,-850,7,paint(col('f0f0ff'),220))
  E=skia.Path();E.moveTo(-130,-905);E.quadTo(0,-1010,130,-905);E.quadTo(170+C,-760,150+C,-600);E.lineTo(-150+C*.5,-600);E.quadTo(-170,-760,-130,-905);E.close();A.drawPath(E,paint(col('eef2ff'),70));A.drawPath(E,paint(col('eef2ff'),120,5));A.restore()
 return A
TWIST=[(0,-28),(.35,-55),(.6,-78),(.8,-95)]
def chupacabras(t=.0,twist=None,crouch=None):
 Q=crouch;M=twist
 def A(cv,x,y,ppm):
  A=cv;U=ppm*1.5/1000;A.save();A.translate(x,y);A.scale(U,U)
  if Q is not None and t>Q:D=min(1,(t-Q)/.3);A.scale(1+.1*D,1-.17*D);A.translate(math.sin(t*31)*4*D,0)
  C=math.sin(t*2.6)*8;N=7 if t*1.7%1>.9 else-4 if(t*1.3+.4)%1>.93 else 0
  if M is not None:
   N=0
   for(D,(V,H))in enumerate(TWIST):
    W=TWIST[D-1][1]if D else 0
    if t>=M+V:N=W+(H-W)*min(1,(t-M-V)/.06)
   if t>M:N+=math.sin(t*47)*1.5
  X,Y,O,a=col('7d806e'),col('454839'),col('15160f'),col('b9bea4')
  def Z(pts,w):
   B=skia.Path();B.moveTo(*pts[0])
   for C in pts[1:]:B.lineTo(*C)
   A.drawPath(B,paint(INK,255,w+14));A.drawPath(B,paint(Y,255,w))
  for R in range(17):H=-80+R*10;K=300+160*abs(math.sin(R*2.1))+math.sin(t*5+R)*10;A.save();A.translate(0,-800+C);A.rotate(H);b=_p((-13,0),(13,0),(0,-K));A.drawPath(b,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeLinear([skia.Point(0,0),skia.Point(0,-K)],[c4(col('1a0606')),c4(col('8a1010'))])));A.restore()
  for B in(-1,1):
   Z([(B*80,-430+C),(B*270,-330),(B*210,-20)],40)
   for S in(-1,0,1):A.drawLine(B*210,-20,B*210+S*34+B*20,18,paint(col('e9e3cc'),255,9))
  E=skia.Path();E.moveTo(-85,-420+C);E.quadTo(-130,-620,-250,-820+C);E.quadTo(0,-900+C,250,-820+C);E.quadTo(130,-620,85,-420+C);E.close();A.drawPath(E,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-60,-780),420,[c4(X),c4(Y),c4(O)],[0,.45,1])))
  for D in range(5):
   T=-720+D*50+C
   for B in(-1,1):A.drawPath(_q((B*18,T),(B*90,T-20),(B*(150-D*12),T+30)),paint(O,200,9))
  A.drawLine(0,-800+C,0,-440+C,paint(O,180,7));A.drawPath(E,paint(INK,255,14))
  for B in(-1,1):
   P=B*(250+math.sin(t*1.4+B)*10);Z([(B*225,-800+C),(B*360,-520),(P,-70)],30)
   for S in range(4):H=math.radians(-60+S*40);K=175;A.drawPath(_q((P,-70),(P+B*math.sin(H)*K*.7,-30),(P+B*math.sin(H)*K,10)),paint(col('ece6cf'),255,10))
  c=skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(150,0,0,0),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,40));A.drawOval(skia.Rect(-170,-720+C,170,-560+C),c);A.save();A.translate(0,-700+C);A.rotate(N);A.translate(0,700);F=skia.Path();F.moveTo(0,-1000);F.cubicTo(175,-1000,175,-800,95,-690);F.quadTo(0,-610,-95,-690);F.cubicTo(-175,-800,-175,-1000,0,-1000);F.close();A.drawPath(F,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-40,-930),300,[c4(a),c4(X),c4(O)],[0,.4,1])));A.drawPath(F,paint(INK,255,14));A.drawPath(_q((-70,-975),(0,-995),(70,-975)),paint(col('e6e9d6'),130,8));d=t%2.7<.09
  for B in(-1,1):
   L=skia.Path();L.moveTo(B*18,-800);L.quadTo(B*70,-905,B*140,-880);L.quadTo(B*100,-790,B*18,-800);L.close()
   if d:A.drawPath(_q((B*18,-805),(B*80,-830),(B*140,-880)),paint(INK,255,10));continue
   A.drawOval(skia.Rect(B*80-85,-915,B*80+85,-775),skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(200,0,0,0),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,22)));A.drawPath(L,paint(col('050505')));e=skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(255,255,10,10),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,26));A.drawCircle(B*82,-848,40,e);A.drawCircle(B*82,-848,11,paint(col('ff2a2a')));A.drawCircle(B*82,-848,4,paint(col('ffd0d0')))
  for B in(-1,1):A.drawOval(skia.Rect(B*10-7,-775,B*10+7,-755),paint(INK))
  I=26+14*max(0,math.sin(t*2.2));G=skia.Path();G.moveTo(-135,-770);G.quadTo(0,-690,135,-770);G.quadTo(0,-690+I*2.6,-135,-770);G.close();A.drawPath(G,paint(col('170404')));A.save();A.clipPath(G,doAntiAlias=True)
  for D in range(15):J=-128+D*18.5;A.drawPath(_p((J-7,-780),(J+7,-780),(J,-712+D%2*8)),paint(col('f1ecd8')));A.drawPath(_p((J+2,-680+I*1.5),(J+14,-680+I*1.5),(J+8,-712+I)),paint(col('e2dcc6')))
  A.restore();A.drawPath(G,paint(INK,255,7));f=t*.5%1;A.drawLine(40,-712+I*.6,42,-712+I*.6+90*f,paint(col('c8d4c0'),140,6));A.restore();A.restore()
 return A
def _glow(cv,x,y,r,rgb,a=200):cv.drawCircle(x,y,r*2.2,skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(a,*[int(A)for A in rgb]),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,r)));cv.drawCircle(x,y,r*.6,paint(col('ffffff')))
def _tufts(cv,cx,cy,rx,ry,n,rgb,a0=0,a1=360,L=40,w=26,seed=0):
 for D in range(n):A=math.radians(a0+(a1-a0)*D/max(1,n-1));E=L*(1+.35*math.sin(D*2.7+seed));B,C=cx+math.cos(A)*rx,cy+math.sin(A)*ry;H,I=B+math.cos(A)*E,C+math.sin(A)*E;F,G=-math.sin(A)*w/2,math.cos(A)*w/2;cv.drawPath(_p((B-F,C-G),(H,I),(B+F,C+G)),paint(rgb))
def charro(t=.0):
 def A(cv,x,y,ppm):
  A=cv;J=ppm*1.9/1000;A.save();A.translate(x,y);A.scale(J,J);I=math.sin(t*1.2)*6;K,M,G=col('121117'),col('25232c'),col('c9ccd6');A.drawOval(skia.Rect(-260,-980,260,-80),skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(60,120,150,255),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,70)))
  for B in(-1,1):
   A.drawLine(B*55,-470,B*70,-40,paint(INK,255,84));A.drawLine(B*55,-470,B*70,-40,paint(K,255,66))
   for D in range(6):A.drawCircle(B*(88-D*1.5),-420+D*62,7,paint(G))
   A.drawPath(_p((B*30,-50),(B*120,-50),(B*135,0),(B*25,0)),paint(col('0a0a0c')))
  E=skia.Path();E.moveTo(-150,-760);E.lineTo(150,-760);E.lineTo(125,-470);E.lineTo(-125,-470);E.close();A.drawPath(E,_lin(-150,0,150,0,'2c2a34','0c0b10'));A.drawPath(E,paint(INK,255,12));A.drawPath(_p((-40,-760),(40,-760),(0,-600)),paint(col('d8d4c8')))
  for B in(-1,1):
   A.drawPath(_q((B*40,-760),(B*90,-650),(B*70,-500)),paint(G,255,6))
   for D in range(3):A.drawCircle(B*70,-680+D*55,9,paint(G))
   H=skia.Path();H.moveTo(B*145,-745);H.quadTo(B*215,-600,B*180+I,-430);A.drawPath(H,paint(INK,255,78));A.drawPath(H,paint(M,255,60));L=B*180+I
   for N in(-1,0,1):A.drawLine(L,-430,L+N*14,-380,paint(col('d9d2bd'),255,9))
  A.drawPath(_p((-45,-770),(0,-745),(45,-770),(0,-730)),paint(col('8f1010')));A.save();A.translate(I*.3,0);C=skia.Path();C.moveTo(-85,-880);C.cubicTo(-90,-990,90,-990,85,-880);C.quadTo(70,-800,35,-780);C.lineTo(-35,-780);C.quadTo(-70,-800,-85,-880);C.close();A.drawPath(C,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-25,-920),140,[c4(col('f1ecdd')),c4(col('bdb5a0'))])));A.drawPath(C,paint(INK,255,9))
  for B in(-1,1):A.drawOval(skia.Rect(B*38-26,-905,B*38+26,-858),paint(INK));_glow(A,B*38,-880,9,col('8fc8ff'))
  A.drawPath(_p((-8,-845),(8,-845),(0,-825)),paint(INK))
  for D in range(7):A.drawLine(-36+D*12,-810,-36+D*12,-785,paint(INK,255,4))
  A.drawLine(-40,-798,40,-798,paint(INK,255,4));A.drawOval(skia.Rect(-300,-965,300,-905),paint(K));A.drawOval(skia.Rect(-300,-965,300,-905),paint(G,255,6));F=skia.Path();F.moveTo(-100,-945);F.quadTo(-95,-1110,0,-1120);F.quadTo(95,-1110,100,-945);F.close();A.drawPath(F,_lin(-100,0,100,0,'2a2830','0b0a0e'));A.drawPath(F,paint(INK,255,8));A.drawLine(-96,-975,96,-975,paint(G,255,12));A.restore();A.restore()
 return A
def nahual(t=.0):
 def A(cv,x,y,ppm):
  C=cv;N=ppm*2.1/1000;C.save();C.translate(x,y);C.scale(N,N);D=math.sin(t*3)*8;I,J,O=col('3b3430'),col('241f1c'),col('5a4f47')
  for B in(-1,1):
   E=skia.Path();E.moveTo(B*70,-450);E.lineTo(B*150,-260);E.lineTo(B*90,-110);E.lineTo(B*140,0);C.drawPath(E,paint(INK,255,70));C.drawPath(E,paint(I,255,54))
   for K in(-1,0,1):C.drawLine(B*140,0,B*140+K*22+B*15,18,paint(col('d8d0bc'),255,8))
  _tufts(C,0,-640+D,175,230,26,J,-200,20,L=55,w=40,seed=1);C.drawOval(skia.Rect(-175,-870+D,175,-410+D),skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-50,-760),330,[c4(O),c4(I),c4(J)],[0,.5,1])));_tufts(C,0,-560+D,120,120,9,col('6b6056'),30,150,L=40,w=30,seed=3)
  for B in(-1,1):
   L=skia.Path();L.moveTo(B*150,-820+D);L.quadTo(B*280,-600,B*230,-300);C.drawPath(L,paint(INK,255,76));C.drawPath(L,paint(I,255,60))
   for K in range(4):C.drawPath(_q((B*230,-300),(B*(230+(K-1.5)*20),-260),(B*(225+(K-1.5)*30),-205)),paint(col('e4dccb'),255,9))
  A=-930+D
  for B in(-1,1):C.drawPath(_p((B*40,A-70),(B*120,A-60),(B*115,A-210)),paint(J))
  _tufts(C,0,A,115,95,14,J,-180,0,L=40,w=34,seed=2);C.drawOval(skia.Rect(-115,A-100,115,A+90),skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-30,A-50),170,[c4(O),c4(I)])));F=skia.Path();F.moveTo(-60,A+10);F.quadTo(0,A-10,60,A+10);F.lineTo(40,A+140);F.quadTo(0,A+160,-40,A+140);F.close();C.drawPath(F,paint(col('2e2824')));C.drawOval(skia.Rect(-22,A+118,22,A+146),paint(INK));G=skia.Path();G.moveTo(-48,A+95);G.quadTo(0,A+160,48,A+95);G.quadTo(0,A+205,-48,A+95);G.close();C.drawPath(G,paint(col('3a0808')))
  for M in(-34,34):C.drawPath(_p((M-9,A+105),(M+9,A+105),(M,A+160)),paint(col('f0ead6')))
  for B in(-1,1):C.drawLine(B*25,A-55,B*85,A-40,paint(INK,255,12));H=skia.Path();H.moveTo(B*25,A-30);H.quadTo(B*60,A-55,B*88,A-25);H.quadTo(B*60,A-10,B*25,A-30);H.close();C.drawPath(H,paint(col('ffd21f')));C.drawLine(B*57,A-42,B*57,A-16,paint(INK,255,8));C.drawCircle(B*57,A-30,28,skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(90,255,200,0),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,16)))
  C.restore()
 return A
def lechuza(t=.0):
 def A(cv,x,y,ppm):
  B=cv;L=ppm*1.7/1000;B.save();B.translate(x,y);B.scale(L,L);O=math.sin(t*2.4)*25;P,Q,R=col('6d5b48'),col('3b3027'),col('a8957a')
  for C in(-1,1):
   B.save();B.translate(C*150,-700);B.rotate(C*(25+O*.3));E=skia.Path();E.moveTo(0,0);E.quadTo(C*260,-120,C*380,60)
   for D in range(7):E.lineTo(C*(380-D*50),60+(110 if D%2==0 else 40)+D*25)
   E.quadTo(C*40,300,0,200);E.close();B.drawPath(E,_lin(0,0,C*380,0,'5a4a3a','2a221b'));B.drawPath(E,paint(INK,255,10))
   for D in range(5):B.drawPath(_q((C*40,40+D*30),(C*200,30+D*40),(C*(330-D*40),120+D*30)),paint(col('1e1813'),160,6))
   B.restore()
  H=skia.Path();H.addOval(skia.Rect(-190,-780,190,-120));B.drawPath(H,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-40,-560),330,[c4(R),c4(P),c4(Q)],[0,.5,1])))
  for I in range(5):
   for S in range(5-I%2):J=-120+S*60+(30 if I%2 else 0);K=-560+I*70;B.drawPath(_q((J-25,K),(J,K+30),(J+25,K)),paint(col('3d3128'),200,6))
  B.drawPath(H,paint(INK,255,12))
  for C in(-1,1):
   for M in(-1,0,1):B.drawPath(_q((C*70,-130),(C*70+M*40,-60),(C*70+M*55,0)),paint(col('2a2622'),255,18))
  A=-880;G=skia.Path();G.moveTo(-170,A-40);G.quadTo(0,A-230,170,A-40)
  for D in range(9):G.lineTo(170-D*42,A+260+(40 if D%2 else-10)+math.sin(t*2+D)*10)
  G.close();B.drawPath(G,_lin(0,A-200,0,A+260,'e4e2da','8e8a80'))
  for D in range(8):B.drawPath(_q((-140+D*40,A-120),(-150+D*42,A+60),(-150+D*42,A+240)),paint(col('6e6a62'),150,4))
  F=skia.Path();F.moveTo(-100,A-70);F.cubicTo(-110,A-170,110,A-170,100,A-70);F.quadTo(90,A+70,0,A+110);F.quadTo(-90,A+70,-100,A-70);F.close();B.drawPath(F,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-20,A-70),170,[c4(col('d8d2c0')),c4(col('9c9582'))])));B.drawPath(F,paint(INK,255,8))
  for D in range(3):B.drawPath(_q((-60,A-110+D*14),(0,A-122+D*14),(60,A-110+D*14)),paint(col('6e6858'),200,4))
  for C in(-1,1):B.drawOval(skia.Rect(C*45-30,A-75,C*45+30,A-15),paint(col('1a1612')));B.drawOval(skia.Rect(C*45-18,A-60,C*45+18,A-28),paint(col('f0c020')));B.drawCircle(C*45,A-44,10,paint(INK));B.drawPath(_q((C*20,A-5),(C*50,A+25),(C*75,A+5)),paint(col('6e6858'),200,4))
  B.drawPath(_p((-14,A-20),(14,A-20),(0,A+20)),paint(col('5a4a30')));N=skia.Path();N.addOval(skia.Rect(-30,A+35,30,A+85+math.sin(t*3)*10));B.drawPath(N,paint(col('1c0808')));B.restore()
 return A
def cadejo(t=.0):
 def A(cv,x,y,ppm):
  B=cv;J=ppm*1.85/1000;B.save();B.translate(x,y);B.scale(J,J);F=math.sin(t*3.4)*10;I,H,K=col('17151a'),col('0b0a0d'),col('2e2b33')
  for C in(-1,1):B.drawLine(C*110,-500,C*130,-40,paint(INK,255,92));B.drawLine(C*110,-500,C*130,-40,paint(I,255,76));B.drawPath(_p((C*85,-50),(C*175,-50),(C*165,0),(C*95,0)),paint(col('050506')))
  _tufts(B,0,-640+F,240,200,30,H,-210,30,L=70,w=50,seed=4);B.drawOval(skia.Rect(-240,-840+F,240,-440+F),skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-60,-760),340,[c4(K),c4(I),c4(H)],[0,.5,1])));_tufts(B,0,-520+F,160,70,11,H,20,160,L=60,w=40,seed=5);A=-720+F
  for C in(-1,1):B.drawPath(_p((C*60,A-120),(C*170,A-140),(C*150,A-260)),paint(H))
  B.drawOval(skia.Rect(-150,A-170,150,A+70),skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-40,A-110),220,[c4(K),c4(I)])));E=skia.Path();E.moveTo(-80,A-10);E.quadTo(0,A-40,80,A-10);E.lineTo(60,A+150);E.quadTo(0,A+175,-60,A+150);E.close();B.drawPath(E,paint(col('201e24')));B.drawOval(skia.Rect(-32,A+120,32,A+160),paint(col('050505')));G=skia.Path();G.moveTo(-70,A+90);G.quadTo(0,A+150,70,A+90);G.quadTo(0,A+230,-70,A+90);G.close();B.drawPath(G,paint(col('3a0606')))
  for D in range(6):B.drawPath(_p((-55+D*22,A+100),(-43+D*22,A+100),(-49+D*22,A+135+D%2*15)),paint(col('ece5cf')))
  for C in(-1,1):B.drawLine(C*25,A-95,C*110,A-75,paint(INK,255,14));_glow(B,C*68,A-55,16,col('ff1a1a'),230)
  for D in range(9):L=math.radians(200+D*17.5);M,N=math.cos(L)*170,A+120+math.sin(L)*-60+60;B.drawOval(skia.Rect(M-18,N-11,M+18,N+11),paint(col('8a8c96'),255,7))
  for D in range(4):B.drawOval(skia.Rect(139,A+200+D*32,161,A+222+D*32+math.sin(t*4)*3),paint(col('8a8c96'),255,7))
  B.restore()
 return A
def nopal(sc=1.,seed=.0):
 def A(cv,x,y,ppm):
  A=cv;C=ppm*sc/1000;A.save();A.translate(x,y);A.scale(C,C);G=[(0,-260,0,1),(-150,-560,-28,.85),(140,-600,24,.9),(-40,-860,-8,.75),(260,-860,40,.6)]
  for(D,H,I,B)in G:
   A.save();A.translate(D,H);A.rotate(I+math.sin(seed*9+D)*4);E=skia.Rect(-120*B,-190*B,120*B,190*B);A.drawOval(E,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-40*B,-60*B),230*B,[c4(col('5f7d4a')),c4(col('3c5631')),c4(col('25361f'))],[0,.6,1])));A.drawOval(E,paint(INK,255,8))
   for F in range(7):A.drawCircle(math.sin(F*2.3)*70*B,math.cos(F*1.7)*120*B,5,paint(col('d8d2a8')))
   A.restore()
  A.restore()
 return A
def maguey(sc=1.,seed=.0):
 def A(cv,x,y,ppm):
  A=cv;B=ppm*sc/1000;A.save();A.translate(x,y);A.scale(B,B)
  for C in range(11):E=-80+C*16;F=620+140*math.sin(C*1.9+seed*5);A.save();A.rotate(E);D=_p((-55,0),(55,0),(0,-F));A.drawPath(D,_lin(-55,0,55,0,'6f8a74','34483a'));A.drawPath(D,paint(INK,255,7));A.restore()
  A.restore()
 return A
def ranchero(st,t,h=1.4,skin=('e9c09a','c99a72','8e6446'),shirt=('f0ece2','c8c2b4'),plaid=False,pants='34507e',hat='d8c28a',hat_w=1.,stache=False,scarf=None,hair='17141a',tee=False,sneakers=False):
 l=scarf;k=shirt;b=tee;a=stache;T=hair;L=hat;G=skin;C=st;m=C.get('expr','neutral');R=C.get('view','front');c=C.get('seed',2);I=R in('left','right')
 def A1(cv):B=cv;B.drawOval(skia.Rect(-260,-892,230,-858),paint(col(L)));B.drawOval(skia.Rect(-260,-892,230,-858),paint(INK,255,9));A=skia.Path();A.moveTo(-115,-878);A.quadTo(-110,-1035,-5,-1040);A.quadTo(105,-1030,110,-878);A.close();B.drawPath(A,_lin(-115,0,110,0,L,'8a7448'));B.drawPath(A,paint(INK,255,9));B.drawLine(-110,-900,106,-900,paint(col('3a2416'),255,16))
 def A2(cv,front=True):
  A=skia.Path();A.moveTo(-158,-790);A.cubicTo(-170,-990,170,-990,158,-790)
  for B in range(8):A.lineTo(150-B*42,-858+(24 if B%2 else-6))
  A.close();cv.drawPath(A,paint(col(T)));cv.drawPath(A,paint(INK,255,11));cv.drawPath(_q((-60,-935),(0,-955),(60,-935)),paint(col('3a3640'),255,8))
 def A(cv,x,y,ppm):
  A=cv;n=ppm*h/1000;A.save();A.translate(x,y);A.scale(n,n)
  if R=='left':A.scale(-1,1)
  o=C.get('walking');p=t*8.5;d=-abs(math.sin(p))*22 if o else math.sin(t*2.3+c)*3;q=1.;e=C.get('react_t')
  if e is not None and 0<=t-e<.35:r=(t-e)/.35;q=1+.12*math.sin(r*math.pi)*(1-r)
  M=math.sin(p)*40 if o else 0;s=col('e8e8ee')if sneakers else col('3a2416');A3=((-10,M*1.6),(10,-M*1.6))if I else((-46,M),(46,-M))
  for(F,H)in A3:
   A.drawLine(F,-300+d,F+H,-30,paint(col(pants),255,46));A.drawLine(F,-300+d,F+H,-30,paint(INK,255,4))
   if I:A.drawPath(_p((F+H-30,-50),(F+H+60,-50),(F+H+66,4),(F+H-32,4)),paint(s))
   else:A.drawPath(_p((F+H-40,-50),(F+H+44,-50),(F+H+52,4),(F+H-42,4)),paint(s))
  A.translate(0,d);A.scale(1,q);U,f=col(k[0]),col(k[1]);A4=((1,),)if I else((-1,),(1,))
  if not I:
   for(V,)in A4:u=V*120,-615;B=V*(160+abs(M)*.3),-335+V*M*.4;J=skia.Path();J.moveTo(*u);J.quadTo(V*188,(u[1]+B[1])/2,*B);A.drawPath(J,paint(INK,255,80));A.drawPath(J,paint(U,255,58));A.drawCircle(*B,30,paint(col(G[1])));A.drawCircle(*B,30,paint(INK,255,9))
  P=C.get('reach',0)or 0
  if I and P>0:
   E=-40*(1-P)-380*P,-360*(1-P)-600*P;W=skia.Path();W.moveTo(-20,-610);W.quadTo(-60-150*P,-500-120*P,*E);A.drawPath(W,paint(INK,255,78));A.drawPath(W,paint(U*.7,255,56));A.drawOval(skia.Rect(E[0]-50,E[1]-42,E[0]-4,E[1]+42),paint(col(G[2])));A.drawOval(skia.Rect(E[0]-50,E[1]-42,E[0]-4,E[1]+42),paint(INK,255,8))
   for v in range(4):A.drawLine(E[0]-48,E[1]-30+v*20,E[0]-64,E[1]-34+v*22,paint(INK,255,14))
  g,X=(80,95)if I else(115,140);K=skia.Path();K.moveTo(-g,-650);K.lineTo(g,-650);K.quadTo(X,-480,X,-300);K.lineTo(-X,-300);K.quadTo(-X,-480,-g,-650);K.close();A.drawPath(K,paint(U));A.save();A.clipPath(K,doAntiAlias=True)
  if plaid:
   for N in range(-6,7):A.drawLine(N*40,-660,N*40,-290,paint(f,200,14,cap=False))
   for w in range(10):A.drawLine(-160,-640+w*40,160,-640+w*40,paint(f,200,14,cap=False))
  if b:A.drawRect(skia.Rect(-160,-470,160,-430),paint(f))
  if not b:A.drawRect(skia.Rect(-160,-340,160,-300),paint(col('3a2416')));A.drawRect(skia.Rect(-30,-338,30,-302),paint(col('c9b27a')))
  A.drawRect(skia.Rect(-160,-660,160,-290),skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(-150,0),skia.Point(150,0)],[skia.ColorSetARGB(50,255,255,255),skia.ColorSetARGB(0,0,0,0),skia.ColorSetARGB(95,10,0,20)],[0,.45,1])))
  if R=='front'and not b:
   A.drawPath(_p((-45,-650),(0,-580),(45,-650)),paint(col(G[1])))
   for N in range(3):A.drawCircle(0,-540+N*60,8,paint(col('ffffff')));A.drawCircle(0,-540+N*60,8,paint(INK,255,3))
  A.restore();A.drawPath(K,paint(INK,255,14))
  if I:
   B=30+M*2.2,-335;J=skia.Path();J.moveTo(0,-615);J.quadTo(20+M,-480,*B);A.drawPath(J,paint(INK,255,80));A.drawPath(J,paint(U,255,58));A.drawCircle(*B,30,paint(col(G[1])));A.drawCircle(*B,30,paint(INK,255,9))
   if C.get('lamp'):A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(B[0]-10,B[1]-34,B[0]+110,B[1]+6),12,12),paint(col('2a2a30')));A.drawRect(skia.Rect(B[0]+100,B[1]-42,B[0]+125,B[1]+14),paint(col('c9ccd6')))
  if l and R=='front':A.drawPath(_p((-110,-660),(110,-660),(0,-560)),paint(col(l)));A.drawPath(_p((-110,-660),(110,-660),(0,-560)),paint(INK,255,9))
  A5={'worried':-4,'scared':3,'nervous':-3}.get(m,0)+math.sin(t*1.7+c)*1.2+(C.get('htilt',0)or 0);A.save();A.translate(0,-650);A.rotate(A5);A.translate(0,650);z=skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-55,-850),260,[c4(col(G[0])),c4(col(G[1])),c4(col(G[2]))],[0,.55,1]))
  if R=='front':
   A.drawCircle(0,-790,150,z);A.drawCircle(0,-790,150,paint(INK,255,14));A6=dict(C,eyes='lively',lid=G[1]);_face(A,m,A6,t);Y=C.get('look',0)*22;A.drawPath(_q((-8+Y*1.2,-790),(12+Y*1.4,-752),(-6+Y*1.2,-748)),paint(col(G[2]),255,8))
   if a:A.save();A.translate(Y,0);D=skia.Path();D.moveTo(-70,-735);D.quadTo(0,-775,70,-735);D.quadTo(60,-705,0,-720);D.quadTo(-60,-705,-70,-735);D.close();A.drawPath(D,paint(col('e8e6e0')));A.drawPath(D,paint(INK,255,6));A.restore()
   if L is None:A2(A)
  elif I:
   A.drawCircle(0,-790,150,z);A.drawCircle(0,-790,150,paint(INK,255,14));A.drawPath(_p((140,-790),(178,-760),(140,-742)),paint(col(G[1])));A.drawPath(_q((140,-790),(182,-762),(140,-742)),paint(INK,255,7));i=(t+c*.7)%3.3<.12;A7=C.get('expr')in('scared','shocked','nervous')
   if A7 and not i:A8=C.get('glance',0)or 0;A9=math.sin(t*41)*1.2;A.drawOval(skia.Rect(72,-826,122,-766),paint(col('f6f3ec')));A.drawOval(skia.Rect(72,-826,122,-766),paint(INK,255,6));A0=106-26*A8+A9;A.drawCircle(A0,-796,11,paint(INK));A.drawCircle(A0+3,-800,3,paint(col('ffffff')));A.drawPath(_q((60,-848),(90,-872),(130,-856)),paint(INK,255,11));A.drawPath(_q((76,-758),(98,-750),(118,-758)),paint(INK,90,4));AA=C.get('breath',1.);Z=(14+10*abs(math.sin(t*6.5)))*AA+4;S=skia.Rect(92,-728-Z*.3,126,-708+Z*.6);A.drawOval(S,paint(col('2a0e0a')));A.save();A.clipPath(skia.Path().addOval(S),doAntiAlias=True);A.drawRect(skia.Rect(92,-734-Z*.3,128,-722-Z*.3),paint(col('f2eee4')));A.restore();A.drawOval(S,paint(INK,255,6));j=t*.45%1;A.drawOval(skia.Rect(-60,-870+j*110,-44,-844+j*110),paint(col('d6ecff'),int(200*(1-j))))
   else:
    A.drawOval(skia.Rect(80,-812+(20 if i else 0),108,-770-(20 if i else 0)),paint(INK));S='open_s'if C.get('talk')and int(t*9+math.sin(t*23)*1.4)%2==0 else'flat'
    if S=='flat':A.drawLine(88,-712,128,-716,paint(INK,255,9))
    else:A.drawOval(skia.Rect(92,-728,128,-700),paint(INK))
   if a:D=skia.Path();D.moveTo(70,-728);D.quadTo(140,-752,160,-722);D.quadTo(120,-705,70,-712);D.close();A.drawPath(D,paint(col('e8e6e0')));A.drawPath(D,paint(INK,255,5))
   A.drawOval(skia.Rect(-40,-820,10,-760),paint(col(G[2])))
   if L is None:
    O=skia.Path();O.moveTo(-155,-760);O.cubicTo(-170,-990,150,-1000,140,-840)
    for N in range(7):O.lineTo(110-N*40,-870+(22 if N%2 else-8))
    O.lineTo(-60,-820);O.lineTo(-150,-740);O.close();A.drawPath(O,paint(col(T)));A.drawPath(O,paint(INK,255,11))
   elif a:A.drawPath(_q((-150,-820),(-160,-760),(-120,-720)),paint(col(T),255,22))
  else:
   A.drawCircle(0,-790,152,paint(col(T)));A.drawCircle(0,-790,152,paint(INK,255,14))
   if L is None:A.drawPath(_q((-70,-900),(0,-925),(70,-900)),paint(col('3a3640'),255,8))
  if L is not None:
   if I:A1(A)
   else:A.save();A.scale(hat_w,1);A.drawOval(skia.Rect(-250,-905,250,-840),paint(col(L)));A.drawOval(skia.Rect(-250,-905,250,-840),paint(INK,255,10));Q=skia.Path();Q.moveTo(-120,-880);Q.quadTo(-120,-1040,0,-1045);Q.quadTo(120,-1040,120,-880);Q.close();A.drawPath(Q,_lin(-120,0,120,0,L,'8a7448'));A.drawPath(Q,paint(INK,255,10));A.drawLine(-116,-905,116,-905,paint(col('3a2416'),255,16));A.restore()
  A.restore();A.restore()
 return A
def beto(st,t):return ranchero(st,t,h=1.3,skin=('d9a77e','b9875e','7a5236'),shirt=('3f6fb0','e8e8ee'),pants='3d5a8a',hat=None,tee=True,sneakers=True,hair='141216')
def abuelo(st,t):return ranchero(st,t,h=1.68,skin=('d6a27a','b07e58','6e4a30'),shirt=('a33b2c','5c1d16'),plaid=True,pants='2f3a4c',hat='e0d0a2',hat_w=1.15,stache=True,hair='cfcac0')
def red_eyes(t=.0,on=None,h=2.4,sep=90):
 def A(cv,x,y,ppm):
  A=cv
  if on and not any(A<=t<B for(A,B)in on):return
  D=ppm/1000;A.save();A.translate(x,y);A.scale(D,D);E=t%2.9<.1
  for F in(-1,1):
   B=-h*1000;C=F*sep
   if E:A.drawLine(C-30,B,C+30,B,paint(col('ff2020'),255,12));continue
   _glow(A,C,B,30,col('ff1010'),255);A.drawOval(skia.Rect(C-34,B-18,C+34,B+18),paint(col('ff2a2a')));A.drawCircle(C,B,10,paint(col('2a0000')))
  A.restore()
 return A
def troca(t=.0):
 def A(cv,x,y,ppm):
  A=cv;C=ppm*1.8/1000;A.save();A.translate(x,y);A.scale(C,C);A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-520,-620,520,-150),60,60),_lin(0,-620,0,-150,'3e4e5a','1c262e'));A.drawPath(_p((-360,-620),(360,-620),(300,-960),(-300,-960)),paint(col('2c3a44')));A.drawPath(_p((-300,-640),(300,-640),(250,-920),(-250,-920)),paint(col('121a22')));A.drawRect(skia.Rect(-300,-480,300,-300),paint(col('101418')))
  for B in(-1,1):A.drawRect(skia.Rect(B*430-70,-160,B*430+70,0),paint(col('0a0a0a')));_glow(A,B*410,-400,70,col('fff2c8'),230);A.drawCircle(B*410,-400,60,paint(col('fffbe8')))
  A.restore()
 return A
def _chupa_head(cv,t,tilt=.0,jaw=.0):
 I=jaw;A=cv;K,J,L=col('7d806e'),col('15160f'),col('b9bea4');M=skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(150,0,0,0),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,40));A.drawOval(skia.Rect(-170,-720,170,-560),M);A.save();A.translate(0,-700);A.rotate(tilt);A.translate(0,700);D=skia.Path();D.moveTo(0,-1000);D.cubicTo(175,-1000,175,-800,95,-690);D.quadTo(0,-610,-95,-690);D.cubicTo(-175,-800,-175,-1000,0,-1000);D.close();A.drawPath(D,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(-40,-930),300,[c4(L),c4(K),c4(J)],[0,.4,1])))
 for E in range(6):A.drawPath(_q((-120+E*45,-990+E%2*20),(-100+E*45,-940),(-125+E*47,-905)),paint(J,90,5))
 A.drawPath(D,paint(INK,255,14));A.drawPath(_q((-70,-975),(0,-995),(70,-975)),paint(col('e6e9d6'),130,8));N=t%2.7<.09
 for B in(-1,1):
  H=skia.Path();H.moveTo(B*18,-800);H.quadTo(B*70,-905,B*140,-880);H.quadTo(B*100,-790,B*18,-800);H.close()
  if N:A.drawPath(_q((B*18,-805),(B*80,-830),(B*140,-880)),paint(INK,255,10));continue
  A.drawOval(skia.Rect(B*80-85,-915,B*80+85,-775),skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(200,0,0,0),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,22)));A.drawPath(H,paint(col('050505')));O=skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(255,255,10,10),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,26));A.drawCircle(B*82,-848,40,O);A.drawCircle(B*82,-848,11,paint(col('ff2a2a')));A.drawCircle(B*82,-848,4,paint(col('ffd0d0')))
 for B in(-1,1):A.drawOval(skia.Rect(B*10-7,-775,B*10+7,-755),paint(INK))
 C=34+18*max(0,math.sin(t*2.2))*(1-I)+95*I+math.sin(t*61)*4*I;F=skia.Path();F.moveTo(-140,-772);F.quadTo(0,-690,140,-772);F.quadTo(0,-690+C*2.6,-140,-772);F.close();A.drawPath(F,paint(col('170404')));A.save();A.clipPath(F,doAntiAlias=True)
 for E in range(16):G=-132+E*17.6;A.drawPath(_p((G-7,-782),(G+7,-782),(G,-708+E%2*10)),paint(col('f1ecd8')));A.drawPath(_p((G+2,-680+C*1.5),(G+14,-680+C*1.5),(G+8,-712+C)),paint(col('e2dcc6')))
 A.restore();A.drawPath(F,paint(INK,255,7));P=t*.5%1;A.drawLine(40,-712+C*.6,42,-712+C*.6+110*P,paint(col('c8d4c0'),150,6));A.drawLine(-60,-720+C*.5,-61,-720+C*.5+70*(t*.37%1),paint(col('c8d4c0'),120,5));A.restore()
_PERCH=[dict(hR=(-70,-1728),hL=(-445,-1080),eR=(-40,-1440),eL=(-600,-1230),sR=(-110,-1290),sL=(-500,-1280),hip=(-300,-880),kR=(-170,-690),fR=(-215,-520),kL=(-410,-690),fL=(-360,-470),head=(-250,-560,-12)),dict(hR=(-70,-1728),hL=(-260,-1720),eR=(150,-1600),eL=(-560,-1640),sR=(-30,-1770),sL=(-420,-1750),hip=(-230,-1400),kR=(-60,-1340),fR=(-300,-1230),kL=(-470,-1370),fL=(-430,-1200),head=(-225,-1020,8)),dict(hR=(20,-1748),hL=(-150,-1735),eR=(240,-1840),eL=(-420,-1830),sR=(150,-1930),sL=(-250,-1930),hip=(-40,-1640),kR=(450,-1640),fR=(360,-1318),kL=(-500,-1580),fL=(-390,-1228),head=(-50,-1150,0))]
def chupa_perch(t=.0,part='back',climb=None,twist=None):
 F=climb;D=twist;f,c,V=col('7d806e'),col('454839'),col('15160f')
 def R(cv,pts,w):
  A=skia.Path();A.moveTo(*pts[0])
  for B in pts[1:]:A.lineTo(*B)
  cv.drawPath(A,paint(INK,255,w+14));cv.drawPath(A,paint(c,255,w))
 def L(cv,x,y,ang,L=130,n=4,sp=22,curl=30):
  for E in range(n):A=math.radians(ang+(E-(n-1)/2)*sp);B,C=x+math.cos(A)*L,y+math.sin(A)*L;D=(x+B)/2-math.sin(A)*curl,(y+C)/2+math.cos(A)*curl;cv.drawPath(_q((x,y),D,(B,C)),paint(INK,255,18));cv.drawPath(_q((x,y),D,(B,C)),paint(col('ece6cf'),255,9))
 def g():
  C=.0 if F is None else max(0,min(1,(t-F)/1.))
  if C<.5:E,G,D=_PERCH[0],_PERCH[1],C/.5
  else:E,G,D=_PERCH[1],_PERCH[2],(C-.5)/.5
  D=D*D*(3-2*D);A={A:tuple(E[A][B]+(G[A][B]-E[A][B])*D for B in range(len(E[A])))for A in E};H=math.sin(t*1.15)*12*(1-C)
  for B in('sR','sL','hip','kR','kL','head'):A[B]=(A[B][0]+H,)+A[B][1:]
  A['fL']=A['fL'][0]+H*1.8,A['fL'][1]
  if C>=1:
   I=math.sin(t*7)*10
   for B in('sR','sL','hip','head','eR','eL'):A[B]=(A[B][0],A[B][1]+I)+A[B][2:]
  return A,C
 def A(cv,x,y,ppm):
  A=cv;d=ppm*1.5/1000;A.save();A.translate(x,y);A.scale(d,d);B,M=g();N=math.sin(t*23)*2;G=.0 if D is None else max(0,min(1,(t-D)/1.2))
  if G>0:h,i=(math.sin(t*53)+math.sin(t*87))*4*G,(math.sin(t*71)+math.sin(t*39))*3*G;A.translate(h,i);N+=math.sin(t*97)*5*G
  if part=='eyes':
   W,X,Y=B['head'];E=Y
   if D is not None and t>D:
    E=0
    for(F,(O,P))in enumerate(TWIST):
     Q=TWIST[F-1][1]if F else 0
     if t>=D+O:E=Q+(P-Q)*min(1,(t-D-O)/.06)
    E+=math.sin(t*47)*1.5
   if t%2.7>=.09:
    A.translate(W+N,X);A.translate(0,-700);A.rotate(E);A.translate(0,700)
    for H in(-1,)if M<.3 else(-1,1):j=skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(230,255,10,10),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,22));A.drawCircle(H*82,-848,30,j);A.drawCircle(H*82,-848,10,paint(col('ff2a2a')));A.drawCircle(H*82,-848,4,paint(col('ffd0d0')))
  elif part=='back':
   J,K=(B['sR'][0]+B['sL'][0])/2,(B['sR'][1]+B['sL'][1])/2
   for F in range(17):P=-80+F*10;e=(300+160*abs(math.sin(F*2.1)))*(1+.3*G)+math.sin(t*(5+40*G)+F)*(10+18*G);A.save();A.translate(J,K+20);A.rotate(P);k=_p((-12,0),(12,0),(0,-e));A.drawPath(k,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeLinear([skia.Point(0,0),skia.Point(0,-e)],[c4(col('1a0606')),c4(col('8a1010'))])));A.restore()
   C=B['hip'];R(A,[(C[0]+40,C[1]),B['kR'],B['fR']],36);R(A,[(C[0]-40,C[1]),B['kL'],B['fL']],34);I=skia.Path();S,T=B['sL'],B['sR'];I.moveTo(C[0]-85,C[1]);I.quadTo(C[0]-140,(C[1]+S[1])/2+30,S[0],S[1]);I.quadTo(J,K-90,T[0],T[1]);I.quadTo(C[0]+140,(C[1]+T[1])/2+30,C[0]+85,C[1]);I.close();A.drawPath(I,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeRadial(skia.Point(J-50,K+40),430,[c4(f),c4(c),c4(V)],[0,.45,1])));l=C[1]-K
   for Z in range(6):
    a=K+80+Z*l/9;b=J+(C[0]-J)*(Z/8)
    for H in(-1,1):A.drawPath(_q((b+H*18,a),(b+H*95,a-22),(b+H*(165-Z*14),a+32)),paint(V,210,9))
   A.drawLine(J,K+40,C[0],C[1]-20,paint(V,180,7));A.drawPath(I,paint(INK,255,14));R(A,[T,B['eR'],B['hR']],30);R(A,[S,B['eL'],B['hL']],30)
   for U in('eR','eL','kR','kL'):A.drawCircle(B[U][0],B[U][1],26,paint(INK));A.drawCircle(B[U][0],B[U][1],17,paint(col('5a5d4b')))
   W,X,Y=B['head'];E=Y
   if D is not None and t>D:
    E=0
    for(F,(O,P))in enumerate(TWIST):
     Q=TWIST[F-1][1]if F else 0
     if t>=D+O:E=Q+(P-Q)*min(1,(t-D-O)/.06)
    E+=math.sin(t*47)*1.5
   A.save();A.translate(W+N,X);_chupa_head(A,t,E,G);A.restore()
  else:
   L(A,B['hR'][0]+N,B['hR'][1],70 if M<.75 else 80,130,4,22,-40);L(A,B['hL'][0],B['hL'][1]+N,20 if M<.25 else 80,125,4,22,40)
   if M<.25:L(A,B['fR'][0],B['fR'][1],15,110,3,26)
   if M>.75:L(A,B['fR'][0],B['fR'][1],70,120,3,28);L(A,B['fL'][0],B['fL'][1],110,120,3,28)
  A.restore()
 return A
def claw_tips(t=.0):
 def A(cv,x,y,ppm):
  C=cv;H=ppm*.5/1000;C.save();C.translate(x,y);C.scale(H,H);C.drawRect(skia.Rect(-700,-40,700,30),skia.Paint(AntiAlias=True,Color=skia.ColorSetARGB(200,0,0,0),MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,18)))
  for(I,L)in enumerate((-380,380)):
   F=max(0,math.sin(t*1.9+I*2.4))**3
   for(J,K)in enumerate((-150,-50,50,150)):
    A=L+K*(1+.15*F);B=(190+40*(J in(1,2)))*(1+.35*F)+math.sin(t*6+J+I)*6;D=K/150*40
    if F>.2:C.drawLine(A+D*.6,40+B*.9,A+D*.9,40+B*(.9+.5*F),paint(col('cdb894'),int(150*F),6))
    E=skia.Path();E.moveTo(A-30,-10);E.cubicTo(A-34,B*.45,A+D-10,B*.85,A+D+8,B);E.cubicTo(A+D+4,B*.7,A+26,B*.35,A+30,-10);E.close();C.drawPath(E,skia.Paint(AntiAlias=True,Shader=skia.GradientShader.MakeLinear([skia.Point(A,-10),skia.Point(A+D,B)],[c4(col('1c1812')),c4(col('6e6248')),c4(col('d9ccaa')),c4(col('3a3226'))],[0,.3,.78,1])))
    for G in(.25,.45,.62):C.drawLine(A-22+D*G*.3,B*G,A+20+D*G*.3,B*G+6,paint(col('2a2418'),140,4))
    C.drawPath(_q((A+14,B*.1),(A+18,B*.5),(A+D+4,B*.9)),paint(col('fff6dc'),120,5));C.drawPath(E,paint(INK,230,6))
  C.restore()
 return A
def tv(t=.0,chyron='',banner='ÚLTIMA HORA',place='',headline=('TITULAR',''),inset=''):
 O=headline;N=chyron;A=skia.Typeface('Inter',skia.FontStyle.Bold());L=skia.Typeface('Inter',skia.FontStyle(900,5,skia.FontStyle.kUpright_Slant))
 def G(cv,s_,x_,y_,sz,rgb,tf=None,a=255):cv.drawString(s_,x_,y_,skia.Font(tf or A,sz),paint(col(rgb),a))
 def B(cv,x,y,ppm):
  A=cv;P=ppm/1000;A.save();A.translate(x,y);A.scale(P,P);A.drawRect(skia.Rect(-330,-520,330,0),paint(col('4a3220')));A.drawRect(skia.Rect(-330,-520,330,0),paint(INK,255,10))
  for J in(-380,-220,-80):A.drawLine(-320,J,320,J,paint(col('2a1a10'),255,8))
  A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-300,-1000,300,-520),40,40),paint(col('3b3530')));A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-300,-1000,300,-520),40,40),paint(INK,255,10));B,E,F,I=-250,-960,170,-580;Q=skia.RRect.MakeRectXY(skia.Rect(B,E,F,I),40,40);A.save();A.clipRRect(Q,doAntiAlias=True);A.drawRect(skia.Rect(B,E,F,I),skia.Paint(Shader=skia.GradientShader.MakeLinear([skia.Point(0,E),skia.Point(0,I)],[c4(col('1f3d6b')),c4(col('0b1730'))])))
  for K in range(6):A.drawLine(B+K*80,E,B+K*80+60,I,paint(col('2f5a96'),60,18))
  A.drawRect(skia.Rect(-10,-905,150,-790),paint(col('8a97a4')));H=skia.Path();H.moveTo(-10,-810);H.lineTo(30,-850);H.lineTo(60,-835);H.lineTo(95,-870);H.lineTo(150,-825);H.lineTo(150,-790);H.lineTo(-10,-790);H.close();A.drawPath(H,paint(col('3f4c3a')));A.drawRect(skia.Rect(-10,-905,150,-790),paint(col('ffffff'),255,3));G(A,inset,-6,-895,13,'ffffff');D,C=-120,-800;A.drawRect(skia.Rect(D-70,C+20,D+70,C+130),paint(col('1b1d26')));A.drawPath(_p((D-20,C+22),(D+20,C+22),(D,C+60)),paint(col('e8e8ee')));A.drawPath(_p((D-8,C+30),(D+8,C+30),(D+6,C+90),(D-6,C+90)),paint(col('8a1c22')));A.drawRect(skia.Rect(D-12,C+4,D+12,C+24),paint(col('c08f6e')));A.drawOval(skia.Rect(D-42,C-70,D+42,C+18),paint(col('c99a7a')));A.drawPath(_q((D-46,C-30),(D-40,C-92),(D+30,C-80)),paint(col('2a1e16'),255,26))
  for M in(-1,1):A.drawCircle(D+M*15,C-30,5,paint(col('1a1210')));A.drawLine(D+M*15-9,C-44,D+M*15+9,C-46,paint(col('2a1e16'),255,4))
  R=4+5*abs(math.sin(t*11))*(1 if t*1.3%1>.15 else 0);A.drawOval(skia.Rect(D-11,C-4,D+11,C-4+R),paint(col('5a1e1e')));A.drawRect(skia.Rect(B,C+110,F,C+140),paint(col('2c3e5c')));A.drawRRect(skia.RRect.MakeRectXY(skia.Rect(B+22,E+18,B+128,E+50),6,6),paint(col('ffffff'),230));G(A,'NOTI',B+30,E+42,22,'1a3a7a',L);G(A,'ZAC',B+84,E+42,22,'c4161c',L)
  if int(t*1.6)%2==0:A.drawCircle(B+150,E+34,7,paint(col('ff2020')))
  G(A,'EN VIVO',B+162,E+42,18,'ffffff');A.drawRect(skia.Rect(B,-712,B+150,-686),paint(col('c4161c')));G(A,banner,B+10,-692,18,'ffffff',L);A.drawRect(skia.Rect(B,-686,F,-632),paint(col('f4f4f4')));G(A,O[0],B+10,-664,21,'111111',L);G(A,O[1],B+10,-640,17,'333333');A.drawRect(skia.Rect(B,-632,F,-606),paint(col('0e1c38')));S=t*60%1500;G(A,N+'   •   '+N,F-S,-613,16,'e6ecff');A.drawRect(skia.Rect(F-70,-632,F,-606),paint(col('c4161c')));G(A,'07:12',F-62,-613,16,'ffffff')
  for J in range(E,I,5):A.drawLine(B,J,F,J,paint(col('000000'),22,1.5))
  A.drawRect(skia.Rect(B,E,F,I),paint(col('9fc4ff'),int(8+6*math.sin(t*40))));A.drawRect(skia.Rect(B,E,F,I),skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point((B+F)/2,(E+I)/2),300,[skia.ColorSetARGB(0,0,0,0),skia.ColorSetARGB(120,0,0,0)])));A.restore();A.drawRRect(Q,paint(INK,255,10));A.drawPath(_q((B+40,E+30),(B+160,E+5),(B+260,E+40)),paint(col('ffffff'),40,14))
  for K in range(3):A.drawCircle(235,-900+K*90,22,paint(col('1c1816')));A.drawCircle(235,-900+K*90,22,paint(INK,255,6))
  A.drawLine(-80,-1000,-200,-1220,paint(INK,255,8));A.drawLine(60,-1000,180,-1240,paint(INK,255,8));A.restore()
 return B
