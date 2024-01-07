import os
import utils
from openai import OpenAI
from tavily import TavilyClient


def create_summarization_assistant():
    # Initialize clients with API keys
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    circular_economy_varied_examples = """ 
               Example 1:
               Problem:
               Many companies face challenges in effectively managing resources, leading to increased environmental impact and higher production expenses. This inefficiency results in waste, excessive energy consumption, and a negative environmental footprint.
               
               Solution:
               Industrial symbiosis, exemplified by the "Sustainable Synergies" project in Aalborg, enables companies to lower production costs, minimize environmental impact, and foster innovation by exchanging surplus materials, water, energy, and resources. This approach enhances resource and energy efficiency, reduces waste management expenses, and generates new economic opportunities. Additionally, it significantly contributes to environmental sustainability by cutting energy consumption, materials usage, and CO2 emissions, benefiting both businesses and the environment.
               
               Example 2: 
               Problem:
               Traditional waste disposal methods for drink cans and bottles lead to environmental issues and resource depletion. Low recycling rates contribute to excessive energy consumption and the extraction of virgin materials like bauxite.
               
               Solution:
               The Danish deposit and return system for recycling drink cans and bottles, led by Dansk Retursystem, achieved a remarkable 93% return rate in 2021, recycling 1.9 billion containers. This circular system promotes energy efficiency by using 95% less energy to produce cans from recycled materials and reduces the need for extracting bauxite. Effective cooperation among producers, consumers, and the Danish Return System ensures a high return rate, serving as an inspiring model to boost recycling rates and support the circular economy, in line with the EU's 90% collection goal for plastic bottles by 2029.
               
               Example 3:
               Problem:
               Worn-out artificial turf poses an environmental challenge, with disposal through incineration leading to significant CO2 emissions and waste accumulation, contributing to environmental pollution.
               
               Solution:
               Re-Match offers a pioneering solution by utilizing patented technology to efficiently separate worn-out artificial turf into clean, reusable components such as rubber granules, sand, and plastic fibers. This process reduces CO2 emissions dramatically, saving 400 tonnes of CO2 per pitch compared to incineration, while also minimizing waste, equivalent to 1.4 million plastic bags or 250 tonnes of waste. Re-Match's sustainable approach emits less than 20 tonnes of CO2 per pitch during the separation process, effectively addressing the environmental concerns associated with artificial turf disposal.
               
               Example 4:
               The recycling of lithium-ion batteries, crucial in the electrification of transportation and the shift towards sustainable energy solutions, has been challenging, resulting in the export, landfill disposal, and burning of these valuable resources in the USA.
               
               Solution:
               Li-Cycle addresses the problem by aiming to recover critical materials from lithium-ion batteries and reintroduce them sustainably into the supply chain. Their innovative approach seeks to establish a closed-loop, circular economy for battery materials, ensuring that secondary materials from used batteries can be economically and sustainably reused and reformed into new batteries. This initiative not only reduces environmental impact but also promotes the responsible and efficient management of lithium-ion batteries, contributing to a more sustainable future.
               
               Example 5:
               Problem:
               Brands often struggle to implement effective product take-back programs in the context of a circular economy. This results in wasted resources, missed revenue opportunities, and difficulties in tracking and measuring the environmental impact of their efforts.
               
               Solution:
               numi.circular's numi.platform offers a solution by providing circular economy software that facilitates product take-back programs for brands. Customers can return used products to earn recovery points, and the platform automates the sorting and distribution of these products. Additionally, it tracks all takebacks and generates impact reports, allowing brands to measure their environmental initiatives. By offering pre-owned inventory for resale and incentivizing customers with discounts, numi.circular helps companies adopt more sustainable practices, close product lifecycles, reduce waste, and create new revenue streams, ultimately contributing to a more circular and eco-conscious business model.
               
               Example 6:
               Problem:
               Agricultural biomass waste poses environmental challenges, as it often goes unused and contributes to pollution and greenhouse gas emissions. Additionally, there is a need for sustainable materials in industries like agriculture, construction, and carbon offsetting.
               
               Solution:
               Zimbanjex addresses these issues by converting agricultural biomass waste into biochar through a pyrolysis process. This biochar serves multiple purposes, including organic soil regeneration, long-term carbon storage, and applications in industries like cement production and road construction. Furthermore, the startup offers carbon removal certificates, allowing companies to offset their emissions while supporting sustainable practices. Zimbanjex's innovative approach not only minimizes biomass waste but also provides eco-friendly solutions for various industries, promoting a circular and environmentally conscious economy.
               
               Example 7:
               Problem:
               The conventional transportation of bikes often involves single-use cardboard packaging, which generates a significant amount of waste and has limited durability. This unsustainable practice contributes to environmental pollution and resource depletion.
               
               Solution:
               Circular logistics, a German startup, addresses this problem by offering the BikeBox, a sustainable bike transport packaging made from durable polypropylene. This foldable box not only reduces to 1/8th of its size for easy storage but also promotes continuous reuse, eliminating the need for single-use cardboard packaging. Polypropylene's durability allows for multiple reuses, and it is 100% recyclable at the end of its lifecycle. The BikeBox is designed for easy assembly, similar to traditional cardboard boxes. Additionally, circular logistics handles the return of these boxes, creating a waste-minimizing, closed-loop system that aligns with circular economy principles and promotes sustainability in bike transportation.
               
               Example 8:
               Problem:
               The hotel industry often faces challenges related to disposing of old mattresses, leading to waste generation and environmental concerns. Conventional mattress disposal methods contribute to landfills and resource depletion.
               
               Solution:
               Austrian startup MATR offers a solution by providing "Mattress-as-a-Service" to hotels, allowing them to reduce their environmental impact. MATR collects mattresses at the end of their lifespan, disassembles them, and recycles most of the components, reintroducing them into the material loop. This approach ensures that MATR mattresses are not wasted but continuously returned to the material cycle, reducing waste and minimizing the CO2 footprint compared to conventional mattress disposal methods. MATR's innovative service aligns with circular economy principles and promotes sustainability in the hotel industry.
            """
    
    assistant_prompt_instruction = f"""You are an unbiased expert on Circular Economy,
    helping a VC analyst sift through ideas with a discerning eye. Adopt a skeptical mindset
    when giving your overall feedback.

    The problem and solution pairs have been evaluated and you have been given those question answer pairs.
    Based on these evaluations, please generate an overall recommendation of how this idea
    compares relative to varied circular economy ideas in your knowledge. 
    These are a variety of great circular economy ideas: {circular_economy_varied_examples}
    """

    # Create an assistant
    assistant = client.beta.assistants.create(
        instructions=assistant_prompt_instruction,
        model="gpt-4-1106-preview",
    )

    return assistant, client, tavily_client

def get_summarization(problem_sol_prompt_answer_dict_list):
    assistant, client, tavily_client = create_summarization_assistant()

    prompt_list = [f"Question: {d[0]}; Answer: {d[1]}" for d in problem_sol_prompt_answer_dict_list]

    prompt_answer_dict_list = utils.get_eval_answers(prompt_list, assistant, client, tavily_client)

    return prompt_answer_dict_list
