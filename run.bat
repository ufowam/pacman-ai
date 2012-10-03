@ECHO OFF
SET JAVA_HOME="C:\Program Files\Java\jre7\bin"
SET JYTHON_LIB="jython.jar\\Lib"
SET JARPATH="pacman-python.jar"

%JAVA_HOME%\java.exe -jar %JARPATH% %JYTHON_LIB% player %* 2>&1
if ERRORLEVEL 1 goto :eof