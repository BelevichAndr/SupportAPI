#SupportAPI
***
###Application for the support service.
***
Realized custom user model, divided into two users.  
A customer and a support worker. Clients can write a ticket, support can respond to it, the client can enter into a dialogue and conduct it indefinitely, respectively, 
support can respond.   
You can get the entire dialog through a special endpoint.


Realized custom JWT authentication system.


The ticket has its own status, support can change this status and close the ticket or freeze it.


## For running project


Firstly you need to install the dependencies
```pip install -r requirements.txt ```

After this use docker to start project  
```docker-compose build  ```  
```docker-compose run  ```

