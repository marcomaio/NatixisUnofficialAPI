__author__ = 'Marco Maio'

from HTMLParser import HTMLParser
import re

FLOAT_REGEX = re.compile('[^0-9,]')


class HomePage(HTMLParser):
    def __init__(self, investments=None):
        if investments == None:
            raise ValueError('INVESTMENTS input/output mandatory object not specified!')

        HTMLParser.__init__(self)
        self.__investments_found = 0
        self.__investment_amount_found = 0
        self.__parts_eur = False
        self.__parts_number = False
        self.__investment_name = ""
        self.investments = investments

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'class' and value == 'eo_ta1_hyp':
                    self.__investments_found += 1
                    break
        if tag == 'td':
            for name, value in attrs:
                if name == 'class' and value == 'tabTotal':
                    self.__investment_amount_found += 1
                    break
        if tag == 'span':
            for name, value in attrs:
                if name == 'id' and value == 'pdtTitle_toolTip':
                    self.__parts_eur = True
                    break
        if tag == 'span':
            for name, value in attrs:
                if name == 'id' and value == 'pdt2Title_toolTip':
                    self.__parts_number = True
                    break

    def handle_endtag(self, tag):
        if tag == 'a' and self.__investments_found > 0:
            self.__investments_found -= 1

        if tag =='td' and self.__investment_amount_found:
            self.__investment_amount_found -= 1

        if tag =='table':
            if self.__parts_eur:
                self.__parts_eur = False
            elif self.__parts_number:
                self.__parts_number = False

    def handle_data(self, data):
        if self.__investments_found:
            self.__investment_name = data.strip()
            if not self.investments.has_key(self.__investment_name):
                self.investments[self.__investment_name] = {}
        if self.__investment_amount_found:
            if self.__parts_eur:
                euros = float(FLOAT_REGEX.sub("", data.strip()).replace(',', '.'))
                self.investments[self.__investment_name]['EUR'] = euros
                if 'numbers' in self.investments[self.__investment_name]:
                    self.investments[self.__investment_name]['EUR'] = \
                        euros/self.investments[self.__investment_name]['Numbers of parts']
            if self.__parts_number:
                number_of_quotes = float(FLOAT_REGEX.sub("", data.strip()).replace(',', '.'))
                self.investments[self.__investment_name]['Numbers of parts'] = number_of_quotes
                if 'EUR' in self.investments[self.__investment_name]:
                    self.investments[self.__investment_name]['EUR'] /= number_of_quotes


