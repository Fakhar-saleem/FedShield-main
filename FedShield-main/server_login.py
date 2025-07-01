import json
import shutil
import socket
import os
import ssl
import threading
import sqlite3
import time
import uuid
from test import add_words
from datetime import datetime
from data import search_user_by_name
from hash import calculate_hash
from matching import calculate_txt_hash,keywordMatching
#from detect_face2 import detect_face
from nlp import nlp_check
import classifer
user=""
user_type=""
clients = {}
name=""
session_id_list=[]
Logined=[]
def handle_client(ssl_client_socket, client_address,session_id):
    global name
    print(f"Connection from {client_address} with Session ID {session_id} has been established.")
    while True:
        try:
                message = ssl_client_socket.recv(1024).decode('utf-8')
                print(f"Received from {session_id}: {message}")
                parts = message.split("@DLP@")
                value = tuple(parts)
                code = value[0]
                if (message=="close_client"):
                    del clients[session_id]
                    print(user)
                    Logined.remove(user)
                    if session_id in session_id_list:
                        session_id_list.remove(session_id)
                    ssl_client_socket.close()
                    break
                if (code=="add_hash"):
                    add_hash(value[1],value[2])
                if (code=="add_words"):
                    add_words(value[1])
                if (code == "login"):
                    searching_verifying_name(session_id,message)
                if (message=="red"):
                    send_alert_to_all_admins("change_alert_color")
                elif(code=="register_user"):
                    register_user(session_id,message)
                elif (message=="sensitive_list"):
                    sensitivty_classification(session_id)
                elif (message=="check_alert_for_button"):
                    check_alert_for_button(session_id)
                elif (code=="move_qFile"):
                    move_qFile(value[1],1)
                elif (code=="delete_qFile"):
                    move_qFile(value[1],2)
                elif (message=="remove_alerts"):
                    if not os.path.exists("alerts"):
                        os.makedirs("alerts")
                    os.remove("alerts\\alerts.txt")
                elif (message=="request_alerts"):
                    send_alert(session_id)
                elif (message=="request_upload_rights_list"):
                    list_upload_rights(session_id)
                elif (message=="get_qFile_names"):
                    qFile_names(session_id)
                elif (code=="send_qFile"):
                    if not os.path.exists("quarantined"):
                        os.makedirs("quarantined")
                    send_qfile(session_id, "quarantined", value[1])
                elif(code=="sent_file"):
                    storing_received_file(ssl_client_socket,session_id,value[1],value[2])
                elif (code=="open_download_directory"):
                    open_directory_for_download_user(session_id,value[1],value[2])
                elif (code=="open_download_directory_for_rights"):
                    open_directory_for_download_rights(session_id,value[1])
                elif(code=="file_name"):
                    send_file(session_id,value[1],value[2])
                elif (code=="PAno+userName"):
                    send_PAnoanduserNames(session_id)
                elif(code=="access_rights"):
                    implement_rights_download(json.loads(value[1]))
                elif (message=="check_rights"):
                    send_rights(session_id)
                elif (code=="delete_rights"):
                    delete_rights(json.loads(value[1]))
                elif(code=="check_upload_rights"):
                    check_upload_rights(session_id,value[1])
                elif(code=="upload_access_rights"):
                    change_upload_rights(json.loads(value[1]),1)
                elif (code == "delete_upload_rights"):
                    change_upload_rights(json.loads(value[1]), 0)
                elif (code=="implement_senstivity"):
                    change_senstivity(value[1],1)
                elif (code=="delete_senstivity"):
                    change_senstivity(value[1],0)
                elif (code=="logs"):
                    create_logs()
                elif (message=="request_logs"):
                    send_log_names(session_id)
                elif (code=="send_log"):
                    if not os.path.exists("logs"):
                        os.makedirs("logs")
                    send_file(session_id,"logs",value[1])
        except:
                if session_id in clients:
                    del clients[session_id]
                    if session_id in session_id_list:
                        session_id_list.remove(session_id)
                if user and Logined:
                    Logined.remove(user)
                ssl_client_socket.close()
                break
def add_hash(Hash,filename):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO ClassifyFiles VALUES(?,?)', (Hash,filename))
    except:
        print("already exist__ add_hash()")
    cursor.close()
    conn.commit()
    conn.close()
