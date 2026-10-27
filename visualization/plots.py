import matplotlib.pyplot as plt
import numpy as np

# czy uczniowie, którzy poświęcają więcej czasu na naukę, osiągają lepsze oceny końcowe?

# kolumny: studytime, G3 (ocena końcowa)


def plot_studytime_vs_grades(df):
    grades_by_studytime = []

    for studytime in range(1, 5):
        grades = df[df["studytime"] == studytime]["G3"]
        grades_by_studytime.append(grades)

    labels = ["< 2h", "2-5h", "5-10h", "> 10h"]

    plt.figure(figsize=(9, 5))

    plt.boxplot(grades_by_studytime, tick_labels=labels)

    plt.title("Czas nauki a oceny końcowe")
    plt.xlabel("Tygodniowy czas nauki")
    plt.ylabel("Ocena końcowa z matematyki")
    plt.ylim(-1, 21)
    plt.grid(axis="y", alpha=0.3)

    plt.show()

# czy liczba nieobecności wpływa na oceny końcowe?

# kolumny: absences, G3

def plot_absences_vs_grades(df):
    plt.figure(figsize=(9, 5))

    plt.scatter(df["absences"], 
                df["G3"], 
                alpha=0.5,
                s=25)

    plt.title("Liczba nieobecności a ocena końcowa")
    plt.xlabel("Liczba nieobecności")
    plt.ylabel("Ocena końcowa z matematyki")
    plt.ylim(-1, 21)
    plt.grid(axis="y", alpha=0.3)

    plt.show()

# czy poziom wykształcenia matki i ojca wiąże się ze średnią oceną końcową ucznia?

# kolumny: Medu, Fedu, G3

def plot_parents_education(df):
    mother_avg = df.groupby("Medu")["G3"].mean().reindex(range(5))
    father_avg = df.groupby("Fedu")["G3"].mean().reindex(range(5))

    x = np.arange(5)
    width = 0.35

    plt.figure(figsize=(9, 5))

    plt.bar(x - width / 2, mother_avg, width=width, label="Matka")
    plt.bar(x + width / 2, father_avg, width=width, label="Ojciec")

    plt.title("Poziom wykształcenia rodziców a średnia ocena końcowa")
    plt.xlabel("Poziom wykształcenia rodzica")
    plt.ylabel("Średnia ocena końcowa z matematyki")

    labels = [
        "Brak",
        "Klasy 1-4",
        "Klasy 5–9",
        "Średnie",
        "Wyższe"
    ]

    plt.xticks(x, labels)
    plt.ylim(0, 20)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()

    # print(df["Medu"].value_counts().sort_index())
    # print(df["Fedu"].value_counts().sort_index())

    # są 3 osoby gdzie matka ma edukacje 0 i 2 gdzie ojciec


# czy poziom spożywania alkoholu w dni robocze i weekendy wiąże się ze średnią oceną końcową uczniów?

# kolumny: Dalc, Walc, G3

def plot_alcohol_vs_grades(df):
    dalc_avg = df.groupby("Dalc")["G3"].mean()
    walc_avg = df.groupby("Walc")["G3"].mean()

    x = np.arange(1,6)
    width = 0.35

    plt.figure(figsize=(9, 5))

    plt.bar(x - width / 2, dalc_avg, width=width, label="Dni robocze")
    plt.bar(x + width / 2, walc_avg, width=width, label="Weekend")

    plt.title("Poziom spożywania alkoholu w dni robocze i weekendy a średnia ocena końcowa")
    plt.xlabel("Poziom spożywania alkoholu")
    plt.ylabel("Średnia ocena końcowa z matematyki")

    labels = [
        "Bardzo niski",
        "Niski",
        "Średni",
        "Wysoki",
        "Bardzo wysoki"
    ]

    plt.xticks(x, labels)
    plt.ylim(0, 20)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()

# jak zmieniają się oceny uczniów w kolejnych okresach?

# kolumny: G1, G2, G3

def plot_grade_progress(df):
    averages = df[["G1", "G2", "G3"]].mean()

    plt.figure(figsize=(9, 5))

    plt.plot(averages.index, averages.values, marker="o")

    plt.title("Zmiany średnich ocen uczniów")
    plt.xlabel("Etap oceniania")
    plt.ylabel("Średnia ocena z matematyki")

    plt.ylim(0, 20)
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()