@ECHO OFF

pushd %~dp0

REM CDI Command file

if "%BUILD%" == "" (
	set BUILD=poetry
)
set SOURCEDIR=source
set BUILDDIR=dist

%BUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'poetry' command was not found. Make sure you have poetry
	echo.installed, then set the BUILD environment variable to point
	echo.to the full path of the 'poetry' executable. Alternatively you
	echo.may add the poetry directory to PATH.
	echo.
	echo.If you don't have poetry installed, install it from eg. conda
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

if "%1" == "" goto help

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%BUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
