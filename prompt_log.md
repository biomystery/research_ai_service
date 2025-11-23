## 1

Read the Kaggle competition page: https://www.kaggle.com/competitions/agents-intensive-capstone-project.

I am an advanced bioinformatician and data scientist specializing in Treg cell therapy, with expertise in full stack development (LIMS, pipelines, CMC data portals), microservices, systems biology, and programming languages including R, Python, Matlab, Shell, and React. I have approximately 2 weeks part-time available for this project.

Considering my background and time constraints, generate at least 3 feasible project ideas for completing this capstone competition. For each idea, provide a clear, concise rationale linking it to my skills and estimated effort required.

Present the ideas and prompt me to select one to proceed with.

After I confirm, create a detailed implementation plan with key milestones covering:

- data preprocessing and integration steps,
- modeling and algorithm selection aligned with the competition objectives,
- evaluation criteria and validation methods.

Pause for my approval before initiating any code generation or automated execution.

## 2

1. please double check if current implementation meets the requirements in the competition page.
2. enable google genmini api as default option
3. particularly i think there is a requrement of using google ADK, please double check if current implementation meets this requirement.

## 3

Can you create current design logic markdown file including mermaid diagram to illustrate? I would like to discuss this with you

## 4

I like current full stack design, but i think we are lacking a significant amount contents, see below:

```
- Multi-agent system, including any combination of:
    - Agent powered by an LLM
    - Parallel agents
    - Sequential agents
    - Loop agents
- Tools, including:
    - MCP
    - custom tools
    - built-in tools, such as Google Search or Code Execution
    - OpenAPI tools
    - Long-running operations (pause/resume agents)
- Sessions & Memory
    - Sessions & state management (e.g. InMemorySessionService)
    - Long term memory (e.g. Memory Bank)
- Context engineering (e.g. context compaction)
- Observability: Logging, Tracing, Metrics
- Agent evaluation
- A2A Protocol
- Agent deployment
```

The above should be all included in the design logic. Can you examine and update a design logic file to include all above contents?

## 5

I like your updated design. Few suggestions:

1. use google-adk (documents can be found here: https://google.github.io/adk-docs/ )
2. use google vertex ai platform (document: https://docs.cloud.google.com/vertex-ai/docs)

Please update the design based on the above 2 tools
