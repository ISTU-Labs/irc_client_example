# irc_client_example
Hand made socket irc client

WARRING: It is a beta. Not stable, but can send and recv messages.

MAIN FILE irc_tui.py

FOR EXIT CTRL+D.
FOR SENDING COMMAND CTRL+A

FOR START CONNECTION TYPE (WITHOUT BRAKETS):

/INFO <NICK> <PASSWORD> <REALNAME> <CHARSET>
/PORT <NUMBER YOU PORT FOR BIND SOCKET>
/CONNECT <DOMAIN OR IP> <PORT>
/START_READ
/LOGIN

YOU DID IT.

FOR JOIN TO CHANNEL: /JOIN <channelname>
FOR EXIT FROM CHANNEL: /PART <channelname>
FOR QUIT FROM SERVER: /QUIT <reason (optional)>

FOR SENDING MSG: /PRIVMSG <channelname> <your message>
