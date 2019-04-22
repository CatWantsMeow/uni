import sys
import json
import socket
import Tkinter
import logging
import DateTime
import tkMessageBox


class Sender(object):

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        try:
            self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except socket.error as e:
            logging.error('Sender initialization has failed: {e[0]}({e[1]})'.format(e=e))
        except Exception as e:
            logging.error('Sender initialization has failed: {e}'.format(e=e))

    def send_message(self, message):
        try:
            address = (self.server_host, self.server_port)
            self.sender.sendto(message, address)
        except socket.error as e:
            logging.error('Error while sending a message: {e}'.format(e=e))

    def close(self):
        self.sender.close()


class Listener(object):

    def __init__(self, host, port, max_message_length=1024, thread_blocking=False):
        self.host = host
        self.port = port
        self.thread_blocking = thread_blocking
        self.max_message_length = max_message_length
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.listener.bind((host, port))
        except socket.error as e:
            logging.error('Server initialization has failed: {e[1]}({e[0]})'.format(e=e))
        except Exception as e:
            logging.error('Server initialization has failed: {e}'.format(e=e))

    def receive_message(self):
        try:
            self.listener.setblocking(self.thread_blocking)
            message, sender = self.listener.recvfrom(self.max_message_length)
            return message, sender
        except socket.error as e:
            return None, None


class Chat(object):

    DEFAULT_USER_NAME = 'popka'

    def __init__(self, port=8888):
        self.app = Tkinter.Tk()
        self.listener = Listener(host='0.0.0.0', port=port)
        self.sender = Sender(server_host='255.255.255.255', server_port=port)

    def init_interface(self):
        self.app.title('The most awesome lan chat')
        self.app.geometry('800x600')

        username_frame = Tkinter.Frame()
        username_frame.pack(side='top', fill='x', pady=10, padx=5)

        message_frame = Tkinter.Frame()
        message_frame.pack(side='top', fill='x', pady=10, padx=5)

        Tkinter.Label(username_frame, text="Username:").pack(side='left')
        self.username_entry = Tkinter.Entry(username_frame, font='Calibri 12')
        self.username_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.username_entry.insert(Tkinter.END, self.DEFAULT_USER_NAME)

        Tkinter.Label(message_frame, text="Message:   ").pack(side='left')
        self.message_entry = Tkinter.Text(message_frame, height=5, width=70, font='Calibri 12')
        self.message_entry.pack(side='left', fill='x', padx=5)
        self.message_entry.bind('<Return>', self.send_message)
        self.message_entry.bind('<Shift-Return>', lambda e: e)

        send_button = Tkinter.Button(message_frame, width=80, text='Send message')
        send_button.pack(side='right', fill='y', expand=True, padx=5)
        send_button.bind('<Button-1>', self.send_message)

        self.messages_log = Tkinter.Text(self.app, font='Calibri 12', spacing1=20)
        self.messages_log.pack(side='top', fill='both', expand=True, padx=5, pady=5)

    def run(self):
        self.init_interface()
        self.app.after(1, self.receive_messages)
        self.app.mainloop()

    def receive_messages(self):
        data, sender = self.listener.receive_message()
        if data and sender:
            try:
                obj = json.loads(data)
                entry = "[{time}] {name}: {msg}\n".format(
                        name=obj["username"],
                        msg=obj["message"],
                        time=DateTime.DateTime().Time()
                )
                self.messages_log.insert(Tkinter.END, entry)
            except KeyError:
                logging.warning('Message with wrong format is received')
            except ValueError:
                logging.warning('Unknown message will received(not json object)')
        self.app.after(1, self.receive_messages)

    def send_message(self, event):
        message = self.message_entry.get('0.0', Tkinter.END).strip()
        self.message_entry.delete('0.0', Tkinter.END)
        username = self.username_entry.get().strip()

        if not message:
            tkMessageBox.showerror('Error', 'Message field is empty')
        elif not username:
            tkMessageBox.showerror('Error', 'Username field is empty')
        else:
            data = {"username": username, "message": message}
            self.sender.send_message(json.dumps(data))


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    chat = Chat()
    chat.run()
