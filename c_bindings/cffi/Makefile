FC = gfortran
FCOPTS = -O0 -fPIC
LN = $(FC)
LNOPTS = -shared -fPIC

# Object files
OBJS = linalg.o supercell.o wrapper.o

all: $(OBJS)
	$(LN) $(LNOPTS) -o libwrapper.so $(OBJS)
linalg.o: linalg.f90
	$(FC) $(FCOPTS) -c linalg.f90

supercell.o: supercell.f90
	$(FC) $(FCOPTS) -c supercell.f90
	#$(FC) -shared -fPIC -c supercell.f90 -o libsupercell.so -fPIC

wrapper.o: wrapper.f90
	$(FC) $(FCOPTS) -c wrapper.f90


clean:
	rm -f *.o *.so *.mod


