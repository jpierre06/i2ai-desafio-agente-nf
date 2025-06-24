import pandas as pd
import zipfile
import io # Necessário para ler o conteúdo do arquivo ZIP como um stream

def get_csv_content(zip_file_path: str, csv_filename_in_zip: str = None) -> pd.DataFrame:
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as z:
            # Se nenhum nome de arquivo CSV for especificado, encontre o primeiro .csv
            if csv_filename_in_zip is None:
                csv_files = [f for f in z.namelist() if f.lower().endswith('.csv')]
                if not csv_files:
                    return f"Erro: Nenhum arquivo CSV encontrado dentro de '{zip_file_path}'."
                csv_filename_in_zip = csv_files[0]
                print(f"Nenhum nome de CSV especificado. Usando o primeiro encontrado: '{csv_filename_in_zip}'")

            # Verifique se o arquivo CSV especificado existe no ZIP
            if csv_filename_in_zip not in z.namelist():
                return (f"Erro: O arquivo '{csv_filename_in_zip}' não foi encontrado dentro de '{zip_file_path}'. "
                        f"Arquivos disponíveis no ZIP: {', '.join(z.namelist())}")

            # Abra o arquivo CSV dentro do ZIP
            with z.open(csv_filename_in_zip, 'r') as f:
                df = pd.read_csv(io.StringIO(f.read().decode('utf-8')))
                return df

    except FileNotFoundError:
        return f"Erro: O arquivo ZIP '{zip_file_path}' não foi encontrado."
    except zipfile.BadZipFile:
        return f"Erro: O arquivo '{zip_file_path}' não é um arquivo ZIP válido ou está corrompido."
    except pd.errors.EmptyDataError:
        return f"Erro: O arquivo CSV '{csv_filename_in_zip}' dentro de '{zip_file_path}' está vazio."
    except Exception as e:
        return f"Ocorreu um erro inesperado ao processar '{zip_file_path}': {e}"