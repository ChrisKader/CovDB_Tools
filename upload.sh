#!/bin/bash

set -e

cd ./CovDB
TAG=$(grep Version CovDB.toc | cut -d ':' -f2 | tr -d ' ')
git commit -am "Update database $TAG"
git tag $TAG
git push origin master
git push origin $TAG
cd ..
zip -r CovDB-$TAG.zip CovDB/*

# https://authors.curseforge.com/knowledge-base/projects/529-api
echo curl -XPOST -d "{changelog: \"A string describing changes.\", displayName: \"$TAG\", gameVersions: [902], releaseType: \"release\" }"
