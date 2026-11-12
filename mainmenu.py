from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PetExpenseTracker import PetExpenseTracker
from FeedingApp import FeedingApp
from Vetapp import vet_app
from GroomingApp import GroomingApp
import os

class homeGui:
    def __init__(self, screen):
        #the main home GUI application
        self.screen = screen 
        self.screen.title("🐾 Pet Care Assistant 🐾")# set pet title
        self.screen.state('zoomed') # zoom screen
        self.screen.configure(bg="#827F7F")  # Set background color
        self.pet_manager = FileManager()  # Create file manager for pet data
        self.AppGui()

    def AppGui(self):
        # main application GUI
        self.title()  # Create title section
        self.main_container()  # Create main container

    def title(self):
        #Create the application title bar
        title_frame = Frame(self.screen, bg='#2c3e50', height=100,relief='ridge', bd=10)
        title_frame.pack(fill='x', padx=10, pady=10)
        Label(title_frame, text="😺 Pet Care 😺", font=('Arial', 50, 'bold'), 
              fg='white', bg='#2c3e50').pack(pady=20)
    
    def main_container(self):
        #Create the main container with sidebar and content area
        main_container = Frame(self.screen, bg="#20517c",relief='solid', bd=3)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
       
        self.Left_container(main_container)  # Create left sidebar
        self.right_container(main_container)  # Create right content area

    def Left_container(self, left_side):
        #Create left sidebar with navigation buttons
        left_frame = Frame(left_side, bg='#34495e', width=250,relief='ridge', bd=10)
        left_frame.pack(side='left', fill='y')

        menu_frame = Frame(left_frame, bg='#34495e')
        menu_frame.pack(fill='x', padx=10, pady=20)
        
        # Pet Management section
        Label(menu_frame, text="🐾 Pet Management", font=('Arial', 16, 'bold'),
              fg='white', bg='#34495e').pack(anchor='w', pady=(0, 10))
        # Add pet button command
        Button(menu_frame, text="➕ Add Pet", font=('Arial', 12, 'bold'), bg='#27ae60',relief='groove', bd=10,
               fg='white', width=15, height=2, command=self.show_add_pet).pack(pady=5)
        # View pets button command
        Button(menu_frame, text="👀 View Pets", font=('Arial', 12, 'bold'), bg='#3498db',relief='groove', bd=10, 
               fg='white', width=15, height=2, command=self.show_pet_list).pack(pady=5)
        # Menu section header
        Label(menu_frame, text="📋 Menu", font=('Arial', 16, 'bold'), 
              fg='white', bg='#34495e').pack(anchor='w', pady=(0, 15))
        # Menu buttons with their commands
        buttons = [
            ("🍚 Feeding Tracker", self.show_feeding_tracker),
            ("🏥 Vet Appointments", self.show_vet_appointments),
            ("💈 Grooming Schedule", self.show_grooming_schedule),
            ("💰 Expense Tracker", self.show_expense_tracker)
        ]
        # Create menu buttons
        i = 0
        while i < len(buttons):
            text, next_page = buttons[i]
            Button(menu_frame, text=text, command=next_page, width=17, height=2,relief='groove', bd=10,
                   bg="#475AC4", fg='white', font=('Arial', 12), anchor='w').pack(pady=5)
            i += 1

    def right_container(self, parent):
        #Create right content area to display forms and data
        self.content_frame = Frame(parent, bg='white')
        self.content_frame.pack(side='left', fill='both', expand=True)
        self.show_welcome_page()  # Show welcome page by default
   
    def show_welcome_page(self):
        #Display the welcome page with application features
        self.clear_content()  # Clear current content
        welcome_frame = Frame(self.content_frame, bg='white')
        welcome_frame.pack(expand=True, fill='both', padx=50, pady=50)
        # Welcome message
        Label(welcome_frame, text="Welcome to Pet Care Assistant!", font=('Arial', 32, 'bold'),
              fg='#2c3e50', bg='white').pack(pady=20)
        Label(welcome_frame, text="Please select a function from the left side menu", 
              font=('Arial', 16), fg='#7f8c8d', bg='white').pack(pady=10)
        # List of features using while loop
        Text = [
            "🐾 Add Pet - Register your pets information",
            "🍚 Feeding Tracker - Manage your pet's feeding schedule and diet",
            "🏥 Vet Appointments - Schedule and track veterinary visits",
            "💈 Grooming Schedule - Organize grooming appointments",
            "💰 Expense Tracker - Monitor pet-related expenses and budgets",
        ]
        i = 0
        while i < len(Text):
            Label(welcome_frame, text=Text[i], font=('Arial', 14),
                  fg="#3B5068", bg='white', justify='left').pack(pady=8)
            i += 1

    def clear_content(self):
        #Clear all widgets from the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_add_pet(self):
        #Show form for adding a new pet
        self.clear_content()
       
        form_frame = Frame(self.content_frame, bg='white')
        form_frame.pack(expand=True, fill='both', padx=50, pady=30)
        Label(form_frame, text="Add New Pet", font=('Arial', 24, 'bold'), 
              bg='white').pack(pady=20)
       
        # Pet name field
        name_frame = Frame(form_frame, bg='white')
        name_frame.pack(pady=15)
        Label(name_frame, text="Pet Name:", font=('Arial', 12, 'bold'),
              bg='white').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        pet_name_var = StringVar()
        Entry(name_frame, textvariable=pet_name_var, font=('Arial', 12),
              width=30).grid(row=0, column=1, padx=10, pady=5)
       
        # Owner name field
        owner_frame = Frame(form_frame, bg='white')
        owner_frame.pack(pady=15)    
        Label(owner_frame, text="Owner Name:", font=('Arial', 12, 'bold'),
              bg='white').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        owner_name_var = StringVar()
        Entry(owner_frame, textvariable=owner_name_var,
              font=('Arial', 12), width=30).grid(row=0, column=1, padx=10, pady=5)

        # Breed selection field
        breed_frame = Frame(form_frame, bg='white')
        breed_frame.pack(pady=15)   
        Label(breed_frame, text="Breed :", font=('Arial', 12, 'bold'),
              bg='white').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        breed_var = StringVar()
        breed_var.set("Choose breed")
        breed_options = ["Dog", "Cat"]
        breed_menu = OptionMenu(breed_frame, breed_var, *breed_options)
        breed_menu.config(font=('Arial', 12), width=20)
        breed_menu.grid(row=0, column=1, padx=10, pady=5)
       
        def save_pet():
            # Save the new pet information to file
            pet_name = pet_name_var.get().strip()
            owner_name = owner_name_var.get().strip()
            breed = breed_var.get().strip()
           
            # Validate inputs
            if not pet_name:
                messagebox.showerror("Error", "Please enter pet name!")
                return
            if not owner_name:
                messagebox.showerror("Error", "Please enter owner name!")
                return
            if breed == "Choose breed":
                messagebox.showerror("Error", "Please select a breed!")
                return
        
            # Save pet to file
            success, message = self.pet_manager.save_pet(pet_name, owner_name, breed)
            if success:
                messagebox.showinfo("Success", message)
                # Clear form fields
                pet_name_var.set("")
                owner_name_var.set("")
                breed_var.set("Choose breed")  
            else:
                messagebox.showerror("Error", message)
       
        # Action buttons
        button_frame = Frame(form_frame, bg='white')
        button_frame.pack(pady=30)
       
        Button(button_frame, text="Save Pet", command=save_pet,
               bg='#27ae60', fg='white', font=('Arial', 12), width=15).pack(side=LEFT, padx=10)      
        Button(button_frame, text="Back", command=self.show_welcome_page,
               bg='#e74c3c', fg='white', font=('Arial', 12), width=15).pack(side=LEFT, padx=10)

    def show_pet_list(self):
        #Display list of all owner info about pet in a view to check
        self.clear_content()
        content_frame = Frame(self.content_frame, bg='white')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
       
        Label(content_frame, text="My Pets", font=('Arial', 24, 'bold'),
              bg='white').pack(pady=20)
       
        # Load pets from file
        pets = self.pet_manager.load_pets()
       
        # Show message if no pets found
        if not pets:
            Label(content_frame, text="No pets found. Click 'Add Pet' to add your first pet!",
                  font=('Arial', 14), bg='white', fg='#666').pack(expand=True)
            return
       
        # Create view for pets , owner and breed
        columns = ["Pet Name", "Owner", "Breed"]
        tree_frame = Frame(content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
       
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        # Configure columns 
        i = 0
        while i < len(columns):
            tree.heading(columns[i], text=columns[i])
            tree.column(columns[i], width=200, anchor='center')
            i += 1
        
        # Insert pet data
        i = 0
        while i < len(pets):
            pet = pets[i]
            tree.insert("", "end", values=(pet['name'], pet['owner'], pet['breed']))
            i += 1
       
        # Add scrollbar on breed
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
       
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
       
        # buttons edit,refresh and delete
        button_frame = Frame(content_frame, bg='white')
        button_frame.pack(pady=10)

        Button(button_frame, text="Edit Selected", command=lambda: self.edit_selected_pet(tree),
               bg='#f39c12', fg='white', font=('Arial', 11),width=15,height=2).pack(side=LEFT, padx=5)
        Button(button_frame, text="Refresh", command=self.show_pet_list,
               bg='#3498db', fg='white', font=('Arial', 11),width=15,height=2).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete Selected", command=lambda: self.delete_selected_pet(tree),
               bg='#e74c3c', fg='white', font=('Arial', 11),width=15,height=2).pack(side=LEFT, padx=5)

    def edit_selected_pet(self, tree):
        #Edit the selected pet from the view
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a pet to edit.")
            return
       
        item = selected_item[0]
        values = tree.item(item, 'values')
        pet_name = values[0]
        owner_name = values[1]
        breed = values[2]
        self.show_edit_pet_form(pet_name, owner_name, breed, item, tree)

    def delete_selected_pet(self, tree):
        #Delete the selected pet from the view and file
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a pet to delete.")
            return
        
        item = selected_item[0]
        values = tree.item(item, 'values')
        pet_name = values[0]
        owner_name = values[1]
        
        # Confirmation delete info
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete pet '{pet_name}'?\n\n"
                                     "This will also delete all related records (feeding, vet, grooming, expenses)!")
        if not confirm:
            return
        
        # Delete the pet and all related records
        success, message = self.pet_manager.delete_pet_and_related(pet_name, owner_name)
        if success:
            messagebox.showinfo("Success", message)
            tree.delete(item)  # Remove from treeview
            # Refresh the view to show updated list
            self.show_pet_list()
        else:
            messagebox.showerror("Error", message)

    def show_edit_pet_form(self, old_pet_name, old_owner_name, old_breed, tree_item, tree):
        #Show form for editing pet information
        self.clear_content()
        
        form_frame = Frame(self.content_frame, bg='white')
        form_frame.pack(expand=True, fill='both', padx=50, pady=30)
        Label(form_frame, text="Edit Pet Information", font=('Arial', 24, 'bold'),
            bg='white').pack(pady=20)
        
        # Pet name field with current value
        name_frame = Frame(form_frame, bg='white')
        name_frame.pack(pady=15)
        Label(name_frame, text="Pet Name:", font=('Arial', 12, 'bold'),
            bg='white').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        pet_name_var = StringVar(value=old_pet_name)
        Entry(name_frame, textvariable=pet_name_var, font=('Arial', 12), 
            width=30).grid(row=0, column=1, padx=10, pady=5)
        
        # Owner name field with current value
        owner_frame = Frame(form_frame, bg='white')
        owner_frame.pack(pady=15)
        
        Label(owner_frame, text="Owner Name:", font=('Arial', 12, 'bold'),
            bg='white').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        owner_name_var = StringVar(value=old_owner_name)
        Entry(owner_frame, textvariable=owner_name_var, font=('Arial', 12), 
            width=30).grid(row=0, column=1, padx=10, pady=5)

        # Breed selection with current value
        breed_frame = Frame(form_frame, bg='white')
        breed_frame.pack(pady=15)
        
        Label(breed_frame, text="Breed:", font=('Arial', 12, 'bold'),
            bg='white').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        breed_var = StringVar(value=old_breed)
        breed_options = ["Dog", "Cat"]
        breed_menu = OptionMenu(breed_frame, breed_var, *breed_options)
        breed_menu.config(font=('Arial', 12), width=20)
        breed_menu.grid(row=0, column=1, padx=10, pady=5)
        
        def update_pet():
            #Update pet information in file
            new_pet_name = pet_name_var.get().strip()
            new_owner_name = owner_name_var.get().strip()
            new_breed = breed_var.get().strip()
            
            # Validate inputs
            if not new_pet_name:
                messagebox.showerror("Error", "Please enter pet name!")
                return
            if not new_owner_name:
                messagebox.showerror("Error", "Please enter owner name!")
                return
            if new_breed == "Choose breed":
                messagebox.showerror("Error", "Please select a breed!")
                return
            
            # Update pet in file
            success, message = self.pet_manager.update_pet(
                old_pet_name, new_pet_name, new_owner_name, new_breed
            )
            if success:
                messagebox.showinfo("Success", message)
                self.show_pet_list()  # Return to pet list
            else:
                messagebox.showerror("Error", message)
        
        #buttons update and leave
        button_frame = Frame(form_frame, bg='white')
        button_frame.pack(pady=30)
        Button(button_frame, text="Update Pet", command=update_pet,
            bg='#f39c12', fg='white', font=('Arial', 12), width=15).pack(side=LEFT, padx=10)
        Button(button_frame, text="Back to List", command=self.show_pet_list,
            bg='#e74c3c', fg='white', font=('Arial', 12), width=15).pack(side=LEFT, padx=10)

    def show_feeding_tracker(self):
        #Open Feeding Tracker application
        feeding_window = Toplevel()
        feeding_window.state('zoomed')
        FeedingApp(feeding_window, self.screen)  # Pass main screen reference

    def show_vet_appointments(self):
        #Open Vet Appointments application
        vet_window = Toplevel()
        vet_window.state('zoomed')
        vet_app(vet_window, self.screen)  # Pass main screen reference

    def show_grooming_schedule(self):
        #Open Grooming Schedule application
        grooming_window = Toplevel()
        grooming_window.state('zoomed')
        GroomingApp(grooming_window, self.screen)  # Pass main screen reference

    def show_expense_tracker(self):
        #Open Expense Tracker application
        expense_window = Toplevel()
        expense_window.state('zoomed')
        PetExpenseTracker(expense_window, self.screen)  # Pass main screen reference

