# Average Candidate

*The average face and description of every candidate for different parties.*

A little tool I put together to crawl different WA party websites to generate the average, candidate in order to create the ultimate candidates that can save the world.

Usage:

First, install OpenCV from source, as it is required for Facemorpher. (stasm requires library files, so the precompiled version available on pip will not work).

After that, cd in `src`, and run `python3 -m pip install --upgrade pip && pip install -r requirements.txt`. Once this is done, you should be able to run `python main.py` and select which one you would like to do.

## To Do:

- Better split up the components so that only parts of the generation can be done
- Investigate the best way to handle templates. I have made templates for each party, but as they were made by modifying websites from each party I do not know if I can legally publish them.
- General code clean up and improvement of messages.
- Investigate using GPT to generate more legible text.
