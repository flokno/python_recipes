module supercell
  use linalg, only: determinant_3x3_real, frobnorm_3x3_real, matinv3x3

  contains

    !> Compute deviation from the target metric, given that cell is normed
    pure function get_deviation(cell, target_metric, norm) result(deviation)
      real*8, dimension(3,3), intent(in) :: cell
      real*8, dimension(3,3), intent(in) :: target_metric
      logical,      optional, intent(in) :: norm
      logical                            :: nrm
      real*8                             :: ncell(3,3)

      nrm = .true.
      if (present(norm)) nrm = norm

      ! Normalize the input lattice
      if (nrm) then
        ncell = cell * (determinant_3x3_real(cell) / determinant_3x3_real(target_metric))**(-1./3.)
      else
        ncell = cell
      end if

      deviation = frobnorm_3x3_real(ncell - target_metric)

    end function

    !> Find optimal supercell matrix to realize supercell lattice of given
    !> metric, e.g., cubic.
    function find_optimal_cell(cell, target_metric, target_size, lower_limit, &
        upper_limit, verbose) result(smatrix)
      real*8,  intent(in)   :: cell(3,3) 
      real*8,  intent(in)   :: target_metric(3,3)
      real*8,  intent(in)   :: target_size
      integer, intent(in)   :: lower_limit, upper_limit
      logical, intent(in)   :: verbose
      integer               :: smatrix(3,3)
      optional              :: lower_limit, upper_limit, verbose
      integer               :: llim, ulim 
      logical               :: vrbs, found
      integer               :: i1, i2, i3, i4, i5, i6, i7, i8, i9, nn
      integer               :: initial_P(3,3), P(3,3), dP(3,3)
      real*8                :: norm, score, best_score, ideal_P(3,3), ccell(3,3)
      
      ! options and defaults
      llim = -2
      ulim =  2
      vrbs = .false.
      if(present(lower_limit)) llim = lower_limit
      if(present(upper_limit)) ulim = upper_limit
      if(present(verbose))     vrbs = verbose

      ! initialize matrices and values
      smatrix    = -1
      score      = 1.e7
      best_score = 1.e6
      ccell      = cell
      found      = .false.
      P          = 0

      if (vrbs) then
        write(*,*) 'Settings:'
        write (*,"(A,/,3(F7.2))") 'Input cell:   ', cell
        write (*,"(A,/,3(F7.2))") 'Target metric:', target_metric
        write (*,"(A,(F7.2))")    'Target size:  ', target_size
        write (*,"(A,2(I3))")     'Limits:       ', llim, ulim
      end if

      ! Normalize the input lattice
      norm = (target_size * determinant_3x3_real(cell) / determinant_3x3_real(target_metric))**(-1./3.)
      ccell = norm * cell

      if (vrbs) write(*,"(A,(F7.3))") 'Normalization factor: ', norm
      if (vrbs) write (*,"(A,/,3(F7.2))") 'Normed cell:  ', ccell

      ! Approximate the perfect smatrix
      ideal_P   = matmul(target_metric, matinv3x3(ccell))
      initial_P = nint(ideal_P)
      if (vrbs) write (*,"(A,/,3(F7.3))") 'Ideal P:   ' , ideal_P 
      if (vrbs) write (*,"(A,/,3(I7))") 'Initial P: ' , initial_P

      !> Expand brute force
      do i1=llim, ulim
      do i2=llim, ulim
      do i3=llim, ulim
      do i4=llim, ulim
      do i5=llim, ulim
      do i6=llim, ulim
      do i7=llim, ulim
      do i8=llim, ulim
      do i9=llim, ulim
        dP(1,1:3) =  (/ i1, i2, i3 /)                                                    
        dP(2,1:3) =  (/ i4, i5, i6 /)                                                    
        dP(3,1:3) =  (/ i7, i8, i9 /)
        P = initial_P + dP
        nn = nint(determinant_3x3_real(real(P, 8)))
        ! Allow up to 20% increase in size from target shape
        if ((nn < target_size  ) .or. (nn > 1.2*target_size)) cycle
        score = get_deviation(matmul(ccell, P), target_metric)
        ! Save the result if it was a good one
        if (score < best_score) then
          found = .true.
          best_score = score
          smatrix = P
        end if
      end do
      end do
      end do
      end do
      end do
      end do
      end do
      end do
      end do

      if (vrbs) then
        write (*,"(A,/,(F7.3))") 'Best score: ' , best_score
        write (*,"(A,/,3(I7))")  'P:          ' , smatrix
        write (*,"(A,/,F7.3,I5)")  'N_target, N:' , target_size, nint(determinant_3x3_real(real(smatrix, 8)))
      end if

      if (.not. found) write(*,*) 'No supercell matrix found.'

    end function
end module
