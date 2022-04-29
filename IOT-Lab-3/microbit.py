def on_data_received():
    global cmd
    cmd = serial.read_until(serial.delimiters(Delimiters.HASH))
    basic.show_string(cmd)
    if cmd == "0":
        basic.show_number(0)
    elif cmd == "1":
        basic.show_number(1)
    elif cmd == "2":
        basic.show_number(2)
    elif cmd == "3":
        basic.show_number(3)
serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)

cmd = ""
interval = 5

def on_forever():
    global interval
    if interval == 5:
        serial.write_string("!1:TEMP:" + ("" + str(input.temperature())) + "#")
    if interval == 10:
        serial.write_string("!1:LIGHT:" + ("" + str(input.light_level())) + "#")
        interval = 0
    interval = interval + 1
    basic.pause(1000)
basic.forever(on_forever)
