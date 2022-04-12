from file.models import FileData, File


def form_ws_message_data(data):

    file_data_list = list()
    for file_data_object in data:
        name = file_data_object.file_url.split("/")[-1]
        file_data_list.append({"id": file_data_object.pk, "name": name, "url": file_data_object.file_url})

    return file_data_list


def get_file_data(room_name=None, room_ip=None):
    """
    :param room_ip:
    :param room_name
    :return clipboard_data:
    """

    try:
        if room_name:
            clipboard_obj = File.objects.filter(room_name=room_name)
        elif room_ip:
            clipboard_obj = File.objects.filter(room_ip=room_ip)
        else:
            clipboard_obj = File.objects.all()
    except Exception as e:
        print("Data not found", e)
        return "Data not found"
    else:

        return [d.get_formatted_data() for d in clipboard_obj]
