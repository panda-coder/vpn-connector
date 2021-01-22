#!/usr/bin/env python3

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, Gdk, GLib
from gi.repository import AppIndicator3 as appindicator

import subprocess

import pexpect

import base64, pyotp
import sys

from dotenv import load_dotenv
load_dotenv()


USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
OVPN_FILE = os.environ.get('OVPN')
TOTP = os.environ.get('TOTP')


APPINDICATOR_ID = 'MY VPN CONNECTOR'

USER_PROMPT = 'Enter Auth Username: '
PASSWORD_PROMPT = 'Enter Auth Password: '
CONNECTED = 'Initialization Sequence Completed'


class VpnConnector():
   def __init__(self):
      self.process = None
      self.connect_config = False
      self.menu_options = {}

      self.init_menu()
      self.init_indicator()
      
      

   def init_indicator(self):
      self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, Gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
      self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
      self.indicator.set_menu(self.menu)

   def init_menu_options(self):
      # Menu Exit
      self.menu_options['exit'] = Gtk.MenuItem(label="Exit")
      self.menu_options['exit'].connect("activate", self.quit)

      # Menu Connect
      self.menu_options['connect'] = Gtk.MenuItem(label="Connect")
      self.menu_options['connect'].connect("activate", self.connect)

      # Menu Connect
      self.menu_options['disconnect'] = Gtk.MenuItem(label="Disconnect")
      self.menu_options['disconnect'].connect("activate", self.disconnect)

      for menu in self.menu_options:
         self.menu.append(self.menu_options[menu])


   def init_menu(self):
      # create a menu
      self.menu = Gtk.Menu()
      self.init_menu_options()
      self.menu.show_all()

   def quit(self, source):
      Gtk.main_quit()

   def connect(self, source):
      self.menu_options['disconnect'].set_sensitive(True)
      self.menu_options['connect'].set_sensitive(False)
      self.connect_config = True

   def disconnect(self, source):
      self.connect_config = False
      print('Sending message to disconnect')
      self.process.sendcontrol('c')
      self.menu_options['disconnect'].set_sensitive(False)
      self.menu_options['connect'].set_sensitive(True)

   def init_process(self):
      self.process = pexpect.spawn(f'sudo openvpn {OVPN}', encoding='utf-8')
      self.process.logfile = sys.stdout
   
   def user_prompt(self):
      i = self.process.expect ([USER_PROMPT])
      if i == 0:
         self.process.sendline()

   def pass_prompt(self):
      totp = pyotp.TOTP(TOTP)
      i = self.process.expect ([PASSWORD_PROMPT])
      if i == 0:
         self.process.sendline(PASSWORD+totp.now())

   def wait_process(self):
      print('Connecting...')
      self.process.expect(CONNECTED)
      print('Connected')
      self.process.wait()

      print('Disconnected')
      self.process = None

      return True


   def loop(self):

      if self.process is None and self.connect_config:
         # self.process = subprocess.Popen(['openvpn', './ovpn/ercy.neto@finnet.corp__ssl_vpn_config.ovpn'], stdout=subprocess.PIPE,stdin=subprocess.PIPE)
         self.init_process()

         try:
            self.user_prompt()
            self.pass_prompt()
            return self.wait_process()

         except pexpect.EOF:
            print('Invalid username and/or password')
            raise InvalidCredentialsError('Invalid OpenVPN username and/or password')
         except pexpect.TIMEOUT:
            print('Connection failed!')
            raise TimeoutError('Cannot connect to OpenVPN server')
         
      return True
      

   def run(self):
      GLib.timeout_add(1000, self.loop)
      Gtk.main()



vpn_connector = VpnConnector()
vpn_connector.run()




