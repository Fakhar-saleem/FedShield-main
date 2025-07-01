import os
import json
import shutil
import socket
import ssl
import threading

from hash import calculate_hash
from tkinter import messagebox
from verification import verification
ssl_socket=None
msg_warning=None
msg_close=None
check=0
upload_rights_list=[]
rights_list=[]
file_list=[]
name_list=[]
access_files=[]
access_names=[]
i=0
upload_right=""
button_color=""
check_duplicate_login=None
def login_credentials_send_message(value, PAno,Uname,Pass):
    if not os.path.exists("captured_images"):
        os.makedirs("captured_images")
    #verification(PAno+"_"+Uname)
    #upload_file_client("login_image", f'captured_images\\{PAno+"_"+Uname}.jpg')
    breaker="@DLP@"
    val=str(value)
    code="login"  #for login
    message=code+breaker+val+breaker+PAno+breaker+Uname+breaker+calculate_hash(Pass)
    send_to_server(message)
def register_client(mesage):
    parts = mesage.split("@DLP@")
    message = tuple(parts)
    #verification(message[1]+"_"+message[2])
    #upload_file_client("login_image", f'captured_images\\{message[1] + "_" + message[2]}.jpg')
    send_to_server(mesage)
    messagebox.showinfo("Registration",f"{message[1]}_{message[2]} has been registered as a new user. Contact Admin to have your upload and download rights")

def upload_file_client(fileName,filePathwithName):
    breaker = "@DLP@"
    code = "sent_file"  # for client file upload
    send_to_server(code + breaker + filePathwithName + breaker + fileName)

    # Send the file data
    with open(filePathwithName, 'rb') as file:
        data = file.read()
    file_size = len(data)
    send_to_server(file_size.to_bytes(4, byteorder='big'))
    send_to_server(data)

    print(f"File '{fileName}' sent successfully.")

def check_alert_for_button(check):
    if check==1:
        send_to_server("check_alert_for_button")
    elif check==2:
        send_to_server("request_alerts")
    else:
        send_to_server("remove_alerts")

def request_file_explorer(folder,username):
    send_to_server("open_download_directory@DLP@"+folder+"@DLP@"+username)
def request_file_explorer_for_rights(folder):
    send_to_server("open_download_directory_for_rights@DLP@"+folder)
def request_userName():
    send_to_server("PAno+userName")
def request_upload_list():
    send_to_server("request_upload_rights_list")
def send_senstivity_list(data,type):
    json_data = json.dumps(data)
    if type==1:
        send_to_server("implement_senstivity"+"@DLP@"+json_data)
    else:
        send_to_server("delete_senstivity"+"@DLP@"+json_data)

def send_rights_download(data,value):
    json_data = json.dumps(data)
    if value==1:
        print("implement")
        send_to_server("access_rights"+"@DLP@"+json_data)
    else:
        print("delete")
        send_to_server("delete_rights" + "@DLP@" + json_data)
def send_rights_upload(data,value):
    json_data = json.dumps(data)
    if value == 1:
        print("implement")
        send_to_server("upload_access_rights" + "@DLP@" + json_data)
    else:
        print("delete")
        send_to_server("delete_upload_rights" + "@DLP@" + json_data)

def request_classfication():
    send_to_server("sensitive_list")
def send_hash(Hash,filename):
    send_to_server("add_hash@DLP@"+str(Hash)+"@DLP@"+filename)
def send_words(words):
    send_to_server("add_words@DLP@"+words)

def receive_messages(ssl_socket):
    global check,msg_warning,msg_close,file_list,name_list,access_files,access_names,upload_right,check_duplicate_login,rights_list,upload_rights_list, button_color
    while True:

            message = ssl_socket.recv(1024).decode('utf-8')
            if(message!=""):
                print("Server:", message)
                parts = message.split("@DLP@")
                value = tuple(parts)
                print(value)
                if(message=="already_logined"):
                    check_duplicate_login=3
                if(message=="change_alert_color"):
                    button_color = "red"
                if (value[0]=="sensitive_list"):
                    file_list = json.loads(value[1])
                elif(value[0]=="register_user"):
                    register_client()
                elif (message=="already_registered"):
                    messagebox.showinfo("Registration","The user is already registered")
                elif (message=="image_verified"):
                    check=1
                elif (value[0]=="sensitive_upload"):
                    if not os.path.exists("quarantined_client"):
                        os.makedirs("quarantined_client")
                    shutil.move(value[1],"quarantined_client\\"+os.path.basename(value[1]))
                elif (message=="No_file_in_doc"):
                    messagebox.showerror("Invalid File","The file you are trying to access is not in the documents folder")
                elif (message=="new_alert_generated"):
                    button_color = "red"
                    send_to_server("red")
                    print("message is red")
                    #check_alert_for_button(2)
                elif (message=="red_button"):
                    button_color="red"
                    print("message is blue")
                elif (value[0]=="qFile_names"):
                    file_list = json.loads(value[1])
                elif(value[0]=="log_names"):
                    file_list=json.loads(value[1])
                elif (value[0]=="send_alert"):
                    receive_file(ssl_socket,value[1],2)
                elif(value[0]=="download_user"):
                    file_list=json.loads(value[1])
                elif (value[0]=="download_for_rights"):
                    rights_list = json.loads(value[1])
                elif (value[0]=="upload_rights_list"):
                    upload_rights_list=json.loads(value[1])
                elif (value[0]=="PAno+userName"):
                    name_list=json.loads(value[1])
                elif (value[0]=="check_rights"):
                    access_files=json.loads(value[1])
                    access_names=json.loads(value[2])
                elif (value[0]=="send_qfile"):
                    receive_qfile(ssl_socket, value[1])
                elif(value[0]=="send_file"):
                    receive_file(ssl_socket,value[1],1)
                elif(value[0]=="sensitive"):
                    messagebox.showwarning(value[0],value[1])
                elif(value[0]=="check_upload_rights"):
                    upload_right=value[1]
                elif(value[0]=="download_access_no"):
                    messagebox.showinfo("Access Right","You do not have the right to download this file")
                if(value[0]=="close" and value[2]=="verified" and value[1]=="Admin"):
                    print("Detected valid login message. Attempting to close window...")
                    msg_close=1
                elif(value[0]=="close" and value[2]=="verified" and value[1]=="User"):
                    msg_close=2
                elif(value[0]=="close" and value[2]=="0"):
                    print("Detected invalid login message. Try Again!!!...")
                    msg_warning = 0


