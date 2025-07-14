from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

columns = ["NAME", "TEAM", "GOALS SCORED", "GAMES", "GOALS PER MATCHES"]


def get_player_stat(row):
    data = row.text.split("\n")

    content = {}

    content["NAME"] = data[1]
    content["TEAM"] = data[2]
    content["GOALS SCORED"] = data[3]
    content["GAMES"] = data[4]
    content["GOALS PER MATCHES"] = data[5]

    return content


def parse_content():
    total_pages = 37
    driver = webdriver.Chrome()
    player_data = []
    for page_number in range(1, 38):
        driver.get(
            f"https://www.laliga.com/en-GB/stats/laliga-easports/scorers/page/{page_number}"
        )
        time.sleep(2)
        table = driver.find_element(By.TAG_NAME, "tbody")
        rows = table.find_elements(By.TAG_NAME, "tr")

        for idx, row in enumerate(rows):
            player_data.append(get_player_stat(row))
    driver.close()

    df = pd.DataFrame(data=player_data, columns=columns)
    df.to_csv("player_stats.csv", mode="w", index=True, header=True)
    print(df)


parse_content()
