import tkinter as tk
import time
import os
from threading import Thread
import client_login
from client_login import send_words,send_hash, register_client,send_senstivity_list,request_classfication,move_qFile,request_qFiles,check_alert_for_button,ret_button_color,request_logs, send_rights_upload,request_upload_list,ret_upload_right_list,ret_rights_list,close_connection,make_none,ret_upload_right,check_upload_rights,request_check_rights,ret_access_file_list,ret_access_name_list,send_rights_download,ret_names_list,login_credentials_send_message,start_client,close_window_server,upload_file_client,request_file_explorer_for_rights,send_download_names,request_file_explorer,ret_file_list,request_userName
from tkinter import Label, filedialog,messagebox
from hash import calculate_txt_hash,calculate_hash
global push_button_5
stop_flag = False
admin=False
def login():
    start_client()
    files=[]

    def logout():
        global stop_flag
        stop_flag = True
        close_connection()
        root.destroy()
        login()
    def destroy_root():
        root.destroy()
    def check_alerts():
        global push_button_5
        global stop_flag,admin
        while not stop_flag:
            try:
                if admin:
                    img1_a = tk.PhotoImage(file="admin_window\\img1_a.png")
                    img1 = tk.PhotoImage(file="admin_window\\img1.png")
                    if ret_button_color()=="red":
                        push_button_5.config(image=img1_a)
                    elif ret_button_color()=="not_red":
                        push_button_5.config(image=img1)
            except:
                print("working on check_alerts()")
            time.sleep(2)
    def admin_window():
        global admin
        admin=True
        make_none()
        if not os.path.exists("captured_images"):
            os.makedirs("captured_images")
        for item in os.listdir("captured_images"):
            item_path = os.path.join("captured_images", item)
            if os.path.isfile(item_path):
                os.remove(item_path)
        global push_button_5

        window = tk.Toplevel(root)
        window.geometry("683x513")
        window.configure(bg="#bce4e2")
        canvas = tk.Canvas(
            window,
            bg="#bce4e2",
            height=513,
            width=683,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = tk.PhotoImage(file="admin_window\\background.png")
        tk.background = canvas.create_image(
            341.5, 248.50000000000003,
            image=background_img)

        label_2 = Label(window, text=entry_username.get(), font=("Arial", 14))
        label_2.place(x=534, y=68,width=136,height=31)
        img0 = tk.PhotoImage(file="admin_window\\img0.png")
        b0 = tk.Button(
            window,
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=logout,
            relief="flat",

        )
        b0.place(
            x=534.0, y=105.0,
            width=136,
            height=31)
        img1 = tk.PhotoImage(file="admin_window\\img1.png")
        push_button_5 = tk.Button(
            window,
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=show_alerts,
            relief="flat")
        push_button_5.place(
            x=54.0, y=177.0,
            width=102,
            height=40)
        check_alert_for_button(1)
        time.sleep(1)
        img2 = tk.PhotoImage(file="admin_window\\img2.png")
        b2 = tk.Button(
            window,
            image=img2,
            borderwidth=0,
            highlightthickness=0,
            command=log_box,
            relief="flat")
        b2.place(
            x=316.0, y=177.0,
            width=102,
            height=40)
        img3 = tk.PhotoImage(file="admin_window\\img3.png")
        b3 = tk.Button(
            window,
            image=img3,
            borderwidth=0,
            highlightthickness=0,
            command=show_qFiles,
            relief="flat")

        b3.place(
            x=432.0, y=177.0,
            width=197,
            height=40)
        img4 = tk.PhotoImage(file="admin_window\\img4.png")
        b4 = tk.Button(
            window,
            image=img4,
            borderwidth=0,
            highlightthickness=0,
            command=access_rights_download,
            relief="flat")

        b4.place(
            x=54.0, y=284.0,
            width=198,
            height=40)
        img5 = tk.PhotoImage(file="admin_window\\img5.png")
        b5 = tk.Button(
            window,
            image=img5,
            borderwidth=0,
            highlightthickness=0,
            command=access_rights_upload,
            relief="flat")

        b5.place(
            x=54.0, y=343.0,
            width=198,
            height=40)
        img6 = tk.PhotoImage(file="admin_window\\img6.png")
        b6 = tk.Button(
            window,
            image=img6,
            borderwidth=0,
            highlightthickness=0,
            command=upload_open_file_explorer,
            relief="flat")

        b6.place(
            x=477.0, y=283.0,
            width=170,
            height=40)
        img7 = tk.PhotoImage(file="admin_window\\img7.png")
        b7 = tk.Button(
            window,
            image=img7,
            borderwidth=0,
            highlightthickness=0,
            command=download_open_file_explorer,
            relief="flat")
        b7.place(
            x=477.0, y=344.0,
            width=182,
            height=40)

        img8 = tk.PhotoImage(file="admin_window\\img8.png")
        b8 = tk.Button(
            window,
            image=img8,
            borderwidth=0,
            highlightthickness=0,
            command=tab_view,
            relief="flat")

        b8.place(
            x=164.0, y=177.0,
            width=141,
            height=40)
        img9 = tk.PhotoImage(file="admin_window\\img9.png")
        b9 = tk.Button(
            window,
            image=img9,
            borderwidth=0,
            highlightthickness=0,
            command=reg_user,
            relief="flat")
        b9.place(
            x=10, y=68.0,
            width=136,
            height=40)
        img10 = tk.PhotoImage(file="admin_window\\img10.png")
        b10 = tk.Button(
            window,
            image=img10,
            borderwidth=0,
            highlightthickness=0,
            command=add_hash,
            relief="flat")
        b10.place(
            x=54.0, y=402.0,
            width=198,
            height=40)
        img11 = tk.PhotoImage(file="admin_window\\img11.png")
        b11 = tk.Button(
            window,
            image=img11,
            borderwidth=0,
            highlightthickness=0,
            command=add_words,
            relief="flat")
        b11.place(
            x=477.0, y=402.0,
            width=182,
            height=40)
        window.resizable(False, False)
        window.protocol("WM_DELETE_WINDOW", destroy_root)
        window.mainloop()

    def user_window():
        window = tk.Toplevel(root)
        window.geometry("683x513")
        window.configure(bg="#bce4e2")
        canvas = tk.Canvas(
            window,
            bg="#bce4e2",
            height=513,
            width=683,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = tk.PhotoImage(file="admin_window\\background.png")
        tk.background = canvas.create_image(
            341.5, 248.50000000000003,
            image=background_img)

        label_2 = Label(window, text=entry_username.get(), font=("Arial", 14))
        label_2.place(x=534, y=68, width=136, height=31)
        img0 = tk.PhotoImage(file="admin_window\\img0.png")
        b0 = tk.Button(
            window,
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=logout,
            relief="flat",

        )
        b0.place(
            x=534.0, y=105.0,
            width=136,
            height=31)

        img6 = tk.PhotoImage(file="admin_window\\img6.png")
        b6 = tk.Button(
            window,
            image=img6,
            borderwidth=0,
            highlightthickness=0,
            command=upload_open_file_explorer,
            relief="flat")
        b6.place(
            x=270, y=283.0,
            width=170,
            height=40)

        img7 = tk.PhotoImage(file="admin_window\\img7.png")
        b7 = tk.Button(
            window,
            image=img7,
            borderwidth=0,
            highlightthickness=0,
            command=download_open_file_explorer,
            relief="flat")
        b7.place(
            x=270, y=344.0,
            width=182,
            height=40)
        window.resizable(False, False)
        window.protocol("WM_DELETE_WINDOW", destroy_root)
        window.mainloop()

    def reg_user():
        window = tk.Toplevel(root)
        window.geometry("683x513")
        window.configure(bg="#bce4e2")
        canvas = tk.Canvas(
            window,
            bg="#bce4e2",
            height=513,
            width=683,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = tk.PhotoImage(file="admin_window\\background-Login.png")
        tk.background = canvas.create_image(
            341.5, 248.50000000000003,
            image=background_img)
        label_pano = Label(window, text="PAno", font=("Arial", 14), bg="#bce4e2")
        label_pano.place(x=120, y=210)

        label_username = Label(window, text="UserName", font=("Arial", 14), bg="#bce4e2")
        label_username.place(x=120, y=270)

        label_password = Label(window, text="Password", font=("Arial", 14), bg="#bce4e2")
        label_password.place(x=120, y=330)

        # Entry fields
        entry_pano = tk.Entry(window, font=("Arial", 14))
        entry_pano.place(x=270, y=210)

        entry_username = tk.Entry(window, font=("Arial", 14))
        entry_username.place(x=270, y=270)

        entry_password = tk.Entry(window, show="*", font=("Arial", 14))
        entry_password.place(x=270, y=330)

        def register_clk():
            if (len(entry_username.get())>7 and len(entry_username.get())<=15 and len(entry_password.get())>7):
                register_client("register_user"+"@DLP@"+entry_pano.get()+"@DLP@"+entry_username.get()+"@DLP@"+entry_password.get())
            else:
                if len(entry_username.get())<7 or len(entry_username.get())>15:
                    messagebox.showerror("Invalid Username","Your username must have more than 7 characters and less than 15 characters")
                elif len(entry_password.get())<7:
                    messagebox.showerror("Invalid Password",
                                         "Your Password must have more than 7 characters")

        button_login = tk.Button(window, text="Register", font=("Arial", 10), command=register_clk)
        button_login.place(x=462, y=410)

        window.resizable(False, False)
        window.mainloop()
        # Radio buttons
    def add_words():

        dialog = tk.Toplevel(root)
        label = tk.Label(dialog, text="Enter Words separated by comma :")
        label.pack()
        text_entry = tk.Entry(dialog)
        text_entry.pack()
        submit_button = tk.Button(dialog, text="Add", command=lambda: send_words(text_entry.get()))
        submit_button.pack()
        dialog.destroy()

    def tab_view():
        make_none()
        if not os.path.exists("documents"):
            os.makedirs("documents")
        request_file_explorer_for_rights("documents")
        #request_classfication()
        time.sleep(2)
        #senstivity = ret_file_list()
        files = ret_rights_list()
        checkboxes = []
        #fileID_Y = senstivity
        fileID_N=files
        rights_to_delete = []
        rights_to_implement = []
        froot = tk.Toplevel()
        froot.title("Action Dialog")
        canvas = tk.Canvas(froot)
        def toggle_checkbox(checkbox_var, label_text):
            if (checkbox_var.get() == False):
                rights_to_delete.append(label_text)
                print("delete ", rights_to_delete)
            else:
                rights_to_implement.append(label_text)
                print("implement ",rights_to_implement)

        def create_checkbox(label_text, right):
            if (right == "Y"):
                checkbox_var = tk.BooleanVar(value=True)
            else:
                checkbox_var = tk.BooleanVar(value=False)

                # Create a new checkbox
            label = tk.Label(canvas, text=label_text)
            label.grid(row=len(checkboxes), column=0, sticky=tk.W, padx=20)

            checkbox = tk.Checkbutton(canvas, variable=checkbox_var,
                                      command=lambda cb=checkbox_var, lt=label_text: toggle_checkbox(cb, lt))
            checkbox.grid(row=len(checkboxes), column=1, sticky=tk.W)
            checkboxes.append(checkbox_var)

            # Update the canvas and configure the scrollbar
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        #for i in range(len(fileID_Y)):
        #    create_checkbox(fileID_Y[i], "Y")
        for i in range(len(fileID_N)):
            create_checkbox(fileID_N[i], "N")

        """
        label = tk.Label(tab, text="Tab 2 View")
        label.pack(padx=10, pady=10)
        """
        def submit_action():
            print("check1.1")
            impl_copy = rights_to_implement.copy()
            del_copy = rights_to_delete.copy()
            print("check1.2")
            rights_to_implement[:] = [elem for elem in impl_copy if elem not in del_copy]
            rights_to_delete[:] = [elem for elem in del_copy if elem not in impl_copy]
            print("check1.3")
            if rights_to_implement:
                send_senstivity_list(rights_to_implement, 1)
                print("check1.4")
            if rights_to_delete:
                send_senstivity_list(rights_to_delete, 0)



        scrollbar = tk.Scrollbar(froot, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the checkboxes
        checkbox_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")

        button_frame = tk.Frame(froot)
        button_frame.pack(side="bottom")

        # Add the submit button to the frame
        button = tk.Button(button_frame, text="Submit", command=submit_action)
        button.pack(pady=10)

        # Center the button horizontally within its frame
        button_frame.grid_columnconfigure(0, weight=1)
    def add_hash():
        file_path_with_name = filedialog.askopenfilename(title="Open File",
                                                         filetypes=(("All Files", "*.*"), ("Python Files", "*.py")))
        filename=os.path.basename(file_path_with_name)
        hash=calculate_txt_hash(file_path_with_name)
        send_hash(hash,filename)

    def show_qFiles():
        request_qFiles("",1)
        time.sleep(2)
        file_names = ret_file_list()
        qroot = tk.Toplevel(root)
        qroot.title("File Selector")
        qroot.geometry("300x400")
        label = tk.Label(qroot, text="Select a file:")
        label.pack(pady=10)

        global listbox
        listbox = tk.Listbox(qroot, selectmode=tk.SINGLE, width=50, height=10)
        for filename in file_names:
            _, ext = os.path.splitext(filename)
            if ext.lower() in ['.jpg', '.jpeg', '.png']:
                listbox.insert(tk.END, filename)
                # Color sensitive images in red
                listbox.itemconfig(tk.END, {'fg': 'red'})
            else:
                listbox.insert(tk.END, filename)
        listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(qroot, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        open_button = tk.Button(qroot, text="Open", command=open_file_qFiles)
        open_button.pack(pady=5, side=tk.BOTTOM)
        move_button = tk.Button(qroot, text="Move to Docs", command=mov_qFile)
        move_button.pack(pady=5, side=tk.BOTTOM)
        delete_button = tk.Button(qroot, text="Delete", command=delete_qFile)
        delete_button.pack(pady=5, side=tk.BOTTOM)
        make_none()
    def mov_qFile():
        selected_item = listbox.curselection()
        if selected_item:
            filename = listbox.get(selected_item)
        move_qFile(filename,1)
    def delete_qFile():
        selected_item = listbox.curselection()
        if selected_item:
            filename = listbox.get(selected_item)
        move_qFile(filename,2)

    def open_file_qFiles():
        selected_item = listbox.curselection()
        if not os.path.exists("static"):
            os.makedirs("static")
        if selected_item:
            print("hehe")
            filename = listbox.get(selected_item)
            print(filename)
            print("hehe")
            request_qFiles(filename,2)
            while True:
                try:
                    with open("static\\" + filename, 'r') as file:
                        file_data=file.read()
                    os.remove("static\\" + filename)
                    break
                except:
                    print("working on open_file_qFiles()")
                time.sleep(1)
            show_text_dialog_logs(file_data)

    def clear_text(text_widget, text_dialog):
        global push_button_5
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.config(state="disabled")
        text_dialog.destroy()
        check_alert_for_button(3)
        client_login.button_color="not_red"

    def show_text_dialog_alert(text):
        text_dialog = tk.Toplevel()
        text_dialog.title("Text Viewer")

        text_widget = tk.Text(text_dialog, wrap="word", font=("Arial", 12))
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", text)
        text_widget.configure(state="disabled")

        scrollbar = tk.Scrollbar(text_dialog, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)

        clear_button = tk.Button(text_dialog, text="Clear", command=lambda: clear_text(text_widget, text_dialog))
        clear_button.pack()

    def show_text_dialog_logs(text):
        text_dialog = tk.Toplevel()
        text_dialog.title("Text Viewer")

        text_widget = tk.Text(text_dialog, wrap="word", font=("Arial", 12))
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", text)
        text_widget.configure(state="disabled")

        scrollbar = tk.Scrollbar(text_dialog, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)

    def show_alerts():
        if not os.path.exists("alerts_client"):
            os.makedirs("alerts_client")
        if ret_button_color()!="red":
            messagebox.showinfo("No alerts","At the moment, there are no alerts")
        else:
            check_alert_for_button(2)
            while True:
                try:
                    with open("alerts/alerts.txt", 'r') as file:
                        file_data = file.read()
                    break
                except:
                    print("working on show_alerts()")
                time.sleep(1)
            show_text_dialog_alert(file_data)

    def open_file_logs():
        if not os.path.exists("documents"):
            os.makedirs("documents")
        selected_item = listbox.curselection()
        if selected_item:
            filename = listbox.get(selected_item)
            request_logs(filename,2)
            while True:
                try:
                    with open("documents\\" + filename, 'r') as file:
                        file_data=file.read()
                    os.remove("documents\\" + filename)
                    break
                except:
                    print("working on open_file_logs()")
                time.sleep(1)
            show_text_dialog_logs(file_data)


    def log_box():
        request_logs("",1)
        time.sleep(2)
        file_names = ret_file_list()
        logroot = tk.Toplevel(root)
        logroot.title("File Selector")
        logroot.geometry("200x300")
        label = tk.Label(logroot, text="Select a file:")
        label.pack(pady=10)

        global listbox
        listbox = tk.Listbox(logroot, selectmode=tk.SINGLE, width=50, height=10)
        for i in range(len(file_names)):
            listbox.insert(tk.END, file_names[i])
        listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(logroot, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        open_button = tk.Button(logroot, text="Open", command=open_file_logs)
        open_button.pack(pady=5, side=tk.BOTTOM)
        make_none()

    def access_rights_upload():
        rights_to_implement=[]
        rights_to_delete=[]
        def toggle_checkbox(checkbox_var, label_text):
            if (checkbox_var.get()==False):
                rights_to_delete.append(label_text)
            else:
                rights_to_implement.append(label_text)


        def create_checkbox(label_text,right):
            if (right=="Y"):
                checkbox_var = tk.BooleanVar(value=True)
            else:
                checkbox_var = tk.BooleanVar(value=False)
            label = tk.Label(uploadroot, text=label_text)
            label.grid(row=len(checkboxes), column=0, sticky=tk.W, padx=20)
            checkbox = tk.Checkbutton(uploadroot, variable=checkbox_var,
                                      command=lambda cb=checkbox_var, lt=label_text: toggle_checkbox(cb, lt))
            checkbox.grid(row=len(checkboxes), column=1, sticky=tk.W)
            checkboxes.append(checkbox_var)
        def submit_action():
            impl_copy = rights_to_implement.copy()
            del_copy = rights_to_delete.copy()
            rights_to_implement[:] = [elem for elem in impl_copy if elem not in del_copy]
            rights_to_delete[:] = [elem for elem in del_copy if elem not in impl_copy]
            if rights_to_implement:
                send_rights_upload(rights_to_implement, 1)
            if rights_to_delete:
                send_rights_upload(rights_to_delete, 0)
            uploadroot.destroy()
        uploadroot = tk.Toplevel()
        uploadroot.title("Upload Access Rights")

        request_upload_list()
        time.sleep(2)
        names = []
        rights=[]
        names_rights=ret_upload_right_list()
        for i in range(len(names_rights)):
            parts = names_rights[i].split("@access_breaker@")
            divison = tuple(parts)
            names.append(divison[0])
            rights.append(divison[1])
        checkboxes = []
        for i in range(len(names)):
            create_checkbox(names[i],rights[i])
        button = tk.Button(uploadroot, text="Submit", command=submit_action)
        button.grid(row=len(checkboxes) + 1, column=0, columnspan=2)
        make_none()
        uploadroot.mainloop()

    def access_rights_download():
        global files
        make_none()
        def create_checkbox(row, col, initial_state=False):
            # Ensure checkboxes and checkbox_vars lists have enough rows
            while len(checkboxes) <= row:
                checkboxes.append([])
                checkbox_vars.append([])

            var = tk.BooleanVar(value=initial_state)
            var.trace_add('write', lambda *args: on_checkbox_change(row, col, var.get()))
            checkbox = tk.Checkbutton(Accessroot, text="", variable=var)
            checkbox.grid(row=row + 1, column=col + 1, padx=5, pady=5)
            checkboxes[row].append(checkbox)
            checkbox_vars[row].append(var)

        Accessroot = tk.Toplevel()
        Accessroot.title("Access Rights")

        # Sample names and files lists
        request_file_explorer_for_rights("documents")
        time.sleep(2)
        files = ret_rights_list()
        request_userName()
        time.sleep(2)
        names = ret_names_list()
        request_check_rights()
        time.sleep(2)

        # Initialize checkboxes and their variables
        checkboxes = []
        checkbox_vars = []
        access_names = ret_access_name_list()
        access_files = ret_access_file_list()

        # Create checkboxes for files
        for i in range(len(files)):
            for j in range(len(names)):
                initial_state = False
                for k in range(len(access_files)):
                    if files[i] == access_files[k] and names[j] == access_names[k]:
                        initial_state = True
                        break
                create_checkbox(i, j, initial_state)
        # Create labels for names
        for i, name in enumerate(names):
            tk.Label(Accessroot, text=name).grid(row=0, column=i + 1, padx=5, pady=5)

        # Create labels for files
        for i, file in enumerate(files):
            tk.Label(Accessroot, text=file).grid(row=i + 1, column=0, padx=5, pady=5)

        rights_to_implement = []
        rights_to_delete = []

        # Function to handle checkbox changes
        def on_checkbox_change(row, col, new_state):
            if new_state:
                rights_to_implement.append(files[row] + "@access_breaker@" + names[col])
            else:
                rights_to_delete.append(files[row]+ "@access_breaker@" + names[col])

        # Button to print the selected checkboxes
        def print_selection():
            impl_copy= rights_to_implement.copy()
            del_copy = rights_to_delete.copy()
            rights_to_implement[:] = [elem for elem in impl_copy if elem not in del_copy]
            rights_to_delete[:] = [elem for elem in del_copy if elem not in impl_copy]
            if rights_to_implement:
                send_rights_download(rights_to_implement,1)
            if rights_to_delete:
                send_rights_download(rights_to_delete,0)
            Accessroot.destroy()
        tk.Button(Accessroot, text="Apply Changes", command=print_selection).grid(row=len(files) + 1,columnspan=len(names) + 1, padx=5, pady=5)

        Accessroot.mainloop()



    def upload_open_file_explorer():
        if(var_user_type.get()==2):
            check_upload_rights(entry_pano.get()+"_"+entry_username.get())
            time.sleep(1)
            if ret_upload_right()=="N":
                messagebox.showinfo("Access Right","You do not have the right to upload content")
                make_none()
                return
        try:
            file_path_with_name = filedialog.askopenfilename(title="Open File", filetypes=(("All Files", "*.*"), ("Python Files", "*.py")))
            file_name = os.path.basename(file_path_with_name)
            if file_path_with_name:
                upload_file_client(file_name, file_path_with_name)
        except:
            return

    def download_open_file_explorer():
        global files
        def selected_folder():
            global files
            request_file_explorer_for_rights(selected_var_folder.get())
            time.sleep(2)
            file_menu['menu'].delete(0, 'end')
            files = ret_rights_list()

            for file in files:
                file_menu['menu'].add_command(label=file, command=tk._setit(selected_var_file, file))

        def selected_file():
            if (var_user_type.get() != 2):
                send_download_names(entry_pano.get()+"_"+entry_username.get(),selected_var_folder.get(),selected_var_file.get())
            else:
                send_download_names(entry_pano.get()+"_"+entry_username.get(),folders[1], selected_var_file.get())
            rootmini.destroy()

        rootmini = tk.Tk()
        rootmini.title("File Selector")
        rootmini.geometry("100x150")
        # List of filenames # Add your filenames here
        if not os.path.exists("real_labeling"):
            os.makedirs("real_labeling")
        if not os.path.exists("test_images"):
            os.makedirs("test_images")
        folders = ['real_labeling',
                   'documents']
        # Variable to store the selected file
        selected_var_folder = tk.StringVar(rootmini)
        selected_var_folder.set("Select Folder")  # Set default value to the first file
        selected_var_file = tk.StringVar(rootmini)
        selected_var_file.set("Select File")
        files = ['abc','def']

        # Dropdown menu
        if (var_user_type.get() != 2):
            folder_menu = tk.OptionMenu(rootmini, selected_var_folder, *folders)
            folder_menu.grid(row=0, column=0, padx=10, pady=10)
            forward_folder_button = tk.Button(rootmini, text="OK", command=selected_folder)
            forward_folder_button.grid(row=0, column=1, padx=5, pady=5)

        file_menu = tk.OptionMenu(rootmini, selected_var_file, *files)
        file_menu.grid(row=1, column=0, padx=10, pady=10)
        if (var_user_type.get() == 2):
            rootmini.geometry("160x50")
            request_file_explorer(folders[1],entry_pano.get()+"_"+entry_username.get())
            time.sleep(2)
            file_menu['menu'].delete(0, 'end')
            files = ret_file_list()
            for file in files:
                file_menu['menu'].add_command(label=file, command=tk._setit(selected_var_file, file))

        forward_file_button = tk.Button(rootmini, text="OK", command=selected_file)
        forward_file_button.grid(row=1, column=1, padx=5, pady=5)
        rootmini.mainloop()


    def login_button_action():

            login_credentials_send_message(var_user_type.get(), entry_pano.get(), entry_username.get(), entry_password.get())

            while True:
                if (close_window_server(3)=="3"):
                    messagebox.showinfo("Duplicate Login","User is already logined somwhere else. Log out from that client first")
                    make_none()
                    break
                elif(close_window_server(1)=="1"):
                    make_none()
                    root.withdraw()  # Hide the login window
                    admin_window()  # Open the admin window
                    break
                elif (close_window_server(1)=="2"):
                    make_none()
                    root.withdraw()  # Hide the login window
                    user_window()  # Open the user window
                    break
                elif (close_window_server(0)=="0"):
                    messagebox.showwarning("Invlid Credentials","Please enter correct credentials")
                    break
                time.sleep(1)
    
    def register_button_action():
        user_type = var_user_type.get()  # 1 for Admin, 0 for User
        pano = entry_pano.get()
        username = entry_username.get()
        password = entry_password.get()

        if not pano or not username or not password:
            messagebox.showwarning("Missing Information", "Please fill in all fields.")
            return

        breaker = "@DLP@"
        message = f"register_user{breaker}{user_type}{breaker}{pano}{breaker}{username}{breaker}{calculate_hash(password)}"
        register_client(message)

    root = tk.Tk()
    root.geometry("683x580")
    root.configure(bg="#bce4e2")
    canvas = tk.Canvas(
        root,
        bg="#bce4e2",
        height=513,
        width=683,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(x=0, y=0)

    background_img = tk.PhotoImage(file="admin_window\\background-Login.png")
    tk.background = canvas.create_image(
        341.5, 248.50000000000003,
        image=background_img)
    root.title("Login Dialog")
    root.resizable(False,False)

    # Labels
    label_pano = Label(root, text="PAno", font=("Arial", 14),bg="#bce4e2")
    label_pano.place(x=120, y=210)

    label_username = Label(root, text="UserName", font=("Arial", 14),bg="#bce4e2")
    label_username.place(x=120, y=270)

    label_password = Label(root, text="Password", font=("Arial", 14),bg="#bce4e2")
    label_password.place(x=120, y=330)

    # Entry fields
    entry_pano = tk.Entry(root, font=("Arial", 14))
    entry_pano.place(x=270, y=210)

    entry_username = tk.Entry(root, font=("Arial", 14))
    entry_username.place(x=270, y=270)

    entry_password = tk.Entry(root, show="*", font=("Arial", 14))
    entry_password.place(x=270, y=330)

    # Radio buttons
    var_user_type = tk.IntVar()
    var_user_type.set(0)  # Default value

    radio_admin = tk.Radiobutton(root, text="Admin", font=("Arial", 10), variable=var_user_type, value=1, highlightthickness=0)
    radio_admin.place(x=330, y=410)

    radio_user = tk.Radiobutton(root, text="User", font=("Arial", 10), variable=var_user_type, value=2,highlightthickness=0)
    radio_user.place(x=430, y=410)

    # Login button
    button_login = tk.Button(root, text="Login", font=("Arial", 10), command=login_button_action)
    button_login.place(x=462, y=460)
    # Register button
    button_login = tk.Button(root, text="Register", font=("Arial", 10), command=register_button_action)
    button_login.place(x=362, y=460)

    thread = Thread(target=check_alerts)
    thread.daemon = True  # Daemonize the thread so it terminates when the main thread terminates
    thread.start()

    root.mainloop()
    

login()