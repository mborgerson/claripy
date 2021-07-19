/**
 * @file
 * \ingroup utils
 * @brief This file defines macro that return a hashes unique to the file (and optionally line)
 */
#ifndef R_UTILS_FILELINEHASH_HPP_
#define R_UTILS_FILELINEHASH_HPP_

#include "norm_path_hash.hpp"


namespace Utils {

/** Return a file specific hash */
#define UTILS_FILE_HASH Utils::norm_path_hash<Utils::strlen(__FILE__)>(__FILE__)

/** Return a file line specific hash */
#define UTILS_FILE_LINE_HASH (UTILS_FILE_HASH + __LINE__)

} // namespace Utils

#endif