/*
 * Unit tests for class BitIO
 */

#include "bitio.hh"
#include <cassert>
#include <sstream>
#include <iostream>

//////////////////////////////////////////////////////////////////////////////
void
test_1_bit()
{
  std::stringstream bits;
  {
    BitIO bitio(&bits, nullptr);
    bitio.write_bit(1);
  }
  {
    BitIO bitio(nullptr, &bits);
    assert(bitio.read_bit() == true);
    assert(bitio.read_bit() == false);  // Should just be a trailing zero
  }
}


//////////////////////////////////////////////////////////////////////////////
void
test_4_bits()
{
  std::stringstream bits;
  {
    BitIO bitio(&bits, nullptr);
    bitio.write_bit(0);
    bitio.write_bit(1);
    bitio.write_bit(0);
    bitio.write_bit(1);
  }
  {
    BitIO bitio(nullptr, &bits);
    assert(bitio.read_bit() == false);
    assert(bitio.read_bit() == true);
    assert(bitio.read_bit() == false);
    assert(bitio.read_bit() == true);
    assert(bitio.read_bit() == false);  // Should just be a trailing zero
  }
}

//////////////////////////////////////////////////////////////////////////////
void
test_8_bits()
{
  std::stringstream bits0, bits1;
  {
    BitIO bitio0(&bits0, nullptr);
    BitIO bitio1(&bits1, nullptr);
    for (int i = 0; i < 8; ++i) {
      bitio0.write_bit(0);
    }
    for (int i = 0; i < 8; ++i) {
      bitio1.write_bit(1);
    }
  }
  {
    BitIO bitio0(nullptr, &bits0);
    BitIO bitio1(nullptr, &bits1);
    for (int i = 0; i < 8; ++i) {
      assert(!bitio0.read_bit());
    }
    bitio0.read_bit();
    assert(bits0.eof()); // Should be no trailing zeros this time!

    for (int i = 0; i < 8; ++i) {
      assert(bitio1.read_bit());
    }
  }
}

//////////////////////////////////////////////////////////////////////////////
void
test_9_bits()
{
  std::stringstream bits0, bits1;
  {
    BitIO bitio1(&bits1, nullptr);
    for (int i = 0; i < 9; ++i) {
      bitio1.write_bit(1);
    }
  }
  {
    BitIO bitio1(nullptr, &bits1);
    for (int i = 0; i < 9; ++i) {
      assert(bitio1.read_bit());
    }
    assert(!bitio1.read_bit());
  }
}

//////////////////////////////////////////////////////////////////////////////
void
test_16_bits()
{
  std::stringstream bits;
  {
    BitIO bitio(&bits, nullptr);
    for (int i = 0; i < 16; ++i) {
      bitio.write_bit(i % 2);
    }
  }
  {
    BitIO bitio(nullptr, &bits);
    for (int i = 0; i < 16; ++i) {
      assert(bitio.read_bit() == i % 2);
    }
    bitio.read_bit();
    assert(bits.eof()); // Should be no trailing zeros this time!
  }
}

//////////////////////////////////////////////////////////////////////////////
void
test_100_bits()
{
  std::stringstream bits;
  {
    BitIO bitio(&bits, nullptr);
    for (int i = 0; i < 100; ++i) {
      bitio.write_bit(!(i % 2));
    }
  }
  {
    BitIO bitio(nullptr, &bits);
    for (int i = 0; i < 100; ++i) {
      assert(bitio.read_bit() != i % 2);
    }
    assert(!bitio.read_bit());
  }
}


//////////////////////////////////////////////////////////////////////////////
int
main() {
  test_1_bit();
  test_4_bits();
  test_8_bits();
  test_9_bits();
  test_16_bits();
  test_100_bits();

  return 0;
}
