from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import os, calendar

class vet_app:
    def __init__(self, root, main_screen=None): 
        # Vet Appointment Application 
        self.root = root
        self.main_screen = main_screen
        self.root.title("💉 Vet Appointment Tracker 💉")  # Set window title
        self.root.state("zoomed")  # Maximize window
        self.root.configure(bg="#7FDC34")  # Set background color
        self.appointment_manager = AppointmentManager()  # Create appointment manager instance
        self.frames, self.current_frame = {}, None  # Initialize frame storage and current frame
        self.UI()  # Build user interface
       
    def UI(self):
        self.title()  # Create title section
        self.main_frame()  # Create main frame

    def title(self):
        # Create title frame with back button
        title_frame = Frame(self.root, bg="#33d6bb", height=100,relief='ridge', bd=10)
        title_frame.pack(fill='x', padx=10, pady=(10, 0))
        Label(title_frame, text="🐾 Vet Appointment 🐾", font=('Arial', 50, 'bold'),
                fg='black', bg="#33d6bb").pack(fill='x',pady=(20, 0))
            
        Button(title_frame, text="← Back to Main", font=("Arial", 12, "bold"), 
                                bg="#E74C3C", fg="white", command=self.leave_to_main).pack(side=RIGHT)
    
    def leave_to_main(self):
        # return to main screen
        if self.main_screen:
            self.root.destroy()
            self.main_screen.state('zoomed') 

    def main_frame(self):
        # Create main container frame
        main_frame = Frame(self.root, bg="#f2f7ff")
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.left_frame(main_frame)  # Create left sidebar
        self.center_frame(main_frame)  # Create center content area

    def left_frame(self, left_side):
        # Create left sidebar with navigation buttons
        left_frame = Frame(left_side, bg="#88efa7", width=100, relief='ridge', bd=10)
        left_frame.pack(side='left', fill='y')

        Button(left_frame, text="Add Appointment", font=('Arial', 12), 
               command=self.show_add_frame, bg="#109F47", fg='white',relief='groove', bd=10, 
               width=15, height=2).pack(pady=10, padx=10)
        Button(left_frame, text="View Appointments", font=('Arial', 12),
               command=self.show_view_frame, bg="#0AAB1C", fg='white',relief='groove', bd=10, 
               width=15, height=2).pack(pady=10, padx=10)

    def center_frame(self, center):
        # Create center content container
        self.center_container = Frame(center, bg="#53585f")
        self.center_container.pack(side='right', fill='both', expand=True)
        self.create_add_frame(self.center_container)  # Create add appointment frame
        self.create_view_frame(self.center_container)  # Create view appointments frame
        self.show_add_frame()  # Show add frame by default

    def show_add_frame(self):
        # Command to display the add appointment form
        if self.current_frame:
            self.current_frame.pack_forget()  # Hide current frame
        self.current_frame = self.frames["add"]  # Set current frame to add frame
        self.current_frame.pack(fill='both', expand=True)  # Show add frame
        self.customers = self.appointment_manager.load_customers()  # Load customer data
        customer_names = self.get_customer_names(self.customers)  # Format customer names
        self.customer_combo['values'] = customer_names  # Populate dropdown
        if customer_names:
            self.customer_var.set(customer_names[0])  # Set default selection

    def show_view_frame(self):
        # display the view appointments section
        if self.current_frame:
            self.current_frame.pack_forget()  # Hide current frame
        self.current_frame = self.frames["view"]  # Set current frame to view frame
        self.current_frame.pack(fill='both', expand=True)  # Show view frame
        self.refresh_view()  # Refresh appointment list

    def create_add_frame(self, parent):
        # Create add appointment form frame
        add_frame = Frame(parent, bg='white')
        self.frames["add"] = add_frame  # Store reference
        Label(add_frame, text="💉 Add Vet Appointment 💉", bg='white', font=('Arial', 25, "bold")).pack(pady=20)
        
        form_container = Frame(add_frame, bg='white')
        form_container.pack(pady=20, padx=50)
    
        # Create form fields
        self.create_form_field(form_container, "Select Customer:", self.create_customer_dropdown)
        self.create_form_field(form_container, "Date:", self.create_date_field)
        self.create_form_field(form_container, "Time:", self.create_time_field)
        self.create_form_field(form_container, "Context Number:", self.create_entry_field, "context")
        self.create_form_field(form_container, "Fee (RM):", self.create_entry_field, "fee")
        self.create_form_field(form_container, "Handler Person:", self.create_entry_field, "handler")

        # Save appointment button
        Button(add_frame, text="Save Appointment", font=('Arial', 12, 'bold'), bg='#3a8e7a', 
               fg='white', width=20, pady=8, command=self.save_new_appointment).pack(pady=30)
   
    def create_form_field(self, parent, label, create_func, var_name=None):
        # Helper method to create form field with label
        frame = Frame(parent, bg='white')
        frame.pack(fill='x', pady=12)
        Label(frame, text=label, font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        if var_name:
            create_func(frame, var_name)  # Create entry field
        else:
            create_func(frame)  # Create dropdown/date/time field

    def create_customer_dropdown(self, parent):
        # Create customer selection dropdown
        self.customers = self.appointment_manager.load_customers()  # Load customers
        customer_names = self.get_customer_names(self.customers)  # Format names
        self.customer_var = StringVar()  # Variable for selected customer
        self.customer_combo = ttk.Combobox(parent, textvariable=self.customer_var,
                                          font=('Arial', 12), width=28, state='readonly')
        self.customer_combo['values'] = customer_names  # Set dropdown options
        if customer_names:
            self.customer_var.set(customer_names[0])  # Set default selection
        self.customer_combo.grid(row=0, column=1, padx=10, pady=5)

    def create_date_field(self, parent):
        # Create date selection field with calendar button
        today = datetime.now()
        self.date_var = StringVar(value=today.strftime("%Y-%m-%d"))  # Set default to today
        Entry(parent, font=('Arial', 12), width=15, textvariable=self.date_var, 
              state='readonly').grid(row=0, column=1, padx=10, pady=5)
        # Calendar button 
        Button(parent, text="📅", font=('Arial', 12), bg="#87ffc7", fg='black', width=3,
               command=lambda: self.open_calendar(self.date_var)).grid(row=0, column=2, padx=10, pady=5)

    def create_time_field(self, parent):
        # Create time selection field with dropdowns
        time_input_frame = Frame(parent, bg='white')
        time_input_frame.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        today = datetime.now()
        self.hour_var = StringVar(value=f"{today.hour:02d}")  # Set default hour
        self.minute_var = StringVar(value="00")  # Set default minute
        # Create hour dropdown
        self.create_time_dropdown(time_input_frame, "Clock:", self.hour_var, 
                                 [f"{h:02d}" for h in range(8, 18)], side='left')
        # Create minute dropdown
        self.create_time_dropdown(time_input_frame, "Minute:", self.minute_var, 
                                 ["00", "15", "30", "45"], side='left', padx=10)

    def create_time_dropdown(self, parent, label, var, values, side, padx=2):
        # Helper method to create time dropdown
        frame = Frame(parent, bg='white')
        frame.pack(side=side, padx=padx)
        Label(frame, text=label, font=('Arial', 11), bg='white').pack(side='left', padx=(0, 5))
        ttk.Combobox(frame, textvariable=var, width=4, font=('Arial', 11), 
                    state='readonly', values=values).pack(side='left')

    def create_entry_field(self, parent, var_name):
        # Create text entry field based on field type
        if var_name == "context":
            self.Context_entry = Entry(parent, font=('Arial', 12), width=30)
            self.Context_entry.grid(row=0, column=1, padx=10, pady=5)
        elif var_name == "fee":
            self.fee_var = StringVar()
            self.Fee_entry = Entry(parent, font=('Arial', 12), width=30, textvariable=self.fee_var)
            self.Fee_entry.grid(row=0, column=1, padx=10, pady=5)
        elif var_name == "handler":
            self.Handler_entry = Entry(parent, font=('Arial', 12), width=30)
            self.Handler_entry.grid(row=0, column=1, padx=10, pady=5)

    def get_customer_names(self, customers):
        # load customer and return customer names to display
        return [f"😺{c['pet_name']} -👤{c['owner']}" + 
                (f" -🐾{c['breed']}" if c.get('breed') else "") for c in customers]

    def create_view_frame(self, parent):
        # Create view appointments frame with treeview
        view_frame = Frame(parent, bg='white')
        self.frames["view"] = view_frame  # Store reference
        Label(view_frame, text="📋 View Appointments 📋", bg='white', font=('Arial', 25, "bold")).pack(pady=20)
        tree_frame = Frame(view_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        cols = ("Pet", "Date", "Time", "Context", "Fee", "Handler")
        self.view_tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15, selectmode='extended')
        
        # Configure treeview columns
        for col, heading, width in [("Pet", "Pet Name", 150), ("Date", "Date", 120), 
                                    ("Time", "Time", 100), ("Context", "Context Number", 150), 
                                    ("Fee", "Fee (RM)", 100), ("Handler", "Handler Person", 150)]:
            self.view_tree.heading(col, text=heading, anchor='center')
            self.view_tree.column(col, width=width, anchor='center')
        self.view_tree.pack(fill='both', expand=True)
        
        # Action buttons
        btn_frame = Frame(view_frame, bg='white')
        btn_frame.pack(pady=10)
        for text, bg, cmd in [ ("Edit Appointment", '#f39c12', self.edit_appointment),
                              ("Refresh", '#3498db', self.refresh_view),
                              ("Delete Selected", '#e74c3c', self.delete_selected_appointments)]:
            Button(btn_frame, text=text, font=('Arial', 12), bg=bg, fg='white', 
                   width=15, height=2, command=cmd).pack(side='left', padx=10)

    def refresh_view(self):
        #refresh appointment list in treeview
        for row in self.view_tree.get_children():
            self.view_tree.delete(row)  # Clear existing rows
        
        data = self.appointment_manager.load_appointments()  # Load appointments
        data.sort(key=lambda x: (x["datetime"].split()[0], x["datetime"].split()[1]))  # Sort by date then time
        
        for check in data:
            date_part, time_part = check["datetime"].split() if " " in check["datetime"] else (check["datetime"], "")
            # Clean fee formatting
            fee_display = check.get("fee", "0.00").replace('RM', '').strip() if check.get("fee", "0.00").startswith('RM') else check.get("fee", "0.00")
            # Insert row into treeview
            self.view_tree.insert("", END, values=(check["pet"], date_part, time_part, 
                                                 str(check.get("phone", "")), fee_display, check["handler"]))

    def delete_selected_appointments(self):
        #  delete selected appointments
        selected = self.view_tree.selection()  # Get selected items
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment to delete.")
            return
        
        # Confirmation dialog
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected)} appointment(s)?"):
            return
        
        all_appointments = self.appointment_manager.load_appointments()  # Load all appointments
        if not all_appointments:
            messagebox.showwarning("Warning", "No appointments found.")
            return
        
        # Create IDs for selected appointments
        selected_ids = [f"{self.view_tree.item(item)['values'][0]}|{self.view_tree.item(item)['values'][1]}|{self.view_tree.item(item)['values'][2]}" 
                       for item in selected]
        
        # Filter out selected appointments
        new_appointments = [a for a in all_appointments 
                          if f"{a['pet']}|{a['datetime'].split()[0] if ' ' in a['datetime'] else a['datetime']}|{a['datetime'].split()[1] if ' ' in a['datetime'] else ''}" 
                          not in selected_ids]
        
        # Save updated list
        if self.appointment_manager.save_appointments(new_appointments):
            self.refresh_view()  # Refresh display
            messagebox.showinfo("Success", f"{len(selected)} appointment(s) deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete appointments from file.")

    def edit_appointment(self):
        # edit selected appointment
        selected = self.view_tree.selection()  # Get selected item
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment to edit.")
            return
        
        item = selected[0]  # Get first selected item
        values = self.view_tree.item(item)['values']  # Get appointment values
        
        # Open edit dialog with current values
        self.open_edit_dialog(values[0], values[1], values[2], values[3], values[4], values[5], item)

    def open_edit_dialog(self, pet, date, time, context, fee, handler, tree_item):
        # Create edit appointment dialog window
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Appointment")
        edit_window.geometry("500x600")
        edit_window.configure(bg='white')
        edit_window.transient(self.root)  # Make window modal
        edit_window.grab_set()  # Focus on this window
        
        Label(edit_window, text="Edit Appointment", font=('Arial', 24, 'bold'),
              bg='white', fg='#2c3e50').pack(pady=(20, 30))
        
        form_container = Frame(edit_window, bg='white')
        form_container.pack(expand=True, padx=40)
        
        # Create form variables with current values
        pet_var = StringVar(value=pet)
        date_var = StringVar(value=date)
        
        # Pet name field
        Label(form_container, text="Pet Name:", font=('Arial', 12, 'bold'),
              bg='white', anchor='w').grid(row=0, column=0, padx=(0, 10), pady=15, sticky='w')
        pet_entry = Entry(form_container, font=('Arial', 12), width=25, textvariable=pet_var)
        pet_entry.grid(row=0, column=1, pady=15, sticky='w')

        # Date field with calendar button
        date_frame = Frame(form_container, bg='white')
        date_frame.grid(row=1, column=0, columnspan=2, sticky='w', pady=15)
        Label(date_frame, text="Date:", font=('Arial', 12, 'bold'),
              bg='white', width=12, anchor='w').pack(side='left', padx=(0, 10))
        
        date_entry = Entry(date_frame, font=('Arial', 12), width=15,
                           textvariable=date_var, state='readonly')
        date_entry.pack(side='left', padx=(0, 10))
        
        Button(date_frame, text="📅", font=('Arial', 12), bg='#3498db', fg='white', width=3,
               command=lambda: self.open_calendar(date_var)).pack(side='left')
        
        # Time field with dropdowns
        time_frame = Frame(form_container, bg='white')
        time_frame.grid(row=2, column=0, columnspan=2, sticky='w', pady=15)
        Label(time_frame, text="Time:", font=('Arial', 12, 'bold'),
              bg='white', width=12, anchor='w').pack(side='left', padx=(0, 10))
        
        time_input_frame = Frame(time_frame, bg='white')
        time_input_frame.pack(side='left')
        
        # Hour dropdown
        hour_frame = Frame(time_input_frame, bg='white')
        hour_frame.pack(side='left', padx=2)
        Label(hour_frame, text="Hour:", font=('Arial', 11), bg='white').pack(side='left', padx=(0, 5))
        
        hour_str = time.split(":")[0] if ":" in time else "08"
        hour_var = StringVar(value=hour_str)
        hour_combo = ttk.Combobox(hour_frame, textvariable=hour_var,
                                  width=4, font=('Arial', 11), state='readonly')
        hour_combo['values'] = [f"{hour:02d}" for hour in range(8, 18)]
        hour_combo.pack(side='left')
        
        # Minute dropdown
        minute_frame = Frame(time_input_frame, bg='white')
        minute_frame.pack(side='left', padx=10)
        Label(minute_frame, text="Minute:", font=('Arial', 11), bg='white').pack(side='left', padx=(0, 5))
        
        minute_str = time.split(":")[1] if ":" in time else "00"
        minute_var = StringVar(value=minute_str)
        minute_combo = ttk.Combobox(minute_frame, textvariable=minute_var,
                                    width=4, font=('Arial', 11), state='readonly')
        minute_combo['values'] = ["00", "15", "30", "45"]
        minute_combo.pack(side='left')
        
        # Context Number field
        Label(form_container, text="Context Number:", font=('Arial', 12, 'bold'),
              bg='white', anchor='w').grid(row=3, column=0, padx=(0, 10), pady=15, sticky='w')
        context_var = StringVar(value=context)
        context_entry = Entry(form_container, font=('Arial', 12), width=25, textvariable=context_var)
        context_entry.grid(row=3, column=1, pady=15, sticky='w')
        
        # Fee field
        Label(form_container, text="Fee (RM):", font=('Arial', 12, 'bold'),
              bg='white', anchor='w').grid(row=4, column=0, padx=(0, 10), pady=15, sticky='w')
        fee_var = StringVar(value=fee)
        fee_entry = Entry(form_container, font=('Arial', 12), width=25, textvariable=fee_var)
        fee_entry.grid(row=4, column=1, pady=15, sticky='w')
        
        # Handler Person field
        Label(form_container, text="Handler Person:", font=('Arial', 12, 'bold'),
              bg='white', anchor='w').grid(row=5, column=0, padx=(0, 10), pady=15, sticky='w')
        handler_var = StringVar(value=handler)
        handler_entry = Entry(form_container, font=('Arial', 12), width=25, textvariable=handler_var)
        handler_entry.grid(row=5, column=1, pady=15, sticky='w')
        
        # Button frame
        button_frame = Frame(edit_window, bg='white')
        button_frame.pack(pady=30)
        
        def save_changes():
            #save edited appointment
            new_pet = pet_var.get().strip()
            new_date = date_var.get()
            new_time = f"{hour_var.get().zfill(2)}:{minute_var.get().zfill(2)}"
            new_context = context_var.get().strip()
            new_fee = fee_var.get().strip()
            new_handler = handler_var.get().strip()
            
            # Validation
            if not new_pet:
                messagebox.showerror("Error", "Pet name cannot be empty.")
                pet_entry.focus()
                return
            elif not new_date:
                messagebox.showerror("Error", "Please select a date.")
                return
            elif not self.is_future_datetime(new_date, new_time):
                messagebox.showerror("Error", "Appointment time must be in the future.")
                return
            elif not new_context:
                messagebox.showerror("Error", "Context number cannot be empty.")
                context_entry.focus()
                return
            elif not self.is_valid_phone(new_context):
                messagebox.showerror("Error", "Please enter a valid context number (012-3456789).")
                context_entry.focus()
                return
            elif not new_fee:
                messagebox.showerror("Error", "Fee cannot be empty.")
                fee_entry.focus()
                return
            elif not self.is_valid_fee(new_fee):
                messagebox.showerror("Error", "Please enter a valid fee (50.00).")
                fee_entry.focus()
                return
            elif not new_handler:
                messagebox.showerror("Error", "Handler person cannot be empty.")
                handler_entry.focus()
                return
            elif not self.is_valid_handler_name(new_handler):
                messagebox.showerror("Error", "Please enter a valid handler name.")
                handler_entry.focus()
                return
            
            # Format fee to 2 decimal places
            try:
                new_fee = f"{float(new_fee):.2f}"
            except:
                messagebox.showerror("Error", "Invalid fee amount.")
                fee_entry.focus()
                return
            
            # Check if anything changed
            if (new_pet, new_date, new_time, new_context, new_fee, new_handler) == (pet, date, time, context, fee, handler):
                messagebox.showinfo("Info", "No changes were made.")
                edit_window.destroy()
                return
            
            # Update appointment in file
            success = self.appointment_manager.update_appointment(
                pet, date, time, context, fee, handler,
                new_pet, new_date, new_time, new_context, new_fee, new_handler
            )
            if success:
                # Update treeview
                self.view_tree.item(tree_item, values=(new_pet, new_date, new_time, new_context, new_fee, new_handler))
                messagebox.showinfo("Success", "Appointment updated successfully!")
                edit_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to update appointment.")
        
        # Save Changes button 
        Button(button_frame, text="Save Changes", font=('Arial', 14, 'bold'), width=15,
               bg='#27ae60', fg='white', pady=8,
               activebackground='#219955', activeforeground='white',
               relief='raised', command=save_changes).pack(side='left', padx=10)
        
        # Cancel button 
        Button(button_frame, text="Cancel", font=('Arial', 14, 'bold'), width=15,
               bg='#95a5a6', fg='white', pady=8,
               activebackground='#7f8c8d', activeforeground='white',
               relief='raised', command=edit_window.destroy).pack(side='left', padx=10)

    def save_new_appointment(self):
        # save new appointment
        selected_customer = self.customer_var.get().strip()
        if not selected_customer:
            messagebox.showerror("Error", "Please select a customer from the dropdown.")
            return
        
        # Parse customer selection
        parts = selected_customer.split(" -👤")
        if len(parts) > 0:
            pet_name = parts[0].replace("😺", "").strip()
        else:
            messagebox.showerror("Error", "Please select a customer.")
            return
        
        # Get form values
        date_part, time_part = self.date_var.get(), self.get_selected_time()
        context, fee, handler = self.Context_entry.get().strip(), self.fee_var.get().strip(), self.Handler_entry.get().strip()
        
        # Validate form inputs using match
        errors = []
        match True:
            case _ if not pet_name:
                errors.append("Pet name cannot be empty.")
            case _ if not date_part:
                errors.append("Please select a date.")
            case _ if not self.is_future_datetime(date_part, time_part):
                errors.append("Appointment time must be in the future.")
            case _ if not context:
                errors.append("Context number cannot be empty.")
            case _ if not self.is_valid_phone(context):
                errors.append("Please enter a valid context number (012-3456789).")
            case _ if not fee:
                errors.append("Fee cannot be empty.")
            case _ if not self.is_valid_fee(fee):
                errors.append("Please enter a valid fee (50.00).")
            case _ if not handler:
                errors.append("Handler person cannot be empty.")
            case _ if not self.is_valid_handler_name(handler):
                errors.append("Please enter a valid handler name.")
                
        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return
        
        # Format fee
        try:
            fee = f"{float(fee):.2f}"
        except:
            messagebox.showerror("Error", "Invalid fee amount.")
            return

        # Save appointment to file
        if self.appointment_manager.add_appointment(pet_name, date_part, time_part, context, fee, handler):
            messagebox.showinfo("Success", "Appointment added and saved to data.txt!")
            # Reset form
            self.Context_entry.delete(0, END)
            self.fee_var.set("")
            self.Handler_entry.delete(0, END)
            # Set default to next hour
            next_hour = datetime.now() + timedelta(hours=1)
            self.date_var.set(next_hour.strftime("%Y-%m-%d"))
            self.hour_var.set(f"{next_hour.hour:02d}")
            self.minute_var.set("00")
            self.Context_entry.focus()
        else:
            messagebox.showerror("Error", "Failed to save appointment.")
   
    def is_future_datetime(self, date_str, time_str):
        # Validate that datetime is in the future
        try:
            return datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M") > datetime.now()
        except:
            return False
   
    def is_valid_fee(self, fee):
        # Validate fee format
        try:
            return fee.replace('.', '', 1).isdigit() and float(fee) >= 0
        except:
            return False
    
    def is_valid_phone(self, phone):
        # Validate phone number format
        cleaned = phone.replace(' ', '')
        if '-' not in cleaned or len(cleaned.split('-')) != 2:
            return False
        parts = cleaned.split('-')
        return (parts[0].isdigit() and parts[1].isdigit() and 
                len(parts[0]) + len(parts[1]) in [10, 11] and 
                parts[0].startswith('01'))
        
    def is_valid_handler_name(self, handler):
        # Validate handler name contains only letters and allowed characters
        cleaned = handler.strip()
        if not cleaned: return False
        return all(char.isalpha() or char in " -'" for char in cleaned)
   
    def get_selected_time(self):
        # Get formatted time from hour and minute variables
        return f"{self.hour_var.get().zfill(2)}:{self.minute_var.get().zfill(2)}"

    def open_calendar(self, date_var):
        # open calendar date picker
        top = Toplevel(self.root)
        top.title("Select Date")
        top.geometry("490x450")
        top.configure(bg='white')
        top.transient(self.root)
        top.grab_set()  # Make window modal
        
        current_year, current_month = datetime.now().year, datetime.now().month
        
        # Calendar header
        header = Frame(top, bg='#2c3e50', height=60)
        header.pack(fill='x')
        date_label = Label(header, text="", font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        date_label.pack(pady=10)
        
        # Calendar frames
        nav_frame, cal_frame, btn_frame = Frame(top, bg='white'), Frame(top, bg='white'), Frame(top, bg='white')
        nav_frame.pack(fill='x', pady=10), cal_frame.pack(fill='both', expand=True, padx=20, pady=10), btn_frame.pack(fill='x', pady=10)
    
        def show_calendar():
            # Display calendar for current month/year
            for widget in cal_frame.winfo_children():
                widget.destroy()  # Clear previous calendar
            
            date_label.config(text=f"{current_year}-{current_month:02d}")  # Update header
            
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
            # select date from calendar
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
            
            date_var.set(f"{selected_date.year}-{selected_date.month:02d}-{selected_date.day:02d}")  # Set date variable
            top.destroy()  # Close calendar
        
        def select_today():
            #select today's date
            date_var.set(datetime.now().strftime("%Y-%m-%d"))
            top.destroy()
        
        def prev_month():
            #navigate to previous month
            nonlocal current_month, current_year
            current_month = 12 if current_month == 1 else current_month - 1
            if current_month == 12: current_year -= 1
            show_calendar()  # Refresh calendar display
        
        def next_month():
            #navigate to next month
            nonlocal current_month, current_year
            current_month = 1 if current_month == 12 else current_month + 1
            if current_month == 1: current_year += 1
            show_calendar()  # Refresh calendar display
        
        # Navigation buttons
        Button(nav_frame, text="◀", font=('Arial', 12), width=5, command=prev_month).pack(side='left', padx=20)
        Button(nav_frame, text="▶", font=('Arial', 12), width=5, command=next_month).pack(side='right', padx=20)
        Button(btn_frame, text="Today", font=('Arial', 12), width=10, command=select_today).pack(side='left', padx=20)
        Button(btn_frame, text="Cancel", font=('Arial', 12), width=10, command=top.destroy).pack(side='right', padx=20)
        
        show_calendar()  # Initial calendar display

class AppointmentManager:
    def __init__(self, FILENAME="data.txt"):
        self.FILENAME = FILENAME  # Data file name

    def load_customers(self):
        # Load customer data from file
        customers = []
        if os.path.exists(self.FILENAME):
            with open(self.FILENAME, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('PET'):  # Identify customer records
                        parts = line.split('|')
                        if len(parts) >= 4:
                            customers.append({
                                'pet_name': parts[1],
                                'owner': parts[2],
                                'breed': parts[3] if len(parts) > 3 else 'Unknown'
                            })
        return customers

    def load_appointments(self):
        # Load appointment data from file
        appointments = []
        if not os.path.exists(self.FILENAME):
            return appointments
        
        with open(self.FILENAME, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = line.split("|")
                if len(parts) >= 7 and parts[0] == "VET":  # Identify appointment records
                    fee_value = parts[5].replace('RM', '').strip() if parts[5].startswith('RM') else parts[5]
                    appointments.append({
                        "pet": parts[1],
                        "datetime": f"{parts[2]} {parts[3]}",  # Combine date and time
                        "phone": parts[4],
                        "fee": fee_value,
                        "handler": parts[6]
                    })
        return appointments
   
    def add_appointment(self, pet, date_part, time_part, phone, fee, handler):
        # Add new appointment to file
        try:
            all_lines = []
            if os.path.exists(self.FILENAME):
                with open(self.FILENAME, "r", encoding='utf-8') as f:
                    all_lines = f.readlines()  # Read existing lines

            # Format fee with RM prefix
            fee_str = f"RM{fee}" if not fee.startswith('RM') else fee
            fee_str = fee_str.replace(' ', '')

            new_line = f"VET|{pet}|{date_part}|{time_part}|{phone}|{fee_str}|{handler}\n"
            
            with open(self.FILENAME, "w", encoding='utf-8') as f:
                # Write existing lines
                for line in all_lines:
                    f.write(line)
                # Append new appointment
                f.write(new_line)
            return True
        
        except Exception as e:
            print(f"Error adding appointment: {e}")
            return False
   
    def save_appointments(self, appointments):
        # Save appointment list to file
        try:
            other_lines = []
            if os.path.exists(self.FILENAME):
                with open(self.FILENAME, "r", encoding='utf-8') as f:
                    for line in f:
                        if not line.strip().startswith("VET|"):  # Keep non-appointment lines
                            other_lines.append(line)

            with open(self.FILENAME, "w", encoding='utf-8') as f:
                # Write non-appointment lines
                for line in other_lines:
                    f.write(line)

                # Write all appointments
                for a in appointments:
                    date_part, time_part = a["datetime"].split() if " " in a["datetime"] else (a["datetime"], "")
                    fee_value = f"RM{a.get('fee', '0.00')}" if not a.get('fee', '0.00').startswith('RM') else a.get('fee', '0.00')
                    fee_value = fee_value.replace(' ', '')
                    f.write(f"VET|{a['pet']}|{date_part}|{time_part}|{a.get('phone', '')}|{fee_value}|{a['handler']}\n")
            return True
        
        except Exception as e:
            print(f"Error saving appointments: {e}")
            return False
    
    def update_appointment(self, old_pet, old_date, old_time, old_phone, old_fee, old_handler,
                          new_pet, new_date, new_time, new_phone, new_fee, new_handler):
        # Update existing appointment in file
        if not os.path.exists(self.FILENAME):
            return False
        try:
            with open(self.FILENAME, "r", encoding='utf-8') as f:
                lines = f.readlines()  # Read all lines

            old_datetime, new_datetime = f"{old_date} {old_time}", f"{new_date} {new_time}"
            updated, new_lines = False, []

            for line in lines:
                line = line.strip()
                if not line:
                    new_lines.append(line + "\n")
                    continue
                parts = line.split("|")

                if len(parts) >= 7 and parts[0] == "VET":  # Check if appointment line
                    line_pet, line_datetime = parts[1], f"{parts[2]} {parts[3]}"
                    line_phone, line_fee, line_handler = parts[4], parts[5], parts[6] if len(parts) > 6 else ""
                    
                    # Clean fee formatting for comparison
                    line_fee_clean = line_fee.replace('RM', '').strip() if line_fee.startswith('RM') else line_fee
                    old_fee_clean = old_fee.replace('RM', '').strip() if old_fee.startswith('RM') else old_fee
                    try:
                        line_fee_num, old_fee_num = float(line_fee_clean), float(old_fee_clean)
                        line_fee_clean, old_fee_clean = f"{line_fee_num:.2f}", f"{old_fee_num:.2f}"
                    except: 
                        pass

                    # Check if this is the appointment to update
                    if (line_pet == old_pet and line_datetime == old_datetime and 
                        line_phone == str(old_phone) and line_fee_clean == old_fee_clean and line_handler == old_handler):
                        # Replace with updated appointment
                        fee_with_prefix = f"RM{new_fee}" if not new_fee.startswith('RM') else new_fee
                        fee_with_prefix = fee_with_prefix.replace(' ', '')
                        new_lines.append(f"VET|{new_pet}|{new_date}|{new_time}|{new_phone}|{fee_with_prefix}|{new_handler}\n")
                        updated = True
                    else:
                        new_lines.append(line + "\n")
                else:
                    new_lines.append(line + "\n")
            
            if updated:
                # Write updated lines to file
                with open(self.FILENAME, "w", encoding='utf-8') as f:
                    f.writelines(new_lines)
                return True
            return False
        except Exception as e:
            print(f"Failed to update: {e}")
            return False

if __name__ == "__main__":
    root = Tk()  # Create main window
    app = vet_app(root)  # Create application
    root.mainloop()  # Start event loop