This is the script to my oral presentation of this project, which will take the place of a proper README until I find the time to write one. The application will be deployed as soon as possible.

------------

My final project is an application called Lion, and it is an interface for performing Leontief
input / output analysis of the United States accounts.

The program is backed by a robust test suite that tests against the Bureau of Economic Analysis' own derivations.

I came up with this idea in order to accomplish several goals I had going into the two-week project period.

Probably my favorite thing about software development is how often you get to the chance to conquer new plateaus, and this time around I wanted to push myself harder than ever before. I’m happy with my decision to pursue Lion, because it required me to teach myself an almost entirely extracurricular software stack, plus enough macroeconomics and linear algebra to write a program that could do the heavy lifting for the user.

I also wanted to solve a real-world problem. I love writing software, but its only half the fun. Bringing those skills to bear on something worth while is truly rewarding.

Breaking into test-driven development was probably my biggest goal, and likewise it's my biggest point of pride. I adhered to the principles of TDD throughout development, even when I was scared I wouldn't finish my project. The lessons I took from this are invaluable, and I'm happy to say I'll be testing before I write my code whenever I can from now on.

So what is the Leontief I/O model?

In any economy, industries buy output from other industries for use during production. This can have unexpected consequences.

Say fabricated metals become more expensive. Every industry that requires metal for production is impacted. But these industries' products are
required by other industries, so those industries will experience the shock as well, as will additional dependencies down the chain, back up the chain, on and on until the change in price has to some degree been passed on to every last good and service in the institution.

To demonstrate this concept, we'll use my application to levy a 20% severance tax on the extraction of oil and gas, using data for 2015 at the summary level.

Examine the results and you may be surprised. Remember, the differences you'll see will have filtered through the entire production structure of the United States.

Even if you're analyzing the output of a sector that doesn't exhaust much of the commodity you tax, if it relies on the output of some other sector that does, it’s going to respond.

That goes for secondary, tertiary, and higher-order inputs to production: the inputs to the inputs to the inputs and so on. This is what makes Leontief estimates so useful.

Let's take a look. So this makes sense. Here we see an intense %12 rise in the price of petroleum and coal products. It doesn't take knowledge of economics to grasp that the production of these commodities should depend heavily on the pricing of oil and gas.

But what do we have over here? Air and water transportation have gone up considerably as well. Cool, so we can see the second-order of effects, too. We can fathom that air and water transportation have been significantly impacted, because petroleum has been significantly impacted.

Same thing here with Securities, commodity contracts, and investments, which experienced a 5.93 percent rise in price, attributable perhaps to markups of crude energy futures.

So here's where things get interesting. Observe that every bar has climbed at least a little bit. The severance tax I imposed on oil and gas extracts impacted the entire economy. By one amount or another, everything has changed, and that gives you an idea of the power of the Leontief method.

Lion uses this method but anyone can use Lion. It's a tool that lets you examine how rises in price can be felt in corners of the economy far removed from the sectors that are the subject of your study.

The design of Lion can be described as a single-page (SPA) model-view-controller (MVC) architecture.

You have relational database PostgreSQl maintaining a copy of the input / output accounts of the BEA for speed and availability.

A Python Django web server runs an application that initializes a connection to the data and exposes a REST API for its retrieval.

The API is consumed by a React-Router React.js client which integrates data-driven DOM library D3.js for rich visualization.

This interface supports arguments to the economic model by attaching user input as query parameters that get dispatched along with the URL for a desired resource — in our case, data for a particular economy, at a certain level of detail, relative to the arguments provided.

My application queries the necessary matrices and vectors for balancing the economy and applies the user-provided tax matrix. The total requirements equations are derived from the new data and used to solve for relative price.

A JSON payload containing the result for each commodity is delivered back to the client, which delegates rendering of the data to D3.
