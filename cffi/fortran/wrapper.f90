
module c_supercells

  use supercell, only: find_optimal_cell
  use iso_c_binding, only: c_int, c_double, c_bool
  implicit none

  contains
  
  subroutine c_find_optimal_cell(cell, target_metric, target_size, smatrix) bind(c)

    real(c_double),  intent(in) :: cell(3,3)
    real(c_double),  intent(in) :: target_metric(3,3) 
    integer(c_int), intent(in), value           :: target_size       
    integer(c_int), intent(out) :: smatrix(3,3)

    ! integer(c_int), optional, intent(in)        :: lower_limit, upper_limit                                                       
    ! logical(c_bool), optional, intent(in)       :: verbose                                                                        
    ! integer(c_int)                              :: llim, ulim                                                                     
    ! logical(c_bool)                             :: vrbs, found                                                                    
    ! options and defaults                                                                                    
    ! llim = -2                                                                                                 
    ! ulim =  2                                                                                                 
    ! vrbs = .false.                                                                                            
    ! if(present(lower_limit)) llim = lower_limit                                                               
    ! if(present(upper_limit)) ylim = upper_limit                                                               
    ! if(present(verbose))     vrbs = verbose

    smatrix = find_optimal_cell(cell, target_metric, target_size) 
    !, lower_limit, &
    !  !upper_limit, verbose)
    
  end subroutine

end module

