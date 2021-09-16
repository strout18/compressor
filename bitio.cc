#include "bitio.hh"
#include <iostream>
#include <fstream>

using namespace std;

BitIO::BitIO(std::ostream* os, std::istream* is) {
    times = 0; //times = how many bits have been placed in buffer
    os_ = os;
    is_ = is;
}

BitIO::~BitIO() {
    while (os_ && times) {      //keep writing zeros if no more bits to write but need to fill buffer
        write_bit(0);
    }
}

unsigned char BitIO::leftbitmask(bool bit, int times) {     //given a bit, pushes it to where it should be in buffer
    unsigned char ret = bit << (7 - times); //so 0th bit is on far left
    return ret;
}

unsigned char BitIO::rightbitmask(char bits, int times) {   //given a series of bits, isolates the one we want
    unsigned char ret = bits >> (7 - times);
    return ret;
}

// Output a single bit (buffered)
void BitIO::write_bit(bool bit) {
    if (times == 0) {
        buff = 0; //reset buffer
    };
    buff = buff | leftbitmask(bit, times);
    if (times == 7) { //reset buffer
        (*os_).put(buff);
        times = 0;
    }   
    else { 
        times += 1;
    };
}

// Read a single bit (or trailing zero)
bool BitIO::read_bit() {
    bool result = 0;
    if (times == 0) {
        buff = 0;
        buff = (*is_).get();
    }
    result = (rightbitmask(buff, times) & 1);   //takes only last bit
    if (times == 7) {
        times = 0;
    }
    else {
        times += 1;
    };
    return result;
}