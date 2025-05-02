import win32com.client
import re


def get_messages(limit=3, unread=False):

    # getting all the messages
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    inbox = namespace.GetDefaultFolder(6)  # 6 is the inbox btw
    messages = inbox.Items

    # sorting by most recent and potentially only unread
    messages.Sort("[ReceivedTime]", True)
    if unread:
        messages = messages.Restrict("[Unread] = true")

    # getting info about the emails
    result = []
    for i in range(min(limit, messages.Count)):
        item = messages.Item(i + 1)  # indexing for COM starts at 1 for some reason??
        email_details = {
            "Sender": item.SenderName,
            "Subject": item.Subject,
            "Body": item.Body,
            "Parts": find_parts(item.subject + " " + item.Body)
        }
        result.append(email_details)
    return result


def find_parts(text):
    matches = re.findall(r"W[HM]\.?\d+|\d{2}\.\d{5}-\d{4}", text)
    result = ' '.join(matches)
    return result
