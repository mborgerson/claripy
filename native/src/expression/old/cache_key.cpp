/** @file */
#include "cache_key.hpp"

#include "raw/type/base.hpp"

#include <sstream>


// For clarity
using namespace Expression;


// Constructor
CacheKey::CacheKey(const Raw::Type::Base &a) : ref(a) {}

// __repr__
/** @todo implement */
std::string CacheKey::repr() const {
    std::ostringstream ret;
    ret << this->ref.hash;
    return ret.str();
}

// CacheKey comparison
bool Expression::operator==(const CacheKey &a, const CacheKey &b) {
    return a.ref.hash == b.ref.hash;
}