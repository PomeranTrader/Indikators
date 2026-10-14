"""
Monte Carlo simulation of the Gold Greed vs Fear PRO scoring logic.

Replicates the Pine Script components in pandas on synthetic H1 bars:
  gold, DXY, US10Y, EURUSD, USDJPY, XAGUSD with regime-switching betas,
  vol clustering and a mean-reverting "gold vs macro" residual.

Purpose: calibrate scaling (zCap, normLen, betaLen, resLen, weights) so the
score has a sensible distribution and the macro-link component carries the
information it is meant to carry. Synthetic data cannot prove predictive
power on real gold, it can only check that the machinery is well scaled.
"""
import numpy as np, pandas as pd, itertools, json, sys, time

rng = np.random.default_rng(42)

# ---------------- synthetic market ----------------
def simulate_market(n=12000, seed=None):
    r = np.random.default_rng(seed)
    # H1 vols (per-bar std) roughly: gold 0.22%, DXY 0.08%, 10Y 1.1 bp, EURUSD 0.08%, USDJPY 0.10%, silver 0.40%
    # regime: 0 = normal macro link (beta_dxy -0.9, beta_y -0.012 per bp), 1 = weak link (-0.25, -0.004)
    p_switch = 1/1500.0
    regime = np.zeros(n, dtype=int)
    for t in range(1, n):
        regime[t] = regime[t-1] if r.random() > p_switch else 1 - regime[t-1]
    # vol clustering (GARCH-like multiplicative factor)
    h = np.ones(n)
    for t in range(1, n):
        h[t] = 0.90*h[t-1] + 0.10*(0.5 + 1.5*r.random()**2)   # mean ~1, bursts
    vmul = np.sqrt(h)
    # macro drivers with cov
    cov = np.array([[1.0, 0.30], [0.30, 1.0]])
    L = np.linalg.cholesky(cov)
    z = r.standard_normal((n, 2)) @ L.T
    rD = 0.0008 * vmul * z[:, 0]              # DXY return
    dY = 1.1 * vmul * z[:, 1]                 # 10Y change in bp
    bD = np.where(regime == 0, -0.9, -0.25)
    bY = np.where(regime == 0, -0.00012, -0.00004)   # per bp -> return
    implied = bD * rD + bY * dY
    # mean-reverting residual level u (gold rich/cheap vs macro), AR(1)
    u = np.zeros(n); phi = 0.985
    eta = 0.0009 * vmul * r.standard_normal(n)
    for t in range(1, n):
        u[t] = phi*u[t-1] + eta[t]
    du = np.diff(u, prepend=0.0)
    eps = 0.0015 * vmul * r.standard_normal(n)
    rG = implied + du + eps + 0.00002       # tiny drift
    # other instruments
    rE = -0.9*rD + 0.0004*vmul*r.standard_normal(n)
    rJ = 0.5*rD + 0.00003*dY + 0.0007*vmul*r.standard_normal(n)
    rS = 1.5*rG + 0.0025*vmul*r.standard_normal(n)
    px = lambda r0, p0: p0*np.exp(np.cumsum(r0))
    df = pd.DataFrame({
        'gold': px(rG, 2400.0), 'dxy': px(rD, 104.0), 'eur': px(rE, 1.08), 'jpy': px(rJ, 150.0), 'xag': px(rS, 28.0),
        'y10': 4.2 + np.cumsum(dY)/100.0, 'regime': regime, 'u': u, 'implied': implied})
    # OHLC for gold from close path with intrabar range
    c = df['gold'].values
    o = np.r_[c[0], c[:-1]]
    rngw = np.abs(0.0018*vmul*r.standard_normal(n)) * c
    df['high'] = np.maximum(o, c) + rngw*0.6
    df['low']  = np.minimum(o, c) - rngw*0.4
    df['open'] = o
    return df

# ---------------- Pine replicas ----------------
def rsi(s, n):
    d = s.diff(); up = d.clip(lower=0); dn = -d.clip(upper=0)
    au = up.ewm(alpha=1/n, adjust=False).mean(); ad = dn.ewm(alpha=1/n, adjust=False).mean()
    return 100 - 100/(1 + au/ad.replace(0, np.nan))
