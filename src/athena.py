# LANG : Python 2.7
# FILE : athena.py
# AUTH : Sayan Bhattacharjee
# EMAIL: aero.sayan@gmail.com
# DATE : 16/JULY/2018            (Started Creation  )
# DATE : 18/JULY/2018            (Last Modified     )
# INFO : Athena - Library for creating educational video frames in LaTex format
from __future__ import print_function
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


#------------------------------------------------------
# Markers for fast identification
#------------------------------------------------------
# Horizontal layout
LAYHOR = 0
# Vertical layout
LAYVER = 1

class Layout:
    """ Defines the different layouts rendered by Athena """
    def __init__(self):
        """ Constructor """
        #------------------------------------------------------
        # Parameters set by default
        #------------------------------------------------------
        # Grid spec layout
        self.gs = []
        # Grid spec axes
        self.ax = []
        # Lines to render and render commands
        self.rcmd = [[]]   # Essentially contains all the lines to be rendered
        # Matplotlib figure
        self.fig = None

    def get_gs(self):
        """ Return the grid spec for splicing
        """
        return self.gs

    def add_gs(self,athena,size):
        """ Create and add a new grid spec
        @param size : array containing size of grid in (n,m) form
        """
        # Create renderer
        self.fig = plt.figure(facecolor=athena.bg_color ,\
        figsize=[athena.length/athena.dpi, athena.width/athena.dpi],\
        dpi = athena.dpi)

        # Delete axes
        plt.axis('off')
        # Set the color parameters TODO : make it controllable
        plt.rcParams['figure.figsize'] =[athena.length/athena.dpi, athena.width/athena.dpi]
        plt.rcParams['figure.facecolor'] = athena.bg_color
        plt.rcParams['axes.facecolor'] = athena.bg_color
        plt.rcParams['text.color'] = athena.font_color
        params = {'text.latex.preamble' : [r'\usepackage{siunitx}', r'\usepackage{amsmath}']}
        #params = {'text.latex.preamble' : [ r'\usepackage{amsmath}']}
        plt.rcParams.update(params)


        # Latex rendering
        rc('text', usetex=True)
        rc('font', family='serif')

        # Clear figure
        plt.gcf()

        # Add the new gs
        self.gs.append(gridspec.GridSpec(size[0],size[1]))

    def add_axis(self,layoutrequest):
        """ Create the layout, and return the x and y positions
        @param layoutrequest : the requested splice of the grid spec
        @info  layoutrequest = lay.add_axis(lay.get_gridspec()[0][:,1])
        """
        self.ax.append(layoutrequest)
    def add_rcmd(self,n,cmd):
        """ Add render command at the position specified
        @param n : the row of self.rcmd in which the cmd is to be stored
        @info  n : the row number corresponds to the parent subplot position in self.ax
        @param cmd : the render command given : mostly will be lines with LaTex
        """
        # Sanity check
        if  len(self.ax) != len(self.rcmd) :
            # Make self.rcmd the same size a self.ax
            for i in xrange(len(self.ax)-1):
                self.rcmd.append(list())
        # else
        self.rcmd[n].append(cmd)


