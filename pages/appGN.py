
import streamlit as st
import plotly.express as px
import pandas as pd
import os


class MyApp:

    def __init__(self):
        self.page_title = "Client_Name"
        self.title = ":bar_chart: Sample Deloitte Client"
        self.functions = {"Product chart": self.product, "City chart": self.city}
        self.product_chart = {"Area": self.area, "Bar": self.bar, "Line": px.line}
        self.city_chart = {"Pie": self.pie}

    def main(self):
        st.set_page_config(page_title=self.page_title, page_icon=":bar_chart", layout="wide")
        st.title(self.title)
        self.upload()
        self.sidebar()
        self.dates()
        self.modify()
        self.functions[self.selected_option]()

    def upload(self):
        self.fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
        if self.fl is not None:
            self.filename = self.fl.name
            self.df = pd.read_csv(self.filename, encoding="ISO-8859-1")
        else:
            os.chdir(os.getcwd())
            self.df = pd.read_csv("supermarket_sales - Sheet1.csv", encoding="ISO-8859-1")


    def __sidebar_filters_options(self)->pd.DataFrame:
        """
            Return a dataframe with the available options for the filters
            based on other filters selection. 
        """
        query = []
        if st.session_state.get("slicer_region") is not None \
            and len(st.session_state.slicer_region) > 0:
            query.append("City in @st.session_state.slicer_region")
        else:
            st.session_state.slicer_region = []

        if st.session_state.get("slicer_state") is not None \
            and len(st.session_state.slicer_state) > 0:
            query.append("Branch in @st.session_state.slicer_state")
        else:
            st.session_state.slicer_state = []

        if st.session_state.get("slicer_customer") is not None \
            and len(st.session_state.slicer_customer) > 0:
            query.append(f"`Customer type` in @st.session_state.slicer_customer")
        else:
            st.session_state.slicer_customer = []
        
        if len(query) > 0:
            query = " & ".join(query)
            self.df2 = self.df.copy()
            self.df2 = self.df.query(query)[["City", "Branch", "Customer type"]]
            available_options = self.df2.query(query).drop_duplicates()
        else:  
            available_options = self.df[["City", "Branch", "Customer type"]].drop_duplicates()
        
        return available_options
    

    def sidebar(self):
        with st.sidebar:
            st.header("Choose your filer:")  
            if self.df is not None:
                available_options = self.__sidebar_filters_options()
                st.write(available_options)
                # Se puede hacer hasta que haga uno por cada columna
                # Create for city
                self.region = st.multiselect("Pick your region", sorted(available_options["City"].unique()), default=st.session_state.slicer_region, key="slicer_region")
                # Create for branch
                self.state = st.multiselect("Pick a branch", sorted(available_options["Branch"].unique()), default=st.session_state.slicer_state, key="slicer_state")
                
                # Create for Customer type
                self.customer = st.multiselect("Pick a customer type", sorted(available_options["Customer type"].unique()), default=st.session_state.slicer_customer, key="slicer_customer")
                

            # Se selecciona el gráfico que se quiera a partir del diccionario
            self.selected_option = st.selectbox(label="Choose a chart type:", options=self.functions.keys())

            # Dependiendo del que se haya elegido, se selecciona el tipo de gráfico que se quiere, seguro que se puede
            # hacer sin tener que poner el if para diferenciarlo
            types = (list(self.product_chart.keys()) if self.selected_option == "Product chart" else
                     list(self.city_chart.keys()))
            self.selected_type = st.selectbox(label="Choose the chart", options=types)

    # La parte de las fechas
    def dates(self):
        self.col1, self.col2 = st.columns((2))
        self.df["order Date"] = pd.to_datetime(self.df["Date"])

        # Getting the min and the max date
        self.startDate = pd.to_datetime(self.df["Date"]).min()
        self.EndDate = pd.to_datetime(self.df["Date"]).max()

        with self.col1:
            date1 = pd.to_datetime(st.date_input("Start Date", self.startDate))

        with self.col2:
            date2 = pd.to_datetime(st.date_input("End Date", self.EndDate))

        self.df = self.df[
            (pd.to_datetime(self.df["Date"]) >= date1) & (pd.to_datetime(self.df["Date"]) <= date2)].copy()

    # En esta función se meterían los filtros que tendría el gráfico dependiendo de lo seleccionado
    def modify(self):

        # filter the data based on region, city and customer
        self.options = {"City": self.region, "Branch": self.state, "Customer type": self.customer}
        self.filtered_df = self.df.copy()

        for key in self.options.keys():
            if self.options[key] != []:
                self.filtered_df = self.filtered_df[self.filtered_df[key].isin(self.options[key])]

