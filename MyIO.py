import pathlib
"""
Name: GetInt
Purpose: Receive an integer value from the user
Param UserMessage: The message to tell the user to input an integer
Return: The integer entered by the user
Author: Samuel McManus
Used By: Main
Date: September 3, 2020
"""
def GetInt(UserMessage):
    while True:
        try:
            value = int(input(UserMessage))
        except ValueError:
            print("That value is not an integer. Please try again.")
        else:
            return value
"""
Name: GetExistingFile
Purpose: Gets the name of a file which already exists
Param UserMessage: The message to tell the user to input an existing filename
Return: The name of the file if it exists
Author: Samuel McManus
Used By: PublicKey.EncryptFile, PrivateKey.DecryptFile
Date: September 30, 2020
"""
def GetExistingFile(UserMessage):
    while True:
        filename = input(UserMessage)
        file = pathlib.Path(filename)
        if file.exists():
            return filename
        else:
            print("That is not a valid file")
"""
Name: GetNewFile
Purpose: Gets the name of a file which does not exist, or which the user wants to overwrite
Param UserMessage: The message to tell the user to input a filename
Return: The name of the chosen file
Author: Samuel McManus
Used By: PublicKey.EncryptFile, PrivateKey.DecryptFile
Date: September 30, 2020
"""
def GetNewFile(UserMessage):
    while True:
        filename = input(UserMessage)
        try:
            f = open(filename, "x")
            f.close()
            return filename
        except FileExistsError:
            valid = input("That file already exists. Are you sure that you want to overwrite it? y/n ")
            if(valid == "y"):
                return filename
"""
Name: ReadFile
Purpose: Returns the text held in a file
Param Filename: The name of the file to be read
Return: The text held in the chosen file
Author: Samuel McManus
Used By: PublicKey.Encrypt
Date: September 30, 2020
"""
def ReadFile(Filename):
    try:
        f = open(Filename, "r")
        a = f.read()
        f.close()
        return a
    except FileNotFoundError:
        return ""
"""
Name: ReadEncodedFile
Purpose: Returns text from an encoded file
Param Filename: The name of the file to be read
Return: The content of the file
Author: Samuel McManus
Used By: PrivateKey.Decrypt
Date: September 30, 2020
"""
def ReadEncodedFile(Filename):
    f = open(Filename, "r", encoding="utf-8")
    a = f.read()
    f.close()
    return a
"""
Name: WriteEncodedFile
Purpose: Encodes a string to utf-8 and writes it to a file
Param Filename: The name of the file to be written to
Param Text: The text being written to the file
Author: Samuel McManus
Used By: PublicKey.Encrypt
Date: September 30, 2020
"""
def WriteEncodedFile(Filename, Text):
    f = open(Filename, "w", encoding="utf-8")
    f.write(Text)
    f.close()
"""
Name: WriteFile
Purpose: Writes text to a file
Param Filename: The file to be written to 
Param Text: The text to be written to the file
Author: Samuel McManus
Used By: PrivateKey.Decrypt
Date: September 30, 2020
"""
def WriteFile(Filename, Text):
    f = open(Filename, "w")
    f.write(Text)
    f.close()

"""
Name: TrimSocket
Purpose: To trim the string received over the socket
Param Text: The text received over the socket
Return: The text received with the leading b' and ending ' removed
Author: Samuel McManus
Date: October 1, 2020
"""
def TrimSocket(Text):
    Text = Text.decode("utf-8")
    return Text
