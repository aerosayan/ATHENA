# LANG : Python 2.7
# FILE : athena.py
# AUTH : Sayan Bhattacharjee
# EMAIL: aero.sayan@gmail.com
# DATE : 16/JULY/2018            (Started Creation  )
# DATE : 17/JULY/2018            (Last Modified     )
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
        self.allign= [] # Allignment of the lines in 2D matrix form
        self.font_size = [] # Font size of the lines
        self.font_color = [] # Font color of the lines

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
        if len(self.lines) != len(self.allign):
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
        # Delete axes
        #fig.axes.get_xaxis().set_visible(False)
        #fig.axes.get_yaxis().set_visible(False)
        plt.axis('off')
        # Clear figure
        plt.gcf()
        print(len(self.lines))
        for i in xrange(len(self.lines)):
            # Render line
            self.render_line(i)
            # Update rendering position
            self.__update_ypos()
        # Call final draw call for this page
        self.__draw_call(athena.dpi,athena.bg_color,tofile)


    def render_line(self,line_num):
        """ Render one line after aligning it correctly and sizing it correctly
        @param line_num : the position of the line in self.lines to be printed
        """
        plt.text(self.xpos_curr,self.ypos_curr,self.lines[line_num],\
        fontsize=self.font_size[line_num],ha=self.allign[line_num],\
        color=self.font_color[line_num])


    def add_line(self,cmd):
        """ Add another string of text to the page
        @cmd : command for string to be rendered onto the string
        """
        self.lines.append(cmd[0][0]) # text
        self.allign.append(cmd[1][0]) # allignment
        self.font_size.append(cmd[2][0]) # font size
        self.font_color.append(cmd[3][0]) # font color



class Athena:
    """ The base class for creating educational video frames in LaTex format """
    def __init__(self,length,width,dpi,bgcolor='#011012',fontcolor='white'):
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
        self.font_size = 30.0
        #------------------------------------------------------
        # Parameters set by default
        #------------------------------------------------------
        self.font = None
        #------------------------------------------------------
        # The Athena core data structures
        #------------------------------------------------------
        self.pages = [] # NOTE : self.text will be an array of object of Page
    def parse_command(self,cmdstr,echo=False):
        """ Parse the commands given in the command string and return them
        @param cmdstr : comma delimited command string
        @info  cmdstr : "t,$\mathtt{EULER'S-IDENTITY}$,a,center,s,30,c,#1111"
        @info  t : text then the text to be printed
        @info  a : allignment then the allignment to be assigned
        @info  s : font size then the fontsize to be assigned
        @info  c : color then the color to be assigned (probably in hex)
        """
        # Split all the commands by comma
        cmds = cmdstr.split(',')

        # Prepare arrays for capturing
        arr_t = []
        arr_a = []
        arr_s = []
        arr_c = []

        # Set some flags for capturing
        cap_t = False     # Capture text
        cap_a = False     # Capture allignment
        cap_s = False     # Capture font size
        cap_c = False     # Capture color
        # Go through the text and find all data
        for c in cmds:
            if c == 't':
                cap_t = True
                continue
            elif c == 'a' :
                cap_a = True
                continue
            elif c == 's':
                cap_s = True
                continue
            elif c == 'c':
                cap_c = True
                continue
            elif cap_t == True:
                arr_t.append(c)
                cap_t = False
                continue
            elif cap_a == True:
                arr_a.append(c)
                cap_a = False
                continue
            elif cap_s == True:
                arr_s.append(float(c))
                cap_s = False
                continue
            elif cap_c == True:
                arr_c.append(c)
                cap_c = False
                continue
        # Ensure if data is not set by user then to set them to default values
        if arr_t == []:
            # If text is not found then show an error
            print("ERR : arr_t is [] : meaning no text is found...")
            print("ERR : Can not render without text")
            assert(False)
        if arr_a == []:
            # If allignment is empty then replace with default allignment
            arr_a.append("left")
        if arr_s == []:
            # If size is empty then replace with default size
            arr_s.append(self.font_size)
        if arr_c == []:
            # If color is empty then replace with default text color
            arr_c.append(self.font_color)

        if echo : print("DBG : Parsed commands"); print(arr_t,arr_a,arr_s,arr_c)
        return (arr_t,arr_a,arr_s,arr_c)




    def create_page(self,cmdstr):
        """ Create page and add to Athena
        @param cmdstr : comma delimited command string
        @info  cmdstr : "t,$\mathtt{EULER'S-IDENTITY}$,a,center,s,30,c,#1111"
        @info  t : text then the text to be printed
        @info  a : allignment then the allignment to be assigned
        @info  s : font size then the fontsize to be assigned
        @info  c : color then the color to be assigned (probably in hex)
        """
        # Create the page object
        page = Page()
        cmds = []
        # Iterate through every line command given parse it then add to page
        for c in cmdstr:
            cmds.append(self.parse_command(c,echo=True))
            page.add_line(cmds[-1])

        """
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
        """
        # Append the newly created page to self.pages
        self.pages.append(page)
        print(self.pages[-1])
        print(self.pages[-1].lines)
        print(self.pages[-1].allign)



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
