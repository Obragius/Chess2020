# Chess2020
This is to store the chess game which i have made in 2020

## Introduction
{
  My learning of programing started with python in 2019. At that time I had no experience and I have decided to create a chess game. I had no intention to follow specific tutorials, and i would only watch tutorials based on a concept or a use of library. It was a project which displayed the baord and the game would be controlled by typing commands in a dialog box which would move the chess pieces. It was a disaster, I had no idea about OOP and all my logic was built on if statements, as well as a broken display board. i have wrote around 4 thousand lines of code and the program would start and crash after 5-6th move. At that time I have gone on holiday and dropped the project. I have made a break for 8 months, and the decided to go back and give programing another attempt. After I've done my basics tic-tac-toe and small scripts, I have gone back to making a new Chess program, now using WxPython, new images, and aquiring more knowledge of programming. This repository contains different folders for different steps that I took making this program and it has been finished for a while, however I did not use git or github before, and I intend to learn it in future, therfore I'm trying to document my progress.
}

## Versions
{
  This folder is the start of the project, it contains the first version of the original program as well as the last. Other branches of use of this programm are in different folders. This folder also contains several image folders, this is because I have started working with the old images, which are all mine except the background which I have collated from images of the internet (At that time I didn't learn much about the importance of copyright), but I have then asked my relatives to create new images for the new look of the game. Some older versions may require old images. 
  For further information about the latest version of the original programm, you can open Chess2020/Versions/FinalChess.py which has comments on what the functions do and as much as I remember what approaches were taken when solving issues.
}

## AI Attempt
{
  This folder was an attmept to create a min-max algorithm to act as an AI player that you could play against. It would recursevily check 3 moves ahead and try to find the best move to make, however this attempt has failed. this was due to the number of operations which were required to check all moves possible for both players, this required much more proccessing power than I could provide and either moves had to be calculated for hours and days, or the AI only could see one move ahaed. I did try to implement alpha-beta pruning, however it didn't work and the project was scrapped for time being, maybe I will return to it in future and make it function within reasonable time. Despite the fail this have helped me to try and play with Threading and runing mulptiple processes. This have also given me ideas of how to lonk separate games into one, which was the start of the development of the next section, the multiplayer option.
}

## Multiplayer
{
  This folder was an attempt to allow to players to play one different devices. This was a great opportunity to learn about ports and using them in python. I had to use some of my findings from the previous folder, as I had to try and make different instances of the game running. One instance was the server which would handle the legal moves and would not progress the move until it was legal, the other one or two instances would be the players which would connect to the port on the server ip and make moves for the indiviual players. The end result is playable and allows to set a server and players which can make moves on the server, cannot cheat unless they are doing so on the server side and if dissconected can reconect. Testing was done on slow and old systems, which would dissconnect frequently, some of those issues were solved, however not all have been solved before the project was no longer in production. It is also important to understand that to play this over the internet, the port which you set needs to be open and forwarded on the router, otherwise it is only possible to play via lan.
}

# Updates
## 21.12.2021
{
  I have put all the files in the appropriate folders, folowing this, in future I will produce comments for the finished versions of the programs and general comments on the versions and the aproach which I took.
  Inroduction and Versions have been started.
}
## 22.12.2021
{
  Added section which talks about the failed AI player attempt.
}
## 31.12.2021
{
  Added section which talks about the multiplayer folder.
}

