# LANG : Python 2.7
# FILE : test_athena.py
# AUTH : Sayan Bhattacharjee
# EMAIL: aero.sayan@gmail.com
# DATE : 16/JULY/2018            (Started Creation  )
# INFO : Test the athena library
import athena as at
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    length = 1080 # length of the image in pixels
    width  = 720 # width of the image in pixels
    dpi = 96.0 # dots per inch
    ath = at.Athena(length,width,dpi,fontsize=20) # create athena object
    # Get layout data
    lay = at.Layout()
    lay.add_gs(ath,[4,4])
    # Define the axes
    lay.add_axis(plt.subplot(lay.get_gs()[0][:,0:2]))
    lay.add_axis(plt.subplot(lay.get_gs()[0][0:2,2:4]))
    lay.add_axis(plt.subplot(lay.get_gs()[0][2:,2:4]))
    # Write stuff
    lay.add_rcmd(0,"t,$\\textcircled{c}{Sayan\ Bhattacharjee}$,a,center,s,25,c,#90de1a,x,0.5,y,0.7")
    lay.add_rcmd(0,"t,$\\mathtt{RSS\ -\ Residual\ Sum\ Of\ Squares}$,a,center,s,25,c,#90de1a,x,0.5,y,0.8")
    lay.add_rcmd(0,"t,$$RSS\ = \\sum_{i=1}^{N} {(y_i -f(x_i))^2}$$,a,center,s,22,x,0.5,y,0.4")
    # Plot stuff
    a = np.linspace(-10,10,100)
    lay.ax[1].plot(a,a**2)
    lay.ax[1].set_xlabel('X')
    lay.ax[1].set_ylabel('RSS')
    lay.ax[1].spines['bottom'].set_color('white')
    lay.ax[1].spines['top'].set_color('white')
    lay.ax[1].spines['left'].set_color('white')
    lay.ax[1].spines['right'].set_color('white')
    lay.ax[1].tick_params(axis='x',colors='white')
    lay.ax[1].tick_params(axis='y',colors='white')
    lay.ax[1].xaxis.label.set_color('white')
    lay.ax[1].yaxis.label.set_color('white')

    # Write some more stuff
    lay.add_rcmd(2,"t,$\\mathtt{ATHENA}$,x,0.5,y,0.9,a,center,c,#90de1a")
    lay.add_rcmd(2,"t,$\\mathtt{IS\ BATTLE\ READY}$,x,0.5,y,0.8,a,center,c,#90de1a")
    lay.add_rcmd(2,"t,\#10ZenDaysOfML is upon us,a,center,x,0.5,y,0.6")
    lay.add_rcmd(2,"t,$\\nabla$,a,center,x,0.5,y,0.4")
    lay.add_rcmd(2,"t,Follow me for more updates on,a,center,x,0.5,y,0.3")
    lay.add_rcmd(2,"t,www.linkedin.com/in/aerosayan,a,center,x,0.5,y,0.2")
    lay.add_rcmd(2,"t,www.twitter.com/aerosayan,a,center,x,0.5,y,0.1")


    # Create a page using the data
    ath.create_page_by_layout(lay.rcmd,lay.ax,"layout-test.png",numlines=17)
    # Render the page
    ath.render_page_at(0,renderlayout=True,tofile=True)
