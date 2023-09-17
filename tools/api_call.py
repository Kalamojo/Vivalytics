import requests
import json


def gpt_res(prompt):
  url = "https://kalamojo.pythonanywhere.com/api5?prompt=" + prompt
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("GET", url, headers=headers)

  res = response.json()

  return res

def gpt_res2(prompt):
  url = "https://kalamojo.pythonanywhere.com/api6?prompt=" + prompt
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("GET", url, headers=headers)

  res = response.json()

  return res

def gpt_res3(prompt, pos, table):
  data = {'pos': pos, 'table': table}
  url = f"https://kalamojo.pythonanywhere.com/api7?prompt={prompt}"

  response = requests.request("GET", url, json=data)
  print(response)

  res = response.json()

  return res