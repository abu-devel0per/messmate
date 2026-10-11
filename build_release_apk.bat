@echo off
set "JAVA_HOME=C:\Program Files\Android\Android Studio\jbr"
set "PATH=%JAVA_HOME%\bin;%PATH%"
cd /d "c:\Users\kames\mess mate\messmate1\frontend\android"
call gradlew.bat assembleRelease
