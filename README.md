# Perfect Circle Game
A Python-based representation of the game "Draw a Perfect Circle" by neal.fun. It is a game in which your skills of drawing a circle are tested. 

## Installation

1. Make sure you have installed python
2. Download the sourcecode files or clone the repository
3. Install pygame by the following command:
  
```bash
  pip install pygame
```
4. Upload the mp3 files in the same directory as the code files


## Usage

Run your code:
```bash
  python main.py
```
Or if it does not work, use:
```bash
  python3 main.py
```
When the game is opened, you will see a black screen with a red dot. This dot is the center of your circle. Using your mouse draw a circle around this dot and the game will provide feedback on the accuracy and completeness of your circle.

- If the drawn circle is not complete, an "INCOMPLETE CIRCLE" error message will be displayed.
- If you took too much time drawing, a "TOO SLOW" error message will be displayed.
- If you are drawing too close to the center, "TOO CLOSE TO DOT!" error will be displayed
- The percentage of perfectness will be shown as you draw and the color of your circle will be changing from green (100%) to more red according to its perfectness. Aim for 100% perfectness

Press the left mouse button to start drawing, and release it to stop. The game will update the feedback messages accordingly. You can reset the game at any time by closing and reopening the game window.


Enjoy the game and have fun drawing perfect circles!
