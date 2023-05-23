import pandas as pd


def main():
    #find the DOI number in bik dataset
    bik_df = pd.read_csv(r'Bikdataset.csv')
    bik_df_doi = bik_df["DOI"]
    DOI = bik_df_doi.to_csv(r'doi.csv',index=False)
    print(DOI)
#web = "https://pubmed.ncbi.nlm.nih.gov/?term="+ DOI + "%5BLocationID%5D&sort="


if __name__ == "__main__":
    main()
