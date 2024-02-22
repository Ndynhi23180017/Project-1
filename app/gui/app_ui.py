from config import *
from app.db.crud import *
from app.utils.validation import ValidationUtils
class MainFrame(ttk.Frame):
    def __init__(self, master, switch_frame, remember_password):
        super().__init__(master)
        self.style = ttk.Style()
        self.switch_frame = switch_frame
        # parameter
        self.id_var = ttk.IntVar(value=0)
        self.name_var = ttk.StringVar(value="")
        self.price_var = ttk.StringVar(value="")
        self.expiry_var = ttk.StringVar(value="")
        self.expired_var = ttk.BooleanVar(value=False)
        # tableview
        self.dtv = None
        # functions
        self.create_widgets()
    def switch_child_frame(self, frame):
        frame.tkraise()
    
    def create_widgets(self):
        self.create_grid()
        self.create_sidebar()
        self.create_entry()
        self.create_button()

    def create_grid(self):
        # Create a PanedWindow widget as the main container
        self.paned_window = ttk.PanedWindow(self, orient="horizontal")
        self.paned_window.pack(fill="both", expand=True)
        # Create frames within the PanedWindow
        # sidebar
        self.sidebar_frame = ttk.Frame(self.paned_window, width=100, relief="raised")
        self.sidebar_frame.grid(row=0, column=0, sticky='ns')
        # entry
        self.ctn1 = ttk.Frame(self.paned_window, padding=10, relief="raised")
        self.ctn1.grid(row=0, column=1, sticky='nsew')
        # toggle frame
        self.toggle_frame = ttk.Frame(self.paned_window, padding=10, relief="raised")
        self.toggle_frame.grid(row=0, column=1, sticky='nsew')
        self.toggle_frame.place_forget()
        # table_view
        self.ctn2 = ttk.Frame(self.paned_window, padding=10, relief="raised")
        self.ctn2.grid(row=0, column=2, sticky='nsew')
        wrapper_table = ttk.LabelFrame(self.ctn2, text="Table Product", padding=10)
        wrapper_table.pack()
        self.create_table(wrapper_table)
        # Add frames to the PanedWindow
        self.paned_window.add(self.sidebar_frame)
        self.paned_window.add(self.ctn1)
        self.paned_window.add(self.toggle_frame)
        self.paned_window.add(self.ctn2)
        self.switch_child_frame(self.ctn1)
        self.toggle_frame_visible = False
        # Set up resizing behavior
        self.paned_window.bind("<B1-Motion>", self.on_resize)

    def on_resize(self, event):
        # Get the current mouse position
        x = event.x_root

        # Get the width of the main frame
        width = self.winfo_width()

        # Calculate the width of the left frame based on the mouse position
        left_width = x - self.paned_window.sash_coord(0)[0]
        # Set the width of the left frame
        self.paned_window.sash_place(0, left_width)
        self.paned_window.sash_place(1, left_width + self.paned_window.sash_coord(0)[1])

    def create_sidebar(self):
        # signout button
        icon_logout = Image.open('logout.png')
        icon_logout = icon_logout.resize((25,25))
        self.icon_logout = ImageTk.PhotoImage(icon_logout)
        self.signout_button = ttk.Button(self.sidebar_frame, text="Sign out", image=self.icon_logout, command=lambda:self.switch_frame(SignInFrame))
        self.signout_button.image = self.icon_logout
        self.signout_button.pack()

        #sth there

        # change theme button
        icon_theme = Image.open('background.png')
        icon_theme = icon_theme.resize((25,25))
        self.icon_theme = ImageTk.PhotoImage(icon_theme)
        self.change_theme_button = ttk.Button(self.sidebar_frame, text="Change theme", image=self.icon_theme,  command=self.show_theme_options)
        self.change_theme_button.image = self.icon_theme
        self.change_theme_button.pack()

        # toggle frame's content
        options = ['solar','superhero']
        selected_option = ttk.StringVar()
        self.combobox = ttk.Combobox(self.toggle_frame, textvariable=selected_option, value=options)
        self.combobox.pack()
        self.combobox.set(options[0])
        self.combobox.bind("<<ComboboxSelected>>", self.change_theme)

    def show_theme_options(self):
        if self.toggle_frame_visible:
            self.toggle_frame.place_forget()
            self.toggle_frame_visible = False
        else:
            self.toggle_frame.place(in_=self.ctn1, relx=0, rely=0, relwidth=1, relheight=1)
            self.switch_child_frame(self.toggle_frame)
            self.toggle_frame_visible = True
            
    def change_theme(self, event=None):
        selected_theme = self.combobox.get()
        self.style.theme_use(selected_theme)
        
    def create_entry(self):
        # Id
        wrapper_id = ttk.Frame(self.ctn1)
        wrapper_id.pack(fill=cs.X, pady=5)
        lbl_id = ttk.Label(wrapper_id, text="Id", width=10)
        lbl_id.pack(side=cs.LEFT, padx=10)
        entry_id = ttk.Entry(wrapper_id, width=24, textvariable=self.id_var)
        entry_id.pack(side=cs.LEFT)
        # Name
        wrapper_name = ttk.Frame(self.ctn1)
        wrapper_name.pack(fill=cs.X, pady=5)
        lbl_name = ttk.Label(wrapper_name, text="Name", width=10)
        lbl_name.pack(side=cs.LEFT, padx=10)
        entry_name = ttk.Entry(wrapper_name, width=24, textvariable=self.name_var)
        entry_name.pack(side=cs.LEFT)
        # Price
        wrapper_price = ttk.Frame(self.ctn1)
        wrapper_price.pack(fill=cs.X, pady=5)
        lbl_price = ttk.Label(wrapper_price, text="Price", width=10)
        lbl_price.pack(side=cs.LEFT, padx=10)
        entry_price = ttk.Entry(wrapper_price, width=24, textvariable=self.price_var)
        entry_price.pack(side=cs.LEFT)
        # Expiry
        wrapper_expiry = ttk.Frame(self.ctn1)
        wrapper_expiry.pack(fill=cs.X, pady=5)
        lbl_expiry = ttk.Label(wrapper_expiry, text="Expiry", width=10)
        lbl_expiry.pack(side=cs.LEFT, padx=10)
        self.expiry_var = wd.DateEntry(wrapper_expiry)
        self.expiry_var.pack(side=cs.LEFT)
        # ---------Validation----------
        ValidationUtils.validate_nullable(entry_name)
        ValidationUtils.validate_nullable(entry_price)
    def create_button(self):
        # crud
        wrapper_action = ttk.Frame(self.ctn1)
        wrapper_action.pack(fill=cs.X, pady=20)
        btn_add = ttk.Button(wrapper_action, text="Add", command=self.add_product)
        btn_add.pack(side=cs.LEFT, padx=5)
        btn_delete = ttk.Button(wrapper_action, text="Delete", command=self.delete_product)
        btn_delete.pack(side=cs.LEFT, padx=5)
        btn_update = ttk.Button(wrapper_action, text="Update", command=self.update_product)
        btn_update.pack(side=cs.LEFT, padx=5)
        
    def create_table(self, master):
        col_data = ["id", "Name", "Price", "Expiry", "Expired"]
        row_data = [
            (item.id, item.name, item.price, item.expiry, item.is_expired()) 
            for item in get_all_products()
        ]
        self.dtv = Tableview(
            master=master,
            coldata=col_data,
            rowdata=row_data,
            paginated=True,
            searchable=True,
        )
        self.dtv.pack()
    
    def update_table(self):
        self.dtv.build_table_data(
            coldata=["id", "Name", "Price", "Expiry","Expired"],
            rowdata=[
                (item.id, item.name, item.price, item.expiry, item.is_expired()) 
                for item in get_all_products()
            ]
        )
        self.dtv.load_table_data()

    def add_product(self):
        if ValidationUtils.check_status:
            create_product(
                name=self.name_var.get(), 
                price=float(self.price_var.get()), 
                expiry=datetime.strptime(self.expiry_var.entry.get(), "%m/%d/%Y")
            )
            self.update_table()
        else:
            mess_error = MessageDialog(title='Error Create Product', message='Please enter all fields')
            mess_error.show()

    def update_product(self):
        if self.check_exist(self.id_var.get()):
            edit_product(
                id=self.id_var.get(),
                name=self.name_var.get(), 
                price=float(self.price_var.get()), 
                expiry=datetime.strptime(self.expiry_var.entry.get(), "%m/%d/%Y"),
            )
            self.update_table()

    def delete_product(self):
        if self.check_exist(self.id_var.get()):
            del_product(self.id_var.get())
            self.update_table()

    def check_exist(self, id:int):
        return id in [item.id for item in get_all_products()]
