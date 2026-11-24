"""Efectos de la ruleta (6.8 s): viento del barrido, whoosh por celda, braam, klaxon, vidrio hidraulico, cuello y gruñido.
uso: python3 nt/sfx_ruleta.py sfx.wav [segundo_del_twist_en_toma2=1.4]"""
import sys, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
SR = 48000; rng = np.random.default_rng(7)
def T(d): return np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=4): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=4): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def env(n, a, r, curve=3):
    e = np.ones(n); A = max(1, int(a * SR)); e[:A] = np.linspace(0, 1, A); e[A:] = np.linspace(1, 0, n - A) ** curve; return e
def saw(f, t): ph = np.cumsum(np.broadcast_to(f, t.shape)) / SR; return 2 * (ph % 1) - 1
def sine(f, t): return np.sin(2 * np.pi * np.cumsum(np.broadcast_to(f, t.shape)) / SR)
def norm(x, p=.9): m = np.abs(x).max(); return x / m * p if m else x
def reverb(x, secs=2.2, wet=.35, damp=4000):
    n = int(secs * SR); t = np.arange(n) / SR; out = []
    for ch in range(2):
        ir = rng.standard_normal(n) * np.exp(-t * 6.9 / secs); ir = lp(ir, damp, 2); ir[:int(.012 * SR)] *= np.linspace(0, 1, int(.012 * SR))
        out.append(fftconvolve(x, ir)[:len(x)] / np.sqrt(n) * 18)
    return np.stack([x, x], 1) * (1 - wet) + np.stack(out, 1) * wet
def drone(d):
    t = T(d); x = sum(saw(f, t) for f in (41.2, 41.5, 61.7, 82.1, 87.3)) * .2
    x = lp(x, 220) + lp(rng.standard_normal(len(t)), 120) * .5
    return x * (0.6 + .4 * np.sin(2 * np.pi * .13 * t)) * env(len(t), 1.0, 0, 0)
def braam(d=3.0):
    t = T(d); x = np.zeros(len(t))
    for f in (36.7, 55.0, 73.4, 110.0):
        for dt in (-.6, 0, .7): x += saw(f + dt, t)
    x = np.tanh(x * .5); x = lp(x, 900); x *= env(len(t), .02, 0, 2.2)
    sub = sine(np.linspace(85, 32, len(t)), t) * env(len(t), .005, 0, 1.5) * 1.6
    hit = lp(rng.standard_normal(len(t)), 2500) * env(len(t), .001, 0, 30) * 2
    return norm(x + sub + hit)
def hydraulic(d=1.0):
    t = T(d); n = rng.standard_normal(len(t)); x = np.zeros(len(t))
    for i, (lo, hi) in enumerate(zip(np.linspace(500, 2600, 12), np.linspace(900, 4200, 12))):
        a, b = i * len(t) // 12, (i + 1) * len(t) // 12; x[a:b] = bp(n, lo, hi)[a:b]
    x *= np.sin(np.linspace(0, np.pi, len(t))) ** .6
    return lp(saw(np.linspace(70, 95, len(t)), t) * .25, 400) + x * .8
def clunk():
    t = T(1.6); th = sine(np.linspace(90, 40, len(t)), t) * env(len(t), .002, 0, 6) * 1.4
    ring = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((221, 1), (563, .7), (1187, .5), (1931, .35), (2893, .2))) * env(len(t), .002, 0, 4) * .5
    return th + ring + bp(rng.standard_normal(len(t)), 300, 3000) * env(len(t), .001, 0, 40)
def growl(d=.5):
    t = T(d); f0 = 62 + 10 * np.sin(2 * np.pi * 7 * t)
    x = saw(f0, t) * (1 + .8 * np.sign(np.sin(2 * np.pi * 31 * t)))
    x = bp(np.tanh(x * 2.5), 120, 1400) + bp(rng.standard_normal(len(t)), 200, 900) * .6
    return x * env(len(t), .08, 0, 1.2)
def wind_pass(d, speed):
    n = int(d * SR); noise = lp(rng.standard_normal(n), 6000) + lp(rng.standard_normal(n), 400) * 2
    out = np.zeros(n); hop = int(.02 * SR)
    for i in range(0, n, hop):
        v = speed(i / SR); c = 250 + 2200 * v
        seg = bp(noise[max(0, i - 2048):i + hop], max(60, c * .45), c * 1.6, 2)[-min(hop, n - i):]
        out[i:i + len(seg)] = seg * (v ** 1.3)
    return out
def whoosh(d=.45):
    t = T(d); x = bp(rng.standard_normal(len(t)), 300, 2600, 2); return x * np.sin(np.pi * t / d) ** 2
def klaxon(d):
    t = T(d); ph = t % 1.1; on = ph < .75; bend = .82 + .18 * np.clip(ph / .09, 0, 1)
    x = sum(saw(f * bend, t) for f in (311, 370, 466)) + saw(155 * bend, t) * .8
    x = np.tanh(bp(x, 180, 3500) * 1.8)
    return x * np.where(on, np.clip(ph / .02, 0, 1) * np.clip((.75 - ph) / .05, 0, 1), 0)
def bone_crack():
    t = T(.18); x = np.zeros(len(t))
    for k in range(rng.integers(3, 6)):
        i = int(rng.uniform(0, .07) * SR); L = int(.012 * SR)
        x[i:i + L] += hp(rng.standard_normal(L), 1200) * np.exp(-np.arange(L) / (L / 5)) * rng.uniform(.5, 1)
    return x + bp(rng.standard_normal(len(t)), 150, 900) * env(len(t), .001, 0, 25) * .8
class Mix:
    def __init__(s, d): s.buf = np.zeros(int(d * SR))
    def add(s, x, at, gain=1.0):
        i = int(at * SR); x = x[:max(0, len(s.buf) - i)]; s.buf[i:i + len(x)] += x * gain
def ruleta(twist=1.4):
    d = 6.8; m = Mix(d); m.add(drone(d), 0, .35)
    spd = lambda tt: (1 - min(tt, 3.8) / 3.8) ** 2 if tt < 3.8 else 0
    m.add(wind_pass(3.9, spd), 0, 1.1)
    for i in range(-2, 9):
        p = (3.2 * i + 1.6 + 4.5) / 20.5
        if 0 <= p < 1:
            tt = (1 - (1 - p) ** (1 / 3)) * 3.8; m.add(whoosh(.35 + .4 * (1 - spd(tt))), max(0, tt - .15), .6 * spd(tt) ** .7)
    m.add(braam(3.0), 3.8, .9); m.add(klaxon(2.0), 4.8, .3)
    m.add(hydraulic(1.0), 4.8, .45); m.add(clunk(), 5.8, .6)
    for dt in (0, .35, .6, .8): m.add(bone_crack(), 3.8 + twist + dt, .9)
    m.add(growl(.6), 6.0, .45)
    x = reverb(m.buf, 2.8, .34); fade = np.ones(len(x)); n = int(.35 * SR); fade[-n:] = np.linspace(1, 0, n)
    return norm(x * fade[:, None], .95)
if __name__ == '__main__':
    out = ruleta(float(sys.argv[2]) if len(sys.argv) > 2 else 1.4)
    wavfile.write(sys.argv[1], SR, (out * 32767).astype(np.int16)); print(sys.argv[1])
