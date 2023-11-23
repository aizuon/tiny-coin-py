pip uninstall -y tiny_coin
pip cache purge
rm -rf ./dist
hatchling build
pip install --find-links=./dist tiny_coin --force
