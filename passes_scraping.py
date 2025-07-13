from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


columns = ["name", "team", "completed_passes", "total_passes"]


def get_player_stat(row):
    data = row.text.split("\n")

    content = {}

    for idx in range(1, 5):
        content[columns[idx - 1]] = data[idx]
    return content


def main():
    driver = webdriver.Chrome()
    player_data = []
    for page_number in range(1, 38):
        page_url = f"https://www.laliga.com/en-GB/stats/laliga-easports/passes/page/{page_number}"
        driver.get(page_url)
        time.sleep(2)

        if page_number == 1:
            accept_button = driver.find_element(
                By.XPATH, "//button[text()='Accept all']"
            )
            accept_button.click()

        table = driver.find_element(By.TAG_NAME, "tbody")

        rows = table.find_elements(By.TAG_NAME, "tr")

        for idx, row in enumerate(rows):
            player_data.append(get_player_stat(row))

    driver.quit()

    df = pd.DataFrame(data=player_data, columns=columns)
    df.to_csv("player_passes.csv", mode="w", header=True)


main()
