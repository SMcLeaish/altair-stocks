import altair as alt
import polars as pl

alt.theme.enable('dark')
def candlestick(df: pl.DataFrame, title: str | None): 
    if title is None:
        title = ''
    open_close_color = (
        alt.when('datum.Open <= datum.Close')
        .then(alt.value('green'))
        .otherwise(alt.value('crimson'))
    )
    base = alt.Chart(df).encode(
        alt.X('Time:T', title=''),
        color=open_close_color
    )
    rule = base.mark_rule().encode(
        alt.Y('Low:Q')
        .title('Price')
        .scale(zero=False),
        alt.Y2('High:Q')
    )
    bar = base.mark_bar().encode(
        alt.Y('Open:Q'),
        alt.Y2('Close:Q')
    )

    return (rule + bar).properties(width=600, title=title)

def line(df: pl.DataFrame, title: str | None):
    if title is None:
        title = ''
    return alt.Chart(df).mark_line().encode(
        alt.X('Date:T', title=''),
        alt.Y('Close:Q').scale(zero=False)).properties(
            title=title, width=600
        )