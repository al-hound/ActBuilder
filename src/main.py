import pandas as pd
import dataManager as dm
import streamlit as st
import matplotlib.pyplot as plt
import os

def main():
    df = dm.read_notas()
    alumnos_list = dm.read_alumnos()
    
    st.title("Gestión de Notas de Alumnos")

    menu = ["Ingresar Nota", "Filtrar Notas", "Actualizar Nota", "Eliminar Nota", "Mostrar Todas las Notas", "Crear Alumno", "Mostrar Estadísticas"]
    choice = st.sidebar.selectbox("Menú", menu)

    if choice == "Ingresar Nota":
        st.subheader("Ingresar Nueva Nota")

        alumno = st.selectbox("Nombre del Alumno", alumnos_list)
        curso = st.text_input("Curso")
        materia = st.text_input("Materia")
        unidad_formativa = st.text_input("Unidad Formativa")
        nota_examen = st.number_input("Nota Examen", min_value=0.0, max_value=10.0, step=0.1)
        comp_claves = st.number_input("Competencias Claves", min_value=0.0, max_value=10.0, step=0.1)
        comp_tecnicas = st.number_input("Competencias Tecnicas", min_value=0.0, max_value=10.0, step=0.1)

        if st.button("Ingresar"):
            df = dm.add_student_data(df, alumno, curso, materia, unidad_formativa, nota_examen, comp_claves, comp_tecnicas)
            dm.save_excel(df, dm.notas_path)
            st.success("Nota ingresada correctamente")
    
    elif choice == "Filtrar Notas":
        st.subheader("Filtrar Notas")

        filtro = st.selectbox("Filtrar por", ["Alumno", "Curso", "Materia", "Unidad Formativa"])
        valor = st.text_input(f"Ingrese el valor para {filtro}")

        if st.button("Filtrar"):
            df_filtrado = dm.filter_data(df, filtro, valor)
            st.dataframe(df_filtrado)
    
    elif choice == "Actualizar Nota":
        st.subheader("Actualizar Nota")

        index = st.number_input("Índice de la nota a actualizar", min_value=0, max_value=len(df)-1, step=1)
        alumno = st.selectbox("Nombre del Alumno", alumnos_list, index=alumnos_list.index(df.at[index, 'Alumno']))
        curso = st.text_input("Curso", value=df.at[index, 'Curso'])
        materia = st.text_input("Materia", value=df.at[index, 'Materia'])
        unidad_formativa = st.text_input("Unidad Formativa", value=df.at[index, 'Unidad Formativa'])
        nota_examen = st.number_input("Nota Examen", value=df.at[index, 'Nota Examen'], min_value=0.0, max_value=10.0, step=0.1)
        comp_claves = st.number_input("Competencias Claves", value=df.at[index, 'Competencias Claves'], min_value=0.0, max_value=10.0, step=0.1)
        comp_tecnicas = st.number_input("Competencias Tecnicas", value=df.at[index, 'Competencias Tecnicas'], min_value=0.0, max_value=10.0, step=0.1)

        if st.button("Actualizar"):
            df = dm.update_student_data(df, index, alumno, curso, materia, unidad_formativa, nota_examen, comp_claves, comp_tecnicas)
            dm.save_excel(df, dm.notas_path)
            st.success("Nota actualizada correctamente")
    
    elif choice == "Eliminar Nota":
        st.subheader("Eliminar Nota")

        index = st.number_input("Índice de la nota a eliminar", min_value=0, max_value=len(df)-1, step=1)

        if st.button("Eliminar"):
            df = dm.delete_student_data(df, index)
            dm.save_excel(df, dm.notas_path)
            st.success("Nota eliminada correctamente")
    
    elif choice == "Mostrar Todas las Notas":
        st.subheader("Todas las Notas")
        st.dataframe(df)

    elif choice == "Crear Alumno":
        st.subheader("Crear Alumno")

        nuevo_alumno = st.text_input("Nombre del Nuevo Alumno")

        if st.button("Crear Alumno"):
            alumnos_list = dm.add_alumno(nuevo_alumno)
            st.success("Alumno creado correctamente")
            st.write("Lista de alumnos actualizada:")
            st.write(alumnos_list)

    elif choice == "Mostrar Estadísticas":
        st.subheader("Estadísticas de Notas")

        # Mostrar estadísticas de notas por alumno
        if st.checkbox("Mostrar medias de notas por alumno"):
            promedio_alumnos = df.groupby('Alumno').mean(numeric_only=True)
            st.dataframe(promedio_alumnos)
            fig, ax = plt.subplots()
            promedio_alumnos['Nota Total'].plot(kind='bar', ax=ax)
            ax.set_title('Media de Notas Totales por Alumno')
            ax.set_xlabel('Alumno')
            ax.set_ylabel('Nota Total')
            st.pyplot(fig)
        
        # Mostrar estadísticas de notas por materia
        if st.checkbox("Mostrar medias de notas por materia"):
            promedio_materias = df.groupby('Materia').mean(numeric_only=True)
            st.dataframe(promedio_materias)
            fig, ax = plt.subplots()
            promedio_materias['Nota Total'].plot(kind='bar', ax=ax)
            ax.set_title('Media de Notas Totales por Materia')
            ax.set_xlabel('Materia')
            ax.set_ylabel('Nota Total')
            st.pyplot(fig)
        
        # Mostrar estadísticas de notas por unidad formativa
        if st.checkbox("Mostrar medias de notas por unidad formativa"):
            promedio_unidades = df.groupby('Unidad Formativa').mean(numeric_only=True)
            st.dataframe(promedio_unidades)
            fig, ax = plt.subplots()
            promedio_unidades['Nota Total'].plot(kind='bar', ax=ax)
            ax.set_title('Media de Notas Totales por Unidad Formativa')
            ax.set_xlabel('Unidad Formativa')
            ax.set_ylabel('Nota Total')
            st.pyplot(fig)
        
        # Mostrar progreso de alumnos por unidad formativa
        if st.checkbox("Mostrar progreso de alumnos por unidad formativa"):
            alumno = st.selectbox("Seleccione un alumno", alumnos_list)
            df_alumno = df[df['Alumno'] == alumno].sort_values(by='Unidad Formativa')
            if not df_alumno.empty:
                fig, ax = plt.subplots()
                ax.plot(df_alumno['Unidad Formativa'], df_alumno['Nota Examen'], marker='o', label='Nota Examen')
                ax.plot(df_alumno['Unidad Formativa'], df_alumno['Competencias Claves'], marker='o', label='Competencias Claves')
                ax.plot(df_alumno['Unidad Formativa'], df_alumno['Competencias Tecnicas'], marker='o', label='Competencias Tecnicas')
                ax.plot(df_alumno['Unidad Formativa'], df_alumno['Nota Total'], marker='o', label='Nota Total')
                ax.set_title(f'Progreso de {alumno} por Unidad Formativa')
                ax.set_xlabel('Unidad Formativa')
                ax.set_ylabel('Notas')
                ax.legend()
                st.pyplot(fig)
            else:
                st.write("No se encontraron datos para el alumno seleccionado.")

if __name__ == '__main__':
    main()
