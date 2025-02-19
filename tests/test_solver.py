# pylint: disable=  [no-self-use,missing-class-docstring]

import unittest
import logging
import nose
import claripy

l = logging.getLogger('claripy.test.solver')

class TestSolver(unittest.TestCase):
    def test_solver(self):
        self.raw_solver(claripy.Solver, True)
        self.raw_solver(claripy.Solver, False)

    def test_solver_Replacement(self):
        self.raw_solver(claripy.SolverReplacement, True)
        self.raw_solver(claripy.SolverReplacement, False)

    def test_solver_Hybrid(self):
        self.raw_solver(claripy.SolverHybrid, True)
        self.raw_solver(claripy.SolverHybrid, False)

    def test_solver_Composite(self):
        self.raw_solver(claripy.SolverComposite, True)
        self.raw_solver(claripy.SolverComposite, False)

    def test_solver_Cacheless(self):
        self.raw_solver(claripy.SolverCacheless, True)
        self.raw_solver(claripy.SolverCacheless, False)

    def test_hybrid_solver(self):
        self.raw_hybrid_solver(True)
        self.raw_hybrid_solver(False)


    def raw_hybrid_solver(self,reuse_z3_solver):

        claripy._backend_z3.reuse_z3_solver = reuse_z3_solver

        s = claripy.SolverHybrid()

        x = claripy.BVS('x', 32, min=0, max=10, stride=2)
        y = claripy.BVS('y', 32, min=20, max=30, stride=5)

        # TODO: for now, the stride isn't respected in symbolic mode, but we'll fix that next.
        # until we do, let's add constraints
        s.add(x <= 10)
        s.add(x % 2 == 0)
        s.add(y >= 20)
        s.add(y <= 30)
        s.add((y-20) % 5 == 0)
        s.add(x != 8)

        nose.tools.assert_equal(sorted(s.eval(x, 20, exact=False)), [0, 2, 4, 6, 8, 10])
        nose.tools.assert_equal(sorted(s.eval(x, 20)), [0, 2, 4, 6, 10])
        nose.tools.assert_equal(sorted(s.eval(y, 20, exact=False)), [20, 25, 30])
        nose.tools.assert_equal(sorted(s.eval(y, 20)), [20, 25, 30])

        # test approximate_first option
        s._approximate_first = True
        old_solve_count = claripy._backends_module.backend_z3.solve_count
        nose.tools.assert_equal(sorted(s.eval(x, 20)), [0, 2, 4, 6, 8, 10])
        nose.tools.assert_equal(claripy._backends_module.backend_z3.solve_count, old_solve_count)
        s._approximate_firsrt = False

        # now constrain things further so that the VSA overapproximates
        s.add(x <= 4)
        nose.tools.assert_equal(sorted(s.eval(x, 20, exact=False)), [0, 2, 4])
        nose.tools.assert_equal(sorted(s.eval(x, 20)), [0, 2, 4])

        s.add(y >= 27)
        nose.tools.assert_equal(s.eval(y, 20, exact=False), (30,))
        nose.tools.assert_equal(s.eval(y, 20), (30,))

        t = claripy.SolverHybrid()
        x = claripy.BVS('x', 32)
        t.add(x <= 10)
        print(t.eval(x, 80, exact=False))
        nose.tools.assert_equal(len(t.eval(x, 5, exact=False)), 5)
        nose.tools.assert_equal(len(t.eval(x, 5, exact=False)), 5)
        nose.tools.assert_equal(len(t.eval(x, 6, exact=False)), 6)
        nose.tools.assert_equal(len(t.eval(x, 8, exact=False)), 8)
        nose.tools.assert_equal(len(t.eval(x, 99, exact=False)), 11)


    def test_replacement_solver(self):
        self.raw_replacement_solver(True)
        self.raw_replacement_solver(False)

    def raw_replacement_solver(self,reuse_z3_solver):

        claripy._backend_z3.reuse_z3_solver = reuse_z3_solver

        sr = claripy.SolverReplacement()
        x = claripy.BVS('x', 32)
        nose.tools.assert_equal(len(sr.eval(x, 10)), 10)
        sr.add_replacement(x, claripy.BVV(0x101, 32))
        nose.tools.assert_equal(sr.eval(x, 10), (0x101,))

        y = claripy.BVS('y', 32)
        sr.add([y+1 == 200])
        assert (y+1).cache_key in sr._replacements
        assert sr._replacement(y+1) is claripy.BVV(200, 32)

        srb = sr.branch()
        assert len(srb.constraints) == len(sr.constraints) #pylint:disable=no-member
        assert (y+1).cache_key in sr._replacements
        assert sr._replacement(y+1) is claripy.BVV(200, 32)

        sr = claripy.SolverReplacement()
        b = claripy.BoolS('b')
        assert sr._replacement(b) is b
        sr.add(claripy.Not(b))
        assert sr._replacement(b) is claripy.false

        sr = claripy.SolverReplacement(claripy.SolverVSA(), complex_auto_replace=True)
        x = claripy.BVS('x', 64)
        sr.add([x + 8 <= 0xffffffffffffffff])
        sr.add([x + 8 >= 0])
        assert sr._replacement(x) is not x

    def raw_solver(self, solver_type, reuse_z3_solver):
        #bc = claripy.backends.BackendConcrete(clrp)
        #bz = claripy.backends.BackendZ3(clrp)
        #claripy.expression_backends = [ bc, bz, ba ]

        claripy._backend_z3.reuse_z3_solver = reuse_z3_solver

        s = solver_type()

        s.simplify()

        x = claripy.BVS('x', 32)
        y = claripy.BVS('y', 32)
        z = claripy.BVS('z', 32)

        l.debug("adding constraints")

        s.add(x == 10)
        s.add(y == 15)

        # Batch evaluation
        results = s.batch_eval([x + 5, x + 6, 3], 2)
        nose.tools.assert_equal(len(results), 1)
        nose.tools.assert_equal(results[0][0], 15) # x + 5
        nose.tools.assert_equal(results[0][1], 16) # x + 6
        nose.tools.assert_equal(results[0][2], 3)  # constant

        l.debug("checking")
        nose.tools.assert_true(s.satisfiable())
        nose.tools.assert_false(s.satisfiable(extra_constraints=[x == 5]))
        nose.tools.assert_equal(s.eval(x + 5, 1)[0], 15)
        nose.tools.assert_true(s.solution(x + 5, 15))
        nose.tools.assert_true(s.solution(x, 10))
        nose.tools.assert_true(s.solution(y, 15))
        nose.tools.assert_false(s.solution(y, 13))

        shards = s.split()
        nose.tools.assert_equal(len(shards), 2)
        nose.tools.assert_equal(len(shards[0].variables), 1)
        nose.tools.assert_equal(len(shards[1].variables), 1)
        if isinstance(s, claripy.frontend_mixins.ConstraintExpansionMixin) or (
            isinstance(s, claripy.frontends.HybridFrontend) and
            isinstance(s._exact_frontend, claripy.frontend_mixins.ConstraintExpansionMixin)
        ): #the hybrid frontend actually uses the exact frontend for the split
            nose.tools.assert_equal({ len(shards[0].constraints), len(shards[1].constraints) }, { 2, 1 }) # adds the != from the solution() check
        if isinstance(s, claripy.frontends.ReplacementFrontend):
            nose.tools.assert_equal({ len(shards[0].constraints), len(shards[1].constraints) }, { 1, 1 }) # not a caching frontend

        # test result caching
        s = solver_type()
        s.add(x == 10)
        s.add(y == 15)
        nose.tools.assert_false(s.satisfiable(extra_constraints=(x==5,)))
        nose.tools.assert_true(s.satisfiable())

        s = solver_type()
        #claripy.expression_backends = [ bc, ba, bz ]
        s.add(claripy.UGT(x, 10))
        s.add(claripy.UGT(x, 20))
        s.simplify()
        nose.tools.assert_equal(len(s.constraints), 1)
        #nose.tools.assert_equal(str(s.constraints[0]._obj), "Not(ULE(x <= 20))")

        s.add(claripy.UGT(y, x))
        s.add(claripy.ULT(z, 5))

        # test that duplicate constraints are ignored
        old_count = len(s.constraints)
        s.add(claripy.ULT(z, 5))
        nose.tools.assert_equal(len(s.constraints), old_count)

        #print("========================================================================================")
        #print("========================================================================================")
        #print("========================================================================================")
        #print("========================================================================================")
        #a = s.eval(z, 100)
        #print("ANY:", a)
        #print("========================================================================================")
        #mx = s.max(z)
        #print("MAX",mx)
        #print("========================================================================================")
        #mn = s.min(z)
        #print("MIN",mn)
        #print("========================================================================================")
        #print("========================================================================================")
        #print("========================================================================================")
        #print("========================================================================================")

        print("CONSTRAINT COUNTS:", [ len(_.constraints) for _ in s.split() ])

        nose.tools.assert_equal(s.max(z), 4)
        nose.tools.assert_equal(s.min(z), 0)
        nose.tools.assert_equal(s.min(y), 22)
        nose.tools.assert_equal(s.max(y), 2**y.size()-1)

        print("CONSTRAINT COUNTS:", [ len(_.constraints) for _ in s.split() ])

        ss = s.split()
        nose.tools.assert_equal(len(ss), 2)
        #if isinstance(s, claripy.frontend_mixins.ConstraintExpansionMixin):
        #   nose.tools.assert_equal({ len(_.constraints) for _ in ss }, { 3, 2 }) # constraints from min or max

        # Batch evaluation
        s.add(y < 24)
        s.add(z < x) # Just to make sure x, y, and z belong to the same solver, since batch evaluation does not support the
                     # situation where expressions belong to more than one solver
        results = s.batch_eval([x, y, z], 20)
        nose.tools.assert_set_equal(
            set(results),
            {(21, 23, 1), (22, 23, 3), (22, 23, 2), (22, 23, 4), (21, 22, 4), (21, 23, 4), (22, 23, 0),
             (22, 23, 1), (21, 22, 1), (21, 22, 3), (21, 22, 2), (21, 22, 0), (21, 23, 0), (21, 23, 2),
             (21, 23, 3)
            }
        )

        # test that False makes it unsat
        s = solver_type()
        s.add(claripy.BVV(1,1) == claripy.BVV(1,1))
        nose.tools.assert_true(s.satisfiable())
        s.add(claripy.BVV(1,1) == claripy.BVV(0,1))
        nose.tools.assert_false(s.satisfiable())

        # test extra constraints
        s = solver_type()
        x = claripy.BVS('x', 32)
        nose.tools.assert_equal(s.eval(x, 2, extra_constraints=[x==10]), ( 10, ))
        s.add(x == 10)
        nose.tools.assert_false(s.solution(x, 2))
        nose.tools.assert_true(s.solution(x, 10))

        # test signed min/max
        s = solver_type()
        x = claripy.BVS('x', 32)
        nose.tools.assert_equal(s.min(x, signed=True), -0x80000000)
        nose.tools.assert_equal(s.max(x, signed=True), 0x7FFFFFFF)
        s.add(claripy.ULE(x, 0x40000000) | claripy.UGE(x, 0xC0000000))
        nose.tools.assert_equal(s.min(x, signed=True), -0x40000000)
        nose.tools.assert_equal(s.max(x, signed=True), 0x40000000)

        # test result caching

        if isinstance(s, claripy.frontend_mixins.ModelCacheMixin):
            count = claripy._backends_module.backend_z3.solve_count

            s = solver_type()
            x = claripy.BVS('x', 32)
            s.add(x == 10)
            nose.tools.assert_true(s.satisfiable())
            assert claripy._backends_module.backend_z3.solve_count == count
            nose.tools.assert_equal(s.eval(x, 1)[0], 10)
            assert claripy._backends_module.backend_z3.solve_count == count
            s.add(x == 10)
            s.add(x > 9)
            nose.tools.assert_equal(s.eval(x, 1)[0], 10)
            assert claripy._backends_module.backend_z3.solve_count == count

            y = claripy.BVS('y', 32)
            s.add(y < 999)
            assert s.satisfiable()
            assert claripy._backends_module.backend_z3.solve_count == count
            nose.tools.assert_equal(s.eval(y, 1)[0], 0)
            assert claripy._backends_module.backend_z3.solve_count == count

    def test_solver_branching_Solver(self):
        self.raw_solver_branching(claripy.Solver, True)
        self.raw_solver_branching(claripy.Solver, False)

    def test_solver_branching_SolverReplacement(self):
        self.raw_solver_branching(claripy.SolverReplacement, True)
        self.raw_solver_branching(claripy.SolverReplacement, False)

    def test_solver_branching_SolverHybrid(self):
        self.raw_solver_branching(claripy.SolverHybrid, True)
        self.raw_solver_branching(claripy.SolverHybrid, False)

    def test_solver_branching_SolverComposite(self):
        self.raw_solver_branching(claripy.SolverComposite, True)
        self.raw_solver_branching(claripy.SolverComposite, False)

    def test_solver_branching_SolverCacheless(self):
        self.raw_solver_branching(claripy.SolverCacheless, True)
        self.raw_solver_branching(claripy.SolverCacheless, False)


    def raw_solver_branching(self, solver_type, reuse_z3_solver):
        claripy._backend_z3.reuse_z3_solver = reuse_z3_solver

        s = solver_type()
        x = claripy.BVS("x", 32)
        y = claripy.BVS("y", 32)
        s.add(claripy.UGT(x, y))
        s.add(claripy.ULT(x, 10))

        nose.tools.assert_greater(s.eval(x, 1)[0], 0)

        t = s.branch()
        if isinstance(s, claripy.frontends.FullFrontend):
            nose.tools.assert_is(s._tls.solver, t._tls.solver)
            nose.tools.assert_true(s._finalized)
            nose.tools.assert_true(t._finalized)
        t.add(x == 5)
        #if isinstance(s, claripy.FullFrontend):
        #   nose.tools.assert_is(t._solver, None)

        s.add(x == 3)
        nose.tools.assert_true(s.satisfiable())
        t.add(x == 3)
        nose.tools.assert_false(t.satisfiable())

        s.add(y == 2)
        nose.tools.assert_true(s.satisfiable())
        nose.tools.assert_equal(s.eval(x, 1)[0], 3)
        nose.tools.assert_equal(s.eval(y, 1)[0], 2)
        nose.tools.assert_false(t.satisfiable())

    def test_combine_Solver(self):
        self.raw_combine(claripy.Solver,True)
        self.raw_combine(claripy.Solver,False)

    def test_combine_SolverReplacement(self):
        self.raw_combine(claripy.SolverReplacement,True)
        self.raw_combine(claripy.SolverReplacement,False)

    def test_combine_SolverHybrid(self):
        self.raw_combine(claripy.SolverHybrid,True)
        self.raw_combine(claripy.SolverHybrid,False)

    def test_combine_SolverComposite(self):
        self.raw_combine(claripy.SolverComposite,True)
        self.raw_combine(claripy.SolverComposite,False)

    def test_combine_SolverCacheless(self):
        self.raw_combine(claripy.SolverCacheless,True)
        self.raw_combine(claripy.SolverCacheless,False)

    def raw_combine(self, solver_type, reuse_z3_solver):
        claripy._backend_z3.reuse_z3_solver = reuse_z3_solver

        s10 = solver_type()
        s20 = solver_type()
        s30 = solver_type()
        x = claripy.BVS("x", 32)

        s10.add(x >= 10)
        s20.add(x <= 20)
        s30.add(x == 30)

        nose.tools.assert_true(s10.satisfiable())
        nose.tools.assert_true(s20.satisfiable())
        nose.tools.assert_true(s30.satisfiable())
        nose.tools.assert_true(s10.combine([s20]).satisfiable())
        nose.tools.assert_true(s20.combine([s10]).satisfiable())
        nose.tools.assert_true(s30.combine([s10]).satisfiable())
        nose.tools.assert_false(s30.combine([s20]).satisfiable())
        nose.tools.assert_equal(s30.combine([s10]).eval(x, 1), ( 30, ))
        nose.tools.assert_equal(len(s30.combine([s10]).constraints), 2)

    def test_composite_solver_with_strings(self):
        try:
            s = claripy.SolverComposite(
                template_solver_string=claripy.SolverCompositeChild(backend=claripy.backend_manager.backends.smtlib_cvc4))
            x = claripy.BVS("x", 32)
            y = claripy.BVS("y", 32)
            z = claripy.BVS("z", 32)
            str_1 = claripy.StringS("sym_str_1", 1024)
            c = claripy.And(x == 1, y == 2, z == 3, str_1 == claripy.StringV("cavallo"))
            s.add(c)
            nose.tools.assert_equal(len(s._solver_list), 4)
            nose.tools.assert_true(s.satisfiable())
            nose.tools.assert_equal(list(s.eval(str_1, 1)), ["cavallo"])
        except claripy.errors.MissingSolverError:
            raise nose.SkipTest()


    def test_composite_solver(self):
        self.raw_composite_solver(True)
        self.raw_composite_solver(False)


    def raw_composite_solver(self, reuse_z3_solver):
        claripy._backend_z3.reuse_z3_solver = reuse_z3_solver

        #pylint:disable=no-member
        s = claripy.SolverComposite()
        x = claripy.BVS("x", 32)
        y = claripy.BVS("y", 32)
        z = claripy.BVS("z", 32)
        c = claripy.And(x == 1, y == 2, z == 3)
        s.add(c)
        nose.tools.assert_equal(len(s._solver_list), 3)
        nose.tools.assert_true(s.satisfiable())

        s.add(x < y)
        nose.tools.assert_equal(len(s._solver_list), 2)
        nose.tools.assert_true(s.satisfiable())

        s.simplify()
        nose.tools.assert_equal(len(s._solver_list), 3)
        nose.tools.assert_true(s.satisfiable())

        s1 = s.branch()
        nose.tools.assert_equal(len(s1._solver_list), 3)

        s1.add(x > y)
        nose.tools.assert_equal(len(s1._solver_list), 2)
        nose.tools.assert_false(s1.satisfiable())
        nose.tools.assert_equal(len(s._solver_list), 3)
        nose.tools.assert_true(s.satisfiable())

        s.add(claripy.BVV(1, 32) == claripy.BVV(2, 32))
        nose.tools.assert_equal(len(s._solver_list), 3)
        nose.tools.assert_false(s.satisfiable())

        ss = s.branch()
        nose.tools.assert_equal(len(ss._solver_list), 3)
        nose.tools.assert_false(ss.satisfiable())

        s = claripy.SolverComposite()
        x = claripy.BVS("x", 32)
        y = claripy.BVS("y", 32)
        z = claripy.BVS("z", 32)
        c = claripy.And(x == 1, y == 2, z > 3)
        s.add(c)

        if isinstance(s._template_frontend, claripy.frontend_mixins.ModelCacheMixin):
            assert len(s._solver_list) == 3
            count = claripy._backends_module.backend_z3.solve_count
            assert s.satisfiable()
            assert claripy._backends_module.backend_z3.solve_count == count + 3
            assert list(s.eval(x+y, 1)) == [3]
            assert claripy._backends_module.backend_z3.solve_count == count + 3


    def test_minmax(self):
        self.raw_minmax(True)
        self.raw_minmax(False)

    def raw_minmax(self,reuse_z3_solver):
        claripy._backend_z3.reuse_z3_solver = reuse_z3_solver

        s = claripy.Solver()
        x = claripy.BVS("x", 32)

        nose.tools.assert_equal(s.max(x), 2**32-1)
        nose.tools.assert_equal(s.min(x), 0)
        nose.tools.assert_true(s.satisfiable())


    def test_composite_discrepancy(self):
        self.raw_composite_discrepancy(True)
        self.raw_composite_discrepancy(False)


    def raw_composite_discrepancy(self,reuse_z3_solver):
        claripy._backend_z3.reuse_z3_solver = reuse_z3_solver

        a = claripy.BVS("a", 8)
        b = claripy.BVS("b", 8)
        x = claripy.BVS("x", 32)
        y = claripy.BVS("y", 32)
        z = claripy.BVS("z", 32)

        xy = x + y
        dst = claripy.BVV(0xbaaaaf50, 32) + xy
        constraints = [ ]
        constraints.append(x <= 0x1)
        constraints.append(x != 0x0)
        constraints.append(claripy.SignExt(24, claripy.If(x > 0x0, a, 0)) != 0xa)
        constraints.append(x < 0x80)
        constraints.append(y <= 0x1)
        constraints.append(x == 0x1)
        constraints.append((0xbaaaaf50 + x) == 0xbaaaaf51)
        constraints.append(y != 0x0)
        constraints.append(claripy.SignExt(24, claripy.If(y > 0x0, b, 0)) != 0xa)
        constraints.append((x + y) < 0x80)
        constraints.append(z <= 0x1)
        constraints.append((x + y) == 0x2)

        sn = claripy.Solver()
        sc = claripy.SolverComposite()

        sn.add(constraints)
        sc.add(constraints)
        print(sn.max(dst), sc.max(dst))
        print(sn.min(dst), sc.min(dst))
        assert sn.max(dst) == sc.max(dst)
        assert sn.min(dst) == sc.min(dst)

    def test_model(self):
        x = claripy.BVS("x", 32)
        y = claripy.BVS("y", 32)
        s = claripy.Solver()

        s.add(x < 10)
        assert sorted(s.eval(x, 20)) == list(range(10))
        s.add(y == 1337)
        assert sorted(s.eval(x, 20)) == list(range(10))

    def test_unsatness(self):
        x = claripy.BVS("x", 32)

        s = claripy.Solver()
        s.add(x == 10)
        assert s.satisfiable()
        s.add(claripy.false)
        assert not s.satisfiable()

    def test_simplification_annotations(self):
        s = claripy.Solver()
        x = claripy.BVS("x", 32)

        s.add(x > 10)
        s.add(x > 11)
        s.add((x > 12).annotate(claripy.SimplificationAvoidanceAnnotation()))

        assert len(s.constraints) == 3
        s.simplify()
        assert len(s.constraints) == 2

    def raw_ancestor_merge(self,solver, reuse_z3_solver):
        claripy._backend_z3.reuse_z3_solver = reuse_z3_solver

        s = solver()
        x = claripy.BVS("x", 32)
        y = claripy.BVS("y", 32)
        z = claripy.BVS("z", 32)

        s.add(x == 10)
        s.add(y == x)

        p = s.branch()
        q = s.branch()
        p.add(z == 1)
        q.add(z == 2)

        r = p.merge([q], [claripy.true, claripy.true])[-1]
        t = p.merge([q], [p.constraints[-1], q.constraints[-1]], common_ancestor=s)[-1]

        if not isinstance(r, claripy.frontends.CompositeFrontend):
            assert len(r.constraints) == 1
        assert len(t.constraints) == 3
        assert t.constraints[-1].variables == z.variables
        assert t.constraints[-1].op == 'Or'
        assert len(t.constraints[-1].args) == 2

    def test_ancestor_merge_Solver(self):
        self.raw_ancestor_merge(claripy.Solver,True)
        self.raw_ancestor_merge(claripy.Solver,False)

    def test_ancestor_merge_SolverReplacement(self):
        self.raw_ancestor_merge(claripy.SolverReplacement,True)
        self.raw_ancestor_merge(claripy.SolverReplacement,False)

    def test_ancestor_merge_SolverHybrid(self):
        self.raw_ancestor_merge(claripy.SolverHybrid,True)
        self.raw_ancestor_merge(claripy.SolverHybrid,False)

    def test_ancestor_merge_SolverComposite(self):
        self.raw_ancestor_merge(claripy.SolverComposite,True)
        self.raw_ancestor_merge(claripy.SolverComposite,False)

    def test_ancestor_merge_SolverCacheless(self):
        self.raw_ancestor_merge(claripy.SolverCacheless,True)
        self.raw_ancestor_merge(claripy.SolverCacheless,False)


    def raw_unsat_core(self,solver, reuse_z3_solver):
        claripy._backend_z3.reuse_z3_solver = reuse_z3_solver

        s = solver(track=True)
        x = claripy.BVS("x", 32)
        y = claripy.BVS("y", 32)
        z = claripy.BVS("z", 32)
        a = claripy.BVS("a", 32)

        s.add(x == y)
        s.add(x == 1)
        s.add(z != a)
        s.add(z == 2)
        s.add(a == 2)

        assert not s.satisfiable()
        unsat_core = s.unsat_core()
        assert len(unsat_core) == 3
        assert unsat_core[0] is not None
        assert unsat_core[1] is not None
        assert unsat_core[2] is not None

    def test_unsat_core_Solver(self):
        self.raw_unsat_core(claripy.Solver, True)
        self.raw_unsat_core(claripy.Solver, False)

    def test_unsat_core_SolverHybrid(self):
        self.raw_unsat_core(claripy.SolverHybrid, True)
        self.raw_unsat_core(claripy.SolverHybrid, False)

    def test_unsat_core_SolverComposite(self):
        self.raw_unsat_core(claripy.SolverComposite, True)
        self.raw_unsat_core(claripy.SolverComposite, False)

    def test_unsat_core_SolverCacheless(self):
        self.raw_unsat_core(claripy.SolverCacheless, True)
        self.raw_unsat_core(claripy.SolverCacheless, False)


    def test_zero_division_in_cache_mixin(self):
        # Bug in the caching backend. See issue #49 on github.
        num = claripy.BVS('num', 256)
        denum = claripy.BVS('denum', 256)
        e = claripy.BVS('e', 256)
        s = claripy.Solver()
        s.add(e == 8)
        assert s.satisfiable()
        s.add(claripy.If(denum == 0, 0, num / denum) == e)
        assert s.satisfiable()
        # As a bonus:
        s.add(num == 16)
        assert s.satisfiable()
        s.add(denum == 3)
        assert not s.satisfiable()

    def test_composite_solver_branching_optimizations(self):
        s = claripy.SolverComposite()
        w = claripy.BVS("w", 32)
        x = claripy.BVS("x", 32)
        y = claripy.BVS("y", 32)
        z = claripy.BVS("z", 32)

        s.add(w == 10)
        assert len(s._unchecked_solvers) == 1
        assert s.satisfiable()
        s.add(x == 10)
        assert len(s._unchecked_solvers) == 1

        s2 = s.branch()
        assert len(s2._unchecked_solvers) == 1
        assert s.satisfiable()
        assert len(s._unchecked_solvers) == 0
        assert len(s2._unchecked_solvers) == 1
        s.add(y == 10)
        assert len(s._unchecked_solvers) == 1
        assert len(s2._unchecked_solvers) == 1
        s2.add(z == 10)
        assert len(s._unchecked_solvers) == 1
        assert len(s2._unchecked_solvers) == 2
        assert s2.satisfiable()
        assert len(s._unchecked_solvers) == 1
        assert len(s2._unchecked_solvers) == 0

        s2.add(z == 12)
        assert not s2.satisfiable()
        assert not s2.satisfiable()

    def test_exhaustion(self):
        s = claripy.Solver()
        x = claripy.BVS('x', 32)
        s.add(x >= 19)
        assert s.min(x) == 19

        s = claripy.Solver()
        x = claripy.BVS('x', 32)
        s.add(x <= 19)
        assert s.max(x) == 19

if __name__ == '__main__':
    unittest.main()