def register_user(session_id,messge):
    parts = messge.split("@DLP@")
    message = tuple(parts)
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Users VALUES(?,?,?)', (message[1],message[2],calculate_hash(message[3])))
        cursor.execute('INSERT INTO AccessRightsUpload VALUES(?,?)', (message[1]+"_"+message[2], 'N'))
    except Exception as e:
        if e=="UNIQUE constraint failed: Users.PAno":
            send_to_clients(session_id,"already_registered")

    time.sleep(2)
    if os.path.exists(f"received_images\\{message[1]}_{message[2]}.jpg"):
        os.makedirs(f"compare\\{message[1]}_{message[2]}")
        shutil.move(f"received_images\\{message[1]}_{message[2]}.jpg",f"compare\\{message[1]}_{message[2]}")
    cursor.close()
    conn.commit()
    conn.close()
    create_logs(f"registration@DLP@{message[1]}_{message[2]}",[],[])
def sensitivty_classification(session_id):
    code = "sensitive_list"
    breaker = "@DLP@"
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Execute a query to fetch data from a specific column
    cursor.execute("SELECT FileID FROM ClassifyFiles")
    rows = cursor.fetchall()
    # Close the cursor and database connection
    cursor.close()
    conn.close()
    data = [f"{row[0]}" for row in rows]
    json_upload_rights_list = json.dumps(data)
    send_to_clients(session_id, code + breaker +json_upload_rights_list )

def change_senstivity(insert,value):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    print(insert)
    data=json.loads(insert)
    if not os.path.exists("documents"):
        os.makedirs("documents")
    if not os.path.exists("quarantined"):
        os.makedirs("quarantined")
    print("inside")
    if value==1:
        for i in range(len(data)):
            hash=calculate_txt_hash("documents\\"+data[i])
            shutil.move("documents\\"+data[i],"quarantined\\"+data[i])
            try:
                cursor.execute('INSERT INTO ClassifyFiles VALUES (?,?)',(str(hash),data[i]))
            except:
                print("carry_on_ change_sentivity()")

    cursor.close()
    conn.commit()
    conn.close()

def move_qFile(filename,type):
    if not os.path.exists("documents"):
        os.makedirs("documents")
    if not os.path.exists("quarantined"):
        os.makedirs("quarantined")

    if type==1:
        Hash = calculate_txt_hash("quarantined\\" + filename)
        shutil.move("quarantined\\"+filename,"documents")
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM ClassifyFiles WHERE Hash=?", (Hash,))
        except:
            print("it doesnt exist _ carryon _ moveqFile()")
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    else:
        os.remove("quarantined\\"+filename)
def check_alert_for_button(session_id):
    if not os.path.exists("alerts"):
        os.makedirs("alerts")

    if os.path.exists("alerts\\alerts.txt"):
        if os.path.getsize("alerts\\alerts.txt") != 0 :
            send_to_clients(session_id,"red_button")

def qFile_names(session_id):
    if not os.path.exists("quarantined"):
        os.makedirs("quarantined")
    directory = "quarantined"
    files = os.listdir(directory)
    breaker = "@DLP@"
    code = "qFile_names"  # for login
    json_data = json.dumps(files)
    send_to_clients(session_id, code + breaker + json_data)

def send_log_names(session_id):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    directory = "logs"
    files = os.listdir(directory)
    breaker = "@DLP@"
    code = "log_names"  # for login
    json_data = json.dumps(files)
    send_to_clients(session_id, code + breaker + json_data)

def send_alert(session_id):
    breaker = "@DLP@"
    code = "send_alert"  # for client file upload
    send_to_clients(session_id, code + breaker + "alerts.txt")
    if not os.path.exists("alerts"):
        os.makedirs("alerts")

    # Send the file data
    with open("alerts\\alerts.txt", 'rb') as file:
        data = file.read()

    file_size = len(data)
    send_to_clients(session_id, file_size.to_bytes(4, byteorder='big'))
    send_to_clients(session_id, data)

    print(f"File has been sent successfully.")
    create_logs("Download@DLP@" + "alert" , [], [])

def send_to_clients(session_id, message):
    try:
        ssl_socket = clients.get(session_id)
        if ssl_socket:
            if isinstance(message, bytes):
                ssl_socket.sendall(message)
            else:
                ssl_socket.sendall(message.encode('utf-8'))
        else:
            print(f"Client with Session ID {session_id} not found.")
    except Exception as e:
        print(f"Error sending message to client with Session ID {session_id}: {e}")

def send_alert_to_all_admins(message):
    global session_id_list
    for i in range(len(session_id_list)):
        try:
            ssl_socket = clients.get(session_id_list[i])
            if ssl_socket:
                if isinstance(message, bytes):
                    ssl_socket.sendall(message)
                else:
                    ssl_socket.sendall(message.encode('utf-8'))
            else:
                print(f"Client with Session ID {session_id_list[i]} not found.")
        except Exception as e:
            print(f"Error sending message to client with Session ID {session_id_list[i]}: {e}")


def open_directory_for_download_user(session_id,folderName,username):
    access_files=[]
    directory=folderName
    files = os.listdir(directory)
    breaker = "@DLP@"
    code = "download_user"  # for login
    for i in range(len(files)):
        print(files[i])
        if(check_download_rights(files[i],username)=="download_access_yes"):
            if check_classification(folderName, files[i]):
                print("into NLP")
                if check_nlp(folderName, files[i]):
                    access_files.append(files[i])
    json_data = json.dumps(access_files)
    send_to_clients(session_id,code+breaker+json_data)

def searching_verifying_name(session_id,message):
    login_check=False
    global user,user_type,Logined
    parts = message.split("@DLP@")
    value = tuple(parts)
    breaker = "@DLP@"
    code = "close"
    cond="1"
    for i in range(len(Logined)):
        if(Logined[i]==value[2]+"_"+value[3]):
            send_to_clients(session_id,"already_logined")
            login_check=True
            print("already:",Logined)

    if not login_check:
        search_result=search_user_by_name(value[1],value[2])
        if (value[1] == "1"):
            var = "Admin"
        else:
            var = "User"
        if search_result==0:
            send_to_clients(session_id, code + breaker + var + breaker + str(0))
            return

        if (value[1] == "1"):
            var = "Admin"
        else:
            var = "User"
        
        if(search_result[1]==value[3] and search_result[2]==value[4]):
            time.sleep(2)
            #condition=detect_face(search_result[0]+"_"+search_result[1])
            condition=1
            cond=str(condition)
        else:
            print("hellooeesdas")
            send_to_clients(session_id, code + breaker + var + breaker + str(0))
            return
        if(value[1] == "1" ):
            var = "Admin"
            session_id_list.append(session_id)
        else: var = "User"
        if cond == "1":
            cond="verified"
            Logined.append(value[2]+"_"+value[3])
        else:
            cond="Invalid"
            generate_alerts(session_id," Type: "+str(var)+"  PA No: "+str(value[2])+" UserID: "+ str(value[3])+" has tried "+cond+" login")

        user_type=value[1]
        user=value[2]+"_"+value[3]
        create_logs("Login"+breaker+var+breaker+value[2]+ breaker+ value[3]+breaker+cond, [], [])
        send_to_clients(session_id,code+breaker+var+breaker+cond)
def generate_alerts(session_id,message):
    global user
    if not os.path.exists("alerts"):
        os.makedirs("alerts")
    with open("alerts\\alerts.txt", 'a') as file:
        file.write(user+" "+message+"\n")
    print("alert generated")
    send_to_clients(session_id,"new_alert_generated")
def open_directory_for_download_rights(session_id,folderName):
    directory = folderName
    files = os.listdir(directory)
    breaker = "@DLP@"
    code = "download_for_rights"  # for login
    json_data = json.dumps(files)
    send_to_clients(session_id, code + breaker + json_data)

def storing_received_file(ssl_client_socket,session_id,filepathwithName,condition):
    print("here")
    name=os.path.basename(filepathwithName)
    file_size_bytes = ssl_client_socket.recv(4)
    file_size = int.from_bytes(file_size_bytes, byteorder='big')
    file_data = b''
    while len(file_data) < file_size:
        remaining_bytes = file_size - len(file_data)
        pdf_chunk = ssl_client_socket.recv(remaining_bytes)
        if not pdf_chunk:
            break
        file_data += pdf_chunk
    if not os.path.exists("received_images"):
        os.makedirs("received_images")

    _, ext = os.path.splitext(name)
    print(ext)
    if ext == ".jpg" and condition=="login_image":
        with open("received_images\\" + name, 'wb') as file:
            file.write(file_data)

    else:
        if not os.path.exists("documents"):
            os.makedirs("documents")
        print("check0.1")
        with open("documents\\"+name, 'wb') as file:
            file.write(file_data)
            print("check0.2")
        
        # Check if file is an image
        if ext.lower() in ['.jpg', '.jpeg', '.png']:
            # Perform combined image and text classification
            result = classifer.combined_prediction(f"documents\\{name}")
            print("check0.3")
            if result == 1:  # If classified as sensitive
                if not os.path.exists("quarantined"):
                    os.makedirs("quarantined")
                shutil.move(f"documents\\{name}", f"quarantined\\{name}")
                generate_alerts(session_id, 
                    f"has tried to upload sensitive image {name}")
                send_to_clients(session_id, f"sensitive_upload@DLP@{filepathwithName}")
                create_logs(f"Tried_upload@DLP@{name}", [], [])
                create_logs(f"Sensitive_Image@DLP@{name}", [], [])
                print("check0.4")
                return
            else:
                print("check0.5")
                create_logs("Upload@DLP@"+name,[],[])
                return
        check_file=check_hash_upload(session_id,"documents",filepathwithName)
        print("final check", check_file)
        if check_file:
            create_logs("Upload@DLP@"+name,[],[])
        else:
            create_logs("Tried_upload@DLP@"+name,[],[])

def check_hash_upload(session_id,folder,filepathwithName):
    global user
    hash = calculate_txt_hash(folder + "\\" + os.path.basename(filepathwithName))
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Hash FROM ClassifyFiles')
    rows = cursor.fetchall()
    file_info = [f"{row[0]}" for row in rows]
    cursor.close()
    conn.close()
    print("check1")
    for i in range(len(file_info)):
        if file_info[i]==hash:
            generate_alerts(session_id,f"has tried to upload file named {os.path.basename(filepathwithName)} which has failed hash comparison test. The file has been quarantined.")
            os.remove("documents\\"+os.path.basename(filepathwithName))
            print("check2")
            send_to_clients(session_id,"sensitive_upload@DLP@"+filepathwithName)
            return False
    print("check3")
    if check_nlp_upload(session_id,folder,filepathwithName):
        return True
    else:
        return False

def check_nlp_upload(session_id,folder,filepathwithName):
    global user
    if not os.path.exists("documents"):
        os.makedirs("documents")

    if nlp_check(folder+"\\"+os.path.basename(filepathwithName))==1:
        print("check4")
        if(keywordMatching(folder+"\\"+os.path.basename(filepathwithName))):
            print("check5")
            generate_alerts(session_id,f"has tried to upload file named {os.path.basename(filepathwithName)} which has failed word matching test. It has been quaratined.")
            os.remove("documents\\"+os.path.basename(filepathwithName))
            send_to_clients(session_id,"sensitive_upload@DLP@"+filepathwithName)
            return False
        else:
            return True
    else:
        generate_alerts(session_id,f"has tried to upload file named {os.path.basename(filepathwithName)} which has failed NLP test. It has been quaratined.")
        os.remove("documents\\"+os.path.basename(filepathwithName))
        send_to_clients(session_id,"sensitive_upload@DLP@"+filepathwithName)
        return False

def send_file(session_id,folder,filename):
    breaker = "@DLP@"
    code = "send_file"  # for client file upload
    send_to_clients(session_id,code + breaker + filename)

    # Send the file data
    with open(folder + "\\" + filename, 'rb') as file:
        data = file.read()

    file_size = len(data)
    send_to_clients(session_id,file_size.to_bytes(4, byteorder='big'))
    send_to_clients(session_id,data)

    print("hi")
    print(f"File '{filename}' sent successfully.")
    print("helllo")
    create_logs("Download@DLP@"+filename,[],[])
    print("world")

def send_qfile(session_id,folder,filename):
    breaker = "@DLP@"
    code = "send_qfile"  # for client file upload
    send_to_clients(session_id,code + breaker + filename)
    # Send the file data
    with open(folder + "\\" + filename, 'rb') as file:
        data = file.read()
    file_size = len(data)
    send_to_clients(session_id,file_size.to_bytes(4, byteorder='big'))
    send_to_clients(session_id,data)

    print(f"File '{filename}' sent successfully.")
    create_logs("Download@DLP@"+filename,[],[])


def send_PAnoanduserNames(session_id):
    code="PAno+userName"
    breaker="@DLP@"
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Execute a query to fetch data from a specific column
    cursor.execute('SELECT PAno, userName FROM Users')

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Extract the column data from the rows and store it in a list
    data = [f"{row[0]}_{row[1]}" for row in rows]
    json_data = json.dumps(data)
    send_to_clients(session_id,code+breaker+json_data)

