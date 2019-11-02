# Display-Boards
Design and develop a Dynamic text display on LED panels modified and  controlled from a web page.
## Implementation Architecture
![Image of Architecture](/readme_images/Architecture.jpg)

# Installation instructions

### Database Setup
1. Install PostgreSQL 11 and pgAdmin4 (OS does not really matter, use linux distro if scalability with containers is the intention)
2. Ensure during the installation you keep track of the following information:
    * IP Address / Domain of database server
    * Username
    * Password
3. Using pgAdmin4, create a database called ```display_msg_details```

### Server Setup
1. Install Python3 
    * Preferably 64 bit for future scalability to do data processing, but 32 bit is fine
    * Make sure python is added to PATH on installation
2. Open Terminal / CMD prompt
3. Change the directory to the desired installation location
4. Clone the repository using ```git clone https://github.com/SirGreat/Display-Boards.git```
5. Enter the directory with ```cd Display-Boards```
6. Enter the server code directory with ```cd server_code_v2```
7. Install the python dependencies using ```pip install -r requirements.txt```
8. Configure the ```config.py``` file with the settings identified during the database setup
8. Run the code using ```flask run -h 0.0.0.0```
9. Configure port forwarding and open ports as required (For testing only port 5000 needs to be opened)
10. Record down the IP address of the server for the RPI setup

### RPI Setup
1. Setup the RPI with the OS Raspbian
2. Open Terminal / CMD prompt
3. Change the directory to the desired installation location
4. Clone the repository using ```git clone https://github.com/SirGreat/Display-Boards.git```
5. Enter the directory with ```cd Display-Boards```
6. Enter the RPI code directory with ```cd rpi_api_code```
7. Install the python dependencies using ```pip install -r requirements.txt```
8. Install memcached using
    * ```sudo apt-get update```
    * ```sudo apt-get install memcached```
9. Open ```display_msg_funcs.py``` with any editor (Thonny or nano is fine)
10. Change the ```HOSTURL``` parameter to the address of the server
8. Run the code using ```python3 api.py```


