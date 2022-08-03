import pandas as pd
import datetime as dt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

# Task 1.1

df = pd.read_csv(
    r"C:\Users\atakan.dalkiran\PycharmProjects\CLTV Prediction with BG-NBD & Gamma-Gamma Models\flo_data_20k.csv")


def check_df(dataframe, head=10):
    """
    This function gives us a first look when we import our dataset.

    Parameters
    ----------
    dataframe: pandas.dataframe
    It is the dataframe from which variable names are wanted to be taken.
    head: int
    The variable that determines how many values we want to look at beginning

    Returns
    -------
    shape: tuple
    that variable gives us to dataset's information which how many columns and rows have
    type: pandas.series
    that variable gives us to our variables' types.
    columns: pandas.Index
    gives us the names of the columns in the dataset.
    head: pandas.Dataframe
    It gives us the variables and values of our dataset, starting from the zero index to the number we entered, as a dataframe.
    tail: pandas.Dataframe
    Contrary to head, this method counts us down starting from the index at the end.
    isnull().sum(): pandas.series
    It visits the variables in the data set and checks if there are any null values and gives us the statistics of how
    many of them are in each variable.
    quantile: pandas.dataframe
    It gives the range values of the variables in our data set as a percentage according to the values we entered.

    Examples
    --------
    The shape return output is given to us as a tuple (5000, 5).
    """
    print("######################### Shape #########################")
    print(dataframe.shape)
    print("\n######################### Type #########################")
    print(dataframe.dtypes)
    print("\n######################## Columns ########################")
    print(dataframe.columns)
    print("\n######################### Head #########################")
    print(dataframe.head(head))
    print("\n######################### Tail #########################")
    print(dataframe.tail(head))
    print("\n######################### NA #########################")
    print(dataframe.isnull().sum())
    print("\n######################### Quantiles #########################")
    print(dataframe.quantile([0, 0.25, 0.5, 0.75, 0.95, 1]).T)


# Task 1.2


def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    up_limit = up_limit.round()
    low_limit = quartile1 - 1.5 * interquantile_range
    low_limit = low_limit.round()
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


# Task 1.3


num_cols = [col for col in df.columns if df[col].dtypes in ["float64"]]
for col in num_cols:
    replace_with_thresholds(df, col)

# Task 1.4

df["total_order"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["total_price"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

# Task 1.5

df.info()
datecol_list = df.columns[df.columns.str.contains("date")]
df[datecol_list] = df[datecol_list].apply(pd.to_datetime)

# Task 2

df["last_order_date"].max()
today_date = dt.datetime(2021, 6, 1)
cltv_df = pd.DataFrame()
cltv_df["customer_id"] = df["master_id"]
cltv_df["recency_cltv_weekly"] = ((df["last_order_date"] - df["first_order_date"]).astype('timedelta64[D]') / 7)
cltv_df["T_weekly"] = ((today_date - df["first_order_date"]).astype('timedelta64[D]') / 7)
cltv_df["frequency"] = df["total_order"]
cltv_df["monetary_cltv_avg"] = df["total_price"] / df["total_order"]

# Task 3.1

bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(cltv_df['frequency'],
        cltv_df['recency_cltv_weekly'],
        cltv_df['T_weekly'])
cltv_df["exp_sales_3_month"] = bgf.conditional_expected_number_of_purchases_up_to_time(4 * 3,
                                                                                       cltv_df['frequency'],
                                                                                       cltv_df['recency_cltv_weekly'],
                                                                                       cltv_df['T_weekly'])
cltv_df["exp_sales_6_month"] = bgf.conditional_expected_number_of_purchases_up_to_time(4 * 6,
                                                                                       cltv_df['frequency'],
                                                                                       cltv_df['recency_cltv_weekly'],
                                                                                       cltv_df['T_weekly'])
cltv_df.sort_values("exp_sales_3_month", ascending=False)[:10]
cltv_df.sort_values("exp_sales_6_month", ascending=False)[:10]

# Task 3.2

ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv_df["frequency"],
        cltv_df["monetary_cltv_avg"])
cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df["frequency"],
                                                                       cltv_df["monetary_cltv_avg"])

# Task 3.3
cltv_df["cltv"] = ggf.customer_lifetime_value(bgf,
                                              cltv_df['frequency'],
                                              cltv_df['recency_cltv_weekly'],
                                              cltv_df['T_weekly'],
                                              cltv_df['monetary_cltv_avg'],
                                              time=6,  # 6 aylık
                                              freq="W",  # T'nin frekans bilgisi
                                              discount_rate=0.01)
cltv_df.sort_values(by="cltv", ascending=False).head(20)

# Task 4

cltv_df["segment"] = pd.qcut(cltv_df["cltv"], 4, labels=["D", "C", "B", "A"])

cltv_df[cltv_df["segment"].isin(["A"])]["customer_id"].to_csv("cltv_predict_segment_a.csv", index=False)
cltv_df[cltv_df["segment"].isin(["B"])]["customer_id"].to_csv("cltv_predict_segment_b.csv", index=False)