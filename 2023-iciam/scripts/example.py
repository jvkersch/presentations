import matplotlib.pyplot as plt
import numpy as np

def euler(f, h, x):
    """Take one step with the euler method."""
    return x + h*f(x)

def stormer_verlet(f, h, x):
    """Take one step with the SV method."""
    q, p = x
    p_prime = p + h/2 * f([q, p])[1]
    q_next = q + h*p_prime
    p_next = p_prime + h/2 * f([q_next, p_prime])[1]
    return np.array([q_next, p_next])


def run_integrator(one_step, f, x0, f_kwargs=None, h=0.1, tmax=10):
    ts = [0]
    xs = [x0]

    if f_kwargs:
        f = make_vector_field(f, **f_kwargs)
        
    while ts[-1] < tmax:
        x0 = one_step(f, h, x0)
        ts.append(ts[-1] + h)
        xs.append(x0)
    return np.asarray(ts), np.asarray(xs).T

def make_vector_field(f, **kwds):
    return lambda x: f(x, **kwds)

def f(x):
    q, p = x
    return np.array([p, -np.sin(q)])

def f_feedback(x, alpha, x0):
    q, p = x
    delta_h = hamiltonian(x) - hamiltonian(x0)
    return f(x) - alpha*delta_h*np.array([np.sin(q), p])

def hamiltonian(xs):
    q, p = xs
    return p**2/2 - np.cos(q)

def main():
    x0 = np.asarray([1., 0.])

    ts_euler, xs_euler = run_integrator(euler, f, x0, tmax=10, h=0.2)
    ts_sv , xs_sv = run_integrator(stormer_verlet, f, x0, tmax=10, h=0.2)
    ts_feedback, xs_feedback = run_integrator(euler, f_feedback, x0, tmax=10, h=0.2,
                                              f_kwargs={"alpha": 2, "x0": x0})
    
    fig, axes = plt.subplots(ncols=3, nrows=2)

    axes[0, 0].plot(xs_euler[0], xs_euler[1], 'o-')
    axes[0, 0].set_title("Forward Euler\n(1st order)")
    axes[0, 1].plot(xs_sv[0], xs_sv[1], 'o-')
    axes[0, 1].set_title("Stormer-Verlet\n(2nd order)")
    axes[0, 2].plot(xs_feedback[0], xs_feedback[1], 'o-')
    axes[0, 2].set_title("Feedback Euler\n(1st order)", fontweight="bold")

    axes[1, 0].plot(ts_euler, hamiltonian(xs_euler))
    axes[1, 1].plot(ts_sv, hamiltonian(xs_sv))
    axes[1, 2].plot(ts_feedback, hamiltonian(xs_feedback))

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
