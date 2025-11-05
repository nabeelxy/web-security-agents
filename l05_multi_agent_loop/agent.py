from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent
from google.adk.tools import google_search

# define basic domain agent
basic_domain_agent = LlmAgent(
    name = "basic_domain_agent",
    model="gemini-2.0-flash",
    instruction= """
        You are an agent that searches a given domain name using the
        google_search tool and find top entries and summerize them.
        """,
    output_key= "basic_domain_output",
    tools=[google_search]
)


advanced_domain_agent = LlmAgent(
    name = "advanced_domain_agent",
    model="gemini-2.0-flash",
    instruction= """ Your are an advanced domain analysis agent that
    takes the initial search results and performs a comprehensive analysis
    and annotate the findings with additional resources and/or verify
    the findings.

    **Input**:
    {basic_domain_output}

    """, 
    output_key= "advanced_domain_output",
    tools=[google_search]

)

report_agent = LlmAgent(
    name = "report_agent",  
    model="gemini-2.0-flash",
    instruction= """ You are an agent responsible for generating a comprehensive
    report based on domain intelligence gathered from previous analysis stages.
    
    **Input**:
    {advanced_domain_output}

    """

)

# define sequential agent that uses basic and advanced domain agents
loop_agent = LoopAgent(
    name = "loop_agent",
    description = "An iterative agent that performs multiple rounds of domain analysis to gather comprehensive intelligence.",
    sub_agents = [basic_domain_agent, advanced_domain_agent],
    max_iterations = 2
)


root_agent = SequentialAgent(
    name = "sequential_agent",
    description = "A sequential agent that performs iterative domain analysis and then generates a comprehensive report.",
    sub_agents = [loop_agent, report_agent]
)