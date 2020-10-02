import socket
import MyIO
import Encryption
Host = '127.0.0.1'
Port = 12345


DestinationFilename = MyIO.GetNewFile("Enter the name of the file you want to store the results in: ")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as S:
    S.connect((Host, Port))
    while True:
        Filename = input("Enter the name of the file you want to get from the server: ")
        S.sendall(bytes(Filename, "utf-8"))
        Good = S.recv(4096)
        Good = MyIO.TrimSocket(Good)
        if(Good == "good"):
            break
        else:
            print("You've entered an invalid file name. Please try again.")
    publickey = MyIO.TrimSocket(S.recv(4096))
    e = int(publickey.split()[0])
    n = int(publickey.split()[1])
    MyPubKey = Encryption.PublicKey(e, n)
    Message = MyIO.TrimSocket(S.recv(1048576))
    SignedHash = Message.split("Hash:")[1]
    Message = Message.split("Hash:")[0]
    MyPubKey.DecryptHash(Message, SignedHash, DestinationFilename)
