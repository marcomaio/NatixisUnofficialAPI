__author__ = 'Marco Maio'

import httplib
import natixis.parsers

HOME_PAGE = "epargnants.interepargne.natixis.fr"
DUMMY_GET_PARAMETERS = "/def_int_ep/ep/home.do?language=fr"
LOGIN_GET_PARAMETERS = "/def_int_ep/ep/gl/aut1.do?dfAT=next&dfMenuId=EC_EP_GL_AUT_01&value%28"
INVESTMENTS_DETAILS_PAGE = "/def_int_ep/ep/menu.do?dfMenuId=SC_EP_AV_SYN"
HISTORICAL_OPERATION_PAGE = "/def_int_ep/ep/menu.do?dfAT=menu&dfMenuId=SC_EP_OP_HIS"
HISTORICAL_DETAILS_GET_PARAMETERS = "/def_int_ep/ep/op/his.do?dfAT=detail&dfMenuId="

class DataRetriever():
    def __init__(self, numero_enterprise=None, code_serveur=None, password=None):
        # input data assessment
        if numero_enterprise == None:
            raise ValueError('NUMERO ENTERPRISE not specified!')
        elif code_serveur == None:
            raise ValueError('CODE SERVEUR not specified!')
        elif password == None:
            raise ValueError('PASSWORD not specified!')

        self.__numero_enterprise = numero_enterprise
        self.__code_serveur = code_serveur
        self.__password = password

    def login(self, connection=None):
        # input data assessment
        if connection == None:
            raise ValueError('CONNECTION object not initialised!')

        # First connection needed to get the session ID (in the cookie)
        connection.request("GET", DUMMY_GET_PARAMETERS)
        r1 = connection.getresponse()
        #print r1.status, r1.reason
        header_cookies = r1.getheader('set-cookie')
        #print r1.length
        #print r1.msg
        cookie = header_cookies.split(';')[0]
        headers = {'Cookie' : cookie}
        # flush data - maybe unnecessary
        data = r1.read()

        # Second connection to login
        login_url = LOGIN_GET_PARAMETERS + "numEntreprise%29=" + self.__numero_enterprise + \
                    "&value%28sCodeServeur%29=" + self.__code_serveur + "&value%28sPsw%29=" + self.__password
        connection.request("GET", login_url, None, headers)
        r2 = connection.getresponse()
        #print r2.status, r2.reason
        # flush data - maybe unnecessary
        data = r2.read()

        return headers

    def retrieve_data(self):
        investments_today = {}
        investments_details_by_name = {}
        investments_details_by_availability = {}

        # Open the connection
        connection = httplib.HTTPSConnection(HOME_PAGE)

        # Login and get the session headers
        headers = self.login(connection)

        # Get the details of investments
        connection.request("GET", INVESTMENTS_DETAILS_PAGE, None, headers)
        response = connection.getresponse()
        #print r4.status, r4.reason
        # flush data - maybe unnecessary
        data = response.read()

        # Get the investments' today situation (investments names, current actions values, number of parts)
        parser = natixis.parsers.HomePage(investments_today)
        parser.feed(data)

        # Get the historical operations
        connection.request("GET", HISTORICAL_OPERATION_PAGE, None, headers)
        response = connection.getresponse()
        # print r5.status, r5.reason
        # flush data - maybe unnecessary
        data = response.read()
        parser2 = natixis.parsers.HistoricalOperations()
        parser2.feed(data)
        historical_operations = parser2.operations

        # Retrieve details from each historical operation
        for operation in parser2.operations:
            recurring_pair = operation[1] + "=" + operation[2]
            url = HISTORICAL_DETAILS_GET_PARAMETERS + operation[0] + \
                  "&dfPgOffset=&dfPgPageSize=&pageA=EP_OP_HIS&" + recurring_pair + "&" \
                  + recurring_pair + "&" + recurring_pair
            connection.request("GET", url, None, headers)
            response = connection.getresponse()
            # print response.status, response.reason
            # flush data
            data = response.read()
            parser3 = natixis.parsers.HistoricalOperationDetails(investments_details_by_name, \
                                                                 investments_details_by_availability)
            parser3.feed(data)

        # Close the connection
        connection.close()

        # return containers
        return investments_today, investments_details_by_name, investments_details_by_availability

