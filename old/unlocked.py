import time
import ctypes

user32 = ctypes.windll.User32
OpenDesktop = user32.OpenDesktopA
SwitchDesktop = user32.SwitchDesktop
DESKTOP_SWITCHDESKTOP = 0x0100

user32.LockWorkStation()
#
# Slight pause to overcome what appears to
# be a grace period during which a switch
# *will* succeed.
#
time.sleep (1.0)

while 1:
  hDesktop = OpenDesktop("default", 0, False, DESKTOP_SWITCHDESKTOP)
  result = SwitchDesktop(hDesktop)
  if result:
    print( "Unlocked")
    break
  else:
    print( time.asctime (), "still locked")
    time.sleep (2)
