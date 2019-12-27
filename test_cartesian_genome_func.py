from cartesian_genome_func import CartesianGenomeFunc
import unittest

class TestBoolCartesian(unittest.TestCase):
    def test_simple_get_genome_func(self):
        def neg(x):
            return not x

        basis = [neg,]

        arity=1
        n_inputs = 1
        n_outputs = 1
        depth = 1
        recurse_depth = 1
        n_rows = 1

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)

        chr = bc.get_genome()

        self.assertEqual(len(chr),(n_rows*(arity+1))*depth+n_outputs)

    def test_simple_get_genome_func2(self):
        def neg(x):
            return not x

        basis = [neg,]

        arity=1
        n_inputs = 1
        n_outputs = 1
        depth = 1
        recurse_depth = 1
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)

        chr = bc.get_genome()

        self.assertEqual(len(chr),(n_rows*(arity+1))*depth+n_outputs)

    def test_two_funcs_get_genome_func(self):
        def neg(x):
            return not x

        def identity(x):
            return x

        basis = [neg,identity]

        arity=1
        n_inputs = 1
        n_outputs = 1
        depth = 1
        recurse_depth = 1
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)

        chr = bc.get_genome()

        self.assertEqual(len(chr), (n_rows* (arity + 1)) * depth + n_outputs)

    def test_two_funcs_set_and_get_genome_func(self):
        def neg(x):
            return not x

        def identity(x):
            return x

        basis = [neg,identity]

        arity = 1
        n_inputs = 1
        n_outputs = 1
        depth = 1
        recurse_depth = 1
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)

        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1,0.1,0.1,0.1,0.9999]

        bc.set_genome(some_genome)
        chr = bc.get_genome()

        self.assertEqual(len(chr),(n_rows * (arity + 1)) * depth + n_outputs)

    def test_calculate_genome_simple(self):
        def neg(x):
            return not x

        basis = [neg,]

        arity = 1
        n_inputs = 1
        n_outputs = 1
        depth = 1
        recurse_depth = 1
        n_rows = 1

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)

        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1,0.1,0.1]

        bc.set_genome(some_genome)

        result = bc.call([False,])
        result_must_be = [True,]

        self.assertListEqual(result,result_must_be)

    def test_calculate_genome_simple2(self):
        def neg(x):
            return not x

        basis = [neg,]

        arity = 1
        n_inputs = 1
        n_outputs = 1
        depth = 1
        recurse_depth = 1
        n_rows = 1

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)

        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1,0.1,0.1]

        bc.set_genome(some_genome)

        result = bc.call([True,])
        result_must_be = [False,]

        self.assertListEqual(result,result_must_be)

    def test_calculate_genome_simple3(self):
        def neg(x):
            return not x

        basis = [neg,]

        arity = 1
        n_inputs = 2
        n_outputs = 1
        depth = 1
        recurse_depth = 1
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)

        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1, 0.1, 0.1,0.1,0.1]

        bc.set_genome(some_genome)

        result = bc.call([False, True])
        result_must_be = [True,]

        self.assertListEqual(result,result_must_be)

    def test_calculate_genome_simple4(self):
        def neg(x):
            return not x

        basis = [neg,]

        arity = 1
        n_inputs = 2
        n_outputs = 1
        depth = 1
        recurse_depth = 1
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)
        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1, 0.9, 0.1,0.1,0.1]

        bc.set_genome(some_genome)

        result = bc.call([False, True])
        result_must_be = [False,]

        self.assertListEqual(result,result_must_be)

    def test_calculate_genome_simple5(self):
        def neg(x):
            return not x

        basis = [neg,]

        arity = 1
        n_inputs = 2
        n_outputs = 2
        depth = 1
        recurse_depth = 1
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)
        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1, 0.9, 0.1,0.1,0.1,0.9]

        bc.set_genome(some_genome)

        result = bc.call([False, True])
        result_must_be = [False,True]

        self.assertListEqual(result,result_must_be)

    def test_calculate_genome_recurse(self):
        def neg(x):
            return not x

        basis = [neg,]

        arity = 1
        n_inputs = 2
        n_outputs = 2
        depth = 1
        recurse_depth = 2
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)
        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1, 0.9, 0.1,0.1,0.1,0.7]

        bc.set_genome(some_genome)

        result = bc.call([False, True])
        result_must_be = [False,False]

        self.assertListEqual(result,result_must_be)
    #
    def test_calculate_genome_simple6(self):
        def neg(x):
            return not x

        basis = [neg, ]

        arity = 1
        n_inputs = 2
        n_outputs = 2
        depth = 2
        recurse_depth = 1
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)
        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1, 0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

        bc.set_genome(some_genome)

        result = bc.call([False, True])
        result_must_be = [True, True]

        self.assertListEqual(result, result_must_be)

    def test_calculate_genome_simple7(self):
        def m_one(x):
            return x-1

        def p_one(x):
            return x+1

        basis = [m_one, p_one]

        arity = 1
        n_inputs = 2
        n_outputs = 2
        depth = 2
        recurse_depth = 1
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)
        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1, 0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

        bc.set_genome(some_genome)

        result = bc.call([1, 2])
        result_must_be = [0, 0]

        self.assertListEqual(result, result_must_be)

    def test_calculate_genome_arity_2(self):
        def summ(x,y):
            return x+y

        def div(x,y):
            return x/y

        basis = [summ, div]

        arity = 2
        n_inputs = 3
        n_outputs = 2
        depth = 2
        recurse_depth = 1
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows,
                                 arity=arity)


        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1, 0.9, 0.5, 0.8, 0.1, 0.1, 0.1,0.1, 0.1, 0.1,0.1, 0.1, 0.1, 0.1]

        bc.set_genome(some_genome)

        result = bc.call([1, 2, 10])
        result_must_be = [24, 24]

        self.assertListEqual(result, result_must_be)

    def test_calculate_genome_mixed_arity(self):
        def summ(x,y):
            return x+y

        def m_one(x):
            return x-1

        basis = [summ, m_one]

        n_inputs = 3
        n_outputs = 2
        depth = 2
        recurse_depth = 1
        n_rows = 2

        bc = CartesianGenomeFunc(n_inputs=n_inputs,
                                 n_outputs=n_outputs,
                                 depth=depth,
                                 basis=basis,
                                 recurse_depth=recurse_depth,
                                 n_rows=n_rows)


        # just create some genome set it and then get back
        # this means for each column: which func, then for each of [arity] input which input in cycle
        # last n_output means from which take output in last recurse
        some_genome = [0.1, 0.9, 0.5, 0.8, 0.1, 0.1, 0.1,0.1, 0.1, 0.1,0.1, 0.1, 0.1, 0.1]

        bc.set_genome(some_genome)

        result = bc.call([1, 2, 10])
        result_must_be = [24, 24]

        self.assertListEqual(result, result_must_be)