class FileManager:
    def __init__(self, data_file="data.txt"):
        #FileManager with data file
        self.data_file = data_file
   
    def load_pets(self):
        #Load all pets from data file
        pets = []
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    # Skip comments and empty lines, only process stand for PET records
                    if line and not line.startswith('#') and line.startswith('PET'):
                        parts = line.split('|')
                        if len(parts) >= 4:
                            pets.append({
                                'name': parts[1],
                                'owner': parts[2],
                                'breed': parts[3] if len(parts) > 3 else "Unknown"
                            })
        return pets
   
    def save_pet(self, pet_name, owner_name, breed="Unknown"):
        #Save a new pet to data file
        existing_pets = self.load_pets()
        
        # Check if pet already get exists
        i = 0
        while i < len(existing_pets):
            pet = existing_pets[i]
            if pet['name'].lower() == pet_name.lower():
                return False, "Pet with this name already exists!"
            i += 1
               
        # Append new pet to file
        line = f"PET|{pet_name}|{owner_name}|{breed}\n"
        with open(self.data_file, 'a', encoding='utf-8') as file:
            file.write(line)
        return True, "Pet added successfully!"
   
    def update_pet(self, old_pet_name, new_pet_name, new_owner_name, new_breed):
        #Update existing pet information
        if not os.path.exists(self.data_file):
            return False, "Data file not found!"

        # Check pet names
        existing_pets = self.load_pets()
        i = 0
        while i < len(existing_pets):
            pet = existing_pets[i]
            if (pet['name'].lower() == new_pet_name.lower() and 
                pet['name'].lower() != old_pet_name.lower()):
                return False, "Another pet with this name already exists!"
            i += 1
       
        # Read all lines from file
        with open(self.data_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
       
        updated = False
        # Find and update the pet record
        i = 0
        while i < len(lines) and not updated:
            line = lines[i].strip()
            if line and not line.startswith('#') and line.startswith('PET'):
                parts = line.split('|')
                if len(parts) >= 4 and parts[1] == old_pet_name:
                    lines[i] = f"PET|{new_pet_name}|{new_owner_name}|{new_breed}\n"
                    updated = True
            i += 1
       
        if not updated:
            return False, "Pet not found!"
        
        # Write updated pet info to file
        with open(self.data_file, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        return True, "Pet information updated successfully!"
    
    def delete_pet_and_related(self, pet_name, owner_name):
        #delete pet info
        if not os.path.exists(self.data_file):
            return False, "Data file not found!"
        
        # Read all lines from file
        with open(self.data_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Filter out the pet record and all related records
        new_lines = []
        pet_found = False
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line and not line.startswith('#'):
                parts = line.split('|')
                if len(parts) >= 2:
                    record_type = parts[0]
                    
                    # Check if the pet record need to delete
                    if record_type == 'PET' and len(parts) >= 4:
                        if parts[1] == pet_name and parts[2] == owner_name:
                            pet_found = True
                            i += 1
                            continue
                    
                    # Check pet record related value of feeding , grooming , vet
                    elif record_type in ['FEEDING', 'GROOMING', 'VET'] and len(parts) >= 2:
                        if parts[1] == pet_name:
                            # Skip this related record
                            i += 1
                            continue
                    
                    # Check for EXPENSE records in file
                    elif record_type == 'EXPENSE' and len(parts) >= 4:
                        if parts[2] == owner_name and parts[3] == pet_name:
                            # Skip this expense record
                            i += 1
                            continue
            
            # Keep all other records in file
            new_lines.append(lines[i])
            i += 1
        
        # if pet name no found 
        if not pet_found:
            return False, f"Pet '{pet_name}' not found!"
        
        # Write updated lines back to file
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                file.writelines(new_lines)
            return True, f"Pet '{pet_name}' and all related records deleted successfully!"
        except Exception as e:
            return False, f"Error deleting pet: {str(e)}"
    
if __name__ == "__main__":
    screen = Tk()  # Create main window
    app = homeGui(screen)  # Create home GUI application 
    screen.mainloop() # main loop of the all app