import socket
import MyIO
import Encryption
Host = '127.0.0.1'
Port = 12345
MyE = 3
MyD = 11787
MyN = 17947


DestinationFilename = MyIO.GetNewFile("Enter the name of the file you want to store the results in: ")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as S:
    S.connect((Host, Port))
    #Gets the file to request from the server
    while True:
        Filename = input("Enter the name of the file you want to get from the server: ")
        S.sendall(bytes(Filename, "utf-8"))
        Good = S.recv(4096)
        Good = MyIO.TrimSocket(Good)
        if(Good == "good"):
            break
        else:
            print("You've entered an invalid file name. Please try again.")
    #Sets the server's public key
    publickey = MyIO.TrimSocket(S.recv(4096))
    e = int(publickey.split()[0])
    n = int(publickey.split()[1])
    MyPubKey = Encryption.PublicKey(e, n)
    #Sets the client's private key
    MyPrivKey = Encryption.PrivateKey(MyD, MyN)
    #Sends the client's public key
    S.sendall(bytes(str(MyE) + " " + str(MyN), "utf-8"))
    #Receives the signed and encrypted message
    Message = MyIO.TrimSocket(S.recv(1048576))
    #Decrypts the message
    Message = MyPrivKey.Decrypt(Message)
    #Decrypts the hash, verifies it, and stores it in a file
    SignedHash = Message.split("Hash:")[1]
    Message = Message.split("Hash:")[0]
    MyPubKey.DecryptHash(Message, SignedHash, DestinationFilename)
