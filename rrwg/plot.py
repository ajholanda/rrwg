"""Plotting procedure for the random reinforced walks.

"""
import matplotlib.pyplot as plt
import numpy as np

def gen_ysets(rrwg, walk: int, nverts: int, nsteps: int):
    """Generate the y-values with the number of visits
    at each step.

    walk (int): walk index
    nverts (int): number of vertices

    """
    # Save the normalized y-values, one per vertice for the specified
    # walk. The vertices are indexed by the column and the number of
    # steps are indexed by the row.
    ysets = np.full((nsteps, nverts), 0.0, dtype=float)

    thewalk = rrwg.walks().get(walk)
    count = 0
    for step, vert in enumerate(thewalk.path()):
        count += 1
        if step == 0:
            # Initialize the 0th step (t=0)
            # TODO: change: All init values for nvisits are 1
            ysets[step, :] = 1.0 # TODO: put the right start value
            continue

        # Repeat the values from the previous step
        ysets[step, :] = ysets[step-1, :]
        # Increment the value for the vertex where the walk step
        # through.
        ysets[step, vert] += 1

    print('\tw{}: ysets={}'.format(walk, ysets)) # TODO: remove this print()
    assert count == len(ysets)

    # Normalize the values
    for i in range(len(ysets)):
        ysets[i, :] /= np.sum(ysets[i, :])

    return ysets

def plot(rrwg, title):
    """Plot the number of visits in the vertices per walk.

    """
    nwalks = rrwg.nwalks()
    nverts = rrwg.nvertices()
    nsteps = rrwg.nsteps()
    # time steps
    xset = np.arange(nsteps)
    #labels = ['$v_{}$'.format(vert) for vert in range(nverts)]

    fig, axs = plt.subplots(nwalks, sharex=True)
    fig.suptitle(title)

    for walk in range(nwalks):
        axs[walk].set_ylim([0.0, 1.0])
        axs[walk].set_ylabel('visits($w_{}$)'.format(walk))
        # Count the visits in the walk and normalized them.
        ysets = gen_ysets(rrwg, walk, nverts, nsteps)
        for vert in range(nverts):
            axs[walk].plot(xset, ysets[:, vert],
                           label='$v_{}$'.format(vert))
        axs[walk].legend()
    plt.xlabel('t')
    plt.show()
