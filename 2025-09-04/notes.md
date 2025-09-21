# Meeting with Ada

Gemini summary of transcript

## Summary of the Alicorn Project Discussion

What Your Advisor is Saying:
- Refine the Core Message: She thinks leading with a narrow comparison of auto-scaling mechanisms might be "too narrow." Instead, you should integrate this comparison into the broader, "higher level illustration of a trade-off in terms of performance versus... efficiency." The goal is not just to replace a figure but to think about how this new data changes the overall positioning and messaging of the paper.

- Don't Reinvent Auto-Scaling: Your messaging needs to be clear: "We aren't inventing auto-scaling." Instead, you are investigating a new mechanism for auto-scaling that offers a different set of trade-offs compared to existing systems like Parcel.

- Create Clear Differentiation: The evaluation must explicitly and visually differentiate Alicorn from Mashup and Parcel. This will likely involve new figures that directly compare their functionalities and performance.

- Add Necessary Detail: You need to address the reviewer's comments about the design and implementation sections being "too brief." This means adding details on:
    * Why you chose a pass-by-reference data movement solution.
    * How your system manages file cleanup and reference tracking.
    * How the different schedulers (orchestrator and batch) interact.

- Finish the Experiments Soon: She affirmed your timeline of getting all experiments and figures done roughly two weeks before the October 2nd deadline (around September 19th). However, she warned that you can't finalize the experiments until you are clear on how the paper's story is changing.


## Summary of the New AI/HPC Application Work

What Your Advisor is Saying:

### How to Frame the Problem

To convince an audience that your research is important, your advisor said you need to prove two different things about the problem of data movement in AI/HPC workflows.

#### Prove the Problem is Fundamental 🧠

This is about showing the problem is an inherent, architectural issue, not just a fluke of one specific experiment.

- What your advisor said: She confirmed that your idea of using Roofline analysis or the concept of "machine balance" is the right way to do this. This approach explains why the data movement happens based on the properties of the application (its arithmetic intensity) and the hardware. She stated this is important because you are "trying to explain that this is a fundamental problem and not something that maybe is just a function of some experiment."

#### Prove the Problem's Scope is Significant 💰

This is about showing that the fundamental problem has a large, meaningful impact in the real world.

- What your advisor said: She was very clear that showing the raw data movement numbers (e.g., 20 GB vs 50 GB) is not enough, as a reviewer might say, "who cares for 20 gigabytes?"

- To establish the scope, you must translate your experimental results (like the bar chart showing a 2x+ increase in data movement) into metrics that people do care about: cost, energy, and time.

- She specifically suggested you frame it in terms of "how much money I spend for these GPUs" or "how much money I'm paying for the energy of data movement." This demonstrates that the problem has a significant practical and financial impact.

- She concluded by saying, "Both are important because they show different things that are equally important." You need the fundamental analysis to explain why it happens and the scope analysis to explain why it matters.

### Bridge the Gap in Your Narrative:

1. Frame the Solution's Goal Explicitly

    Your advisor pointed out that if you just present your policies ("Temporal Batching," "State-Aware Thresholding") after the problem, they seem arbitrary. She said, "I can really solve the problem... by not-running the AI at all".

    To fix this, she wants you to first state a clear, overarching goal for your solution.

    - What she said: Your solution's goal is to "limit the interference effects... in a way that it still lets you get benefit" and to "reduce the cost you pay for the AI, while limiting any impact on loss of benefit".

    - How to apply this: Before you even mention your specific policies, you should have a sentence like: "Our research goal is to develop a strategy that minimizes the data movement costs associated with the AI agent, but only when doing so does not compromise the scientific benefits of its steering."

2. Let the Goal Define the Requirements

    Once you have a clear goal, it becomes obvious how to measure success and what any potential solution needs to do. This creates a logical link between the high-level goal and your specific design.

    - What she said: By framing the goal this way, "it becomes clearer, what is it that... what are the requirements of whatever solution you present" and "that makes it clear how... success measured here".

    - How to apply this: After stating your goal, you can define the requirements. For example: "This goal requires a system that can (1) monitor the cost of AI-simulation interaction and (2) assess the potential benefit of an AI intervention, allowing it to make intelligent decisions about when to pay that cost."

3. Present Your Policies as Mechanisms to Fulfill the Requirements

    Now, your two policies are no longer random ideas; they are the specific tools you will use to meet the requirements you just defined. They are the "how" that follows the "what" and "why."

    - What she said: She referred to your policies as the "different mechanisms that you can use to achieve that that goal".

    - How to apply this: You can now introduce your ideas naturally. For example: "To meet these requirements, we investigate two primary mechanisms: (1) Temporal Batching, which amortizes the AI's cost over multiple simulation steps, and (2) State-Aware Thresholding, which uses feedback from the simulation to avoid paying the cost for redundant AI interventions." 

    By following this narrative structure—Goal → Requirements → Mechanisms—you create a tight, logical connection that makes your solution feel like the inevitable and intelligent answer to the problem you've raised. This is the bridge your advisor wants you to build.

## Overarching Direction and Quals Strategy

Your advisor wants you to prepare a one-slide presentation for both projects to help you crystallize the core message for each. For your quals, which will happen in mid-October, she wants you to:

1. Present Yourself Holistically: Start with a single slide that frames your PhD experience, connecting your work on resource management (Alicorn) and support for emerging workloads (AI/HPC).

2. Focus on Alicorn: Present the revised Alicorn paper, showing you can complete and defend a research project.

3. Show a Strong Future Direction: Use your one-slide summary of the new AI/HPC work to demonstrate that you are "way ahead of the curve" on your next steps. This proactively answers the committee's potential questions about your progress and ensures they see you as a productive, forward-thinking researcher.