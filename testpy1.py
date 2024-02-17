import requests

url = 'https://discord.com/api/webhooks/1058089613689888768/a0hqsSxSyhLxlHeA6jjOK0OEZQGbMk1SXikaX_ggvmwg9YNOZAqZ740Dsb65ppbKwBdV'

json = {"content": '''Hey there, @everyone

I've got some exciting news to share with all of you. Dexvmaster0 is making a comeback, but with a twist – introducing Xvirus-Firmware!

I have a deep passion for this project, and it's been on my mind for a while now. I wanted to keep the momentum going right here on this server. However, discord took an unexpected turn, and I lost access to this server. But you know what they say, when one door closes, another one opens. So, I'm reaching out to all of you to hop on board the new train at https://discord.gg/xvirustool.

The new server is a fresh start, a clean slate, and an opportunity to build something amazing together. We're not just continuing from where we left off; we're taking it to the next level. Your presence and support would mean the world to me as we embark on this exciting journey.

From now on, all the action and updates will happen exclusively on our new server. I'm genuinely hoping to breathe new life into my firmware, and with your help, I'm confident we can do it.

For those tech enthusiasts out there who want to dive into the nitty gritty details, you can find the code for Xvirus-Firmware at https://github.com/Xvirus-Team/xvirus-firmware.

So, what do you say? Let's rally together, bring the Xvirus-Firmware community back to life, and make it even better than before. Your enthusiasm, ideas, and contributions are not only welcome but essential to our success.

Thanks a bunch for your support, and I can't wait to see you on our new platform!'''}

response = requests.post(url, json=json)

if response.status_code == 204 or response.status_code == 200:
    print(f"<*> Message sent({response.status_code}) ({response.text})")
else:
    print(f"<!> Error: ({response.status_code}) ({response.text})")