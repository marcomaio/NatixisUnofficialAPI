# NatixisUnofficialAPI
Unofficial python API for Natixis Interepargne accounts


Less than an "alfa" version, I just need some feedbacks on the data retrieved by the module natixis.connections.DataRetriever.
Three containers retrieved:
- map \<key: investment_name, value: current_investment_value, number_of_parts\>
- map \<key: investment_name, map \<key: purchase_date, value: purchase_value, parts_number_bought\> \>
- map \<key: availability_date, map \<key: investment_name, value: number_of_available_parts\> \>

A Natixis data handler has been developed, built upon the three containers above, aiming to ease the reading of data. It provides following methods:
- get_amount_by_stock_name(self, stock_name)
- get_amount_total_investment(self)
- get_total_amount_by_date(self, date=None, stock_name="", closest_availability_only=False)
- get_paid_by_stock_name(self, stock_name=None)
- get_total_gain(self)
- get_gain_by_stock_name(self, stock_name)
- get_next_available_amount(self)


It currently does not support:
- cases in which you already withdrew some parts.
- error cases

Please try to play with the main.py file, just insert your credentials in the pre-set variables, save it and launch it:
python main.py

Any feedback on the data retrieved consinstency + contribution are more than welcome
