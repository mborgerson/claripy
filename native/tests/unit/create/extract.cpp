/**
 * @file
 * \ingroup unittest
 */
#include "create.hpp"
#include "testlib.hpp"


/** A dynamic down-cast alias */
template <typename T, typename U> auto dcast(const U &u) {
    return Utils::dynamic_down_cast_throw_on_fail<T>(u);
}

/** Verify that the extract<T> function compiles and can be run without issue */
template <typename T> void extract_t() {

    // For brevity
    namespace F = UnitTest::TestLib::Factories;
    namespace Ex = Expression;

    // Create distinct inputs
    const Constants::UInt high { 2 };
    const Constants::UInt low { 2 };
    const auto a { F::t_literal<T>(0) };

    // Test
    const auto exp { Create::extract<T>(Create::EAnVec {}, high, low, a) };

    // Pointer checks
    UNITTEST_ASSERT(a.use_count() == 2)
    UNITTEST_ASSERT(exp->op.use_count() == 1)

    // Type check
    const auto op_down { dcast<Op::Extract>(exp->op) };
    const auto exp_down { dcast<T>(exp) };
    const auto a_down { dcast<T>(a) };

    // Contains check
    UNITTEST_ASSERT(op_down->from == a)

    // Size check
    UNITTEST_ASSERT(exp_down->size == high + 1 - low)
}

/** Verify that the extract function compiles and can be run without issue */
void extract() {
    extract_t<Expression::BV>();
    extract_t<Expression::String>();
}

// Define the test
UNITTEST_DEFINE_MAIN_TEST(extract)
