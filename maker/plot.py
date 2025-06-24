# script: generar_plots.py

import plotly.express as px
import plotly.graph_objects as go
import os

# Directorio donde se guardarán los HTML
output_dir = "source/_static"

# Crea el directorio si no existe
os.makedirs(output_dir, exist_ok=True)

# Primer plot: gráfico de líneas
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=[1, 2, 3, 4, 5],
    y=[10, 15, 13, 17, 22],
    mode='lines+markers',
    name='Serie 1'
))
fig1.update_layout(title="Gráfico de líneas")

# Segundo plot: gráfico de barras
df = px.data.tips()
fig2 = px.bar(df, x="day", y="total_bill", color="sex", barmode="group", title="Facturación por día y sexo")



# Guarda los plots como HTML
fig1.write_html(os.path.join(output_dir, "plot1.html"))
fig2.write_html(os.path.join(output_dir, "plot2.html"))

import plotly.graph_objects as go

fig = go.Figure(go.Scatter(x=[1,2,3], y=[4,1,2], mode='lines+markers'))

html_str = fig.to_html(full_html=False, include_plotlyjs='cdn')

# Now add a script that attaches dblclick to the plot div

# The plot div usually has id="..." inside the html_str, so we can wrap it in a container with id:

html_with_dblclick = f'''
<div id="my-plot-container">
{html_str}
</div>

<script>
document.getElementById('my-plot-container').addEventListener('click', function() {{
    window.location.href = "file:///wsl.localhost/Ubuntu/home/vic/interfaz/build/html/data/Bacteria/Proteobacteria/Gammaproteobacteria/Enterobacterales/Enterobacteriaceae/Escherichia/Escherichia%20coli/index.html";
}});
</script>
'''

with open("source/_static/plot3.html", "w") as f:
    f.write(html_with_dblclick)
    
print("Plots generados en:", output_dir)
