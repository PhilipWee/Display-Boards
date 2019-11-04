# Display-Boards
Design and develop a Dynamic text display on LED panels modified and  controlled from a web page.
## Implementation Architecture
![Image of Architecture](/readme_images/Architecture.jpg)

# Installation instructions

### Database And Server Setup (Preferably both on same system)
1. Install docker according to your system requirements
2. Run the app using ```docker run -it -p 5000:5000 philipandrewweedewang/display-boards:latest```

### RPI Setup
1. Setup the RPI with the OS Raspbian
2. Open Terminal / CMD prompt
3. Change the directory to the desired installation location
4. Clone the repository using ```git clone https://github.com/SirGreat/Display-Boards.git```
5. Enter the directory with ```cd Display-Boards```
6. Enter the RPI code directory with ```cd rpi_api_code```
6. Activate the virtual environment with ```source env/bin/activate```
8. Install memcached using
    * ```sudo apt-get update```
    * ```sudo apt-get install memcached```
9. Run memcached using a new terminal instance and ```memcached```
    * The terminal will seem to hang. It is just running memcached
9. Open ```display_msg_funcs.py``` with any editor (Thonny or nano is fine)
10. Change the ```HOSTURL``` parameter to the address of the server
8. Run the code using ```python3 api.py```


