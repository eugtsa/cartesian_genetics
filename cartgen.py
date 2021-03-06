"""
``cartgen`` is module with models which could be used with sklearn library.




Copyright (C) 2021 Evgenii Tsatsorin eugtsa@gmail.com 
Full license in LICENSE file.

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

import random
import numpy as np
import logging
from cartesian_genetics_base.cartesian_genome_func import CartesianGenomeFunc

class CartGenModel:
    """``CartGenModel`` is a class with model which could process any ML task (regression, classification, multiclass,
    etc). It utilizes sklearn interface for usage. It consists of simple generations-based optimizer for
    ``CartesianGenomeFunc`` and any custom metric.

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
            full_mutate_prob (float): probability of all possible mutation occurs for some individual
            basis_funcs (list): list of callable, basis functions for genome func representations
            cgf (CartesianGenomeFunc) : function to use as cgf if you don't want to create one

    Examples:

        ::

            import numpy as np
            from cartgen import CartGenModel
            from tqdm import tqdm_notebook
            from sklearn.datasets import load_digits
            from sklearn.metrics import mean_absolute_error
            from sklearn.model_selection import train_test_split
            from sklearn.utils import shuffle
            from sklearn.preprocessing import StandardScaler

            dataset = load_digits()
            data,target = dataset['data'],dataset['target']

            data,target = shuffle(data,target,random_state=1)
            data = StandardScaler().fit_transform(data)

            X_train,X_test,y_train,y_test = train_test_split(data,target,test_size=0.33,random_state=42)

            def sqrt(x):
                return np.sqrt(np.abs(x))

            def log(x):
                return np.log(np.abs(x+0.00001))

            def summ(x,y):
                return x+y

            def diff(x,y):
                return x-y

            def div(x,y):
                return x/(y+0.1)

            def neg(x):
                return -x

            def mult(x,y):
                return x*y

            def div_2(x):
                return x/2

            def mult_3(x):
                return x*3

            def abss(x):
                return np.abs(x)


            basis = [sqrt,log,neg,summ,mult,div,abss,div_2,mult_3,diff]

            model = CartGenModel(metric_to_minimize=mean_absolute_error,
                                 n_generations=150,
                                samples_in_gen=50,
                                mutation_points=3,
                                elitarity_n=9,
                                tqdm=tqdm_notebook,
                                n_inputs=X_train.shape[1],
                                n_outputs=1,
                                depth=36,
                                recurse_depth=9,
                                basis_funcs=basis,
                                seed=9,
                                n_rows=1)

            model.fit(X_train,y_train)

            test_preds = model.predict(X_test)
            print(mean_absolute_error(test_preds,y_test))

        ::

            from sklearn.ensemble import BaggingRegressor

            bclf = BaggingClassifier(base_estimator=model, n_estimators=10, max_samples=1.0, max_features=1.0, bootstrap=True,
                                           bootstrap_features=False, oob_score=False,
                                           warm_start=False, n_jobs=None, random_state=None, verbose=0)

            bclf.fit(X_train,y_train)

            test_preds = bclf.predict(X_test)
            print(mean_absolute_error(test_preds,y_test))

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
                 full_mutate_prob = 0.0,
                 seed = None,
                 cgf = None):
        """CGP Model for ML. Uses regression with cartesian genome function, optimized with elitarity N+lambda genetic process

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
            full_mutate_prob (float): probability of all possible mutation occurs for some individual
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
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.depth = depth
        self.n_rows = n_rows
        self.basis_funcs = basis_funcs
        self.full_mutate_prob = full_mutate_prob
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

        if self.arity is None:
            self.arity = self.cgf._arity
        if seed is not None:
            random.seed(seed)
        self.metric_to_minimize = metric_to_minimize
        self.tqdm = tqdm
        if tqdm is None:
            self.tqdm = lambda x: x

    def _set_initial_params(self, arity, basis_funcs, cgf, depth, elitarity_n, metric_to_minimize, mutation_points,
                            n_generations, n_inputs, n_outputs, n_rows, recurse_depth, samples_in_gen, seed, tqdm,full_mutate_prob):
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
        self.full_mutate_prob = full_mutate_prob
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

    def _get_mutated_samples(self, in_sample, n_points=1, new_samples_count=10, full_mutate_prob=0.0):
        while new_samples_count != 0:
            points_to_do = n_points
            new_sample = [v for v in in_sample]

            while points_to_do > 0:
                mutate_point = random.choice([i for i in range(len(in_sample))])
                new_sample[mutate_point] = random.random()
                points_to_do -= 1

            if full_mutate_prob>0:
                if random.random()<full_mutate_prob:
                    if mutate_point%3!=0:
                        n_to_mutate = self.arity*self.n_rows
                    else:
                        n_to_mutate = len(self.basis_funcs)

                    for i in range(n_to_mutate):
                        returned_sample = [v for v in new_sample]
                        returned_sample[mutate_point] = float(i)/n_to_mutate
                        yield returned_sample

                    new_samples_count -= 1
                    continue

            yield new_sample
            new_samples_count -= 1

    def get_params(self, deep=False):
        """Get parameters of fitted estimator (sklearn interface here: https://scikit-learn.org/stable/developers/develop.html#cloning)

        Args:
            deep(bool): sklearn parameter stub

        Returns:
            dict with parameters of estimator
        """
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
                 'cgf':self.cgf,
                 'full_mutate_prob':self.full_mutate_prob}

    def set_params(self,**params):
        """Set parameters of fitted estimator (sklearn interface here: https://scikit-learn.org/stable/developers/develop.html#cloning)

        Args:
            params(kwargs): parameters kwargs

        Returns:
            CartGenModel: model with parameters from kwargs
        """
        if params:
            self._set_initial_params(**params)
        return self

    def fit(self, X, y):
        """Fit X and y: run genetic evolution for some generations and acquire best learned CGF

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
                                          new_samples_count=self.samples_in_gen,
                                          full_mutate_prob = self.full_mutate_prob)
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
        """Predict X by running best fitted CGF function

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
