@echo off
echo #
echo #
echo # EXAMPLE: JPEG-LS ENCODER COMPLIANCE TEST ROUTINE
echo #
echo #


echo #
echo # Test 1: T8C0E0.JLS
echo #
set testnum=1
nlocoe -N -v1 -c0 test8r.pgm test8g.pgm test8b.pgm
if errorlevel 1 goto FAILED
fcomp nlocoe.jls T8C0E0.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%


echo #
echo # Test 2: T8C1E0.JLS
echo #
set testnum=2
nlocoe -N -v1 -c1 test8r.pgm test8g.pgm test8b.pgm
if errorlevel 1 goto FAILED
fcomp nlocoe.jls T8C1E0.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%


echo #
echo # Test 3: T8C2E0.JLS
echo #
set testnum=3
nlocoe -N -v1 -c2 test8.ppm
if errorlevel 1 goto FAILED
fcomp nlocoe.jls T8C2E0.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%


echo #
echo # Test 4: T8C0E3.JLS
echo #
set testnum=4
nlocoe -N -v1 -c0 -e3 test8r.pgm test8g.pgm test8b.pgm
if errorlevel 1 goto FAILED
fcomp nlocoe.jls T8C0E3.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%


echo #
echo # Test 5: T8C1E3.JLS
echo #
set testnum=5
nlocoe -N -v1 -c1 -e3 test8r.pgm test8g.pgm test8b.pgm
if errorlevel 1 goto FAILED
fcomp nlocoe.jls T8C1E3.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%


echo #
echo # Test 6: T8C2E3.JLS
echo #
set testnum=6
nlocoe -N -v1 -c2 -e3 test8.ppm
if errorlevel 1 goto FAILED
fcomp nlocoe.jls T8C2E3.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%


echo #
echo # Test 7: T8SSE0.JLS
echo #
set testnum=7
nlocoe -N -v1 -c1 test8r.pgm test8gr4.pgm test8bs2.pgm
if errorlevel 1 goto FAILED
fcomp nlocoe.jls T8SSE0.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%


echo #
echo # Test 8: T8SSE3.JLS
echo #
set testnum=8
nlocoe -N -v1 -c1 -e3 test8r.pgm test8gr4.pgm test8bs2.pgm
if errorlevel 1 goto FAILED
fcomp nlocoe.jls T8SSE3.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%

echo #
echo # Test 9: T8NDE0.JLS
echo #
set testnum=9
nlocoe -N -v1 -c1 -Sa9 -Sb9 -Sc9 -r31 test8bs2.pgm
if errorlevel 1 goto FAILED
fcomp nlocoe.jls T8NDE0.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%

echo #
echo # Test 10: T8NDE3.JLS
echo #
set testnum=10
nlocoe -N -v1 -c1 -e3 -Sa9 -Sb9 -Sc9 -r31 test8bs2.pgm
if errorlevel 1 goto FAILED
fcomp nlocoe.jls T8NDE3.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%

echo #
echo # Test 11: T16E0.JLS
echo #
set testnum=11
nloco16e -N -v1 -c1 test16.pgm
if errorlevel 1 goto FAILED
fcomp nloco16e.jls T16E0.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%

echo #
echo # Test 12: T16E3.JLS
echo #
set testnum=12
nloco16e -N -v1 -c1 -e3 test16.pgm
if errorlevel 1 goto FAILED
fcomp nloco16e.jls T16E3.JLS
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%


:PASSED
echo.
echo.
echo !!!!!!!!!!!!!!!!! PASSED %testnum% TESTS !!!!!!!!!!!!!!!!!!!!
echo.
echo.
goto out

:FAILED
echo.
echo.
echo !!!!!!!!!!!!!!!!! FAILED ON TEST %testnum% !!!!!!!!!!!!!!!!!!!!
echo.
echo.
goto out

:out

