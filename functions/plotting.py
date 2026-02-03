import sys 
sys.path.append("./functions")
import functions as fn 
import numpy as np 
from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Wedge
import time

def plot(space, file=time.time(),dpi = 100):
    fig, ax = plt.subplots()
    for i in space.boundary_regions:
        add_line(i, ax)
    q = plot_flockers(space,ax)
    ax.autoscale_view()
    fig.savefig("./figs/"+str(file)+".png", dpi=dpi)

def plot_flockers(space, axes):
    pr = np.array([np.real(space.manifest.pos_master)])
    pi = np.array([np.imag(space.manifest.pos_master)])
    vr = np.array([np.real(space.manifest.vel_master)])
    vi = np.array([np.imag(space.manifest.vel_master)]) 
    ang = np.angle(space.manifest.vel_master)
    quiv = axes.quiver(pr, pi,vr,vi, (ang /(2*np.pi)))
    return quiv

def add_line(region, axes):
    patches = []
    if region.type == "rectangle":
        axes.plot(np.real([region.origin,region.points[1]]),
                  np.imag([region.origin,region.points[1]]))
    elif region.type == "circle":
        patches += [
                  Wedge((region.origin.real,region.origin.imag),
                        region.radius, rtd(region.arc[0]), rtd(region.arc[1]),width=0.03)
                  ]
        p = PatchCollection(patches)
        axes.add_collection(p)
    elif region.type == "ring":
        patches += [
                  Wedge((region.origin.real,region.origin.imag),
                        region.radius_inner, rtd(region.arc[0]), rtd(region.arc[1]), width=0.03)
                  ]
        p = PatchCollection(patches)
        axes.add_collection(p)
    else:
        print("Region type not recognized")

def rtd(ang):
    return ang * 360 / (2*np.pi)

def plot_gen2(manifest, file=time.time(),dpi = 100):
    fig, ax = plt.subplots()
    for i in manifest.lines:
        add_line_gen2(i, ax)
    q = plot_flockers_gen2(space,ax)
    ax.autoscale_view()
    fig.savefig("./figs/"+str(file)+".png", dpi=dpi)

def add_line_gen2 = (line, axes):
    axes.plot(np.real(line.x), np.imag(line.x))

def plot_flockers_gen2(manifest, axes):
    pr = np.array([np.real(manifest.pos)])
    pi = np.array([np.imag(manifest.pos)])
    vr = np.array([np.real(manifest.vel)])
    vi = np.array([np.imag(manifest.vel)]) 
    ang = np.angle(manifest.vel)
    quiv = axes.quiver(pr, pi,vr,vi, (ang /(2*np.pi)))
    return quiv
2
