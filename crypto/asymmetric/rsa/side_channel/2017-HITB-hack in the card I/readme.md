Welcome to work for C.I.A. Our agent 47 has successfully penetrated to an evil company and sent this secret smart card to us. Intelligence department said the crypto chip on this card is doing RSA operation and the public key we got is [here]('./attachments/publickey.pem'). Your mission is to extract the private key embedded in this smart card and decrypt the following hex-encoded ciphertext. 

fe59520a80f7e88bc471ec9660805ef3da2703f7b2cc7260d8f9edb510da0b6470578c54b49d5e61b42f689698b9c4f6df67c1a01a611bfecb6edb323b90614300424dfc04391b6df59a9d6210f6f732d2fd3b6c3af9a8910ce3e7be616d2d8047cf688876617747731667ddb90e33588e8c1674b2da383b7922f3baad7d031daec3c7c98d54a1526b4f159ed13e8c8fc9b2c16ffb514a79c9dc7e76acd08743cab9c1a3e42c0e4ee5cc2c676a431e2a44e8b7bb74f676a85ca7c5475ce386394e968aad1bbf3ed8fb568164cc15388e24a5efc4ebf17cd9be741c19dbf3a4e67884f62cb386882d938d6254e51ac604b3d222c767039520ab6a33dec277f541

The progress of hacking was going well untill it got stuck, what we did so far is that as you can see the smartcard, an oscilloscope, a computer (act as the card reader) and a resistor are plugged into a circuit board. The circuit diagram is given as follows. 
![alt text](./attachments/circuitdiagram.png "Logo Title Text 1") 

We finally managed to decrypt a crafted message and captured [voltage variation]('./attachments/index.html') of the resistor during the whole process. Now we are counting on you to do the rest... 
