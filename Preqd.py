# -*- coding: utf-8 -*-
"""
FHWwallDesignSCR

This script finds the value of the force required to mantain stability of a 
slope (Preqd), maximizing the failure surface's angle (alpha) and the d/H
relation (xi). Additionally, calculates the safety factor of the sliding
wedge that was found by the FHWA's simplified method.

Created on Mon Sep 21 09:05:48 2020

Copyright (R) 2020 E. Jaramillo-Rincon & Universidad Nacional de Colombia.
License BSD-2

"""
## Force Preqd

# Los parámetros que utiliza la función son:

# gm = Peso unitario del suelo [kN/m3]
# H = Altura, con respecto a la superficie del terreno de confinamiento
# pasivo, de la pared de retención [m]
# d = Distancia debajo de la superficie del terreno por donde pasa la
# superficie de falla [m]
# xi = Relación d/H [ad]
# beta = Ángulo en radianes de la superficie del terreno detrás de la
# estructura de retención
# kp = Coeficiente de presión pasiva [ad]
# delta = Ángulo de fricción en la interface [rad]
# phi = Ángulo de fricción  interna del suelo [rad]

import numpy as np
import scipy.optimize as opt
import sympy as sym
import shapely.geometry as shp
import matplotlib.pyplot as plt

# Constant parameters:

# gm = Unit weight of soil [kN/m3]
gm = 22;
print("-The unit weight of soil (\u03B3) is %.6s [kN/m^3]" % (gm))
# H = Height of the retaining wall [m]
H = 2;
print("-The height of the retaining wall (H) is %.6s [m]" % (H))
# beta = Angle respect of the horizontal of the land's surface behind the 
# retaining wall [rad]
beta = np.deg2rad(22);
print("-The angle of the land's surface behind the wall (\u03B2) is %.6s [rad]" % (beta))
# kp = Passive earth pression coefficient [ad] took from Kerisel y ABSI's values
kp = 7; 
print("-The passive earth pression coefficient (Kp) is %.6s" % (kp) )
# delta = Friction angle at the soil-wall interface  {rad}
delta = np.deg2rad(23);
print("-The soil-wall interface friction angle (\u03B4) is %.6s [rad]" % (delta))
# phi = Internal friction angle of the soil [rad]
phi = np.deg2rad(23);
print("-The internal friction angle of the soil (\u03C6) is %.6s [rad]" % (phi))
# Cohesion of the soil [kPa]
c = 5
print("-The cohesion of the soil (c) is %.6s [kPa]" % (c))

def preqd(x):
    # The fuction preqd return the value of the force required [kN/m] 
    # for the retaining wall's equilibrium.
    # Entry is a 2x1 vector containing the value of xi (x[0]) and alpha (x[1])
    
    fn = 0.5 * gm * (H**2) * \
    ((((1 + x[0])**2) / (np.tan(x[1]) - np.tan(beta))) - kp * \
     (x[0]**2) * (np.sin(delta) + (np.cos(delta) / (np.tan((x[1]) - phi))))) *\
     np.tan(x[1] - phi);
     
    return fn

def objective(x):
    # This function defines the function "predq" as the objective fuction
    # The return is negative so that it can be a maximization problem
    return -preqd(x) 


# Bounds for  xi
supBoundxi = np.inf
infBoundxi = 0

# Bounds for alpha
supBoundalpha = np.deg2rad(90)
infBoundalpha = phi

# Error function
erf = 0.01

# Define the inferior and superior bound of the variables xi and alpha
varbounds = opt.Bounds([infBoundxi + erf, infBoundalpha + erf],\
                       [supBoundxi, supBoundalpha])

# Initial assumptions

x0xi = 0.01
x0alpha = 0.2
x0 = np.array([x0xi, x0alpha])

# Solve the optimization problem
res = opt.minimize(objective, x0, bounds=varbounds)

xi = res.x[0]
alpha = res.x[1]
PreqdMax = preqd(res.x)

print("-The values of xi=%.6s and alpha=%.6s [rad] maximize the value of the force\
 required to stabilize the wall, Preqd = %.6s [kN/m]" % (xi, alpha,PreqdMax))

## Safety factor

# Wedge's dimensions

# Total Height with embedment [m]
Ht = H * (1 + xi) 
dEmp = H * xi
print("-The total height with the embedment (d) is %.6s [m]" % (Ht))

# Intersection between failure surface and land's surface
xeq=sym.Symbol('xeq')

# Land's surface line
yterreno = np.tan(beta) * xeq + Ht; 
# Failure surface line
yfalla = np.tan(alpha) * xeq; 

# Find the abscissa of the intersection point
xint = sym.solve(np.tan(beta) * xeq + Ht - (np.tan(alpha) * xeq), xeq)
# The ordinate of the intersection point [m]
yint = yterreno.evalf( subs={xeq:xint[0]})
# Lenght of land's surface [m]
lterreno = xint/np.cos(beta)
# Lenght of failure surface [m]
lfalla = xint/np.cos(alpha)
# Height of the triangle defined by the wedge [m]
hcuna = Ht * np.sin((np.pi/2) - alpha)
# Area of the sliding wedge [m^{2}]
AreaCuna = hcuna * lfalla/2 
# Angle between Preqd and the perpendicular line to the failure surface
thetat = (np.pi/2) - alpha; 

# Weight of the sliding wedge [kN/m]
W = AreaCuna*gm

# Safety factor
FS = (c * lfalla + np.tan(phi) * (W * np.cos(alpha) + PreqdMax * np.cos(thetat)))/\
(W * np.sin(alpha) - PreqdMax * np.sin(thetat))

print("-The factor of safety is %.6s" % (FS[0]))

# Drawing with Shapely
Wedge = shp.Polygon([(0,0), (0,round(Ht,2)), (round(xint[0],2),round(yint,2)), (0,0)])
GroundSurface = shp.LineString([(-10 , dEmp) , (0 , dEmp)])

# Separate de values of wedge's abscissas and ordinates
x,y = Wedge.exterior.xy
x1,y1 = GroundSurface.coords.xy
plt.fill(x,y,'lightgray')
# Plot the values of wedge's abscissas and ordinates
plt.plot(x,y, "gray", x1, y1, 'gray')
# Labelling the graphic
labels = Wedge.exterior.coords
for label, x, y in zip(labels, x, y):
       plt.annotate(
           label,
           xy=(x, y), xytext=(0, 0),
           textcoords='offset pixels', ha='right', va='center')
# Define the limits of the plotting space
plt.xlim([-5,15])
plt.ylim([-1,7])

ax = plt.gca() #you first need to get the axis handle
ax.set_aspect('equal')

textGamma = r'$\gamma = %.2s$' % (gm)
textPhi = r'$\varphi = %.2s$°' % (np.rad2deg(phi))
textDelta = r'$\delta = %.2s°$' % (np.rad2deg(delta))
textAlpha = r'$\alpha = %.2s°$' % (np.rad2deg(alpha))
plt.text(10, 5, textGamma, fontsize=12)
plt.text(10,4, textPhi, fontsize=12)
plt.text(10,3, textDelta, fontsize=12)
plt.text(10,2, textAlpha, fontsize=12)
plt.show()






