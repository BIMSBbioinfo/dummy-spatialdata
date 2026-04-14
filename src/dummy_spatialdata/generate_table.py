# generate anndata
def generate_anndata(n_obs=12, n_vars=20):
    obs = pd.DataFrame(index=[f'obs_{i}' for i in range(n_obs)])
    var = pd.DataFrame(index=[f'var_{i}' for i in range(n_vars)])
    X = np.random.rand(n_obs, n_vars)
    adata = ad.AnnData(X=X, obs=obs, var=var)
    return adata