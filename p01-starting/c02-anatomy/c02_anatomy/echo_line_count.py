ls_cmd_list = ["ls" "/tmp/images/"]
ls_cmd_str = " ".join(ls_cmd_list)

wc_cmd_list = ["wc", "-l"]
wc_cmd_str = " ".join(wc_cmd_list)

ls_to_wc_pipe = f"$({ls_cmd_str} | {wc_cmd_str})"
notify_cmd_list = ["echo", f"There are now {ls_to_wc_pipe} images."]

notify_cmd_str = " ".join(notify_cmd_list)
