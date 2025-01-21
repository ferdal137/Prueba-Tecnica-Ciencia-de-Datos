import plotly.express as px
import pandas as pd

class Graficador:
    def __init__(self, data):
        self.data = data

    
    def generar_grafica_barras_univariado(self, columna):
        # Verificamos si es númerica la columna y la convertimos
        if self.data[columna].apply(lambda x: str(x).replace('.', '', 1).isdigit() if pd.notnull(x) else False).all():
            self.data[columna] = pd.to_numeric(self.data[columna])

        # Generamos el self.data a graficar
        self.data_conteo = self.data[columna].value_counts().reset_index().sort_values(columna).reset_index(drop=True)
        total = self.data_conteo['count'].sum()
        self.data_conteo['percentage'] = (self.data_conteo['count'] / total * 100).round(2)
        self.data_conteo['text'] = self.data_conteo['count'].astype(str) + ' (' + self.data_conteo['percentage'].astype(str) + '%)'

        # Generamos la gráfica
        fig = px.bar(self.data_conteo, x=columna, y='count', text='text', title=f'Número de reservaciones por {columna}')

        # Personalizamos la barras y el texto
        fig.update_traces(marker_color='#FF6F61', textfont_size=12,textposition='outside')

        # Personalizamos el fondo y diseño general 
        fig.update_layout(
        plot_bgcolor='#222222',  # Fondo negro de la gráfica
        paper_bgcolor='#222222',  # Fondo negro de todo el gráfico
        font=dict(color='white', size=14),  # Texto en blanco
        xaxis=dict(gridcolor='#444444'),  # Cuadrícula en gris claro
        yaxis=dict(gridcolor='#444444'),  
        title=dict(font=dict(size=18)),  # Tamaño del título
        xaxis_title=columna, 
        yaxis_title=columna)

        # Actualizamos el alto de la gráfica
        fig.update_layout(yaxis=dict(range=[0, self.data_conteo['count'].max() * 1.2]))
        fig.update_xaxes(tickmode='linear')

        # Modificamos el alto si solo se tienen dos columnas
        if self.data_conteo.shape[0] == 2:
            fig.update_layout(width=600) 
        else: 
            # Agregar fuente
            fig.add_annotation( text="Fuente: Datos originales", xref="paper", yref="paper", x=0, y=-0.15, showarrow=False, font=dict(color='white', size=12))
        

        return fig
    


    def generar_grafico_violin_bivariado(self, columna_x, columna_y):

        fig = px.violin(self.data, x=columna_x, y=columna_y, box=True, title=f"{columna_x} por {columna_y}")

        # Modificamos el color de las cajas y las líneas
        fig.update_traces(line_color='#4DB6AC', fillcolor='#80CBC4',box_line_color='#004D40', meanline_color='#004D40', marker=dict(color='white', size=6))

        # Personalizamos el fondo y diseño general
        fig.update_layout(
        plot_bgcolor='#222222',  # Fondo negro de la gráfica
        paper_bgcolor='#222222',  # Fondo negro del papel
        font=dict(color='white', size=14),  # Texto blanco
        xaxis=dict(gridcolor='#444444'),  # Cuadrícula gris claro
        yaxis=dict(gridcolor='#444444'),
        title=dict(font=dict(size=18)),  # Tamaño del título
        xaxis_title=columna_x, 
        yaxis_title=columna_y)

        # Añadimos la fuente
        fig.add_annotation(
        text="Fuente: Datos originales", xref="paper", yref="paper", x=0, y=-0.15, showarrow=False, font=dict(color='white', size=12))
        
        return fig
    



    def generar_grafico_barras_apiladas_bivariado(self, column_x, column_y):

        # Creamos la grafica
        fig = px.histogram(self.data, x=column_x, color=column_y, barmode='stack', 
                            title=f"Distribución de {column_x} por {column_y}",
                            color_discrete_sequence=["#388E3C", "#81C784"], text_auto=True)
        
        # Personalizamos el fondo y diseño general
        fig.update_layout(
        plot_bgcolor='#222222',  # Fondo negro de la gráfica
        paper_bgcolor='#222222',  # Fondo negro del papel
        font=dict(color='white', size=14),  # Texto blanco
        xaxis=dict(gridcolor='#444444'),  # Cuadrícula gris claro
        yaxis=dict(gridcolor='#444444'),
        title=dict(font=dict(size=18)),  # Tamaño del título
        xaxis_title=column_x, 
        yaxis_title=column_y)

        # Modificamos el alto si solo se tienen dos columnas
        if self.data[column_x].nunique() == 2:
            fig.update_layout(width=600) 
        else:
            # Agregar una anotación de fuente
            fig.add_annotation(text="Fuente: Datos originales", xref="paper", yref="paper", x=0, y=-0.15, showarrow=False, font=dict(color='white', size=12))
        

        return fig
    


    def generar_grafica_dispersion_bivariado(self, columna_x, columna_y, color):

        # Crear el gráfico de dispersión
        fig = px.scatter(self.data, x=columna_x, y=columna_y, color=color, title=f"{columna_x} vs {columna_y} por {color}")
        
        # Personalizar el fondo y diseño general
        fig.update_layout(
            plot_bgcolor='#222222',  # Fondo negro de la gráfica
            paper_bgcolor='#222222',  # Fondo negro del papel
            font=dict(color='white', size=14),  # Texto blanco
            xaxis=dict(gridcolor='#444444'),  # Cuadrícula gris claro para el eje X
            yaxis=dict(gridcolor='#444444'), 
            title=dict(font=dict(size=18)))  # Tamaño del título

        # Agregar una anotación de fuente
        fig.add_annotation(text="Fuente: Datos originales",  xref="paper", yref="paper", x=0, y=-0.15, showarrow=False, font=dict(color='white', size=12))

        return fig