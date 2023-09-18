import tkinter as tk
from tkinter import messagebox
import os.path
import pickle
import ipaddress
import psutil
import pyuac
import sys

HEIGHT = 620
WIDTH = 420      
options = []
network_details = []
network_interfaces = []
data = []

class App(tk.Tk):
    
    def __init__(self):
        
        def gui_mode_reactions(*args):
            
            current_mode = location.get()
            
            network_name_entry.config(fg="#000000", highlightthickness=0, state='disabled')
            ip_address_entry.config(fg="#000000", highlightthickness=0, state='normal')
            subnet_mask_entry.config(fg="#000000", highlightthickness=0, state='normal')
            default_gateway_entry.config(fg="#000000", highlightthickness=0, state='normal')
            
            network_name_entry.delete(0,tk.END)
            ip_address_entry.delete(0,tk.END)
            subnet_mask_entry.delete(0,tk.END)
            default_gateway_entry.delete(0,tk.END)
    
            if(current_mode == 'Manual'):
                submit_button.configure(text="Validate y submit", bg="#Ff9c0a", fg="#000000")
                delete_button.configure(state='disabled', bg='#875454')
                
            elif(current_mode == 'Register'):
                network_name_entry.configure(state='normal')
                submit_button.configure(text="Validate and register", bg="#Ff9c0a", fg="#000000")
                delete_button.configure(state='disabled', bg='#875454')
                
            else:
            
                delete_button.configure(state='normal', bg='#ff0000')
                submit_button.configure(text="Aceptar", bg="#3c7e1f", fg="#ffffff")
                
                current_network_data = {}
                
                for network in network_details:
                    
                    if(network['name'] == current_mode):
                        
                        current_network_data = network
                        break
                
                ip_address_entry.insert(0, current_network_data['address'])
                subnet_mask_entry.insert(0, current_network_data['subnet_mask'])
                default_gateway_entry.insert(0, current_network_data['default_gateway'])
                
                ip_address_entry.config(state='disabled')
                subnet_mask_entry.config(state='disabled')
                default_gateway_entry.config(state='disabled')
        
        def button_mode_actions():
            
            current_mode = location.get()
            
            current_interface = interface.get()
            network_name = network_name_entry.get().strip()
            ip_address = ip_address_entry.get()
            subnet_mask = subnet_mask_entry.get()
            default_gateway = default_gateway_entry.get()
        
            are_errors = False
            
            if(not ip_address_is_valid(ip_address)):
                ip_address_entry.config(fg="#ff0000", highlightthickness=1, highlightbackground="#ff0000", highlightcolor="#ff0000")
                are_errors = True
            else:
                ip_address_entry.config(fg="#000000", highlightthickness=0)
            
            if(not ip_address_is_valid(subnet_mask)):
                subnet_mask_entry.config(fg="#ff0000", highlightthickness=1, highlightbackground="#ff0000", highlightcolor="#ff0000")
                are_errors = True
            else:
                subnet_mask_entry.config(fg="#000000", highlightthickness=0)
            
            if(not ip_address_is_valid(default_gateway)):
                default_gateway_entry.config(fg="#ff0000", highlightthickness=1, highlightbackground="#ff0000", highlightcolor="#ff0000")
                are_errors = True
            else:
                default_gateway_entry.config(fg="#000000", highlightthickness=0)
            
            if(network_name == '' and current_mode == 'Registrar'):
                network_name_entry.config(fg="#ff0000", highlightthickness=1, highlightbackground="#ff0000", highlightcolor="#ff0000")
                are_errors = True
            else:
                network_name_entry.config(fg="#000000", highlightthickness=0)
            
            if(current_mode == 'Registrar'):
                for option in options:
                    if(option == network_name):
                        network_name_entry.config(fg="#ff0000", highlightthickness=1, highlightbackground="#ff0000", highlightcolor="#ff0000")
                        messagebox.showerror('Network alredy exists','Networks must not have the same name')
                        are_errors = True
                        break
                    else:
                        network_name_entry.config(fg="#000000", highlightthickness=0)
                    
            
            if(are_errors):
                return
            
            if(not are_addresses_in_same_network(ip_address, default_gateway)):
                proceed = messagebox.askokcancel("Unmatching networks","IPv4 address and default gateway are on different networks, comtinue?")
                
                if(not proceed):
                    messagebox.showerror("Cancelled","Operation cancelled by user.")
                    return
            
            
            match current_mode:
                
                case 'Register':
                    network_data = {'name': network_name, 'address': ip_address, 'subnet_mask': subnet_mask, 'default_gateway': default_gateway}
                    
                    network_details.append(network_data)
                    options.insert(0, network_name)
                    new_data = [options, network_details]
                    
                    with open('data.pkl', 'wb') as file:
                        
                        pickle.dump(new_data, file)
                    
                    messagebox.showinfo('Restart required', 'It is necessary to restart the app in order to update network values')
                    sys.exit()
                
                case _:
                    change_interface_network_settings(current_interface, ip_address, subnet_mask, default_gateway)
                    
        def delete_button_actions():
            
            current_network = location.get()
            network_details_index = 0
            options_index = 0
            
            for index, network in enumerate(network_details):
                
                if(network['name'] == current_network):
                    
                    network_index = index
                    break
                
            for index, option in enumerate(options):
                
                if(option == current_network):
                    
                    options_index = index
                    break
            
            network_details.pop(network_details_index)
            options.pop(options_index)
            
            new_data = [options, network_details]
            
            print(new_data)
            
            with open('data.pkl', 'wb') as file:
                        
                pickle.dump(new_data, file)
            
            messagebox.showinfo('Restart required', 'It is necessary to restart the app in order to update network values')
            sys.exit()
                    
        super().__init__()
    
        self.title("Cambiar IP")
        self.geometry('{}x{}'.format(WIDTH, HEIGHT))
        self.resizable(False, False)
        self.iconbitmap('Icon.ico')
        
        title_label = tk.Label(self.master, text="Change IPv4", font=('Poppins 20 bold'))
        
        interface_label = tk.Label(self.master, text="Interface:", font=('Poppins 12 bold'))
        
        interface = tk.StringVar(self)
        
        select_list_interface = tk.OptionMenu(self, interface, *network_interfaces)
        select_list_interface.config(width=35)
        
        location_label = tk.Label(self.master, text="Mode:", font=('Poppins 12 bold'))
        
        location = tk.StringVar(self)
        location.trace('w', gui_mode_reactions)
        
        select_list_location = tk.OptionMenu(self, location, *options)
        select_list_location.config(width=35)
        
        network_name = tk.Label(self.master, text="Network name:", font=('Poppins 15'))
        network_name_entry = tk.Entry(self, width=30, justify='center', font=('Poppins 15'))
        network_name_entry.configure(state='disabled')
        
        ip_address_label = tk.Label(self.master, text="IPv4 address:", font=('Poppins 15'))
        ip_address_entry = tk.Entry(self, width=30, justify='center', font=('Poppins 15'))
        
        subnet_mask_label = tk.Label(self.master, text="Subnet mask:", font=('Poppins 15'))        
        subnet_mask_entry = tk.Entry(self, width=30, justify='center', font=('Poppins 15'))
        
        default_gateway_label = tk.Label(self.master, text="Default gateway:", font=('Poppins 15'))  
        default_gateway_entry = tk.Entry(self, width=30, justify='center', font=('Poppins 15'))
        
        space_label = tk.Label(self.master, text="", font=('Poppins 8'))
                
        submit_button = tk.Button(self, text='Submit', font=25, width=32, height=1, bg="#3c7e1f", fg="#ffffff", command=button_mode_actions)
        delete_button = tk.Button(self, text='Delete', font=25, width=32, height=1, bg="#ff0000", fg="#ffffff", command=delete_button_actions)
        
        title_label.pack(pady=15)
        interface_label.pack()
        select_list_interface.pack()
        location_label.pack()
        select_list_location.pack()
        network_name.pack(pady=10)
        network_name_entry.pack()
        ip_address_label.pack(pady=10)
        ip_address_entry.pack()
        subnet_mask_label.pack(pady=10)
        subnet_mask_entry.pack()
        default_gateway_label.pack(pady=10)
        default_gateway_entry.pack()
        
        space_label.pack()
        
        submit_button.pack(pady=5) 
        delete_button.pack(pady=5)
        
        location.set('Manual')
        interface.set(network_interfaces[0])
        
        
