import time

def log(message):
  currentTime = time.strftime('%B %d,  %I:%M %p', time.localtime(time.time()))
  print(currentTime + "::: " + message)