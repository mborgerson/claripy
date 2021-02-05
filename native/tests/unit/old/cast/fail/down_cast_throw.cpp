/**
 * @file
 * \ingroup unittest
 */
#include "expression.hpp"
#include "testlib.hpp"

#include <set>


// For brevity
using namespace Expression;
using namespace UnitTest::TestLib;


/** Down casting should fail with an exception */
void down_cast_throw() {
    ConcreteIntLiteral a { literal_int() };
    Base b { up_cast<Base>(a) };
    try {
        Bool c { down_cast_throw_on_fail<Bool>(b) };
        (void) c;
    }
    catch (Utils::Error::Unexpected::BadCast &e) {
        return;
    }
    UNITTEST_ERR("No bad cast exception caught")
}

// Define the test
UNITTEST_DEFINE_MAIN_TEST(down_cast_throw)