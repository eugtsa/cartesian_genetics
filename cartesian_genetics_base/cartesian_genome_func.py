"""
``cartesian_genome_func`` is module with cartesian genome functions representation. Currently consists of pure python
3.x non-optimized ``CartesianGenomeFunc``.




Copyright (C) 2021 Evgenii Tsatsorin eugtsa@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import math
import random
from inspect import signature


class CartesianGenomeFunc:
    """``CartesianGenomeFunc`` class is simple and naive CGP function implementation (https://en.wikipedia.org/wiki/Cartesian_genetic_programming).
    It is still not optimized, goes front to back, propagate through all nodes to calculate result

    Args:
            n_inputs (int): number on inputs
            n_outputs (int): number of outputs
            depth (int): depth of genome func representation
            n_rows (int): number of functions on each layer of depth
            recurse_depth (int): depth of previous layers allowed to transmit inputs to each next level
            arity (int): arity of basis functions, if not set then would be determined automatically on given basis
            seed (int): random seed for random operations (init_random_genome and such)
            basis_funcs (list): list of callable, basis functions for genome func representations
    """
    def __init__(self,
                 n_inputs=None,
                 n_outputs=None,
                 depth=None,
                 n_rows=None,
                 basis_funcs=None,
                 recurse_depth=1,
                 arity=None,
                 seed=None):
        """CGP function representation. Creates cartesian genome function. This function can calculate expressions with given genome and basis.

        Args:
            n_inputs (int): number on inputs
            n_outputs (int): number of outputs
            depth (int): depth of genome func representation
            n_rows (int): number of functions on each layer of depth
            recurse_depth (int): depth of previous layers allowed to transmit inputs to each next level
            arity (int): arity of basis functions, if not set then would be determined automatically on given basis
            seed (int): random seed for random operations (init_random_genome and such)
            basis_funcs (list): list of callable, basis functions for genome func representations

        Returns:
            CartesianGenomeFunc: constructed CG function representation

        """
        self._basis_funcs = basis_funcs
        self._arity = arity
        if arity is None:
            self._count_and_set_max_arity_on_basis(basis_funcs)

        self._n_inputs = n_inputs
        self._n_outputs = n_outputs
        self._depth = depth
        self._recurse_depth = recurse_depth
        self._layers_calls = list()
        self._n_rows = n_rows
        self._layer_funcs = list()

        self._init_layers()
        self.seed = seed
        if seed is not None:
            random.seed(seed)

        self._genome = ([1, ] * self._n_rows * (self._arity + 1)) * self._depth + [1, ] * self._n_outputs

    def _count_and_set_max_arity_on_basis(self, basis):
        max_arity = 0
        for func in basis:
            func_arity = len(signature(func).parameters)
            if func_arity > max_arity:
                max_arity = func_arity

        self._arity = max_arity

    def set_basis(self,new_basis):
        """Set basis functions to this genome function

        Args:
            new_basis (list): list of callables for use as basis functions

        Returns:
            None: nothing to return
        """
        self._basis_funcs = new_basis
        self._count_and_set_max_arity_on_basis()
        self._recreate_layer_funcs()

    def _init_layers(self):
        self._layers_calls.append([False, ] * self._n_inputs)

        for d in range(self._depth):
            self._layers_calls.append([False, ] * self._n_rows)

        self._layers_calls.append([False, ] * self._n_outputs)

    def get_genome(self):
        """Get current genome representation

        Returns:
            list: list of floats with current genome
        """
        return self._genome

    def get_int_genome(self):
        """Get current genome representation as ``int`` type, could be used to well-build optimisation. Todo in 0.0.2 version

        Returns:
            list: list of ints with current genome
        """

    def set_genome(self,new_genome):
        """Validate and set genome using current basis

        Args:
            new_genome: list of floats

        Returns:
            None: inplace operation, returns None
        """
        assert len(new_genome) == self._n_rows*(self._arity+1)*self._depth+self._n_outputs
        assert all([v>=0.0 and v<=1.0 for v in new_genome])
        self._genome = new_genome

        self._recreate_layer_funcs()

    def _recreate_layer_funcs(self):
        if len(self._layer_funcs)!=0:
            self._layer_funcs.clear()

        for l in range(self._depth):
            offset = l*(self._n_rows*(self._arity+1))

            self._layer_funcs.append(list())

            for row_num in range(self._n_rows):
                func_index_from = row_num * (self._arity + 1)
                func_index_to = (row_num+1) * (self._arity + 1)

                func_code,*inputs_codes = self._genome[offset+func_index_from: offset+func_index_to]
                decoded_function = self._get_function_from_basis(func_code)

                # appending func to last layer
                self._layer_funcs[-1].append((decoded_function,inputs_codes))

    def _get_function_from_basis(self,func_num):
        func_index = math.floor(func_num * len(self._basis_funcs))
        return self._basis_funcs[func_index]

    def call(self, input_vals):
        """Call genome function with input vals

        Args:
            input_vals (list): list of input arguments (arguments type depends on basis functions)

        Returns:
            list: output values from output layer
        """
        self._make_top_down_propagation(input_vals)
        return list(self._layers_calls[-1])

    def _make_top_down_propagation(self,inputs):
        for i,v in enumerate(inputs):
            self._layers_calls[0][i] = v

        for l in range(self._depth):
            self._propagate_calls(to_layer=l)

        self._propagate_outputs()

        return self._layers_calls[-1]

    def _propagate_outputs(self):
        last_inputs = self._get_inputs_for_layer(self._depth)
        encoded_outs = self.get_genome()[-self._n_outputs:]

        out_value = self._decode_and_get_inputs(last_inputs,encoded_outs)
        for i,v in enumerate(out_value):
            self._layers_calls[-1][i] = v

    def _propagate_calls(self,to_layer=None):
        layer_functions_with_encoded_inputs = self._layer_funcs[to_layer]
        layer_total_inputs = self._get_inputs_for_layer(to_layer)

        for i,(layer_func,encoded_inputs) in enumerate(layer_functions_with_encoded_inputs):
            func_input = self._decode_and_get_inputs(layer_total_inputs,encoded_inputs)
            func_arity = len(signature(layer_func).parameters)
            func_result = layer_func(*(func_input[:func_arity]))
            self._layers_calls[to_layer+1][i] = func_result

    def _decode_and_get_inputs(self,total_inputs,encoded_inputs):
        return tuple(total_inputs[math.floor(i*len(total_inputs))] for i in encoded_inputs)

    def _get_inputs_for_layer(self, layer_num):
        inputs = list()

        for depth in range(0, self._recurse_depth):
            if layer_num-depth>=0:
                inputs.extend(self._layers_calls[layer_num-depth])

        return inputs

    def init_random_genome(self):
        """Inits random genome with uniform distribution

        Returns:
            None: inits random genome inplace, doesn't return anything
        """
        self.set_genome([random.random() for _ in self._genome])
