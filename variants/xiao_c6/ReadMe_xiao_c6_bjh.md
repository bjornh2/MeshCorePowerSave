# Readme for Xiao C6 and fixes to BjH

## Power consumtion C6
Stock MeshCore - branch - 33mA (61mA when measure)
PowerSave - Whithout changes - 31.5mA

## GIT fix for fork of fork
•	A – Original upstream repository.
•	B – Someone else's fork of A.
•	C – Your fork of B.
git remote add parent https://github.com/other-person/B.git
git remote add upstream https://github.com/original-owner/A.git

### B, fork of A
git remote add parent https://github.com/IoTThinks/MeshCore.git

### A, original
git remote add upstream https://github.com/meshcore-dev/MeshCore.git
if error remove upstream first by: git remote remove upstream

## Check path
git remote -v                                                
origin  https://github.com/bjornh2/MeshCorePowerSave.git (fetch)
origin  https://github.com/bjornh2/MeshCorePowerSave.git (push)
parent  https://github.com/IoTThinks/MeshCore.git (fetch)
parent  https://github.com/IoTThinks/MeshCore.git (push)
upstream        https://github.com/meshcore-dev/MeshCore.git (fetch)
upstream        https://github.com/meshcore-dev/MeshCore.git (push)

## pull changes from remote C, B and A

### This pulls changes from your own fork (C), not B or A.
git pull origin main

### Fetch updates from fork (B)
git fetch parent  
Merge them into your local branch:  
git checkout main  
git merge parent/main  
Then push the updates to your fork:  
git push origin main  
*** or go to github and press button "Sync" :) ***

### To get updates directly from A:
This is useful if B hasn't incorporated the latest changes from A.
git fetch upstream
git merge upstream/main
git push origin main
