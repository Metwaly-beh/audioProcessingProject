#I will now start my signals project using VScode
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft
#from scipy.io.wavfile import write



#defining x
def x(t):
    N=4
    Fi=[130.81,164.81,196.00,220.00]
    fi=[261.63,329.63,392.00,440.00]
    ti=[0.0,1.0,1.75,2.5]
    Ti=[1,0.75,0.75,0.5]
    x= np.zeros(len(t))
    for i in range(N):
     x+=((np.sin(2*np.pi*Fi[i]*t)+np.sin(2*np.pi*fi[i]*t))*(u(t-ti[i])-u(t-ti[i]-Ti[i])))
    return x

#unitstep function here to make second part of signal
def u(t):
  return np.where(t >= 0, 1, 0)

t = np.linspace(0, 3, 3 * 44100 )


x_t= x(t)
#ploting the signal and hearing the sound it made
plt.plot(t[::100], x_t[::100], linewidth=0.5)
plt.ylabel("amplitude")
plt.xlabel("time")
plt.title("original wave")
sd.play(x_t, 3 * 44100 )
plt.show()
#part 1&2 end here

#this is part 3&4 start







#generating noise

def n(t):
   fn1=np.random.randint(0,512)
   fn2=np.random.randint(0,512)
   n=np.sin(2*np.pi*fn1*t)+np.sin(2*np.pi*fn2*t)
   return n

#generating noisy wave
n_t = n(t)
xn_t = x_t + n_t

def xn(t):  # keep this function but no longer used
   return x(t)+n(t)

#plotting noisy signal and hearing it
plt.plot(t[::100], xn_t[::100], linewidth=0.5)
plt.ylabel("amplitude")
plt.xlabel("time")
plt.title("noisy wave")
sd.play(xn_t, 3 * 44100 )
plt.show()


#computing frequency domain of both signals and plotting them


N = 3 * 44100
f = np.linspace(0, 44100/2, int(N/2))

xf=fft(x_t)
xf = 2/N * np.abs(xf[0:int(N/2)])

xnf=fft(xn_t)
xnf = 2/N * np.abs(xnf[0:int(N/2)])

plt.plot(f[(f>=0)&(f<=512)], xf[(f>=0)&(f<=512)], linewidth=0.5)
plt.ylabel("amplitude")
plt.xlabel("frequency")
plt.title("original wave fourier")
plt.show()


plt.plot(f[(f>=0)&(f<=512)], xnf[(f>=0)&(f<=512)], linewidth=0.5)
plt.ylabel("amplitude")
plt.xlabel("frequency")
plt.title("noisy wave fourier")
plt.show()


#cleaning


   #get the noise
def clean(a,f,w,t):
   max=0
   max2=0
   max1_idx = 1
   max2_idx = 1
   for i in range(len(a)):
      if a[i] > max:
        max2 = max
        max2_idx = max1_idx
        max = a[i]
        max1_idx = i
        
   
   f1 = int(f[max1_idx])
   f2 = int(f[max2_idx])

   z=np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
   return (w-z)

      

xclean = clean(xnf,f,xn_t,t)  

plt.plot(t[::100], xclean[::100], linewidth=0.5)
plt.ylabel("amplitude")
plt.xlabel("time")
plt.title("cleaned wave")
sd.play(xclean, 3 * 44100 )
plt.show()

xcleanf=fft(xclean)
xcleanf= 2/N * np.abs(xcleanf[0:int(N/2)])

plt.plot(f[(f>=0)&(f<=512)], xcleanf[(f>=0)&(f<=512)], linewidth=0.5)
plt.ylabel("amplitude")
plt.xlabel("frequency")
plt.title("cleaned wave fourier")
plt.show()
