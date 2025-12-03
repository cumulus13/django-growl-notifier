@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
\tset SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
\techo.
\techo.The 'sphinx-build' command was not found. Make sure you have Sphinx
\techo.installed, then set the SPHINXBUILD environment variable to point
\techo.to the full path of the 'sphinx-build' executable. Alternatively you
\techo.may add the Sphinx directory to PATH.
\techo.
\techo.If you don't have Sphinx installed, grab it from
\techo.https://www.sphinx-doc.org/
\texit /b 1
)

if "%1" == "" goto help

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd