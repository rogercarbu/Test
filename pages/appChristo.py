# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 08:13:18 2024

@author: GoCh810
"""

import streamlit as st
import os
from PIL import Image
import datetime

class dataApp:
    
    def __init__(self):

        self.title = "Streamlit DTT Visualization Tool"
        self.sidebar_options = ["Visualization Tool", "Second Option Tool"]
        self.path_to_logo = Image.open('Logo Primario Digital -S2G.png')
        
        
    def run(self):
        st.set_page_config(page_title=self.title, layout="wide")
        self.show_sidebar()
        self.show_main_content()

    def show_sidebar(self):
        self.elementType = 'sidebar'


        self.show_image(os.getcwd() + '/Logo Primario Digital -S2G.png')
        st.sidebar.title("Navigation")
        st.sidebar.write('Start Date')


        self.startDate = st.sidebar.date_input("Start Date", value=datetime.date(2000,1,1))
        self.endDate = st.sidebar.date_input("End Date")


        self.selected_page = st.sidebar.radio("Go to", self.sidebar_options)

    def show_main_content(self):
        self.elementType = 'maincontent'
        
        st.title(self.title)
        if self.selected_page == "Visualization Tool":
            self.show_visualization_tool()
        elif self.selected_page == "Second Option Tool":
            self.show_second_option_tool()


    def show_visualization_tool(self):
        st.markdown("# Business Visualization Tool")
        col1, col2 = st.columns([1,3])
        with col1:
            self.boolFile = st.checkbox('I would like to upload my own file')
            self.show_uploadfile(self.boolFile)
        with col2:
            st.markdown('### Selected Filters')
            filtercontainer = st.container(border=True)
            filtercontainer.write('asdadadsa')
            
            
    
    def show_second_option_tool(self):
        st.write("# Possible Second Function of the code")



    def show_image(self, path_to_image):
       self.binimg = Image.open(path_to_image)
       if self.elementType == 'sidebar':
            st.sidebar.image(self.binimg)
       elif self.elementType == 'maincontent':
            st.image(self.binimg)
            
            
            
    def show_uploadfile(self, boolFile):
        if boolFile:
            st.file_uploader('Please, upload your data file: ', accept_multiple_files=False)
        

if __name__ == "__main__":
    dataApplication = dataApp()
    dataApplication.run()



