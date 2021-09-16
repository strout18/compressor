#include "bitio.hh"
#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

vector<bool> get_encoding(string wd) {
    // to be replaced with nn stuff
    auto x = wd;
    vector<bool> temp(2);
    return temp;    // temporary - assign two false bits per word
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; i++) {                            //loops through if multiple command line arguments
        auto out = string(argv[i]) + ".comp";
        ifstream infile(argv[i]);

        if (!infile.is_open()) {
            cerr << "Can't open input file";
            return -2;
        };

        auto outfile = ofstream(out); 
        BitIO bit_io(&outfile, nullptr);
        string word;
        while (infile >> word) {
            vector<bool> outbits = get_encoding(word);
            for (auto b: outbits) {
                bit_io.write_bit(b);
            }
        }
    }
}