def implement_rights_download(data):
    files=[]
    names=[]
    for i in range(len(data)):
        parts = data[i].split("@access_breaker@")
        divison=tuple(parts)
        files.append(divison[0])
        names.append(divison[1])

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    for i in range(len(files)):
        cursor.execute('INSERT INTO AccessRightsDownload VALUES (?, ?)', (names[i], files[i]))
    conn.commit()
    cursor.close()
    conn.close()
    create_logs("Give_Rights",files,names)


def send_rights(session_id):
    code = "check_rights"
    breaker = "@DLP@"
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    # Execute a query to fetch data from a specific column
    cursor.execute('SELECT UserID, FileID FROM AccessRightsDownload')

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Extract the column data from the rows and store it in a list
    data = [f"{row[0]}@access_breaker@{row[1]}" for row in rows]
    files=[]
    names=[]
    for i in range(len(data)):
        parts = data[i].split("@access_breaker@")
        divison = tuple(parts)
        names.append(divison[0])
        files.append(divison[1])
    json_files = json.dumps(files)
    json_names=json.dumps(names)
    send_to_clients(session_id,code + breaker + json_files+breaker+json_names)

def list_upload_rights(session_id):
    code = "upload_rights_list"
    breaker = "@DLP@"
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Execute a query to fetch data from a specific column
    cursor.execute("SELECT UserID, Access FROM AccessRightsUpload")
    rows = cursor.fetchall()
    # Close the cursor and database connection
    cursor.close()
    conn.close()
    data = [f"{row[0]}@access_breaker@{row[1]}" for row in rows]
    json_upload_rights_list = json.dumps(data)
    send_to_clients(session_id, code + breaker +json_upload_rights_list )

def delete_rights(data):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    files = []
    names = []
    for i in range(len(data)):
        parts = data[i].split("@access_breaker@")
        divison = tuple(parts)
        files.append(divison[0])
        names.append(divison[1])

    # Execute a query to fetch data from a specific column
    for i in range(len(files)):
        cursor.execute("DELETE FROM AccessRightsDownload WHERE UserID=? AND FileID=?", (names[i], files[i]))
    conn.commit()
    cursor.close()
    conn.close()
    create_logs("Delete_Rights",files,names)

def check_upload_rights(session_id,userID):
    code = "check_upload_rights"
    breaker = "@DLP@"
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Execute a query to fetch data from a specific column
    cursor.execute("SELECT Access FROM AccessRightsUpload WHERE UserID=?",(userID,))
    row = cursor.fetchone()
    access_val=str(row[0])
    # Close the cursor and database connection
    cursor.close()
    conn.close()

    send_to_clients(session_id,code+breaker+access_val)

def change_upload_rights(data,value):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Execute a query to fetch data from a specific column
    if value==1:

        for i in range(len(data)):

            cursor.execute('UPDATE AccessRightsUpload SET Access = "Y" WHERE UserID=(?)', (data[i],))

    else:
        for i in range(len(data)):
            cursor.execute('UPDATE AccessRightsUpload SET Access = "N" WHERE UserID=(?)', (data[i],))

    # Close the cursor and database connection
    conn.commit()
    cursor.close()
    conn.close()

def check_download_rights(file,userID):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    # Execute a query to fetch data from a specific column
    cursor.execute('SELECT UserID, FileID FROM AccessRightsDownload where UserID=?',(userID,))
    rows = cursor.fetchall()
    # Close the cursor and database connection
    cursor.close()
    conn.close()
    data = [f"{row[0]}***{row[1]}" for row in rows]
    print(data)
    for i in range(len(data)):
        if data[i]==userID+"***"+file:
            return "download_access_yes"
    return "download_access_no"

def check_classification(folder,filename):
    if not os.path.exists("quarantined"):
        os.makedirs("quarantined")
    hash = calculate_txt_hash(folder + "\\" + filename)
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Hash FROM ClassifyFiles')
    rows = cursor.fetchall()
    file_info = [f"{row[0]}" for row in rows]
    print("hashes: ",file_info)
    cursor.close()
    conn.close()
    hashes = file_info
    for i in range(len(hashes)):
        if (hash == hashes[i]):
            shutil.move(folder + "\\" + filename,"quarantined")
            return False
    return True
