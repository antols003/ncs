from getmyip import *
mqtt_username = "oora"
mqtt_password = "oora"
mqtt_topic = "NCS01/#"
mqtt_broker_ip = get_ip()
print("IP Address is:" + get_ip())
DB_Name =  "datafarm.db"
#noofrows=2
#noofcolumn=4
#numberseries=0 #serial number starting digit
actualbedcount=9
dsptxt=	{
  1: "201",
  2: "202",
  3: "203",
  4: "204",
  5: "205",
  6: "206",
  7: "207",
  8: "208",
  9:"209",
  10:"210",
  11:"211",
  12:"213",
  13:"214"
  }

# for index_auto.html
# noofrows=4
# noofcolumn=4
# numberseries=200
# actualbedcount=16
# dsptxt=	{
#   1: "0"
# }
#for index_custom.html
# noofrows=4
# noofcolumn=4
# numberseries=0
# actualbedcount=16
# dsptxt=	{
#   1: "Ford",
#   2: "Mustang",
#   3: "1964",
#   4: "1954",
#   5: "1974",
#   6: "1994"
# }
