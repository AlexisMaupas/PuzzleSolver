from tkinter import *
from PIL import ImageTk, Image, ImageDraw
from tkinter import filedialog
import os


def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename
    
def open_puzzle():
    #x1 = openfn()
    x1= "puzzle.png"

    global puzzle
    puzzle = img = Image.open(x1)  

    #update default puzzle image
    img = img.resize((450,300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img


def open_piece():
    #y1 = openfn()
    y1= "puzzle2.png"

    global piece
    piece = img2 = Image.open(y1)  

    #update default puzzle image
    img2 = img2.resize((125,125), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)
    panel2.configure(image=img2)
    panel2.image = img2

def encadre_piece(x,y,l,h,color):
    

    line_size=3

    x1=x-line_size
    y1=y-line_size

    x2= x1+l+2*line_size-1
    y2= y1+h+2*line_size-1

    

    #upadte new puzzle img
    img = puzzle
    draw = ImageDraw.Draw(img) 
    draw.line((x1,y1, x2, y1), fill=color, width=5)
    draw.line((x2,y1, x2, y2), fill=color, width=5)
    draw.line((x1,y2, x2, y2), fill=color, width=5)
    draw.line((x1,y1, x1, y2), fill=color, width=5)

    #img.show()
   
    img = img.resize((450,300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img     


def verify_piece(initx,inity):
    pixpuzzle = puzzle.load()
    pixpiece = piece.load()

    (l1, h1) = piece.size
    #print("Piece Size : [{},{}] \n".format(l1,h1))


    for y in range(h1):
        for x in range(l1):
            #(r,g,b) = pixpiece[x,y]
            #(r1,g1,b1) = pixpuzzle[initx+x,inity+y]
            #print("R: {}, G: {}, B: {}".format(r,g,b))
            #print("R: {}, G: {}, B: {}".format(r1,g1,b1))

            #f r1+5<=r<=r1-5 or g1+5<=g<=g1-5 or b1+5<=b<=b1-5:
            #    return False 


            a = pixpiece[x,y]
            b = pixpuzzle[initx+x,inity+y]

            if a!=b:
               return False 

    return True            




def find_piece():
    if 'puzzle' in globals() and 'piece' in globals():
        #use to create a array of pixel
        pixpuzzle = puzzle.load()
        pixpiece = piece.load()

        (l, h) = puzzle.size
        (l1, h1) = piece.size

        #print("Puzzle Size : [{},{}] \n".format(l,h))
        


        for y in range(h):
            for x in range(l):
                a = pixpuzzle[x,y]
                b = pixpiece[0,0]

                #(r,g,b) = pixpiece[0,0]
                #(r1,g1,b1) = pixpuzzle[x,y]

                #if r-4<=r1<=r+4 and g-4<=g1<=g+4 and b-4<=b1<=b+4:
                if a == b:
                    text = "Position de la pièce : [{},{}]".format(x,y)
                    #encadre_piece(x,y,l1, h1, "yellow")      
                    #print(text)
                    if verify_piece(x,y):
                        status_text.configure(text=text)               
                        encadre_piece(x,y,l1, h1, "red")      
                        return 

     
        text = "Impossible de trouver la pièce!"
        print(text)
        status_text.configure(text=text)  
                            
    else:
        text="Vous n'avez pas sélectionné les deux images!"
        print(text)
        status_text.configure(text=text)



def show_puzzle():
    puzzle.show()

def save_puzzle():
    puzzle.save("Saves/puzzle.png", "png")


def compare():
    pixpuzzle = puzzle.load()
    pixpiece = piece.load()


    x = int(entry_X.get())
    y= int(entry_Y.get())

    x1 = int(entry_X1.get())
    y1= int(entry_Y1.get())

    r,g,b = pixpuzzle[x,y]

    r1,g1,b1 = pixpiece[x1,y1]

    colorpuzzle = '#%02x%02x%02x' % (r, g, b)

    colorpiece = '#%02x%02x%02x' % (r1, g1, b1)

    if(colorpuzzle==colorpiece):
        highlightcolor="green"
    else:
        highlightcolor="red"
    

    puzzlecolor.config(bg=colorpuzzle, highlightthickness=1, highlightbackground=highlightcolor)
    piececolor.config(bg=colorpiece, highlightthickness=1, highlightbackground=highlightcolor)

    encadre_piece(x,y,125,125,"blue")  



def mean_color():
    pixpuzzle = puzzle.load()

    rmean=0
    gmean=0
    bmean=0
    (l, h) = puzzle.size

    for y in range(h):
        for x in range(l):
            r,g,b = pixpuzzle[x,y]

            rmean +=r
            gmean +=g
            bmean +=b
    

    rmean= int(rmean /(l*h))
    gmean= int(gmean /(l*h))          
    bmean= int(bmean /(l*h))

    color = '#%02x%02x%02x' % (rmean, gmean, bmean)

    puzzle_meancolor.config(bg=color)
    entry_meanColor.delete(0, 'end')
    entry_meanColor.insert(0,color)


def find_color():

    searchcolor = entry_meanColor.get()
    puzzle_meancolor.config(bg=searchcolor)


    pixpuzzle = puzzle.load()
    (l, h) = puzzle.size

    howmany=0

    for y in range(h):
        for x in range(l):
            r,g,b = pixpuzzle[x,y]
            color = '#%02x%02x%02x' % (r, g, b)

            if(color==searchcolor):
                howmany+=1
                encadre_piece(x,y,1,1,"orange")
    

    print("Fréquence : {}/{}".format(howmany, l*h))






root = Tk()
root.title("Puzzle Solver")
root.geometry("800x550")
root.minsize(700,550)
root.iconbitmap("UI/logo.ico")
root.config(background="#4065A4")
root.resizable(width=True, height=True)


frame = Frame(root, bg='#4065A4')

#Image pour la pièce à trouver
piecebg = Image.open("UI/defaultbgpiece.png")
piecebg = piecebg.resize((125,125), Image.ANTIALIAS)
piecebg = ImageTk.PhotoImage(piecebg)
panel2 = Label(frame, image=piecebg)
panel2.image = piecebg
panel2.grid(row=0, column=0,  rowspan = 2, sticky=E+W, padx=26)

#Image pour le puzzle qui contient la pièce
puzzlebg = Image.open("UI/defaultbgpuzzle.png")
puzzlebg = puzzlebg.resize((450,300), Image.ANTIALIAS)
puzzlebg = ImageTk.PhotoImage(puzzlebg)
panel = Label(frame, image=puzzlebg)
panel.image = puzzlebg
panel.grid(row=3, column=0, columnspan = 3, rowspan=10, sticky=N+S, pady=10)

####### LEFT Part #######

#Boutons pour sélectionner les images
btnUploadPuzzle = Button(frame, text = "Select piece", font=('Helvetica', 20), bg='white', fg='#4065A4', command=open_piece)
btnUploadPuzzle.grid(row=0, column=1, sticky=E+W)

btnUploadPuzzle = Button(frame, text = "Select puzzle", font=('Helvetica', 20), bg='white', fg='#4065A4', command=open_puzzle)
btnUploadPuzzle.grid(row=0, column=2, sticky=E+W)

#Bouton pour trouver la pièce dans le puzzle
btnFind = Button(frame, text = "Find piece", font=('Helvetica', 20), bg='white', fg='#4065A4', command=find_piece)
btnFind.grid(row=1, column=1, columnspan = 2, sticky=E+W)

#Bouton pour show le puzzle
btnShow = Button(frame, text = "Show Puzzle", font=('Helvetica', 15), bg='white', fg='#4065A4', command=show_puzzle)
btnShow.grid(row=14, column=0, columnspan = 2, sticky=E+W)

#Bouton pour save l'image du puzzle
btnShow = Button(frame, text = "Save Puzzle", font=('Helvetica', 15), bg='white', fg='#4065A4', command=save_puzzle)
btnShow.grid(row=14, column=2,  sticky=E+W)


#Text status
status_text = Label(frame, text="Status Message", font=('Helvetica', 15), bg='#4065A4', fg='white')
status_text.grid(row=2, column=0, columnspan = 3, sticky=E+W)



####### Right Part #######

##Puzzle color
infopuzzle_text = Label(frame, text="Puzzle", font=('Helvetica', 15), bg='#4065A4', fg='white')
infopuzzle_text.grid(row=3, column=3, columnspan=2, sticky=W+E)

puzzlecolor = Canvas(frame,bg = "pink",height = "50", width="50")   
puzzlecolor.grid(row=4, column=3, columnspan=2, rowspan = 2) 

entry_X = Entry(frame, font=('Helvetica', 10), width=3,  bg='#4065A4', fg='white')
entry_X.insert(0, "0")
entry_X.grid(row=6, column=3,sticky=W+E)

entry_Y = Entry(frame, font=('Helvetica', 10), width=3,  bg='#4065A4', fg='white')
entry_Y.insert(0, "0")
entry_Y.grid(row=6, column=4,sticky=W+E)

##Piece color

infopiece_text = Label(frame, text="Piece", font=('Helvetica', 15), bg='#4065A4', fg='white')
infopiece_text.grid(row=3, column=5, columnspan=2, sticky=W+E)


piececolor = Canvas(frame,bg = "blue",height = "50", width="50")   
piececolor.grid(row=4, column=5, columnspan=2, rowspan = 2) 

entry_X1 = Entry(frame, font=('Helvetica', 10), width=3,   bg='#4065A4', fg='white')
entry_X1.insert(0, "0")
entry_X1.grid(row=6, column=5,sticky=W+E)

entry_Y1 = Entry(frame, font=('Helvetica', 10),  width=3,  bg='#4065A4', fg='white')
entry_Y1.insert(0, "0")
entry_Y1.grid(row=6, column=6,sticky=W+E)

#Bouton pour print la couleur
btnCompare = Button(frame, text = "Compare", font=('Helvetica', 12), bg='white', fg='#4065A4', command=compare)
btnCompare.grid(row=7, column=3, columnspan=4, sticky=W+E)



### Mean Color



puzzle_meancolor = Canvas(frame,bg = "black",height = "50", width="50")   
puzzle_meancolor.grid(row=8, column=4, columnspan=2, rowspan = 2) 

entry_meanColor = Entry(frame, font=('Helvetica', 10), width=3,  bg='#4065A4', fg='white')
entry_meanColor.insert(0, "#000")
entry_meanColor.grid(row=10, column=3,columnspan=4,sticky=W+E)

#Bouton obtenir la couleur moyenne
btnMeanColor = Button(frame, text = "Means", font=('Helvetica', 12), bg='white', fg='#4065A4', command=mean_color)
btnMeanColor.grid(row=11, column=3, columnspan=4, sticky=W+E)

#Bouton trouver la couleur
btnFindColor = Button(frame, text = "Find", font=('Helvetica', 12), bg='white', fg='#4065A4', command=find_color)
btnFindColor.grid(row=12, column=3, columnspan=4, sticky=W+E)




# show frame
frame.pack(expand=YES)

root.mainloop()


