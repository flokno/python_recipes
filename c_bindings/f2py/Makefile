FC = gfortran
FCOPTS = -O3
LN = $(FC)
LNOPTS =

# Object files
OBJS = linalg.o

all: $(OBJS)
	f2py -c linalg.f90 supercell.f90 -m supercell
linalg.o: linalg.f90
	$(FC) $(FCOPTS) -c linalg.f90

clean:
	rm -f *.o *.so *.mod


