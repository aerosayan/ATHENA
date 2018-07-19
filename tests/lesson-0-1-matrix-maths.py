import athena as at
# WARNING : SHOULD BE MOVED TO WHERE ATHENA IS FOR IT TO WORK
# LANG : Python 2.7
# FILE : test_athena.py
# AUTH : Sayan Bhattacharjee
# EMAIL: aero.sayan@gmail.com
# DATE : 17/JULY/2018            (Started Creation  )
# INFO : Test the athena library
if __name__ == "__main__":
    n = 1
    length = 1080*2*n # length of the image in pixels
    width  = 720*4*n # width of the image in pixels
    dpi = 199.0 # dots per inch
    ath = at.Athena(length,width,dpi,fontsize=18) # create athena object
    # Get data for a page
    page1 = []

    # Information added to the page
    # Header
    page1.append("t,$\\mathtt{MATRIX\ \ MATHEMATICS\ CHEAT\ SHEET\ VERSION-1 }$,"\
    +"a,center,x,0.5,s,22,c,#90de1a")
    page1.append("t,$\\mathtt{10\ ZEN\ DAYS\ OF\ MACHINE\ LEARNING}$,"\
    +"a,center,x,0.5,c,#90de1a")
    page1.append("t,$\\textcircled{c}{Sayan\ Bhattacharjee}$,"\
    +"a,center,x,0.5")
    # Add a blank line
    #page1.append("t, ")
    #page1.append("t, ")
    page1.append("t,$\\mathtt{MATRIX\  ORIENTATION}$,a,center,c,#90de1a")

    page1.append("t,All matrices are set to be made of column vectors,a,center")
    #page1.append("t, ")
    page1.append("t,$X = \\begin{bmatrix} x_1 \\\ x_2 \\end{bmatrix}"\
    +"; X^{T} = \\begin{bmatrix} x_1 & x_2 \\end{bmatrix}$,a,center")



    page1.append("t,$\\mathtt{MATRIX\ ADDITION\ \&\ SUBTRACTION}$,a,center"\
    +",c,#90de1a")
    #page1.append("t, ")
    page1.append("t,$\\begin{bmatrix} x_{11} & x_{12} \\\ x_{21} & x_{22}"\
    +"\\end{bmatrix} \pm \\begin{bmatrix} y_{11} & y_{12} \\\  y_{21} & y_{22} \\end{bmatrix}"\
    +" = \\begin{bmatrix} x_{11} \pm y_{11} & x_{12} \pm y_{12} \\\ x_{21} \pm y_{21} & x_{22} \pm y_{22}"\
    +"\\end{bmatrix}$,a,center")
    page1.append("t, ")
    page1.append("t,$\\mathtt{MATRIX\ MULTIPLICATION}$,a,center"\
    +",c,#90de1a")
    #page1.append("t, ")

    page1.append("t,$X.Y = X^{T}.Y = \\begin{bmatrix} x_1 & x_2\\end{bmatrix}"\
    +".\\begin{bmatrix} y_1 \\\ y_2  \\end{bmatrix} = "\
    +" x_1.y_1 + x_2.y_2 $,a,center")
    page1.append("t, ")
    page1.append("t,$X \\otimes Y = X.Y^{T} = "\
    +"\\begin{bmatrix} x_1 \\\ x_2 \\\ x_3 \\end{bmatrix} \\begin{bmatrix} y_1 & y_2 & y_3\\end{bmatrix}"\
    +" = \\begin{bmatrix} "\
    +"x_1y_1 & x_1y_2 & x_1y_3 \\\ " \
    +"x_2y_1 & x_2y_2 & x_2y_3 \\\ " \
    +"x_3y_1 & x_3y_2 & x_3y_3 \\\ " \
    +"\\end{bmatrix}$,a,center")


    # Footer
    page1.append("t,$Follow\ me\ for\ more\ updates on...$,"\
    +"a,center,x,0.5,y,0.15")
    page1.append("t,$www.linkedin.com/in/aerosayan$,"\
    +"a,center,x,0.5,c")
    page1.append("t,$www.twitter.com/aerosayan$,"\
    +"a,center,x,0.5,c")

    # Create a page using the data
    ath.create_page(page1,"pic-lesson-0-1-matrix-maths.png",numlines=15*n)
    # Render the page
    ath.render_page_at(0,tofile=True)