class Page:
    """ Defines the different pages rendered by Athena """
    def __init__(self,numlines=7):
        """ Constructor """
        #------------------------------------------------------
        # Parameters set by default
        #------------------------------------------------------
        # Starting position of text renderer
        self.xpos_start = 0.01 # TODO : allow control
        self.ypos_start = 0.9 # TODO : allow control
        self.num_lines = numlines
        # Line Spacing of the text
        # formula (1.0 - 2.0*0.1 )/5.0  should produce 5 lines per page
        self.line_spacing = (1.0 - 2.0*0.1 )/float(self.num_lines)
        #------------------------------------------------------
        # Parameters updated during runtime
        #------------------------------------------------------
        # Current position of text renderer
        self.xpos_curr = self.xpos_start
        self.ypos_curr = self.ypos_start
        #------------------------------------------------------
        # The Athena core data structure
        #------------------------------------------------------
        self.x = [] # x position
        self.y = [] # y position
        self.dx = [] # change in x position
        self.dy = [] # change in y position
        self.lines = [] # Lines to be rendered
        self.allign= [] # Allignment of the lines
        self.font_size = [] # Font size of the lines
        self.font_color = [] # Font color of the lines
        self.layout_axis = [] # The axis of plot produced in grid spec

    def __draw_call(self,dpi,saveas="testfig.png",bgcolor='black',tofile=False):
        """ The final draw call that will render the page
        @param toFile : if true then print to file else render on screen
        """
        # Ensure that extra padding is not given in the image and it is tight
        plt.tight_layout()
        # Render to either screen or file
        if tofile :
            plt.savefig(saveas,facecolor=bgcolor,dpi=dpi)
        else:
            plt.draw()
            plt.show()

    def __new_ypos(self,returncount = 1,getdy=False,dy=None):
        """ Update the y positon of the renderer
        @param returnCount : number of new-line characters rendered
        @param getdy : if true then return only the change in y position
        @param dy : the change in the y axis (+ve dy creates line downwards)
        """
        if dy == None:
            dy = -self.line_spacing
        else :
            dy *= -1.0

        if getdy : return dy*float(returncount)
        return self.ypos_curr + dy*float(returncount)

    def render_page(self,athena,n,renderlayout=False,tofile=False):
        """ Render the full page
        @param toFile : if true then print to file else render on screen
        """
        # Sanity check
        if len(self.lines) != len(self.allign):
            print("ERR : Page can not be rendered...")
            print("ERR : No. of lines and allignment mismatch...")
            assert(False)
        # Iterate through the lines and render
        print(len(self.lines))
        for i in xrange(len(self.lines)):
            # Render line
            if renderlayout == False:
                self.render_line(i)
            else:
                self.render_layout(i)

        # Call final draw call for this page
        self.__draw_call(athena.dpi,athena.pages_id[n],athena.bg_color,tofile)

    def render_layout(self,n):
        """ Render the full layout of the page , using the modern layout axis feature
        @param n : the positon of the line  to be printed
        """
        self.layout_axis[n].text(x=self.x[n],y=self.y[n],s=r"%s" % self.lines[n],\
        fontsize=self.font_size[n],ha=self.allign[n],color=self.font_color[n])

    def render_line(self,n):
        """ Render one line after aligning it correctly and sizing it correctly
        @param n : the position of the line in self.lines to be printed
        """
        prevx = self.xpos_curr
        prevy = self.ypos_curr

        if self.x[n] == -100: # if user did not set the values explicitly
            if n == 0:
                pass
            else:
                self.xpos_curr +=  float(self.dx[n])
        else:
            self.xpos_curr = float(self.x[n]) + float(self.dx[n])
        if self.y[n] == -100:
            if n == 0:
                pass
            else:
                self.ypos_curr += self.dy[n]
        else:
            self.ypos_curr = self.y[n] + self.dy[n]

        # Finally plot the stuff
        plt.text(self.xpos_curr,self.ypos_curr,r"%s"% self.lines[n],\
        fontsize=self.font_size[n],ha=self.allign[n],\
        color=self.font_color[n])


    def add_line(self,cmd,layoutaxis = None):
        """ Add another string of text to the page
        @cmd : command for string to be rendered onto the string
        @info : cmd :(arr_t,arr_a,arr_s,arr_c,arr_x,arr_y,arr_dx,arr_dy)
        """
        self.lines.append(cmd[0][0]) # text
        self.allign.append(cmd[1][0]) # allignment
        self.font_size.append(cmd[2][0]) # font size
        self.font_color.append(cmd[3][0]) # font color
        self.x.append(cmd[4][0]) # x position
        self.y.append(cmd[5][0]) # y position
        self.dx.append(cmd[6][0]) # change in x positon
        self.dy.append(cmd[7][0]) # change in y positon
        if layoutaxis : self.layout_axis.append(layoutaxis) # add the plot axis



