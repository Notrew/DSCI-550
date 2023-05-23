This document outlines the feature collection process and guides you to the corresponding files and Python source codes.


Final Dataset: Bik.tsv
Final Report:TEAMA++_BIGDATA.pdf


Bik additional features
* Affiliation University, Degree Area, Country (all members)
   * Ziyue Chen (1-91line): Bik_Feature_Related/Ziyue_paper_features.py, chromedriver
   * Wenting Shang (92-119line):Bik_Feature_Related/ web_crawl.py
   * Cheng Shi (120 - 129line): Bik_Feature_Related/getinfo.py
   * Ziquan Cheng (130-194line): Bik_Feature_Related/affiliation.py, Bik_Feature_Related/chromedriver.exe
   * Ying Wang(195-215line): Bik_Feature_Related/get_department_country_university_wy.py, Bik_Feature_Related/chromedriver
* Highest degree obtained (all members)
   * Searched manually on ResearchGate, LinkedIn, Google, etc.
* Other Journal Published In (Cheng Shi)
   * Bik_Feature_Related/doi_output.py (output all journals’ sources into doi.csv file)
   * Bik_Feature_Related/doi.csv (all paper’s doi)
   * Bik_Feature_Related/doi_process.py (get other journals published in)
* Publication Rate & Duration of Career (Wenting Shang)
   * Code: Bik_Feature_Related/publications_info.py
   * Input file: Bik_Feature_Related/bik.csv
   * Output file: Bik_Feature_Related/bik_Pub.csv (for merging landslide features)
* Lab Size (Ziquan Cheng)
   * Code:Bik_Feature_Related/ labSize.py
   * Input file: Bik_Feature_Related/bik_pub_landslide_ranking.csv
   * Output file: Bik_Featur e_Related/bik_pub_landslide_ranking_labsize.csv (for merging GDP features)
* Tika Related (Ying Wang & Cheng Shi)
   * myBikTransform.py (transform csv file to python script dictionary )
      * Input File: all .csv files in TIKA_Related/csv_and_dict_py/rawdata
      * Output File: all .py files in TIKA_Related/csv_and_dict_py/rawdata
   * cosine_similarity.py (Tika source code calculating cos similarity scores)
      * Input File: all .py files in TIKA_Related/csv_and_dict_py/rawdata
      * Output File:Input File: all .csv files in TIKA_Related/similarity_score/cos_similarity
   * mysplit.py(split all rows to files)
      * Input File: TIKA_Related/csv_and_dict_py/rawdata/bik_aff_labsize_otherpub_pub_landslide_ranking_country.csv
      * Output Directory:TIKA_Related/csv_and_dict_py/for_edit_value_and_jaccard/bik_all_features
   * jaccard_similarity.py
      * Input Directory: TIKA_Related/csv_and_dict_py/for_edit_value_and_jaccard/bik_all_features
      * Output File:TIKA_Related/similarity_score/jaccard_similarity/jaccard_all_features.csv
   * edit_value_similarity.py
      * Input Directory:TIKA_Related/csv_and_dict_py/for_edit_value_and_jaccard/bik_all_features
      * Output File:TIKA_Related/similarity_score/edit_value_similarity/edit_v_all_features.csv
   * compare_in_cosine_similarity.py
      * Input File:all .csv files in TIKA_Related/similarity_score/cos_similarity
   * compare_three_similarity_methods.py
      * Input File: TIKA_Related/similarity_score/cos_similarity/cos_all_features.csv
TIKA_Related/similarity_score/edit_value_similarity/edit_v_all_features.csv
TIKA_Related/similarity_score/jaccard_similarity/jaccard_all_features.csv




Three other datasets
* Global Landslide (Ying Wang, Ziquan Cheng, Wenting Shang)
(https://catalog.data.gov/dataset/global-landslide-catalog-export/resource/e9aad2b3-4ac1-443f-a6a8-e2e56a18babc)
   * Features: number of event happened, fatality number, injury number
   * Input file: bik_Pub.csv, Global_Landslide_Catalog_Export.json
   * Clean & merge: ying_merge_landslide.py/(landsilde_analysis.py)
   * Output file: bik_pub_landslide.csv (for merging ranking features and analysis)
   * Analysis: landsilde_analysis.py
* 2013 World University Ranking (Ziyue Chen)
(https://www.kaggle.com/mylesoneill/world-university-rankings?select=timesData.csv)
   * Features: University, World Rank, Teaching, Research
   * Input file: bik_pub_landslide.csv, RawRanking.csv
   * Clean & merge: Ziyue_merge_ranking.py
   * Output file: bik_pub_landslide_ranking.csv (for merging lab size and analysis)
   * Analysis: Ziyue_ranking_analysis.py
* GDP (Zichao Wang)
(https://www.kaggle.com/stieranka/predicting-gdp-world-countries/data)
   * Features: Country, GDP, literacy, pop density
   * Input file: bik_pub_landslide_ranking_labsize.csv, countries_of_the_world_raw.csv
   * Clean & merge & analysis: Zichao_merge_country&Analysis.py
   * Output file: bik_pub_landslide_ranking_labsize_country.csv