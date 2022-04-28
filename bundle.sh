# Prepare minimal files for plugin release

rm -rf ./releaseBundle
mkdir ./releaseBundle


cp -r pip ./releaseBundle
cp index.html ./releaseBundle
cp -r dist ./releaseBundle
cp main.py ./releaseBundle
cp plugin.json ./releaseBundle

cd ./releaseBundle
zip ../media-controls-plugin.zip -r ./*