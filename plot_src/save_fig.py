#!/usr/bin/python -B

# Thank to Jessica B. Hamrick
# I copied this code from her github which is linked from her website at:
# http://www.jesshamrick.com/2012/09/03/saving-figures-from-pyplot/
import os
import sys

def save(user_plt, path, ext='png', close=True, verbose=True):
    """Save a figure from pyplot.

    Parameters
    ----------
    user_plt: matplotlib.pyplot
        The pyplot object so we can use it to draw our graph

    path : string
        The path (and filename, without the extension) to save the
        figure to.

    ext : string (default='png')
        The file extension. This must be supported by the active
        matplotlib backend (see matplotlib.backends module).  Most
        backends support 'png', 'pdf', 'ps', 'eps', and 'svg'.

    close : boolean (default=True)
        Whether to close the figure after saving.  If you want to save
        the figure multiple times (e.g., to multiple formats), you
        should NOT close it in between saves or you will have to
        re-plot it.

    verbose : boolean (default=True)
        Whether to print information about when and where the image
        has been saved.

    """

    # Extract the directory and filename from the given path
    directory = os.path.split(path)[0]
    filename = "%s.%s" % (os.path.split(path)[1], ext)
    if directory == '':
        directory = '.'

    # If the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # The final path to save to
    savepath = os.path.join(directory, filename)

    if verbose:
        sys.stderr.write("Saving figure to '%s'..." % savepath)

    # Actually save the figure
    user_plt.savefig(savepath)

    # Close it
    if close:
        user_plt.close()

    if verbose:
        sys.stderr.write("Done\n")
