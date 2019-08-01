#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 09:43 2019

@author: claire
"""

from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip
		
class ItemValidationTest(FunctionalTest):
	
	def get_error_empty_element(self):
		return self.browser.find_element_by_css_selector('#id_text:invalid')
	
	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to submit an empty list item. she hits Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		# The home page refreshes, and there is an error message saying that list items cannot be blank
		self.wait_for(lambda: self.get_error_empty_element())
		
		# She starts typing some text for the new item and the error disappears
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
		
		# ... and she can submit it successfully
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		
		# Perversely, she now decides to submit a second blank list item
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		# Again, the server will not comply
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for(lambda: self.get_error_empty_element())
		
		# And she can correct it by filling some text in
		self.get_item_input_box().send_keys('Prepare matcha')
		self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Prepare matcha')
		
	def test_error_messages_are_cleared_on_input(self):
		# Edith starts a list and causes a validation error
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for(lambda: self.get_error_empty_element())
		
		# She starts typing in the input box to clear the error
		self.get_item_input_box().send_keys('a')
		
		# She is pleased to see that the error message disappears
		self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))	