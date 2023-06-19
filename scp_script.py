import tkinter as tk
from tkinter import ttk
from paramiko import SSHClient
from scp import SCPClient

root = tk.Tk()
root.title("SCP")
root.geometry("300x400")

def clear_button():
    to_entry.delete(0, tk.END)
    entry_from.delete(0, tk.END)
    ip_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def get_data():
    from_1 = entry_from.get()
    to = to_entry.get()
    ip = ip_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    return from_1, to, ip, username, password

def scp_go(check):
    global except_label1
    data = get_data()
    try:
        except_label1.destroy()
    except:
        print("fix")

    if data[0] == "" or data[1] == "" or data[2] == "" or data[3] == "":
        except_label1 = ttk.Label(root, text="Not all required data is filled in!")
        except_label1.pack(side="bottom", fill="x", padx=5, pady=2)
    else:
        try:
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(hostname=str(data[2]),
                        username=str(data[3]),
                        password=str(data[4]),)

            # SCPCLient takes a paramiko transport as its only argument
            scp = SCPClient(ssh.get_transport())

            if check:
                try:
                    scp.put(data[0], data[1], recursive=True)
                except:
                    print("fail")
            else:
                try:
                    scp.get(data[1], data[0],recursive=True)
                except Exception as e:
                    print(e)

            scp.close()
            succes_label = ttk.Label(root, text="Success!")
            succes_label.pack(side="left", fill="x", padx=5, pady=2)
        except Exception as e:
            except_label2 = ttk.Label(root, text=str(e))
            except_label2.pack(side="bottom", fill="x", padx=5, pady=2)


from_label1 = ttk.Label(root,text="Local Machine Path")
from_label1.pack(side="top", fill="x", padx=5, pady=2)

entry_from = ttk.Entry(root)
entry_from.pack(side="top", fill="x", padx=5, pady=2)


to_label1 = ttk.Label(root,text="Remote Host Path")
to_label1.pack(side="top", fill="x", padx=5, pady=2)

to_entry = ttk.Entry(root)
to_entry.pack(side="top", fill="x", padx=5, pady=2)

ip_label = ttk.Label(root,text="IP:")
ip_label.pack(side="top", fill="x", padx=5, pady=2)

ip_entry = ttk.Entry(root)
ip_entry.pack(side="top", fill="x", padx=5, pady=2)

username_label = ttk.Label(root,text="Username:")
username_label.pack(side="top", fill="x", padx=5, pady=2)

username_entry = ttk.Entry(root)
username_entry.pack(side="top", fill="x", padx=5, pady=2)

password_label = ttk.Label(root,text="Password")
password_label.pack(side="top", fill="x", padx=5, pady=2)

password_entry = ttk.Entry(root, show="*")
password_entry.pack(side="top", fill="x", padx=5, pady=2)

send_button = ttk.Button(text="SEND", command=lambda: scp_go(True))
send_button.pack(side="top")

get_button = ttk.Button(text="GET", command=lambda: scp_go(False))
get_button.pack(side="top")

clear_button = ttk.Button(text="Clear all", command=clear_button)
clear_button.pack(side="top")

root.mainloop()
