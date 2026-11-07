import warnings

import pandas as pd

from utils.validation import check_columns


def load_data(file_path):
    """Wczytuje plik UCI do DataFrame. Czyszczenie odbywa się osobno."""
    try:
        with warnings.catch_warnings():
            # Nie pozwalamy Pandas po cichu obciąć zbyt długiego wiersza.
            warnings.simplefilter("error", pd.errors.ParserWarning)
            with open(file_path, "r", encoding="utf-8-sig") as file:
                df = pd.read_csv(file, sep=";", na_values=["?"], index_col=False)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Nie znaleziono pliku: {file_path}") from error
    except pd.errors.EmptyDataError as error:
        raise ValueError("Plik jest pusty lub nie zawiera nagłówka.") from error
    except (pd.errors.ParserError, pd.errors.ParserWarning) as error:
        raise ValueError(
            "Niepoprawny CSV. Sprawdź średniki, cudzysłowy i liczbę pól."
        ) from error
    except UnicodeError as error:
        raise ValueError("Nie można odczytać pliku. Zapisz go jako UTF-8.") from error
    except OSError as error:
        raise OSError(f"Nie można otworzyć pliku: {file_path}") from error

    check_columns(df)
    if df.empty:
        raise ValueError("Plik zawiera nagłówek, ale nie ma danych uczniów.")
    return df
