import streamlit as st

# NOTE: run using `streamlit run screen_results.py`

###############################################################################
# Helper Functions
###############################################################################

def update_responses(data, unique_query_name):
    return data 
    # TODO: this needs to be written (find the history row in data, see if it has gen AI answers yet, and if it does not, then create them)

def update_screen(screen, results):
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            .main-container {
                display: flex;
                flex-direction: column;
                align-items: stretch;
                width: 100%;
            }

            .box {
                flex: 1;
                background-color: #f1f2f6;
                padding: 10px;
                margin-right: 10px;
            }

            .container {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
            }
        </style>
        <title>Gray Boxes</title>
    </head>
    <body>
        <div class="main-container">
            <div class="container">
                <div class="box">
                    <p><b>Problem:</b> """ + results["problem"] + """</p>
                    <p><b>Solution:</b> """ + results["solution"] + """</p>
                </div>
            </div>
            <div class="container">
                <div class="box">
                    <h4>Problem Evaluation</h4>
                    <p>Text...</p>
                    <p>More Information [[TODO: make button]]</p>
                </div>
                <div class="box">
                    <h4>Solution Evaluation</h4>
                    <p>Text...</p>
                    <p>More Information [[TODO: make button]]</p>
                </div>
                <div class="box">
                    <h4>Summary</h4>
                    <p>Text...</p>
                    <p>More Information [[TODO: make button]]</p>
                </div>
            </div>
            <div class="container">
                <div class="box">
                    <center>
                        <p>Chat [[TODO: make button]]</p>
                    </center>
                </div>
                <div class="box">
                    <center>
                        <p>Decision [[TODO: make button]]</p>
                    </center>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    screen.markdown(html_code, unsafe_allow_html=True)
    # TODO: still need to get the more information/chat/decision buttons working

###############################################################################
# Print Screen with Results
###############################################################################

def show_results_screen(data):
    # Title and Layout
    st.set_page_config(layout = "wide")
    unique_query_name = st.sidebar.radio("Queries", data.keys()) # TODO: consider capping queries at 100
    main_content = st

    # Main Screen
    main_content.title("sustAInable VC Evaluator")
    update_responses(data, unique_query_name)
    update_screen(main_content, data[unique_query_name])

    # Disclaimer (TODO: should customize disclaimer)
    main_content.markdown("*Disclaimer: Generative AI can make mistakes. Consider checking important information.*")

###############################################################################
# Example Instance
###############################################################################

if __name__ == "__main__":
    data = {"Modular Construction": {"problem": "The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage.   ", "solution": "Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application."},
            "Death to Windmills!": {"problem": "I'm sure you, like me, are feeling the heat - literally! With World Health Organization declaring climate change as the greatest threat to global health in the 21st century, we're in a race against time to move away from fossil fuels to more efficient, less polluting electrical power. But as we take bold leaps into a green future with electric cars and heating, we're confronted with a new puzzle - generating enough electrical power without using fossil fuels!  ", "solution": "Imagine standing on a green hill, not a single towering, noisy windmill in sight, and yet, you're surrounded by wind power generation! Using existing, yet under-utilized technology, I propose a revolutionary approach to harness wind energy on a commercial scale, without those monstrously large and environmentally damaging windmills. With my idea, we could start construction tomorrow and give our electrical grid the jolt it needs, creating a future where clean, quiet and efficient energy isn't a dream, but a reality we live in. This is not about every home being a power station, but about businesses driving a green revolution from the ground up!"},
            "Book Swap": {"problem": "The massive shift in student learning towards digital platforms has resulted in an increased carbon footprint due to energy consumption from data centers and e-waste from obsolete devices. Simultaneously, physical books are often produced, used once, and then discarded, leading to waste and deforestation.  ", "solution": "Implement a Book Swap program within educational institutions and local communities. This platform allows students to trade books they no longer need with others who require them, reducing the need for new book production and hence, lowering the rate of resource depletion. Furthermore, the platform could have a digital component to track book exchanges, giving users credits for each trade, which they can accrue and redeem. This system encourages and amplifies the benefits of reusing and sharing resources, thus contributing to the circular economy.   By integrating gamification, getting students and parents involved and providing an easy-to-use platform, the program could influence a cultural shift towards greater resource value appreciation and waste reduction. In terms of the financial aspect, less reliance on purchasing new books could save money for students, parents and schools."},
            "Good Will": {"problem": "The fashion industry is one of the top contributors to global pollution. The mass production, distribution and disposal of clothing is not sustainable long-term, leading to the release of greenhouse gases from manufacturing, shipping and wasted clothing in landfills.   ", "solution": "The proposed solution is a garment rental service. Such a service should work closely with major clothing brands. When buying items, customers should have the option to buy or rent. This model would be like a subscription service where customers can select a set number of items each month, wear them, then return them for other items. Clothing would be professionally cleaned between customers and repaired as necessary to maximize its life cycle. When a garment is no longer suitable for rental, it can be recycled into new clothes. This solution reduces the number of garments produced, the amount of transportation needed, and the quantity of clothes going to landfills. Completely damaged or unusable textiles can be reused or recycled into new products. It also gives financial value to businesses as it transforms fashion from a single-purchase model into a subscription service, creating a continuous income stream. Its feasibility and scalability depend on factors such as location, culture, and income level. However, as digital platforms become more common for commerce, this concept could be globally implemented."},
            "Modular Electronic Device M": {"problem": "The majority of the materials used in producing electronic goods are not being utilized optimally. Numerous electronic devices are replaced before their lifespan ends, often due to minor malfunctioning or outdated components, resulting in significant production of electronic waste and underutilization of natural resources.  ", "solution": "An innovative concept would be a modular electronic device model where users are able to upgrade or swap components, rather than replacing the entire device, thus promoting a circular economy. This goes beyond just restoration but rather the idea of creating an electronic gadget that thrives on reuse and modifications, maximising the life and value of each part.   Manufacturers need to design gadgets with modules for core components, allowing for easy upgrades or replacements. For instance, a smartphone could have individually upgradeable components: camera, battery, CPU, etc. When a module fails or becomes outdated, only that module needs to be replaced.  This idea promotes resource use efficiency and significantly cuts waste, under the 'reduce, reuse, repair' mantra. The replaced modules should be sent back to manufacturers for refurbishment or extraction of critical raw materials.   For businesses it opens a new market space, enabled by sale of modules and recycled components, providing long term value capture. It also increases customer loyalty as they continually engage with the manufacturers in the lifecycle of their device. The model is scalable as it allows for the continuous incorporation of technological advancements within the same core device.   This modular approach is not only novel but it clearly addresses the broader picture of how electronic devices should be designed for a circular economy, considering environmental protection, resource efficiency, economic viability, and customer value."}}
    show_results_screen(data)

