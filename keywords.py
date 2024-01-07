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

    # If there are no nouns, then report the first 5 words
    try:
        tfidf = vectorizer.fit_transform(nouns) 
        top_nouns = sorted(vectorizer.vocabulary_, key=lambda x: tfidf[0, vectorizer.vocabulary_[x]], reverse=True)[:5] 
    except:
        top_nouns = text.split()[:5]

    return " ".join(top_nouns).capitalize()

def process_dataframe(dataframe):
    # TODO We select first 200 rows to avoid overloading the MVP, in the future we might ask user which rows to select
    subset_df = dataframe.head(200)
    if 'problem' in subset_df.columns and 'solution' in subset_df.columns:        
        subset_df['problem'] = subset_df['problem'].str.strip() 
        subset_df['solution'] = subset_df['solution'].str.strip()
        
        # Merge the problem and solution and apply the keywords() function on each
        subset_df['merged_text'] = subset_df['problem'].astype(str) + " " + subset_df['solution'].astype(str)
        subset_df['keywords'] = subset_df['merged_text'].apply(keywords)
        subset_df['count'] = subset_df.groupby('keywords').cumcount()
        subset_df['keywords'] = subset_df.apply(lambda x: x['keywords'] if x['count'] == 0 else f"{x['keywords']}({x['count']})", axis=1)
        subset_df.drop('count', axis=1, inplace=True)

        result_dict = {}
        for _ , row in subset_df.iterrows():
        # Use the 'keywords' column value as the key
            result_dict[row['keywords']] = {
                'problem': row['problem'], 
                'solution': row['solution'], 
                'eval_problem': [], 
                'eval_solution': [], 
                'eval_summary': []}
        return result_dict
    else:
        raise ValueError("The dataframe does not have the required 'problem' and 'solution' columns.")
