/**
 * @file
 * @brief This file defines a floating point width class
 */
#ifndef __BACKEND_Z3_FPWIDTH_HPP__
#define __BACKEND_Z3_FPWIDTH_HPP__

#include "../../constants.hpp"


namespace Backend::Z3::FP {

    /** A floating point width struct */
    struct Width {
        /** The width of the exponent */
        Constants::UInt exp;
        /** The width of the mantissa */
        Constants::UInt mantissa;
    };

    /** A single wide fp width */
    static inline const constexpr Width dbl { 8, 24 };

    /** A double wide fp width */
    static inline const constexpr Width flt { 11, 53 };
} // namespace Backend::Z3::FP

#endif