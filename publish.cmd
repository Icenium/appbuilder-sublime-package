@if "%1" == "" goto error

@for /f "delims=. tokens=1-3" %%a in ( "%1" ) do (set major=%%a && set minor=%%b && set revision=%%c)

@if not defined revision goto error
@if not defined minor goto error
@if not defined major goto error

git fetch
git tag -a v%1 -m "Telerik AppBuilder %1" remotes/origin/master
git push origin v%1

@goto :EOF

:error
@echo Version string must be in Major.Minor.Revision format
@echo Sample usage: publish 1.2.3
