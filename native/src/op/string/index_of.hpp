/**
 * @file
 * @brief This file defines the String::IndexOf class
 */
#ifndef R_OP_STRING_INDEXOF_HPP_
#define R_OP_STRING_INDEXOF_HPP_

#include "../base.hpp"


namespace Op::String {

    /** The op class: String::IndexOf */
    class IndexOf final : public Base {
        OP_FINAL_INIT(IndexOf, 0, "String::");

      public:
        /** String to search: This must be an Expr::String pointer
         *  Note: We leave it as a base for optimizations purposes
         */
        const Expr::BasePtr str;
        /** Pattern to search for: This must be an Expr::String pointer
         *  Note: We leave it as a base for optimizations purposes
         */
        const Expr::BasePtr pattern;
        /** Start Index
         *  Note: We leave it as a base for optimizations purposes
         */
        const Expr::BasePtr start_index;

        /** Python's repr function (outputs json) */
        inline void repr(std::ostream &out, const bool verbose = false) const override final {
            out << R"|({ "name":")|" << op_name() << R"|(", "str":)|";
            Expr::repr(str, out, verbose);
            out << R"|(, "pattern":)|";
            Expr::repr(pattern, out, verbose);
            out << R"|(, "start_index":)|";
            Expr::repr(start_index, out, verbose);
            out << " }";
        }

        /** Adds the raw expr children of the expr to the given stack in reverse
         *  Warning: This does *not* give ownership, it transfers raw pointers
         */
        inline void unsafe_add_reversed_children(Stack &s) const override final {
            s.emplace(start_index.get());
            s.emplace(pattern.get());
            s.emplace(str.get());
        }

      private:
        /** Protected constructor
         *  Ensure that str and pattern are of type String
         */
        explicit inline IndexOf(const Hash::Hash &h, const Expr::BasePtr &s,
                                const Expr::BasePtr &pat, const Expr::BasePtr &si)
            : Base { h, static_cuid }, str { s }, pattern { pat }, start_index { si } {
            using E = Error::Expr::Type;
            Util::affirm<E>(CUID::is_t<Expr::String>(str), WHOAMI "str expr must be a String");
            Util::affirm<E>(CUID::is_t<Expr::String>(pattern),
                            WHOAMI "pattern expr must be a String");
            Util::affirm<E>(CUID::is_t<Expr::BV>(start_index),
                            WHOAMI "start_index expr must be a BV");
        }
    };

} // namespace Op::String

#endif
