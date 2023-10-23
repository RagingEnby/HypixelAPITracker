import requests
import os
import time
import difflib

storage_file = 'response.html'
history_file = 'history/{}.html'
url = 'https://api.hypixel.net/'

def get_current_data():
  data = requests.get(url)
  return data.text

def get_past_data():
  try:
    with open(storage_file, 'r') as file:
      return file.read()
  except Exception:
    return None
    
def write_data(data):
  now = str(round(time.time()))
  with open(storage_file, 'w') as file:
    file.write(data)
  with open(history_file.format(now), 'w') as file:
    file.write(data)

def find_string_differences(before, after):
  d = difflib.Differ()
  before_lines = before.splitlines()
  after_lines = after.splitlines()

  lines_to_ignore = [
      '<script defer src="https://static.cloudflareinsights.com/beacon.min.js'
  ]

  before_lines = [line for line in before_lines if all(ignore not in line for ignore in lines_to_ignore)]
  after_lines = [line for line in after_lines if all(ignore not in line for ignore in lines_to_ignore)]

  diff = list(d.compare(before_lines, after_lines))
  changed_lines = [line for line in diff if line.startswith('- ') or line.startswith('+ ')]
  return changed_lines

def main():
  before = get_past_data()
  if before is None:
    write_data(get_current_data())
    return
  after = get_current_data()
  diff = find_string_differences(before, after)
  if diff != []:
    write_data(after)
    print('omg change')
    print(diff)
  else:
    print('no change :(')

while True:
  main()
  time.sleep(60 * 5)