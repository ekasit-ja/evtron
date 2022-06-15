### test evtron

for development on Windows environments, **Git Bash** originally does not reply verbose feedback text. We need to use `vim .bahsrc` and add code `alias python='winpty python.exe'` then save it and restart **Git Bash** 2 times.

---

### Development
for this development, we cannot use command `source bin/activate` for virtual environment.  Instead, command `source venv/Scripts/activate` has to be executed.
