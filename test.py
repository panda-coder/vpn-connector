#!/usr/bin/env python3
import random
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'MY VPN CONNECTOR'


class VpnConnector():
    def __init__(self):
        self.init_menu()
        self.init_indicator()
        

    def init_indicator(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, Gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu)

    def init_menu(self):
        # create a menu
        self.menu = Gtk.Menu()
        self.menu_items = Gtk.MenuItem("Exit")
        self.menu.append(self.menu_items)
        self.menu_items.connect("activate", self.quit)
        self.menu_items.show_all()

    def quit(source):
        Gtk.main_quit()

    def run(self):
        Gtk.main()



vpn_connector = VpnConnector()
vpn_connector.run()