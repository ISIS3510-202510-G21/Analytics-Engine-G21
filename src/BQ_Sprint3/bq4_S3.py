import pandas as pd

def process_home_interactions(data):
    df = pd.DataFrame(data['home_interactions'])
    df_counts = (
        df.groupby(["interactionType"])  
        .size() 
        .reset_index(name='count')  
    )
    df_counts.rename(columns={'count': '# Interactions'}, inplace=True)
    df_counts=df_counts.sort_values(by="# Interactions", ascending=False)
    return df_counts