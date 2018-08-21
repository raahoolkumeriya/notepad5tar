#---------------------------------------------------------------------
#					31 Oct 2017 02:21 PM
#					Rahul Kumeriya
#---------------------------------------------------------------------

from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import os


root = Tk()
root.title("NOTEpad5TAR")
#root.wm_iconbitmap('TrayIconEOO.ico')#changing the default icon
root.geometry('1200x600+150+200')


def callback():
	print('hello')
	pass

def new_file():
	root.title("Untitled*.*")
	global filename
	filename = None
	textPad.delete(1.0,END)

def open_file():
	global filename
	filename = tkinter.filedialog.askopenfilename(defaultextension=".txt",filetypes =[("All Files","*.*"),("Text Documents","*.txt")])
	if filename == "": # If no file chosen.
		filename = None # Absence of file.
	else:
		root.title(os.path.basename(filename) + " - notepad5tar") #
		#Returning the basename of 'file'
		textPad.delete(1.0,END)
		fh = open(filename,"r")
		textPad.insert(1.0,fh.read())
		fh.close()

def save():
	global filename
	try:
		f = open(filename, 'w')
		letter = textPad.get(1.0, 'end')
		f.write(letter)
		f.close()
	except:
		save_as()
		
#Defining save_as method
def save_as():
	try:
		# Getting a filename to save the file.
		f = tkinter.filedialog.asksaveasfilename(initialfile ='Untitled.txt', defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
		fh = open(f, 'w')
		textoutput = textPad.get(1.0, END)
		fh.write(textoutput)
		fh.close()
		root.title(os.path.basename(f) + " - pyPad")
	except:
		pass

def exit_editor(event=None):
	if tkinter.messagebox.askokcancel("Quit", "Do you really want to quit?"):
		root.destroy()
	def exit_command():
		root.destroy()
		
	root.protocol('WM_DELETE_WINDOW', exit_command) # override close
		

def cut():
	textPad.event_generate("<<Cut>>")
	
def copy():
	textPad.event_generate("<<Copy>>")

def paste():
	textPad.event_generate("<<Paste>>")
	
def undo():
	textPad.event_generate("<<Undo>>")
	
def redo():
	textPad.event_generate("<<Redo>>")

def select_all():
	textPad.tag_add('sel', '1.0', 'end')
		
def on_find():
	t2 = Toplevel(root)
	t2.title('Find')
	t2.geometry('262x65+200+250')
	
	t2.transient(root)
	Label(t2, text="Find All:").grid(row=0, column=0, sticky='e')
	v=StringVar()
	e = Entry(t2, width=25, textvariable=v)
	e.grid(row=0, column=1, padx=2, pady=2, sticky='we')
	e.focus_set()
	c=IntVar()
	Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1,column=1, sticky='e', padx=2, pady=2)
	Button(t2, text="Find All", underline=0, command=lambda:search_for(v.get(), c.get(), textPad, t2, e)).grid(row=0,column=2, sticky='e'+'w', padx=2, pady=2)
	
	def close_search():
		textPad.tag_remove('match', '1.0', END)
		t2.destroy()

	t2.protocol('WM_DELETE_WINDOW', close_search)#override close

def search_for(needle, cssnstv, textPad, t2, e) :
	textPad.tag_remove('match', '1.0', END)
	count =0
	if needle:
		pos = '1.0'
		while True:
			pos = textPad.search(needle, pos, nocase=cssnstv,stopindex=END)
			if not pos: break
		lastpos = '%s+%dc' % (pos, len(needle))
		textPad.tag_add('match', pos, lastpos)
		count += 1
		pos = lastpos
		textPad.tag_config('match', foreground='red',background='yellow')
	e.focus_set()
	t2.title('%d matches found' %count)
	
def about(event=None):
	tkinter.messagebox.showinfo("About","Author: Rahul Kumeriya \n\nContact: rahul.kumeriya@gmail.com \n\nMob: +91 9766 9696 22")
def help_box(event=None):
	tkinter.messagebox.showinfo("Help","For help refer to book:\n\nConatct : Rahul Kumeriya ")#  ,icon='question')

	#LINE NO UPDATE
def update_line_number(event=None):
	txt = ''
	if showln.get():
		endline, endcolumn = textPad.index('end-1c').split('.')
		txt = '\n'.join(map(str, range(1, int(endline))))
		lnlabel.config(text=txt, anchor='nw')
		currline, curcolumn = textPad.index("insert").split('.')
		infobar.config(text= 'Line: %s | Column: %s' %(currline,curcolumn))
		
def show_info_bar():
	val = showinbar.get()
	if val:
		infobar.pack(expand=NO, fill=None, side=RIGHT,anchor='se')
	elif not val:
		infobar.pack_forget()


#line highlighting
def highlight_line(interval=100):
	textPad.tag_remove("active_line", 1.0, "end")
	textPad.tag_add("active_line", "insert linestart", "insert lineend+1c")
	textPad.after(interval, toggle_highlight)

def undo_highlight():
	textPad.tag_remove("active_line", 1.0, "end")

def toggle_highlight(event=None):
	val = hltln.get()
	undo_highlight() if not val else highlight_line()

#ADDING MENU BUTTON TO WIDGET

menubar = Menu(root)

