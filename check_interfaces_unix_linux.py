import sys
import re
import time
import fcntl
import paramiko
import socket

from bs4 import BeautifulSoup

INTERFACES_FNAME = '/var/www/html/status/interfaces.xml'

def search(dictionary, searchFor):
    for key, value in dictionary.items():
                if searchFor in key:
                        return value

def update_power(hostname, host_addr, new_eth):
        try:
                soup = BeautifulSoup(open(INTERFACES_FNAME), 'html.parser')

                if len(new_eth) == 0:
                        return 'No change'
                elem = None
                for item in soup.find_all('host'):
                        hname = item.find_all('name')[0].string.strip()
                        haddr = item.find_all('addr')[0].string.strip()
                        if hname == hostname and haddr == host_addr:
                                elem = item
                                elem.eth.string.replaceWith('brak')
                                elem.eth1.string.replaceWith('brak')
                                elem.eth2.string.replaceWith('brak')
                                elem.eth3.string.replaceWith('brak')
                                elem.eth4.string.replaceWith('brak')
                                elem.eth5.string.replaceWith('brak')
                                elem.eth6.string.replaceWith('brak')
                                elem.eth7.string.replaceWith('brak')
                                break
                #print new_eth
                if elem is not None:
                        for key, value in new_eth.items():
                                for host_key, eth_value in value.items():
                                        if host_key is 1:
                                                elem.eth.string.replaceWith(eth_value)
                                        if host_key is 2:
                                                elem.eth1.string.replaceWith(eth_value)
                                        if host_key is 3:
                                                elem.eth2.string.replaceWith(eth_value)
                                        if host_key is 4:
                                                elem.eth3.string.replaceWith(eth_value)
                                        if host_key is 5:
                                                elem.eth4.string.replaceWith(eth_value)
                                        if host_key is 6:
                                                elem.eth5.string.replaceWith(eth_value)
                                        if host_key is 7:
                                                elem.eth6.string.replaceWith(eth_value)
                                        if host_key is 8:
                                                elem.eth7.string.replaceWith(eth_value)

                with open(INTERFACES_FNAME,'wb') as f:
                        f.write(soup.prettify())
                return 'OK'
        except:
                return 'Error: Problem with Upload XML File'

def get_output_key(IP, login, key_fname, command_list, dummy_string, exit_string, line_sep):
        try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(IP, username=login, key_filename=key_fname)
                channel = client.invoke_shell()
                channel.set_combine_stderr(True)
                channel.settimeout(30)

                command = line_sep.join(command_list)
                input = command + line_sep
                if dummy_string != '':
                        input = input + dummy_string + line_sep

                if dummy_string == '':
                        input = input + exit_string + line_sep

                # Send the input to the device
                channel.send(input)
                while not channel.recv_ready():
                        time.sleep(1)

                bytes_received = 0
                end_loop = False
                reply = ''
                while end_loop is False:
                        chunk = channel.recv(65535)
                        bytes_received = bytes_received + len(chunk)
                        reply = reply + chunk
                        if dummy_string == '':
                                if chunk == '':
                                        end_loop = True
                        if dummy_string != '':
                                if dummy_string in reply:
                                        channel.send(exit_string+line_sep)
                                        end_loop = True
                return reply

                # Wait for ssh session to terminate
                while not channel.exit_status_ready():
                        time.sleep(1)
                client.close()
        except socket.timeout:
                return ("error_timeout")
        except paramiko.AuthenticationException:
                return ("error_auth")
        except paramiko.BadHostKeyException:
                return('error_badhostkey')
        except paramiko.SSHException:
                return('error_sshexception')
        except socket.error, e:
                return ('error_socket')
        except Exception, e:
                return('error_exception')

def get_output(IP, login, password, command_list, dummy_string, exit_string, line_sep):
# command_list - the command sequence to be run, as a list
# dummy_string - helpful for some devices, that don't seem to finish the ssh session correctly
# Presence of the dummy_command string in the output helps to recognize that the output ends.
# exit_string - the command to stop the ssh session
# Assumptions: dummy_string != ''  ==>  exit_string != ''
# line_sep - the proper line separator char sequence. It goes to the end of command/dummy_string/exit_string

        try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(IP, username=login, password=password, timeout=20)
                channel = client.invoke_shell()
                channel.set_combine_stderr(True)
                channel.settimeout(30)

                command = line_sep.join(command_list)
                input = command + line_sep
                if dummy_string != '':
                        input = input + dummy_string + line_sep

                if dummy_string == '':
                        input = input + exit_string + line_sep

                # Send the input to the device
#               print 'sleep...'
#               time.sleep(3)
                channel.send(input)
                while not channel.recv_ready():
                        time.sleep(1)

                bytes_received = 0
                end_loop = False
                reply = ''
                while end_loop is False:
                        chunk = channel.recv(65535)
                        bytes_received = bytes_received + len(chunk)
                        reply = reply + chunk
                        if dummy_string == '':
                                if chunk == '':
                                        end_loop = True
                        if dummy_string != '':
                                if dummy_string in reply:
                                        channel.send(exit_string+line_sep)
                                        end_loop = True
                return reply

                # Wait for ssh session to terminate
                while not channel.exit_status_ready():
                        time.sleep(1)
                client.close()
        except socket.timeout:
                return ("error_timeout")
        except paramiko.AuthenticationException:
                return ("error_auth")
        except paramiko.BadHostKeyException:
                return('error_badhostkey')
        except paramiko.SSHException:
                return('error_sshexception')
        except socket.error, e:
                return ('error_socket')
        except Exception, e:
                return('error_exception')

