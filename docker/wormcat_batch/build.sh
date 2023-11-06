#!/bin/bash
USER="danhumassmed"
TAG="wormcat_batch"
VERSION="1.0.1"
SHORT_DESC="Software for Bioinformatics pipelines Wormcat & wormcat batch"
clear
echo "********************************************"
echo "Some Helpful command line calls"
echo "********************************************"
echo
echo ../push_description.py -u \"${USER}\" -i ${USER}/${TAG} -r README.md -s \"${SHORT_DESC}\"
echo "********************************************"
echo
#docker build -t danhumassmed/wormcat_batch:1.0.1 .
echo docker buildx prune
echo docker buildx build --platform linux/amd64,linux/arm64 --push -t ${USER}/${TAG}:${VERSION} .
echo docker buildx build --platform linux/amd64 --push -t ${USER}/${TAG}:${VERSION} .
echo "********************************************"
echo
echo docker run -it ${USER}/${TAG}:${VERSION} /bin/bash
echo docker run --rm -p 8787:8787 -e PASSWORD=password -v ${HOME}/projects:/home/rstudio/projects ${USER}/${TAG}:${VERSION}
echo docker run --rm -v ${HOME}/projects:/home/rstudio/projects ${USER}/${TAG}:${VERSION} /rstudio/projects/
echo docker run --rm -v ${HOME}/projects:/home/rstudio/projects ${USER}/${TAG}:${VERSION} wormcat_cli --input-excel /home/rstudio/projects/Murphy_TS.xlsx --output-path /home/rstudio/projects/output
echo