def send_to_server(message):
    global ssl_socket
    if isinstance(message, bytes):
        ssl_socket.sendall(message)
    else:
        ssl_socket.sendall(message.encode('utf-8'))
def start_client():
        global ssl_socket
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations('ssl.pem')
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
        ssl_socket = context.wrap_socket(client_socket,server_hostname='localhost')
        ssl_socket.connect(('127.0.0.1', 59988))
        receive_thread = threading.Thread(target=receive_messages, args=(ssl_socket,))
        receive_thread.start()

def receive_file(ssl_socket_server,name,type):
    file_size_bytes = ssl_socket_server.recv(4)
    file_size = int.from_bytes(file_size_bytes, byteorder='big')
    file_data = b''

    while len(file_data) < file_size:
        remaining_bytes = file_size - len(file_data)
        pdf_chunk = ssl_socket_server.recv(remaining_bytes)
        if not pdf_chunk:
            break
        file_data += pdf_chunk

    if type!=1:
        if not os.path.exists("alerts"):
            os.makedirs("alerts")
        with open("alerts/alerts.txt", 'wb') as file:
            file.write(file_data)
        print("File received successfully.")
    else:
        if not os.path.exists("documents"):
            os.makedirs("documents")
        with open("documents\\" + name, 'wb') as file:
            file.write(file_data)
        print("File received successfully.")

def receive_qfile(ssl_socket_server,name):
    file_size_bytes = ssl_socket_server.recv(4)
    file_size = int.from_bytes(file_size_bytes, byteorder='big')
    file_data = b''
    while len(file_data) < file_size:
        remaining_bytes = file_size - len(file_data)
        pdf_chunk = ssl_socket_server.recv(remaining_bytes)
        if not pdf_chunk:
            break
        file_data += pdf_chunk

    if not os.path.exists("static"):
        os.makedirs("static")
    with open("static\\" + name, 'wb') as file:
        file.write(file_data)
    print("File received successfully.")

def move_qFile(name,type):
    if type==1:
        send_to_server("move_qFile@DLP@"+name)
    else:
        send_to_server("delete_qFile@DLP@"+name)
def request_qFiles(filename,type):
    if type==1:
        send_to_server("get_qFile_names")
    else:
        send_to_server("send_qFile@DLP@"+filename)
def send_download_names(userID,folder,file):
    code="file_name"
    breaker="@DLP@"
    send_to_server(code+breaker+folder+breaker+file+breaker+userID)

def request_check_rights():
    send_to_server("check_rights")
def request_logs(name,type):
    if type==1:
        send_to_server("request_logs")
    else:
        send_to_server("send_log@DLP@"+name)
def check_upload_rights(uname):
    send_to_server("check_upload_rights@DLP@"+uname)

def close_connection():
    send_to_server("close_client")

def close_window_server(type):
    global msg_warning,msg_close,check_duplicate_login
    if (type==1):
        mssg = msg_close
        return str(mssg)
    elif (type==0):
        mssg = msg_warning
        msg_warning= None
        return str(mssg)
    elif (type==3):
        mssg=check_duplicate_login
        return str(mssg)

def make_none():
    global msg_close,check_duplicate_login,rights_list,file_list,name_list,access_names,access_files,button_color
    msg_close=None
    check_duplicate_login=None
    rights_list.clear()
    file_list.clear()
    name_list.clear()
    access_names.clear()
    access_files.clear()

def ret_file_list():
    global file_list
    return file_list
def ret_image():
    global check
    print("check:",check)
    return check
def ret_names_list():
    global name_list
    return name_list
def ret_rights_list():
    global rights_list
    return rights_list
def ret_access_name_list():
    global access_names
    return  access_names
def ret_access_file_list():
    global access_files
    return access_files
def ret_upload_right():
    global upload_right
    return upload_right
def ret_upload_right_list():
    global upload_rights_list
    return upload_rights_list
def ret_button_color():
    global button_color
    return button_color