from tkinter import *
from tkinter import messagebox
from threading import *
import ipaddress
import os
import win32com.shell.shell as shell

OPTIONS = [
"CEAM",
"Centro de computo 1",
"Centro de computo 2",
"Centro de computo 3",
"Manual"
]
    
class App:
    def __init__(self, master) -> None:

        def Manual(*args):
            if(not location.get() == "Manual"):
                ipEntry.config(state="disabled", fg="#000000", highlightthickness=0)
                netMaskEntry.config(state="disabled", fg="#000000", highlightthickness=0)
                gatewayEntry.config(state="disabled", fg="#000000", highlightthickness=0)
                submitButton.configure(text="Aceptar", bg="#3c7e1f", fg="#ffffff")
            else: 
                ipEntry.configure(state="normal")
                netMaskEntry.configure(state="normal")
                gatewayEntry.configure(state="normal")
                submitButton.configure(text="Validar y aceptar", bg="#Ff9c0a", fg="#000000")

        def Submit():
            match location.get():
                case "Manual":
                    ip = ipEntry.get()
                    netMask = netMaskEntry.get()
                    gateway = gatewayEntry.get()

                    validIp = ValidateIpAdress(ip)
                    validNetMask = ValidateIpAdress(netMask)
                    validGate = ValidateIpAdress(gateway)

                    ValidateEntry(validIp, validNetMask, validGate)

                    if(validIp == False or validNetMask == False or validGate == False):
                        messagebox.showerror("Datos no validos","Alguno de los datos que ingresó NO son validos.")
                    else:
                        ValidateGateway(ip, netMask, gateway)

                case "CEAM":
                    ip = "148.237.195.99"
                    netMask = "255.255.255.192"
                    gateway = "148.237.195.65"
                    ShellIpChange(ip, netMask, gateway)

                case "Centro de computo 1":
                    ip = "148.237.194.9"
                    netMask = "255.255.255.0"
                    gateway = "148.237.194.1"
                    ShellIpChange(ip, netMask, gateway)

                case "Centro de computo 2": 
                    ip = "148.237.194.65"
                    netMask = "255.255.255.0"
                    gateway = "148.237.194.1"
                    ShellIpChange(ip, netMask, gateway)

                case "Centro de computo 3":
                    ip = "148.237.194.137"
                    netMask = "255.255.255.0"
                    gateway = "148.237.194.1"
                    ShellIpChange(ip, netMask, gateway)

        def ValidateIpAdress(address):
            try:
                ipObject = ipaddress.ip_address(address)
                return True
            except ValueError:
                return False
        
        def ValidateEntry(validIp, validNetMask, validGate):
            if(validIp == False):
                ipEntry.config(fg="#ff0000", highlightthickness=1,highlightbackground="#ff0000", highlightcolor="#ff0000")
            else:
                ipEntry.config(fg="#000000", highlightthickness=0)
            if(validNetMask == False):
                netMaskEntry.config(fg="#ff0000", highlightthickness=1,highlightbackground="#ff0000", highlightcolor="#ff0000")
            else:
                netMaskEntry.config(fg="#000000", highlightthickness=0)
            if(validGate == False):
                 gatewayEntry.config(fg="#ff0000", highlightthickness=1,highlightbackground="#ff0000", highlightcolor="#ff0000")
            else:
                 gatewayEntry.config(fg="#000000", highlightthickness=0)

        def ShellIpChange(ip, netMask, gateway):
            commands = ('netsh interface ip set address "Ethernet" static {} {} {}').format(ip, netMask, gateway)
            try:
                shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
                messagebox.showinfo("Exito","Cambio de parametros Ipv4 realizado de manera exitosa.")
            except Exception:
                messagebox.showerror("Error","Operacion no autorizada por el usuario.")

        def ValidateGateway(ip, netMask, gateway):
            ipArray = [None] * 4
            gatewayArray = [None] * 4

            ipArray = ip.split(sep=".")
            gatewayArray = gateway.split(sep=".")

            if(ipArray[0] != gatewayArray[0] or ipArray[1] != gatewayArray[1] or ipArray[2] != gatewayArray[2]):
                procced = messagebox.askokcancel("Red diferente","La direccion Ipv4 y la puerta de enlace se encuentran en redes distintas ¿Contnuar?")
                if(procced):
                    ShellIpChange(ip, netMask, gateway)
                else:
                    messagebox.showerror("Cancelado","Operacion cancelada por el usuario.")
            else:
                ShellIpChange(ip, netMask, gateway)
            

        # Defining values
        self.master = master

        Label(self.master, text = "¿En que lugar te encuentras ahora?", font=25).pack(pady=10)

        ipLabel = Label(self.master, text="Direccion ip:", font=20)
        ipEntry = Entry(self.master, width=40)

        netLabel = Label(self.master, text="Mascara de red:", font=20)
        netMaskEntry = Entry(self.master, width=40)

        gateLabel = Label(self.master, text="Puerta de enlace:", font=20)
        gatewayEntry = Entry(self.master, width=40)

        submitButton = Button(self.master, text="Aceptar", font=25, width=40, command=Submit, bg="#3c7e1f", fg="#ffffff")

        location = StringVar(self.master)
        location.trace("w", Manual)
        location.set("CEAM")
        selectList = OptionMenu(self.master, location, *OPTIONS)
        selectList.config(width=35)
        selectList.pack(pady=5)

        # Packing
        ipLabel.pack(pady=3)
        ipEntry.pack()
        netLabel.pack(pady=3)
        netMaskEntry.pack()
        gateLabel.pack(pady=3)
        gatewayEntry.pack()
        submitButton.place(x=21, y=268)

def main():
    root = Tk()
    root.title("Cambiar IP")
    root.geometry('500x315')
    root.resizable(False, False)
    root.iconbitmap("Icon.ico")
    app =  App(root)
    root.mainloop()

if __name__ == "__main__":
    main()