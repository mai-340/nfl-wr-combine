import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()


def load_stats(start: int, end: int) -> pd.DataFrame:
    """
    Loads and stacks regular season player stats from
    the start to the end (inclusive) returning one
    dataframe
    """
    stats = []
    for year in range(start, end + 1):
        df = pd.read_csv(f"data/stats_player_reg_{year}.csv")
        stats.append(df)
    return pd.concat(stats)


def filter_combine(combine: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the combine rows for WRs drafted between 2010 and 2025
    inclusive. Keeping only the columns needed for analysis.
    """
    is_wr = combine['pos'] == 'WR'

    within_years = (combine['draft_year'] >= 2010) & (combine['draft_year'] <= 2025)
    has_id = combine['pfr_id'].notnull()
    wr = combine[is_wr & within_years & has_id]
    columns = ['player_name', 'pfr_id', 'draft_year', 'draft_round',
                'draft_ovr', 'ht', 'wt', 'forty', 'bench', 'vertical', 'broad_jump',
                'cone', 'shuttle']
    return wr[columns]


def add_gsis_id(wr: pd.DataFrame, draft: pd.DataFrame) -> pd.DataFrame:
    """
    Merges the WR's with the draft picks data
    to attach each player's gsis_id. links to player stats
    data
    """
    
    ids = draft[['pfr_player_id', 'gsis_id']]
    ids = ids[ids['gsis_id'].notnull()]
    return wr.merge(ids, left_on='pfr_id', right_on='pfr_player_id', 
                    how='left')


def add_rookie_stats(wr: pd.DataFrame, stats: pd.DataFrame) -> pd.DataFrame:
    """
    Merges the WR's with their regular season stats and keeps only each 
    player's rookie season.
    """
    wr = wr.dropna(subset=['gsis_id'])
    
    small = stats[['player_id', 'season', 'fantasy_points_ppr']]
    small = small.dropna(subset=['player_id'])
    merged = wr.merge(
        small,
        left_on='gsis_id',
        right_on='player_id',
        how='left'
    )
    
    is_rookie = merged['season'] == merged['draft_year']
    return merged[is_rookie].copy()


def main():
    """
    Loads the combine, draft pick, and player stats datasets
    and prints their sizes and column names.
    """
    combine = pd.read_csv('data/combine.csv')
    draft = pd.read_csv('data/draft_picks.csv')
    stats = load_stats(2010, 2025)

    # print('combine shape:', combine.shape)
    # print(list(combine.columns))

    # print('draft shape:', draft.shape)
    # print(list(draft.columns))

    # print('stats shape:', stats.shape)
    # print(list(stats.columns))

    # print(stats['season_type'].unique())

    wr = filter_combine(combine)
    print('Drafted WRs: ', wr.shape)

    wr = add_gsis_id(wr, draft)
    print("After adding gsis_id: ", wr.shape)
    print('Missing gsis_id:', wr['gsis_id'].isnull().sum())

    wr = add_rookie_stats(wr, stats)
    print("With rookie stats: ", wr.shape)
    print(wr.head())

    print('Total rows:', len(wr))
    print('Unique players:', wr['pfr_id'].nunique())

    print('Duplicate player rows:',
      wr.duplicated(['pfr_id', 'draft_year']).sum())
  
    print('Missing values by column:')
    print(wr.isna().sum())

    print()
    print('Players by draft year:')
    print(wr['draft_year'].value_counts().sort_index())

    print()
    print('Duplicate player seasons in stats:')
    print(stats.duplicated(['player_id', 'season']).sum())

    #Seven-number Summaries
    #For draft_ovr, forty, bench, vertical,
    # broad_jump, cone, shuttle, and fantasy_points_ppr
    print(wr[['draft_ovr', 'forty', 'bench', 'vertical',
              'broad_jump', 'cone', 'shuttle',
              'fantasy_points_ppr']].describe())
    
    print('Players by draft round:')
    print(wr['draft_round'].value_counts().sort_index())

    sns.relplot(data=wr, x='draft_ovr', y='fantasy_points_ppr')
    plt.title('Draft Overall vs. Rookie Fantasy Points (PPR)')
    plt.xlabel('Draft Overall')
    plt.ylabel('Rookie Fantasy Points (PPR)')
    plt.savefig('plots/draft_ovr_vs_fantasy_points.png')

    sns.relplot(data=wr, x='forty', y='fantasy_points_ppr')
    plt.title('40 Yard Dash vs. Rookie Fantasy Points (PPR)')
    plt.xlabel('40 Yard Dash (seconds)')
    plt.ylabel('Rookie Fantasy Points (PPR)')
    plt.savefig('plots/forty_vs_fantasy_points.png')

    sns.relplot(data=wr, x='forty', y='draft_ovr')
    plt.title('40 Yard Dash vs. Draft Overall')
    plt.xlabel('40 Yard Dash (seconds)')
    plt.ylabel('Draft Overall')
    plt.savefig('plots/forty_vs_draft_ovr.png')

    sns.relplot(data=wr, x='vertical', y='fantasy_points_ppr')
    plt.title('Vertical Jump vs. Rookie Fantasy Points (PPR)')
    plt.xlabel('Vertical Jump (inches)')
    plt.ylabel('Rookie Fantasy Points (PPR)')
    plt.savefig('plots/vertical_vs_fantasy_points.png')



if __name__ == '__main__':
    main()