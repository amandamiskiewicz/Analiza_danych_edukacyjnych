import pandas as pd

from utils.validation import GRADE_COLUMNS, check_columns, find_invalid_values


def clean_data(df):
    """Usuwa niepełne i niepoprawne rekordy oraz dokładne duplikaty."""
    check_columns(df)
    cleaned = df.copy()

    for column in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[column] = cleaned[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
    cleaned = cleaned.replace(["", "?"], pd.NA)

    for column in GRADE_COLUMNS + ["studytime"]:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    # Zera są ocenami. Nie uzupełniamy braków zerem ani średnią.
    cleaned = cleaned.dropna()
    invalid = find_invalid_values(cleaned)
    cleaned = cleaned.loc[~invalid.any(axis=1)].copy()
    cleaned = cleaned.drop_duplicates()

    if cleaned.empty:
        raise ValueError("Po czyszczeniu nie pozostał żaden poprawny rekord.")

    for column in GRADE_COLUMNS + ["studytime"]:
        cleaned[column] = cleaned[column].astype(int)
    return cleaned.reset_index(drop=True)


def filter_students(df, min_grade=0, max_grade=20, sex=None, studytime=None):
    """Filtruje oczyszczone dane według G3, płci i kategorii czasu nauki."""
    check_columns(df)
    try:
        min_grade = float(min_grade)
        max_grade = float(max_grade)
    except (ValueError, TypeError, OverflowError) as error:
        raise ValueError("Granice ocen muszą być liczbami.") from error

    if not 0 <= min_grade <= max_grade <= 20:
        raise ValueError("Zakres ocen musi spełniać: 0 <= minimum <= maksimum <= 20.")
    if sex not in (None, "F", "M"):
        raise ValueError("Płeć musi być oznaczona jako F lub M.")
    if studytime is not None and studytime not in (1, 2, 3, 4):
        raise ValueError("Czas nauki musi być kategorią 1, 2, 3 lub 4.")

    selected = df["G3"].between(min_grade, max_grade)
    if sex is not None:
        selected &= df["sex"] == sex
    if studytime is not None:
        selected &= df["studytime"] == studytime
    return df.loc[selected].copy()


def sort_students(df, column="G3", ascending=False):
    """Sortuje dane; domyślnie od najwyższej oceny końcowej."""
    if column not in df.columns:
        raise ValueError(f"Nie ma kolumny: {column}")
    if not isinstance(ascending, bool):
        raise ValueError("Parametr ascending musi mieć wartość True lub False.")
    return df.sort_values(
        by=column, ascending=ascending, kind="stable"
    ).reset_index(drop=True)


def iter_batches(df, batch_size=100):
    """Zwraca kolejne partie wierszy z już wczytanego DataFrame."""
    if isinstance(batch_size, bool) or not isinstance(batch_size, int):
        raise ValueError("Wielkość partii musi być dodatnią liczbą całkowitą.")
    if batch_size <= 0:
        raise ValueError("Wielkość partii musi być większa od zera.")

    for start in range(0, len(df), batch_size):
        yield df.iloc[start:start + batch_size].copy()