#FILE
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="NEW", underline=0, accelerator='Ctrl+N', command=new_file)
update_line_number
filemenu.add_command(label="OPEN", underline=0, accelerator='Ctrl+O', command=open_file)
update_line_number
filemenu.add_command(label="SAVE", accelerator='Ctrl+S',command=save)
update_line_number
filemenu.add_command(label="SAVE AS", accelerator='Shift+Ctrl+S',command=save_as)
update_line_number
filemenu.add_command(label="EXIT", accelerator='Alt+F4',command=exit_editor)
menubar.add_cascade(label="FILE", menu=filemenu)

#EDIT
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="UNDO", accelerator='Ctrl + Z',compound=LEFT, command=undo)
editmenu.add_command(label="REDO", accelerator='Ctrl + Y',compound=LEFT, command=redo)
editmenu.add_separator()
editmenu.add_command(label="CUT",  accelerator='Ctrl + X',compound=LEFT,command=cut)
editmenu.add_command(label="COPY",  accelerator='Ctrl + C',compound=LEFT,command=copy)
editmenu.add_command(label="PASTE",  accelerator='Ctrl + V',compound=LEFT,command=paste)
editmenu.add_separator()
editmenu.add_command(label="FIND ALL",  accelerator='Ctrl + F',compound=LEFT, command=on_find)
editmenu.add_separator()
editmenu.add_command(label="SELECT ALL",  accelerator='Ctrl + A',underline=6,compound=LEFT,  command=select_all)
menubar.add_cascade(label="EDIT", menu=editmenu)


#VIEW
viewmenu = Menu(menubar, tearoff=0)
showln = IntVar()
showln.set(1)
viewmenu.add_checkbutton(label="SHOW LINE NUMBER",variable=showln)
update_line_number
viewmenu.add_checkbutton(label="SHOW INFO BAR AT BOTTOM", command=show_info_bar)

hltln = IntVar()
viewmenu.add_checkbutton(label="HIGHLIGHT CURRENT LINE",onvalue=1, offvalue=0, variable=hltln, command=toggle_highlight)

clrschms = {
	'1. Default White': '000000.FFFFFF',
	'2. Greygarious Grey': '83406A.D1D4D1',
	'3. Lovely Lavender': '202B4B.E1E1FF' ,
	'4. Aquamarine': '5B8340.D1E7E0',
	'5. Bold Beige': '4B4620.FFF0E1',
	'6. Cobalt Blue': 'ffffBB.3333aa',
	'7. Olive Green': 'D1E7E0.5B8340',
	}

def theme():
	global bgc,fgc
	val = themechoice.get()
	clrs = clrschms.get(val)
	fgc, bgc = clrs.split('.')
	fgc, bgc = '#'+fgc, '#'+bgc
	textPad.config(bg=bgc, fg=fgc)
	
themechoice= StringVar()
themechoice.set('1. Default White')
themesmenu=Menu(menubar, tearoff=0)
viewmenu.add_cascade(label="THEMES", menu=themesmenu)
for k in sorted(clrschms):
	themesmenu.add_radiobutton(label=k, variable=themechoice,command=theme)

menubar.add_cascade(label="VIEW", menu=viewmenu)


#ABOUT
aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label="ABOUT", command=about)
aboutmenu.add_command(label="HELP", command=help_box)
menubar.add_cascade(label="ABOUT", menu=aboutmenu)

#
shortcutbar = Frame(root, height=30, bg='DarkGray')
#CREATING ICON TOOLBAR
icons = ['new_file', 'open_file', 'save', 'cut', 'copy', 'paste', 'undo', 'redo', 'on_find', 'about']
for i, icon in enumerate(icons):
	tbicon = PhotoImage(file='icons/'+icon+'.gif')  
	cmd = eval(icon)
	toolbar = Button(shortcutbar, image=tbicon, command=cmd) 
	toolbar.image = tbicon
	toolbar.pack(side=LEFT)
shortcutbar.pack(expand=NO, fill=X)
lnlabel = Label(root, width=4, bg = 'BlanchedAlmond')
lnlabel.pack(side=LEFT, anchor='nw', fill=Y)


# ADDING TEXT PAD
textPad = Text(root, undo=True)
textPad.pack(expand=YES, fill=BOTH)
scroll=Scrollbar(textPad)
textPad.configure(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)
textPad.bind("<Any-KeyPress>", update_line_number)
textPad.tag_configure("active_line", background="ivory2")



#EVENT T ADD FOR SHORTCUTS
event=None
textPad.bind('<Control-N>', new_file)
textPad.bind('<Control-n>', new_file)
textPad.bind('<Control-O>', open_file)
textPad.bind('<Control-o>', open_file)
textPad.bind('<Control-S>', save)
textPad.bind('<Control-s>', save)
textPad.bind('<Control-A>', select_all)
textPad.bind('<Control-a>', select_all)
textPad.bind('<Control-f>', on_find)
textPad.bind('<Control-F>', on_find)
textPad.bind('<KeyPress-F1>', help_box)
textPad.bind (event, lambda e: callback())

#FOR POPUP MENU
cmenu = Menu(textPad)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
	cmd = eval(i)
	cmenu.add_command(label=i, compound=LEFT, command=cmd)
cmenu.add_separator()
cmenu.add_command(label='Select All', underline=7, command=select_all)

def popup(event):
	cmenu.tk_popup(event.x_root, event.y_root, 0)

textPad.bind("<Button-3>", popup)

root.iconbitmap('icons/about.gif')

#INFO BAR AT BOTTAM
infobar = Label(textPad, text='Line: 1 | Column: 0')
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
root.config(menu=menubar)


root.mainloop()