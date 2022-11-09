import numpy as np
import numba as nb

@nb.njit( (nb.double[:,:], nb.double[:,:], nb.double) )
def collisions(r,v,collision_radius2):
    """Resolve pairwise collisions"""
    N = len(r)
    for i in range(N-1):
        for j in range(i+1,N):
            dr2 = ((r[i]-r[j])**2).sum()
            if dr2<collision_radius2:
                # collision rule for equal masses
                v[i] = v[i] - np.dot(v[i]-v[j],r[i]-r[j])/dr2*(r[i]-r[j])
                v[j] = v[j] - np.dot(v[j]-v[i],r[j]-r[i])/dr2*(r[j]-r[i])

class System:
    """ Gas of particles with unit mass"""

    def __init__(self,N,L,T =1.0, ndim=2, radius=0.5, vmax=1.5, delta=False):
        """ Setup the gas with random  positions """

        self.N = N
        self.L = L
        self.ndim = ndim
        self.T = T

        self.r = np.random.uniform(0,self.L, size=(self.N,self.ndim))

        if delta:
            self.v = np.ones_like(self.r)
        else:
            self.v = np.random.uniform(-vmax,vmax,self.r.shape)

        Ttemp = 2*(self.v**2).mean()/self.ndim
        self.v = self.v*np.sqrt(T/Ttemp)

        self.collision_radius2 = radius**2
        self.collision_radius = radius


    def evolve(self,dt):
        """Time evolution of the particles, with resolution of pairwise colisions"""

        self.r = self.r +self.v*dt
        # inter-particle collisions
        collisions(self.r,self.v,self.collision_radius2)
        # wall collisions
        test0,testL= self.r<=0, self.r>=self.L
        self.r[test0]*=-1
        self.v[test0]*=-1
        self.r[testL]=2*self.L-self.r[testL]
        self.v[testL]*=-1

    def theory(self):
        """Maxwell-Boltzmann distribution"""
        if self.ndim ==2:
            s = np.linspace(0,10,100)
            ps = s/self.T*np.exp(-s**2/(2*self.T))
            return s,ps




def matplot_view(system,dt=0.001,steps=200):
    import matplotlib.pyplot as plt
    from matplotlib import animation

    L = system.L
    fig,(ax1, ax2)= plt.subplots(1,2,figsize=(8.5,4))

    ax1.spines["top"].set_visible(True)
    ax1.spines["right"].set_visible(True)
    pts, = ax1.plot([], [], 'o', ms=3.0, alpha=0.4, mec="k", mew=0.5)
    hist, = ax2.plot([],[],'go',ms=2.)
    vl = ax2.vlines([],[],[],'g')
    ax2.plot(*system.theory(),'r-')
    plots = [pts, hist,vl]
    edges = np.linspace(0,5,64)


    ax1.axis("equal")
    ax1.set_xlim((0,L))
    ax1.set_ylim((0,L))
    ax2.set_xlim(0,5)
    ax2.set_ylim(0,1.5)
    ax2.set_xlabel("v")
    ax2.set_ylabel("P(v)")

    cumul,edg = np.histogram(np.linalg.norm(system.v, axis=1),bins=edges,density=True)

    count = 1

    def animate(i):
        nonlocal cumul
        nonlocal count
        system.evolve(dt)
        r = system.r
        pts.set_data(r[:,0],r[:,1])
        # print(r[r>L])

        H,e = np.histogram(np.linalg.norm(system.v, axis=1),bins=edges,density=True)
        centers = e[:-1]+0.5*(e[1]-e[0])
        zeros = np.zeros_like(centers)

        cumul += H
        count+=1

        hist.set_data(centers,cumul/count)

        vpoints = [ [(c,0),(c,h)] for c,h in zip(centers,cumul/count)]
        vl.set_segments(vpoints)
        return plots

    anim = animation.FuncAnimation(fig, animate,frames=steps,  interval=1, blit=True)
    return anim
    # plt.show()
