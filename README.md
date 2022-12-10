# py-chael
Python code for downloading The Office from online directory

This code actually works, but do not blindly run the .py file directly. Open it on VS Code or any other code editor and change the paths and filenames to your preference. Also, please run it on terminal so that you can ctrl+C it when further download does not proceed... because it happened to me, my data got exhausted and the code was stuck on downloading S03E16 (I guess)... so yeah, generally, each episode takes 2-3 mins to download at an average 4G network speed, but if it gets stuck somewhere for 7+ mins, then terminate the code, and delete the file on which it got stuck (since, if you might check, it'll be partially downloaded), and rerun the code when internet connection is available again.

Future updates/modifications:
- Feature to input how many episodes user wants to download in a run (to not use up all of the data in your limit)
- Feature to stop the code in case download speed reaches 0 for sometime (which indicates that data limit has reached and/or internet connection has stopped)
