#VPN Connector Makefile

F1_EXISTS=$(shell [ -e .env ] && echo 1 || echo 0 )

all : install configure

install:
	pip3 install -r requirements

configure:
ifeq ($(F1_EXISTS), 1)
	@echo "env file exists. Exiting. Please execute make clean if you want to proceed"; 
else    
	@read -p "Username: " VPNUSER ; \
	read -p "PASSWORD: " VPNPASS ; \
	read -p "OVPN: " OVPN ; \
	read -p "TOTP: " TOTP ; \
	echo "OVPN=$$OVPN\n\
PASSWORD=$$VPNPASS\n\
VPN_USER=$$VPNUSER\n\
TOTP=$$TOTP" > .env \
	fi
endif


clean :
	@rm .env
