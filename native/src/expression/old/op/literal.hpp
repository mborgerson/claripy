/**
 * @file
 * @brief The expression representing a Literal
 */
#ifndef __EXPRESSION_RAW_OP_LITERAL_HPP__
#define __EXPRESSION_RAW_OP_LITERAL_HPP__

#include "base.hpp"

#include "../cusized.hpp"

#include <variant>

#include <boost/multiprecision/cpp_int.hpp>
#include <boost/multiprecision/gmp.hpp>


namespace Expression::Raw::Op {

    /** The op class Literal */
    class Literal : virtual public Base, virtual public CUSized {
        EXPRESSION_RAW_ABSTRACT_INIT_CUSTOM_CTOR(Literal)
      public:
        /** Return the op */
        Constants::CCS op() const override final;

        /** Value type */
        using ValueT = std::variant<int_fast64_t, boost::multiprecision::int128_t,
                                    boost::multiprecision::mpz_int>;

      protected:
        /** Protected constructor
         *  @todo figure out how this will work
         *  @todo Intern strings
         */
        explicit Literal(const std::string &data);

        /** Representation */
        const ValueT value;
    };

} // namespace Expression::Raw::Op

#endif