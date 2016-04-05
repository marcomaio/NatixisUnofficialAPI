import natixis.connections
from natixis.handler import Handler

## YOUR CREDENTIALS HERE ##
NUMERO_ENTERPRISE = raw_input("Insert your \"NUMERO D\'ENTERPRISE\": ")
CODE_SERVEUR = raw_input("Insert your \"CODE SERVEUR\": ")
PASSWORD = raw_input("Insert your \"PASSWORD\": ")

# Get your natixis data!
data_retriever = natixis.connections.DataRetriever(NUMERO_ENTERPRISE, CODE_SERVEUR, PASSWORD)

# You can directly access to all natixis data retrieved
investments_today, investments_by_name, investments_by_availability = data_retriever.retrieve_data()

# ..or instantiate the handler which will let you browse your data in a more meaningful manner
h = Handler(investments_today, investments_by_name, investments_by_availability)

# handler usage example
print "Your total investments are:", h.get_amount_total_investment()
print h.get_total_amount_by_date("10/10/2021", closest_availability_only=True)
print h.get_total_gain()
for k in investments_today:
    print k
    print h.get_gain_by_stock_name(k)
print h.get_next_available_amount()