def load_data():
    
    options = ['Manual', 'Register']
    network_details = []
    
    auxilar_data = [options, network_details]
    
    file_exists = os.path.exists('data.pkl')
    
    if(file_exists):
        
        with open('data.pkl', 'rb') as file:
            auxilar_data = pickle.load(file)
            return auxilar_data

    with open('data.pkl', 'wb') as file:
        pickle.dump(auxilar_data, file)
        return auxilar_data
    
def ip_address_is_valid(address):
    
    try:
        ipaddress.ip_address(address)
        return True
    
    except Exception:
        return False

def get_ip_address_cidr(address):
    
    address_section_array_str = address.split(sep='.')
    cidr = 0
    
    for section in address_section_array_str:
        
        int_section = int(section)
        binary_section = "{0:b}".format(int_section)
        
        for bit in binary_section:
            
            if(bit == '1'):
                
                cidr += 1
                
    return cidr

def are_addresses_in_same_network(first_address, second_address):
    
    first_address_array = first_address.split(sep='.')
    second_address_array = second_address.split(sep='.')
    
    for index, address_section in enumerate(first_address_array):
        
        if address_section != second_address_array[index] and index != len(second_address_array) - 1:
            
            return False
    
    return True

def get_network_interfaces():
    
    nics = psutil.net_if_addrs().keys()
            
    nics_names = []
    
    for nic in nics:
        nics_names.append(nic)
        
    return nics_names

def change_interface_network_settings(interface, ip, netMask, gateway):
    
    try:
        commands = ('netsh interface ip set address "{}" static {} {} {}').format(interface, ip, netMask, gateway)
        os.system(commands)
        messagebox.showinfo('Success', 'IPv4 parameters changed to interface {}'.format(interface))
    except Exception:
        messagebox.showerror('Failure','The program was unable to change IPv4 parameters')        

def main():
    
    global network_interfaces
    global data
    global options
    global network_details
    
    options, network_details = load_data()
    network_interfaces = get_network_interfaces()

    app = App()
    
    app.mainloop()
    
    
if __name__ == "__main__":
    
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:        
        main()
    