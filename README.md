# Monopoly_MMO

Monopoly_MMO is an online multiplayer Monopoly game implemented in Python using the Pygame module. The game is inspired by the concept introduced by the YouTuber Yoonns "https://www.youtube.com/@YoonnsLoL".

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Online Multiplayer:** Play Monopoly with friends in real-time over the internet.
- **Inspiration:** The game draws inspiration from the concept introduced by Yoonns on YouTube.
- **Pygame:** Built using the Pygame module for Python, providing a user-friendly interface.

## Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/Houdeifa/Monopoly_MMO.git
cd Monopoly_MMO
```

2.  **Install Dependencies:**
Ensure you have Python and the requirements installed. You can install the requirements using:<br />
```bash
pip install requirements.txt
```
3. **Create a bot/application**
In order to use the Discord mode you need to have a bot installed on your channel, to create that bot you need to go to the **delelopers portal of discord : https://discord.com/developers/applications**<br />
- Then create new Application :<br />
![Creating App](readme_images/1.png?raw=true "Title")<br />
- Give it a name then hit create :<br />
![Givin the App a name](readme_images/2.png?raw=true "Title")<br />
- Go to bot settings :<br />
![Givin the App a name](readme_images/3.png?raw=true "Title")<br />
- Reset the token and copy it (the token will be shown only one time so you need to save it) :<br />
![Givin the App a name](readme_images/4.png?raw=true "Title")<br />
![Givin the App a name](readme_images/5.png?raw=true "Title")<br />

4. **Add the token file**
- On the clonned folder (at same folder of main.py) create a folder named **"auth"** and inside it create a the file **"tokens.txt"** and paste your token : <br />
![Givin the App a name](readme_images/6.png?raw=true "Title")<br />

5. **Add the bot to the server**
- On the developpers portal go to OAuth2 -> URL Generator :<br />
![Givin the App a name](readme_images/7.png?raw=true "Title")<br />
- On the scope area check the **bot** and the **applications.commands** checkboxes :<br />
![Givin the App a name](readme_images/7_1.png?raw=true "Title")<br />
- On the Bot permissions area check **Send Messages** , **Read Messages/View Channels** and **Use Slash Commands** checkboxes :<br />
![Givin the App a name](readme_images/8.png?raw=true "Title")<br />
- You will get a link as shown on the following image , copy it :<br />
![Givin the App a name](readme_images/9.png?raw=true "Title")<br />
- And past it on the url input on your favorite web navigator , then choose your server and hit continue :<br />
![Givin the App a name](readme_images/10.png?raw=true "Title")<br />

5. **Choose the Channel**
- Now go to server **settings -> integrations**, on the **Bots and Apps** you will find all your bots, choose the one we added and click on **Manage** :<br />
![Givin the App a name](readme_images/11.png?raw=true "Title")<br />
- On the **Channels** section add the channel where you want players to contol the game by cliking on **Add Channel** , you can also disable the other Channels to make sure that the bot uses only the selected channel : <br />
![Givin the App a name](readme_images/12.png?raw=true "Title")<br />
- Now you can enjoy the game by writting the commands on the discord channel : <br />
![Givin the App a name](readme_images/13.png?raw=true "Title")<br />

## Usage
```bash
python main.py
```
Discord Commands :
- /hello : a command to test the bot, the bot should replay by "Hello <username> !"
- /spawn : Spawn the player with the name same as the discord username
- /move : move the player
- /buy : Buy the current Square
- /buy+1 : Buy the next Square
- /buy-1 : Buy the previous Square

Note : all commands entred by users will be executed (by order), you should configure a slow mode in the channel to make sure you won have a very big queue of commands<br/>
Note : on the game window the you an disable the discord commands by clicking on the "Manual Command" button<br/>

## Contributing
Contributions are welcome! Follow these steps to contribute:

- Fork the repository.
- Create a new branch: 
```bash
git checkout -b feature-branch
```
- Make your changes and commit: 
```bash
git commit -m 'Add new feature'
```
- Push to the branch: 
```bash
git push origin feature-branch
```
- Create a pull request.

## License
This project is licensed under the GPL License.
