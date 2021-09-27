/*
 * A simple class to perform stream I/O on individual bits.
 * Before reading any bits, ensure your input stream still has valid inputs.
 */
#include <iostream>

class BitIO {
 public:
  // Construct with one of either an input stream or output (the other null)
  BitIO(std::ostream* os, std::istream* is);

  // Flushes out any remaining output bits and trailing zeros, if any:
  ~BitIO();

  BitIO(const BitIO&) = default;
  BitIO(BitIO&&) = default;
  BitIO& operator=(const BitIO&) = default;
  BitIO& operator=(BitIO&&) = default;

  unsigned char leftbitmask(bool bit, int times);

  unsigned char rightbitmask(char bits, int times);

  void write_bit(bool bit); // write bit to file

  // write a single bit (or trailing zero) from the stream to the output
  bool read_bit();

 private:
  std::ostream* os_;
  std::istream* is_;
  int times;
  unsigned char buff;
};
