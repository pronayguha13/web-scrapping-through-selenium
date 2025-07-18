from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pandas as pd
import time


def prepare_csv(data, columns, file_name):
    df = pd.DataFrame(data=data, columns=columns)
    # re ordered columns' name sequence
    new_columns = [
        "NAME",
        "POSITION",
        "MIN",
        "PLD",
        "TIT",
        "SUP",
        "SUST",
        "YC",
        "RC",
        "2Y",
        "GOALS",
        "PEN",
        "OG",
        "GC",
    ]
    df = df.reindex(columns=new_columns)
    # save the data frame into a csv file
    df.to_csv(path_or_buf=file_name, mode="w", header=True)


def prepare_data(row, columns):
    data = row.text.split("\n")
    content = {}
    for i in range(len(columns)):
        content[f"{columns[i]}"] = data[i + 1]
    return content


def scrap_data():
    player_data = []
    columns = [
        "POSITION",
        "NAME",
        "MIN",
        "PLD",
        "TIT",
        "SUP",
        "SUST",
        "YC",
        "RC",
        "2Y",
        "GOALS",
        "PEN",
        "OG",
        "GC",
    ]
    driver = webdriver.Chrome()
    url = "https://www.laliga.com/en-GB/clubs/fc-barcelona/stats"
    # get the page
    driver.get(url=url)
    time.sleep(2)
    # get the accept all button from the page
    accept_all_btn = driver.find_element(By.XPATH, "//button[text()='Accept all']")
    if accept_all_btn:
        accept_all_btn.click()
    # get the table element from the page
    table = driver.find_element(
        By.XPATH, "//table[contains(@class, 'styled__TableStyled')]"
    )
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        player_data.append(prepare_data(row=row, columns=columns))
    # prepare the csv file from the player_data list
    prepare_csv(data=player_data, columns=columns, file_name="BARCELONA.csv")


scrap_data()
