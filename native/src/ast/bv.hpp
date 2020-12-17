/**
 * @file
 * @brief This file defines the AST::Cached::BV class and defines AST::BV
 */
#ifndef __AST_BV_HPP__
#define __AST_BV_HPP__

#include "using_declarations.hpp"

#include "../macros.hpp"

#include "bits.hpp"


/** A namespace used for the ast directory */
namespace AST {

    /** A namespace to denote self-caching classes
     *  These classes are unlikely to be accessed directly, but rather should be accessed via a
     * shared_ptr
     */
    namespace Cached {

        /** This class represents an AST bit vector */
        class BV : public Bits {

            /** Return the name of the type this class represents irrespective of length */
            std::string fundamental_type_name() const;

            /** Delete all default constructors */
            DELETE_DEFAULTS(BV);
        };
    } // namespace Cached

    /** An abbreviation for a shared pointer to the cached bv class */
    using BV = std::shared_ptr<Cached::BV>;

} // namespace AST

#endif