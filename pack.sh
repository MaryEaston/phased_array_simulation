rm -rf ./result

mkdir ./result
cd ./result
pwd

mkdir ./antenna
mkdir ./simulation
mkdir ./graph
cd ./graph
pwd

mkdir ./x
mkdir ./y
cd ../../
pwd

python simulation.py;

python show.py
