import pandas as pd
import os

notas_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'notas.xlsx')
alumnos_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'alumnos.xlsx')

def save_excel(df, path):
    df.to_excel(path, index=False)

def read_excel(path):
    if not os.path.exists(path):
        if path == alumnos_path:
            df = pd.DataFrame(columns=['Alumno'])
        else:
            df = pd.DataFrame(columns=[
                'Alumno', 'Curso', 'Materia', 'Unidad Formativa', 
                'Nota Examen', 'Competencias Claves', 'Competencias Tecnicas', 'Nota Total'
            ])
    else:
        df = pd.read_excel(path)
    return df

def read_notas():
    return read_excel(notas_path)

def read_alumnos():
    return read_excel(alumnos_path)['Alumno'].tolist()

def add_alumno(alumno):
    df = read_excel(alumnos_path)
    if alumno not in df['Alumno'].values:
        nuevo_alumno = pd.DataFrame({'Alumno': [alumno]})
        df = pd.concat([df, nuevo_alumno], ignore_index=True)
        save_excel(df, alumnos_path)
    return df['Alumno'].tolist()

def filter_data(df, col, value):
    return df[df[col] == value]

def calculate_total(nota_examen, comp_claves, comp_tecnicas):
    return (nota_examen * 0.6) + (comp_tecnicas * 0.3) + (comp_claves * 0.1)

def add_student_data(df, alumno, curso, materia, unidad_formativa, nota_examen, comp_claves, comp_tecnicas):
    nota_total = calculate_total(nota_examen, comp_claves, comp_tecnicas)
    nueva_nota = {
        'Alumno': alumno,
        'Curso': curso,
        'Materia': materia,
        'Unidad Formativa': unidad_formativa,
        'Nota Examen': nota_examen,
        'Competencias Claves': comp_claves,
        'Competencias Tecnicas': comp_tecnicas,
        'Nota Total': nota_total
    }
    nuevo_df = pd.DataFrame([nueva_nota])
    df = pd.concat([df, nuevo_df], ignore_index=True)
    return df

def update_student_data(df, index, alumno, curso, materia, unidad_formativa, nota_examen, comp_claves, comp_tecnicas):
    if index in df.index:
        nota_total = calculate_total(nota_examen, comp_claves, comp_tecnicas)
        df.loc[index, 'Alumno'] = alumno
        df.loc[index, 'Curso'] = curso
        df.loc[index, 'Materia'] = materia
        df.loc[index, 'Unidad Formativa'] = unidad_formativa
        df.loc[index, 'Nota Examen'] = nota_examen
        df.loc[index, 'Competencias Claves'] = comp_claves
        df.loc[index, 'Competencias Tecnicas'] = comp_tecnicas
        df.loc[index, 'Nota Total'] = nota_total
    return df

def delete_student_data(df, index):
    if index in df.index:
        df = df.drop(index)
        df = df.reset_index(drop=True)  # Resetear el índice después de eliminar
    return df
