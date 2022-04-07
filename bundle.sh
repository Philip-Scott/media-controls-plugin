# Prepare minimal files for plugin release

rm -rf ./releaseBundle
mkdir ./releaseBundle

cp index.html ./releaseBundle
cp -r dist ./releaseBundle
cp main.py ./releaseBundle

cd ./releaseBundle
zip ../media-controls-plugin.zip -r ./*