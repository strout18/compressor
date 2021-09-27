CXX=g++
CXXFLAGS=-Wall -Wextra -pedantic -Werror -std=c++17 -O0 -g
LDFLAGS=$(CXXFLAGS)
OBJ=$(SRC:.cc=.o)

all:  test_bitio encoder decoder

test_bitio: bitio.o test_bitio.o
	$(CXX) $(LDFLAGS) -o $@ $^

encoder: encoder.o bitio.o
	$(CXX) $(LDFLAGS) -o $@ $^

decoder: decoder.o  bitio.o
	$(CXX) $(LDFLAGS) -o $@ $^

%.o: %.cc %.hh
	$(CXX) $(CXXFLAGS) $(OPTFLAGS) -c -o $@ $<

clean:
	rm -rf *.o test_bitio encoder decoder

test: all
	./test_bitio
