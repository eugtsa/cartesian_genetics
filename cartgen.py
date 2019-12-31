"""
This is the main module of cartesian_genetics library
"""

import random
import numpy as np
import logging
from cartesian_genetics_base.cartesian_genome_func import CartesianGenomeFunc

class CartGenModel:
    """

    """
    def __init__(self,
                 metric_to_minimize=None,
                 n_generations = 20,
                 samples_in_gen = 50,
                 elitarity_n = 5,
                 mutation_points = 3,
                 tqdm=None,
                 n_inputs = None,
                 n_outputs = None,
                 depth = None,
                 n_rows = 1,
                 basis_funcs = None,
                 recurse_depth = 5,
                 arity = None,
                 seed = None,
                 cgf = None):
        """CGP Model for ML

        Uses regression with cartesian genome function, optimized with elitarity N+lambda genetic process

        Args:
            metric_to_minimize (callable): metric function with signature analogous to sklearn (see sklearn metrics) to minimize
            n_generations (int): number of generations to evolve
            samples_in_gen (int): number of samples in each generation for each elitary sample
            elitarity_n (int): number of elite best samples to save
            mutation_points (int): number of points to mutate in each elitary sample on new samples acquisition
            tqdm (callable): tqdm function with signature: lambda x: x . Use tqdm or tqdm_notebook from tqdm package
            n_inputs (int): number on inputs
            n_outputs (int): number of outputs
            depth (int): depth of genome func representation
            n_rows (int): number of functions on each layer of depth
            recurse_depth (int): depth of previous layers allowed to transmit inputs to each next level
            arity (int): arity of basis functions, if not set then would be determined automatically on given basis
            seed (int): random seed for random operations (init_random_genome and such)
            basis_funcs (list): list of callable, basis functions for genome func representations
            cgf (CartesianGenomeFunc) : function to use as cgf if you don't want to create one
        Returns:
            CartesianGenomeFunc: constructed CG function representation

        """
        self.n_generations = n_generations
        self.samples_in_gen = samples_in_gen
        self.elitarity_n = elitarity_n
        self.mutation_points = mutation_points
        self.recurse_depth = recurse_depth
        self.n_inputs = n_inputs,
        self.n_outputs = n_outputs
        self.depth = depth
        self.n_rows = n_rows
        self.basis_funcs = basis_funcs
        self.recurse_depth = 5
        self.arity = arity
        self.seed = seed
        if cgf is not None and isinstance(cgf, CartesianGenomeFunc):
            self.cgf = cgf
            self.not_fitted_yet = False
        else:
            self.cgf = CartesianGenomeFunc(n_inputs=n_inputs,
                                           n_outputs=n_outputs,
                                           depth=depth,
                                           n_rows=n_rows,
                                           basis_funcs=basis_funcs,
                                           recurse_depth=recurse_depth,
                                           arity=arity, seed=seed)
            self.not_fitted_yet = True
        if seed is not None:
            random.seed(seed)
        self.metric_to_minimize = metric_to_minimize
        self.tqdm = tqdm
        if tqdm is None:
            self.tqdm = lambda x: x

    def _set_initial_params(self, arity, basis_funcs, cgf, depth, elitarity_n, metric_to_minimize, mutation_points,
                            n_generations, n_inputs, n_outputs, n_rows, recurse_depth, samples_in_gen, seed, tqdm):
        self.n_generations = n_generations
        self.samples_in_gen = samples_in_gen
        self.elitarity_n = elitarity_n
        self.mutation_points = mutation_points
        self.recurse_depth = recurse_depth
        self.n_inputs = n_inputs,
        self.n_outputs = n_outputs
        self.depth = depth
        self.n_rows = n_rows
        self.basis_funcs = basis_funcs
        self.recurse_depth = 5
        self.arity = arity
        self.seed = seed
        if cgf is not None and isinstance(cgf, CartesianGenomeFunc):
            self.cgf = cgf
            self.not_fitted_yet = False
        else:
            self.cgf = CartesianGenomeFunc(n_inputs=n_inputs,
                                           n_outputs=n_outputs,
                                           depth=depth,
                                           n_rows=n_rows,
                                           basis_funcs=basis_funcs,
                                           recurse_depth=recurse_depth,
                                           arity=arity, seed=seed)
            self.not_fitted_yet = True
        if seed is not None:
            random.seed(seed)
        self.metric_to_minimize = metric_to_minimize
        self.tqdm = tqdm
        if tqdm is None:
            self.tqdm = lambda x: x

    def _get_mutated_samples(self, in_sample, n_points=1, new_samples_count=10):
        while new_samples_count != 0:
            points_to_do = n_points
            new_sample = [v for v in in_sample]
            while points_to_do > 0:
                mutate_point = random.choice([i for i in range(len(in_sample))])
                new_sample = [v if i != mutate_point else random.random() for i, v in enumerate(new_sample)]
                points_to_do -= 1
            yield new_sample
            new_samples_count -= 1

    def get_params(self, deep = False):
        return {'metric_to_minimize':self.metric_to_minimize,
                'n_generations':self.n_generations,
                'samples_in_gen': self.samples_in_gen,
                 'elitarity_n': self.elitarity_n,
                 'mutation_points' :self.mutation_points,
                 'tqdm':self.tqdm,
                 'n_inputs':self.n_inputs,
                 'n_outputs':self.n_outputs,
                 'depth':self.depth,
                 'n_rows':self.n_rows,
                 'basis_funcs':self.basis_funcs,
                 'recurse_depth':self.depth,
                 'arity':self.arity,
                 'seed':self.seed,
                 'cgf':self.cgf}

    def set_params(self,**params):
        self._set_initial_params(**params)
        return self

    def fit(self, X, y):
        """

        Fit X and y: run genetic evolution for some generations and acquire best learned CGF

        Args:
            X (numpy.array): numpy array matrix with features to learn
            y (numpy.array): numpy array matrix with target to learn
        Returns:
            CartGenModel: learned model with best learned self._cgf
        """
        already_scored_cgp = dict()

        cgf = self.cgf

        cgf.init_random_genome()

        preds = cgf.call([X[:, i] for i in range(X.shape[1])])[0]
        self._top_scores = [self.metric_to_minimize(preds, y) for _ in range(self.elitarity_n)]
        self._top_genomes = [cgf.get_genome() for _ in range(self.elitarity_n)]

        # learning genome for some generations
        for gen in self.tqdm(range(self.n_generations)):
            for elitary_mutated_genomes in zip(*[
                self._get_mutated_samples(self._top_genomes[_i_],
                                          n_points=self.mutation_points,
                                          new_samples_count=self.samples_in_gen)
                                          for _i_ in range(len(self._top_genomes))]):

                    for new_sample in elitary_mutated_genomes:
                        if tuple(new_sample) in already_scored_cgp:
                            continue
                        already_scored_cgp[tuple(new_sample)] = 1
                        cgf.set_genome(new_sample)
                        new_preds = cgf.call([X[:, i] for i in range(X.shape[1])])[0]
                        new_score = self.metric_to_minimize(new_preds, y)

                        last_bigger = None
                        already_in = False
                        for i_, old_score in enumerate(self._top_scores):
                            if new_score <= old_score:
                                last_bigger = i_

                        if (last_bigger is not None) and not already_in:
                            self._top_scores[last_bigger] = new_score
                            self._top_genomes[last_bigger] = cgf.get_genome()

        # setting learned genome to self._cgf
        self.cgf.set_genome(self._top_genomes[-1])
        self.not_fitted_yet = False
        return self

    def predict(self, X):
        """

        Predict X by running best fitted CGF function

        Args:
            X (numpy.array): numpy array matrix with features to learn
            y (numpy.array): numpy array matrix with target to learn
        Returns:
            CartGenModel: learned model with best learned self._cgf
        """
        if self.not_fitted_yet:
            logging.error('Model is not fitted! Use fit method or set_params method first!')
            raise NotImplementedError()
        test_preds = self.cgf.call([X[:, i] for i in range(X.shape[1])])

        return np.vstack(test_preds).T
