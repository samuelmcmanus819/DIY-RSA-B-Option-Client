import MyIO
import base64
import math
import hashlib
class PublicKey:
    def __init__(self, e, n):
        self.e = e
        self.n = n
    """
    Name: EncryptFile
    Purpose: To encrypt a file and write the ciphertext to another file
    Param Source: The file where the plaintext is read from
    Param Destination: The file where the ciphertext is written to
    Author: Samuel McManus
    Uses: MyIO.ReadFile, MyIO.WriteEncodedFile
    Date: September 30, 2020
    """
    def EncryptFile(self, Source, Destination):
        #Read the source file and encode it to base64. This is necessary to decode some characters later,
        #particularly "-"
        Plaintext = MyIO.ReadFile(Source)
        PlaintextEncoded = str(base64.b64encode(Plaintext.encode("utf-8")), "utf-8")
        Ciphertext = ""
        for i in PlaintextEncoded:
            #Take the integer value of one ascii character and encrypt it
            CharsIntValue = ord(i)
            EncryptedInt = (CharsIntValue**self.e) % self.n
            #If the Encrypted int is out of the range of ascii characters, then split it into 2 
            #encrypted integers, then transform them into ascii characters
            if(EncryptedInt > 255):
                EncryptedInt2 = EncryptedInt % 100
                EncryptedInt = math.floor(EncryptedInt/100)
                Ciphertext = Ciphertext + chr(EncryptedInt)
                Ciphertext = Ciphertext + chr(EncryptedInt2)
            #If the Encrypted integer is in the range of ascii characters, then just
            #transform the integer directly to a character
            else:
                Ciphertext = Ciphertext + chr(EncryptedInt)
            Ciphertext = Ciphertext + " "
        Ciphertext = str(base64.b64encode(Ciphertext.encode("utf-8")), "utf-8")
        #Ascii-armor the ciphertext
        MyIO.WriteEncodedFile(Destination, Ciphertext)
    """
    Name: DecryptHash
    Purpose: To decrypt a signed hash
    Param Message: The message sent by the signer
    Param Ciphertext: The signed hash
    Param Destination: The file to store the message in
    Author: Samuel McManus
    Date: October 2, 2020
    """
    def DecryptHash(self, Message, Ciphertext, Destination):
        i = 0
        Plaintext = ""
        #Decode the ascii-armored ciphertext
        Ciphertext = str(base64.b64decode(Ciphertext), ('utf-8'))
        while(i < len(Ciphertext)): 
            #If the character after i is a space, then we know that the one character of ciphertext 
            #maps to a single character of plaintext.
            #If this is the case, then get the integer value of the character, decrypt it, and 
            #transform it into ascii again
            if(Ciphertext[i + 1] == " "):
                CharsIntValue = ord(Ciphertext[i])
                DecryptedInt = (CharsIntValue ** self.e) % self.n
                Plaintext = Plaintext + chr(DecryptedInt)
            #If the character after i is a space, then we know that two characters of ciphertext
            #map to a single character of plaintext.
            #Here, we first have to combine the two integer values of the ciphertext back into one,
            #Decrypt the value, then transform it back into ascii
            else:
                CharsIntValue = ord(Ciphertext[i])
                CharsIntValue1 = ord(Ciphertext[i+1])
                CharsIntValue = (CharsIntValue * 100) + CharsIntValue1
                DecryptedInt = ((CharsIntValue ** self.e) % self.n)
                Plaintext = Plaintext + chr(DecryptedInt)
                i = i + 1
            i = i + 2
        #Decode the plaintext from base64
        Plaintext = str(base64.b64decode(Plaintext), ('utf-8'))
        #Calculate the SHA-256 and SHA-512 hashes of the message
        CalculatedHash0 = SHA256Hash(Message)
        CalculatedHash1 = SHA512Hash(Message)
        #Store the given hashes of the message in a variable
        GivenHash0 = Plaintext.split("\n")[0]
        GivenHash0 = GivenHash0.split(": ")[1]
        GivenHash1 = Plaintext.split("\n")[1]
        GivenHash1 = GivenHash1.split(": ")[1]
        #If the hashes match, write them to a file. Otherwise, tell the user
        #that they obtained a forged message
        if(CalculatedHash0 != GivenHash0 or CalculatedHash1 != GivenHash1):
            print("This message is forged")
        else:
            MyIO.WriteFile(Destination, Message)