class Athena:
    """ The base class for creating educational video frames in LaTex format """
    def __init__(self,length,width,dpi, bgcolor='#202020',
    fontcolor='white', fontsize=20.0):
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
        self.font_size = float(fontsize)
        #------------------------------------------------------
        # Parameters set by default
        #------------------------------------------------------
        self.font = None
        #------------------------------------------------------
        # The Athena core data structures
        #------------------------------------------------------
        self.pages = [] # NOTE : self.text will be an array of object of Page
        self.pages_id = []

    def parse_command(self,page,cmdstr,echo=False):
        """ Parse the commands given in the command string and return them
        @param page : object of the page class
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
        arr_x = []
        arr_y = []
        arr_dx = []
        arr_dy = []
        arr_b = []

        # Set some flags for capturing
        cap_t = False     # Capture text
        cap_a = False     # Capture allignment
        cap_s = False     # Capture font size
        cap_c = False     # Capture color
        cap_x = False     # Capture x co-ordinate
        cap_y = False     # Capture y co-ordinate
        cap_dx = False     # Capture change in x
        cap_dy = False     # Capture change in y
        cap_b = False    # Capture number of line breaks to produce

        # Go through the text and find all data
        for c in cmds:
            if c == 't':
                cap_t = True; continue
            elif c == 'a' :
                cap_a = True; continue
            elif c == 's':
                cap_s = True; continue
            elif c == 'c':
                cap_c = True; continue
            elif c == 'x':
                cap_x = True; continue
            elif c == 'y':
                cap_y = True; continue
            elif c == 'dx':
                cap_dx = True; continue
            elif c == 'dy':
                cap_dy = True; continue
            elif c == 'b':
                cap_b = True; continue
            elif cap_t == True:
                arr_t.append(c); cap_t = False; continue
            elif cap_a == True:
                arr_a.append(c); cap_a = False; continue
            elif cap_s == True:
                arr_s.append(float(c)); cap_s = False; continue
            elif cap_c == True:
                arr_c.append(c); cap_c = False; continue
            elif cap_x == True:
                arr_x.append(float(c)); cap_x = False; continue
            elif cap_y == True:
                arr_y.append(float(c)); cap_y = False; continue
            elif cap_dx == True:
                arr_dx.append(float(c)); cap_dx = False; continue
            elif cap_dy == True:
                arr_dy.append(float(c)); cap_dy = False; continue
            elif cap_b == True:
                arr_b.append(int(c)); cap_d = False; continue
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
        if arr_x == []:
            # If the x is empty then set to default value
            arr_x.append(-100)#page.xpos_start)
        if arr_y == []:
            # If the y is empty then set to default value
            arr_y.append(-100)#page.ypos_start)
        if arr_dx == []:
            # If the dx is empty then set to default value
            arr_dx.append(0.0)
        if arr_dy == []:
            # If the dy is empty then set to default value
            arr_dy.append( page._Page__new_ypos(getdy=True) )
        if arr_b == []:
            # If arr_b is empty then set to default value
            arr_b.append(1)

        if echo : print("DBG : Parsed commands"); print(arr_t,arr_a,arr_s,arr_c)
        return (arr_t,arr_a,arr_s,arr_c,arr_x,arr_y,arr_dx,arr_dy,arr_b)




    def create_page(self,cmdstr,pageid,numlines):
        """ Create page and add to Athena
        @param cmdstr : comma delimited command string
        @info  cmdstr : "t,$\mathtt{EULER'S-IDENTITY}$,a,center,s,30,c,#1111"
        @info  t : text then the text to be printed
        @info  a : allignment then the allignment to be assigned
        @info  s : font size then the fontsize to be assigned
        @info  c : color then the color to be assigned (probably in hex)
        @param pageid : Save the rendered page in this name
        """
        # Create the page object
        page = Page(numlines)
        cmds = []
        # Iterate through every line command given parse it then add to page
        for c in cmdstr:
            cmds.append(self.parse_command(page,c,echo=True))
            page.add_line(cmds[-1])

        # Append the newly created page to self.pages
        self.pages.append(page)
        self.pages_id.append(pageid)
    def create_page_by_layout(self,rcmd,layoutaxis,pageid,numlines):
        """ Create page from layout and add to Athena
        @param rcmd : render commands coming in from layout create_rcmd method
        """
        # Create page object
        page = Page()
        cmds = []
        # Iterate through the render commands and process them
        for i in xrange(len(rcmd)) : # for each axis correspondent array in rcmd
            # The subplot axis
            ax = rcmd[i]
            if ax == []:
                pass # Means we have no text in a particular subplot
            for c in ax: # for command in each axis correspondent array
                # else
                cmds.append(self.parse_command(page,c,echo=True))
                page.add_line(cmds[-1],layoutaxis=layoutaxis[i])
        # Append the newly created page to self.pages
        self.pages.append(page)
        self.pages_id.append(pageid)




    def add_pages(self,pages):
        """ Add pages in Athena
        @param pages : an object or array of objects of the page class
        """
        self.pages.append(pages)

    def render_page_at(self,n,renderlayout=False,tofile=False):
        """ Render page at position given position
        @param n : the position of the page to be rendered
        """
        self.pages[n].render_page(self,n,renderlayout=renderlayout,tofile=tofile)


    def render(self,toFile=False):
        """ Render every page to either screen or file
        @param toFile : if true render to file else to screen
        """
        pass
