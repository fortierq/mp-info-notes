import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool

st.set_page_config(layout="wide")
# st.title("Notes d'informatique en MP2I")

col1, col2 = st.columns(2)
width = 400
url = "https://raw.githubusercontent.com/fortierq/notes-mp2i/master/grade.csv"

df = pd.read_csv("grade.csv", index_col="id")
ranks = list(range(1, len(df) + 1))

with col2:
    student = st.selectbox("", df.index.sort_values())
    df_student = df.loc[[student], ::-1].dropna(axis=1)
    fig_line = figure(
        toolbar_location=None,
        title=f"Notes élève n°{student}",
        height=350,
        width=width,
        y_axis_label="Note",
        x_axis_label=f"Moyenne : {df_student.iloc[0, :].mean():.2f}",
        y_range=(0, 20),
    )
    fig_line.line(list(range(len(df.columns))), df_student.iloc[0], line_width=2)
    x = list(range(len(df_student.columns)))  # TODO : fix warning
    fig_line.xaxis.ticker = x
    fig_line.xaxis.major_label_overrides = {i: df_student.columns[i] for i in x}
    st.bokeh_chart(fig_line)

with col1:
    ds = st.selectbox('', df.columns)
    df_sort = df.sort_values(by=ds, ascending=False)
    df_sort["eleves"] = df_sort.index
    df_sort["rang"] = ranks
    df_sort["note"] = df_sort[ds]
    p = figure(toolbar_location=None,
               title=f"Classement {ds}\nMoyenne : {df[ds].mean():.2f}, Écart-type : {df[ds].var()**.5:.2f}",
               height=350,
               width=width,
               x_axis_label="Rang",
               y_axis_label="Note",
               tooltips=[("Élève n°", "@eleves"), ("Note", "@note"), ("Rang", "@rang")])
    p.vbar(x="rang", top=ds, width=0.9, source=df_sort)
    st.bokeh_chart(p)

st.markdown("""---""")

df["mean"] = df.mean(axis=1)
df["eleves"] = df.index
df.sort_values(by="mean", ascending=False, inplace=True)
df["rang"] = ranks
fig_mean = figure(
    toolbar_location=None,
    title=f"Classement général\nMoyenne de classe : {df['mean'].mean():.2f}, Écart-type : {df['mean'].var()**.5:.2f}",
    height=350,
    width=int(2.35 * width),
    x_axis_label="Rang",
    y_axis_label="Note",
    tooltips=[("Élève n°", "@eleves"), ("Moyenne", "@mean"), ("Rang", "@rang")])
fig_mean.vbar(x="rang", source=df, top="mean", width=0.9)
st.bokeh_chart(fig_mean)
