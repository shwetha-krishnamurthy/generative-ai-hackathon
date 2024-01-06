import nltk 
from sklearn.feature_extraction.text import TfidfVectorizer 

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def keywords(text):
    text = text.lower().replace(".", "") 

    # Tokenize the text into words 
    tokens = nltk.word_tokenize(text)

    # Use part-of-speech tagging to identify the nouns in the text 
    tags = nltk.pos_tag(tokens) 
    nouns = [word for (word, tag) in tags if tag == "NN"] 

# Use term frequency-inverse document frequency (TF-IDF) analysis to rank the nouns 
    vectorizer = TfidfVectorizer() 
    tfidf = vectorizer.fit_transform(nouns) 

# Get the top 3 most important nouns 
    top_nouns = sorted(vectorizer.vocabulary_, key=lambda x: tfidf[0, vectorizer.vocabulary_[x]], reverse=True)[:5] 

# Print the top 5 keywords 
    return " ".join(top_nouns)



def process_dataframe(dataframe):
    
    # We only want the first 100 rows to avoid overloading the MVP
    subset_df = dataframe.head(100)
    if 'problem' in subset_df.columns and 'solution' in subset_df.columns:        
        subset_df['problem'] = subset_df['problem'].str.strip()
        subset_df['solution'] = subset_df['solution'].str.strip()
        
        # Merge the problem and solution and apply the keywords() function on each
        subset_df['merged_text'] = subset_df['problem'] + " " + subset_df['solution']
        subset_df['keywords'] = subset_df['merged_text'].apply(keywords)

        result_dict = {}
        for _ , row in subset_df.iterrows():
        # Use the 'keywords' column value as the key
            result_dict[row['keywords']] = {'problem': row['problem'], 'solution': row['solution']}
        example_key = next(iter(result_dict))
        print(example_key)
        print(result_dict[example_key])
        return result_dict
    else:
        raise ValueError("The dataframe does not have the required 'problem' and 'solution' columns.")
    


#if __name__ == "__main__":
#    dataframe = pd.read_csv("/home/myu14/Documents/genAI-sustAInable/generative-ai-hackathon/AI EarthHack Dataset.csv", encoding='ISO-8859-1')
#    dict_data = process_dataframe(dataframe)

#    keywords("The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage.   	Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application..")
