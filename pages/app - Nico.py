import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Client_Name",page_icon=":bar_chart",layout="wide")


st.title(":bar_chart: Sample Deloitte Client")
st.markdown('<style>div.block-container{padding-top:1rem;}</stryle>',unsafe_allow_html=True)

fl=st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename=fl.name
    st.write(filename)
    df=pd.read_csv(filename,encoding="ISO-8859-1")
else:
    os.chdir(os.getcwd())
    df=pd.read_csv("supermarket_sales - Sheet1.csv",encoding="ISO-8859-1")

col1,col2=st.columns((2))
df["order Date"]=pd.to_datetime(df["Date"])

#Getting the min and the max date
startDate=pd.to_datetime(df["Date"]).min()
EndDate=pd.to_datetime(df["Date"]).max()

with col1:
    date1=pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2=pd.to_datetime(st.date_input("End Date", EndDate))

df=df[(pd.to_datetime(df["Date"]) >= date1) & (pd.to_datetime(df["Date"]) <= date2)].copy()

#Create for the sity
st.sidebar.header("Choose your filer: ")
region=st.sidebar.multiselect("Pick your region", df["City"].unique())

if not region:
    df2=df.copy()
else:
    df2=df[df["City"].isin(region)]

#create for branch
    
state=st.sidebar.multiselect("Pick a branch",df2["Branch"].unique())
if not state:
    df3=df2.copy()
else:
    df3=df2[df2["Branch"].isin(state)]

#create for Customer type
customer=st.sidebar.multiselect("Pick a customer type",df3["Customer type"].unique())
if not customer:
    df4=df3.copy()
else:
    df4=df3[df3["Customer type"].isin(customer)]

#filter the data based on region, city and customer
if not region and not state and not customer:
    filtere_df=df
elif not state and not customer:
    filtere_df=df[df["City"].isin(region)]
elif not region and not customer:
    filtere_df=df[df["Branch"].isin(state)]
elif state and customer:
    filtere_df=df3[df3["Branch"].isin(state) & df3["Customer type"].isin(customer)]
elif state and region:
    filtere_df=df3[df3["Branch"].isin(state) & df3["City"].isin(region)]
elif region and customer:
    filtere_df=df3[df3["City"].isin(region) & df3["Customer type"].isin(customer)]
elif customer:
    filtere_df=df3[df3["Customer type"].isin(customer)]
else:
    filtere_df=df3[df3["City"].isin(region) & df3["Branch"].isin(state) & df3["Customer Type"].isin(customer)]

category_df=filtere_df.groupby(by=["Product line"],as_index=False)["Total"].sum()

with col1:
    st.subheader("Product line with Total")
    fig=px.bar(category_df, x= "Product line", y="Total",text=['${:,.2f}'.format(x) for x in category_df["Total"]],template="seaborn")
    st.plotly_chart(fig,use_container_widht=True, height=200)

with col2:
    st.subheader("City with Total")
    fig=px.pie(filtere_df, values="Total", names="City", hole =0.5)
    fig.update_traces(text=filtere_df["City"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

cl1,cl2=st.columns(2)
with cl1:
    with st.expander("Product_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv=category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv", help="Click here to download the data as CSV file")

with cl2:
    with st.expander("City_ViewData"):
        city=filtere_df.groupby(by="City", as_index=False)["Total"].sum()
        st.write(city.style.background_gradient(cmap="Oranges"))
        csv=city.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="City.csv", mime="text/csv", help="Click here to download the data as CSV file")