def z(s, n):
    m = s.rolling(n).mean(); sd = s.rolling(n).std(ddof=1)
    return (s - m)/sd
def zscore(zz, cap):
    return 50 + 50*np.clip(zz/cap, -1, 1)
def atr(df, n):
    tr = pd.concat([df.high-df.low, (df.high-df.gold.shift()).abs(), (df.low-df.gold.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1/n, adjust=False).mean()
def roc(s, n): return s.pct_change(n)*100
def corr(a, b, n): return a.rolling(n).corr(b)

def ols2(y, x1, x2, n):
    """rolling bivariate OLS betas via rolling covariances"""
    c11 = x1.rolling(n).var(); c22 = x2.rolling(n).var(); c12 = x1.rolling(n).cov(x2)
    cy1 = y.rolling(n).cov(x1); cy2 = y.rolling(n).cov(x2)
    det = c11*c22 - c12**2
    b1 = (cy1*c22 - cy2*c12)/det; b2 = (cy2*c11 - cy1*c12)/det
    return b1, b2

def score_model(df, P):
    g = df.gold
    rG = roc(g, 1)
    sRsi = rsi(g, P['rsiLen'])
    dF = (g - g.rolling(P['fastLen']).mean())/g.rolling(P['fastLen']).mean()*100
    dS = (g - g.rolling(P['slowLen']).mean())/g.rolling(P['slowLen']).mean()*100
    sFast = zscore(z(dF, P['normLen']), P['zCap']); sSlow = zscore(z(dS, P['normLen']), P['zCap'])
    a = atr(df, 14); aa = a.rolling(100).mean(); ratio = a/aa
    up = g >= g.ewm(span=20, adjust=False).mean()
    ve = np.clip((ratio-1)/(1.8-1), -1, 1)
    sVol = np.where(ve >= 0, np.where(up, 50+50*ve*0.6, 50-50*ve), 50 + 10*(-ve)*np.where(up, 1, -1))
    sVol = pd.Series(sVol, index=df.index)
    # ---- macro link ----
    rD = roc(df.dxy, 1); dY = df.y10.diff()*100   # bp
    bD, bY = ols2(rG, rD, dY, P['betaLen'])
    implied = bD*rD + bY*dY
    resid = rG - implied
    cumRes = resid.rolling(P['resLen']).sum()
    sRes = zscore(z(cumRes, P['normLen']), P['zCap'])
    tail = -(z(roc(df.dxy, P['resLen']), P['normLen']) + z(df.y10.diff(P['resLen']), P['normLen']))/2
    sTail = zscore(tail, P['zCap'])
    # ---- factor slots (DXY inv, 10Y inv, EUR dir, JPY inv, XAG dir) with corr weighting ----
    def factor(px, inverse, w, bp=False):
        chg = px.diff(20)*100 if bp else roc(px, 20)
        zz = z(chg, P['normLen']); r = corr(rG, roc(px,1), 60)
        e = 1.0 if not inverse else -1.0
        sc = zscore(zz, P['zCap']) if not inverse else 100 - zscore(zz, P['zCap'])
        wE = w*np.clip(e*r, 0, None)
        return sc, wE
    facs = [factor(df.dxy, True, 10), factor(df.y10, True, 10, bp=True), factor(df.eur, False, 5), factor(df.jpy, True, 5), factor(df.xag, False, 5)]
    comps = [(sRsi, P['wRsi']), (sFast, P['wFast']), (sSlow, P['wSlow']), (sVol, P['wVol']), (sRes, P['wRes']), (sTail, P['wTail'])] + facs
    num = sum(c.fillna(0)*w for c, w in comps); den = sum((~c.isna())*w for c, w in comps)
    raw = num/den.replace(0, np.nan)
    score = raw.ewm(span=P['smooth'], adjust=False).mean()
    return pd.DataFrame({'score': score, 'sRes': sRes, 'sTail': sTail, 'sRsi': sRsi, 'sFast': sFast, 'sSlow': sSlow, 'sVol': sVol,
                         'bD': bD, 'bY': bY, 'u': df.u, 'regime': df.regime, 'rG': rG, 'cumRes': cumRes, 'resid': resid})

def evaluate(df, out, H=24):
    s = out.score.dropna()
    fwd = np.log(df.gold.shift(-H)/df.gold)*100            # forward H-bar gold return %
    fwd_u = out.u.shift(-H) - out.u                          # forward change of macro residual level
    res = {}
    res['pct_fear'] = float((s < 25).mean()*100); res['pct_greed'] = float((s > 75).mean()*100)
    res['pct_caution'] = float(((s >= 25) & (s < 45)).mean()*100); res['pct_greedz'] = float(((s > 55) & (s <= 75)).mean()*100)
    res['std'] = float(s.std()); res['ac1'] = float(s.autocorr(1)); res['ac24'] = float(s.autocorr(24))
    # episodes
    ext = (s < 25) | (s > 75)
    runs = (ext != ext.shift()).cumsum(); lens = ext.groupby(runs).sum(); lens = lens[lens > 0]
    res['ext_episodes_per_1000'] = float(len(lens)/len(s)*1000); res['ext_mean_len'] = float(lens.mean()) if len(lens) else 0.0
    for name, mask in [('fear', s < 25), ('greed', s > 75), ('mid', (s >= 45) & (s <= 55))]:
        res[f'fwd{H}_{name}'] = float(fwd[mask.index][mask].mean()); res[f'fwdU{H}_{name}'] = float(fwd_u[mask.index][mask].mean())
    # macro link quality: corr of recovered beta with true beta, sRes vs true residual level u
    res['corr_bD_true'] = float(np.corrcoef(out.bD.dropna(), np.where(out.regime[out.bD.dropna().index]==0, -0.9, -0.25))[0,1])
    res['corr_sRes_u'] = float(out.sRes.corr(out.u))
    res['corr_sRes_fwdU'] = float(out.sRes.corr(fwd_u))
    return res

BASE = dict(rsiLen=14, fastLen=50, slowLen=200, normLen=250, zCap=2.0, betaLen=120, resLen=60, smooth=3,
            wRsi=30, wFast=15, wSlow=15, wVol=15, wRes=35, wTail=15)

def run(P, paths=12, n=12000):
    accs = []
    for i in range(paths):
        df = simulate_market(n, seed=1000+i)
        accs.append(evaluate(df, score_model(df, P)))
    return pd.DataFrame(accs).mean().to_dict()

if __name__ == '__main__':
    t0 = time.time()
    print('== base ==', json.dumps({k: round(v, 3) for k, v in run(BASE).items()}, indent=None))
    grid = {'zCap': [1.5, 2.0, 2.5], 'normLen': [120, 250, 500], 'betaLen': [60, 120, 250], 'resLen': [10, 20, 40]}
    rows = []
    for zc, nl, bl, rl in itertools.product(*grid.values()):
        P = dict(BASE, zCap=zc, normLen=nl, betaLen=bl, resLen=rl)
        r = run(P, paths=6, n=9000); r.update(zCap=zc, normLen=nl, betaLen=bl, resLen=rl); rows.append(r)
        print(f"zCap={zc} normLen={nl} betaLen={bl} resLen={rl} | ext%={r['pct_fear']+r['pct_greed']:.1f} std={r['std']:.1f} "
              f"bD~={r['corr_bD_true']:.2f} sRes~u={r['corr_sRes_u']:.2f} sRes~fwdU={r['corr_sRes_fwdU']:.2f} "
              f"fwdU fear={r['fwdU24_fear']:+.4f} greed={r['fwdU24_greed']:+.4f}", flush=True)
    G = pd.DataFrame(rows); G.to_csv('/home/user/Indikators/sim/grid_results.csv', index=False)
    # weight sweep for macro link
    for wRes, wTail in [(0,0),(15,10),(25,15),(35,20),(50,25)]:
        r = run(dict(BASE, wRes=wRes, wTail=wTail), paths=8, n=9000)
        print(f"wRes={wRes} wTail={wTail} | ext%={r['pct_fear']+r['pct_greed']:.1f} std={r['std']:.1f} fwdU24 fear={r['fwdU24_fear']:+.4f} greed={r['fwdU24_greed']:+.4f} fwd24 fear={r['fwd24_fear']:+.3f} greed={r['fwd24_greed']:+.3f}", flush=True)
    print('elapsed', round(time.time()-t0), 's')
