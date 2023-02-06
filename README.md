Elevator-system
Steps to run this app
  1. Git Clone this repo.
  2. then do cd into elevator-system
  3. Create a venv using python3.9 ```python3 -m venv venv```
  4. Activate your venv ```source venv/bin/activate```
  5. Not do pip install -r requirements.txt
  6. Now since you want to setup a db. I have used postgres DB. You can install psql and create a db with the name elevator and update the database section in the settings.py file.
  7. now you can run the server using ```python manage.py runserver``` command
  8 Once the server is up and running you can open the swagger api view and can hit and test the api.
  
<img width="1548" alt="image" src="https://user-images.githubusercontent.com/45592222/216893226-ec2570e4-9a59-4977-93a1-497839b96a0d.png">
