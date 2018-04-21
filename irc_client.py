import socket
import traceback

#socket wrap

class irc_client():

    #logical attributes
    nick = None
    password = None
    realname = None
    host = None
    conn_port = None
    my_port = None
    charset = None

    #usually ignoring attributes
    hostname = None
    servername = None
    
    #support attributes
    socket = None
    status_msg = None

    #cache attributes
    current_channel = None

    def __init__(self):
        pass
    
    def init_data(self, nick = None,
                 password = None,
                 realname = None,
                 host = None,
                 conn_port = 6667,
                 charset = 'ascii',
                 my_port = 8196,
                 hostname = None,
                 servername = None):
        try:
            self.nick = nick
            self.password = password
            self.realname = realname
            self.host = host
            self.conn_port = conn_port
            self.charset = charset
            self.my_port = my_port
            self.hostname = hostname
            self.servername = servername
            self.current_channel = None
        except:
            traceback.print_exc()
            self.status_msg = 'IRC_client: data was not init'
        else:
            self.status_msg = None
        finally:
            self.ret_status_msg()
    
    #need redef
    
    #help printing method

    def ret_help_msg(self):
        pass
    
    #error printing method

    def ret_status_msg(self):
        if self.status_msg is not None:
            print(self.status_msg)
        return self.status_msg

    def printer(self, text):
        if text is not None and text != '':
            print(text)

    #end of need redef
    
    #low level
    
    def create_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', self.my_port))
        except:
            traceback.print_exc()
            self.status_msg = 'Socket: object was not created.'
        else:
            self.status_msg = None
        finally:
            self.ret_status_msg()
        
    def low_level_connect(self):
        try:
            self.socket.connect((self.host, self.conn_port))
        except:
            traceback.print_exc()
            self.status_msg = 'Socket: low level connect to ' + self.host + ':' + str(self.conn_port) + ' was failed.'
        else:
            self.status_msg = None
        finally:
            self.ret_status_msg()

    def low_level_disconnect(self):
        try: 
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.socket = None
        except:
            traceback.print_exc()
            self.status_msg = 'Socket: low level disconnect was failed.'
        else:
            self.status_msg = None
        finally:
            self.ret_status_msg()

    def socket_recreate(self):
        try:
            if self.socket is not None:
                self.low_level_disconnect()
            self.create_socket()
        except:
            traceback.print_exc()
            self.status_msg = 'Socket: object recreation was failed.'
        else:
            self.status_msg = None
        finally:
            self.ret_status_msg()
        
    #middle level
    
    def create_cmd(self, prefix, cmdname, params):
        try:
            if prefix is None:
                command = ''
            else:
                command = ':' + prefix + ' '
            command += cmdname
            if params is not None:
                command += ' ' + params
            command += '\r\n'    
        except:
            traceback.print_exc()
            self.status_msg = 'IRC level: command creation was failed.'
            command = None
        else:
            self.status_msg = None
        finally:
            self.ret_status_msg()
            return command
        
    def send_cmd(self, prefix, cmdname, params):
        try:
            command = self.create_cmd(prefix, cmdname, params)
            byte_command = command.encode(self.charset)
            if command is not None:
                self.socket.send(byte_command)
        except:
            traceback.print_exc()
            self.status_msg = 'Socket: message sending was failed.'
        else:
            self.status_msg = None
        finally:
            self.ret_status_msg()

    #commands ping-pong

    def cmd_PING(self, reciever = None):
        if reciever is not None:
            self.send_cmd(None, 'PING', reciever)

    def cmd_PONG(self, reciever = None):
        if reciever is not None:
            self.send_cmd(None, 'PONG', '{0} {1}'.format(self.nick, reciever))

    #commands for registration and connection

    def cmd_PASS(self, password = None):
        if password is not None:
            self.password = password
        self.send_cmd(None, 'PASS', self.password)

    def cmd_NICK(self, nick = None):
        if nick is not None:
            self.nick = nick
        self.send_cmd(None, 'NICK', self.nick)

    def cmd_USER(self):
        self.send_cmd(None, 'USER', '{0} {1} {2} {3}'.format(self.nick, self.hostname, self.servername, self.realname))

    def cmd_OPER(self):
        self.send_cmd(None, 'OPER', "{0} {1}".format(self.nick, self.password))
    
    def cmd_QUIT(self, reason = None):
            self.send_cmd(None, 'QUIT', reason)

    #basic commands for operation with channels

    def cmd_LIST(self, temp = None):
        self.send_cmd(None, 'LIST', temp)

    def cmd_NAMES(self, channelname = None):
        self.send_cmd(None, 'NAMES', channelname)

    def cmd_TOPIC(self, channelname = None):
        if channelname is not None:
            self.send_cmd(None, 'TOPIC', channelname)
    
    def cmd_JOIN(self, channelname = None):
        if channelname is not None:
            self.send_cmd(None, 'JOIN', channelname)

    def cmd_PART(self, channelname = None):
        if channelname is not None:
            self.send_cmd(None, 'PART', channelname)

    def cmd_INVITE(self, nick = None, channelname = None):
        if nick is not None and channelname is not None:
            self.send_cmd(None, 'INVITE', '{0} {1}'.format(nick, channelname))

    #commands for operators
    
    def cmd_KICK(self, nick = None, channelname = None, reason = None):
        if nick is not None and channelname is not None:
            if reason is None:
                self.send_cmd(None, 'KICK', '{0} {1}'.format(channelname, nick))
            else:
                self.send_cmd(None, 'KICK', '{0} {1} {2}'.format(channelname, nick, reason))

    def cmd_KILL(self, nick = None, reason = None):
        if nick is not None:
            if reason is None:
                self.send_cmd(None, 'KILL', nick)
            else:
                self.send_cmd(None, 'KILL', '{0} {1}'.format(nick, reason))

    #commands for messanging

    def cmd_PRIVMSG(self, reciever = None, text = None):
        if reciever is not None and text is not None:
            self.send_cmd(None, 'PRIVMSG', '{0} {1}'.format(reciever, text))

    def cmd_NOTICE(self, reciever = None, text = None):
        if reciever is not None and text is not None:
            self.send_cmd(None, 'NOTICE', '{0} {1}'.format(reciever, text))

    def cmd_AWAY(self, text = None):
        if text is None:
            self.send_cmd(self.nick, 'AWAY', None)
        else:
            self.send_cmd(None, 'AWAY', text)


    #other commands
    
    def cmd_WHO(param = None):
            self.send_cmd(None, 'WHO', param)

    #high level
        
    #logical blocks of commands

    def set_port(self, port = 8196):
        self.my_port = port
    
    def connect(self, host = None, port = None):
        self.host = host
        self.conn_port = port
        self.socket_recreate()
        self.low_level_connect()

    def set_info(self, nick, password, realname,
                 charset = 'ascii',
                 hostname = 'irc_hand_made_client',
                 servername = 'server'):
        self.nick = nick
        self.password = password
        self.realname = realname
        self.charset = charset
        self.hostname = hostname
        self.servername = servername
    
    def login(self):
        if self.password is not None:
            self.cmd_PASS()
        self.cmd_USER()
        self.cmd_NICK()

    def goto_channel(self, channelname = None):
        self.current_channel = channelname  

    def break_connection(self):
        self.cmd_QUIT()
        self.low_level_disconnect()

    #raw input command method
    
    def cmd_raw_input(self, text = None):
        try:
            if text is not None:
                byte_command = text.encode(self.charset)
                if byte_command is not None and byte_command != b'':
                    byte_command += b'\r\n'
                    self.socket.send(byte_command)
        except:
            traceback.print_exc()
            self.status_msg = 'Socket: message sending was failed.'
        else:
            self.status_msg = None
        finally:
            self.ret_status_msg()

        
    #command parse method

    def cmd_parse(self, line):
        buf = line.split(' ')
        if len(buf) == 0: return None
        '''
        if buf[0][0] != '/' and self.current_channel is not None:
            print(self.current_channel)
            self.cmd_PRIVMSG(None, self.current_channel, line)
            return None
        '''
        #parse pseudo command
        
        command = buf[0][1:len(buf[0]):1]
        
        if len(buf) == 1:
            param = None
        else:
            command_l = len(command) + 2
            param = line[command_l::]
        
        #find specific pseudo commands

        #need more code for incorrect command format
        
        if command == 'ABOUT':
           self.ret_help_msg()
        elif command == 'RAW':
            self.cmd_raw_input(param)
        elif command == 'PORT':
            port = int(buf[1])
            self.set_port(port)
        elif command == 'INFO':
            nick = buf[1]
            password = buf[2]
            realname = buf[3]
            charset = buf[4]
            self.set_info(nick, password, realname, charset)
        elif command == 'CONNECT':
            host = buf[1]
            port = int(buf[2])
            self.connect(host, port)
        elif command == 'LOGIN':
            self.login()
        elif command == 'GOTO':
            self.goto_channel(param)
        elif command == 'BREAK':
            self.break_connection()
        else:
            self.send_cmd(None, command, param)
        self.printer(line)


    #return human-readable server reaction

    #need more code :D
    def answer_parse(self, text):
        return text
