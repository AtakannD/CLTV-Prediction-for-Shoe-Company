*CLTV Prediction with BG-NBD & Gamma-Gamma*

1. Business Problem

FLO wants to set a roadmap for sales and marketing activities. In order for the company to make a medium-long-term 
plan, it is necessary to estimate the potential value that existing customers will provide to the company in the 
future.

2. Story of Dataset

The dataset consists of information obtained from the past shopping behaviors of customers who made their last 
purchases from Flo as OmniChannel (both online and offline shopper) in the years 2020-2021.


3. Variables of Dataset

master_id: Unique client number
order_channel: Which channel of the shopping platform is used (Android, iOS, Desktop, Mobile)
last_order_channel: The channel where the last purchase was made
first_order_date: The date of the first purchase made by the customer
last_order_date: The date of the customer's last purchase
last_order_date_online: The date of the last purchase made by the customer on the online platform
last_order_date_offline: The date of the last purchase made by the customer on the offline platform
order_num_total_ever_online: The total number of purchases made by the customer on the online platform
order_num_total_ever_offline: Total number of purchases made by the customer offline
customer_value_total_ever_offline: The total price paid by the customer for offline purchases
customer_value_total_ever_online: The total price paid by the customer for their online shopping
interested_in_categories_12: List of categories the customer has purchased from in the last 12 months


Task 1:
	Step 1: Read the dataset.
	Step 2: Define the functions required to suppress outliers.
	Step 3: If the variables "order_num_total_ever_online", "order_num_total_ever_offline", 
	"customer_value_total_ever_offline", "customer_value_total_ever_online" have outliers, suppress them.
	Step 4: Create new variables for each customer's total purchases and spending.
	Step 5: Examine the variable types. Change the type of variables that express date to date.


Task 2: Creating the CLTV Data Structure


Task 3: Establishment of BG/NBD, Gamma-Gamma Models and Calculation of CLTV

	Step 1: Fitting BG/NBD model
	Step 2: Fitting Gamma-Gamma model
	Step 3: Calculating six months CLTV.


Task 4: Creating Segments by CLTV Value

	Step 1: Dividing all customers into 4 groups (segments) according to 6-month CLTV
	Step 2: Making short 6-month action suggestions to the management for 2 groups that you will choose 
	from among 4 groups.
























