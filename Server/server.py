"""
  Adding employees:
  - When someone enters your group in the client GUI menu press Add Employee.
  - In the new tab enter the name and password.
  - After that it will ask for a picture, make sure to give one where 
    the face is visible and clear.
  - Press 'Done' and you're done, a new employee was added.
"""

"""
  Start of operations:
  - The server initializes the loging in feature.
  - Client enters and gives a name that exists with the correct password,
    the check is done by encrypting the password and checking if the encrypted
    entered password is the same as the stored one.
  - Server checks and then sends the client the encrypted image of the employee.
  - Client does the decrypting with the user_key and checks if the faces match.
  - If they match the server accepts the client and gives confirmation.
"""

import socket