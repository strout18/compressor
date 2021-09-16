#include "bitio.hh"
#include <iostream>
#include <fstream>
#include <cstdlib>


using namespace std;

bool first = true;
int count = 0;

int get_decoding(bool bit __attribute__((unused))) {
    // to be replaced with nn stuff
    // temporary
    ::count++;
    if (::count > 20) {
        return 'b';};
    if (first) {
        first = false;
        return -3;
    }
    else {
        first = true;
        return 'a';
    }
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; i++) {    //loops through if multiple command line arguments
        auto out = string(argv[i]) + ".plaintext";
        ofstream outfile (out);        
        auto infile = ifstream(argv[i]); 

        if (!infile.is_open()) {
            cerr << "Can't open input file.";
            return -2;
        };

        BitIO bit_io(nullptr, &infile);
        int symbol = -1;     //holds char 
        while (symbol != 'b') {     // how should we encode eof?
            bool read = bit_io.read_bit();
            symbol = get_decoding(read);
            if (symbol >= 0 && symbol != 'b') {     // to be replaced
                outfile.put(symbol);
            }
        }
    }
}