class SignInFrame(ttk.Frame):
    def __init__(self, master, switch_frame, remember_password):
        super().__init__(master)
        self.switch_frame = switch_frame
        self.username_entry = ttk.Entry(self)
        self.password_entry = ttk.Entry(self, show="*")
        self.sign_in_button = ttk.Button(self, text="Sign In", command=lambda: self.sign_in(remember_password))
        self.sign_up_button = ttk.Button(self, text="Sign Up", command=lambda: self.sign_up(remember_password))

        ttk.Label(self, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.sign_up_button.grid(row=2, column=0, padx=5, pady=5)
        self.sign_in_button.grid(row=2, column=1, padx=5, pady=5)
    def sign_up(self, remember_password):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            remember_password[username] = password
            signup_success = MessageDialog(message='Success')
            signup_success.show()
        else:
            signup_error = MessageDialog(message='Error')
            signup_error.show()
    def sign_in(self, remeber_password):
        username = self.username_entry.get()
        password = self.password_entry.get()
        stored_password = remeber_password.get(username)
        if password == stored_password:
            self.switch_frame(MainFrame)
        else:
            signin_error = MessageDialog(message='Ivalid username or password')
            signin_error.show()
class App(ttk.Frame):
    def __init__(self, master: ttk.Window):
        super().__init__(master, padding=10)
        self.remember_password = {}
        self.frames = {}
        # create frame for function 
        for F in (SignInFrame, MainFrame):
            frame = F(self, self.switch_frame, self.remember_password)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_frame(SignInFrame)
    def switch_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
    def switch_to_sign_in(self):
        self.switch_frame(self.sign_in_frame)
    def remember_password(self, username, password):
        self.remember_password[username] = password


def main():
    config_window = {
        "title": "App",
        "themename": "solar",
        "size": (1500,700),
        "resizable": (True, True),
        "position": (1920-1500, 0)
    }
    window = ttk.Window(**config_window)
    app = App(window)
    app.pack()
    window.mainloop()