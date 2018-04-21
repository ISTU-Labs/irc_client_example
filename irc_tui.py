#!/usr/bin/env python3
# encoding: ascii

import npyscreen as nps
import curses
import irc_client as irc
import threading as th
import sys
import time

my_nick = 'PyTester'
my_password = 'test'
conn_host = 'irc.freenode.net'
port = 6667

class HistoryBox(nps.BoxTitle):
    _contained_widget = nps.MultiLineEdit

class InputBox(nps.BoxTitle):
    _contained_widget = nps.Textfield

class MainForm(nps.FormBaseNew):

    def create(self):
        self.resize()
        max_y, max_x = self.useable_space()
        #self.channel_box = self.add(nps.TitleFixedText, name = 'Channel name: ')
        self.history_box = self.add(HistoryBox, name='Messange history:', max_height = max_y // 2)
        self.input_box = self.add(InputBox, name='Input:', max_height = 3)

    def afterEdditing(self):
        self.parrentApp.setNextForm(None)

class irc_tui(nps.NPSAppManaged):

    irc_socket = None
    interface = None
    read_thread = None

    def onStart(self):
        self.irc_socket = irc.irc_client()
        self.interface = self.addForm('MAIN', MainForm, name = 'IRC client')
        self.interface.history_box.value = ''
        handlers = {
            '^I' : self.focus_input,
            '^H' : self.focus_history,
            '^A' : self.send_msg,
            '^F' : self.input_clear,
            '^D' : self.exit_app
        }
        self.interface.add_handlers(handlers)
        

    def send_msg(self, _input):
        line = self.interface.input_box.value
        if line == '':
            return
        if line == '/START_READ':
            self.start_read()
        else:
            self.irc_socket.cmd_parse(line)
            
        self.interface.input_box.value = ''
        self.interface.input_box.display()
        
    def input_clear(self, _input):
        self.interface.input_box.value = ''
        self.interface.input_box.display()
     
    def focus_input(self, _input):
        pass

    def focus_history(self, _input):
        pass

    
    def exit_app(self, _input):
        sys.exit()

    def display_current_channel(self):
        self.interface.channel_box.value = self.irc_socket.current_channel
        self.interface.channel_box.display()
    
    def printer(self, text):
        self.interface.history_box.value += text
        self.interface.history_box.display()
        
    def read_socket(self):
        self.irc_socket.socket.settimeout(0)
        n = 256
        while True:
            try:
                buffer = self.irc_socket.socket.recv(n)
                if buffer is not None and buffer != b'':
                    text = buffer.decode(self.irc_socket.charset)
                    self.printer(text)
            except:
                pass
            else:
                pass
            finally:
                pass
            
    
    def start_read(self):
        self.read_thread = th.Thread(target = self.read_socket)
        self.read_thread.start()

def main():
    app = irc_tui()
    app.run()
    if app.read_thread is not None:
        app.read_thread.join()
    
if __name__ == "__main__":
    main()
