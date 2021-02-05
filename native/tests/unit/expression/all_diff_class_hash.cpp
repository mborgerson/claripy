/**
 * @file
 * \ingroup unittest
 */
#include "testlib.hpp"

#include <set>


// For brevity
using namespace Expression;
using namespace UnitTest::TestLib;


/** Each construction should have a unique pointer and hash */
void all_diff_class_hash() {

    const auto a1 { Factories::t_literal<Int>() };
    const auto a2 { Factories::t_literal<Bool>() };
    const auto a3 { Factories::t_literal<String>() };
    const auto a4 { Factories::t_literal<FP>() };
    const auto a5 { Factories::t_literal<BV>() };
    const auto a6 { Factories::t_literal<VS>() };

    // Verify unique hashes

    std::set<Hash::Hash> hashes;
    hashes.insert(a1->hash);
    hashes.insert(a2->hash);
    hashes.insert(a3->hash);
    hashes.insert(a4->hash);
    hashes.insert(a5->hash);
    hashes.insert(a6->hash);

    UNITTEST_ASSERT(hashes.size() == 6)

    // Verify unique pointers

    std::set<Constants::CTSC<Base>> ptrs;
    ptrs.insert(a1.get());
    ptrs.insert(a2.get());
    ptrs.insert(a3.get());
    ptrs.insert(a4.get());
    ptrs.insert(a5.get());
    ptrs.insert(a6.get());

    UNITTEST_ASSERT(ptrs.size() == 6)
}

// Define the test
UNITTEST_DEFINE_MAIN_TEST(all_diff_class_hash)
