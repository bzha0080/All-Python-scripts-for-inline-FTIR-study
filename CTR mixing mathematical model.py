import math

V1 = 0.5 # starting monomer concentration of the gradient in mol/L
V2 = 5 # End monomer concentration of the gradient in mol/L
T = 10*60 # monomer concentration changing time in seconds
F = 15 # flow rate of the fluid in ul/sec
V = 50 # volume of the IR chamber in uL (volume of CSTR without stirring) 
alpha = 0.00344 # /(sec uL) for Methyl acrylate in DMSO at room temperature only.
k = alpha*F
print (type(V1), type(V2), type(T), type(F), type(V), type(alpha), type(k))

'''
The flow dynamic in the IR head is more like a Continuous Stirred Tank Reactor (CSTR) without stirring.
For all the liqiud flows into the IR chamber to be analyzed, the process can be clearified as two stages

Stage 1: Concentration linearly increasing from V1 to V2; during this stage, the input concentration at any specific time can be represented as
    Concentration at any time t (0<t<T): V(t) = V1 + (V2-V1)*t/T

Stage 2: Concentration fixed at V2: the concentration at any time in this stage can be represented using mass balance as:
    dc/dt = k (V(t)-C(t))    

Solution for the above concentrations:

Stage 1: 
dc/dt + kC(t) = kV(t), substituting V(t) = V1 + (V2-V1)*t/T
dc/dt +kC(t) = k(V1+(V2-V1)*t/T)
  Solve the homogeneous equation:
          dc/dt + kC(t) = 0, get Ch(t) = Ce^{-kt}
  Find a particular solution:
        The right hand side is linear function, assume a particular solution of the form: 
           Cp(t) = At+B, substituting into the equation A + k(At+B) = kV1 + (V2-V1)*t/T
           kA = k(V2-V1)/T, giving A = (V2-V1)/T
           A + kB = kV1, giving B = V1-A/k = V1 - (V2-V1)/(kT)
           so, the general solution for C(t) = Ch(t) + Cp(t) = Ce^{-kt} + (V2-V1)*t/T + V1 - (V2-V1)/(kT)
           Apply initial conditions C(0) = V1, giving C = (V2-V1)/(kT)

           Thus C(t) = V1 + (V2-V1)/T*(t-1/k) + [-V1 + (V2-V1)/(kT)]e^{-kt} 

Stage 2:
dc/dt = k(V2-C(t)), giving dc/(V2-C) = kdt  #C is concentration at end of stage 1
      integral on both sides giving C(t) = V2 - Ce^{-kt}
      Applying inital conditions C(T) = V2 - Ce^{-kT}, solving C = (V2-C(T))e^{-kT}
      Giving the final formula of C(t) = V2-(V2-C(T))e^{-k(t-T)} 
'''

C_t1 = round(V1 + (V2-V1)*(T- 1/k)/T + (-V1 + (V2-V1)/(k*T))*math.exp(-k*T),2)

print(f'the concentration at the end of the sweeping T is {C_t1}')

# the time need to reach 97% of the desired concentration
C_T = V1 + (V2-V1)/T*(T-1/k) + (-V1 + (V2-V1)/(k*T)) * math.exp(-k*T)
C_t2 = 0.97 * V2

t2 = round(T + math.log((V2-C_t2)/(V2-C_T))/(-k),1)

print (f'the time needed to each 97% of desired concentration ({V2} mol/L) is {t2} seconds')                