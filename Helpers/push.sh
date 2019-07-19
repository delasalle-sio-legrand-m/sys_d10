python3 macro.py -v show -o Generated
#python3 macro.py -v diff -v ~-1 -o Changes
git add -A
git commit
git push
git checkout gh-pages && git merge age-of-chaos && git push && git checkout age-of-chaos
