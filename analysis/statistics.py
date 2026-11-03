import numpy as np
from utils.data_loader import load_data
from scipy import stats  # type: ignore[reportMissingImports]

# Obliczenie średniej ocen G3
def avgG3(df):
    grades = df["G3"]
    return sum(grades) / len(grades)
    
# Sprawdzenie układu normalnego dla G3
def shapiroG3(df):
    grades = df["G3"]
    return stats.shapiro(grades)

# Sprawdzenie układu normalnego dla Ilości godzin nauki
def shapirostudytime(df):
    studytime = df["studytime"]
    return stats.shapiro(studytime)


def correlation(df):
    pvalueST = shapirostudytime(df).pvalue
    pvalueG3 = shapiroG3(df).pvalue
    st = df["studytime"]
    G3 = df["G3"]
    if pvalueG3 > 0.05 and pvalueST > 0.05:
        res_pearson = stats.pearsonr(G3, st)
        print("Pearson r:", res_pearson.statistic)
    else:
        res_spearman = stats.spearmanr(G3, st)
        print("Spearman rho:", res_spearman.statistic)
def anova_for_G3(df):
    G3 = df["G3"]
    st = df["studytime"]
    relationship = df["famrel"]
    abs = df["absences"]
    daily_alc = df["Dalc"] 
    Weekedn_alc = df["Walc"]
    Parents = df["Pstatus"]
    p_classes = df["paid"]

    

    