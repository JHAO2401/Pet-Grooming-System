from tkinter import *
from tkinter import ttk, messagebox
import os
from datetime import datetime

class PetExpenseTracker:
    def __init__(self, screen, main_screen=None):
        #PetExpenseTracker application
        self._screen = screen
        self._main_screen = main_screen
        self._screen.title("💵 Pet Expense Tracker 💵")  # Set window title
        self._screen.state('zoomed')  # Maximize window
        self._screen.configure(bg="#54216C") # Set background color
        self._data_file = "data.txt"  # Data file name
        self._file_manager = FileManager(self._data_file)  # Create file manager
        self.UI()  # Build user interface

    def UI(self):
        #Create the main user interface
        self._create_title()  # Create title section
        self._main_container()  # Create main container

    def _create_title(self):
        #Create the application title bar with back button
        title_frame = Frame(self._screen, bg="#271738", height=100,relief='ridge', bd=10)
        title_frame.pack(fill='x', padx=10, pady=(10, 0))
        Label(title_frame, text="🐾Pet Expense Tracker🐾", font=('Arial', 50, 'bold'),
                        fg='white', bg="#271738").pack(fill='x',pady=(20, 0))          
        # Back to main screen button
        Button(title_frame, text="← Back to Main", font=("Arial", 12, "bold"), 
                                        bg="#E74C3C", fg="white", command=self.leave_to_main).pack(side=RIGHT)
            
    def leave_to_main(self):
        #Return to main application screen
        if self._main_screen:
            self._screen.destroy() # Close window
            self._main_screen.state('zoomed')  #zoom screen
    def _main_container(self):
        #Create the main container with letf,right frame and 
        main_container = Frame(self._screen, bg="#FFFFFF")
        main_container.pack(fill='both', expand=True, padx=10, pady=20)

        self._Left_container(main_container)  # Create left frame
        self._right_container(main_container)  # Create right frame

    def _Left_container(self, left_side):
        #Create left frame with buttons
        left_frame = Frame(left_side, bg="#0B043D",width=250,relief='ridge', bd=10)
        left_frame.pack(side='left', fill='y')

        #buttons add expense , view expense and view customer
        button_configs = [
            ("Add Expense", "#7cea87", self.show_add_expense),
            ("View Expenses", "#dadd77", self.show_all_expenses),
            ("View Customers", "#c87c7c", self.show_customers)
        ]
        i = 0
        while i < len(button_configs):
            text, color, command = button_configs[i]
            Button(left_frame, text=text, font=("Arial", 12), bg=color, width=15, height=2,
                   relief='groove', bd=10, command=command).pack(pady=10, padx=(10,15))
            i += 1
    
    def _right_container(self, right_side):
        # Create right frame
        self._center_frame_widget = Frame(right_side, bg="#20517c", height=400)
        self._center_frame_widget.pack(fill='both', side='left', expand=True, padx=10, pady=10)
        self.show_add_expense()  # Show add expense 
        
    def show_customers(self):
        #Display customer list in a view
        for widget in self._center_frame_widget.winfo_children():
            widget.destroy()  # Clear current content

        content_frame = Frame(self._center_frame_widget, bg="white")
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        Label(content_frame, text="Customer List 💵", 
              font=("Arial", 16, "bold"), bg="white").pack(anchor='w', pady=(0, 20))
        # Load customers from file
        customers = self._file_manager.load_customers()

        if not customers:
            Label(content_frame, text="No customer records found.",
                  font=("Arial", 14), bg="white", fg="#666666").pack(expand=True)
            return
        
        # Create view for customers
        tree_frame = Frame(content_frame)
        tree_frame.pack(fill='both', expand=True)
        tree = ttk.Treeview(tree_frame, columns=("Pet Name", "Owner", "Breed"), show="headings", height=15)
        
        #configure columns
        columns_config = [("Pet Name", 200), ("Owner", 200), ("Breed", 200)]
        i = 0
        while i < len(columns_config):
            col_name, width = columns_config[i]
            tree.heading(col_name, text=col_name)
            tree.column(col_name, width=width, anchor='center')
            i += 1

        # Insert customer data into view
        i = 0
        while i < len(customers):
            customer = customers[i]
            tree.insert("", "end", values=(customer['pet_name'], customer['owner'], customer.get('breed', 'Unknown')))
            i += 1
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill="both", expand=True)
        scrollbar.pack(side='right', fill=Y)

    def show_add_expense(self):
        #Show add expense records
        for widget in self._center_frame_widget.winfo_children():
            widget.destroy()  # Clear current content
        
        add_expense = Frame(self._center_frame_widget, bg="white")
        add_expense.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load customers for selection
        customers = self._file_manager.load_customers()
        main_frame = Frame(add_expense)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Customer selection dropdown
        Label(main_frame, text="Select Customer:", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        customer_var = StringVar(add_expense)
        customer_names = [f"😺{cust['pet_name']} -👤{cust['owner']} -🐾{cust.get('breed', 'Unknown')}" for cust in customers]
        
        if customer_names:
            customer_var.set(customer_names[0])
            OptionMenu(main_frame, customer_var, *customer_names).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        else:
            Label(main_frame, text="No customers available", fg="red").grid(row=0, column=1, padx=5, pady=5)
            customer_var.set("")
        
        # Date selection field
        Label(main_frame, text="Date (YYYY-MM-DD):", font=("Arial", 11, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        date_var = StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        Entry(main_frame, width=20, font=("Arial", 10), textvariable=date_var,state='readonly', readonlybackground="#f0f0f0").grid(row=1, column=1, padx=5, pady=5)
        
        # Services section header
        Label(main_frame, text="Service Details and Costs:", font=("Arial", 12, "bold"), fg="#2C3E50").grid(row=2, column=0, columnspan=2, padx=5, pady=15, sticky='w')
        
        # Service vet ,grooming and feeding
        services = [
            {"name": "Grooming", "key": "grooming", "type": "GROOMING"},
            {"name": "Vet", "key": "vet", "type": "VET"},
            {"name": "Feeding", "key": "feeding", "type": "FEEDING"}
        ]
        price_vars = {}
        service_labels = {}
        has_service = {} 
        
        #create service fields
        i = 0
        while i < len(services):
            service = services[i]
            row_num = 3 + i
            
            # Service name label
            Label(main_frame, text=f"{service['name']}:", font=("Arial", 10, "bold"), 
                  width=12, anchor='w').grid(row=row_num, column=0, padx=5, pady=8, sticky='w')
            
            # Service detail label
            service_label = Label(main_frame, text="No service found", font=("Arial", 9), 
                                 width=40, anchor='w', bg="#f0f0f0", relief="solid", bd=1)
            service_label.grid(row=row_num, column=1, padx=5, pady=8, sticky='w')
            service_labels[service['key']] = service_label
            
            # Price label
            Label(main_frame, text="RM", font=("Arial", 9, "bold")).grid(row=row_num, column=2, padx=(10, 2), pady=8, sticky='w')
            
            # Price entry field 
            default_value = "Free" if service['key'] == 'feeding' else "0.00"
            price_var = StringVar(value=default_value)
            price_entry = Entry(main_frame, width=10, font=("Arial", 9), 
                               textvariable=price_var, state='readonly', readonlybackground="#f0f0f0")
            price_entry.grid(row=row_num, column=3, padx=2, pady=8, sticky='w')
            price_vars[service['key']] = price_var
            has_service[service['key']] = False
            i += 1
        
        def calculate_total_amount():
            #calculate the total amount from vet and grooming, except feeding 
            total = 0.0
            for service_key in ['grooming', 'vet', 'feeding']:
                price_str = price_vars[service_key].get()
                try:
                    price = float(price_str) if price_str and price_str != "Free" else 0.0
                    total += price
                except ValueError:
                    pass
            total_var.set(f"{total:.2f}")
        
        # Total amount display
        Label(main_frame, text="Total Amount (RM):", font=("Arial", 12, "bold")).grid(row=6, column=0, padx=5, pady=15, sticky='w')
        total_var = StringVar(value="0.00")
        Label(main_frame, textvariable=total_var, font=("Arial", 12, "bold"), 
              fg="#E74C3C", bg="#f0f0f0", width=10).grid(row=6, column=1, padx=5, pady=15, sticky='w')

        # Payment method selection Cash, Credit Card, Debit Card ,Online Payment
        Label(main_frame, text="Payment Method:", font=("Arial", 11, "bold")).grid(row=7, column=0, padx=5, pady=10, sticky='w')
        payment_var = StringVar(add_expense)
        payment_var.set("Cash")
        OptionMenu(main_frame, payment_var, "Cash", "Credit Card", "Debit Card", "Online Payment").grid(row=7, column=1, padx=5, pady=10, sticky='w')
        
        def refresh_services():
            # Load services for selected customer
            selected_customer = customer_var.get()
            if not selected_customer or " -👤" not in selected_customer:
                messagebox.showwarning("Warning", "Select a customer")
                return
            
            # Extract pet name and owner from customer string
            parts = selected_customer.split(" -👤")
            if len(parts) >= 2:
                pet_name = parts[0].replace("😺", "").strip()
                owner_breed_part = parts[1]
                if " -🐾" in owner_breed_part:
                    owner = owner_breed_part.split(" -🐾")[0].strip()
                else:
                    owner = owner_breed_part.strip()
                
                #Get customer services from file
                customer_services = self._file_manager.get_customer_services(owner, pet_name)
                
                #update service details
                i = 0
                while i < len(services):
                    service = services[i]
                    key = service['key']
                    if service['type'] in customer_services and customer_services[service['type']]:
                        found = customer_services[service['type']][0]
                        service_labels[key].config(text=found['detail'], fg="black")
                        if key == 'feeding':
                            price_vars[key].set("Free")
                        else:
                            price_vars[key].set(found.get('price', '0.00'))
                        has_service[key] = True
                    else:
                        service_labels[key].config(text=f"No {service['name']} service", fg="red")
                        if key == 'feeding':
                            price_vars[key].set("Free")
                        else:
                            price_vars[key].set("0.00")
                        has_service[key] = False
                    i += 1
                calculate_total_amount()  # Recalculate total amount
        
        def save_expense():
            # Save new expense record to file
            # Validate inputs
            if not date_var.get():
                messagebox.showerror("Error", "Select a date")
                return

            # Check if any service exists
            has_any = False
            keys = ['grooming', 'vet', 'feeding']
            i = 0
            while i < len(keys):
                if has_service.get(keys[i], False):
                    has_any = True
                    break
                i += 1
                
            if not has_any:
                messagebox.showerror("Error", "No services found")
                return
            
            # Validate total amount 
            try:
                total_amount = float(total_var.get())
                if total_amount < 0:
                    messagebox.showerror("Error", "Invalid total")
                    return
            except:
                messagebox.showerror("Error", "Invalid total")
                return
            
            # Extract customer information and load customer record
            selected_customer = customer_var.get()
            if not selected_customer or " -👤" not in selected_customer:
                messagebox.showerror("Error", "Select a customer")
                return
            
            parts = selected_customer.split(" -👤")
            if len(parts) >= 2:
                pet_name = parts[0].replace("😺", "").strip()
                owner_breed_part = parts[1]
                if " -🐾" in owner_breed_part:
                    owner = owner_breed_part.split(" -🐾")[0].strip()
                else:
                    owner = owner_breed_part.strip()
            
            existing_records = self._file_manager.check_duplicate_expense(date_var.get(), owner, pet_name)
            if existing_records:
                response = messagebox.askyesno("Duplicate Record", 
                    f"This pet already has an expense record on {date_var.get()}. Do you want to continue and create a new record?")
                if not response:
                    return
            
            # Get service details
            grooming_detail = service_labels['grooming'].cget("text") or "None"
            vet_detail = service_labels['vet'].cget("text") or "None"
            feeding_detail = service_labels['feeding'].cget("text") or "None"

            # Create expense record line in file 
            line = f"EXPENSE|{date_var.get()}|{owner}|{pet_name}|{grooming_detail}|{vet_detail}|{feeding_detail}|RM{total_var.get()}|{payment_var.get()}\n"
            
            # Save to file
            try:
                with open(self._data_file, 'a', encoding='utf-8') as file:
                    file.write(line)
                messagebox.showinfo("Success", "Expense added!")
                self.show_all_expenses()  # Refresh view
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {str(e)}")
        
        # Buttons frame 
        button_frame = Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=4, pady=20, sticky='ew')
        
        # buttons save and load
        button_configs = [
            ("Save Expense", "#27AE60", save_expense),
            ("Load Service", "#3498DB", refresh_services)
        ]
        
        i = 0
        while i < len(button_configs):
            text, bg_color, command = button_configs[i]
            font_size = 11 if text != "Load Service" else 10
            Button(button_frame, text=text, command=command,
                   bg=bg_color, fg="white", font=("Arial", font_size), width=15).pack(side=LEFT, padx=5, expand=True)
            i += 1
    
    def show_all_expenses(self):
        #Display all expense records with total spending
        for widget in self._center_frame_widget.winfo_children():
            widget.destroy()  # Clear current content
        
        # Load expense data
        data = self._file_manager.load_expense_data()
        columns = ["Date", "Owner", "Pet Name", "Grooming", "Vet", "Feeding", "Total Amount", "Payment Method"]
        
        # Calculate total spending
        total_spending = 0.0
        i = 0
        while i < len(data):
            expense = data[i]
            if len(expense) >= 7:
                total_str = expense[6]
                if total_str.startswith('RM'):
                    try:
                        total_spending += float(total_str[2:])
                    except:
                        pass
            i += 1
        
        # Total spending display on the view top
        stats_frame = Frame(self._center_frame_widget, bg="#2C3E50", height=60)
        stats_frame.pack(fill='x', padx=10, pady=(10, 0))
        total_text = f"💸 Total Spending for All Customers: RM{total_spending:.2f}"
        Label(stats_frame, text=total_text, font=("Arial", 20, "bold"), 
              fg="lightgreen", bg="#2C4250").pack(pady=15)
        
        # Show message if no data
        if len(data) == 0:
            Label(self._center_frame_widget, 
                  text="No expense records found.\nClick 'Add Expense' to create new records.",
                  font=("Arial", 14), bg="#AED6F1", fg="#666666").pack(expand=True)
            return
        else:
            self._create_expense_tree_view("All Expenses 💵", columns, data)

    def _create_expense_tree_view(self, title, columns, data):
        #Create view for display expense records
        content_frame = Frame(self._center_frame_widget, bg="white", relief='solid', bd=10)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        Label(content_frame, text=title, 
              font=("Arial", 16, "bold"), bg="white").pack(anchor='w', pady=(0, 10))
        
        # buttons frame
        button_frame = Frame(content_frame, bg="white")
        button_frame.pack(fill='x', pady=(0, 10))
        
        #buttons edit and delete
        button_configs = [
            ("✏️ Edit Record", "#f39c12", lambda: self._simple_change_record(tree)),
            ("🗑️ Delete Selected", "#E74C3C", lambda: self._delete_selected_record(tree))]
        
        i = 0
        while i < len(button_configs):
            text, bg_color, command = button_configs[i]
            Button(button_frame, text=text, font=("Arial", 10, "bold"), 
                   bg=bg_color, fg="white", command=command).pack(side=LEFT, padx=5)
            i += 1
        
        # Create view for data
        tree_frame = Frame(content_frame)
        tree_frame.pack(fill='both', expand=True)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        #configure columns
        i = 0
        while i < len(columns):
            tree.heading(columns[i], text=columns[i])
            tree.column(columns[i], width=120, anchor='center')
            i += 1
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill="both", expand=True)
        scrollbar.pack(side='right', fill=Y)
        
        # Insert data into view 
        i = 0
        while i < len(data):
            row = data[i]
            if len(row) > 0:
                tree.insert("", "end", values=row)
            i += 1

    def _simple_change_record(self, tree):
        #Open window to edit selected expense record
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to change")
            return
            
        # Get selected record values
        item_values = tree.item(selected_item[0])['values']

        # Find original line in file
        original_line = self._file_manager.find_expense_line_by_values(item_values)
        if not original_line:
            messagebox.showerror("Error", "Cannot find original record in file!")
            return

        # Create edit window
        change_window = Toplevel(self._screen)
        change_window.title("Edit Record")
        change_window.geometry("550x650") 
        change_window.transient(self._screen)
        change_window.grab_set() # Make modal
        
        Edit_frame = Frame(change_window)
        Edit_frame.pack(fill='both', expand=True, padx=20, pady=20)
        Label(Edit_frame, text="Edit Expense Record", 
              font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Store field variables
        fields = {}
        price_vars = {}
        price_widgets = {}
        
        # Create fields for each data item
        field_names = ["Date", "Owner", "Pet Name", "Grooming Detail", "Vet Detail", "Feeding Detail"]
        i = 0
        while i < len(field_names):
            name = field_names[i]
            frame = Frame(Edit_frame)
            frame.pack(fill='x', pady=5)
            
            Label(frame, text=f"{name}:", font=("Arial", 10, "bold"), width=20, anchor='w').pack(side=LEFT, padx=5)
            
            # Create entry field with existing value
            value_var = StringVar(value=item_values[i] if i < len(item_values) else "")
            entry = Entry(frame, width=30, font=("Arial", 10), textvariable=value_var)
            entry.pack(side=LEFT, padx=5, fill='x', expand=True)
            
            fields[name] = value_var
            i += 1
        
        # Payment method selection
        payment_frame = Frame(Edit_frame)
        payment_frame.pack(fill='x', pady=5)
        Label(payment_frame, text="Payment Method:", font=("Arial", 10, "bold"), width=20, anchor='w').pack(side=LEFT, padx=5)
        
        payment_var = StringVar(value=item_values[7] if len(item_values) > 7 else "Cash")
        payment_methods = ["Cash", "Credit Card", "Debit Card", "Online Payment"]
        payment_menu = OptionMenu(payment_frame, payment_var, *payment_methods)
        payment_menu.pack(side=LEFT, padx=5, fill='x', expand=True)
        fields["Payment Method"] = payment_var
        
        # Service prices section header
        Label(Edit_frame, text="Service Prices:", 
              font=("Arial", 12, "bold")).pack(anchor='w', pady=(20, 10))
        
        # Service definitions
        services = [
            {"name": "Grooming", "key": "grooming", "type": "GROOMING"},
            {"name": "Vet", "key": "vet", "type": "VET"},
            {"name": "Feeding", "key": "feeding", "type": "FEEDING"}
        ]
        
        # Extract original prices
        original_parts = original_line.split('|')
        grooming_price = "0.00"
        vet_price = "0.00"
        
        if len(original_parts) >= 12:
            grooming_price = original_parts[9].replace('Grooming:RM', '').strip() if len(original_parts) > 9 else "0.00"
            vet_price = original_parts[10].replace('Vet:RM', '').strip() if len(original_parts) > 10 else "0.00"
        
        def is_service_valid(service_detail):
            #Check if service detail is valid
            service_detail_lower = service_detail.lower().strip()
            invalid_keywords = ["no record", "no", "-", "none", "NO"]
            i = 0
            while i < len(invalid_keywords):
                if invalid_keywords[i] in service_detail_lower:
                    return False
                i += 1
            return True
        
        # Create price fields for each service
        i =0
        while i < len(services):
            service = services[i]
            frame = Frame(Edit_frame)
            frame.pack(fill='x', pady=5)
            
            Label(frame, text=f"{service['name']} Price (RM):", 
                  font=("Arial", 10, "bold"), width=20, anchor='w').pack(side=LEFT, padx=5)
            
            # Set default price based on service type
            if service['key'] == 'grooming': 
                default_price = grooming_price
            elif service['key'] == 'vet':
                default_price = vet_price
            else: 
                default_price = "Free"
            
            # grooming and vet cannot edit price
            price_var = StringVar(value=default_price)
            initial_state = 'readonly' #set the entry display readonly cannot edit
            initial_bg = '#f0f0f0'
            
            if service['key'] == 'feeding':
                initial_state = 'readonly' #set the entry display readonly cannot edit
                initial_bg = '#f0f0f0'
            
            # Create price entry field
            price_entry = Entry(frame, width=30, font=("Arial", 10), 
                              textvariable=price_var, state=initial_state, bg=initial_bg)
            price_entry.pack(side=LEFT, padx=5, fill='x', expand=True)
            price_vars[service['key']] = price_var
            price_widgets[service['key']] = (price_entry, service['key'] != 'feeding')  #feeding cannot edit
            i += 1
        
        def load_services():
            #Load services for current customer
            owner = fields['Owner'].get()
            pet_name = fields['Pet Name'].get()
            
            if not owner or not pet_name:
                messagebox.showwarning("Warning", "Owner and Pet Name are required!")
                return
            
            # Get customer services from file
            customer_services = self._file_manager.get_customer_services(owner, pet_name)
            
            # Update service details and prices
            i = 0
            while i < len(services):
                service = services[i]
                key = service['key']
                if service['type'] in customer_services and customer_services[service['type']]:
                    found = customer_services[service['type']][0]
                    fields[f"{service['name']} Detail"].set(found['detail'])
                    if key == 'feeding':
                        price_vars[key].set("Free")
                    else:
                        price_vars[key].set(found.get('price', '0.00'))
                else:
                    fields[f"{service['name']} Detail"].set(f"No {service['name']} service")
                    if key == 'feeding':
                        price_vars[key].set("Free")
                    else:
                        price_vars[key].set("0.00")
                i += 1
            
            # Determine which fields can be edited
            grooming_detail_new = fields['Grooming Detail'].get()
            vet_detail_new = fields['Vet Detail'].get()
            
            can_edit_grooming_new = is_service_valid(grooming_detail_new)
            can_edit_vet_new = is_service_valid(vet_detail_new)
            
            # Update if grooming have record then can update price you want    
            i = 0
            while i < len(services):
                service = services[i]
                key = service['key']
                widget, _ = price_widgets[key]

                if key == 'feeding':
                    can_edit = False
                else:
                    can_edit = can_edit_grooming_new if key == 'grooming' else can_edit_vet_new
                
                #can edit only vet and grooming ,except feeding
                if can_edit:
                    widget.config(state='normal', bg='white')
                    if key == 'grooming':
                        price_vars[key].trace_add('write', lambda *args: calculate_total())
                    elif key == 'vet':
                        price_vars[key].trace_add('write', lambda *args: calculate_total())
                else:
                    widget.config(state='readonly', bg='#f0f0f0')
                
                price_widgets[key] = (widget, can_edit)
                i += 1
            calculate_total()  # Recalculate total
        
        def calculate_total(*args):
            #Calculate total from service prices
            total = 0.0
            keys = ['grooming', 'vet']
            i = 0
            while i < len(keys):
                key = keys[i]
                try:
                    price_str = price_vars[key].get()
                    price = float(price_str) if price_str and price_str != "Free" else 0.0
                    total += price
                except:
                    pass
                i += 1
            total_var.set(f"{total:.2f}")
            return total
        
        # write the price again on grooming and vet
        price_vars['grooming'].trace_add('write', calculate_total)
        price_vars['vet'].trace_add('write', calculate_total)
        
        # Calculate the total from grooming and vet ,except feeding
        total_amount = 0.0
        price_list = [grooming_price, vet_price]
        i = 0
        while i < len(price_list):
            try:
                price_str = price_list[i]
                price = float(price_str) if price_str and price_str != "Free" else 0.0
                total_amount += price
            except:
                pass
            i += 1
        
        # Total amount display
        total_frame = Frame(Edit_frame)
        total_frame.pack(fill='x', pady=10)
        Label(total_frame, text="Total Amount (RM):", font=("Arial", 12, "bold"), 
              width=20, anchor='w').pack(side=LEFT, padx=5)
        
        total_var = StringVar(value=f"{total_amount:.2f}")
        Label(total_frame, textvariable=total_var, font=("Arial", 12, "bold"), 
              fg="#E74C3C", bg="#f0f0f0", width=15).pack(side=LEFT, padx=5)
        
        def save_changes():
            # Save edited record to file
            # Validate required fields 
            required_fields = ['Date', 'Owner', 'Pet Name']
            i = 0
            while i < len(required_fields):
                field_name = required_fields[i]
                if not fields[field_name].get().strip():
                    messagebox.showerror("Error", f"{field_name} cannot be empty!")
                    return
                i += 1
            
            # Validate price about the grooming and vet
            keys = ['grooming', 'vet']
            i = 0
            while i < len(keys):
                key = keys[i]
                price_entry, can_edit = price_widgets[key]
                
                # edit the value
                if can_edit:
                    try:
                        price_str = price_vars[key].get()
                        price = float(price_str) if price_str and price_str != "Free" else 0.0
                        if price < 0:
                            messagebox.showerror("Error", f"{key.capitalize()} price cannot be negative!")
                            return
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid {key} price!")
                        return
                else:
                    if not price_vars[key].get().strip():
                        price_vars[key].set("0.00")
                i += 1
            
            # Validate total amount
            try:
                total_amount_val = float(total_var.get())
                if total_amount_val < 0:
                    messagebox.showerror("Error", "Invalid total amount")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid total amount")
                return

            # Create new expense record line in file
            new_line = f"EXPENSE|{fields['Date'].get()}|{fields['Owner'].get()}|{fields['Pet Name'].get()}|{fields['Grooming Detail'].get()}|{fields['Vet Detail'].get()}|{fields['Feeding Detail'].get()}|RM{total_amount_val:.2f}|{fields['Payment Method'].get()}"
            
            # Update record in file
            success = self._file_manager.update_record(original_line, new_line)
            if success:
                messagebox.showinfo("Success", "Record updated successfully!")
                change_window.destroy()
                self.show_all_expenses()  # Refresh view
            else:
                messagebox.showerror("Error", "Update failed!")
        
        #buttons load, save and cancel
        button_frame = Frame(Edit_frame)
        button_frame.pack(fill='x', pady=20)
        
        button_configs = [
            ("Load Service", "#3498DB", load_services, 10),
            ("Save Changes", "#27AE60", save_changes, 11),
            ("Cancel", "#E74C3C", change_window.destroy, 11)
        ]
        
        i = 0
        while i < len(button_configs):
            text, bg_color, command, font_size = button_configs[i]
            Button(button_frame, text=text, command=command,
                   bg=bg_color, fg="white", font=("Arial", font_size), width=15).pack(side=LEFT, padx=5, expand=True)
            i += 1

    def _delete_selected_record(self, tree):
        #Delete selected record from view and file
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a record")
            return
        
        # Confirmation to delete
        confirm = messagebox.askyesno("Confirm", "Delete this record?")
        if confirm:
            try:
                item_values = tree.item(selected_item[0])['values']
                # Delete from file
                success = self._file_manager.delete_expense_record(item_values)
                if success:
                    tree.delete(selected_item[0])  # Remove from treeview
                    messagebox.showinfo("Success", "Record deleted")
                    self.show_all_expenses()  # Refresh view
                else:
                    messagebox.showerror("Error", "Delete failed")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

class FileManager:
    def __init__(self, data_file="data.txt"):
        # FileManager with data file
        self._data_file = data_file
    
    def check_duplicate_expense(self, date, owner, pet_name):
        #check file info and check if have file exist
        if not os.path.exists(self._data_file):
            return []
        
        duplicates = []
        try:
            with open(self._data_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('EXPENSE'):#check
                        parts = line.split('|')
                        if len(parts) >= 4:
                            if parts[1] == date and parts[2] == owner and parts[3] == pet_name:
                                duplicates.append(line)
        except:
            pass
        return duplicates
    
    def load_customers(self):
        #Load customer data from file
        customers = []
        if os.path.exists(self._data_file):
            with open(self._data_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('PET'):  # Identify customer records
                        parts = line.split('|')
                        if len(parts) >= 4:
                            customers.append({
                                'pet_name': parts[1],
                                'owner': parts[2],
                                'breed': parts[3]
                            })
        return customers
    
    def get_customer_services(self, owner, pet_name):
        #Get services for specific customer
        services = {'FEEDING': [], 'VET': [], 'GROOMING': []}
        if os.path.exists(self._data_file):
            with open(self._data_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            rec_type = parts[0]
                            # Find services for specific pet
                            if rec_type in ['FEEDING', 'VET', 'GROOMING'] and parts[1] == pet_name:
                                service_data = {
                                    'type': rec_type,
                                    'detail': self._parse_service_detail(rec_type, parts),
                                    'price': self._extract_price(line)
                                }
                                services[rec_type].append(service_data)
        return services
    
    def _parse_service_detail(self, service_type, parts):
    #service details from parts
        match service_type:
            case 'FEEDING' if len(parts) >= 5:
                return parts[4]
            case 'VET' if len(parts) >= 7:
                return parts[6]
            case 'GROOMING' if len(parts) >= 5:
                return parts[4]
            case _:
                return "No details"
    
    def _extract_price(self, line):
        #Check price from line containing 'RM' 
        if 'RM' in line:
            start = line.find('RM') + 2
            price = ''
            i = start
            while i < len(line):
                char = line[i]
                if char.isdigit() or char == '.':
                    price += char
                else:
                    break
                i += 1
            return price if price else "0.00"
        return "0.00"

    def load_expense_data(self):
        #Load expense records from file
        data = []
        if os.path.exists(self._data_file):
            with open(self._data_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('EXPENSE'):  # Identify expense records
                        parts = line.split('|')
                        if len(parts) >= 9:
                            data.append(parts[1:9])  # Skip 'EXPENSE' then check behind record
        return data
    
    def find_expense_line_by_values(self, item_values):
        #Find expense line matching specific values
        if not os.path.exists(self._data_file):
            return ""
        try:
            with open(self._data_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('EXPENSE'):
                        parts = line.split('|')
                        if len(parts) >= 9:
                            # Check if all values match
                            match = True
                            i = 1
                            while i <= 8 and match:
                                if i < len(parts) and i <= len(item_values):
                                    if parts[i] != item_values[i-1]:
                                        match = False
                                else:
                                    match = False
                                i += 1
                            if match:
                                return line
        except:
            pass
        return ""
        
    def delete_expense_record(self, record_values):
        #Delete expense record from file
        if not os.path.exists(self._data_file):
            return False
        try:
            with open(self._data_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            new_lines = []
            found = False
            # Filter out matching record
            for line in lines:
                line = line.strip()
                if line.startswith('EXPENSE'):
                    parts = line.split('|')
                    if len(parts) >= 9:
                        match = True
                        i = 1
                        while i <= 8 and match:
                            if i < len(parts) and i <= len(record_values):
                                if parts[i] != record_values[i-1]:
                                    match = False
                            else:
                                match = False
                            i += 1
                        if match:
                            found = True
                            continue
                new_lines.append(line + '\n')
            
            # Save updated file if record was found
            if found:
                with open(self._data_file, 'w', encoding='utf-8') as file:
                    file.writelines(new_lines)
                return True
        except:
            pass
        return False
        
    def update_record(self, original_line, new_line):
        #Update existing record in file
        if not os.path.exists(self._data_file):
            return False
        try:
            with open(self._data_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            new_lines = []
            found = False
            # Replace original line with new line
            i = 0
            while i < len(lines):
                if lines[i].strip() == original_line:
                    new_lines.append(new_line + '\n')
                    found = True
                else:
                    new_lines.append(lines[i])
                i += 1
            # Save updated file if record was found
            if found:
                with open(self._data_file, 'w', encoding='utf-8') as file:
                    j = 0
                    while j < len(new_lines):
                        file.write(new_lines[j])
                        j += 1
                return True
        except:
            pass 
        return False

if __name__ == "__main__":
    screen = Tk()  # Create main window
    app = PetExpenseTracker(screen)  # Create expense tracker 
    screen.mainloop()  # Start GUI event loop