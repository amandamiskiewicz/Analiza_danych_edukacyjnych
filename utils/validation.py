import pandas as pd


GRADE_COLUMNS = ["G1", "G2", "G3"]
REQUIRED_COLUMNS = [
    "school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu",
    "Mjob", "Fjob", "reason", "guardian", "traveltime", "studytime", "failures",
    "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet",
    "romantic", "famrel", "freetime", "goout", "Dalc", "Walc", "health",
    "absences", "G1", "G2", "G3",
]


def check_columns(df):
    """Sprawdza, czy tabela zawiera wszystkie 33 kolumny zbioru UCI."""
    if not df.columns.is_unique:
        raise ValueError("Nazwy kolumn nie mogą się powtarzać.")
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(
            "Brakuje kolumn: " + ", ".join(missing)
            + ". Sprawdź nagłówek i separator CSV (średnik)."
        )


def find_invalid_values(df):
    """Zwraca tabelę True/False: True oznacza błędną lub brakującą wartość."""
    check_columns(df)
    invalid = pd.DataFrame(index=df.index)

    for column in GRADE_COLUMNS:
        values = pd.to_numeric(df[column], errors="coerce")
        valid = (values.between(0, 20) & (values % 1 == 0)).fillna(False)
        invalid[column] = ~valid

    studytime = pd.to_numeric(df["studytime"], errors="coerce")
    invalid["studytime"] = ~studytime.isin([1, 2, 3, 4])
    invalid["sex"] = ~df["sex"].isin(["F", "M"])
    return invalid


def validate_data(df):
    """Zwraca podsumowanie problemów, nie zmieniając danych."""
    invalid = find_invalid_values(df)
    missing = df.isna()
    for column in df.select_dtypes(include=["object", "string"]).columns:
        blank = df[column].map(
            lambda value: isinstance(value, str) and value.strip() in ("", "?")
        )
        missing[column] = missing[column] | blank

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": missing.sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "invalid_values": invalid.sum().to_dict(),
        "invalid_rows": int(invalid.any(axis=1).sum()),
    }
