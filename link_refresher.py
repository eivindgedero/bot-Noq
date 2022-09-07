import webbrowser
import os

def link_refresher():  
  with open('file_with_links.txt', 'r') as file:
    for line in file.readlines():
      webbrowser.open(line)
link_refresher()
os.system("taskkill /im chrome.exe /f")