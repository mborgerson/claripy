/**
 * @file
 * \ingroup util
 */
#include "ostream.hpp"

#include "../../affirm.hpp"
#include "../../err.hpp"

#include <map>


// For brevity
using namespace Util;
using namespace Log;
using Lvl = Level::Level;


/** Create a map entry for a log level */
#define MAP_ENTRY(X)                                                                               \
    { Lvl::X, std::string(#X) }


/** Map Levels to their names */
static const std::map<Lvl, std::string> names { MAP_ENTRY(Verbose), MAP_ENTRY(Debug),
                                                MAP_ENTRY(Info),    MAP_ENTRY(Warning),
                                                MAP_ENTRY(Error),   MAP_ENTRY(Critical),
                                                MAP_ENTRY(Disabled) };


std::ostream &Level::operator<<(std::ostream &os, const Lvl &l) {
    const auto it { names.find(l) };
    Util::affirm<Err::Usage>(it != names.end(),
                             WHOAMI_HEADER_ONLY "Unknown level passed to << operator");
    os << it->second;
    return os;
}