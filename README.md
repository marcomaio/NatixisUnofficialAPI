# NatixisUnofficialAPI
Unofficial python API for Natixis Interepargne accounts


Less than an "alfa" version, I just need some feedbacks on the data retrieved by the module natixis.connections.DataRetriever.
Three containers retrieved:
- map \<key: investment_name, value: current_investment_value, number_of_parts\>
- map \<key: investment_name, map \<key: purchase_date, value: purchase_value, parts_number_bought\> \>
- map \<key: availability_date, map \<key: investment_name, value: number_of_available_parts\> \>

It currently does not support:
- cases in which you already withdrew some parts.
- error cases

Please try to play with the main.py file, just insert your credentials in the pre-set variables, save it and launch it:
python main.py

!! Do not forget to remove your credentials from the main.py file  and re-save it!!

Any feedback on the data retrieved consinstency + contribution are more than welcome
