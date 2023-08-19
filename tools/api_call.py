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
