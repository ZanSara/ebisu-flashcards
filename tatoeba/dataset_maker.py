import pandas as pd


def main():
    #return split_by_language()
    #return pairs_creation()




def pairs_creation():
    print("Loading ENG sentences...")
    eng = pd.read_csv("filtered/eng.csv")
    print(eng.shape)
    print(eng.head())

    print("Loading ITA sentences...")
    ita = pd.read_csv("filtered/ita.csv")
    print(ita.shape)
    print(ita.head())

    print("Loading HUN sentences...")
    hun = pd.read_csv("filtered/hun.csv")
    print(hun.shape)
    print(hun.head())

    create_pairs(eng, ita, "eng", "ita")
    create_pairs(ita, eng, "ita", "eng")
    create_pairs(eng, hun, "eng", "hun")
    create_pairs(hun, eng, "hun", "eng")



def create_pairs(sources: pd.DataFrame, translations: pd.DataFrame, source_name: str, translation_name: str):
    print(f"Creating translation matches: {source_name.upper()} -> {translation_name.upper()}...")
    sources = sources.drop('source', axis=1)
    sources.columns = ['id', 'original']
    translations = translations.drop('tatoeba_id', axis=1)
    translations.columns = ['id', 'translation']
    pairs = pd.merge(sources, translations)
    print(pairs.shape)
    print(pairs.head())
    pairs.to_csv(f"pairs/{source_name.lower()}->{translation_name.lower()}.csv")



def split_by_language():
    print("Loading sentences...")
    sentences = pd.read_csv("sentences.csv", sep="\t")
    sentences.columns = ['id', 'lang', 'sentence']
    print(sentences.shape)
    print(sentences.head())

    print("Loading bases...")
    pairs = pd.read_csv("sentences_base.csv", sep="\t")
    pairs.columns = ["id", "root"]
    print(pairs.shape)
    print(pairs.head())

    print("Merging datasets...")
    sentences = pd.merge(pairs, sentences)
    sentences.columns = ['id', 'source', 'lang', 'sentence']
    print(sentences.shape)
    print(sentences.head())

    print("Listing languages...")
    languages = sentences['lang'].unique()
    print(languages.shape)
    print(languages[:5], "...")

    print("Filtering by language...")
    for idl, lang in enumerate(languages):
        print(f" - Filtering #{idl}: {lang}")
        filtered = sentences[sentences['lang'] == lang]
        filtered.columns = ['tatoeba_id', 'source', 'lang', 'sentence']
        filtered = filtered.drop(['lang'], axis=1)
        print(filtered.head())
        filtered.to_csv(f"filtered/{lang}.csv", index=False)
        #if idl > 3:
        #    return



if __name__=="__main__":
    main()