Last login: Fri May 30 15:31:22 on console
(base) qiruili@Qiruis-Mac-mini ~ % sudo systemsetup -getremotelogin
Password:
Remote Login: Off
(base) qiruili@Qiruis-Mac-mini ~ % sudo systemsetup -setremotelogin on
setremotelogin: Turning Remote Login on or off requires Full Disk Access privileges.
(base) qiruili@Qiruis-Mac-mini ~ % d Documents
zsh: command not found: d
(base) qiruili@Qiruis-Mac-mini ~ % cd Do*
cd: string not in pwd: Documents
(base) qiruili@Qiruis-Mac-mini ~ % cd Downloads
(base) qiruili@Qiruis-Mac-mini Downloads % mv id_rsa.pub ~/.ssh
(base) qiruili@Qiruis-Mac-mini Downloads % cd ~
(base) qiruili@Qiruis-Mac-mini ~ % cd .ssh
(base) qiruili@Qiruis-Mac-mini .ssh % ls
id_rsa.pub	known_hosts	known_hosts.old	office_computer
(base) qiruili@Qiruis-Mac-mini .ssh % 
(base) qiruili@Qiruis-Mac-mini .ssh % chmode 700 ./
zsh: command not found: chmode
(base) qiruili@Qiruis-Mac-mini .ssh % chmod 700 ./
(base) qiruili@Qiruis-Mac-mini .ssh % ls 
id_rsa.pub	known_hosts	known_hosts.old	office_computer
(base) qiruili@Qiruis-Mac-mini .ssh % mv id_rsa.pub authorized_keys
(base) qiruili@Qiruis-Mac-mini .ssh % ls
authorized_keys	known_hosts	known_hosts.old	office_computer
(base) qiruili@Qiruis-Mac-mini .ssh % chmod 600 authorized_keys
(base) qiruili@Qiruis-Mac-mini .ssh % sudo systemsetup -getremotelogin
Password:
Remote Login: On
(base) qiruili@Qiruis-Mac-mini .ssh % 
(base) qiruili@Qiruis-Mac-mini .ssh % 
(base) qiruili@Qiruis-Mac-mini .ssh % ngrok tcp 22
ERROR:  failed to start tunnel: You must add a credit or debit card before you can use TCP endpoints on a free account. We require a valid card as a way to combat abuse and keep the internet a safe place. This card will NOT  be charged.
ERROR:  Add a card to your account here: https://dashboard.ngrok.com/settings#id-verification
ERROR:  
ERROR:  ERR_NGROK_8013
ERROR:  https://ngrok.com/docs/errors/err_ngrok_8013
ERROR:  
(base) qiruili@Qiruis-Mac-mini .ssh % ngrok tcp 22

ngrok                                                           (Ctrl+C to quit)
                                                                                
🤖 Want to hang with ngrokkers on our new Discord? http://ngrok.com/discord     
                                                                                
Session Status                online                                            
Account                       qqzipcar@gmail.com (Plan: Free)                   
Version                       3.22.1                                            
Region                        United States (California) (us-cal-1)             
Latency                       35ms                                              
Web Interface                 http://127.0.0.1:4040                             
Forwarding                    tcp://6.tcp.us-cal-1.ngrok.io:15934 -> localhost:2
                                                                                
Connections                   ttl     opn     rt1     rt5     p50     p90       
                              0       0       0.00    0.00    0.00    0.00      
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                

