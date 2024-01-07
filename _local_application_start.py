# Author:		Michael Rubin
# Created:		1/5/2024
# Modified:	    1/6/2024
#
# Copyright 2023 - 2024 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------------
import json
import os
from pynput import keyboard
import lambda_function
import global_utility as gu

gu.isLocalDevelopment = True
gu.useLocalSecret = True

with open("local-secret.json") as f:
    gu.localSecret = json.load(f)

files = []

print("Select Test Case Folder ([Esc] to exit)\n{}".format("-" * 35))
print("1. Content Test Cases")
print("2. Image Test Cases")
print("3. Recipe Test Cases")
print("4. RecipeContent Test Cases")
print()


print()
folder = None


# key handler, invoked from keyboard.Listener
def onPress(key):
    global folder
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    index = -1
    if key == keyboard.Key.esc:
        return False
    try:
        if not key.vk and not key.char:
            pass
        elif key.vk and (key.vk in range(49, 53) or key.vk in range(97, 101)):
            index = key.vk if key.vk in range(49, 53) else key.vk - 48
            if index == 49:
                folder = "TestCases/Content/"
            elif index == 50:
                folder = "TestCases/Image/"
            elif index == 51:
                folder = "TestCases/Recipe/"
            elif index == 52:
                folder = "TestCases/RecipeContent/"

            print("Select a Test Case ([Esc] to exit)\n{}".format("-" * 35))
            index = 0
            for filename in os.listdir(folder):
                if ".json" in filename:
                    files.append(filename)
                    print(
                        "{}. {}".format(
                            alphabet[index],
                            filename.replace(".json", ""),
                        )
                    )
                    index += 1
            print()
            index = -1
        else:
            index = key.vk - 65
            if index == -1:
                raise Exception(f"Key {key} not found")
            else:
                with open(f"{folder}{files[index]}") as f:
                    event = json.load(f)
                    if (
                        "params" in event
                        and "header" in event["params"]
                        and "Authorization" in event["params"]["header"]
                    ):
                        with open("accesstoken.txt") as f_token:
                            event["params"]["header"][
                                "Authorization"
                            ] = f"Bearer {f_token.read()}"

                response = lambda_function.lambda_handler(event, None)
                if isinstance(response, dict):
                    # filename = "D:\\Michael\\Desktop\\API_output.json"
                    filename = "C:\\Users\Michael\\Desktop\\API_output.json"
                    try:
                        responseJson = json.dumps(response, indent=2)
                        with open(filename, "w") as f:
                            f.write(responseJson)
                        print(responseJson)
                    except Exception as e:
                        with open(filename, "w") as f:
                            f.write(str(response))
                        ex = e
                        print(response)
                else:
                    print(response)
            return False

    except BaseException as e:
        print(f"{key} {e}\n")
        return False


# key handler, invoked from keyboard.Listener
def onRelease(key: keyboard.Key):
    try:
        if not (key.vk in range(49, 53) or key.vk in range(97, 101)):
            raise Exception
    except Exception as e:
        e = None
        return False


# key handler: listener requires on_press and on_release loaded beforehand
with keyboard.Listener(on_press=onPress, on_release=onRelease) as listener:
    listener.join()
