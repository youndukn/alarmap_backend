from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json
import datetime

import prompts
import llm
import folium

# Use the application default credentials
cred = credentials.Certificate('./credentials.json') # Replace with the path to your JSON file
firebase_admin.initialize_app(cred)

db = firestore.client()
url = "https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?menuSeq=679"

driver = webdriver.Chrome()

while True:
    driver.get(url)
    
    # Find the tbody element by its ID
    tbody = driver.find_element(By.ID, 'disasterSms_tr')

    # Find the table rows within the tbody
    table_rows = tbody.find_elements(By.XPATH, './/tr[starts-with(@id, "disasterSms_tr_")]')

    # Iterate through the rows and get the required information
    for row in table_rows:
        row_id = row.get_attribute('id').replace('_apiData1', '')
        disaster_info = {}
        disaster_info['id'] = row.find_element(By.ID, row_id + '_MD101_SN').text
        disaster_info['ds_type'] = row.find_element(By.ID, row_id + '_DSSTR_SE_NM').text
        disaster_info['em_type'] = row.find_element(By.ID, row_id + '_EMRGNCY_STEP_NM').text
        disaster_info['title'] = row.find_element(By.TAG_NAME, 'a').get_attribute('title')

        # Check if the disaster with the given id already exists
        disaster_ref = db.collection('disasters').document(disaster_info['id'])
        if disaster_ref.get().exists:
            print(f"Already exists: {disaster_info['id']}")
        else:
            # Add the data to Firestore
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # prompt_current = prompts.prompt_generate.format(disaster_info['title'], current_time)
            
            # generated_text = llm.generate_text(prompt_current)
            # prompt_current1 = prompts.prompt_validation.format(disaster_info['title'], current_time, generated_text)
            generated_text1 = llm.chatgpt_generate_text(disaster_info['title'], current_time)
            time.sleep(3)
            # print("generated\n",generated_text)
            
            if len(generated_text1) > 0:
                print("corrected\n",generated_text1)
                print("current_time", current_time)
                try: 
                    deserialized_json = json.loads(generated_text1)
                except:
                    print("Error in creatingjson", disaster_info)
                else:
                    disaster_info['gpt'] = deserialized_json

                    # keywords = []

                    # for subdistrict in deserialized_json["location"]["subdistricts"]:
                    #     # print(deserialized_json["location"]["district"]+subdistrict)
                    #     a = input(deserialized_json["location"]["district"]+subdistrict)
                    #     if len(a) > "":
                    #         keywords.append({"name": deserialized_json["location"]["district"]+subdistrict, "address": })

                    # for landmark in deserialized_json["location"]["landmarks"]:
                    #     a = input(deserialized_json["location"]["district"]+landmark["name"])
                    #     if len(a) > "":
                    #     a = input(deserialized_json["location"]["district"]+landmark["detail"])
                    #     if len(a) > "":
                    #     a = input(deserialized_json["location"]["district"]+landmark["name"]+ " "+ ["detail"])
                    #     if len(a) > "":
                    
                    
                    # deserialized_json["location"]["addresses"] = keywords
                finally:
                    disaster_ref.set(disaster_info)
                    print(f"Stored: {disaster_info}")
    time.sleep(60*4)                       
    

# Close the WebDriver
driver.quit()

