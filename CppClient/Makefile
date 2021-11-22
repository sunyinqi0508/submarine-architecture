all:
	g++ SubmarineClient.cpp --std=c++1y -g3 -o SubmarineClient 
	g++ TrenchClient.cpp --std=c++1y -g3 -o TrenchClient 
release:
	g++ SubmarineClient.cpp --std=c++1y -march=native -O3 -s SubmarineClient
	g++ TrenchClient.cpp --std=c++1y -march=native -O3 -s TrenchClient
clean:
	rm -rf SubmarineClient TrenchClient
	