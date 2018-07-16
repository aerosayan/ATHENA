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

    def __draw_call(self,dpi,bgcolor='black',tofile=False):
        """ The final draw call that will render the page
        @param toFile : if true then print to file else render on screen
        """
        if tofile :
            plt.savefig("testfig.png",facecolor=bgcolor,dpi=dpi)
        else:
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

    def render_page(self,athena,tofile=False):
        """ Render the full page
        @param toFile : if true then print to file else render on screen
        """
        # Sanity check
        if len(self.lines) != len(self.allignment):
            print("ERR : Page can not be rendered...")
            print("ERR : No. of lines and allignment mismatch...")
            assert(False)
        # Create renderer
        fig = plt.figure(facecolor=athena.bg_color ,\
        figsize=[athena.length/athena.dpi, athena.width/athena.dpi],\
        dpi = athena.dpi)
        # Set the color parameters TODO : make it controllable
        plt.rcParams['figure.figsize'] =[athena.length/athena.dpi, athena.width/athena.dpi]
        plt.rcParams['figure.facecolor'] = athena.bg_color
        plt.rcParams['axes.facecolor'] = athena.bg_color
        plt.rcParams['text.color'] = athena.font_color
        # Clear figure
        plt.gcf()
        for i in xrange(len(self.lines)):
            # Render line
            self.render_line(i,athena.font_size)
            # Update rendering position
            self.__update_ypos()
        # Call final draw call for this page
        self.__draw_call(athena.dpi,athena.bg_color,tofile)


    def render_line(self,line_num,fontsize):
        """ Render one line after aligning it correctly and sizing it correctly
        @param line_num : the position of the line in self.lines to be printed
        """
        plt.text(self.xpos_curr,self.ypos_curr,self.lines[line_num],\
        fontsize=fontsize,ha=self.allignment[line_num])

    def add_line(self,line,allign='left'):
        """ Add another string of text to the page
        @line : string to be added to the page and later to be rendered
        """
        self.lines.append(line)
        self.allignment.append(allign)



class Athena:
    """ The base class for creating educational video frames in LaTex format """
    def __init__(self,length,width,dpi,bgcolor='black',fontcolor='white'):
        """ Constructor
        @param length : the length in pixels of the image to be rendered
        @param width : the width in pixels of the image to be rendered
        @param dpi : dots per inch
        @param bg_color : default= 'black' : the background color
        @param font_color : default= 'white' : the font color
        """
        #------------------------------------------------------
        # Parameters set by the user
        #------------------------------------------------------
        # Length ,width and dpi of the rendered image
        self.length = length
        self.width = width
        self.dpi = dpi
        # Background color,font color and font size to use in the rendering
        self.bg_color = bgcolor
        self.font_color = fontcolor
        self.font_size = 30
        #------------------------------------------------------
        # Parameters set by default
        #------------------------------------------------------
        self.font = None
        #------------------------------------------------------
        # The Athena core data structures
        #------------------------------------------------------
        self.pages = [] # NOTE : self.text will be an array of object of Page

    def create_page(self,data):
        """ Create page and add to Athena
        @param data : get both the line and the allignment data
        @info  data = [["hello"],["world","left"]]
        """
        # Create the page object
        page = Page()
        # Iterate through every line given
        for i in xrange(len(data)):
            if len(data[i]) == 1 :
                # If only a single line is given then use the default allignment
                page.add_line(data[i][0])
            elif len(data[i]) == 2:
                # We have both line data and allignment data
                page.add_line(data[i][0],allign=data[i][1])
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
    def render_page_at(self,n,tofile=False):
        """ Render page at position given position
        @param n : the position of the page to be rendered
        """
        self.pages[n].render_page(self,tofile=tofile)

    def render(self,toFile=False):
        """ Render every page to either screen or file
        @param toFile : if true render to file else to screen
        """
        pass
