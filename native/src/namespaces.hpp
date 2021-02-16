/**
 * @file
 * @brief This file defines the namespaces for documentation purposes
 * This file should not be included in any C++ code and will not compile intentionally
 */

/** A namespace that defines constants */
namespace Constants {}


/** A namespace used for the utils directory */
namespace Utils {

    /** A namespace that contains the max functions */
    namespace Max {}

    /** A namespace that contains members used to ensure thread safety */
    namespace ThreadSafe {}

    /** A namespace that contains private members of Utils
     *
     *  These members should not be called outside of the utils directory
     *  This is useful for helper functions templated functions call
     */
    namespace Private {}

    /** A namespace used to contain color terminal codes */
    namespace ANSIColorCodes {

        /** Bold color codes */
        namespace Bold {}
        /** Underlined color codes */
        namespace Underline {}
        /** High intensity color codes */
        namespace HighIntensity {
            /** HighIntensity Bold */
            namespace Bold {}
        } // namespace HighIntensity
        /** Background color codes */
        namespace Background {
            /** High intensity background color codes */
            namespace HighIntensity {}
        } // namespace Background

    } // namespace ANSIColorCodes

    /** A namespace used for the util's errors directory */
    namespace Error {

        /** A namespace used exceptions to be passed back to python */
        namespace Python {}

        /** A namespace used for unexpected errors
         *
         *  These should never be thrown; they indicate an error with the code
         */
        namespace Unexpected {}

    } // namespace Error

    /** A namespace used for logging functions
     *
     *  Unless otherwise specified, each public logging function in this namespace takes in
     *  whatever arguments it is given by copy, and returns void. There are no restrictions on
     *  what types of arguments, or how many arguments are given, other than that the '<<'
     *  stream operator must be defined for the type. Optionally, a class can be provided as an
     *  extra template argument to log. If it is provided the log written to will be a custom log
     *  related to that particular class. If no custom log is specified a default log is used.
     */
    namespace Log {

        /** A namespace used to designate certain items in Utils::Log as private
         *
         *  These members should not be called outside of Utils::Log members
         */
        namespace Private {}

        /** A namespace used for log level members */
        namespace Level {}

        /** A namespace used for log styles */
        namespace Style {

            /** A namespace used for private members of Style */
            namespace Private {}

        } // namespace Style

        /** A namespace used for log backends */
        namespace Backend {

            /** A namespace used for private members of Backend */
            namespace Private {}

        } // namespace Backend

    } // namespace Log

    /** A namespace used for type dependent constants */
    namespace TD {}

} // namespace Utils

/** A namespace used for the CUID related members */
namespace CUID {}

/** A namespace used for the factory directory */
namespace Factory {

    /** A namespace used for private members of factory */
    namespace Private {}

} // namespace Factory

/** A namespace used for the hash directory */
namespace Hash {}

/** A namespace used for the errors directory */
namespace Error {

    /** A namespace used for Expression errors */
    namespace Expression {}

} // namespace Error


/** A namespace used for the expressions directory */
namespace Expression {

    /** A namespace used to designate certain items in expression as private
     *
     *  These members should not be called outside of the expression directory
     *  This is useful for helper functions templated functions call
     */
    namespace Private {}

} // namespace Expression

/** A namespace that contains the various Op classes */
namespace Op {

    /** A namespace that contains various FP Op classes */
    namespace FP {}

} // namespace Op


/** A namespace used for the simplifications directory */
namespace Simplification {

    /** A namespace used to designate certain items in Simplifications as private
     *
     *  These members should not be called outside of the simplifications directory
     */
    namespace Private {}

    /** A namespace which contains the simplifiers */
    namespace Simplifier {

        /** A namespace for bv Simplifiers */
        namespace BV {}
        /** A namespace for shift Simplifiers */
        namespace Shift {}
        /** A namespace for boolean Simplifiers */
        namespace Boolean {}
        /** A namespace for bitwise Simplifiers */
        namespace Bitwise {}

    } // namespace Simplifier

} // namespace Simplification

/** A namespace used for members which create expressions with ops
 *
 *  These are analogous to functions like __add__ in claripy; they create
 *  an op via a factory, then create an expression with said op
 */
namespace Create {

    /** A namespace for FP creation functions */
    namespace FP {}

    /** A namespace for private members of Create */
    namespace Private {}
} // namespace Create

/** A namespace used for unimplemented dummy objects that are required for compilation
 *
 * These objects will be replaced later, but for now Dummy stand-ins allow for testing
 * the rest of the system without implementing these first
 */
namespace Dummy {}

/** A namespace used for the annotations directory */
namespace Annotation {}


/** A namespace used for unittesting instrumentation */
namespace UnitTest {}


/** Disable compilation */
#error This file exists only for documentation purposes
