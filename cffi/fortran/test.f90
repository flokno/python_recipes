program test 
  use supercell, only: find_optimal_cell

  implicit none
  real*8,  dimension(3, 3) :: matrix
  real*8,  dimension(3, 3) :: metric
  integer, dimension(3, 3) :: smatrix

  ! define some matrix                                                                         
  ! matrix(1,1:3) =  (/ 0.d0, 2.d0, 2.d0 /)                                                    
  ! matrix(2,1:3) =  (/ 2.d0, 0.d0, 2.d0 /)                                                    
  ! matrix(3,1:3) =  (/ 2.d0, 2.d0, 0.d0 /)

  ! GaO:
  matrix(1,1:3) =  (/  6.22768603, -1.54124518,  0.        /)                                                   
  matrix(2,1:3) =  (/  6.22768603,  1.54124518,  0.        /)                                                   
  matrix(3,1:3) =  (/ -1.39028711,  0.        ,  5.7080621 /)

  ! Metric: cubic cell
  metric(1,1:3) =  (/ 1.d0, 0.d0, 0.d0 /)                                                    
  metric(2,1:3) =  (/ 0.d0, 1.d0, 0.d0 /)                                                    
  metric(3,1:3) =  (/ 0.d0, 0.d0, 1.d0 /)

  smatrix = find_optimal_cell(transpose(matrix), metric, 30, verbose=.true.)
  ! smatrix = find_optimal_cell(matrix, metric, 30, verbose=.true.)
  write (*,"(A,/,3(F7.2))") 'Initial Matrix:', matrix 
  write (*,"(A,/,3(I7))") 'Supercell mat.:', smatrix 
  write (*,"(A,/,3(F7.2))") 'Supercell lat.:', matmul(transpose(matrix), smatrix)

end program