class PrivateKey:
    def __init__(self, d, n):
        self.d = d
        self.n = n
    """
    Name: DecryptFile
    Purpose: Decrypt a ciphertext file and write it to a plaintext file
    Param Source: The source ciphertext file
    Param Destination: The destination plaintext file
    Uses: MyIO.ReadEncodedFile, MyIO.WriteFile
    Used By: Main
    Date: September 30, 2020
    """
    def DecryptFile(self, Source, Destination):
        #Get the Ciphertext from the utf-8 encoded file
        Ciphertext = MyIO.ReadEncodedFile(Source)
        Plaintext = ""
        i = 0
        Ciphertext = str(base64.b64decode(Ciphertext), "utf-8")
        while(i < len(Ciphertext)):
            #If the character after i is a space, then we know that the one character of ciphertext 
            #maps to a single character of plaintext.
            #If this is the case, then get the integer value of the character, decrypt it, and 
            #transform it into ascii again
            if(Ciphertext[i + 1] == " "):
                CharsIntValue = ord(Ciphertext[i])
                DecryptedInt = (CharsIntValue ** self.d) % self.n
                Plaintext = Plaintext + chr(DecryptedInt)
            #If the character after i is a space, then we know that two characters of ciphertext
            #map to a single character of plaintext.
            #Here, we first have to combine the two integer values of the ciphertext back into one,
            #Decrypt the value, then transform it back into ascii
            else:
                CharsIntValue = ord(Ciphertext[i])
                CharsIntValue1 = ord(Ciphertext[i+1])
                CharsIntValue = (CharsIntValue * 100) + CharsIntValue1
                DecryptedInt = ((CharsIntValue ** self.d) % self.n)
                Plaintext = Plaintext + chr(DecryptedInt)
                i = i + 1
            i = i + 2
        #Lastly, you have a base64 encoded text, so we have to decode it and write it
        #to a file
        Plaintext = str(base64.b64decode(Plaintext), "utf-8")
        MyIO.WriteFile(Destination, Plaintext)


    """
    Name: DigitallySign
    Purpose: Encrypt a plaintext file and a message hash with the user's private key
    Param Message: The message to be signed
    Author: Samuel McManus
    Date: October 1, 2020
    """
    def DigitallySign(self, Message):
        Ciphertext = ""
        #Creates a hash of the message using SHA-256 and SHA-512
        Hash = "SHA-256 Hash: " + SHA256Hash(Message) + "\nSHA-512 Hash: " + SHA512Hash(Message)
        #Encode the hash to base64 so that we don't lose any characters
        Hash = str(base64.b64encode(Hash.encode("utf-8")), "utf-8")
        for i in Hash:
            #Take the integer value of one ascii character and encrypt it
            CharsIntValue = ord(i)
            EncryptedInt = (CharsIntValue**self.d) % self.n
            #If the Encrypted int is out of the range of ascii characters, then split it into 2 
            #encrypted integers, then transform them into ascii characters
            if(EncryptedInt > 255):
                EncryptedInt2 = EncryptedInt % 100
                EncryptedInt = math.floor(EncryptedInt/100)
                Ciphertext = Ciphertext + chr(EncryptedInt)
                Ciphertext = Ciphertext + chr(EncryptedInt2)
            #If the Encrypted integer is in the range of ascii characters, then just
            #transform the integer directly to a character
            else:
                Ciphertext = Ciphertext + chr(EncryptedInt)
            Ciphertext = Ciphertext + " "
        #Return the message plus an ascii-armored encrypted hash
        return Message + "Hash:" + str(base64.b64encode(Ciphertext.encode("utf-8")), "utf-8")


"""
Name: SHA256Hash
Purpose: To obtain a SHA-256 hash for a message
Param Message: The message to be hashed
Return: The hash of the message
Date: October 1, 2020
"""
def SHA256Hash(Message):
    MessageBytes = bytes(Message, "utf-8")
    Sha = hashlib.sha256()
    Sha.update(MessageBytes)
    return Sha.hexdigest()

"""
Name: SHA512Hash
Purpose: To obtain a SHA-512 hash for a message
Param Message: The message to be hashed
Return: The hash of the message
Date: October 1, 2020
"""
def SHA512Hash(Message):
    MessageBytes = bytes(Message, "utf-8")
    Sha = hashlib.sha512()
    Sha.update(MessageBytes)
    return Sha.hexdigest()
    
