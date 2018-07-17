import athena as at
# LANG : Python 2.7
# FILE : test_athena.py
# AUTH : Sayan Bhattacharjee
# EMAIL: aero.sayan@gmail.com
# DATE : 16/JULY/2018            (Started Creation  )
# DATE : 12/JULY/2018            (Last Modified     )
# INFO : Test the athena library
if __name__ == "__main__":
    length = 1080 # length of the image in pixels
    width = 720 # width of the image in pixels
    dpi = 96 # dots per inch
    ath = at.Athena(length,width,dpi) # create athena object
    # Get data for a page
    page1 = [] # NOTE : 2D structure is required

    # Test 1: Euler's Identity
    #line1 = "t,$\mathtt{EULER'S-IDENTITY}$,a,center,s,40,c,#e85f04"
    #line2 = "t,$e^{i\pi} + 1 = 0$,a,center,s,27"

    # Test 2 : Navier Stoke's Equation
    line1 = "t,$\mathtt{NAVIER-STOKE'S-EQUATION}$,a,center,s,50,c,#90de1a"
    line2 = "t,$\\rho \\left[ \\frac{\delta \\vec u}{\delta t} + "\
    +"\\vec u . \\nabla \\vec u \\right] = - \\nabla p + \\nu \Delta \\vec u $,"+\
    "a,center,s,25"
    line3 = "t,$\\nabla . \\vec u = 0$,a,center,s,25"

    page1.append(line1) # NOTE : Creates a 2D structure which is required
    page1.append(line2)
    page1.append(line3)
    # Create a page using the data
    ath.create_page(page1)
    # Render the page
    ath.render_page_at(0,tofile=False)
    #ath.parse_command("t,$\mathtt{EULER'S-IDENTITY}$,a,center,s,40,c,red",echo=True)
