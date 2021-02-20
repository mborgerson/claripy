/**
 * @file
 * @brief This file defines the generic Extract Op class
 */
#ifndef __OP_EXTRACT_HPP__
#define __OP_EXTRACT_HPP__

#include "base.hpp"


namespace Op {

    /** The op class: Extract */
    class Extract final : public Base {
        OP_FINAL_INIT(Extract)
      public:
        /** High index */
        const Constants::UInt high;
        /** Low index */
        const Constants::UInt low;
        /** What we extract from */
        const Expression::BasePtr from;

      private:
        /** Protected constructor */
        explicit inline Extract(const Hash::Hash &h, const Constants::UInt hi,
                                const Constants::UInt lo, const Expression::BasePtr &f)
            : Base { h, static_cuid }, high { hi }, low { lo }, from { f } {}
    };

} // namespace Op

#endif
