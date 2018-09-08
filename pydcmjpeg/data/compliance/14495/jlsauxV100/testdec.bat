@echo off
echo #
echo #
echo # EXAMPLE: JPEG-LS DECODER COMPLIANCE TEST ROUTINE
echo #
echo #


echo #
echo # Test 1: T8C0E0.JLS
echo #
set testnum=1
nlocod -N -v0 T8C0E0.JLS
if errorlevel 1 goto FAILED
diffpnm -e0 nlocod1.out test8r.pgm
if errorlevel 1 goto FAILED
diffpnm -e0 nlocod2.out test8g.pgm
if errorlevel 1 goto FAILED
diffpnm -e0 nlocod3.out test8b.pgm
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%
del nlocod*.out


echo #
echo # Test 2: T8C1E0.JLS
echo #
set testnum=2
nlocod -N -v0 -P T8C1E0.JLS
if errorlevel 1 goto FAILED
diffpnm -e0 nlocod.out test8.ppm
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%
del nlocod*.out


echo #
echo # Test 3: T8C2E0.JLS
echo #
set testnum=3
nlocod -N -v0 -P T8C2E0.JLS
if errorlevel 1 goto FAILED
diffpnm -e0 nlocod.out test8.ppm
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%
del nlocod*.out


echo #
echo # Test 4: T8C0E3.JLS
echo #
set testnum=4
nlocod -N T8C0E3.JLS
if errorlevel 1 goto FAILED
diffpnm -e3 nlocod1.out test8r.pgm
if errorlevel 1 goto FAILED
diffpnm -e3 nlocod2.out test8g.pgm
if errorlevel 1 goto FAILED
diffpnm -e3 nlocod3.out test8b.pgm
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%
del nlocod*.out


echo #
echo # Test 5: T8C1E3.JLS
echo #
set testnum=5
nlocod -N -v0 -P T8C1E3.JLS
if errorlevel 1 goto FAILED
diffpnm -e3 nlocod.out test8.ppm
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%
del nlocod*.out


echo #
echo # Test 6: T8C2E3.JLS
echo #
set testnum=6
nlocod -N -v0 -P T8C2E3.JLS
if errorlevel 1 goto FAILED
diffpnm -e3 nlocod.out test8.ppm
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%
del nlocod*.out

echo #
echo # Test 7: T8SSE0.JLS
echo #
set testnum=7
nlocod -N -v0 T8SSE0.JLS
if errorlevel 1 goto FAILED
diffpnm -e0 nlocod1.out test8r.pgm
if errorlevel 1 goto FAILED
diffpnm -e0 nlocod2.out test8gr4.pgm
if errorlevel 1 goto FAILED
diffpnm -e0 nlocod3.out test8bs2.pgm
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%
del nlocod*.out


echo #
echo # Test 8: T8SSE3.JLS
echo #
set testnum=8
nlocod -N -v0 T8SSE3.JLS
if errorlevel 1 goto FAILED
diffpnm -e3 nlocod1.out test8r.pgm
if errorlevel 1 goto FAILED
diffpnm -e3 nlocod2.out test8gr4.pgm
if errorlevel 1 goto FAILED
diffpnm -e3 nlocod3.out test8bs2.pgm
if errorlevel 1 goto FAILED
echo !! Comparison OK on test %testnum%
del nlocod*.out

echo #
echo # Test 9: T8NDE0.JLS
echo #
set testnum=9
nlocod -N -v0 T8NDE0.JLS
if errorlevel 1 goto FAILED
diffpnm -e0 nlocod1.out test8bs2.pgm
echo !! Comparison OK on test %testnum%
if errorlevel 1 goto FAILED

echo #
echo # Test 10: T8NDE3.JLS
echo #
set testnum=10
nlocod -N -v0 T8NDE3.JLS
if errorlevel 1 goto FAILED
diffpnm -e3 nlocod1.out test8bs2.pgm
echo !! Comparison OK on test %testnum%
if errorlevel 1 goto FAILED

echo #
echo # Test 11: T16E0.JLS
echo #
set testnum=11
nloco16d -N -v0  T16E0.JLS
if errorlevel 1 goto FAILED
diffpnm -e3 nloco16d1.out test16.pgm
echo !! Comparison OK on test %testnum%
if errorlevel 1 goto FAILED

echo #
echo # Test 12: T16E3.JLS
echo #
set testnum=12
nloco16d -N -v0  T16E3.JLS
if errorlevel 1 goto FAILED
diffpnm -e3 nloco16d1.out test16.pgm
echo !! Comparison OK on test %testnum%
if errorlevel 1 goto FAILED


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

