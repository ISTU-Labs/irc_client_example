# irc_client_example
Hand made socket irc client

WARRING: It is a beta. Not stable, but can send and recv messages. No support HTTPS.

MAIN FILE irc_tui.py

for exit CTRL+D.
for sending command CTRL+A

for start connection type (without breakets):

/INFO <nick> <password> <realname> <charset>
  
/PORT <number of you port for bind socket>

/CONNECT <domain or ip> <port>

/START_READ

/LOGIN

YOU DID IT.

for join to channel: /JOIN <channelname>
  
for exit from channel: /PART <channelname>
  
for quit from server: /QUIT <reason (optional)>
for sending msg: /PRIVMSG <channelname> <your message>