def check():
        try:
                login        = 'example'
                password     = 'examplePassword'
                command_network_devices  = '''ifconfig | grep -B4 "inet " | awk '{ if ( $1 == "inet") { print "ip:",$2 } else if ( $1 != "inet6" && $1 != "--" && $0 !~ /^([[:blank:]])/) { print "dev:",$1 } }'
                '''
                pattern  = r"dev: ([a-zA-z0-9]+)|ip: ([0-9]+[0-9]+.[0-9]+.[0-9]+.[0-9]+)"
                command = [command_network_devices]
                dummy_string = ''
                exit_string  = 'exit'
                line_sep     = '\n'
                message      = ''
                status       = 0

                server_list = ['10.10.10.2', '10.10.10.3','10.10.10.4','10.10.10.5','10.10.10.6','10.10.10.7','10.10.10.8','10.10.10.9',
                                '10.10.10.10','10.10.10.11','10.10.10.12','10.10.10.13','10.10.10.14','10.10.10.15','10.10.10.16','10.10.10.17','10.10.10.18',
                                '10.10.10.19','10.10.10.20','10.10.10.21','10.10.10.22','10.10.10.23','10.10.10.24','10.10.10.25']

                server_name = {'10.10.10.2': 'ns1.example.pl',
                                                        '10.10.10.3': 'db.example.pl',
                                                        '10.10.10.4': 'vma.example.pl',
                                                        '10.10.10.5': 'vmb.example.pl',
                                                        '10.10.10.6': 'www.example.pl',
                                                        '10.10.10.7': 'mail.example.pl',
                                                        '10.10.10.8': 'ns2.example.pl',
                                                        '10.10.10.9': 'pusty',
                                                        '10.10.10.10': 'pusty1',
                                                        '10.10.10.11': 'jail1.example.pl',
                                                        '10.10.10.12': 'jail2.example.pl',
                                                        '10.10.10.13': 'jail3.example.pl',
                                                        '10.10.10.14': 'jail4.example.pl',
                                                        '10.10.10.15': 'jail5.example.pl',
                                                        '10.10.10.16': 'vma1.example.pl',
                                                        '10.10.10.17': 'vma2.example.pl',
                                                        '10.10.10.18': 'vma3.example.pl',
                                                        '10.10.10.19': 'vma4.example.pl',
                                                        '10.10.10.20': 'vma5.example.pl',
                                                        '10.10.10.21': 'vmb1.example.pl',
                                                        '10.10.10.22': 'vmb2.example.pl',
                                                        '10.10.10.23': 'vmb3.example.pl',
                                                        '10.10.10.24': 'vmb4.example.pl',
                                                        '10.10.10.25': 'vmb5.example.pl'}

                for server in server_list:
                        if server == '10.10.10.3':
                                # login        = 'root'
                                # pattern = r"dev: ([a-zA-z0-9]+)|ip: ([0-9]+[0-9]+.[0-9]+.[0-9]+.[0-9]+)|addr:([0-9]+[0-9]+.[0-9]+.[0-9]+.[0-9]+)"
                        if server == '10.10.10.4':
                                # pattern = r"dev: ([a-zA-z0-9]+)|ip: ([0-9]+[0-9]+.[0-9]+.[0-9]+.[0-9]+)|addr:([0-9]+[0-9]+.[0-9]+.[0-9]+.[0-9]+)"
                        # if Oppen SSH is enabled
						if server  == '10.10.10.5':
                                        # login        = 'exampleuser'
                                        # key_fname    = '/usr/lib64/nagios/plugins/m.example.openssh'
                                        # output       = get_output_key(server, login, key_fname, command, dummy_string, exit_string, line_sep)
                        else:
                        output       = get_output(server, login, password, command, dummy_string, exit_string, line_sep)
                        input_array= {}
                        output_array = {}
                        key_for_arr = 0
                        lines = output.split('\n')
                        if server == '213.156.98.156' or server == '213.156.98.153':
                                for line in lines:
                                        line = line.strip(' \t\r\n')
                                        match = re.search(pattern, line)
                                        if match:
                                                new_line = match.group(1)
                                                new_line2 = match.group(3)
                                                #new_line3 = match.group(3)
                                                if new_line:
                                                        device = new_line
                                                else:
                                                        if new_line2 == '127.0.0.1' or new_line2 == '192.168.122.1':# or new_line3 == '127.0.0.1' or new_line3 == '192.168.122.1':
                                                                continue
                                                        key_for_arr += 1
                                                        input_array[key_for_arr] = device + (' ')  + new_line2
                                                        #input_array[key] = device + (' ')  + new_line3
                                                        output_array[server] = input_array
                                output_array[server] = input_array
                                name =  search(server_name, server)
                                print output_array
                                update_power(name, server,  output_array)
                        else:
                                for line in lines:
                                        line = line.strip(' \t\r\n')
                                        match = re.search(pattern, line)
                                        if match:
                                                new_line = match.group(1)
                                                new_line2 = match.group(2)
                                                if new_line:
                                                        device = new_line
                                                else:
                                                        if new_line2 == '127.0.0.1' or new_line2 == '192.168.122.1':
                                                                continue
                                                        key_for_arr += 1
                                                        input_array[key_for_arr] = device + (' ')  + new_line2
                                output_array[server] = input_array
                                name =  search(server_name, server)
                                print output_array
                                update_power(name, server,  output_array)

        except:
                return 'dupa'
check()
