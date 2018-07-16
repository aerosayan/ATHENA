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
    length = 1024 # length of the image in pixels
    width = 768 # width of the image in pixels
    ath = at.Athena(1024,768) # create athena object
    # Get data for a page
    page1 = [] # NOTE : 2D structure is required
    line1 = ["Hello"]
    line2 = ["World!","right"] # Store both the line text and allignment
    line3 = ["aero.sayan signing out..."]
    page1.append(line1) # NOTE : Creates a 2D structure which is required
    page1.append(line2)
    page1.append(line3)
    # Create a page using the data
    ath.create_page(page1)
    # Render the page
    ath.render_page_at(0)
