"""Build exact, original teaching figures. Run from any directory; requires numpy/matplotlib."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
parser=argparse.ArgumentParser()
parser.add_argument("--preview-dir", type=Path, help="Optional directory for PNG previews")
args=parser.parse_args()
if args.preview_dir:
 args.preview_dir.mkdir(parents=True, exist_ok=True)
R=Path(__file__).resolve().parents[1]
OUT=R/'docs/course_20h/assets'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','svg.hashsalt':'micro-course-20260905','figure.facecolor':'#f7f9fc','axes.facecolor':'white'})
BLUE='#2468b4';RED='#d55244';GREEN='#278477';GOLD='#d89a20'
def setup(ax,title,xlabel='Quantity Q (units / period)',ylabel='Price P (currency / unit)',xlim=(0,100),ylim=(0,65)):
 ax.set(title=title,xlabel=xlabel,ylabel=ylabel,xlim=xlim,ylim=ylim);ax.grid(alpha=.15);ax.set_axisbelow(True)
def save(fig,name):
 fig.tight_layout(pad=2);fig.savefig(OUT/(name+'.svg'),metadata={'Date':None})
 if args.preview_dir:fig.savefig(args.preview_dir/(name+'.png'),dpi=130)
 plt.close(fig)
def point(ax,x,y,label,offset=(7,9)):
 ax.plot(x,y,'o',color='#233248',ms=5);ax.annotate(label,(x,y),xytext=offset,textcoords='offset points',fontsize=10)
q=np.linspace(0,100,201)
d=50-.5*q;s=10+.5*q
fig,axs=plt.subplots(1,2,figsize=(12,4.9))
for a in axs: setup(a,'')
axs[0].set_title('A: movement along the same demand curve')
axs[0].plot(q,d,color=BLUE,label='D: P = 50 - 0.5Q');point(axs[0],40,30,'A (40, 30)');point(axs[0],60,20,'B (60, 20)')
axs[0].annotate('',(58,21),(43,28),arrowprops={'arrowstyle':'->','color':RED,'lw':2});axs[0].legend(loc='upper right',fontsize=9)
axs[1].set_title('B: demand shifts; supply stays fixed')
axs[1].plot(q,d,color=BLUE,label='D0');axs[1].plot(q,60-.5*q,color=BLUE,ls='--',label='D1');axs[1].plot(q,s,color=RED,label='S')
point(axs[1],40,30,'E0 (40, 30)',(-92,-22));point(axs[1],50,35,'E1 (50, 35)');axs[1].legend(loc='upper right',fontsize=9)
save(fig,'demand_movement_shift')
fig,axs=plt.subplots(1,2,figsize=(12,5.1))
for a in axs:
 setup(a,'',xlim=(0,90),ylim=(0,60));a.plot(q,d,color=BLUE,label='D');a.plot(q,s,color=RED,label='S')
a=axs[0];a.set_title('Before tax: P = 30, Q = 40');x=np.linspace(0,40,80)
a.fill_between(x,30,50-.5*x,color=BLUE,alpha=.2);a.fill_between(x,10+.5*x,30,color=GREEN,alpha=.2);a.text(8,36,'CS = 400');a.text(8,21,'PS = 400');point(a,40,30,'E')
a=axs[1];a.set_title('Unit tax 10: buyer pays 35, seller gets 25');x=np.linspace(0,30,80)
a.fill_between(x,35,50-.5*x,color=BLUE,alpha=.2);a.fill_between(x,10+.5*x,25,color=GREEN,alpha=.2);a.fill_between(x,25,35,color=GOLD,alpha=.27)
x=np.linspace(30,40,30);a.fill_between(x,10+.5*x,50-.5*x,color=RED,alpha=.35)
a.text(4,41,'CS = 225');a.text(4,28,'Tax = 300');a.text(4,19,'PS = 225');a.annotate('DWL = 50',(35,30),xytext=(52,40),arrowprops={'arrowstyle':'->'});a.vlines(30,25,35,color='#233248',lw=2)
for y in [25,35]:a.axhline(y,color='#8992a1',ls=':',lw=.8)
save(fig,'surplus_tax')
fig,ax=plt.subplots(figsize=(8,5.2));setup(ax,'External cost 10: market Q = 40; social optimum Q = 30',xlim=(0,75),ylim=(0,65))
ax.plot(q,d,color=BLUE,label='MB = 50 - 0.5Q');ax.plot(q,s,color=GREEN,label='MPC = 10 + 0.5Q');ax.plot(q,s+10,color=RED,label='MSC = MPC + 10')
x=np.linspace(30,40,30);ax.fill_between(x,50-.5*x,20+.5*x,color=RED,alpha=.25,label='Avoidable welfare loss = 50');point(ax,30,35,'Social optimum',(-123,14));point(ax,40,30,'Market');ax.legend(loc='upper right',fontsize=9);save(fig,'externality')
fig,ax=plt.subplots(figsize=(8,5.2));x=np.linspace(.65,7,300);avc=10-2*x+x*x;atc=avc+4/x;mc=10-4*x+3*x*x
setup(ax,'Costs: VC = 10Q - 2Q² + Q³; FC = 4',xlim=(0,5),ylim=(0,40),ylabel='Cost per unit (currency / unit)')
ax.plot(x,avc,color=GREEN,label='AVC');ax.plot(x,atc,color=BLUE,label='ATC');ax.plot(x,mc,color=RED,label='MC');point(ax,1,9,'Minimum AVC (1, 9)',(10,-22))
qmin=next(float(z.real) for z in np.roots([1,-1,0,-2]) if abs(z.imag)<1e-9 and z.real>0);ymin=10-2*qmin+qmin*qmin+4/qmin;point(ax,qmin,ymin,'MC = ATC at minimum ATC',(30,10));ax.legend(loc='upper left');save(fig,'cost_curves')
fig,ax=plt.subplots(figsize=(8,5.2));x=np.linspace(0,60,200)
setup(ax,'Single-price monopoly: choose Q first, then read P',xlim=(0,60),ylim=(0,110))
ax.plot(x,100-2*x,color=BLUE,label='Demand: P = 100 - 2Q');ax.plot(x,100-4*x,color=RED,label='MR = 100 - 4Q');ax.axhline(20,color=GREEN,label='MC = 20')
ax.vlines(20,20,60,color='#233248',ls=':');point(ax,20,20,'MR = MC',(10,-22));point(ax,20,60,'Monopoly: Q = 20, P = 60');point(ax,40,20,'P = MC',(6,8));x=np.linspace(20,40,50);ax.fill_between(x,20,100-2*x,color=GOLD,alpha=.2,label='DWL = 400');ax.legend(loc='upper right',fontsize=9);save(fig,'monopoly')
fig,ax=plt.subplots(figsize=(8,5.1));x=np.arange(1,5);v=np.array([600,480,360,240]);setup(ax,'Hiring with price-taking output and labor markets',xlabel='Worker number (equal work periods)',ylabel='Extra revenue / wage (currency per period)',xlim=(.4,4.7),ylim=(0,700));ax.bar(x,v,color=BLUE,alpha=.7,width=.55,label='VMPL = P × MPL');ax.axhline(400,color=RED,label='Wage = 400')
for a,b in zip(x,v):ax.text(a,b+13,str(b),ha='center')
ax.text(2.4,620,'P = 20; MPL = 30, 24, 18, 12',ha='center');ax.set_xticks(x);ax.legend(loc='upper right',bbox_to_anchor=(1,0.84),fontsize=9);save(fig,'labor_marginal')
fig,axs=plt.subplots(1,2,figsize=(12,5.3));x=np.linspace(.1,125,500)
for ax in axs:setup(ax,'',xlabel='Good X (units)',ylabel='Good Y (units)',xlim=(0,125),ylim=(0,130))
a=axs[0];a.set_title('Budget: 4x + y ≤ 120');x0=np.linspace(0,30,100);a.fill_between(x0,0,120-4*x0,color=BLUE,alpha=.12);a.plot(x0,120-4*x0,color=BLUE,label='4x + y = 120');a.plot(x,900/x,color=GREEN,label='xy = 900');point(a,15,60,'A (15, 60)');a.legend(loc='upper right',fontsize=9)
a=axs[1];a.set_title('Hicks decomposition: price of X falls 4 → 1');a.plot(x,120-4*x,color=BLUE,label='Old budget');a.plot(x,120-x,color=RED,label='New budget');a.plot(x,60-x,color=GOLD,ls='--',label='Compensated budget');a.plot(x,900/x,color=GREEN,alpha=.8,label='Old utility: xy = 900');a.plot(x,3600/x,color=GREEN,ls=':',label='New utility: xy = 3600')
point(a,15,60,'A',(6,10));point(a,30,30,'B',(6,0));point(a,60,60,'C',(6,9));a.annotate('',(29,32),(16,58),arrowprops={'arrowstyle':'->','color':GOLD,'lw':2});a.annotate('',(58,58),(32,32),arrowprops={'arrowstyle':'->','color':RED,'lw':2});a.legend(loc='upper right',fontsize=8);save(fig,'consumer_hicks')
