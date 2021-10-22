/**
 * @file
 * \ingroup unittest
 */
#include "testlib.hpp"


/** Try to simplify a claricpp expr via BoolTactic */
void bool_tactic() {
    auto z3 { Backend::Z3::Z3 {} };
    namespace Ex = Expr;

    // Leaves
    const auto x { Create::symbol("x") };
    const auto y { Create::literal(true) };

    // Negations
    const auto not_x { Create::not_(x) };
    const auto not_y { Create::not_(y) };

    // Ors
    const auto c1 { Create::or_({ x, not_y }) };
    const auto c2 { Create::or_({ x, y }) };
    const auto c3 { Create::or_({ not_x, y }) };

    // And
    const auto statement { Create::and_({ c1, c2, c3 }) };

    // Simplify
    const auto simp { z3.simplify(statement.get()) };

    // Solution
    // x && y = x && true = x
    const auto sol { x }; // NOLINT

    // Verify equality
    UNITTEST_ASSERT(Ex::inline_repr(simp) == Ex::inline_repr(sol));
}

// Define the test
UNITTEST_DEFINE_MAIN_TEST(bool_tactic)
