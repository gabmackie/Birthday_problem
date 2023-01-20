# Birthday_problem

The birthday problem asks that, given *n* people, what is the probability that two of them will share a birthday. The birthday paradox is the counter-intuative fact that only 23 total people are needed for that probability to be over 50%.

It is relatively simple to calculate the odds that two or more people will share a birthday, because you can calculate the odds that no one shares a birthday and then subtract that from 1. It is also easy to generalise that to any number of days. It gets harder to calculate the odds that *exactly* two people will share a birthday. Or that three or more people share a birthday, or four or more etc.

A solution to this is to use a simulation. This is where you generate *n* number of people, and check whether or not *x* number of them share a birthday. You do this, say, 10,000 times and it ends up extremely close to the true probability that *x* number of people share a birthday.
  
<br>

This code can do three things:
- Calculate the exact probability that given *n* people and *y* days, what is the probability that two or more of them will share the same day.
- Use a Monte Carlo simulation to approximate whether, given *n* people and *y* days, what is the probability that *x* or more people share the same day.
- Use a Monte Carlo simulation to approximate whether, given *n* people and *y* days, what is the probability that **exactly** *x* of them share the same day.

It can also draw a pretty graph that shows the mean probability as the simulation is run. This shows how it eventually converges on the true answer.
  
<br>

More information can be found at:
- https://en.wikipedia.org/wiki/Birthday_problem
- https://www.youtube.com/watch?v=a2ey9a70yY0
- https://www.youtube.com/watch?v=ofTb57aZHZs