class HistoricalOperations(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.operations = []
        self.__operation = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'onclick' and 'DfdetailAction' in value:
                    operation = value.split(',')[1]
                    self.__operation.append(operation.strip("'"))
                    break
        if tag == 'input' and len(self.__operation) == 1:
            for name, value in attrs:
                if name == 'name':
                    self.__operation.append(value)
                if name == 'value':
                    self.__operation.append(value)
                if len(self.__operation) == 3:
                    self.operations.append(self.__operation)
                    self.__operation = []


class HistoricalOperationDetails(HTMLParser):
# row class "lgn-fusion" = start
# within the same row, the 3 span class "txt-imp" are useful
# First value = investment name
# Second value = date of purchase acquisto
# Thirs value = value of purchase
# * if tab4 class "noLeftBorder" does not contain "CSG"
# Start recording td class "tab7". Take only the third one (number of parts bought)
# take td class "tab19" => date of availability.
# reset tab7 counter
# back to point "*"

    def __init__(self, actions_by_name, actions_by_availability):
        HTMLParser.__init__(self)

        # indicators
        self.__trigger_record = False
        self.__investment_found = False
        self.__investment_attributes = 0
        self.__span_counter = 0
        self.__possible_investment_parts_found = False
        self.__availability_date_found = False
        self.__investment_end_indicator = False

        # global temporary attributes
        self.__investment_name = None
        self.__date_of_purchase = None
        self.__date_of_availability = None
        self.__number_of_parts = None

        # Containers
        ## First key: investment name
        ## Second key: date of purchase
        ## Content: price of purchase, number of parts
        ## structure: map <str, map <str, (int, int)>>
        self.actions_by_name = actions_by_name

        ## First key: date of availability
        ## Second key: investment name
        ## Content: number of parts
        ## structure: map <str, map <str,int> >
        self.actions_by_availability = actions_by_availability


    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            for name, value in attrs:
                if name == 'class' and value == 'lgn-fusion':
                    self.__trigger_record = True
                    break

        if tag == 'span':
            for name, value in attrs:
                if name == 'class' and value == 'txt-impt' and self.__trigger_record:
                    self.__investment_attributes += 1
                    self.__investment_found = True
                    break

        if tag == 'td':
            for name, value in attrs:
                if name == 'class' and value == 'tab4 noLeftBorder' and self.__trigger_record:
                    self.__possible_investment_parts_found = True
                    break
                if name == 'class' and value == 'tab7' and self.__possible_investment_parts_found:
                    self.__span_counter += 1
                if name == 'class' and value == 'tab19':
                    self.__availability_date_found  = True



    def handle_endtag(self, tag):
        if tag == 'span' and self.__investment_found:
            self.__investment_found = False
        if tag == 'span' and self.__investment_attributes == 3:
            self.__investment_attributes = 0

        if tag =='tr' and self.__investment_end_indicator:
            self.__trigger_record = False
            self.__number_of_parts= None
            self.__investment_name = None
            self.__date_of_purchase = None

        if tag =='td' and self.__span_counter == 3:
            self.__span_counter = 0
            self.__possible_investment_parts_found = False

        if tag =='td' and self.__availability_date_found:
            self.__availability_date_found = False

        if tag == 'td' and self.__investment_end_indicator:
            self.__investment_end_indicator = False

    def handle_data(self, data):
        if self.__investment_found and self.__investment_attributes <=3:
            if self.__investment_attributes == 1:
                self.__investment_name = data.strip()
                if not self.actions_by_name.has_key(self.__investment_name):
                    self.actions_by_name[self.__investment_name] = {}
            elif self.__investment_attributes == 2:
                self.__date_of_purchase = data.strip()
                if not self.actions_by_name[self.__investment_name].has_key(self.__date_of_purchase):
                    self.actions_by_name[self.__investment_name][self.__date_of_purchase] = {}
            elif self.__investment_attributes == 3:
                purchase_value = float(FLOAT_REGEX.sub("", data.strip()).replace(',', '.'))
                if self.actions_by_name[self.__investment_name][self.__date_of_purchase].has_key("Purchase value"):
                    self.actions_by_name[self.__investment_name][self.__date_of_purchase]["Purchase value"] += purchase_value
                else:
                    self.actions_by_name[self.__investment_name][self.__date_of_purchase]["Purchase value"] = purchase_value

        if self.__possible_investment_parts_found:
            if 'CSG' in data:
                self.__investment_end_indicator = True

        if self.__possible_investment_parts_found and self.__span_counter == 3:
            self.__number_of_parts = float(FLOAT_REGEX.sub("", data.strip()).replace(',', '.'))
            if self.actions_by_name[self.__investment_name][self.__date_of_purchase].has_key("Number of actions bought"):
                self.actions_by_name[self.__investment_name][self.__date_of_purchase]["Number of actions bought"] += \
                    self.__number_of_parts
            else:
                self.actions_by_name[self.__investment_name][self.__date_of_purchase]["Number of actions bought"] = \
                    self.__number_of_parts

        if self.__availability_date_found:
            self.__date_of_availability = data.strip()
            if not self.actions_by_availability.has_key(self.__date_of_availability):
                self.actions_by_availability[self.__date_of_availability] = {}
            if not self.actions_by_availability[self.__date_of_availability].has_key(self.__investment_name):
                self.actions_by_availability[self.__date_of_availability][self.__investment_name] = self.__number_of_parts
            else:
                self.actions_by_availability[self.__date_of_availability][self.__investment_name] += self.__number_of_parts
