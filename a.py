#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib import animation as animation
import math

class Pendulo:
	def __init__(self, massa, comprimento, theta, vangular):
		self.m=massa
		self.l=comprimento
		self.x=theta
		self.v=vangular
		self.wo=math.sqrt(g/comprimento)
		self.T=2*math.pi*math.sqrt(comprimento/g)
		self.E= 0.5*self.m*(self.l*self.v)**2 + self.m*g*self.l*(1-math.cos(self.x))
	
	def a(self,x,v,t):
		return(-self.wo**2*math.sin(x)-gama*v+A*math.sin(wf*t))
		
	def movimento(self, t):
		at=self.a(self.x, self.v, t)
		self.x=self.x + self.v*dt+0.5*at*dt**2
		atem=self.a(self.x,self.v,t)
		vtemp=self.v+0.5*(at+atem)*dt
		atemp=self.a(self.x,vtemp, t)
		self.v=self.v+0.5*(at+atemp)*dt
		self.at=self.a(self.x, self.v, t)
		self.E=0.5*self.m*(self.l*self.v)**2 + self.m*g*self.l*(1-math.cos(self.x))

g=9.8
gama=0
A=0
wf=2.0/3.0
t=0.0
dt=0.2

p1=Pendulo(1., 10., math.pi/6., 0)
p2=Pendulo(1.,10.,math.pi/6-1e4,0)

tmax=20*p1.T


t=np.arange(0, tmax, dt)


x1=np.zeros(t.size)
v1=np.zeros(t.size)
E1=np.zeros(t.size)

x2=np.zeros(t.size)
v2=np.zeros(t.size)
E2=np.zeros(t.size)

difx=np.zeros(t.size)
difv=np.zeros(t.size)
dife=np.zeros(t.size)


x1[0]=(p1.x+np.pi)%(2*np.pi)-np.pi
v1[0]=p1.v
E1[0]=p1.E

x2[0]=(p2.x+np.pi)%(2*np.pi)-np.pi
v2[0]=p2.v
E2[0]=p2.E



for i in range(t.size):
	p1.movimento(t[i])
	p2.movimento(t[i])
	x1[i]=(p1.x+np.pi)%(2*np.pi)-np.pi
	v1[i]=p1.v
	E1[i]=p1.E
	
	
	x2[i]=(p2.x+np.pi)%(2*np.pi)-np.pi
	v2[i]=p2.v
	E2[i]=p2.E

	difx[i]=math.fabs(x1[i]-x2[i])
	difv[i]=math.fabs(v1[i]-v2[i])
	dife[i]=math.fabs(E1[i]-E2[i])



fig = plt.figure()
plt.title('Pendulo Simples', fontsize=12)

XxT=fig.add_subplot(331, xlim=(0, tmax), ylim=(min(x1)-0.1, max(x1)+0.1))
XxT.xaxis.grid(True)
XxT.yaxis.grid(False)
plt.setp(XxT.get_xticklabels(), visible=False)
plt.xlabel('Tempo(s)')
plt.ylabel('Posicao(m)')
plt.grid()
line1, = XxT.plot([], [], 'm-', lw=2, label="$x_{(t)}$")
plt.legend(loc='upper right')

VxT=fig.add_subplot(334, xlim=(0, tmax), ylim=(min(v1)-0.1, max(v1)+0.1))
VxT.xaxis.grid(True)
VxT.yaxis.grid(False)
plt.setp(VxT.get_xticklabels(), visible=False)
plt.xlabel('Tempo(s)')
plt.ylabel('Velocidade(m/s)')
line2, = VxT.plot([], [], 'y-', lw=2, label="$v_{(t)}$")
plt.legend(loc='upper right')

ExT=fig.add_subplot(337, xlim=(0, tmax), ylim=(min(E1)-0.005, max(E1)+0.005))
plt.xlabel('Tempo(s)')
plt.ylabel('Energia(J)')
line3, = ExT.plot([], [], 'b-', lw=2, label="$e_{(t)}$")
plt.legend(loc='upper right')

EF=fig.add_subplot(122, xlim=(min(x1)-0.1, max(x1)+0.1), ylim=(min(v1)-0.1, max(v1)+0.1))
plt.xlabel('Posicao(m)')
plt.ylabel('Velocidade(m/s)')
line4, = EF.plot([], [], 'c.', lw=2, label="X x V")
plt.legend(loc='upper right')

def init():
	line1.set_data([],[])
	line2.set_data([],[])
	line3.set_data([],[])
	line4.set_data([],[])
	return line1, line2, line3, line4,
	
def animate(i):
	x=t[:i]
	y=x1[:i]
	z=v1[:i]
	ene=E1[:i]
	line1.set_data(x, y)
	line2.set_data(x, z)
	line3.set_data(x, ene)
	line4.set_data(y, z)
	return line1, line2, line3, line4,
		
anim=animation.FuncAnimation(fig, animate, init_func=init, frames=t.size+4,
interval=0, blit=True)

anim.save('pendulosimples.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
