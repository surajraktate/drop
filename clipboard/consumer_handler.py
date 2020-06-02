from clipboard.models import  ClipBoardData


def store_message_into_database(clipboard_request_data):
    clipboard_obj = None
    room_name = clipboard_request_data.get("room_name")
    room_ip = clipboard_request_data.get("room_ip")
    room_data = clipboard_request_data.get("room_data")
    try:
        if room_name:
            clipboard_obj = ClipBoardData.objects.get(room_name=room_name)
        else:
            clipboard_obj = ClipBoardData.objects.get(room_ip=room_ip)
    except Exception as e:
        print(e, 'first')
    else:
        clipboard_obj.room_data = room_data
        clipboard_obj.room_ip = room_ip
        clipboard_obj.room_name = room_name if room_name else ""
        clipboard_obj.save()

    if not clipboard_obj:
        print("clipboard_request_data :", clipboard_request_data)
        try:
            clipboard_obj = ClipBoardData(room_ip=room_ip, room_data=room_data, room_name=room_name)
        except Exception as e:
            print(e, "Second")
        else:
            clipboard_obj.save()


def get_clipboard_data(room_name, room_ip):
    """
    :param room_ip:
    :param room_name
    :return clipboard_data:
    """

    try:
        if room_name:
            clipboard_obj = ClipBoardData.objects.get(room_name=room_name)
        else:
            clipboard_obj = ClipBoardData.objects.get(room_ip=room_ip)
    except Exception as e:
        print(e)
        return "Data not found"
    else:
        return clipboard_obj.room_data
