from utils.data_loader import load_data
from visualization.plots import *
from analysis.statistics import *
def main():
    df = load_data("data/student-mat.csv")
    print(df.head())
    # plot_studytime_vs_grades(df)
    # plot_absences_vs_grades(df)
    # plot_parents_education(df)
    # plot_alcohol_vs_grades(df)
    plot_grade_progress(df)

    print(avgG3(df))

if __name__ == "__main__":
    main()
