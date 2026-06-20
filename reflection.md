# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  : The first time I ran it, I thought everything was going smoothly. I started at 5 
  and it said that the correct number was higher than that. I inputted 50, 70, 90, 99, 100,
  and it was still saying "higher", even though the max was 100. I reached the max attempts,
  and it said that "16" was the correct number. Which, if we were following the game, is not true.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  1. The hints were backwards
  2. Score penalty is constant across all difficulties [Default: 15]
  5. Number of attempts is not consistent to the "actual" number of attempts

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input                       | Expected Behavior             | Actual Behavior                | Console Output / Error        |
|-----------------------------|-------------------------------|--------------------------------|-------------------------------|
|New game button              |Resets & create new game       | Nothing happened               |  n/a                          |
|Range of number in difficulty|Higher difficulty = more range | Higher difficulty = less range | n/a                           |
|Submit Guess when nothing in input|Doesn't count as attempt|Counts as an attempt | ["","","",""] |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
 Claude AI
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
 One example was the bug error of the Difficulty range not being
 consistent that Claude handled that was in my intention
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  One example was that Claude suggested that we should move the test_game_logic.py into another,
  new folder instead of the dedicated folder tests/. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I check the game logic, run pytest, & run the Streamlit game to verify if the bug is still there. 
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  One test that I ran using pytest is that it showed me that the attempts sure enough were working 
  as intended, when last time it was always an attempt short than promised.
- Did AI help you design or understand any tests? How?
  Claude helped me understand the tests between the logic of points. The point system works by giving 
  the player a penalty of 5 points for guessing wrong. Sometimes, in the earlier version of the 
  code, whenever the player guessed higher than the number, it rewarded them points instead of deducting
  them. 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  I would respond by explaining that Streamlit reruns your whole script every time the user does
  anything, like pressing a button, dragging a slider, type in a box: normal variables get reset 
  back to their original value. A session state is like automatically saving in modern video games,
  except that it saves every change, using the updated, modified values instead of going back to
  local variables. 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  One habit I would reuse is probably use a new chatbox for each problem, error, bug I've identified
- What is one thing you would do differently next time you work with AI on a coding task?
  One thing I would do differently is planning more with Claude, and have a log file every time
  Claude modified anything in the code, so that I would be able to keep track
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  Claude was very fast and straightforward in generating code. It fixed most of the bugs that I've found,
  & it also found that I did not expect, and fixed them as well. But in some cases, 
  Claude left some error at some point in the game logic,
  in which I had to troubleshoot with it, and remove the errors.
  This changed how I think that programmers could rely on AI to generate code, but
  they would have to figure out the mistakes after. Which is why we have to understand
  that AI is no more than just a tool. We can't rely on it to generate clean, perfect code.
  