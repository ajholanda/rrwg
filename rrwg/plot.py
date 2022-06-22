"""Plotting procedure for the random reinforced walks.

"""
import matplotlib.pyplot as plt
import numpy as np

def gen_yset(rrwg, walk: int, vert: int):
    """Generate the y-values with the number of visits
    at each step.

    walk (int): walk index
    vert (int): vertex index

    """
    yset = []

    thewalk = rrwg.walks().get(walk)
    count = 0
    for idx, vloc in enumerate(thewalk.path()):
        count += 1
        if idx == 0:
            if vloc == vert:
                yset.append(1.0) # TODO: put the right start value
            else:
                yset.append(0.0) # TODO: put the right start value
            continue

        yset.append(yset[idx-1])
        if vloc == vert:
            yset[idx] += 1                

        yset[idx] /= count
            
    return yset

def plot(rrwg, title):
    """Plot the number of visits in the vertices per walk.

    """
    nwalks = rrwg.nwalks()
    nverts = rrwg.nvertices()
    # time steps
    xset = np.arange(rrwg.nsteps())
    #labels = ['$v_{}$'.format(vert) for vert in range(nverts)]

    fig, axs = plt.subplots(nwalks, sharex=True)
    fig.suptitle(title)

    for walk in range(nwalks):
        axs[walk].set_ylim([0.0, 1.0])
        axs[walk].set_ylabel('visits($w_{}$)'.format(walk))
        for vert in range(nverts):
            yset = gen_yset(rrwg, walk, vert)
            axs[walk].plot(xset, yset, label='$v_{}$'.format(vert))
        axs[walk].legend()
    plt.xlabel('t')
    plt.show()
