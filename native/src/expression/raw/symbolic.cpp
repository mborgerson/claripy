/** @file */
#include "symbolic.hpp"

// For brevity
using namespace Expression::Raw;


Symbolic::~Symbolic() = default;

bool Symbolic::symbolic() const {
    return true;
}
