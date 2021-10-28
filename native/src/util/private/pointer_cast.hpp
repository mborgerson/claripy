/**
 * @file
 * \ingroup util
 * @brief This file defines private pointer cast methods
 * These methods preserve the const-ness of the internal type
 */
#ifndef R_UTIL_PRIVATE_POINTERCAST_HPP_
#define R_UTIL_PRIVATE_POINTERCAST_HPP_

#include "../transfer_const.hpp"

#include <memory>
#include <type_traits>

namespace Util::Cast::Private {

    /** A const preserving static pointer cast */
    template <typename Out, typename In>
    constexpr auto static_pointer_cast(const std::shared_ptr<In> &in) noexcept {
        if constexpr (is_exactly_same<In, Out>) {
            return in;
        }
        else {
            return std::static_pointer_cast<TransferConst<Out, In>>(in);
        }
    }

    /** An unchecked dynamic pointer cast */
    template <typename Out, typename In>
    constexpr auto dynamic_pointer_cast(const std::shared_ptr<In> &in) noexcept {
        if constexpr (is_same_ignore_const<In, Out>) {
            return Private::static_pointer_cast<Out>(in);
        }
        else {
            return std::dynamic_pointer_cast<TransferConst<Out, In>>(in);
        }
    }

} // namespace Util::Cast::Private

#endif