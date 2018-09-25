module linalg
  contains
  ! FlK: math helpers
  !> Determinant of a 3x3 matrix, doubles
  pure function determinant_3x3_real(a) result(det)
    real*8, dimension(3,3), intent(in) :: a
    real*8 :: det
    !
    det = a(1,1)*(a(2,2)*a(3,3) - a(3,2)*a(2,3)) &
        + a(1,2)*(a(3,1)*a(2,3) - a(2,1)*a(3,3)) &
        + a(1,3)*(a(2,1)*a(3,2) - a(3,1)*a(2,2))
  end function

  !> Trace of a 3x3 matrix, doubles
  pure function trace_3x3_real(a) result(trace)
    real*8, dimension(3,3), intent(in) :: a
    real*8 :: trace
    !
    trace = (a(1,1) + a(2,2) + a(3,3)) / 3.d0
  end function

  !> Frobenius norm of a 3x3 matrix, doubles
  pure function frobnorm_3x3_real(a) result(frob)
    real*8, dimension(3,3), intent(in) :: a
    real*8 :: frob
    !
    frob = sqrt(trace_3x3_real(matmul(a, transpose(a))))
  end function

  !> Inverse of 3x3 matrix
  pure function matinv3x3(A) result(B)
    real(8), intent(in) :: A(3,3)   !! Matrix
    real(8)             :: B(3,3)   !! Inverse matrix
    real(8)             :: detinv

    ! Calculate the inverse determinant of the matrix
    detinv = 1/(A(1,1)*A(2,2)*A(3,3) - A(1,1)*A(2,3)*A(3,2)&
              - A(1,2)*A(2,1)*A(3,3) + A(1,2)*A(2,3)*A(3,1)&
              + A(1,3)*A(2,1)*A(3,2) - A(1,3)*A(2,2)*A(3,1))

    ! Calculate the inverse of the matrix
    B(1,1) = +detinv * (A(2,2)*A(3,3) - A(2,3)*A(3,2))
    B(2,1) = -detinv * (A(2,1)*A(3,3) - A(2,3)*A(3,1))
    B(3,1) = +detinv * (A(2,1)*A(3,2) - A(2,2)*A(3,1))
    B(1,2) = -detinv * (A(1,2)*A(3,3) - A(1,3)*A(3,2))
    B(2,2) = +detinv * (A(1,1)*A(3,3) - A(1,3)*A(3,1))
    B(3,2) = -detinv * (A(1,1)*A(3,2) - A(1,2)*A(3,1))
    B(1,3) = +detinv * (A(1,2)*A(2,3) - A(1,3)*A(2,2))
    B(2,3) = -detinv * (A(1,1)*A(2,3) - A(1,3)*A(2,1))
    B(3,3) = +detinv * (A(1,1)*A(2,2) - A(1,2)*A(2,1))
  end function
end module linalg

