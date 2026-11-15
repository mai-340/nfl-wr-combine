"""
Name: Denny Nguyen, Gia-Hao Mai, Jacob So
CSE 163
Final Project: NFL WR Combine Analysis

Tests the filtering and merging functions created in eda.py
"""


import pandas as pd
from eda import filter_combine, add_gsis_id, add_rookie_stats


def make_combine():
    """
    Creates a small sample dataset of combine results.
    """
    combine = pd.DataFrame({
        'player_name': ['Player A', 'Player B', 'Player C'],
        'pos': ['WR', 'WR', 'QB'],
        'draft_year': [2020, 2021, 2020],
        'pfr_id': ['AAA', 'BBB', 'CCC'],
        'draft_round': [1, 2, 1],
        'draft_ovr': [10, 45, 5],
        'ht': ['6-0', '6-1', '6-2'],
        'wt': [200, 195, 220],
        'forty': [4.4, 4.5, 4.6],
        'bench': [10, 12, 15],
        'vertical': [35, 36, 33],
        'broad_jump': [120, 125, 115],
        'cone': [7.0, 7.1, 7.2],
        'shuttle': [4.1, 4.2, 4.3]
    })
    return combine


def make_draft():
    """
    Creates a small sample dataset of draft picks.
    """
    draft = pd.DataFrame({
        'pfr_player_id': ['AAA', 'BBB', 'CCC'],
        'gsis_id': ['001', '002', '003']
    })
    return draft


def make_stats():
    """
    Creates a small sample dataset of player stats.
    """
    stats = pd.DataFrame({
        'player_id': ['001', '001', '002', '003'],
        'season': [2020, 2021, 2021, 2020],
        'fantasy_points_ppr': [100, 200, 150, 250]
    })

    return stats


def test_filter_combine():
    """
    Tests that only wr are kept.
    """
    combine = make_combine()
    result = filter_combine(combine)

    assert len(result) == 2
    assert list(result['player_name']) == ['Player A', 'Player B']


def test_add_gsis_id():
    """
    Tests that wr draft pick data is merged correctly with their gsis id
    """
    combine = make_combine()
    draft = make_draft()

    wr = filter_combine(combine)
    result = add_gsis_id(wr, draft)

    assert len(result) == 2
    assert list(result['gsis_id']) == ['001', '002']


def test_add_rookie_stats():
    """
    Tests that only rookie season stats are kept
    """
    combine = make_combine()
    draft = make_draft()
    stats = make_stats()

    wr = filter_combine(combine)
    wr = add_gsis_id(wr, draft)
    result = add_rookie_stats(wr, stats)

    assert len(result) == 2
    assert list(result['fantasy_points_ppr']) == [100, 150]


def main():
    test_filter_combine()
    test_add_gsis_id()
    test_add_rookie_stats()
    print("All tests passes!")


if __name__ == '__main__':
    main()
