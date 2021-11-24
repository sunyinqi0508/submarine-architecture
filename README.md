# hps-submarine-architecture

Dear Classmates,
    This is the architecture for our last game, submarine. \
    Written by Yinqi Sun and Yue Zhou. \
    The Web UI is adapted from the 
    2018 architecture team https://github.com/jbitton/hps-submarine-architecture  
    If there are any questions, please feel free to sending an email either to ys3540@nyu.edu or yz1268@nyu.edu

There are multiple parts to this project:
* The Web interface display the statics and game progress  
* The server/client code that plays the game

## Setup Client / Server Code

1. The server code requires `Python 3` to run properly.
2. You may then install dependencies: `pip3 install -r requirements.txt` 
3. `cd` into this project on your machine and run `python3 submarine_server.py`

You should see some output that looks similar to this:
```
*** Game Configuration ***:
        d = 36
        y = 6
        r = 6
        m = 10
        L = 4
        p = 2

Starting Trench Server on port 61409
Starting Submarine Server on port 5005


sub {'m': 10, 'L': 4, 'pos': 78}
trench {'d': 36, 'y': 6, 'r': 6, 'm': 10, 'L': 4, 'p': 2}
The trench manager's final cost is: 120. The safety condition was satisfied.
Your final cost is: 120. The safety condition was satisfied.
```

## Including Your Client Code

Under the `[Python|Cpp|Java]Clients` folders you may find the framework code 
for the client in the respective language. 

 - For the python Clients simply run the respective clients. The common methods such as socket communication are included in `client_abstract_class.py`. 
 - For C++ clients, build with `make .`. You may simply add your logics in the [Submarine|Trench]Client.cpp. The helper functions are included in Context.hpp, which deals with socket communication as well as parsing the messages. 
 - For java clients, build with `mvn clean package` and run java -jar target/original-JavaClient-1.0-SNAPSHOT.jar [Submarine|Trench] for one of the two clients.

## Modifying the Initial Game State
Simply pass the parameters to GameServerCore

```
controller = GameServerCore(d=45, y=10, r=50, m=3, L=10, p=3, gui=False)
```

## Running the Web Application

Okay, so you want to see the awesome UI. It's stored under the `submarine-vis` folder. However, you do need to install some packages (it's written in `React.js`):

1. Install `Node.js`: for Macs with homebrew installed, it's as easy as: `brew install node`. Or, you can visit the node website: https://nodejs.org/en/download/
2. Install `yarn`: for Macs with homebrew installed, it's as easy as `brew install yarn`. Or, you can visit the yarn website: https://yarnpkg.com/lang/en/docs/install
3. `cd` into `submarine-vis`
4. Run `yarn install`. This will install all of the needed node dependencies
5. Afterwards, run `yarn start` and the app should open up in a new tab. It's hosted on `localhost:3000`
6. To have the GameServer provide an endpoint pass `True` to the gui optional parameter. ie. `GameServer(gui=True)`. This will provide an endpoint on `localhost:8000`

**TIPS**:
The players will not be allowed to connect until the gui has connected to the GameServer. This means you should change your `run_server.py` to sleep for a longer amount of time prior to connecting to the game server.

You can independently open the gui in a browser by going to the address `localhost:8000`... assuming you're running the react app on your computer. You could also run both of your clients independently and connect to the game server after you connect the GUI.

If you have any questions about how the game would work, please stick with the descriptions on the course website: https://cs.nyu.edu/courses/fall21/CSCI-GA.2965-001/subhunt.html and if you find possible implementation differences in this architecture, please report the bugs to us and we will verify and fix them immediately.
