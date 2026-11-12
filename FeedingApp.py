from tkinter import * #tk
from tkinter import ttk, messagebox #tk
from datetime import datetime, timedelta #for date
import os, calendar #calender

class FeedingApp:
    def __init__(self, root, main_screen=None): 
        #feeding application
        self.root, self.main_screen = root, main_screen  # Store references
        self.root.title("🐾 Pet Feeding Tracker 🐾")  # Set window title
        self.root.state('zoomed')  # Maximize window
        self.root.configure(bg="#A4C9ED")  # Set background color
        self.feeding_manager = FeedingManager()  # Create feeding manager
        self.UI()  # Build user interface

    def UI(self):
        #  Build the main user interface
        self.title()  # Create title section
        self.main_container()  # Create main container

    def title(self):
        #  Create the title bar with back button
        title_frame = Frame(self.root, bg="#b5d2eb", height=100,relief='ridge', bd=10) #Color UI
        title_frame.pack(fill='x', padx=10, pady=(10, 0)) #saiz and x,y
        #Label the title
        Label(title_frame, text="🐾 Pet Feeding Tracker 🐾", font=('Arial', 50, 'bold'),
                        fg='black', bg="#b1d0ea").pack(fill='x',pady=(20, 0))
                    
        # Back to main screen 
        Button(title_frame, text="← Back to Main", font=("Arial", 12, "bold"), 
                                        bg="#E74C3C", fg="white", command=self.leave_to_main).pack(side=RIGHT)
            
    def leave_to_main(self):
        #  Return to the main application screen
        if self.main_screen:
            self.root.destroy()  # Close current window
            self.main_screen.state('zoomed')  # Restore main window

    def main_container(self):
        #  Create the main container frame
        self.main_container_frame = Frame(self.root, bg='white') # set background
        self.main_container_frame.pack(fill='both', expand=True, padx=(10,20), pady=20) # set x,y
        self.Left_container()  # Create left sidebar
        self.show_add_record()  # Show add record form by default

    def Left_container(self):
        # Create the left sidebar with navigation buttons
        left_frame = Frame(self.main_container_frame, bg="#A6DCEA", width=10, relief='ridge', bd=10)
        left_frame.pack(side='left', fill='y') # set x,y
        
        # Navigation buttons with their
        for text, color, cmd in [("Add Record", "#399ce7", self.show_add_record), 
                                 ("Check Records", "#2688C1", self.show_check_records)]:
            Button(left_frame, text=text, width=15, height=2, font=('Arial', 11, 'bold'),relief='groove', bd=10, 
                   bg=color, fg='white', command=cmd).pack(pady=10, padx=10) # for all the button(Add Record,Check Records)
    
    def clear_main_frame(self):
        #  Clear all widgets from the main frame except sidebar
        for widget in self.main_container_frame.winfo_children()[1:]:
            widget.destroy()

    def show_add_record(self):
        #  Display the add record form
        self.clear_main_frame()
        self.create_add_record_form()
    
    def show_check_records(self):
        #  Display the check records section
        self.clear_main_frame()
        self.create_check_records_frame()

    def create_add_record_form(self):
        # Create the form for adding feeding records
        right_frame = Frame(self.main_container_frame, bg='white') 
        right_frame.pack(side='left', expand=True)
        # Label the small title add feeding record and design
        Label(right_frame, text="🦴 Add Feeding Record 🦴", font=('Arial', 28, 'bold'), 
              bg='white', fg='#2c3e50').pack(pady=(0,30))
        
        form_container = Frame(right_frame, bg='white')
        form_container.pack() #create and run
        self.create_form_fields(form_container)  # Create form fields

        # Save record button
        Button(right_frame, text="Save Record", font=('Arial', 14, 'bold'), width=20,
               bg='#27ae60', fg='white', pady=8, command=self.add_record).pack(pady=40)

    def create_form_fields(self, parent):
        # Create all form fields for adding records
        today = datetime.now()
        
        # Customer selection dropdown
        Label(parent, text="Customer:", font=('Arial', 12, 'bold'), 
              bg='white').grid(row=0, column=0, padx=(100, 10), pady=15, sticky='w')
        self.customer_var = StringVar() # Value holder for strings variables.
        self.customer_combo = ttk.Combobox(parent, textvariable=self.customer_var, 
                                          width=23, font=('Arial', 12), state='readonly')
        self.customer_combo.grid(row=0, column=1, padx=10, pady=15, sticky='w')  # set row and the pleace
        self.load_customers()  # Load customers into dropdown
        
        # Date selection field with calendar button
        date_frame = Frame(parent, bg='white')
        # set row and the pleace
        date_frame.grid(row=1, column=0, columnspan=2, sticky='w', pady=15, padx=(100, 0))
        
        #Label the date and setting the design
        Label(date_frame, text="Date:", font=('Arial', 12, 'bold'), 
              bg='white', width=12).pack(side='left', padx=(0, 10))
        # set the format
        self.date_var = StringVar(value=today.strftime("%Y-%m-%d"))
        # use entry for date to input
        Entry(date_frame, font=('Arial', 12), width=15, 
              textvariable=self.date_var, state='readonly').pack(side='left', padx=(0, 10))
        # Calendar button 
        Button(date_frame, text="📅", font=('Arial', 12), bg='#A5CAD4', fg='black', width=3,
               command=lambda: self.open_calendar(self.date_var)).pack(side='left')
        
        # Create morning and evening time dropdowns
        self.create_time_combos(parent, "Morning Time:", 2, 1, 16)
        self.create_time_combos(parent, "Evening Time:", 3, 16, 24  , True)
        
        # Food and Worker entry fields
        for i, (label, var_name) in enumerate([("Food:", "Food_entry"), ("Worker:", "Worker_entry")], 4):
            #Label the Food and Worker
            Label(parent, text=label, font=('Arial', 12, 'bold'), 
                  bg='white').grid(row=i, column=0, padx=(100, 10), pady=15, sticky='w')
            # use entry for food and worker to input
            entry = Entry(parent, font=('Arial', 12), width=25)
            entry.grid(row=i, column=1, padx=10, pady=15, sticky='w') #set row
            setattr(self, var_name, entry)  # Store reference to entry widget

    # def for create time combos
    def create_time_combos(self, parent, label_text, row, start_hour, end_hour, include_midnight=False):
        #  Create time selection dropdowns for morning/evening feeding
        time_frame = Frame(parent, bg='white')
        time_frame.grid(row=row, column=0, columnspan=2, sticky='w', pady=15, padx=(100, 0)) # setting the row and pleace
        #Lebal the time o select
        Label(time_frame, text=label_text, font=('Arial', 12, 'bold'), 
              bg='white').pack(side='left', padx=(0, 10))
        
        # Generate time options
        times = []
        # setting the time in 30min
        for hour in range(start_hour, end_hour):
            for minute in [0, 30]:
                if hour == 15 and minute == 30:  # Skip 15:30
                    break
                # append and set format in 00.00
                times.append(f"{hour:02d}:{minute:02d}")
        
        if include_midnight:
            times.extend(["00:00", "00:30"])  # Add midnight times
        
        time_var = StringVar()
        # combines a text field with a pop-down list of values.
        time_combo = ttk.Combobox(time_frame, textvariable=time_var, 
                                  width=8, font=('Arial', 11), state='readonly')
        time_combo['values'] = times 
        time_combo.pack(side='left') # side is left
        
        # Store references based on label
        if "Morning" in label_text:
            self.morning_time_var, self.morning_time_combo = time_var, time_combo # make the morning time
        else:
            self.evening_time_var, self.evening_time_combo = time_var, time_combo # else use evening time

    def create_check_records_frame(self):
        # Create the frame for viewing and managing records
        check_frame = Frame(self.main_container_frame, bg='white') # Framee gui fo background
        check_frame.pack(side='left', fill='both', expand=True, padx=20, pady=20) # setting e pleace 
        # setting and label for the small title Check Feeding Records
        Label(check_frame, text="📋 Check Feeding Records 📋", 
              font=("Arial", 28, 'bold'), bg='white', fg='#2c3e50').pack(pady=(0, 20)) # setting design
        
        # Treeview for displaying records
        tree_frame = Frame(check_frame, bg='white')
        tree_frame.pack(fill='both', expand=True)
        # Treeview for displaying records
        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # ttk.Treeviw to set the colunm and add te colunm
        self.tree = ttk.Treeview(tree_frame, columns=("Pet", "Date", "Time", "Food", "Worker"),
                                 show="headings", height=20, yscrollcommand=scrollbar.set,
                                 selectmode='extended')
        scrollbar.config(command=self.tree.yview) # run
        
        # Configure treeview columns
        # For the column and setting the saiz
        for col, heading, width in [("Pet", "Pet Name", 150), ("Date", "Date", 120), 
                                    ("Time", "Time", 100), ("Food", "Food", 250), 
                                    ("Worker", "Worker", 150)]: 
            self.tree.heading(col, text=heading, anchor='center') # sub the small small title like key
            self.tree.column(col, width=width, anchor='center') #setting the value
        
        self.tree.pack(fill='both', expand=True) #set place
        
        # Action buttons
        btn_container = Frame(check_frame, bg='white') # backgrund color
        btn_container.pack(pady=10)# Load records initially
        
        # Button for record management
        for text, bg, cmd in [("Edit Record", '#f39c12', self.edit_record),# color and func
                              ("Refresh", '#3498db', self.refresh_records),# color func
                              ("Delete Selected", '#e74c3c', self.delete_selected)]:# color func
            # create the button and set design
            Button(btn_container, text=text, font=('Arial', 12, 'bold'), width=15, height=2,
                   bg=bg, fg='white', command=cmd).pack(side='left', padx=10)
        self.refresh_records() # Load records initially

    def validate_record_inputs(self, pet, date, morning_time, evening_time, food, worker, validate_times=True):
        # Validate all input fields for feeding records
        errors = []
        
        # Validate individual fields using match
        match True:
            case _ if not pet or pet == "No customers found":
                errors.append("Please select a customer.") # display for error customer are nothing
            case _ if not date:
                errors.append("Please select a date.") # display for error date are nothing
            case _ if not morning_time and not evening_time:
                errors.append("Please select at least one feeding time.") # display for error time are nothing
            case _ if not food:
                errors.append("Food name cannot be empty.") # display for error food are nothing
            case _ if not worker:
                errors.append("Worker name cannot be empty.") # display for error worker are nothing
            case _ if not self.is_valid_worker_name(worker):
                errors.append("Please enter a valid worker name.") # display for error worker

        if validate_times and (morning_time or evening_time):
            for t in [t for t in [morning_time, evening_time] if t]:
                if not self.is_future_datetime(date, t):
                    errors.append("All feeding times must be in the future.")
                    break
        return errors

    def is_future_datetime(self, date_str, time_str):
        # Check if datetime is in the future
        try:
            return datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M") > datetime.now()# the function of time and testing
        except:
            return False
        
    def is_valid_worker_name(self, worker):
        #  Validate worker name format
        cleaned = worker.strip()
        if not cleaned: return False
        return all(char.isalpha() or char in " -'" for char in cleaned)

    def add_record(self):
        #  Save a new feeding record
        pet = self.get_selected_customer_pet_name() # get for input in pet
        date = self.date_var.get()# get for input in date
        morning_time, evening_time = self.morning_time_var.get(), self.evening_time_var.get() # get for input in time
        food, worker = self.Food_entry.get().strip(), self.Worker_entry.get().strip() # get for input in food and worker

        # Validate inputs
        errors = self.validate_record_inputs(pet, date, morning_time, evening_time, food, worker)
        if errors:
            messagebox.showerror("Error", errors[0]) # turn to messagebox to output error
            return
        
        # Format time string
        time = f"{morning_time}/{evening_time}" if morning_time and evening_time else morning_time or evening_time
        # setting the output if they are success
        if self.feeding_manager.add_record(pet, date, time, food, worker):
            messagebox.showinfo("Success", f"Feeding record added for {pet}!") # from messagebox to show the success message
            self.clear_form_fields()  # Reset form
        else:
            messagebox.showerror("Error", "Failed to save record to file.") # from messagebox to show the error message

    def edit_record(self):
        # Edit selected feeding record
        if not hasattr(self, 'tree'): return       
        selected = self.tree.selection() #use the record are select
        if not selected:
            messagebox.showerror("Error", "Please select a record to edit.") # show error are select record before edit
            return   
        if len(selected) > 1:
            messagebox.showerror("Error", "Please select only one record to edit.") #show error are just can select one record
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        self.open_edit_record_dialog(*values, item)  # Open edit dialog

    def open_edit_record_dialog(self, pet, date, time, food, worker, tree_item):
        # Open dialog for editing a record
        self.edit_top = Toplevel(self.root)
        self.edit_top.title("Edit Record") # setting the title
        self.edit_top.geometry("500x650") # setting the saiz
        self.edit_top.configure(bg='white') # setting the background
        self.edit_top.transient(self.root) # setting the stored
        self.edit_top.grab_set()  # Make modal
        self.edit_old_values = (pet, date, time, food, worker)  # Store old values
        self.edit_tree_item = tree_item  # Store tree item reference
        self.create_edit_dialog_ui()  # Create edit UI

    def create_edit_dialog_ui(self):
        # Create UI for edit dialog
        Label(self.edit_top, text="Edit Feeding Record", # setting the edit title
              font=('Arial', 24, 'bold'), bg='white', fg='#2c3e50').pack(pady=(20, 30)) # setting the design 
        # frame design
        form_container = Frame(self.edit_top, bg='white')
        form_container.pack(expand=True, padx=40)
        
        # Customer selection for edit
        Label(form_container, text="Select Customer:", font=('Arial', 12, 'bold'), # setting the edit title
              bg='white').grid(row=0, column=0, padx=(0, 10), pady=15, sticky='w') # setting the row and design
        self.edit_customer_var = StringVar() # selection edit
        # setting the design 
        self.edit_customer_combo = ttk.Combobox(form_container, textvariable=self.edit_customer_var, 
                                                width=23, font=('Arial', 12), state='readonly')
        self.edit_customer_combo.grid(row=0, column=1, pady=15, sticky='w')# row and place
        self.load_info_customers(self.edit_old_values[0])  # Load with current pet
        
        # Date selection for edit
        date_frame = Frame(form_container, bg='white')
        date_frame.grid(row=1, column=0, columnspan=2, sticky='w', pady=15) # frame design
         # Label the date and design color,text...
        Label(date_frame, text="Date:", font=('Arial', 12, 'bold'), 
              bg='white', width=12).pack(side='left', padx=(0, 10))
        
        self.edit_date_var = StringVar(value=self.edit_old_values[1])
        #Entry the date
        Entry(date_frame, font=('Arial', 12), width=15, 
              textvariable=self.edit_date_var, state='readonly').pack(side='left', padx=(0, 10))   
            # Make a button to click the calender and design
        Button(date_frame, text="📅", font=('Arial', 12), bg='#3498db', fg='white', width=3,
               command=lambda: self.open_calendar(self.edit_date_var)).pack(side='left')
        
        # Time selection parsing for edit
        existing_times = self.edit_old_values[2].split("/") if "/" in self.edit_old_values[2] else [self.edit_old_values[2]]
        existing_morning_time = existing_evening_time = "" # format
        
        # testing existing times
        for t in existing_times:
            try:
                hour = int(t.split(":")[0])
                if 1 <= hour <= 15:
                    existing_morning_time = t
                elif hour >= 16 or hour == 0:
                    existing_evening_time = t
            except: pass
        
        # Create time dropdowns for edit
        self.create_edit_time_combos(form_container, "Morning Time:", 2, 1, 16, existing_morning_time)
        self.create_edit_time_combos(form_container, "Evening Time:", 3, 16, 24, existing_evening_time, True)
        
        # Food and Worker fields for edit
        for i, (label, value, var_name) in enumerate([("Food:", self.edit_old_values[3], "edit_food_var"), # setting and add
                                                      ("Worker:", self.edit_old_values[4], "edit_worker_var")], 4): # setting and add
            # Label the text for food and worker
            Label(form_container, text=label, font=('Arial', 12, 'bold'), 
                  bg='white').grid(row=i, column=0, padx=(0, 10), pady=15, sticky='w') # design
            var = StringVar(value=value)
            # Entry the label and row to show
            Entry(form_container, font=('Arial', 12), width=25, 
                  textvariable=var).grid(row=i, column=1, pady=15, sticky='w')
            setattr(self, var_name, var)  # Store variable reference
        
        # Edit dialog buttons
        button_frame = Frame(self.edit_top, bg='white') # background edit
        button_frame.pack(pady=30) # up side down
        Button(button_frame, text="Save Changes", font=('Arial', 14, 'bold'), width=15, # Save Changes button
               bg='#27ae60', fg='white', pady=8, command=self.save_edit_changes).pack(side='left', padx=10) 
        Button(button_frame, text="Cancel", font=('Arial', 14, 'bold'), width=15,
               bg='#95a5a6', fg='white', pady=8, command=self.edit_top.destroy).pack(side='left', padx=10) # cancle button
    
    def create_edit_time_combos(self, parent, label_text, row, start_hour, end_hour, default_value, include_midnight=False):
        # Create time dropdowns for edit dialog
        time_frame = Frame(parent, bg='white')
        time_frame.grid(row=row, column=0, columnspan=2, sticky='w', pady=15)
        
        Label(time_frame, text=label_text, font=('Arial', 12, 'bold'), 
              bg='white').pack(side='left', padx=(0, 10))
        
        # Generate time options
        times = []
        for hour in range(start_hour, end_hour):
            for minute in [0, 30]:
                if hour == 15 and minute == 30:
                    break
                times.append(f"{hour:02d}:{minute:02d}") # format in 00.00
        
        if include_midnight:
            times.extend(["00:00", "00:30"])
        
        # Create appropriate dropdown based on label
        if "Morning" in label_text:
            self.edit_morning_time_var = StringVar(value=default_value)
            self.edit_morning_time_combo = ttk.Combobox(time_frame, textvariable=self.edit_morning_time_var, 
                                                        width=8, font=('Arial', 11), state='readonly')
            self.edit_morning_time_combo['values'] = times
            self.edit_morning_time_combo.pack(side='left')
        else:
            self.edit_evening_time_var = StringVar(value=default_value)
            self.edit_evening_time_combo = ttk.Combobox(time_frame, textvariable=self.edit_evening_time_var, 
                                                        width=8, font=('Arial', 11), state='readonly')
            self.edit_evening_time_combo['values'] = times
            self.edit_evening_time_combo.pack(side='left')
    
    def load_info_customers(self, current_pet):
        #Load customers into edit dropdown with current selection
        customers, selected_customer = [], []
        
        if os.path.exists(self.feeding_manager.filename):
            with open(self.feeding_manager.filename, 'r', encoding='utf-8') as file: # open file
                for line in file:
                    line = line.strip()
                    if line.startswith('PET'): #set the file in pet
                        parts = line.split('|') # make space and next
                        if len(parts) >= 4:
                            pet_name, owner, breed = parts[1], parts[2], parts[3] if len(parts) > 3 else "Unknown"
                            customer_str = f"😺{pet_name} -👤{owner} -🐾{breed}" # select customer in function output
                            customers.append(customer_str)
                            if pet_name == current_pet:
                                selected_customer = customer_str
        
        # Set dropdown values
        if customers:
            self.edit_customer_combo['values'] = customers
            self.edit_customer_combo.set(selected_customer or customers[0])
        else:
            self.edit_customer_combo['values'] = ["No customers found"]
            self.edit_customer_combo.set("No customers found") #output if dont have any customer
    
    def get_customer_info(self):
        #detect customer from load customer and return customer names to display
        selected = self.edit_customer_var.get()
        if selected and " -👤" in selected:
            return selected.split(" -👤")[0].replace("😺", "").strip()
        return ""
    
    def save_edit_changes(self):
        # Save edited record changes
        selected_customer = self.edit_customer_var.get()
        if not selected_customer or selected_customer == "No customers found":
            messagebox.showerror("Error", "Please select a customer.") # output error in select customer
            return
        
        pet = self.get_customer_info() # get pet
        date = self.edit_date_var.get() # get date
        time = self.get_edit_selected_time() # get time
        food = self.edit_food_var.get().strip() # get food
        worker = self.edit_worker_var.get().strip() # get worker
        morning_time = getattr(self, 'edit_morning_time_var', StringVar()).get() # get morning
        evening_time = getattr(self, 'edit_evening_time_var', StringVar()).get() # get evening

        # Validate inputs
        errors = self.validate_record_inputs(pet, date, morning_time, evening_time, food, worker, False)
        if errors:
            messagebox.showerror("Error", errors[0]) # feedback error
            return
    
        # Check if anything changed
        if (pet, date, time, food, worker) == self.edit_old_values:
            messagebox.showinfo("Info", "No changes were made.") # if nothing change feedback
            self.edit_top.destroy()
            return

        # Update record in data file
        success = self.update_record_in_data(*self.edit_old_values, pet, date, time, food, worker)
        
        if success:
            self.update_record_in_tree(self.edit_tree_item, pet, date, time, food, worker)
            messagebox.showinfo("Success", "Record updated successfully!") # feedback success edit
            self.edit_top.destroy()
        else:
            messagebox.showerror("Error", "Failed to update record.") # error output

    def get_edit_selected_time(self):
        # Get formatted time string from edit time selections
        morning_time = getattr(self, 'edit_morning_time_var', StringVar()).get()
        evening_time = getattr(self, 'edit_evening_time_var', StringVar()).get()
        
        if morning_time and evening_time:
            return f"{morning_time}/{evening_time}"
        return morning_time or evening_time or ""

    def refresh_records(self):
        # Refresh and reload all records in treeview
        if hasattr(self, 'tree'):
            self.tree.delete(*self.tree.get_children()) 
             # Clear existing

        records = self.get_all_records_sorted()
        # Insert sorted records
        for rec in records:
            self.tree.insert("", END, values=(rec["pet"], rec["date"], rec["time"], rec["food"], rec['Worker']))

    def delete_selected(self):
        # Delete selected records
        if not hasattr(self, 'tree'): 
            return
            
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No records selected.")
            return
        
        # Confirmation 
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected)} record(s)?"):
            return

        # Collect selected records
        selected_records = []
        for item in selected:
            values = self.tree.item(item)['values']
            # set the values and key to chooose
            selected_records.append({
                'pet': values[0], 'date': values[1], 'time': values[2], 
                'food': values[3], 'Worker': values[4]
            })
        
        # Group records by pet for efficient deletion
        pet_records = {}
        for rec in selected_records:
            pet = rec['pet']
            if pet not in pet_records:
                all_pet_records = self.feeding_manager.get_pet_records(pet)
                pet_records[pet] = {'records': all_pet_records, 'delete': []}
            # Find indices of matching records
            for i, pet_rec in enumerate(pet_records[pet]['records']):
                if (pet_rec['date'] == rec['date'] and pet_rec['time'] == rec['time'] and 
                    pet_rec['food'] == rec['food'] and pet_rec['Worker'] == rec['Worker']):
                    pet_records[pet]['delete'].append(i)

        # Delete records from each pet
        success = True
        for pet, data in pet_records.items():
            if data['delete']:
                if not self.feeding_manager.delete_records(pet, data['delete']):
                    success = False 
        
        if success:
            messagebox.showinfo("Success", f"Successfully deleted {len(selected)} record(s).") # delete display
            self.refresh_records()  # Refresh display
        else:
            messagebox.showerror("Error", "Failed to delete records.") # error delete display

    def update_record_in_tree(self, item, pet, date, time, food, worker):
        # Update a record in the treeview
        self.tree.item(item, values=(pet, date, time, food, worker))
        
    def update_record_in_data(self, old_pet, old_date, old_time, old_food, old_worker,
                            new_pet, new_date, new_time, new_food, new_worker):
        #  Update record in the feeding manager data
        # Remove old record
        if old_pet in self.feeding_manager.feeding_log:
            # scan the record are old
            for i, record in enumerate(self.feeding_manager.feeding_log[old_pet]):
                if (record["date"] == old_date and record["time"] == old_time and 
                    record["food"] == old_food and record["Worker"] == old_worker):
                    self.feeding_manager.feeding_log[old_pet].pop(i)
                    # Clean up empty pet entries
                    if old_pet != new_pet and not self.feeding_manager.feeding_log[old_pet]:
                        del self.feeding_manager.feeding_log[old_pet]
                    break

        # Add new record
        if new_pet not in self.feeding_manager.feeding_log:
            self.feeding_manager.feeding_log[new_pet] = []
        # new one record 
        self.feeding_manager.feeding_log[new_pet].append({
            "date": new_date, "time": new_time, "food": new_food, "Worker": new_worker
        })
        return self.feeding_manager.save_to_file()  # Save to file

    def get_all_records_sorted(self):
        # Get all records sorted by date and time
        all_records = []
        for pet, records in self.feeding_manager.feeding_log.items():
            for rec in records:
                # apend record
                all_records.append({
                    "pet": pet, "date": rec["date"], "time": rec["time"], 
                    "food": rec["food"], "Worker": rec["Worker"]
                })
        all_records.sort(key=lambda x: (x["date"], x["time"]), reverse=True)
        return all_records

    def get_selected_date(self):
        #Get the currently selected date
        return self.date_var.get()
    
    def get_selected_customer_pet_name(self):
        # Extract pet name from customer selection
        selected = self.customer_var.get()
        if selected and " -👤" in selected:
            return selected.split(" -👤")[0].replace("😺", "").strip()
        return ""

    def open_calendar(self, date_var):
        # Open calendar date picker
        top = Toplevel(self.root)
        top.title("Select Date") # calender top title
        top.geometry("490x450") # calender saiz
        top.configure(bg='white') # calender backgrund
        top.transient(self.root) 
        top.grab_set()  # Make modal
        
        current_year, current_month = datetime.now().year, datetime.now().month
        
        # Calendar UI components
        # design and place
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
            for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]): # make the day
                Label(cal_frame, text=day, font=('Arial', 10, 'bold'), bg='white', fg='#2c3e50', width=6).grid(row=0, column=i, padx=2, pady=2)
            
            cal, today = calendar.monthcalendar(current_year, current_month), datetime.now() # detect date now
            week_num = 0 
            #week number and day
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
            while selected_date < today: #date must in future
                selected_date += timedelta(days=1)
                days_added += 1
            
            if days_added > 0:
                messagebox.showinfo("Date Adjusted", 
                                f"Selected date was in the past.\n" 
                                f"Automatically adjusted to {selected_date.strftime('%Y-%m-%d')}") # format for date
            
            date_var.set(f"{selected_date.year}-{selected_date.month:02d}-{selected_date.day:02d}") # format for date
            top.destroy()
        
        def select_today():
            #Select today's date
            date_var.set(datetime.now().strftime("%Y-%m-%d")) # format for date
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

    def clear_form_fields(self):
        # Clear all form fields
        self.Food_entry.delete(0, END)
        self.Worker_entry.delete(0, END)
        next_hour = datetime.now() + timedelta(hours=1)
        self.date_var.set(next_hour.strftime("%Y-%m-%d")) # format for date
        self.morning_time_var.set("")
        self.evening_time_var.set("")
        self.customer_combo.focus()  # Focus on customer dropdown

    def load_customers(self):
        # Load customers from data file into and disply to select customer
        customers = []
        if os.path.exists(self.feeding_manager.filename):
            with open(self.feeding_manager.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('PET'):
                        parts = line.split('|')
                        if len(parts) >= 4:
                            pet_name, owner, breed = parts[1], parts[2], parts[3] if len(parts) > 3 else "Unknown" # setting the file must have data to save
                            customers.append(f"😺{pet_name} -👤{owner} -🐾{breed}") # func the customer
        
        if customers:
            self.customer_combo['values'] = customers
            self.customer_combo.set(customers[0])
        else:
            self.customer_combo['values'] = ["No customers found"] #display error
            self.customer_combo.set("No customers found")

# file
class FeedingManager:
    def __init__(self, filename="data.txt"):
        # Initialize feeding manager with data file
        self.filename = filename
        self.feeding_log = {}  # Dictionary to store feeding records
        self.load_from_file()  # Load existing data
    
    def load_from_file(self):
        # Load feeding records from data file
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, 'r', encoding='utf-8') as file: # open file
                for line in file:
                    line = line.strip()
                    if line.startswith("FEEDING|"):  # Identify feeding records
                        parts = line.split("|")
                        if len(parts) >= 6:
                            pet, date, time, food, worker = parts[1], parts[2], parts[3], parts[4], parts[5]
                            if pet not in self.feeding_log:
                                self.feeding_log[pet] = []
                            self.feeding_log[pet].append({
                                "date": date, "time": time, "food": food, "Worker": worker # add record
                            })
        except Exception as e:
            print(f"Error loading file {self.filename}: {e}") # if not is error file and save
    
    def save_to_file(self):
        # Save feeding records to data file
        try:
            all_lines = []
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file: # open file
                    all_lines = file.readlines()
            
            # Keep non-feeding data
            other_data = [line for line in all_lines if line.strip() and not line.strip().startswith("FEEDING|")] # seting the opening is topic feeding
            
            with open(self.filename, 'w', encoding='utf-8') as file:
                file.writelines(other_data)  # Write other data
                # Write all feeding records
                for pet, records in self.feeding_log.items():
                    for record in records:
                        file.write(f"FEEDING|{pet}|{record['date']}|{record['time']}|{record['food']}|{record['Worker']}\n") # write the all value anad key to record to save
            return True
        except Exception as e:
            print(f"Error saving file {self.filename}: {e}") # else error save
            return False
    
    def add_record(self, pet, date, time, food, worker):
        # Add a new feeding record
        if pet not in self.feeding_log:
            self.feeding_log[pet] = []
        self.feeding_log[pet].append({
            "date": date, "time": time, "food": food, "Worker": worker
        })
        return self.save_to_file()  # Save to file
    
    def delete_records(self, pet, indices):
        # Delete records by indices for a specific pet
        if pet not in self.feeding_log:
            return False
        indices.sort(reverse=True)  # Sort descending to avoid index issues
        for i in indices:
            if i < len(self.feeding_log[pet]):
                self.feeding_log[pet].pop(i)
        # Clean up if no records left for pet
        if not self.feeding_log[pet]:
            del self.feeding_log[pet]
        return self.save_to_file()
    
    def get_pet_records(self, pet):
        #  Get all records for a specific pet
        return self.feeding_log.get(pet, [])

if __name__ == "__main__":
    root = Tk()  # Create main window
    app = FeedingApp(root)  # Create feeding application
    root.mainloop()