__version__ = '1'
__date__    = '12Apr2018'
__author__  = 'Y. Litman'
__name__    = 'Spec'


import numpy as np
import time
import sys


def acf(f,lag=2000,window=2,conv=True):
    """My own interface to scipy"""
    from scipy import signal
    import numpy as np

    f2 = np.concatenate((f,np.zeros((f.shape[0],f.shape[1])))) ##This is needed due how scipy computes the ACF (it rolls)

    if not conv:
        acf = signal.correlate(f2,f ,mode="valid",method='direct')[:-1]  #Usually we need only the sum  
    else:
        acf= signal.correlate(f2,f,mode="valid")[:-1] #Usually we need only the sum  

    #Normalize
    acf = np.divide(acf.flatten(), np.flip(np.arange(1,acf.size+1),axis=0) )
    #Select window
    if window==1:
        win = np.blackman(2*lag)
    elif window==2:
        win = np.hanning(2*lag)
    elif window==3:
        win = np.hamming(2*lag)
    elif window==4:
        win = np.bartlett(2*lag)
    else:
        win=np.ones(2*lag)

    #Apply window
    acf  = np.multiply(acf[:lag],win[lag:])


    return acf


def acf_old(f,conv=False,lag=0):
   """My own interface to scipy"""
   from scipy import signal

   print('')
   if conv:
      print('@ACF: Using Convolution theorem')
   else:
      print('@ACF: Using direct method')
   print('')

   if lag == 0:
      zeros=f.shape[0]
   else:
      zeros=lag
   
   t0= time.clock()
   f2=np.concatenate((f,np.zeros((zeros,f.shape[1])))) ##This is needed due how scipy computes the ACF (it rolls)

   if not conv:
       #acf1= signal.correlate(f2[:,0],f[:,0],mode="valid")
       #acf2= signal.correlate(f2[:,1],f[:,1],mode="valid")
       #acf3= signal.correlate(f2[:,2],f[:,2],mode="valid")
       acf= signal.correlate(f2,f ,mode="valid",method='direct')  #Usually we need only the sum  
       t1= time.clock()
   else:
     #Computes the ac applying the convolution theorem.
     #acf1= signal.correlate(f2[:,0],f[:,0],mode="valid")
     #acf2= signal.correlate(f2[:,1],f[:,1],mode="valid")
     #acf3= signal.correlate(f2[:,2],f[:,2],mode="valid")
     acf= signal.correlate(f2,f,mode="valid")#Usually we need only the sum  
     t1= time.clock()

     print('The acf calculation duration was {}'.format(t1-t0))
 
   #Normalize:
   acf = acf/f.size
    
   #return acf1+acf2+acf3
   return acf


def FT(ft,step=1.0,nzeros=2000):
    """My own interface to scipy FFT
      f: function 
      step: time step in fs"""
    import numpy as np
    from scipy.fftpack import fft,dct
    from tools import units

    #Add zeros
    ft  = np.concatenate((ft,np.zeros(nzeros)))

    #Compute FT considering an even function of time
    #fw  = np.fft.hfft(ft)
    fw  = dct(ft,type=1) #It is the same as hfft

    #Compute FT NOT considering an even function of time and takin abs
    #ff  = np.abs(fft(f)) 

    #Add units 
    FourierT=np.zeros((2,fw.size))
    #print('Unit convertion {}'.format(1./units.convert.cm2Phz))
    FourierT[0]=np.linspace(0,1./(2.*float(step)),fw.size)/ units.convert.cm2Phz
    FourierT[1]=fw.copy()

    return FourierT.T



def FT_old(f,step=1.0,lag=2000,window=2,nzeros=10000):
   """My own interface to scipy FFT
      f: function 
      step: time step in fs
      window: boolean wich decides if a window is applied"""
   import numpy as np 
   from scipy.fftpack import fft,dct
   from tools import units
   print('')
   print('@FT: PLEASE CLEAN ME')
   print('')

   n=lag
    
   if window==1:
      win = np.blackman(2*n)
   elif window==2:
      win = np.hanning(2*n)
   elif window==3:
      win = np.hamming(2*n)
   elif window==4:
      win = np.bartlett(2*n)
   else:
      win=np.ones(2*n)
   #Apply window
   fw  = np.multiply(f[:n],win[n:])  
   #Add zeros
   print( 'test1',fw.shape)

   fw  = np.concatenate((fw,np.zeros(nzeros)))  
   print( 'test2',fw.shape)
 
  
   #Apply an average
   #m   = n // av
   #fww  = np.mean(fw.reshape(m,av),axis=1) 

    
   #Compute FT considering an even function of time
   ft  = np.fft.hfft(fw)
   ft  = dct(fw,type=1) #It is the same as hfft

   #Compute FT NOT considering an even function of time and takin abs
   #ff  = np.abs(fft(f)) 

   #Add units 
   FT=np.zeros((2,n+nzeros))
   print('Unit convertion {}'.format(1./units.convert.cm2Phz))
   FT[0]=np.linspace(0,1./(2.*float(step)),n+nzeros)/ units.convert.cm2Phz
   FT[1]=ft.copy()

   ###FT=np.zeros((2,m))
   ###FT[0]=np.linspace(0,1./(2*float(step*av)),m)/ units.convert.cm2Phz
   ###FT[1]=ft[:m]

   return FT.T

def BSAS_FT(f,step=1):

   
    f[0]=norm
    f=f/norm
    size=f.size
    ff=np.zeros(size)

    delta= np.pi/(size-1)
    rk=np.arange(size)*delta
    smooth = (np.cos(rk)+1.0)*0.5
    f=np.multiply(f,smooth)
    print( 'smooth')
    for i in smooth:
       print(smooth)

    ff[0]=1.0/3.0 
    ff[size] = 0.0
    for j in xrange(1,size,2):
        ff[j]   =  4./3.
        ff[j+1] = 2./3.
    print( 'j')
 
    for j in ff:
        print( j)
    delk = 0.5

    for k in range(size):
        suma=0.0
        rk = (k)*delk
      
        for nt in range(size): 
            t = nt*delt
            suma = suma+np.cos(rk*t)*ff(nt)*f(nt)*delt
