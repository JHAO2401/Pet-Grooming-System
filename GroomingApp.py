from tkinter import *
from tkinter import ttk, messagebox
import os
import calendar
from datetime import datetime, timedelta

class GroomingApp:
    def __init__(self, root, main_screen=None):
        # Main application class for managing grooming records and user interface
        self.root = root
        self.main_screen = main_screen  
        self.root.title("🪞 Grooming Tracker 🪞")  # Set window title
        self.root.state("zoomed")  # Maximize window
        self.root.configure(bg="#ecc9cf")  # Set background color
        
        # Dictionary storing grooming services with their corresponding prices and durations
        self.GROOMING = {
            "Deluxe Grooming Package": ("75.00", "60 min"),
            "Skin Treatment": ("50.30", "45 min"),
            "Basic Bath & Brush": ("35.00", "30 min"),
            "Spa Treatment Package": ("120.00", "75 min"),
            "Sensitive Skin Care": ("55.80", "60 min")
        }
        self.manager = GroomingManager()  # Create grooming data manager
        self.header()  # Create header section
        self.create_ui()  # Create main UI
        self.show_add_record()  # Show add record form by default

    def header(self):
        # Create the application header section including the title and navigation button
        header_frame = Frame(self.root, bg="#ecc9cf", height=100,relief='ridge', bd=10)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        Label(header_frame, text="🐾 Grooming Tracker 🐾", font=("Helvetica", 50, "bold"), 
                bg="#ecc9cf", fg="black").pack(fill='x',pady=(20, 0))
        
        # Back to main screen button 
        Button(header_frame, text="← Back to Main", font=("Arial", 12, "bold"), 
                              bg="#E74C3C", fg="white", command=self.leave_to_main).pack(side=RIGHT)
    
    def leave_to_main(self):
        # Return to the main application screen when the back button is clicked
        if self.main_screen:
            self.root.destroy()  # Close current window
            self.main_screen.state('zoomed')  # Restore main window

    def create_ui(self):
        # Create the main layout of the user interface
        main_container = Frame(self.root, bg="white")
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create the left navigation sidebar containing menu options
        nav_frame = Frame(main_container, bg="#dbbed7", width=100,relief='ridge', bd=10)
        nav_frame.pack(side='left', fill='y')
        
        # Navigation buttons with their
        Button(nav_frame, text="Add Record", font=("Helvetica", 12, "bold"), width=15, height=2, bg="#CF93E4", fg="white",relief='groove', bd=10,
               command=self.show_add_record).pack(pady=10, padx=10)
        Button(nav_frame, text="View Records", font=("Helvetica", 12, "bold"),width=15, height=2, bg="#BC77D1", fg="white", relief='groove', bd=10,
               command=self.show_all_records).pack(pady=10, padx=10)
        
        # Main content area used to display forms and record tables
        self.content_frame = Frame(main_container, bg="white")
        self.content_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
    
    def show_all_records(self):
        # Display all grooming records in a table using Treeview
        for widget in self.content_frame.winfo_children():
            widget.destroy()  # Clear current content

        title_frame = Frame(self.content_frame, bg="white")
        title_frame.pack(fill='x', pady=(10, 20))
        Label(title_frame, text="📋 All Grooming Records 📋", 
              font=("Helvetica", 25, "bold"), bg="white").pack()
        
        # Treeview frame for records
        tree_frame = Frame(self.content_frame, bg="white")
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create Treeview widget and define table columns
        self.tree = ttk.Treeview(tree_frame, columns=("pet", "date", "time", "grooming", "price", "duration"),
                                 show="headings",selectmode='browse')
        # Configure columns
        columns = [
            ("pet", "Pet Name", 150),
            ("date", "Date", 120),
            ("time", "Time", 100),
            ("grooming", "Grooming", 150),
            ("price", "Price (RM)", 120),
            ("duration", "Duration", 100)
        ]
        for col, heading, width in columns:
            self.tree.heading(col, text=heading, anchor='center')
            self.tree.column(col, width=width, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
        self.load_all_records()  # Load records into treeview
        
        # Frame containing action buttons for record management
        action_frame = Frame(self.content_frame, bg="white")
        action_frame.pack(pady=10)

        # Action buttons
        Button(action_frame, text="Edit Selected", font=("Helvetica", 12, "bold"),bg="#F39C12", fg="white",
               width=15,height=2, command=self.open_edit_dialog).pack(side='left', padx=10)
        Button(action_frame, text="Refresh", font=("Helvetica", 12, "bold"),bg="#3498DB", fg="white",
               width=15,height=2, command=self.refresh_records).pack(side='left', padx=10)
        Button(action_frame, text="Delete Selected", font=("Helvetica", 12, "bold"),bg="#E74C3C", fg="white",
               width=15,height=2, command=self.delete_selected).pack(side='left', padx=10)
    
    def get_customers(self):
        # Load customer information from the data file
        customers = []
        if os.path.exists("data.txt"):
            with open("data.txt", 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('PET|'):  # Identify customer records
                        parts = line.split('|')
                        if len(parts) >= 4:
                            customer_data = {
                                'pet_name': parts[1],
                                'owner': parts[2],
                                'breed': parts[3] if len(parts) > 3 else 'Unknown'
                            }
                            customers.append(customer_data)
        return customers
    
    def format_customer_names(self, customers):
        # Format customer information for display in the selection dropdown
        customer_names = []
        for customer in customers:
            formatted_name = f"😺{customer['pet_name']} -👤{customer['owner']}"
            if customer.get('breed'):
                formatted_name += f" -🐾{customer['breed']}"
            customer_names.append(formatted_name)
        return customer_names
    
    def extract_pet_name(self, selected_customer):
        # Extract the pet name from the selected customer string
        if not selected_customer:
            return ""
        
        parts = selected_customer.split(" -👤")
        if len(parts) > 0:
            pet_name_part = parts[0].replace("😺", "").strip()
            return pet_name_part
        return ""
    
    def load_all_records(self):
        # Load all grooming records from memory into the Treeview table
        for item in self.tree.get_children():
            self.tree.delete(item)  # Clear existing items
        
        # Collect all records
        all_records = []
        for pet_name, recs in self.manager.records.items():
            for rec in recs:
                all_records.append((pet_name, rec))
    
        # Insert records into treeview
        for pet_name, rec in all_records:
            display_price = rec['price'].replace('RM', '').strip() if rec['price'].startswith('RM') else rec['price']
            values = (
                pet_name,
                rec['date'],
                rec['time'],
                rec['grooming'],
                display_price,
                rec['duration']
            )
            self.tree.insert("", END, values=values)
    
    def delete_selected(self):
        # Load all grooming records from memory into the Treeview table
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select records to delete.")
            return
        
        # Confirmation dialog
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected)} record(s)?")
        if not confirm:
            return

        # Collect records to delete
        records_to_delete = []
        for item in selected:
            values = self.tree.item(item)['values']
            records_to_delete.append(values)

        deleted_count = 0
        # Delete each selected record
        for pet_name, date, time, grooming, price, duration in records_to_delete:
            pet_records = self.manager.records.get(pet_name, [])
            for i, rec in enumerate(pet_records):
                if (rec['date'] == date and 
                    rec['time'] == time and 
                    rec['grooming'] == grooming):
                    rec_price = rec['price'].replace('RM', '').strip() if rec['price'].startswith('RM') else rec['price']
                    if rec_price == price and rec['duration'] == duration:
                        pet_records.pop(i)  # Remove record
                        deleted_count += 1
                        break
            
            # Remove pet entry if no records left
            if not pet_records:
                self.manager.records.pop(pet_name, None)
        
        # Save changes to file
        if self.manager.save_to_file():
            messagebox.showinfo("Success", f"{deleted_count} record(s) deleted successfully!")
            if hasattr(self, 'tree') and self.tree:
                for item in selected:
                    self.tree.delete(item)
            else:
                self.show_all_records()
        else:
            messagebox.showerror("Error", "Failed to delete records.")
    
    def refresh_records(self):
        # Refresh the displayed records by reloading data from the file
        self.manager.load_from_file()  
        self.load_all_records() 
    
    def show_add_record(self):
        # Display the form used to add new grooming records
        for widget in self.content_frame.winfo_children():
            widget.destroy()  # Clear current content

        title_frame = Frame(self.content_frame, bg="white")
        title_frame.pack(fill='x', pady=(10, 20))
        Label(title_frame, text="🪞 Add New Grooming Record 🪞",
              font=("Helvetica", 25, "bold"), bg="white").pack()
        
        # Form frame
        form_frame = Frame(self.content_frame, bg="white")
        form_frame.pack(pady=20, padx=50)
        
        # Customer selection dropdown
        Label(form_frame, text="Select Customer:", font=("Helvetica", 12, "bold"),
              bg="white", width=15, anchor="w").grid(row=0, column=0, padx=10, pady=12, sticky='w')

        customers = self.get_customers()
        customer_names = self.format_customer_names(customers)
        
        customer_var = StringVar()
        customer_combo = ttk.Combobox(form_frame, textvariable=customer_var,
                                     values=customer_names, state="readonly",
                                     font=("Helvetica", 12), width=30)
        customer_combo.grid(row=0, column=1, columnspan=2, pady=12, sticky='w')
        
        # Show message if no customers found
        if not customer_names:
            Label(form_frame, text="No customers found in data.txt. Please add customers first.",
                  font=("Helvetica", 10), bg="white", fg="red").grid(row=1, column=1, columnspan=2, pady=5, sticky='w')
        
        # Date selection
        Label(form_frame, text="Date:", font=("Helvetica", 12, "bold"),
              bg="white", width=15, anchor="w").grid(row=2, column=0, padx=10, pady=12, sticky='w')
        
        date_var = StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        Entry(form_frame, font=("Helvetica", 12), width=15,
                          textvariable=date_var, state='readonly').grid(row=2, column=1, pady=12, sticky='w')
        
        # Button to open the calendar date selection window 
        Button(form_frame, text="📅", font=("Helvetica", 12),bg='#f7a9a9', fg='black', width=3,
               command=lambda: self.open_calendar(date_var)).grid(row=2, column=2, padx=10, pady=12, sticky='w')
        
        # Time selection
        Label(form_frame, text="Time:", font=("Helvetica", 12, "bold"),
              bg="white", width=15, anchor="w").grid(row=3, column=0, padx=10, pady=12, sticky='w')
        
        time_frame = Frame(form_frame, bg='white')
        time_frame.grid(row=3, column=1, columnspan=2, pady=12, sticky='w')
        
        hour_var = StringVar(value="08")
        hour_combo = ttk.Combobox(time_frame, textvariable=hour_var,
                                 width=4, font=("Helvetica", 11), state='readonly')
        hour_combo['values'] = [f"{hour:02d}" for hour in range(8, 18)]
        hour_combo.pack(side='left', padx=2)
        
        Label(time_frame, text=":", bg='white', font=("Helvetica", 12)).pack(side='left')
        minute_var = StringVar(value="00")
        minute_combo = ttk.Combobox(time_frame, textvariable=minute_var,
                                   width=4, font=("Helvetica", 11), state='readonly')
        minute_combo['values'] = ["00", "15", "30", "45"]
        minute_combo.pack(side='left', padx=2)

        # Grooming service selection dropdown
        Label(form_frame, text="Grooming:", font=("Helvetica", 12, "bold"),
              bg="white", width=15, anchor="w").grid(row=4, column=0, padx=10, pady=12, sticky='w')
        grooming_var = StringVar()
        grooming_combo = ttk.Combobox(form_frame, textvariable=grooming_var,
                                    values=list(self.GROOMING.keys()), state="readonly",
                                    font=("Helvetica", 12), width=30)
        grooming_combo.grid(row=4, column=1, columnspan=2, pady=12, sticky='w')

        def on_grooming_selected(event):
            # Update price and duration when grooming is selected
            self.update_grooming_details(grooming_var, price_var, duration_var)
        grooming_combo.bind("<<ComboboxSelected>>", on_grooming_selected)
        
        # Price field
        Label(form_frame, text="Price (RM):", font=("Helvetica", 12, "bold"),
              bg="white", width=15, anchor="w").grid(row=5, column=0, padx=10, pady=12, sticky='w')
        
        price_var = StringVar()
        Entry(form_frame, font=("Helvetica", 12), width=30,
                           textvariable=price_var).grid(row=5, column=1, columnspan=2, pady=12, sticky='w')
        
        # Duration field
        Label(form_frame, text="Duration:", font=("Helvetica", 12, "bold"),
              bg="white", width=15, anchor="w").grid(row=6, column=0, padx=10, pady=12, sticky='w')
        duration_var = StringVar()
        Entry(form_frame, font=("Helvetica", 12), width=30,
              textvariable=duration_var).grid(row=6, column=1, columnspan=2, pady=12, sticky='w')   

        # Error display label
        error_label = Label(form_frame, text="", font=("Helvetica", 10),
                           bg="white", fg='red')
        error_label.grid(row=7, column=1, columnspan=2, pady=(5, 10), sticky='w')
        
        # Button frame
        button_frame = Frame(self.content_frame, bg="white")
        button_frame.pack(pady=20)
        
        def save_record():
            # Validate input fields and save a new grooming record
            selected_customer = customer_var.get().strip()
            date = date_var.get()
            time = f"{hour_var.get()}:{minute_var.get()}"
            grooming = grooming_var.get()
            price = price_var.get().strip()
            duration = duration_var.get().strip()
            pet_name = self.extract_pet_name(selected_customer)

            # Validation
            match True:
                case _ if not selected_customer:
                    error_label.config(text="Please select a customer.")
                    customer_combo.focus()
                    return

                case _ if not pet_name:
                    error_label.config(text="Invalid customer selection.")
                    return

                case _ if not date:
                    error_label.config(text="Please select date.")
                    return

                case _ if not grooming:
                    error_label.config(text="Please select grooming.")
                    return

                case _ if not price:
                    error_label.config(text="Please enter price.")
                    return

                case _ if not self.is_valid_price(price):
                    error_label.config(text="Invalid price format (e.g., 50.00).")
                    return

                case _ if not duration:
                    error_label.config(text="Please enter duration.")
                    return
            
            # Save record
            if self.manager.add_record(pet_name, date, time, grooming, price, duration):
                messagebox.showinfo("Success", "Record added successfully!")
                # Reset form
                customer_var.set("")
                date_var.set(datetime.now().strftime("%Y-%m-%d"))
                hour_var.set("08")
                minute_var.set("00")
                grooming_var.set("")
                price_var.set("")
                duration_var.set("")
                error_label.config(text="")
                # Refresh customer list
                customers = self.get_customers()
                customer_names = self.format_customer_names(customers)
                customer_combo['values'] = customer_names
            else:
                error_label.config(text="Failed to save record.")
        
        # Form buttons
        Button(button_frame, text="Save Record", font=("Helvetica", 12, "bold"),bg="#27ae60", fg="white",
               width=15, command=save_record).pack(side='left', padx=10)
    
    def update_grooming_details(self, grooming_var, price_var, duration_var):
        # Update price and duration fields based on selected grooming
        grooming = grooming_var.get()
        if grooming in self.GROOMING:
            price, duration = self.GROOMING[grooming]
            price_var.set(price)
            duration_var.set(duration)
    
    def open_edit_dialog(self):
        # Open a dialog window to edit the selected grooming record
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a record to edit.")
            return
        if len(selected) > 1:
            messagebox.showerror("Error", "Please select only one record to edit.")
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        
        # Create edit window
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Grooming Record")
        edit_window.geometry("500x600")
        edit_window.configure(bg='white')
        edit_window.transient(self.root)
        edit_window.grab_set()  # Make modal
        
        title_label = Label(edit_window, text="Edit Grooming Record",
                           font=('Helvetica', 24, 'bold'), 
                           bg='white', fg='#2c3e50')
        title_label.pack(pady=(20, 30))
        
        form_container = Frame(edit_window, bg='white')
        form_container.pack(expand=True, padx=40)
        
        # Pet name field (readonly)
        Label(form_container, text="Pet Name:", font=('Helvetica', 12, 'bold'),
              bg='white', anchor='w').grid(row=0, column=0, padx=(0, 10), pady=15, sticky='w')
        
        pet_name_var = StringVar(value=values[0])
        pet_entry = Entry(form_container, font=('Helvetica', 12), width=25,
                         textvariable=pet_name_var, state='readonly')
        pet_entry.grid(row=0, column=1, pady=15, sticky='w')
        
        # Date field (readonly)
        Label(form_container, text="Date:", font=('Helvetica', 12, 'bold'),
              bg='white', anchor='w').grid(row=1, column=0, padx=(0, 10), pady=15, sticky='w')
        
        date_var = StringVar(value=values[1])
        date_entry = Entry(form_container, font=('Helvetica', 12), width=15,
                          textvariable=date_var, state='readonly')
        date_entry.grid(row=1, column=1, pady=15, sticky='w')
        
        # Time field
        Label(form_container, text="Time:", font=('Helvetica', 12, 'bold'),
              bg='white', anchor='w').grid(row=2, column=0, padx=(0, 10), pady=15, sticky='w')
        
        time_var = StringVar(value=values[2])
        time_entry = Entry(form_container, font=('Helvetica', 12), width=15,
                          textvariable=time_var)
        time_entry.grid(row=2, column=1, pady=15, sticky='w')
        
        # Grooming selection
        Label(form_container, text="Grooming:", font=('Helvetica', 12, 'bold'),
              bg='white', anchor='w').grid(row=3, column=0, padx=(0, 10), pady=15, sticky='w')
        
        grooming_var = StringVar(value=values[3])
        grooming_combo = ttk.Combobox(form_container, textvariable=grooming_var,
                                    values=list(self.GROOMING.keys()), state="readonly",
                                    font=('Helvetica', 12), width=25)
        grooming_combo.grid(row=3, column=1, pady=15, sticky='w')

        def on_grooming_selected_edit(event):
            # Update price and duration when grooming changes
            self.update_grooming_details(grooming_var, price_var, duration_var)
        grooming_combo.bind("<<ComboboxSelected>>", on_grooming_selected_edit)
        
        # Price field
        Label(form_container, text="Price (RM):", font=('Helvetica', 12, 'bold'),
              bg='white', anchor='w').grid(row=4, column=0, padx=(0, 10), pady=15, sticky='w')
        
        price_var = StringVar(value=values[4])
        price_entry = Entry(form_container, font=('Helvetica', 12), width=25,
                           textvariable=price_var)
        price_entry.grid(row=4, column=1, pady=15, sticky='w')
        
        # Duration field
        Label(form_container, text="Duration:", font=('Helvetica', 12, "bold"),
              bg='white', anchor='w').grid(row=5, column=0, padx=(0, 10), pady=15, sticky='w')
        
        duration_var = StringVar(value=values[5])
        duration_entry = Entry(form_container, font=('Helvetica', 12), width=25,
                              textvariable=duration_var)
        duration_entry.grid(row=5, column=1, pady=15, sticky='w')
        
        # Error display label
        error_label = Label(form_container, text="", font=('Helvetica', 10),
                           bg='white', fg='red')
        error_label.grid(row=6, column=1, pady=(5, 10), sticky='w')
        
        # Button frame
        button_frame = Frame(edit_window, bg='white')
        button_frame.pack(pady=20)
        
        def save_edit():
            # Validate and save the edited grooming record
            pet = pet_name_var.get().strip()
            date = date_var.get()
            time = time_var.get().strip()
            grooming = grooming_var.get()
            price = price_var.get().strip()
            duration = duration_var.get().strip()
            
            # Validation
            match True:
                case _ if not pet:
                    error_label.config(text="Please enter pet name.")
                    return

                case _ if not date:
                    error_label.config(text="Please select date.")
                    return

                case _ if not grooming:
                    error_label.config(text="Please select grooming.")
                    return

                case _ if not price:
                    error_label.config(text="Please enter price.")
                    return

                case _ if not self.is_valid_price(price):
                    error_label.config(text="Invalid price format (e.g., 50.00).")
                    return

                case _ if not duration:
                    error_label.config(text="Please enter duration.")
                    return
            
            # Update record in memory
            for pet_name, recs in list(self.manager.records.items()):
                for i, rec in enumerate(list(recs)):
                    if (pet_name == values[0] and 
                        rec['date'] == values[1] and 
                        rec['time'] == values[2] and 
                        rec['grooming'] == values[3]):

                        self.manager.records[pet_name][i] = {
                            "date": date,
                            "time": time,
                            "grooming": grooming,
                            "price": f"RM{price}",
                            "duration": duration
                        }
                        # Handle pet name change
                        if pet != pet_name:
                            self.manager.records[pet_name].pop(i)
                            if not self.manager.records[pet_name]:
                                del self.manager.records[pet_name]
                            self.manager.records.setdefault(pet, []).append({
                                "date": date,
                                "time": time,
                                "grooming": grooming,
                                "price": f"RM{price}",
                                "duration": duration
                            })  
                        break
            
            # Save to file
            if self.manager.save_to_file():
                messagebox.showinfo("Success", "Record updated successfully!")
                edit_window.destroy()
                self.load_all_records()  # Refresh display
            else:
                error_label.config(text="Failed to update record.")
        
        # Edit dialog buttons
        Button(button_frame, text="Save Changes", font=('Helvetica', 14, 'bold'), width=15, bg='#27ae60', fg='white', pady=8,
               command=save_edit).pack(side='left', padx=10)
        Button(button_frame, text="Cancel", font=('Helvetica', 14, 'bold'),width=15, bg='#95a5a6', fg='white', pady=8,
               command=edit_window.destroy).pack(side='left', padx=10)
    
    def is_valid_price(self, price):
        # Validate the price input to ensure it is a non-negative numeric value
        try:
            if price.replace('.', '', 1).isdigit():
                value = float(price)
                if value >= 0:
                    return True
            return False
        except:
            return False

    def open_calendar(self, date_var):
        # Open a calendar window for date selection
        top = Toplevel(self.root)
        top.title("Select Date")
        top.geometry("490x450")
        top.configure(bg='white')
        top.transient(self.root)
        top.grab_set() 
        
        current_year, current_month = datetime.now().year, datetime.now().month
        
        # Calendar UI components
        header = Frame(top, bg='#2c3e50', height=60)
        header.pack(fill='x')
        date_label = Label(header, text="", font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        date_label.pack(pady=10)
        nav_frame, cal_frame, btn_frame = Frame(top, bg='white'), Frame(top, bg='white'), Frame(top, bg='white')
        nav_frame.pack(fill='x', pady=10), cal_frame.pack(fill='both', expand=True, padx=20, pady=10), btn_frame.pack(fill='x', pady=10)
    
        def show_calendar():
            #Display calendar for current month
            for widget in cal_frame.winfo_children():
                widget.destroy()
            
            date_label.config(text=f"{current_year}-{current_month:02d}")
            # Day headers
            for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
                Label(cal_frame, text=day, font=('Arial', 10, 'bold'), bg='white', fg='#2c3e50', width=6).grid(row=0, column=i, padx=2, pady=2)
            
            cal, today = calendar.monthcalendar(current_year, current_month), datetime.now()
            week_num = 0 
            while week_num < len(cal):
                week = cal[week_num]
                day_num = 0 
                
                while day_num < len(week):
                    day = week[day_num]
                    
                    if day != 0:
                        is_today = (current_year == today.year and current_month == today.month and day == today.day)
                        btn_text = f"*{day}*" if is_today else str(day)
                        # Day button 
                        Button(cal_frame, text=btn_text, font=('Arial', 10), bg='#e74c3c' if is_today else '#ecf0f1',
                            fg='white' if is_today else '#2c3e50', width=6, height=2, 
                            command=lambda d=day: select_date(d)).grid(row=week_num+1, column=day_num, padx=2, pady=2)
                    day_num += 1 
                week_num += 1 
    
        def select_date(day):
            # Handle date selection from calendar
            selected_date = datetime(current_year, current_month, day)
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            # Adjust if date is in past
            days_added = 0
            while selected_date < today:
                selected_date += timedelta(days=1)
                days_added += 1
            
            if days_added > 0:
                messagebox.showinfo("Date Adjusted", 
                                f"Selected date was in the past.\n"
                                f"Automatically adjusted to {selected_date.strftime('%Y-%m-%d')}")
            
            date_var.set(f"{selected_date.year}-{selected_date.month:02d}-{selected_date.day:02d}")
            top.destroy()
        
        def select_today():
            #Select today's date
            date_var.set(datetime.now().strftime("%Y-%m-%d"))
            top.destroy()
        
        def prev_month():
            #Navigate to previous month
            nonlocal current_month, current_year
            current_month = 12 if current_month == 1 else current_month - 1
            if current_month == 12: current_year -= 1
            show_calendar()
        
        def next_month():
            # Navigate to next month
            nonlocal current_month, current_year
            current_month = 1 if current_month == 12 else current_month + 1
            if current_month == 1: current_year += 1
            show_calendar()
        
        # Navigation buttons
        Button(nav_frame, text="◀", font=('Arial', 12), width=5, command=prev_month).pack(side='left', padx=20)
        Button(nav_frame, text="▶", font=('Arial', 12), width=5, command=next_month).pack(side='right', padx=20)
        Button(btn_frame, text="Today", font=('Arial', 12), width=10, command=select_today).pack(side='left', padx=20)
        Button(btn_frame, text="Cancel", font=('Arial', 12), width=10, command=top.destroy).pack(side='right', padx=20)
        show_calendar()  # Initial display

class GroomingManager:
    def __init__(self, filename="data.txt"):
        # Initialize the GroomingManager class and load existing grooming records
        self.filename = filename
        self.records = {}  # Dictionary to store grooming records
        self.load_from_file()  # Load existing data
    
    def load_from_file(self):
        # Load grooming records from the data file into memory
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("GROOMING|"):  # Identify grooming records
                        parts = line.split("|")
                        if len(parts) >= 7:
                            pet = parts[1]
                            rec = {
                                "date": parts[2], "time": parts[3], "grooming": parts[4],
                                "price": parts[5], "duration": parts[6]
                            }
                            self.records.setdefault(pet, []).append(rec)
        except Exception as e:
            print(f"Error loading file: {e}")
    
    def save_to_file(self):
        # Save all grooming records from memory back to the data file
        try:
            # Read all non-GROOMING lines
            other_lines = []
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    for line in file:
                        if not line.strip().startswith("GROOMING|"):
                            other_lines.append(line)
            
            # Write all lines back
            with open(self.filename, 'w', encoding='utf-8') as file:
                # Write other lines first
                for line in other_lines:
                    file.write(line)
                
                # Write all GROOMING records
                for pet, recs in self.records.items():
                    for r in recs:
                        # Add "RM" prefix when saving to file
                        price_str = r['price']
                        if not price_str.startswith('RM'):
                            price_str = f"RM{price_str}"
                        line = f"GROOMING|{pet}|{r['date']}|{r['time']}|{r['grooming']}|{price_str}|{r['duration']}\n"
                        file.write(line)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

    def add_record(self, pet, date, time, grooming, price, duration):
        # Add a new grooming record and store it in the data file
        # Add "RM" prefix when storing in memory
        formatted_price = f"RM{price}" if not price.startswith('RM') else price
        self.records.setdefault(pet, []).append({
            "date": date, "time": time, "grooming": grooming,
            "price": formatted_price, "duration": duration
        })
        return self.save_to_file()  # Save to file

    def delete_records(self, pet, indices):
        #  Delete grooming records by indices
        if not pet:
            # Delete from all records
            all_records = []
            for pet_name, recs in self.records.items():
                for rec in recs:
                    all_records.append((pet_name, rec))

            # Delete records in reverse order to avoid index issues
            for i in sorted(indices, reverse=True):
                if 0 <= i < len(all_records):
                    pet_name_to_delete, record_to_delete = all_records[i]
                    pet_records = self.records.get(pet_name_to_delete, [])
                    for j, rec in enumerate(pet_records):
                        if (rec["date"] == record_to_delete["date"] and
                            rec["time"] == record_to_delete["time"] and
                            rec["grooming"] == record_to_delete["grooming"] and
                            rec["price"] == record_to_delete["price"] and
                            rec["duration"] == record_to_delete["duration"]):
                            pet_records.pop(j)
                            break
                    
                    # Remove pet entry if no records left
                    if not pet_records:
                        self.records.pop(pet_name_to_delete, None)
        else:
            # Delete from specific pet
            if pet not in self.records:
                return False
            
            # Delete records in reverse order
            for i in sorted(indices, reverse=True):
                if 0 <= i < len(self.records[pet]):
                    self.records[pet].pop(i)
            
            # Remove pet entry if no records left
            if not self.records[pet]:
                del self.records[pet]
        return self.save_to_file()

    def get_records(self, pet):
        # Get records for a specific pet or all records
        if pet:
            return self.records.get(pet, [])
        else:
            # Return all records
            all_records = []
            for pet_recs in self.records.values():
                all_records.extend(pet_recs)
            return all_records

if __name__ == "__main__":
    root = Tk()  # Create main window
    app = GroomingApp(root)  # Create grooming application 
    root.mainloop()