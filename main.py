import natixis.connections
from collections import defaultdict

## YOUR CREDENTIALS HERE ##
## REMEMBER TO DELETE THEM AFTER USING IT!! ##
NUMERO_ENTERPRISE = ""
CODE_SERVEUR = ""
PASSWORD = ""

# Init the output data containers
investments_today = {}
investments_by_name = {}
investments_by_availability = {}

# Get your natixis data!
data_retriever = natixis.connections.DataRetriever(NUMERO_ENTERPRISE, CODE_SERVEUR, PASSWORD)
data_retriever.retrieve_data(investments_today, investments_by_name, investments_by_availability)

print investments_today
print investments_by_name
print investments_by_availability