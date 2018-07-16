import athena as at
# LANG : Python 2.7
# FILE : test_athena.py
# AUTH : Sayan Bhattacharjee
# EMAIL: aero.sayan@gmail.com
# DATE : 16/JULY/2018            (Started Creation  )
# DATE : 00/XXXX/XXXX            (Finished Creation )
# DATE : 16/JULY/2018            (Last Modified     )
# INFO : Test the athena library
if __name__ == "__main__":
    length = 1080 # length of the image in pixels
    width = 720 # width of the image in pixels
    dpi = 96 # dots per inch
    ath = at.Athena(length,width,dpi) # create athena object
    # Get data for a page
    page1 = [] # NOTE : 2D structure is required
    line1 = ["$\mathtt{EULER'S-IDENTITY}$","center"]
    line2 = ["$e^{i\pi} + 1 = 0$","center"] # Store both the line text and allignment
    page1.append(line1) # NOTE : Creates a 2D structure which is required
    page1.append(line2)
    # Create a page using the data
    ath.create_page(page1)
    # Render the page
    ath.render_page_at(0,tofile=True)
