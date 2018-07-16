# LANG : Python 2.7
# FILE : athena.py
# AUTH : Sayan Bhattacharjee
# EMAIL: aero.sayan@gmail.com
# DATE : 16/JULY/2018            (Started Creation  )
# DATE : 00/XXXX/XXXX            (Finished Creation )
# DATE : 16/JULY/2018            (Last Modified     )
# INFO : Athena - Library for creating educational video frames in LaTex format
from __future__ import print_function
import matplotlib.pyplot as plt

class Page:
    """ Defines the different pages rendered by Athena """
    def __init__(self):
        """ Constructor """
        #------------------------------------------------------
        # Parameters set by default
        #------------------------------------------------------
        # Starting position of text renderer
        self.xpos_start = 0.5 # TODO : allow control
        self.ypos_start = 0.6 # TODO : allow control
        # Line Spacing of the text
        # formula (1.0 - 2.0*0.1 )/5.0  should produce 5 lines per page
        self.line_spacing = (1.0 - 2.0*0.1 )/5.0
        #------------------------------------------------------
        # Parameters updated during runtime
        #------------------------------------------------------
        # Current position of text renderer
        self.xpos_curr = self.xpos_start
        self.ypos_curr = self.ypos_start
        #------------------------------------------------------
        # The Athena core data structure
        #------------------------------------------------------
        self.lines = [] # Lines to be rendered in 2D matrix form
        self.allignment = [] # Allignment of the lines in 2D matrix form

    def __draw_call(self,toFile=False):
        """ The final draw call that will render the page
        @param toFile : if true then print to file else render on screen
        """
        plt.draw()
        plt.show()

    def __update_ypos(self,returnCount = 1,dy=None):
        """ Update the y positon of the renderer
        @param returnCount : number of new-line characters rendered
        @param dy : the change in the y axis (+ve dy creates line downwards)
        """
        if dy == None:
            dy = -self.line_spacing
        else :
            dy *= -1.0

        self.ypos_curr += dy*float(returnCount)

    def render_page(self,toFile=False):
        """ Render the full page
        @param toFile : if true then print to file else render on screen
        """
        # Sanity check
        if len(self.lines) != len(self.allignment):
            print("ERR : Page can not be rendered...")
            print("ERR : No. of lines and allignment mismatch...")
            assert(False)
        # Create renderer
        fig = plt.figure(facecolor='black')
        # Set the color parameters TODO : make it controllable
        plt.rcParams['figure.facecolor'] = 'black'
        plt.rcParams['axes.facecolor'] = 'black'
        plt.rcParams['text.color'] = 'white'
        # Clear figure
        plt.gcf()
        for i in xrange(len(self.lines)):
            # Render line
            self.render_line(i)
            # Update rendering position
            self.__update_ypos()

        self.__draw_call(toFile)





    def render_line(self,line_num):
        """ Render one line
        @param line_num : the position of the line in self.lines to be printed
        """
        plt.text(self.xpos_curr,self.ypos_curr,self.lines[line_num],fontsize=30,ha='center',va='center')

    def add_line(self,line,allign='left'):
        """ Add another string of text to the page
        @line : string to be added to the page and later to be rendered
        """
        self.lines.append(line)
        self.allignment.append(allign)



class Athena:
    """ The base class for creating educational video frames in LaTex format """
    def __init__(self,length,width,bg_color='black',font_color='white'):
        """ Constructor
        @param length : the length in pixels of the image to be rendered
        @param width : the width in pixels of the image to be rendered
        @param bg_color : default= 'black' : the background color
        @param font_color : default= 'white' : the font color
        """
        #------------------------------------------------------
        # Parameters set by the user
        #------------------------------------------------------
        self.length = length
        self.width = width
        self.bg_color = bg_color
        self.font_color = font_color
        #------------------------------------------------------
        # Parameters set by default
        #------------------------------------------------------
        self.font = None
        #------------------------------------------------------
        # The Athena core data structures
        #------------------------------------------------------
        self.pages = [] # NOTE : self.text will be an array of object of Page

    def create_page(self,lines_alligned):
        """ Create page and add to Athena
        @param lines_alligned : get both the line and the allignment data
        @info  lines_alligned = [["hello"],["world","left"]]
        """
        # Create the page object
        page = Page()
        # Iterate through every line given
        for i in xrange(len(lines_alligned)):
            if len(lines_alligned[i]) == 1 :
                # If only a single line is given then use the default allignment
                page.add_line(lines_alligned[i][0])
            elif len(lines_alligned[i]) == 2:
                # We have both line data and allignment data
                page.add_line(lines_alligned[i][0],allign=lines_alligned[i][1])
            else:
                print("ERR : lines_alligned size error...")
                assert(False)

        # Append the newly created page to self.pages
        self.pages.append(page)
        print(self.pages[-1])
        print(self.pages[-1].lines)
        print(self.pages[-1].allignment)




    def add_pages(self,pages):
        """ Add pages in Athena
        @param pages : an object or array of objects of the page class
        """
        self.pages.append(pages)
    def render_page_at(self,n):
        """ Render page at position given position
        @param n : the position of the page to be rendered
        """
        self.pages[n].render_page()

    def render(self,toFile=False):
        """ Render every page to either screen or file
        @param toFile : if true render to file else to screen
        """
        pass
