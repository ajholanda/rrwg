"""Handle data operations like writing to a file.

"""
from walk import Walk

class Data():
    def __init__(self, walks: list[Walk]):
        self._walks = walks
        self._fname = 'rrwg.dat'
        self._dataf = open(self._fname, 'w')
        for i, walk in enumerate(walks):
            for j in walk.vertices():
                self._dataf.write('\tw{}v{}'.format(i, j))
        self._dataf.write('\n')
        self.write()

    def __del__(self):
        if self._dataf:
            self._dataf.close()
        print('* Wrote {}'.format(self._fname))
        self.write_R()

    def write_R(self):
        fname = 'rrwg.R'
        thef = open(fname, 'w')
        cmds = 'df <- read.table("{}", header=TRUE)\n'.format(self._fname)
        cmds += 'df$t <- seq(1, nrow(df))\n'
        cmds += 'library(ggplot2);\nlibrary(grid)\n'

        grid = 'ggsave("rrwg.pdf", grid.draw(rbind('
        cmds += 'ggplot(df, aes(x=t))\n'
        for i, walk in enumerate(self._walks):
            cmds += 'p{} <- ggplot(df, aes(x = t)) + \n'.format(i)
            for count, j in enumerate(walk.vertices()):
                cmds += \
                    '\t geom_line(aes(y = w{}v{}, colour = "v{}")) + \n'\
                    .format(i, j, j)
            cmds += '\tylab("w{}")\n'.format(i)
            grid += 'ggplotGrob(p{}), '.format(i)
                
        thef.write(cmds)
        grid += 'size = "last")))\n'
        thef.write(grid)
        thef.close()
        print('* Wrote {}'.format(fname))
        
    def write(self):
        """Write the current data saved in walk list
        to the output file.

        """
        for walk in self._walks:
            for i in walk.vertices():
                self._dataf.write('\t{}'.format(walk.nvisits(i)))
        self._dataf.write('\n')
        self._dataf.flush()
