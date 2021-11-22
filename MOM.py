import streamlit as st
import pandas as pd
import numpy as np
import os.path
if not (os.path.isfile("data.csv")):
    data = pd.DataFrame()
    data['Rack']=[]
    data['Item']=[]
    data['Item Description']=[]
    data.to_csv("data.csv",index=False)

def add_items():
    placeholder1 = st.empty()
    placeholder2 = st.empty()
    data=pd.read_csv("data.csv")
    rack=st.radio("Select Area",('Left Shelf', 'Right Shelf', 'Top Shelf','Bottom Shelf','Locker'))
    item=placeholder1.text_input("Enter Item")
    item_description = placeholder2.text_input("Enter Item Description")
    raw_data=pd.DataFrame({'Rack':[rack],'Item':[item],'Item Description':[item_description]})
    new_data=pd.concat([data,raw_data] ,ignore_index=True,axis=0)
    if(st.button("Save")):
        st.info("Item Added")
        item = placeholder1.text_input('Enter Item', value='', key=1)
        item_description = placeholder2.text_input('Enter Item Description', value='', key=1)
        new_data.sort_values(['Rack', 'Item'],inplace=True)
        new_data.to_csv("data.csv",index=False)
    return new_data

def search_items():
    data = pd.read_csv("data.csv")
    item_list = data['Item'].values.tolist()
    item_list_set = set(item_list)
    item_list = (list(item_list_set))
    searched_item = st.multiselect("Enter Item to be searched", item_list)
    details = data[data['Item'].isin(searched_item)]
    details=details[['Rack','Item','Item Description']]
    if details.shape[0] > 0:
        st.dataframe(details)

def delete_items():
    indicies_to_be_deleted=[]
    data = pd.read_csv("data.csv")
    for ind in data.index:
        dict={ind:(data['Rack'][ind], data['Item'][ind],data['Item Description'][ind])}
        option=st.checkbox(str(dict))
        if option:
            indicies_to_be_deleted.append(ind)
    if (st.button("Confirm Delete")):
        indicies_to_be_deleted=list(indicies_to_be_deleted)
        data.drop(indicies_to_be_deleted,inplace=True)
        st.warning("Item Deleted")
        data.to_csv("data.csv",index=False)
        return

def flow():
    with st.expander("ADD"):
        add_items()
    with st.expander("SEARCH"):
        search_items()
    with st.expander("DELETE"):
        delete_items()
    if (st.button("DISPLAY")):
        data = pd.read_csv("data.csv")
        data.sort_values(['Rack','Item'],inplace=True)
        st.table(data)

if __name__ == '__main__':
    st.header("Organizer")
    password=st.text_input("Password: ", value="", type="password")
    if password=='archie':
        st.success("Welcome")
        flow()
    elif password=='':
        st.warning("Enter Password")
    else:
        st.error("Wrong Password entered")
