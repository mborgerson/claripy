/**
 * @file
 * \ingroup utils
 * @brief This file defines a method to determine if Derived derives from or is Base
 */
#ifndef __UTILS_ISANCESTOR_HPP__
#define __UTILS_ISANCESTOR_HPP__

#include "transfer_const.hpp"

#include <type_traits>


namespace Utils {

    /** Return true if Derived is Base or subclasses Base */
    template <typename Base, typename Derived>
    const constexpr bool is_ancestor =
        std::is_same_v<TransferConst<Base, Derived>, Derived> || std::is_base_of_v<Base, Derived>;

} // namespace Utils

#endif