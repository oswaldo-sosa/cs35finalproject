Tutorial Source: [Medium Article](https://codeburst.io/building-your-first-chat-application-using-flask-in-7-minutes-f98de4adfa5d)

Welcome to our collaborative online collection of games where users can interact together to make the next move in a game. Below are instructions for how to install and run our game. 

Our team uses Python 3.6 on our backend. If Python 3.x is not your default Python version, you may have to use `pip3` instead of `pip` to install Python packages and `python3` instead of `python` to run the Python programs. We recommend the you check your location and version of Python by using `which pip` and `pip --version commands`.

### Installation

```bash
# Clone the repository
> git clone https://github.com/oswaldo-sosa/cs35finalproject.git
> cd cs35finalproject

# Installation
> which pip
/Users/<your username>/anaconda3/bin/pip
> pip --version
pip 9.0.1 from /Users/<your username>/anaconda3/lib/python3.6/site-packages (python 3.6)
> pip install -r requirements.txt
> python main.py
```
Open [http://localhost:5000](http://localhost:5000) to see the chat app.
...and in a separate shell
```bash 
# Running Snake Game 
> python snake.py
```
or 
```bash
# Running Pacman Game
> python pacman.py
```
For more information on how to play Snake or Pacman, visit the [library](http://www.grantjenks.com/docs/freegames/) our team used. 


