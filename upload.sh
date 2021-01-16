#!/bin/bash

set -e

cd ./CovDB_Addon
TAG=$(grep Version ./CovDB_US_H/CovDB_US_H.toc | cut -d ':' -f2 | tr -d ' ' )
git commit -am "Update database $TAG"
git tag $TAG
git push origin main
git push origin $TAG
cd ..
zip -r ./addon_dist/CovDB-$TAG.zip CovDB_Addon/*

# https://authors.curseforge.com/knowledge-base/projects/529-api
#echo curl -XPOST -d "{changelog: \"A string describing changes.\", displayName: \"$TAG\", gameVersions: [902], releaseType: \"release\" }"
