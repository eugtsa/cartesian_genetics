|project|
========================================

|project| is simple realization of CGP (https://en.wikipedia.org/wiki/Cartesian_genetic_programming)

Look how easy it is to use:

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   api

Features
--------

- support any basis functions with any arity count
- native representation, without any (!) dependencies for python 3.0

Installation
------------

Install |project| by running:

    pip install cartgen

Contribute
----------

- Source Code: github.com/|author|/|project_github|

Fast Example
-------------

You can use ``CartGenModel`` as sklearn regression model:

First, let's setup everything:

::

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

Then create some basis functions.  ``CartGenModel`` is created with usage as ML model in mind so let's take basis
functions from numpy:

::

    import numpy as np

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

Let's create model. Underneath it would start optimisation problem and evolve best fitted species for us:

::

    from cartgen import CartGenModel
    from tqdm import tqdm_notebook


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

And last but not least is predict:

::

    test_preds = model.predict(X_test)
    print(mean_absolute_error(test_preds,y_test))


Using together with bagging regressor from sklearn
---------------------------------------------------

::

    from sklearn.ensemble import BaggingRegressor

    bclf = BaggingClassifier(base_estimator=model, n_estimators=10, max_samples=1.0, max_features=1.0, bootstrap=True,
                                   bootstrap_features=False, oob_score=False,
                                   warm_start=False, n_jobs=None, random_state=None, verbose=0)

    bclf.fit(X_train,y_train)

    test_preds = bclf.predict(X_test)
    print(mean_absolute_error(test_preds,y_test))

Support
-------

Author's mail: eugtsa@gmail.com

License
-------

The project is licensed under the BSD license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
