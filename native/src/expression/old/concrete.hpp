/**
 * @file
 * @brief This file defines a concrete expression
 */
#ifndef __EXPRESSION_RAW_CONCRETE_HPP__
#define __EXPRESSION_RAW_CONCRETE_HPP__

#include "base.hpp"


namespace Expression {

    namespace Raw {

        /** A concrete expression
         *  All concrete expressions must subclass this
         */
        struct Concrete : virtual public Base {
            EXPRESSION_RAW_ABSTRACT_INIT_IMPLICIT_CTOR(Concrete)
          public:
            /** Return true if and only if this expression is symbolic */
            bool symbolic() const override final;
        };

    } // namespace Raw

    // Create a shared pointer alias
    EXPRESSION_RAW_DECLARE_SHARED(Concrete, Raw)

} // namespace Expression

#endif