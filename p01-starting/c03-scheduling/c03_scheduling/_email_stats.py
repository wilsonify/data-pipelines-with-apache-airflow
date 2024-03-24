import pandas as pd


def _print_stats(stats: pd.DataFrame, email: str):
    """
    Pretend to send an email
    """
    print(f"stats.shape = {stats.shape}")
    print(f"We would like to sending stats to email={email}...")


def _print_stats_from_template(email, **context):
    """
    read stats from context, then
    Pretend to send an email
    """
    stats_path = context["templates_dict"]["stats_path"]
    stats_df = pd.read_csv(stats_path)
    print(f"stats_df.shape = {stats_df.shape}")
    print(f"We would like to sending stats to email={email}...")
