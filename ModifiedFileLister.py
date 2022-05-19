from pathlib import Path
from tkinter import filedialog
import tkinter as tk
import datetime
import os

TARGET_DURATION_DAYS = str(90)
EXCEPTION_PATH = "\\Lib\\"
MAX_DISP_ENTRY = str(500)
MAX_PATH_LENGTH = 130

SUFFIXS = {
    ".xlsx":True,
    ".xlsxm":True,
    ".pptx":True,
    ".docx":True,
    ".txt": False,
    ".py": False,
    ".c": False,
    ".h": False,
    ".map": False,
    ".elf": False,
    ".a2l": False,
    ".pdx": False,
    ".bin": False,
    ".cpp": False,
    ".slx": False,
    ".mdl": False,
    ".xml": False,
    ".arxml": False,
    ".html": False,
    ".htm": False,
    ".jpg": False,
    ".jpeg": False,
    ".gif": False,
    ".bmp": False,
    ".tiff": False,
    ".tif": False,
    ".exe": False,
    ".cfg": False,
    }

class FileLister():
    def __init__(self):
        self.root = None
        self.check = [None for i in range(len(SUFFIXS))]
        self.duration_in = None
        self.opt_suffix_in = None
        self.max_display = None
        self.exclude_path = None

        self.tksetup()

    def start(self) :
        self.root.mainloop()

    def tksetup(self) :
        self.root = tk.Tk()
        self.root.geometry('400x300')
        self.root.title('Modified File Lister')

        frame2 = tk.Frame(self.root, borderwidth = 2, relief = tk.SUNKEN)
        if frame2 :
            frame2_sub = tk.Frame(self.root, borderwidth = 2)
            if frame2_sub :
                for i, (k, v) in enumerate(SUFFIXS.items()):
                    self.check[i] = tk.BooleanVar(value=v)
                    checkbtn = tk.Checkbutton(frame2_sub,
                                variable = self.check[i],
                                text = k
                                )
                    if (i + 1) % 5 == 0 :
                        checkbtn.pack(anchor = tk.W)
                        frame2_sub.pack(anchor = tk.W)
                        frame2_sub = tk.Frame(self.root, borderwidth = 2)
                    else :
                        checkbtn.pack(fill = 'x', padx=5, side = 'left')
                        if i + 1 == len(SUFFIXS) :
                            frame2_sub.pack(anchor = tk.W)
            
        frame2.pack(fill = tk.X)

        frame1 = tk.Frame(self.root, borderwidth = 2)
        if frame1 :
            frame1_1 = tk.Frame(frame1, borderwidth = 2)

            if frame1_1 :
                label2 = tk.Label(frame1_1, text="Other filetypes")
                label2.pack(fill = 'x', padx=5, side = 'left')
                self.opt_suffix_in = tk.Entry(frame1_1,width=30)
                self.opt_suffix_in.pack(fill = 'x', padx=5, side = 'left')
            frame1_1.pack(fill = tk.X)

            frame1_1_1 = tk.Frame(frame1, borderwidth = 2)
            if frame1_1_1 :
                label2 = tk.Label(frame1_1_1, text="Exclude path")
                label2.pack(fill = 'x', padx=5, side = 'left')
                self.exclude_path = tk.Entry(frame1_1_1,width=30)
                self.exclude_path.pack(fill = 'x', padx=5, side = 'left')
                self.exclude_path.insert(0,EXCEPTION_PATH)
            frame1_1_1.pack(fill = tk.X)

            frame1_2 = tk.Frame(frame1, borderwidth = 2)
            if frame1_2 :
                label2 = tk.Label(frame1_2, text="Serch duration up to")
                label2.pack(fill = 'x', padx=5, side = 'left')
                self.duration_in = tk.Entry(frame1_2,width=10)
                self.duration_in.pack(fill = 'x', padx=5, side = 'left')
                self.duration_in.insert(0,TARGET_DURATION_DAYS)
                label2 = tk.Label(frame1_2, text="days before")
                label2.pack(fill = 'x', padx=5, side = 'left')
            frame1_2.pack(fill = tk.X)


            frame1_3 = tk.Frame(frame1, borderwidth = 2)
            if frame1_3 :
                label2 = tk.Label(frame1_3, text="Display ")
                label2.pack(fill = 'x', padx=5, side = 'left')
                self.max_display = tk.Entry(frame1_3,width=10)
                self.max_display.pack(fill = 'x', padx=5, side = 'left')
                self.max_display.insert(0,MAX_DISP_ENTRY)
                label2 = tk.Label(frame1_3, text=" items")
                label2.pack(fill = 'x', padx=5, side = 'left')
            frame1_3.pack(fill = tk.X)

        frame1.pack(fill = tk.X)

        btn = tk.Button(self.root, text='Start!', command=self.btn_click)
        btn.pack()
        

    def btn_click(self) :
        dc = {}
        folder_selected = filedialog.askdirectory()
        if not os.path.exists(folder_selected) :
            return False

        p = Path(folder_selected)
        current_time = datetime.datetime.now()

        # Get target file condition
        #   From check box
        target_list = []
        for i, (k,v) in zip(self.check, SUFFIXS.items()) :
            if i.get() :
                target_list.append(k.lower())
        print("Selected suffix: ",target_list)
        
        #   From entry box
        additional_tgt_list = []
        additional_tgt_list = [i.strip() for i in self.opt_suffix_in.get().split(',')]
        additional_tgt_list = [i.lower() for i in additional_tgt_list if len(i) > 0]
        print("Optional suffix: ",additional_tgt_list)
        
        final_tgt_tuple = tuple(target_list + additional_tgt_list)
        print("Total target suffix: ",final_tgt_tuple)

        # Get exception path condition
        exception_path_list = []
        exception_path_list = [i.strip() for i in self.exclude_path.get().split(',')]
        exception_path_list = [i.lower() for i in exception_path_list if len(i) > 0]
        exception_path_tuple = tuple(exception_path_list)
        print("Exception path: ",exception_path_tuple)

        # Get modified day condition
        target_duration_days = int(self.duration_in.get())

        # Run Search files
        for p_f in p.glob("**/*.*") :
            if len(str(p_f)) > MAX_PATH_LENGTH:
                continue

            if any(x in str(p_f).lower() for x in exception_path_tuple):
                continue
            
            if any(str(p_f).lower().endswith(x) for x in final_tgt_tuple):
                td = current_time - datetime.datetime.fromtimestamp(p_f.stat().st_mtime)
                if td.days < target_duration_days :

                    #add in dict. Key is modification date(epoc). Value is filePath
                    self.update_dict(dc, p_f.stat().st_mtime, str(p_f))

        # Sort from new to old
        dc_sorted = sorted(dc.items(), reverse=True)

        # Display result
        td_lastdays = -1
        for i, (t,v) in enumerate(dc_sorted) :
            if i > int(self.max_display.get()) :
                print("Break : ", self.max_display.get(), "items shown")
                break
            else :
                # Display days ago from now, if date is different from last entry.
                td = current_time - datetime.datetime.fromtimestamp(t)
                if td.days != td_lastdays :
                    td_lastdays = td.days
                    if td.days == 0 :
                        print("today")
                    else :
                        print(td.days, "days ago")
                
                # Dispay 1 entry
                print(" ",os.path.splitext(os.path.basename(v))[1][1]," ",datetime.datetime.fromtimestamp(t),(os.path.basename(v)).ljust(30),v)
        print("Finished : ",len(dc_sorted)," items")

    def update_dict(self, dict, key, value) :
        if key in dict :
            if value == dict[key]:
                # Skip, if same entry
                pass
            else :
                # Same date but diffent file path
                try :
                    # try to register with small date change (recursive up to 499)
                    self.update_dict(dict, key+0.000001, value) 
                except :
                    print("Too many files with same DateTime",key,value)
        else :
            # add in dict
            dict[key] = value

def main():
    fl = FileLister()
    fl.start()

if __name__ == "__main__" :
    main()

