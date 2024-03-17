curl_command_list = [
    "curl",
    "-o", "/tmp/launches.json",
    "-L", "https://ll.thespacedevs.com/2.0.0/launch/upcoming"
]
curl_command_str = " ".join(curl_command_list)
