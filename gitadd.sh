# Add the Buildroot configuration
git add -f .config

# Add your ubinize.cfg file
git add -f ubinize.cfg

# Add key output images
git add -f output/images/rootfs.ubi
git add -f output/images/rootfs.ubifs
git add -f output/images/uImage
git add -f output/images/*.dtb

git add gitadd.sh