#        if not self.region and not self.state and not self.customer:
#            self.filtered_df = self.df
#        elif not self.state and not self.customer:
#            self.filtered_df = self.df[self.df["City"].isin(self.region)]
#        elif not self.region and not self.customer:
#            self.filtered_df = self.df[self.df["Branch"].isin(self.state)]
#        elif self.state and self.customer:
#            self.filtered_df = self.df[self.df["Branch"].isin(self.state) & self.df["Customer type"].isin(self.customer)]
#        elif self.state and self.region:
#            self.filtered_df = self.df[self.df["Branch"].isin(self.state) & self.df["City"].isin(self.region)]
#        elif self.region and self.customer:
#            self.filtered_df = self.df[self.df["City"].isin(self.region) & self.df["Customer type"].isin(self.customer)]
#        elif self.customer:
#            self.filtered_df = self.df[self.df["Customer type"].isin(self.customer)]
#        else:
#            self.filtered_df = self.df[self.df["City"].isin(self.region) & self.df["Branch"].isin(self.state) & self.df["Customer Type"].isin(self.customer)]

        self.category_df = self.filtered_df.groupby(by=["Product line"], as_index=False)["Total"].sum()

    #Aquí se crean los gráficos si se ha elegido Product chart
    def product(self):
        st.subheader("Product line with Total")

        # El siguiente if es para ver dos ejemplos distintos, solo nos quedaremos con uno. Las opciones son:

        # Se crea una función por cada tipo de gráfico, que podemos personalizar toda la que queramos. Se pondría
        # como valor del diccionario el nombre de la función correspondiente, creada por nosotros (ej. self.bar)

        # Si todos los gráficos tienen los mismos parámetros y solo se diferencia en el tipo, se puede poner como
        # valor del diccionario el nombre de la función que crea el gráfico (ej. px.line), lo que nos ahorraría
        # crear funciones
        if self.selected_type == "Line":
            self.fig = self.product_chart[self.selected_type](self.category_df, x="Product line", y="Total",
                                                              text=['${:,.2f}'.format(x) for x in
                                                                    self.category_df["Total"]], template="seaborn")
            st.plotly_chart(self.fig, use_container_widht=True, height=200)
        else:
            self.product_chart[self.selected_type]()

        with st.expander("Product_ViewData"):
            st.write(self.category_df.style.background_gradient(cmap="Blues"))
            csv = self.category_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv",
                               help="Click here to download the data as CSV file")

    # Aquí se crean los gráficos si se ha elegido City chart
    def city(self):
        st.subheader("City with Total")
        self.city_chart[self.selected_type]()

        with st.expander("City_ViewData"):
            city = self.filtered_df.groupby(by="City", as_index=False)["Total"].sum()
            st.write(city.style.background_gradient(cmap="Oranges"))
            csv = city.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="City.csv", mime="text/csv",
                               help="Click here to download the data as CSV file")

    def area(self):
        self.fig = px.area(self.category_df, x="Product line", y="Total",
                           text=['${:,.2f}'.format(x) for x in self.category_df["Total"]], template="seaborn")
        st.plotly_chart(self.fig, use_container_widht=True, height=200)

    def bar(self):
        self.fig = px.bar(self.category_df, x="Product line", y="Total",
                          text=['${:,.2f}'.format(x) for x in self.category_df["Total"]], template="seaborn")
        st.plotly_chart(self.fig, use_container_widht=True, height=200)

    # def line(self):
        #self.fig = px.line(self.category_df, x="Product line", y="Total",
                           #text=['${:,.2f}'.format(x) for x in self.category_df["Total"]], template="seaborn")
        #st.plotly_chart(self.fig, use_container_widht=True, height=200)

    def pie(self):
        fig = px.pie(self.filtered_df, values="Total", names="City", hole=0.5)
        fig.update_traces(text=self.filtered_df["City"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    dataApplication = MyApp()
    dataApplication.main()