"""
        for i in range(len(hashes)):
        if user_class==3:
            return True
        elif (hash == hashes[i]):
            if user_class>=int(classification_files[i]):
                return True
            else:
                return False
    return True
"""

def check_nlp(folder,filename):
    global user
    if not os.path.exists("quarantined"):
        os.makedirs("quarantined")
        if nlp_check(folder+"\\"+filename)==1:
            if(keywordMatching(folder+"\\"+filename)):
                conn = sqlite3.connect('example.db')
                cursor = conn.cursor()
                hash = calculate_txt_hash(folder+"\\"+filename)
                try:
                    cursor.execute('INSERT INTO ClassifyFiles VALUES(?,?)', (hash, filename))
                except:
                    print("carry_on check_nlp()")
                shutil.move(folder + "\\" + filename, "quarantined\\" + filename)
                cursor.close()
                conn.commit()
                conn.close()
                print("word matching it is")
                return False
            else:
                return True
        else:
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()
            hash = calculate_txt_hash(folder + "\\" + filename)
            cursor.execute('INSERT INTO ClassifyFiles VALUES(?,?)', (hash, filename))
            shutil.move(folder + "\\" + filename, "quarantined\\" + filename)
            cursor.close()
            conn.commit()
            conn.close()
            print("else it is")
            return False
    return True
def create_logs(message,files,names):
    global user
    if not os.path.exists("logs"):
        os.makedirs("logs")

    parts = message.split("@DLP@")
    value = tuple(parts)
    current_date=datetime.now().date()
    current_time=datetime.now().time()
    if(value[0]=="Login"):
        with open("logs\\"+str(current_date)+" Login_logs.txt", 'a') as file:
            file.write(str(current_time)+"\tType: "+value[1]+"\tPA no. : "+value[2]+"\tUsername: "+value[3]+"\tVerified: "+value[4]+"\n")
    if (value[0] == "Upload"):
        with open("logs\\" + str(current_date) + " upload_logs.txt",'a') as file:
            file.write(str(current_time)+"\tName: "+user+"\tFunction: Uploaded\tFile_Name: "+value[1]+"\n")
    if (value[0]=="Tried_upload"):
        with open("logs\\" + str(current_date) + " Quarantined_upload_logs.txt",'a') as file:
            file.write(str(current_time)+"\tName: "+user+"\tFunction: Uploaded\tFile_Name: "+value[1]+"\n")
    if (value[0] == "Download"):
        with open("logs\\" + str(current_date) + " download_logs.txt",'a') as file:
            file.write(str(current_time)+"\tName: "+user+"\tFunction: Downloaded\tFile_Name: "+value[1]+"\n")
    if(message == "Give_Rights"):
        for i in range(len(files)):
            with open("logs\\" + str(current_date) + " access_rights_logs.txt",'a') as file:
                file.write(str(current_time)+"\tName: "+user+"\tgave download access right to "+names[i]+" for file "+files[i]+"\n")
    if (message == "Delete_Rights"):
        for i in range(len(files)):
            with open("logs\\" + str(current_date) + " access_rights_logs.txt", 'a') as file:
                file.write(str(current_time) + "\tName: " + user + "\tremoved download access right to " + names[i] + " for file " + files[i]+"\n")
    if (value[0] == "registration"):
        with open("logs\\" + str(current_date) + " registration_logs.txt",'a') as file:
            file.write(str(current_time)+"\tName: "+user+"\tFunction: Registered a new user named\t"+value[1]+"\n")
    if (value[0] == "Sensitive_Image"):
            with open("logs\\" + str(current_date) + " sensitive_image_logs.txt", 'a') as file:
                file.write(str(current_time) + "\tName: " + user + 
                        "\tFunction: Detected Sensitive Image\tFile_Name: " + 
                        value[1] + "\n")


    return

def start_server():
    global session_id_list
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('ssl.pem', 'private.key')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
    server_address = ('0.0.0.0', 59988)
    server_socket.bind(server_address)
    server_socket.listen(5)

    ssl_socket = context.wrap_socket(server_socket,server_side=True)
    print("Server is listening for incoming connections...")

    while True:
        ssl_client_socket, client_address = ssl_socket.accept()
        session_id = str(uuid.uuid4())
        clients[session_id] = ssl_client_socket
        client_thread = threading.Thread(target=handle_client, args=(ssl_client_socket, client_address, session_id))
        client_thread.start()

start_server()
